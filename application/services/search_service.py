from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from application import db, models

if TYPE_CHECKING:
    from application.api.v1.search_controller import (
        CreateSearch,
        CreateSearchTerms,
        CreateSearchLocations,
        UpdateSearch,
    )


class SearchService(object):
    def _check_user_owns_search(self, user_id: str, search_id: str):
        search: models.Search = models.Search.query.filter_by(
            user_id=user_id, id=search_id
        ).one_or_none()
        if not search:
            raise NotFound("This search term was not found")

    def _bulk_delete_by_id(self, ids: List[int], model):
        model.query.filter(model.id.in_(ids)).delete()
        db.session.commit()

    def create_search(self, user_id: int, body: CreateSearch):
        search = models.Search(
            name=body.name,
            description=body.description,
            user_id=user_id,
        )
        db.session.add(search)
        db.session.commit()

    def get_all_searches(self, user_id: int) -> List[dict]:
        searches: List[models.Search] = models.Search.query.filter_by(
            user_id=user_id
        ).order_by(models.Search.name)
        return [{"id": s.id, "name": s.name} for s in searches]

    def get_search(self, user_id: int, id: int) -> models.Search:
        search: models.Search = (
            models.Search.query.filter_by(user_id=user_id, id=id)
            .options(
                joinedload(models.Search.search_locations),
                joinedload(models.Search.search_terms),
            )
            .one_or_none()
        )
        if not search:
            raise NotFound("This search was not found")

        return search

    def update_search(self, user_id: int, body: UpdateSearch):
        search: models.Search = models.Search.query.get(body.id)
        if not search:
            raise NotFound("Search not found")
        search.name = body.name
        search.description = body.description
        db.session.add(search)
        db.session.commit()

    def create_search_terms(self, user_id: int, body: CreateSearchTerms):
        self._check_user_owns_search(user_id, body.search_id)
        terms = [
            models.SearchTerm(term=t, search_id=body.search_id) for t in body.terms
        ]
        db.session.add_all(terms)
        db.session.commit()
        return [t.serialize() for t in terms]

    def create_search_locations(self, user_id: int, body: CreateSearchLocations):
        self._check_user_owns_search(user_id, body.search_id)
        locations = [
            models.SearchLocation(
                name=l["name"],
                url=l["url"],
                search_id=body.search_id,
            )
            for l in body.locations
        ]
        db.session.add_all(locations)
        db.session.commit()
        return [l.serialize() for l in locations]

    def delete_search(self, user_id: int, search_id: int):
        models.Search.query.filter_by(user_id=user_id, id=search_id).delete()
        db.session.commit()

    def delete_search_terms(self, user_id: int, search_id: str, ids: List[int]):
        self._check_user_owns_search(user_id, search_id)
        self._bulk_delete_by_id(ids, models.SearchTerm)

    def delete_search_locations(self, user_id: int, search_id: str, ids: List[int]):
        self._check_user_owns_search(user_id, search_id)
        self._bulk_delete_by_id(ids, models.SearchLocation)
