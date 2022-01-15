from __future__ import annotations

from dataclasses import dataclass
from typing import List, TypedDict
from flask.globals import request

from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields
from marshmallow.schema import Schema
from werkzeug.exceptions import BadRequest

from application.decorators.validation import validate_payload
from application.services.search_service import SearchService
from flask_jwt_extended import current_user


class CreateSearchSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    is_rss = fields.Boolean(required=True)


@dataclass
class CreateSearch:
    name: str
    description: str
    is_rss: bool


class UpdateSearchSchema(CreateSearchSchema):
    id = fields.Integer(required=True)


@dataclass
class UpdateSearch(CreateSearch):
    id: int


class GetSearchParam(Schema):
    search_id = fields.Integer(required=True)


@dataclass
class GetSearchData:
    search_id: int


class Search(Resource):
    @jwt_required()
    @validate_payload(CreateSearchSchema, CreateSearch)
    def post(self, body: CreateSearch):
        return SearchService().create_search(current_user.id, body)

    @jwt_required()
    def delete(self):
        id = request.args.get("id")
        if not id:
            raise BadRequest("No ID supplied")
        return SearchService().delete_search(current_user.id, int(id))

    @jwt_required()
    @validate_payload(UpdateSearchSchema, UpdateSearch)
    def put(self, body: UpdateSearch):
        return SearchService().update_search(current_user.id, body)

    @jwt_required()
    @validate_payload(
        GetSearchParam,
        GetSearchData,
        validate_params=True,
        validate_body=False,
    )
    def get(self, params: GetSearchData):
        search = SearchService().get_search(current_user.id, params.search_id)
        return search.serialize()


class SearchAll(Resource):
    @jwt_required()
    def get(self):
        return SearchService().get_all_searches(current_user.id)


class CreateSearchTermsSchema(Schema):
    terms = fields.List(fields.String, required=True)
    search_id = fields.Integer(required=True)


@dataclass
class CreateSearchTerms:
    terms: List[str]
    search_id: int


class SearchTerms(Resource):
    @jwt_required()
    @validate_payload(CreateSearchTermsSchema, CreateSearchTerms)
    def post(self, body: CreateSearchTerms):
        return SearchService().create_search_terms(current_user.id, body)

    @jwt_required()
    def delete(self):
        ids = request.args.get("ids")
        search_id = request.args.get("search_id")
        if not ids or not search_id:
            raise BadRequest("No ID supplied")
        id_list = [int(id) for id in ids.split(",")]
        return SearchService().delete_search_terms(current_user.id, search_id, id_list)


class CreateSearchLocationsSchema(Schema):
    locations = fields.List(
        fields.Dict(keys=fields.String(), values=fields.String()), required=True
    )
    search_id = fields.Integer(required=True)


@dataclass
class CreateSearchLocations:
    locations: List[Locations]
    search_id: int


class Locations(TypedDict):
    name: str
    url: str


class SearchLocations(Resource):
    @jwt_required()
    @validate_payload(CreateSearchLocationsSchema, CreateSearchLocations)
    def post(self, body: CreateSearchLocations):
        return SearchService().create_search_locations(current_user.id, body)

    @jwt_required()
    def delete(self):
        ids = request.args.get("ids")
        search_id = request.args.get("search_id")
        if not ids or not search_id:
            raise BadRequest("No ID supplied")
        id_list = [int(id) for id in ids.split(",")]
        return SearchService().delete_search_locations(
            current_user.id, search_id, id_list
        )
