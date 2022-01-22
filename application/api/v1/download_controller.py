from flask_jwt_extended.view_decorators import jwt_required
from flask import Blueprint
from dataclasses import dataclass
from marshmallow import fields

from marshmallow.schema import Schema

from application.services.download_service import DownloadService
from application.services.validate_service import deserialize_body

bp = Blueprint("download", __name__)


class DownloadCsvBody(Schema):
    ids = fields.List(fields.Integer, required=True)
    search_id = fields.Integer(required=True)


@dataclass
class DownloadCsvData:
    ids: int
    search_id: int


@jwt_required()
@bp.post("/download-csv")
def download_csv():
    body: DownloadCsvData = deserialize_body(DownloadCsvBody, DownloadCsvData)
    return DownloadService().download_csv(body.ids, body.search_id)
