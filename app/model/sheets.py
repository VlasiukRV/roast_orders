import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.model.order import Order

def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_service_account_file.json", scope)
    client = gspread.authorize(creds)
    return client.open("Roaster Orders").worksheet(sheet_name)

def save_order(order: Order):
    sheet = get_sheet("orders")
    sheet.append_row(order.to_row())

    sheet = get_sheet("orders_data")
    for item in order.order_items:
        sheet.append_row(item.to_row())


def add_order_to_sheet(data):
    sheet = get_sheet("orders")
    sheet.append_row(data)

def add_order_data_to_sheet(data):
    sheet = get_sheet("orders_data")
    sheet.append_row(data)

def get_orders():
    sheet = get_sheet("orders")
    return sheet.get_all_records()

def load_products():
    sheet = get_sheet("products")
    return sheet.get_all_records()

def update_order_status_by_row(order_row, new_status):
    sheet = get_sheet("orders")
    sheet.update_cell(order_row, 9, new_status)