# import pytest
# from sqlalchemy.ext.asyncio.session import AsyncSession

# from app.models.flow import Flow, FlowDocument
# from app.models.shop import Shop
# from app.models.template import Template


# async def flow_factory(db_session, document={}, **flow_kwargs):
#     session: AsyncSession
#     async with db_session as session:
#         fd = FlowDocument(document=document)
#         f = Flow(**flow_kwargs, flow_document=fd)
#         session.add(f)
#         await session.commit()
#         return f


# async def shop_factory(db_session, **shop_kwargs):
#     session: AsyncSession
#     async with db_session as session:
#         s = Shop(**shop_kwargs)
#         session.add(s)
#         await session.commit()
#         return s


# async def template_factory(db_session, **template_kwargs):
#     session: AsyncSession
#     async with db_session as session:
#         t = Template(**template_kwargs)
#         session.add(t)
#         await session.commit()
#         return t


# @pytest.fixture
# async def shop(db_session):
#     s = await shop_factory(
#         db_session,
#         token="faketoken",
#         shop_name="test",
#         scopes="fakescopes",
#         host="fakehost",
#     )
#     return s


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
