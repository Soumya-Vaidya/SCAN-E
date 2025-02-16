from typing import Union

from beanie import init_beanie
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from backend.main import settings
from backend.models.users import Users

user_router = APIRouter()


async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client["sample_mflix"], document_models=[Users], skip_indexes=True
    )


# Register the startup event at the app level
@user_router.on_event("startup")
async def startup_event():
    await init_db()


@user_router.get("/users")
async def get_users():
    result = await Users.find({"name": "Mercedes Tyler"}).to_list()
    return result


@user_router.get("/")
async def read_root():
    return {"Banana": "babababababbabba"}


@user_router.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
