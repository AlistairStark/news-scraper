from dataclasses import dataclass

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from marshmallow.schema import Schema

from application.decorators.validation import validate_payload
from application.services.user_service import UserService


class CreateUserSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


@dataclass
class UserEmailPassword:
    email: str
    password: str


class CreateUser(Resource):
    @validate_payload(CreateUserSchema, UserEmailPassword)
    def post(self, body: UserEmailPassword):
        return UserService().create_user(body)

    @jwt_required()
    def get(self):
        return "SUCCESS"


class LoginUserSchema(CreateUserSchema):
    pass


class LoginUser(Resource):
    @validate_payload(LoginUserSchema, UserEmailPassword)
    def post(self, body: UserEmailPassword):
        token = UserService().login(body)
        return jsonify(token=token)
