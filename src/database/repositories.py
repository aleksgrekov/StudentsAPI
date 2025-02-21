from typing import Optional, Dict, Any, Sequence

from sqlalchemy import delete, select, exists, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.dml import ReturningDelete

from src.handlers.custom_exceptions import (
    IntegrityViolationException,
    RowNotFoundException,
)
from src.database.models import Student, Faculty
from src.schemas.base_schemas import SuccessResponse
from src.schemas.student_schemas import (
    BodyStudentSchema,
    UpdateStudentSchema,
    ResponseStudentSchema,
    ResponseStudentsWithPaginationSchema,
    GetStudentSchema,
)


class StudentRepository:
    """
    Репозиторий для работы со студентами в базе данных.
    """

    @classmethod
    async def add_new_student(
        cls, session: AsyncSession, student_data: BodyStudentSchema
    ) -> ResponseStudentSchema:
        """
        Добавляет нового студента в базу данных.

        :param session: Асинхронная сессия SQLAlchemy.
        :param student_data: Данные нового студента.
        :return: Ответ с информацией о созданном студенте.
        """
        await cls._check_faculty_exists(session, student_data.faculty_id)
        new_student = Student(**student_data.model_dump())

        session.add(new_student)
        await cls._secure_commit(session)
        return ResponseStudentSchema.model_validate(new_student)

    @classmethod
    async def get_students(
        cls, session: AsyncSession, filters: Dict[str, Optional[Any]]
    ) -> ResponseStudentsWithPaginationSchema:
        """
        Получает список студентов с возможностью фильтрации и пагинации.

        :param session: Асинхронная сессия SQLAlchemy.
        :param filters: Словарь с фильтрами (например, limit, page, date_of_birth и др.).
        :return: Объект с информацией о студентах и пагинацией.
        """
        conditions = cls._build_conditions(filters)

        total_count = await cls._get_total_count(session, conditions)

        limit_value = filters.get("limit", 10)
        page_value = filters.get("page", 1)
        offset_value = (page_value - 1) * limit_value

        students_query = (
            select(Student)
            .options(joinedload(Student.faculty))
            .where(*conditions)
            .limit(limit_value)
            .offset(offset_value)
        )

        students_request = await session.scalars(students_query)
        students = students_request.all()

        return ResponseStudentsWithPaginationSchema(
            total=total_count,
            page=page_value,
            limit=limit_value,
            students=[
                GetStudentSchema.model_validate(student) for student in students
            ],
        )

    @classmethod
    async def update_student(
        cls, session: AsyncSession, student_id: int, student_data: UpdateStudentSchema
    ) -> ResponseStudentSchema:
        """
        Обновляет информацию о студенте.

        :param session: Асинхронная сессия SQLAlchemy.
        :param student_id: ID студента, которого нужно обновить.
        :param student_data: Данные для обновления.
        :return: Обновленная информация о студенте.
        """
        student = await session.get(Student, student_id)
        if not student:
            raise RowNotFoundException()

        await cls._check_faculty_exists(session, student_data.faculty_id)

        for key, value in student_data.model_dump(exclude_unset=True).items():
            setattr(student, key, value)

        await cls._secure_commit(session)
        return ResponseStudentSchema.model_validate(student)

    @classmethod
    async def remove_student(
        cls, session: AsyncSession, student_id: int
    ) -> SuccessResponse:
        """
        Удаляет студента по его ID.

        :param session: Асинхронная сессия SQLAlchemy.
        :param student_id: ID студента для удаления.
        :return: Сообщение об успешном удалении.
        """
        delete_query = (
            delete(Student).returning(Student.id).where(Student.id == student_id)
        )
        await cls._execute_delete(session, delete_query)
        return SuccessResponse(message="Студент успешно удален!")

    @classmethod
    async def remove_students_with_params(
        cls, session: AsyncSession, **filters
    ) -> SuccessResponse:
        """
        Удаляет студентов по переданным параметрам.

        :param session: Асинхронная сессия SQLAlchemy.
        :param filters: Фильтры для удаления студентов.
        :return: Сообщение с количеством удаленных студентов.
        """
        conditions = cls._build_conditions(filters)
        delete_query = delete(Student).returning(Student.id).where(*conditions)

        deleted_rows = await cls._execute_delete(session, delete_query)
        return SuccessResponse(message=f"Удалено {deleted_rows} студентов!")

    @classmethod
    async def _execute_delete(
        cls, session: AsyncSession, query: ReturningDelete
    ) -> int:
        """
        Выполняет запрос на удаление студентов.

        :param session: Асинхронная сессия SQLAlchemy.
        :param query: Запрос на удаление.
        :return: Количество удаленных записей.
        """
        request = await session.execute(query)
        rows_deleted = len(request.fetchall())

        if rows_deleted == 0:
            raise RowNotFoundException()

        await cls._secure_commit(session)
        return rows_deleted

    @classmethod
    async def _check_faculty_exists(
        cls, session: AsyncSession, faculty_id: Optional[int]
    ) -> None:
        """
        Проверяет, существует ли факультет с данным ID.

        :param session: Асинхронная сессия SQLAlchemy.
        :param faculty_id: ID факультета.
        """
        if faculty_id and not await session.scalar(
            select(exists().where(Faculty.id == faculty_id))
        ):
            raise RowNotFoundException(
                "Факультет не найден! Сначала создайте факультет!"
            )

    @classmethod
    def _build_conditions(cls, filters: Dict[str, Optional[Any]]) -> Sequence:
        """
        Формирует условия для SQL-запросов на основе переданных фильтров.

        :param filters: Словарь фильтров.
        :return: Список условий для SQLAlchemy.
        """
        return [
            (
                getattr(Student, key) >= value
                if key == "date_of_birth"
                else getattr(Student, key) == value
            )
            for key, value in filters.items()
            if value is not None and key not in ("page", "limit")
        ]

    @classmethod
    async def _get_total_count(cls, session: AsyncSession, conditions: Sequence) -> int:
        """
        Подсчитывает общее количество студентов, соответствующих условиям.

        :param session: Асинхронная сессия SQLAlchemy.
        :param conditions: Условия для подсчета.
        :return: Количество студентов.
        """
        count_query = select(func.count()).select_from(Student).where(*conditions)
        return (await session.execute(count_query)).scalar()

    @classmethod
    async def _secure_commit(cls, session: AsyncSession) -> None:
        """
        Безопасно выполняет commit в базу данных.
        """
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(str(exc))
