import os
from dotenv import load_dotenv

from beanie import init_beanie
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from backend.models.reciepts import Reciepts

from backend.utils import (
    convert_receipt_to_text,
    convert_text_to_json,
    download_image,
)

receipts_router = APIRouter(prefix="/receipts", tags=["receipts"])

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client["scan-e"], document_models=[Reciepts], skip_indexes=True
    )


# Register the startup event at the app level
@receipts_router.on_event("startup")
async def startup_event():
    await init_db()


@receipts_router.post("/upload", summary="Convert a receipt image to text")
async def store_reciepts_to_cluster(image_url: str):
    download_image(image_url)
    image_path = "./bills/downloaded_image.jpg"
    output = convert_receipt_to_text(image_path)
    final_lineitems = convert_text_to_json(output)
    return await Reciepts.insert(final_lineitems)
