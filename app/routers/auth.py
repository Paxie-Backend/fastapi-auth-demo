from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.schemas.user import UserLogin, UserCreate
from app.core.database import get_session
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.schemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_creds: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        user =  await AuthService(session).register(user_creds)
        return user
    
    except Exception as e:
        raise e

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_creds: UserLogin,
    session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        user =  await AuthService(session).login(user_creds)
        return user
    
    except Exception as e:
        raise e

