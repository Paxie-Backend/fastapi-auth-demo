from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str | None = Field(min_length=2, max_length=100, default=None)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class UserUpdate(BaseModel):
    first_name: str | None = Field(min_length=2, max_length=50, default=None)
    last_name: str | None = Field(min_length=2, max_length=100, default=None)
    password: str | None = Field(min_length=8, default=None)
    email: EmailStr | None = Field(max_length=120, default=None)

class UserLogin(BaseModel):
    password: str = Field(min_length=8)
    email: EmailStr = Field(max_length=120)

class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hashed_password: str

class UserCreateInternal(UserBase):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str