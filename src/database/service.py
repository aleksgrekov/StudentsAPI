from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.config import settings
from src.database.models import Base

DB_URL = settings.get_db_url
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(create_session)]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
