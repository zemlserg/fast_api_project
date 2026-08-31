from fastapi import FastAPI, status  # 1. Импортируем status
from routers.task import router as tasks_router
import uvicorn
from contextlib import asynccontextmanager
from database import engine, Model  # Импортируем из database.py


# ... импорты роутеров ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield  # Разделяет старт и выключение

    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")


# Передаем lifespan в приложение
app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

# Добавляем этот блок в конец файла
if __name__ == "__main__":
    # Обратите внимание: имя файла передается как строка
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)