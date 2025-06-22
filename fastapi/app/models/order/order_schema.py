from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = ""
    address: Optional[str] = ""
    cart_data: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        phone: str = Form(...),
        email: Optional[str] = Form(""),
        address: Optional[str] = Form(""),
        cart_data: str = Form(...)
    ) -> "OrderCreate":
        return cls(
            name=name,
            phone=phone,
            email=email,
            address=address,
            cart_data=cart_data
        )

class OrderStatusUpdate(BaseModel):
    order_id: str
    status: str