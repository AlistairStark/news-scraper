import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from application.worker import init_celery

db = SQLAlchemy()
jwt = JWTManager()

CONFIG = os.getenv("FLASK_CONFIG", "config.DevelopmentConfig")


def init_app():
    app = Flask("main")
    api = Api(app)
    app.config.from_object(CONFIG)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    jwt.init_app(app)

    # register sse endpoint
    app.register_blueprint(sse, url_prefix="/stream")

    with app.app_context():
        from application.api.v1.routes import init_routes
        from application.managers.bcrypt import init_bcrypt
        from application import helpers

        init_bcrypt(app)
        init_routes(api)
        init_celery(app)

    return app
