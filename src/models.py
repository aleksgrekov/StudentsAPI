import enum
from datetime import date
from typing import Optional

from sqlalchemy import String, Date, Enum, ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class StudentStatus(enum.Enum):
    active = "active"  # Активный студент
    academic_leave = "academic_leave"  # Академический отпуск
    expelled = "expelled"  # Отчислен
    graduated = "graduated"  # Выпускник


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=30))
    last_name: Mapped[str] = mapped_column(String(length=30))
    date_of_birth: Mapped[date] = mapped_column(Date)
    status: Mapped[StudentStatus] = mapped_column(Enum(StudentStatus), default=StudentStatus.active)
    faculty_id: Mapped[Optional[int]] = mapped_column(ForeignKey("faculties.id", ondelete="set null"), nullable=True)

    faculty: Mapped[Optional["Faculty"]] = relationship(backref="students", passive_deletes=True)

    faculty_title: AssociationProxy[Optional[str]] = association_proxy("faculty", "name")


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
