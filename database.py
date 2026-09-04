from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# 1. Ссылку очищаем — УБИРАЕМ из самого конца "?sslmode=require"
DATABASE_URL = "postgresql+asyncpg://postgres:steelzsv0826@://supabase.com"

# 2. Создаем контекст SSL программно через встроенную библиотеку Python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 3. Передаем SSL-контекст напрямую внутрь движка через connect_args
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context} # Теперь asyncpg поймет защиту и не выдаст ошибку
)

# Дальше ваш код сессий и базы остается без изменений:
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 3. Фабрика сессий (Session Factory)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# 4. Базовый класс моделей
class Model(MappedAsDataclass, DeclarativeBase):
    pass
SessionDep = Annotated[AsyncSession, Depends(get_db)]