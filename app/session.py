from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import settings

engine = create_async_engine(
    settings.get_db_url(),
    echo=False,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
