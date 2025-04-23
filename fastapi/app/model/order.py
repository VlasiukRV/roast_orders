import json
from enum import Enum

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.utils import generate_order_id


class OrderStatus(str, Enum):
    accepted = "Accepted"
    processing = "Processing"
    canceled = "Completed"


class OrderPayStatus(str, Enum):
    unpaid = "Unpaid"
    paid = "Paid"


class OrderItem(BaseModel):
    order_id: str
    name: str
    price: float
    quantity: int
    summ: float
    status: OrderStatus = "Accepted"

    @classmethod
    def from_customer_data(cls, name: str, price: float, quantity: int, status: OrderStatus = "Accepted"):
        return cls(
            order_id="",
            name=name,
            price=price,
            quantity=quantity,
            summ=price * quantity,
            status=status)

    def to_row(self):
        return [
            self.order_id,
            self.name,
            self.price,
            self.quantity,
            self.price * self.quantity,
            self.status
        ]


class Order(BaseModel):
    order_id: str
    order_time: datetime
    name: str
    phone: str
    email: Optional[str] = ""
    address: Optional[str] = ""
    order_items: List[OrderItem] = Field(default_factory=list)
    cart_total: float = 0.0
    status: str = "Accepted"
    pay_status: str = "Unpaid"

    def add_order_item(self, item: OrderItem):
        item.order_id = self.order_id
        self.order_items.append(item)
        self.cart_total += item.price * item.quantity

    @classmethod
    def from_customer_data(cls, name: str, phone: str, email: str = "", address: str = "",
                           items: List[OrderItem] = None, status="Accepted", pay_status="Unpaid"):
        timestamp = datetime.now()
        order_id = generate_order_id(timestamp)
        order = cls(
            order_id=order_id,
            order_time=timestamp,
            name=name,
            phone=phone,
            email=email,
            address=address,
            order_items=items or [],
            cart_total=sum(item.price * item.quantity for item in items) if items else 0.0,
            status=status,
            pay_status=pay_status
        )
        return order

    def to_row(self) -> List:
        return [
            self.order_id,
            self.order_time.strftime("%Y-%m-%d %H:%M:%S"),
            self.name,
            self.phone,
            self.email,
            self.address,
            self.cart_total,
            json.dumps([item.to_row() for item in self.order_items], ensure_ascii=False),
            self.status,
            self.pay_status
        ]
