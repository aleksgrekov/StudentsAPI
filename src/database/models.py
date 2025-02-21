import enum
from datetime import date
from typing import Optional, List, Annotated

from sqlalchemy import String, Date, Enum, ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


class StudentStatus(enum.Enum):
    """Перечисление возможных статусов студента."""
    active = "active"  # Активный студент
    academic_leave = "academic_leave"  # Академический отпуск
    expelled = "expelled"  # Отчислен
    graduated = "graduated"  # Выпускник

    def __str__(self) -> str:
        return self.value


class Student(Base):
    """Модель студента."""
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Annotated[str, 30]] = mapped_column(String(length=30))
    last_name: Mapped[Annotated[str, 30]] = mapped_column(String(length=30))
    date_of_birth: Mapped[date] = mapped_column(Date)
    study_status: Mapped[StudentStatus] = mapped_column(
        Enum(StudentStatus), default=StudentStatus.active
    )
    faculty_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("faculties.id", ondelete="SET NULL"), nullable=True
    )

    faculty: Mapped[Optional["Faculty"]] = relationship(
        back_populates="students", passive_deletes=True
    )

    faculty_title: AssociationProxy[Optional[str]] = association_proxy(
        "faculty", "name"
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name}, status={self.study_status})>"


class Faculty(Base):
    """Модель факультета."""
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    students: Mapped[Optional[List["Student"]]] = relationship(back_populates="faculty")

    def __repr__(self) -> str:
        return f"<Faculty(id={self.id}, name={self.name})>"
