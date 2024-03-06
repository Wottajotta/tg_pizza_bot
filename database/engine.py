import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base

# Инициализируем движок
engine = create_async_engine(os.getenv('DB_URL'), echo=True)

# Для сооздания сессий при запросах в БД
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)