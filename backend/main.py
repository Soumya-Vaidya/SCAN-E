from fastapi import FastAPI

from backend.routers.user import user_router
from backend.routers.receipts import receipts_router

app = FastAPI()

app.include_router(user_router)
app.include_router(receipts_router)
