import os
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient

from backend.models.lowest import Lowest
from backend.models.reciepts import Reciepts

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

lowest_router = APIRouter(prefix="/lowest", tags=["lowest"])


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client["scan-e"], document_models=[Lowest], skip_indexes=True
    )


# Register the startup event at the app level
@lowest_router.on_event("startup")
async def startup_event():
    await init_db()


@lowest_router.get("", summary="Gives the lowest price of all products")
async def give_lowest():
    receipts = await Reciepts.find_all().to_list()  # Fetch all receipts
    product_prices = {}

    for receipt in receipts:
        for item in receipt.line_items:  # Iterate over line items in each receipt
            if item.name not in product_prices:
                product_prices[item.name] = item.cost
            else:
                product_prices[item.name] = min(product_prices[item.name], item.cost)

        for name, cost in product_prices.items():
            existing_product = await Lowest.find_one(Lowest.name == name)
            if existing_product:
                # Update only if the new price is lower
                if cost < existing_product.cost:
                    existing_product.cost = cost
                    await existing_product.save()
            else:
                # Insert new record if not found
                await Lowest.insert(name, cost)

    return {"message": "Lowest prices stored successfully", "data": product_prices}
