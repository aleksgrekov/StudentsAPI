from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, status

from src.database.repository import StudentRepository
from src.database.service import DBSession
from src.schemas.base_schemas import SuccessResponse
from src.schemas.student_schemas import (
    BodyStudentSchema,
    DeleteQueryStudentSchema,
    QueryStudentSchema,
    ResponseStudentSchema,
    ResponseStudentsWithPaginationSchema,
    StudentStatusEnum,
    UpdateStudentSchema,
)

router = APIRouter(prefix="/api/v1/students", tags=["Студенты"])


@router.post(
    "/",
    response_model=ResponseStudentSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить нового студента",
    description="Добавляет нового студента в базу данных. Возвращает данные созданного студента.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Студент успешно добавлен",
            "model": ResponseStudentSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Факультет не найден! Сначала создайте факультет!"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def add_student(
    session: DBSession,
    student_data: BodyStudentSchema,
) -> ResponseStudentSchema:
    """Добавление нового студента"""
    return await StudentRepository.add_new_student(session, student_data)


@router.get(
    "/",
    response_model=ResponseStudentsWithPaginationSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить список студентов",
    description="Возвращает список студентов с возможностью фильтрации и пагинации.",
    responses={
        status.HTTP_200_OK: {
            "description": "Список студентов успешно получен",
            "model": ResponseStudentsWithPaginationSchema,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def get_students(
    session: DBSession,
    params: QueryStudentSchema = Depends(),
) -> ResponseStudentsWithPaginationSchema:
    """Получение списка студентов"""
    query_params = params.model_dump()
    return await StudentRepository.get_students(session, query_params)


@router.patch(
    "/{student_id}",
    response_model=ResponseStudentSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновить информацию о студенте",
    description="Обновляет данные студента по его ID.",
    responses={
        status.HTTP_200_OK: {
            "description": "Информация о студенте успешно обновлена",
            "model": ResponseStudentSchema,
        },
        status.HTTP_404_NOT_FOUND: {"description": "Запрашиваемая запись не найдена!"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def update_student(
    session: DBSession,
    student_data: UpdateStudentSchema,
    student_id: int = Path(..., title="Student ID", description="ID студента", ge=1),
) -> ResponseStudentSchema:
    """Обновление информации о студенте"""
    return await StudentRepository.update_student(session, student_id, student_data)


@router.delete(
    "/{student_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить студента",
    description="Удаляет студента по его ID и возвращает подтверждение.",
    responses={
        status.HTTP_200_OK: {
            "description": "Студент успешно удален",
            "model": SuccessResponse,
        },
        status.HTTP_404_NOT_FOUND: {"description": "Запрашиваемая запись не найдена!"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def delete_student(
    session: DBSession,
    student_id: int = Path(..., ge=1),
) -> SuccessResponse:
    """Удаление студента"""
    return await StudentRepository.remove_student(session, student_id)


@router.delete(
    "/",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Удалить студентов с фильтрацией",
    description="Удаляет студентов по заданным фильтрам (статус обучения, факультет).",
    responses={
        status.HTTP_200_OK: {
            "description": "Студенты успешно удалены",
            "model": SuccessResponse,
        },
        status.HTTP_404_NOT_FOUND: {"description": "Запрашиваемая запись не найдена!"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации данных"
        },
    },
)
async def delete_students_with_params(
    session: DBSession,
    params: DeleteQueryStudentSchema = Depends(),
) -> SuccessResponse:
    """Удаление студентов с параметрами"""
    query_params = params.model_dump()
    return await StudentRepository.remove_students_with_params(session, query_params)
