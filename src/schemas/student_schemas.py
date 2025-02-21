from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, List
from enum import Enum


class StudentStatusEnum(str, Enum):
    active = "active"
    academic_leave = "academic_leave"
    expelled = "expelled"
    graduated = "graduated"


class BodyStudentSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)
    date_of_birth: date
    study_status: StudentStatusEnum = Field(default=StudentStatusEnum.active)
    faculty_id: Optional[int] = Field(None, ge=1)

    model_config = ConfigDict(from_attributes=True)


class UpdateStudentSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: Optional[str] = Field(None, min_length=1, max_length=30)
    date_of_birth: Optional[date] = None
    study_status: Optional[StudentStatusEnum] = None
    faculty_id: Optional[int] = Field(None, ge=1)


class QueryStudentSchema(UpdateStudentSchema):
    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=10, ge=1)


class ResponseNewStudentSchema(BodyStudentSchema):
    id: int


class ResponseStudentSchema(ResponseNewStudentSchema):
    faculty_title: Optional[str]


class ResponseStudentsWithPaginationSchema(BaseModel):
    total: int
    page: int
    limit: int
    students: List[ResponseStudentSchema]
