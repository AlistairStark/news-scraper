from application import jwt, models


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return models.User.query.filter_by(email=identity).one_or_none()