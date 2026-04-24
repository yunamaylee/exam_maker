from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import anthropic
from app.core.config import DATABASE_URL, ANTHROPIC_API_KEY


# PostgreSQL async URL로 변환 (postgresql:// → postgresql+asyncpg://)
def get_async_database_url() -> str:
    return DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# 모듈 레벨에서 1회 초기화 (커넥션 풀 재사용)
engine = create_async_engine(
    get_async_database_url(),
    echo=False,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Anthropic 클라이언트 싱글턴 (HTTP 커넥션 풀 재사용)
anthropic_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise