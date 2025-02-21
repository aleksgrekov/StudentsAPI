from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.config import settings
from src.database.models import Base

# Создаем движок
DB_URL = settings.db_url
engine = create_async_engine(DB_URL)

# Фабрика сессий
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии БД."""
    async with async_session() as session:
        yield session


# Используется для внедрения зависимостей в FastAPI
DBSession = Annotated[AsyncSession, Depends(get_session)]


async def create_tables():
    """Создание всех таблиц в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    """Удаление всех таблиц из базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
