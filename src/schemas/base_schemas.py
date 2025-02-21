from pydantic import BaseModel, Field


class ErrorResponseSchema(BaseModel):
    type: str = Field(...)
    message: str = Field(...)


class SuccessResponse(BaseModel):
    message: str
