from typing import List
from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    password: str


class CreateUserSchema(UserSchema):
    create_secret: str


class CreateSearchSchema(BaseModel):
    name: str
    description: str
    is_rss: bool


class UpdateSearchSchema(CreateSearchSchema):
    id: int


class CreateSearchTermsSchema(BaseModel):
    terms: List[str]
    search_id: int


class SearchSchema(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    is_rss: bool

    class Config:
        orm_mode = True


class SearchTermsSchema(BaseModel):
    id: int
    term: str

    class Config:
        orm_mode = True