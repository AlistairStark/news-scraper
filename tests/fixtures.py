# import pytest
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import Search

# from app.models.flow import Flow, FlowDocument
# from app.models.shop import Shop
# from app.models.template import Template


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


# @pytest.fixture
# async def flow(db_session, shop):
#     f = await flow_factory(
#         db_session,
#         document={},
#         shop_id=shop.id,
#         name="fake flow",
#         short_code="fake code",
#         description="this is a fake description",
#     )
#     return f


# @pytest.fixture
# async def template(db_session, shop):
#     s = await template_factory(
#         db_session,
#         shop_id=shop.id,
#         name="test template",
#         description="stuff",
#         markup="<h1>TEST</h1>",
#         block_markup={"test": {"test1": 1}},
#     )
#     return s
