from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class DBRepository(Generic[ModelType]):

    Model: Type[ModelType] = None

    def __init__(self, session: AsyncSession):
        if not self.Model:
            raise ValueError("Model class is missing!")
        self.session: AsyncSession = session

    async def get_by_id(self, pk: int) -> ModelType:
        session: AsyncSession
        async with self.session as session:
            r = await session.get(self.Model, pk)
            return r

    async def update(self, db_model: ModelType, **data) -> ModelType:
        for k, v in data.items():
            setattr(db_model, k, v)
        async with self.session as session:
            session.add(db_model)
            await session.commit()
            return db_model

    async def create(self, **data) -> ModelType:
        async with self.session as session:
            db_model = self.Model(**data)
            session.add(db_model)
            await session.commit()
            return db_model

    async def delete(self, db_model: ModelType):
        session: AsyncSession
        async with self.session as session:
            await session.delete(db_model)
            await session.commit()
