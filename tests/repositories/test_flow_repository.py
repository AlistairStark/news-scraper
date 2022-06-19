# import pytest
# from sqlalchemy.ext.asyncio.session import AsyncSession

# from app.models.flow import Flow
# from app.repositories.flow_repository import FlowRepository
# from tests.fixtures import flow_factory, shop_factory


# @pytest.mark.asyncio
# async def test_create_flow(db_session: AsyncSession, shop):
#     shop_id = shop.id
#     flow = await FlowRepository(db_session).create_flow(
#         shop_id=shop.id,
#         name="test flow",
#         short_code="testcode",
#         description="stuff",
#     )

#     got = flow.serialize()

#     expected = {
#         "id": 1,
#         "name": "test flow",
#         "shop_id": shop_id,
#         "short_code": "testcode",
#         "description": "stuff",
#         "flow_document_id": 1,
#     }

#     assert got == expected
