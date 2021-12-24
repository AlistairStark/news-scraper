from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_bcrypt(app):
    bcrypt = Bcrypt(app)
