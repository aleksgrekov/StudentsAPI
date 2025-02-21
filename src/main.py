import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.service import delete_tables, create_tables
from src.handlers.handlers import exception_handler
from src.router import router

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    """Функция управления жизненным циклом приложения."""
    await delete_tables()
    logger.info("База данных очищена")

    await create_tables()
    logger.info("База данных готова к работе")

    yield

    logger.info("Выключение сервиса...")


# Создание экземпляра FastAPI
app = FastAPI(title="API Студентов", version="1.0.0", lifespan=lifespan)

# Глобальный обработчик исключений
app.add_exception_handler(Exception, exception_handler)

# Подключение маршрутов
app.include_router(router)

# Точка входа
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)