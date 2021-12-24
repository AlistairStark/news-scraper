from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from dataclasses import dataclass
from marshmallow import fields

from marshmallow.schema import Schema

from application.decorators.validation import validate_payload
from application.services.download_service import DownloadService


class DownloadCsvBody(Schema):
    ids = fields.List(fields.Integer, required=True)
    search_id = fields.Integer(required=True)


@dataclass
class DownloadCsvData:
    ids: int
    search_id: int


class DownloadCsv(Resource):
    @jwt_required()
    @validate_payload(DownloadCsvBody, DownloadCsvData)
    def post(self, body: DownloadCsvData):
        return DownloadService().download_csv(body.ids, body.search_id)
