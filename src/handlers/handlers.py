from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.logger import get_logger
from src.schemas.base_schemas import ErrorResponseSchema

logger = get_logger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_type = exc.__class__.__name__
    error_message = str(exc)

    schema = ErrorResponseSchema(
        type=error_type, message=error_message
    ).model_dump()

    logger.exception(
        "\nОшибка!\n%s: %s\n",
        error_type,
        error_message,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=schema,
    )
