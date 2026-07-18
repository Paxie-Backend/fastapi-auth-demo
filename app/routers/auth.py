from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserLogin, UserCreate, UserResponse, UserInDB
from app.core.security.dependencies import get_current_user
from app.services.auth_service import AuthService
from app.core.database import get_session
from app.schemas.token import Token


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_creds: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)]):
        user =  await AuthService(session).register(user_creds)
        return user
    

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_creds: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)]
    ):
        credentials = UserLogin(
            email=user_creds.username,
            password=user_creds.password
        )
        
        token =  await AuthService(session).login(credentials)
        return token

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
    ):
    
    return current_user