from typing import Optional

from fastapi import APIRouter, status, Query, Path, Depends

from src.database import DBSession
from src.repositories import StudentRepository
from src.schemas import (
    BodyStudentSchema,
    ResponseStudentSchema,
    StudentStatusEnum,
    SuccessResponse,
    UpdateStudentSchema,
    QueryStudentSchema,
    ResponseStudentsWithPaginationSchema,
    ResponseNewStudentSchema,
)

router = APIRouter(prefix="/api/v1/students", tags=["Студенты"])


@router.post(
    "/",
    response_model=ResponseNewStudentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_student(
    session: DBSession,
    student_data: BodyStudentSchema,
) -> ResponseNewStudentSchema:
    return await StudentRepository.add_new_student(session, student_data)


@router.get(
    "/",
    response_model=ResponseStudentsWithPaginationSchema,
    status_code=status.HTTP_200_OK,
)
async def get_students(
    session: DBSession,
    params: QueryStudentSchema = Depends(),
) -> ResponseStudentsWithPaginationSchema:
    query_params = params.model_dump()
    return await StudentRepository.get_students(session, query_params)


@router.patch(
    "/{student_id}",
    response_model=ResponseStudentSchema,
    status_code=status.HTTP_200_OK,
)
async def update_student(
    session: DBSession,
    student_data: UpdateStudentSchema,
    student_id: int = Path(
        ...,
    ),
) -> ResponseStudentSchema:
    return await StudentRepository.update_student(session, student_id, student_data)


@router.delete(
    "/{student_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_student(
    session: DBSession,
    student_id: int = Path(..., ge=1),
) -> SuccessResponse:
    return await StudentRepository.remove_student(session, student_id)


@router.delete(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_students_with_params(
    session: DBSession,
    study_status: Optional[StudentStatusEnum] = Query(None),
    faculty_id: Optional[int] = Query(None, ge=1),
) -> SuccessResponse:
    return await StudentRepository.remove_students_with_params(
        session, study_status=study_status, faculty_id=faculty_id
    )
