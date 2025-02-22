from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.config import settings
from src.database.models import Base

# Создаем движок
DB_URL = settings.db_url(driver="asyncpg")
engine = create_async_engine(DB_URL)

# Фабрика сессий
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии БД."""
    async with async_session() as session:
        yield session


# Используется для внедрения зависимостей в FastAPI
DBSession = Annotated[AsyncSession, Depends(get_session)]
