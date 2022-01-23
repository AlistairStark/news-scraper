from dataclasses import dataclass

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import fields
from marshmallow.schema import Schema
from werkzeug.exceptions import Forbidden

from application.services.user_service import UserService
from application.services.validate_service import deserialize_body
from config import Config

bp = Blueprint("user", __name__)


class UserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class CreateUserSchema(UserSchema):
    create_secret = fields.String(required=True)


@dataclass
class UserEmailPassword:
    email: str
    password: str


@dataclass
class CreateUserEmailPassword(UserEmailPassword):
    create_secret: str


@bp.post("/user/create")
def post_user_create():
    body: CreateUserEmailPassword = deserialize_body(
        CreateUserSchema, CreateUserEmailPassword
    )
    if body.create_secret != Config().CREATE_SECRET:
        raise Forbidden("Get outta here!")
    UserService().create_user(body)
    return "", 201


@bp.get("/user/create")
@jwt_required()
def get_user_create():
    return "SUCCESS", 200


class LoginUserSchema(UserSchema):
    pass


@bp.post("/user/login")
def post_user_login():
    body: UserEmailPassword = deserialize_body(LoginUserSchema, UserEmailPassword)
    token = UserService().login(body)
    return jsonify(token=token)
