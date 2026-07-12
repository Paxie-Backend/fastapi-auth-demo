from typing import Any
import jwt
from datetime import datetime, UTC, timedelta
from app.core.config import settings


def create_access_token(
    email: str, expires_delta: timedelta | None = None)-> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "sub": str(email),
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
        expire = datetime.now(UTC) + timedelta(minutes=settings.refresh_token_expire_days)
    to_encode = {
        "sub": str(subject),
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

def decode_token(token: str)-> dict[str, Any]:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm]
        )
    
    return payload