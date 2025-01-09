from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from src.database.db_models import User
from src.database.db_init import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/get_user")
async def get_user_from_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        return {"error": "User not found"}

    return {
        "username": user.username,
        "is_admin": user.is_admin,
    }

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return {"error": "Invalid credentials"}

    request.session["user"] = username
    return {
        "username": username,
        "is_admin": user.is_admin,
    }

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    hashed_password = pwd_context.hash(password)
    result = await db.execute(select(User).where(User.username == username))
    existing_user = result.scalars().first()

    if existing_user:
        return {"error": "User already exists"}

    new_user = User(
        username=username,
        hashed_password=hashed_password,
        is_admin=False,
    )
    db.add(new_user)
    await db.commit()

    return {"message": "Registration successful"}

@router.get("/logout")
async def logout(request: Request):
    user = request.session.get("user")
    request.session.pop("user", None)

    return {"message": f"{user} has logged off"}