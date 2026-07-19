from typing import Any

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from datetime import datetime, UTC, timedelta

from fastapi import HTTPException, status

from app.core.config import settings



def create_access_token(
    subject: str, expires_delta: timedelta | None = None)-> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=2)
    to_encode = {
        "sub": str(subject),
        "type": "access",
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key.get_secret_value(),
        settings.jwt_algorithm
        )
    
    return encoded_jwt

def create_refresh_token(
    subject: str, expires_delta: timedelta | None = None)-> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    to_encode = {
        "sub": str(subject),
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(UTC)
    }
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key.get_secret_value(),
        settings.jwt_algorithm
        )
    
    return encoded_jwt

def decode_access_token(token: str)-> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm]
            )
        
        if payload.get("type") != "access":
            raise credentials_exception
        
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def decode_refresh_token(token: str)-> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm]
            )
        
        if payload.get("type") != "refresh":
            raise credentials_exception
        
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )