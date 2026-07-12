from sqlalchemy import select
from .base import BaseRepository
from app.models.user import User
from app.schemas.user import UserCreateInternal, UserInDB



class AuthRepository(BaseRepository):
    async def create_user(self, user_creds: UserCreateInternal)-> UserInDB:
        new_user = User(**user_creds.model_dump())

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        
        return UserInDB.model_validate(new_user)
    
    async def user_exists_by_email(self, email: str)-> bool:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return bool(user)
    
    async def get_user_by_email(self, email: str)-> UserInDB:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return UserInDB.model_validate(user)
    
    async def get_user_by_id(self, user_id: int)-> UserInDB:
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalars().one()
        return UserInDB.model_validate(user)