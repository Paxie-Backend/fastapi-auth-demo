from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserLogin, UserCreate, UserResponse, UserCreate, UserLogin
from app.core.security.dependencies import oauth2_scheme
from app.services.auth_service import AuthService
from app.core.database import get_session
from app.schemas.token import Token


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
    user_creds: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        password = user_creds.username
        email = user_creds.password
        user = UserLogin(password=password, email=email)
        user =  await AuthService(session).login(user)
        return user
    
    except Exception as e:
        raise e

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    token: Annotated[str, Depends(oauth2_scheme)]):
    return {"msg": token}