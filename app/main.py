from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import get_session, engine, Base
from app.routers.auth import router as authRouter


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, prefix="/api/auth", tags=["auth"])