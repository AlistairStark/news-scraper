from datetime import datetime
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


class LocationSchema(BaseModel):
    name: str
    url: str


class CreateSearchLocationsSchema(BaseModel):
    locations: List[LocationSchema]
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


class SearchLocationsSchema(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class SearchWithTermsLocations(SearchSchema):
    search_terms: List[SearchTermsSchema]
    search_locations: List[SearchLocationsSchema]


class ResultsSchema(BaseModel):
    id: int
    agency: str
    deleted: bool
    link: str
    title: str
    search_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ResultsListSchema(BaseModel):
    links: List[ResultsSchema]
