import json

from app.model.order import OrderItem, Order

def create_order(name: str, phone: str, email: str, address: str, cart_raw: str) -> Order:

    order = Order.from_customer_data(
        name=name,
        phone=phone,
        email=email,
        address=address
    )
    for item in json.loads(cart_raw):
        order.add_order_item(OrderItem.from_customer_data(**item))

    return order

def save_order(order: Order):
    from app.model.sheets import save_order
    save_order(order)