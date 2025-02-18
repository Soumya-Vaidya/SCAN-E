from beanie import Document


class Lowest(Document):
    name: str
    cost: float
