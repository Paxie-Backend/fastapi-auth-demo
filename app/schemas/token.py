from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: datetime | None = None

class TokenData(BaseModel):
    email: EmailStr | None = Field(max_length=120, default=None)