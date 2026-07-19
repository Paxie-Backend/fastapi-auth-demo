from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    type: Literal["access", "refresh"]
    exp: datetime 

class TokenData(BaseModel):
    email: EmailStr = Field(max_length=120)

class RefreshTokenRequest(BaseModel):
    refresh_token: str