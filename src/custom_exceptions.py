from fastapi import HTTPException, status


class RowNotFoundException(HTTPException):
    default_message = "Пользователь не найден!"

    def __init__(self, message: str = default_message):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class IntegrityViolationException(Exception):
    def __init__(self, message: str):
        self.message = message
