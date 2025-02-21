from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.logger import get_logger
from src.schemas.base_schemas import ErrorResponseSchema
import traceback

logger = get_logger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Обработчик непредвиденных ошибок. Логирует подробности ошибки и возвращает
    ответ с кодом состояния 500 (Internal Server Error) и информацией об ошибке.

    Параметры:
    - request: Объект запроса FastAPI.
    - exc: Исключение, которое было выброшено.

    Возвращает:
    - JSONResponse: Ответ с типом ошибки, сообщением и кодом состояния 500.
    """
    error_type = exc.__class__.__name__
    error_message = str(exc)
    error_details = traceback.format_exc()

    logger.exception(
        "Ошибка! Тип: %s, Сообщение: %s\nДетали: %s",
        error_type,
        error_message,
        error_details,
    )

    error_response = ErrorResponseSchema(
        type=error_type, message=error_message
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response,
    )
