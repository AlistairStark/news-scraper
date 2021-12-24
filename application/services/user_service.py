from __future__ import annotations

from typing import TYPE_CHECKING

from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, Forbidden

from application import db, models

if TYPE_CHECKING:
    from application.api.v1.user_controller import UserEmailPassword


class UserService(object):
    def create_user(self, body: UserEmailPassword):
        user = models.User()
        user.create_user(body.email, body.username, body.password)
        db.session.add(user)
        db.session.commit()

    def login(self, body: UserEmailPassword):
        user: models.User = models.User.query.filter_by(email=body.email).one_or_none()
        if not user:
            raise BadRequest(f"User with email {body.email} not found")
        password_is_valid = user.check_password(body.password)
        if not password_is_valid:
            raise Forbidden("incorrect email or password")
        return create_access_token(identity=user.email)
