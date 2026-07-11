from fastapi import APIRouter


router = APIRouter()


@router.post("/login")
async def login():
    return {"msg": "Hello!"}

@router.post("/signup")
async def sign_up():
    return {"msg": "Hello!"}

