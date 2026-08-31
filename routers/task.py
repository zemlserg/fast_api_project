from fastapi import APIRouter
from typing import Annotated

from database import SessionDep
from schemas.task import STask, STaskAdd
from repository import TaskRepository  # Импортируем наш новый класс

router = APIRouter(prefix="/tasks", tags=["Задачи"])

@router.post("", response_model=STask)
async def create_task(
    task: STaskAdd,
    session: SessionDep,
):
    # Вся логика сохранения ушла в репозиторий.
    # Роутер просто передает данные и ждет результат.
    task_model = await TaskRepository.add_one(task, session)
    return task_model

@router.get("", response_model=list[STask])
async def get_tasks(
    session: SessionDep,
):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    tasks = await TaskRepository.find_all(session)
    return tasks