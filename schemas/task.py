from pydantic import BaseModel, ConfigDict

# 1. Базовый класс (общие поля)
class STaskBase(BaseModel):
    name: str
    description: str | None = None
    id: int = 127

# 2. Класс для создания (ничего не добавляет, просто копирует базу)
class STaskAdd(STaskBase):
    pass

# 3. Класс для чтения (добавляет id)
class STask(STaskBase):
    id: int
model_config = ConfigDict(from_attributes=True)