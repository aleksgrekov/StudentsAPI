from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import create_session
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
        session: AsyncSession = Depends(create_session)
) -> JSONResponse:
    return await StudentRepository.add_new_student(student_data, session)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,

)
async def delete_student(
        student_id: int,
        session: AsyncSession = Depends(create_session)
) -> JSONResponse:
    return await StudentRepository.remove_student(student_id, session)
