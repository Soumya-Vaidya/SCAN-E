from beanie import Document
from typing import List, Optional
from pydantic import BaseModel


class LineItems(BaseModel):
    name: str
    cost: List[str]


class Reciepts(Document):
    image_url: Optional[str]
    date: Optional[str]
    shop_name: Optional[str]
    total_amount: Optional[str]
    line_items: List[LineItems]

    class Settings:
        name = "receipts"
