from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional
from enum import Enum


class StudentStatusEnum(str, Enum):
    active = "active"
    academic_leave = "academic_leave"
    expelled = "expelled"
    graduated = "graduated"


class SuccessResponse(BaseModel):
    message: str


class StudentSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)
    date_of_birth: date
    status: StudentStatusEnum = Field(default=StudentStatusEnum.active)
    faculty_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class NewStudentSchema(StudentSchema):
    id: int
