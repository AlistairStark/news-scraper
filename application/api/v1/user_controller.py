from dataclasses import dataclass
from werkzeug.exceptions import Forbidden
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from marshmallow.schema import Schema

from application.decorators.validation import validate_payload
from application.services.user_service import UserService
from config import Config


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


class CreateUser(Resource):
    @validate_payload(CreateUserSchema, CreateUserEmailPassword)
    def post(self, body: UserEmailPassword):
        if body.create_secret != Config().CREATE_SECRET:
            raise Forbidden("Get outta here!")
        return UserService().create_user(body)

    @jwt_required()
    def get(self):
        return "SUCCESS"


class LoginUserSchema(UserSchema):
    pass


class LoginUser(Resource):
    @validate_payload(LoginUserSchema, UserEmailPassword)
    def post(self, body: UserEmailPassword):
        token = UserService().login(body)
        return jsonify(token=token)
