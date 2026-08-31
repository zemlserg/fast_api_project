from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tasks import TasksModel
from schemas.task import STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd, session: AsyncSession) -> TasksModel:
        # 1. Превращаем данные из Pydantic в словарь
        task_dict = data.model_dump()

        # 2. Создаем объект модели
        task = TasksModel(**task_dict)

        # 3. Добавляем и сохраняем
        session.add(task)
        await session.commit()
        await session.refresh(task)

        # 4. Возвращаем созданный объект
        return task

    @classmethod
    async def find_all(cls, session: AsyncSession):
        # 1. Готовим запрос
        query = select(TasksModel)

        # 2. Выполняем
        result = await session.execute(query)

        # 3. Возвращаем список объектов
        tasks_models = result.scalars().all()
        return tasks_models