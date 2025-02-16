from beanie import Document
from pydantic import Field


class Users(Document):
    name: str
    email: str
    password: str = Field(exclude=True)

    class Settings:
        name = "users"
