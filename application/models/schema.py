from __future__ import annotations

from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import Boolean

from application.managers.bcrypt import bcrypt
from application.models.helpers import Base, CreatedAtUpdatedAtMixin


class User(CreatedAtUpdatedAtMixin, Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)

    searches: RelationshipProperty[List["Search"]] = relationship(
        "Search",
        back_populates="user",
        cascade="all, delete",
    )

    def hash_password(self):
        password = bcrypt.generate_password_hash(self.password, 10)
        self.password = password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def create_user(self, email: str, password: str):
        self.email = email
        self.password = password
        self.hash_password()


class Search(CreatedAtUpdatedAtMixin, Base):

    __tablename__ = "search"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user: RelationshipProperty["User"] = relationship("User", back_populates="searches")

    search_terms: RelationshipProperty[List["SearchTerm"]] = relationship(
        "SearchTerm",
        back_populates="search",
        cascade="all, delete",
        passive_deletes=True,
    )

    search_locations: RelationshipProperty[List["SearchLocation"]] = relationship(
        "SearchLocation",
        back_populates="search",
        cascade="all, delete",
        passive_deletes=True,
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "search_terms": [t.serialize() for t in self.search_terms],
            "search_locations": [t.serialize() for t in self.search_locations],
        }


class SearchTerm(CreatedAtUpdatedAtMixin, Base):

    __tablename__ = "search_term"

    id = Column(Integer, primary_key=True)
    term = Column(String(50), nullable=False)
    search_id = Column(
        Integer, ForeignKey("search.id", ondelete="CASCADE"), nullable=False
    )

    search: RelationshipProperty["Search"] = relationship(
        "Search", back_populates="search_terms"
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "term": self.term,
        }


class SearchLocation(CreatedAtUpdatedAtMixin, Base):

    __tablename__ = "search_location"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    url = Column(String, nullable=False)
    search_id = Column(
        Integer, ForeignKey("search.id", ondelete="CASCADE"), nullable=False
    )

    search: RelationshipProperty["Search"] = relationship(
        "Search", back_populates="search_locations"
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        }


class Result(CreatedAtUpdatedAtMixin, Base):

    __tablename__ = "result"

    __table_args__ = (
        UniqueConstraint(
            "link",
            "search_id",
            name="unique_link_search",
        ),
    )

    id = Column(Integer, primary_key=True)
    agency = Column(String(50), nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    search_id = Column(
        Integer, ForeignKey("search.id", ondelete="CASCADE"), nullable=False
    )

    search: RelationshipProperty["Search"] = relationship("Search")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "agency": self.agency,
            "title": self.title,
            "link": self.link,
            "search_id": self.search_id,
        }
