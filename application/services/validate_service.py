from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest


def deserialize(data_to_validate, validation_class, dataclass):
    try:
        data = validation_class().load(data_to_validate)
        if dataclass:
            data = dataclass(**data)
    except ValidationError as e:
        raise BadRequest(str(e))
    return data


def deserialize_body(validation_class, dataclass=None):
    """Deserialize flask request body"""
    return deserialize(request.get_json(), validation_class, dataclass)


def deserialize_params(validation_class, dataclass=None):
    """Deserialize flask request params"""
    return deserialize(request.args.to_dict(), validation_class, dataclass)
