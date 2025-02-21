from datetime import date
from pathlib import Path

import pytest
from faker import Faker
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.config import settings
from src.database.models import Base, Faculty
from src.database.repositories import StudentRepository
from src.database.service import get_session
from src.main import app
from src.schemas.student_schemas import BodyStudentSchema, StudentStatusEnum

TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session = async_sessionmaker(
    bind=engine_test, expire_on_commit=False
)

fake = Faker()


async def override_db_session():
    """Фикстура для переопределения зависимости получения сессии БД."""
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_db_session


async def setup_db():
    """Создает тестовую базу данных."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def teardown_db():
    """Удаляет тестовую базу данных."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    db_path = Path("test.db")
    if db_path.exists():
        db_path.unlink()


@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    """Глобальная фикстура для настройки и удаления тестовой БД."""
    assert settings.MODE == "TEST"
    await setup_db()
    yield
    await teardown_db()


@pytest.fixture
async def db_session():
    """Фикстура для создания сессии БД."""
    async with async_session() as session:
        yield session


@pytest.fixture
async def client():
    """Фикстура для создания тестового клиента FastAPI."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def create_faculty(db_session):
    """Фикстура для создания факультета в тестовой БД."""
    faculty = Faculty(name=fake.company())
    db_session.add(faculty)
    await db_session.commit()
    return faculty


@pytest.fixture
async def create_student(db_session, create_faculty):
    """Фикстура для создания студента в тестовой БД."""
    student_data = BodyStudentSchema(
        first_name="Иван",
        last_name="Иванов",
        date_of_birth=date(2000, 1, 1),
        study_status=StudentStatusEnum.active,
        faculty_id=create_faculty.id,
    )
    return await StudentRepository.add_new_student(db_session, student_data)


@pytest.fixture
async def create_expelled_student(db_session, create_faculty):
    """Фикстура для создания отчисленного студента в тестовой БД."""
    student_data = BodyStudentSchema(
        first_name="Петр",
        last_name="Петров",
        date_of_birth=date(2000, 1, 1),
        study_status=StudentStatusEnum.expelled,
        faculty_id=create_faculty.id,
    )
    return await StudentRepository.add_new_student(db_session, student_data)
