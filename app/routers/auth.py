from fastapi import APIRouter
from app.schemas.user import UserLogin, UserCreate

router = APIRouter()


@router.post("/login")
async def login(user_credentials: UserLogin):
    return {"msg": user_credentials}

@router.post("/signup")
async def sign_up(user_credentials: UserCreate):
    return {"msg": user_credentials}

