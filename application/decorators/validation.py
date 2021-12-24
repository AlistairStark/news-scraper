from functools import wraps
from typing import Optional

from flask import request
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema
from werkzeug.exceptions import BadRequest


def validate_payload(
    validation_class: Optional[Schema],
    dataclass: Optional[object] = None,
    validate_params=False,
    validate_body=True,
):
    def real_decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                data = {}
                if validate_params:
                    data = validation_class().load(request.args)
                if validate_body:
                    data = validation_class().load(request.get_json())
                if dataclass:
                    data = dataclass(**data)
            except ValidationError as e:
                raise BadRequest(str(e))
            return method(args[0], data, **kwargs)

        return wrapper

    return real_decorator
