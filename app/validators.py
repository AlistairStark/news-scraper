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