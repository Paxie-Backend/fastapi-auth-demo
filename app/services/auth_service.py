from app.repository.user_repo import AuthRepository
from app.schemas.user import UserResponse, UserCreate, UserLogin, UserCreateInternal
from app.schemas.token import Token, TokenData
from app.core.security.jwt_handlers import create_access_token, create_refresh_token, decode_token
from app.core.security.utils import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  HTTPException, status


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.__auth_repository = AuthRepository(session)
    
    
    async def register(self, user_creds: UserCreate)-> UserResponse:
        if await self.__auth_repository.user_exists_by_email(user_creds.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please login"
            )
        
        hashed_password = get_password_hash(user_creds.password)
        user_internal = UserCreateInternal(
            **user_creds.model_dump(exclude={"password"}),
            hashed_password=hashed_password
            )
        
        new_user = await self.__auth_repository.create_user(user_internal)
        return UserResponse.model_validate(new_user)
    
    async def login(self, user_creds: UserLogin)-> Token:
        if not await self.__auth_repository.user_exists_by_email(user_creds.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please register"
            )
        
        user = await self.__auth_repository.get_user_by_email(user_creds.email)
        if not verify_password(user_creds.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password not match"
            )
        
        access_token = create_access_token(email=user.email)
        refresh_token = create_refresh_token(subject=user.email)
        
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        } 
        
        return Token(**token)