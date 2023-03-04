import os
from datetime import timedelta


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@postgres/postgres"
    )
    REDIS_URL = os.environ.get("CELERY_BROKER_URL")
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CREATE_SECRET = os.environ.get("CREATE_SECRET", "")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
