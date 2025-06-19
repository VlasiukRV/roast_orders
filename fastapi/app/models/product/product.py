from pydantic import BaseModel


class Product(BaseModel):
    group: str
    name: str
    price: float
    image_url: str