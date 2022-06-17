from app.models.schema import Search
from app.repositories.base import DBRepository


class SearchRepository(DBRepository[Search]):
    pass