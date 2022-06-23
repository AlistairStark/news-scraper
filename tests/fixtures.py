import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import Search, SearchLocation, SearchTerm


async def search_factory(db_session, **search_kwargs):
    session: AsyncSession
    async with db_session as session:
        s = Search(**search_kwargs)
        session.add(s)
        await session.commit()
        return s


@pytest.fixture
async def search(db_session, user_fixture):
    s = await search_factory(
        db_session,
        name="search test",
        description="test search",
        user_id=user_fixture.id,
        is_rss=False,
    )
    return s


async def search_term_factory(db_session, search, term):
    session: AsyncSession
    async with db_session as session:
        s = SearchTerm(search_id=search.id, term=term)
        session.add(s)
        await session.commit()
        return s


@pytest.fixture
async def search_terms(db_session, search):
    terms = ["term 1", "term 2", "term 3"]
    terms_obj = []
    for term in terms:
        s = await search_term_factory(
            db_session,
            search,
            term,
        )
        terms_obj.append(s)
    return terms_obj


async def search_location_factory(db_session, search, url, name):
    session: AsyncSession
    async with db_session as session:
        s = SearchLocation(search_id=search.id, url=url, name=name)
        session.add(s)
        await session.commit()
        return s


@pytest.fixture
async def search_locations(db_session, search):
    locations = [
        {"url": "www.term1.com", "name": "test1"},
        {"url": "www.term2.com", "name": "test2"},
        {"url": "www.term3.com", "name": "test3"},
    ]
    location_obj = []
    for l in locations:
        s = await search_location_factory(
            db_session,
            search,
            l["url"],
            l["name"],
        )
        location_obj.append(s)
    return location_obj
