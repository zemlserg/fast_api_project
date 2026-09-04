import ssl
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

# 1. Создаем безопасный контекст SSL для Supabase
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 2. Инициализируем движок, передавая все параметры Supabase в connect_args
# Это решает проблему блокировки IPv6 на Vercel и ошибку парсинга порта
engine = create_async_engine(
    "postgresql+asyncpg://",
    echo=True,
    connect_args={
        "user": "postgres",
        "password": "steelzsv0826",
        "host": "aws-0-eu-central-1.pooler.supabase.com",
        "port": 6543,
        "database": "postgres",
        "ssl": ssl_context
    }
)

# 3. Асинхронная фабрика сессий (используем async_sessionmaker, который был у вас)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# 4. Базовый класс моделей (ваш класс Model)
class Model(MappedAsDataclass, DeclarativeBase):
    pass

# 5. Функция-генератор сессий для зависимости FastAPI
async def get_db():
    async with new_session() as session:
        yield session

# 6. Зависимость для ваших роутеров (SessionDep)
SessionDep = Annotated[AsyncSession, Depends(get_db)]