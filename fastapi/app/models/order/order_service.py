import json

from app.models.order.order import OrderItem, Order
from app.models.order.order_schema import OrderCreate

from app.services.google_sheets_service import append_row_to_sheet, append_rows_to_sheet, get_all_records, update_sheet_cell, \
    find_row_by_value, read_row

_SHEET_NAME_ORDER = "orders"
_SHEET_NAME_ORDER_DATA = "orders_data"
_ORDER_STATUS_COL_NUM = 9

def get_orders():
    return get_all_records(_SHEET_NAME_ORDER)

def create_order(data: OrderCreate) -> Order:

    order = Order.from_customer_data(**data.dict(exclude={"cart_data"}))

    for item in json.loads(data.cart_data):
        order.add_order_item(OrderItem.from_customer_data(**item))

    return order

def save_order(order: Order):
    append_row_to_sheet(_SHEET_NAME_ORDER, order.to_row())
    append_rows_to_sheet(_SHEET_NAME_ORDER_DATA, [item.to_row() for item in order.order_items])

def get_order(order_id) -> Order:
    row_index = find_row_by_value(_SHEET_NAME_ORDER, "order_id", order_id)

    if row_index:
        row = read_row(_SHEET_NAME_ORDER, row_index)
        return Order.from_row(row)

    return None

def update_order_status_by_row(order_row: int, new_status):
    update_sheet_cell(_SHEET_NAME_ORDER, order_row, _ORDER_STATUS_COL_NUM, new_status)