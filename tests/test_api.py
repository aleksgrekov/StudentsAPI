import pytest
from fastapi import status

from src.schemas.student_schemas import StudentStatusEnum


@pytest.mark.asyncio
async def test_add_student(client, create_faculty):
    """
    Тест на добавление нового студента.
    Проверяет, что студент успешно создается и возвращает корректные данные.
    """
    student_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "date_of_birth": "2000-01-01",
        "study_status": StudentStatusEnum.active,
        "faculty_id": create_faculty.id,
    }

    response = await client.post("/api/v1/students/", json=student_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "Иван"
    assert data["last_name"] == "Иванов"
    assert data["study_status"] == "active"


@pytest.mark.asyncio
async def test_add_student_invalid_data(client):
    """
    Тест на добавление студента с некорректными данными.
    Ожидается ошибка 422 из-за неверных или отсутствующих значений.
    """
    student_data = {
        "first_name": "",
        "last_name": "",
        "date_of_birth": "invalid-date",
        "study_status": "unknown",
        "faculty_id": None,
    }

    response = await client.post("/api/v1/students/", json=student_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_students(client, create_student):
    """
    Тест на получение списка студентов.
    Проверяет, что API возвращает непустой список студентов.
    """
    response = await client.get("/api/v1/students/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] > 0
    assert len(data["students"]) > 0


@pytest.mark.asyncio
async def test_update_student(client, create_student):
    """
    Тест на обновление данных студента.
    Проверяет, что имя студента успешно изменяется.
    """
    update_data = {"first_name": "Петр"}
    response = await client.patch(
        f"/api/v1/students/{create_student.id}", json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Петр"


@pytest.mark.asyncio
async def test_delete_student(client, create_student):
    """
    Тест на удаление студента.
    Проверяет, что студент успешно удаляется и возвращается соответствующее сообщение.
    """
    response = await client.delete(f"/api/v1/students/{create_student.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Студент успешно удален!"


@pytest.mark.asyncio
async def test_delete_nonexistent_student(client):
    """
    Тест на удаление несуществующего студента.
    Ожидается ошибка 404, так как студент с указанным ID не существует.
    """
    response = await client.delete("/api/v1/students/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_students_with_params(
    client, db_session, create_student, create_expelled_student
):
    """
    Тест на удаление студентов по параметрам (например, отчисленные студенты).
    Проверяет, что API корректно удаляет указанную группу студентов.
    """
    response = await client.delete(
        "/api/v1/students/", params={"study_status": "expelled"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Удалено 1 студентов!"
