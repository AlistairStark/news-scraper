from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource
from dataclasses import dataclass
from marshmallow import fields

from marshmallow.schema import Schema

from application.decorators.validation import validate_payload
from application.services.search_service import SearchService

from flask_jwt_extended import current_user

from application.services.scraper_service import ScraperService


class GetScrapeParam(Schema):
    search_id = fields.Integer(required=True)
    include_previous = fields.Boolean(required=True)


@dataclass
class GetScrapeData:
    search_id: int
    include_previous: bool


class Scrape(Resource):
    @jwt_required()
    @validate_payload(
        GetScrapeParam,
        GetScrapeData,
        validate_body=False,
        validate_params=True,
    )
    def get(self, params: GetScrapeData):
        search = SearchService().get_search(current_user.id, params.search_id)
        if search.is_rss:
            results = ScraperService(search).scrape_all(params.include_previous)
        else:
            results = ScraperService(search).scrape_sites(params.include_previous)
        return jsonify({"links": [r.serialize() for r in results]})
