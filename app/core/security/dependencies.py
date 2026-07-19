from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.jwt_handlers import decode_access_token
from app.schemas.token import TokenPayload, TokenData
from app.repository.user_repo import AuthRepository
from app.core.database import get_session
from app.schemas.user import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)]
    )-> UserInDB:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
            )
    
    try:
        payload = decode_access_token(token=token)
        token_payload = TokenPayload(**payload)
        token_data = TokenData(email=token_payload.sub)
        
        user = await AuthRepository(session).get_user_by_email(email=token_data.email) 
        if user is None:
            raise credentials_exception
        
        return user
        
    except ValidationError:
        raise credentials_exception