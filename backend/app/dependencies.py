from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from app.core.config import DATABASE_URL

# PostgreSQL async URL로 변환 (postgresql:// → postgresql+asyncpg://)
def get_async_database_url() -> str:
    return DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# async engine 생성
def get_engine():
    return create_async_engine(
        get_async_database_url(),
        echo=False,
    )


# async session factory
def get_session_local():
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_session_local()
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise