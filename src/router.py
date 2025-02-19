from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.database import DBSession
from src.repositories import StudentRepository
from src.schemas import StudentSchema, NewStudentSchema

router = APIRouter(prefix="/api/students", tags=["Студенты"])


@router.post(
    "/",
    response_model=NewStudentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_student(
        student_data: StudentSchema,
        session: DBSession
) -> JSONResponse:
    return await StudentRepository.add_new_student(student_data, session)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,

)
async def delete_student(
        student_id: int,
        session: DBSession
) -> JSONResponse:
    return await StudentRepository.remove_student(student_id, session)
