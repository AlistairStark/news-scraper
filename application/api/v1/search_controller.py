from __future__ import annotations

from dataclasses import dataclass
from typing import List, TypedDict

from flask import Blueprint, jsonify
from flask.globals import request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import fields
from marshmallow.schema import Schema
from werkzeug.exceptions import BadRequest

from application.services.search_service import SearchService
from application.services.validate_service import deserialize_body, deserialize_params

bp = Blueprint("search", __name__)


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


@bp.post("/search")
@jwt_required()
def post_search():
    body: CreateSearch = deserialize_body(CreateSearchSchema, CreateSearch)
    SearchService().create_search(current_user.id, body)
    return "", 201


@bp.delete("/search")
@jwt_required()
def delete_search():
    id = request.args.get("id")
    if not id:
        raise BadRequest("No ID supplied")
    SearchService().delete_search(current_user.id, int(id))
    return "", 204


@bp.put("/search")
@jwt_required()
def put_search():
    body: UpdateSearch = deserialize_body(UpdateSearchSchema, UpdateSearch)
    SearchService().update_search(current_user.id, body)
    return "", 200


@bp.get("/search")
@jwt_required()
def get_search():
    params: GetSearchData = deserialize_params(GetSearchParam, GetSearchData)
    search = SearchService().get_search(current_user.id, params.search_id)
    return jsonify(search.serialize())


@bp.get("/search-all")
@jwt_required()
def get_search_all():
    searches = SearchService().get_all_searches(current_user.id)
    return jsonify(searches)


class CreateSearchTermsSchema(Schema):
    terms = fields.List(fields.String, required=True)
    search_id = fields.Integer(required=True)


@dataclass
class CreateSearchTerms:
    terms: List[str]
    search_id: int


@bp.post("/search-terms")
@jwt_required()
def post_search_terms():
    body: CreateSearchTerms = deserialize_body(
        CreateSearchTermsSchema, CreateSearchTerms
    )
    terms = SearchService().create_search_terms(current_user.id, body)
    return jsonify(terms)


@bp.delete("/search-terms")
@jwt_required()
def delete_search_terms():
    ids = request.args.get("ids")
    search_id = request.args.get("search_id")
    if not ids or not search_id:
        raise BadRequest("No ID supplied")
    id_list = [int(id) for id in ids.split(",")]
    SearchService().delete_search_terms(current_user.id, search_id, id_list)
    return "", 204


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


@bp.post("/search-location")
@jwt_required()
def post_search_locations():
    body: CreateSearchLocations = deserialize_body(
        CreateSearchLocationsSchema, CreateSearchLocations
    )
    locations = SearchService().create_search_locations(current_user.id, body)
    return jsonify(locations)


@bp.delete("/search-location")
@jwt_required()
def delete_search_locations():
    ids = request.args.get("ids")
    search_id = request.args.get("search_id")
    if not ids or not search_id:
        raise BadRequest("No ID supplied")
    id_list = [int(id) for id in ids.split(",")]
    SearchService().delete_search_locations(current_user.id, search_id, id_list)
    return "", 204
