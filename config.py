from datetime import timedelta
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@server-postgres-1/postgres"
    )
    REDIS_URL = os.environ.get("CELERY_BROKER_URL")
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "1234")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "2345")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
