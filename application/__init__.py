import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

import logging

db = SQLAlchemy()
jwt = JWTManager()

CONFIG = os.getenv("FLASK_CONFIG", "config.DevelopmentConfig")

logging.basicConfig(
    # filename="record.log",
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


def init_app():
    app = Flask("main")
    app.config.from_object(CONFIG)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from application.managers.bcrypt import init_bcrypt
        from application import helpers

        from application.api.v1 import bp as v1_bp

        app.register_blueprint(v1_bp)
        init_bcrypt(app)

    return app
