# Students API Service

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)](https://www.postgresql.org/)

## Описание проекта

API-сервис, позволяющий вести учет студентов. Документация на Swagger: `http://127.0.0.1:8000/docs`

## Основной функционал

1. **Добавление студента**
    - **URL**: `POST /api/v1/students`
    - **Тело запроса**:
      ```json
      {
       "first_name": "Иван",
       "last_name": "Иванов",
       "date_of_birth": "1995-07-31",
       "study_status": "active",
       "faculty_id": 1
      }
      ```
    - **Ответ**:
      ```json
      {
       "first_name": "Иван",
       "last_name": "Иванов",
       "date_of_birth": "1995-07-31",
       "study_status": "active",
       "faculty_id": 1,
       "id": 1
      }
      ```

2. **Удаление студента по ID**
    - **URL**: `DELETE /api/v1/students/<id>`
    - **Ответ**:
      ```json
      {
        "message": "Студент успешно удален!"
      }
      ```

3. **Удаление студентов по параметрам**
     - **URL**: `DELETE /api/v1/students/`
     - **Доступные query параметры**
       - study_status
       - faculty_id
     - **Ответ**:
       ```json
       {
         "message": "Удалено N студентов!"
       }
       ```

4. **Изменение данных студента**
     - **URL**: `PATCH /api/v1/students/<id>`
     - **Тело запроса**:
      ```json
      {
       "first_name": "Иван",
       "last_name": "Иванов",
       "date_of_birth": "1995-07-31",
       "study_status": "active",
       "faculty_id": 1
      }
      ```
     - **Ответ**:
      ```json
      {
       "first_name": "Иван",
       "last_name": "Иванов",
       "date_of_birth": "1995-07-31",
       "study_status": "active",
       "faculty_id": 1,
       "id": 1
      }
      ```

5. **Получение студентов по параметрам**
     - **URL**: `GET /api/v1/students/`
     - **Доступные query параметры**
       - first_name
       - last_name
       - date_of_birth
       - study_status
       - faculty_id
       - page
       - limit
     - **Ответ**:
       ```json
       {
        "total": 1,
        "page": 1,
        "limit": 10,
        "students": [
        {
            "first_name": "Иван",
            "last_name": "Иванов",
            "date_of_birth": "1995-07-31",
            "study_status": "active",
            "faculty_id": 1,
            "id": 1
        }
        ]
       }
       ```

## Технические особенности

- **Язык**: Python 3.12.6
- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker и docker-compose
- **Тестирование**: pytest
- **Линтинг**: mypy, black, isort

### Запуск с использованием Docker

1. Настройте переменные окружения, используя файл `.env.template`:
   ```bash
   cp .env.template .env
   ```
   Заполните необходимые значения в файле `.env`. Обратите внимание на переменную `MODE=TEST`. Это значение используется
   для запуска тестов. Вы можете заменить его на любое значение, соответствующее режиму работы вашего приложения (например,
   `MODE=development` или `MODE=production`), в зависимости от ваших потребностей.

2. Убедитесь, что значения из файла .env соответствуют параметрам в docker-compose.yml. Замените переменные окружения
   для PostgreSQL:
   environment:
   ```dockerfile
     - POSTGRES_USER=<ваше_значение>
     - POSTGRES_PASSWORD=<ваше_значение>
     - POSTGRES_DB=<ваше_значение>
   healthcheck:
     test: [ "CMD-SHELL", "pg_isready -U <ваше_значение> -d <ваше_значение>" ]
   ```

3. Соберите и запустите контейнеры:
   ```bash
   docker-compose up -d
   ```

4. Убедитесь, что приложение работает: `http://127.0.0.1:8000`

## Тестирование

Для запуска тестов выполните:

   ```bash
   pytest tests
   ```
