from fastapi import HTTPException, status

from src.logger import get_logger

logger = get_logger(__name__)


class RowNotFoundException(HTTPException):
    default_message = "Пользователь не найден!"

    def __init__(self, message: str = default_message):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        logger.warning(
            "\nОшибка! %s: %s\n", self.__class__.__name__, message
        )


class IntegrityViolationException(Exception):
    def __init__(self, message: str):
        self.message = message
