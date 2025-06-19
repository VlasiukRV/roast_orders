from typing import Dict, List
from collections import defaultdict

from app.services.google_sheets_service import get_all_records

_SHEET_NAME_PRODUCT = "products"

def get_products():
    return get_all_records(_SHEET_NAME_PRODUCT, True)

def get_products_group_by_group() -> Dict[str, List[Dict]]:
    products = get_products()

    grouped = defaultdict(list)
    for product in products:
        group = product.get('group', 'Uncategorized')
        grouped[group].append(product)

    result = dict(grouped)

    return result