from datetime import datetime

from sqlalchemy import DECIMAL, TIMESTAMP, Column, func


def make_decimal():
    return DECIMAL(asdecimal=True)


def make_timestamptz():
    return TIMESTAMP(timezone=True)


class CreatedAtMixin:
    created_at = Column(
        "created_at",
        make_timestamptz(),
        server_default=func.current_timestamp(),
        nullable=False,
        doc="Time at which the row was created.",
    )


class UpdatedAtMixin:
    updated_at = Column(
        "updated_at",
        make_timestamptz(),
        server_default=func.current_timestamp(),
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Time at which the row was updated.",
    )


class CreatedAtUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
