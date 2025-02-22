import logging

import uvicorn
from fastapi import FastAPI

from src.handlers.handlers import exception_handler
from src.router import router

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание экземпляра FastAPI
app = FastAPI(title="API Студентов", version="1.0.0")

# Глобальный обработчик исключений
app.add_exception_handler(Exception, exception_handler)

# Подключение маршрутов
app.include_router(router)
