from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database import delete_tables, create_tables
from src.router import router


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(title="API Студентов", lifespan=lifespan)

app.include_router(router=router)

if __name__ == '__main__':
    uvicorn.run("main:app")
