from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.service import delete_tables, create_tables
from src.handlers.handlers import exception_handler
from src.router import router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(title="API Студентов", version="1.0.0", lifespan=lifespan)

app.add_exception_handler(Exception, exception_handler)

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app")
