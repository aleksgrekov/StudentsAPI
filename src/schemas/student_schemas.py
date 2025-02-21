from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, List
from enum import Enum


class StudentStatusEnum(str, Enum):
    """
    Перечисление для статуса студента.
    """

    active = "active"
    academic_leave = "academic_leave"
    expelled = "expelled"
    graduated = "graduated"


class BodyStudentSchema(BaseModel):
    """
    Схема для создания или обновления информации о студенте.
    """

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        title="Имя",
        description="Имя студента. Должно быть от 1 до 30 символов.",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        title="Фамилия",
        description="Фамилия студента. Должна быть от 1 до 30 символов.",
    )
    date_of_birth: date = Field(
        ...,
        title="Дата рождения",
        description="Дата рождения студента в формате YYYY-MM-DD.",
    )
    study_status: StudentStatusEnum = Field(
        default=StudentStatusEnum.active,
        title="Статус обучения",
        description="Текущий статус обучения студента.",
    )
    faculty_id: Optional[int] = Field(
        None,
        ge=1,
        title="ID факультета",
        description="ID факультета, к которому принадлежит студент. Значение должно быть больше или равно 1.",
    )

    model_config = ConfigDict(from_attributes=True)


class UpdateStudentSchema(BaseModel):
    """
    Схема для обновления информации о студенте.
    """

    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=30,
        title="Имя",
        description="Имя студента. Должно быть от 1 до 30 символов.",
    )
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=30,
        title="Фамилия",
        description="Фамилия студента. Должна быть от 1 до 30 символов.",
    )
    date_of_birth: Optional[date] = Field(
        None,
        title="Дата рождения",
        description="Дата рождения студента в формате YYYY-MM-DD.",
    )
    study_status: Optional[StudentStatusEnum] = Field(
        None, title="Статус обучения", description="Текущий статус обучения студента."
    )
    faculty_id: Optional[int] = Field(
        None,
        ge=1,
        title="ID факультета",
        description="ID факультета, к которому принадлежит студент. Значение должно быть больше или равно 1.",
    )


class QueryStudentSchema(UpdateStudentSchema):
    """
    Схема для фильтрации студентов с параметрами пагинации.
    """

    page: Optional[int] = Field(
        default=1,
        ge=1,
        title="Страница",
        description="Номер страницы для пагинации. Значение должно быть больше или равно 1.",
    )
    limit: Optional[int] = Field(
        default=10,
        ge=1,
        title="Лимит",
        description="Количество студентов на одной странице. Значение должно быть больше или равно 1.",
    )


class ResponseStudentSchema(BodyStudentSchema):
    """
    Схема для ответа с информацией о новом студенте.
    """

    id: int = Field(
        ..., title="ID студента", description="Уникальный идентификатор студента."
    )


class GetStudentSchema(ResponseStudentSchema):
    """
    Схема для ответа с информацией о студенте, включая факультет.
    """

    faculty_title: Optional[str] = Field(
        None,
        title="Название факультета",
        description="Название факультета, к которому принадлежит студент.",
    )


class ResponseStudentsWithPaginationSchema(BaseModel):
    """
    Схема для ответа с пагинированным списком студентов.
    """

    total: int = Field(
        ...,
        title="Общее количество студентов",
        description="Общее количество студентов.",
    )
    page: int = Field(
        ...,
        title="Текущая страница",
        description="Номер текущей страницы с результатами.",
    )
    limit: int = Field(
        ...,
        title="Лимит на странице",
        description="Количество студентов на одной странице.",
    )
    students: List[ResponseStudentSchema] = Field(
        ...,
        title="Список студентов",
        description="Список студентов на текущей странице.",
    )
