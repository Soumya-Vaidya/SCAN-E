from typing import Optional

from beanie import Document


class Users(Document):
    name: str
    email: str
    password: Optional[str] = None

    class Settings:
        name = "users"
