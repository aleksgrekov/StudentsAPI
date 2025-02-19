from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.custom_exceptions import IntegrityViolationException, RowNotFoundException
from src.models import Student
from src.schemas import StudentSchema, NewStudentSchema, SuccessResponse


class StudentRepository:
    @staticmethod
    async def add_new_student(student_data: StudentSchema, session: AsyncSession):
        student_schema = student_data.model_dump()
        new_student = Student(**student_schema)

        session.add(new_student)

        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(str(exc))

        return NewStudentSchema.model_validate(new_student)

    @staticmethod
    async def remove_student(student_id: int, session: AsyncSession):
        query = delete(Student).returning(Student.id).where(Student.id == student_id)

        request = await session.execute(query)
        if not request.fetchone():
            raise RowNotFoundException()

        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise IntegrityViolationException(str(exc))

        return SuccessResponse(message="Студент с id {student_id} успешно удален.".format(student_id=student_id))
