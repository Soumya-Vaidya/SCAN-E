from fastapi import APIRouter
from typing import Union

user_router = APIRouter()

@user_router.get("/users")
def get_users():
    return {"message": "List of users"}

@user_router.get("/")
def read_root():
    return {"Banana": "babababababbabba"}


@user_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}