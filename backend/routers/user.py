import os
from datetime import timedelta
from typing import Annotated

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient

from backend.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    CurrentUser,
    Token,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from backend.models.users import Users

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

user_router = APIRouter(prefix="/user", tags=["user"])


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client["scan-e"], document_models=[Users], skip_indexes=True
    )


# Register the startup event at the app level
@user_router.on_event("startup")
async def startup_event():
    await init_db()


@user_router.post("", summary="Create a new user")
async def create_user(email: str, name: str, password: str):
    user = Users(name=name, email=email, password=get_password_hash(password))
    db_user = await Users.insert(user)
    return f"{db_user.name} created successfully"


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await Users.find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "name": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("me", response_model=CurrentUser)
async def read_users_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    return current_user
