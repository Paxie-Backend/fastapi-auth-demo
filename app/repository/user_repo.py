from sqlalchemy import select
from .base import BaseRepository
from app.models.user import User
from app.schemas.user import UserCreate



class AuthRepository(BaseRepository):
    async def create_user(self, session, user_credentials: UserCreate)-> User:
        ...