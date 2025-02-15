from beanie import Document


class Users(Document):
    name: str
    email: str
    password: str

    class Settings:
        name = "users"
