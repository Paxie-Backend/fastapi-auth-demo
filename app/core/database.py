from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings



engine =  create_async_engine(
    settings.DATABASE_URL,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    )


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass