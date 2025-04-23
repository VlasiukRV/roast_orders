import os
from typing import Dict, List
from collections import defaultdict

from starlette.templating import Jinja2Templates

from app.model.sheets import load_products, get_orders
from app.utils import generate_version


def get_jinja_template()-> Jinja2Templates:
    return Jinja2Templates(directory="app/templates")

def get_static_file_versions_for_index_page() -> Dict[str, str]:
    js_file_version = generate_version(os.path.join('/app/static/js/', 'main.js'))
    css_file_version = generate_version(os.path.join('/app/static/css/', 'styles.css'))
    return {"js_file_version": js_file_version, "css_file_version": css_file_version}


def get_static_file_versions_for_admin_page() -> Dict[str, str]:
    js_file_version = generate_version(os.path.join('/app/static/js/', 'settings.js'))
    css_file_version = generate_version(os.path.join('/app/static/css/', 'styles.css'))
    return {"js_file_version": js_file_version, "css_file_version": css_file_version}

def get_group_products() -> Dict[str, List[Dict]]:
    products = load_products()

    grouped = defaultdict(list)
    for product in products:
        group = product.get('group', 'Uncategorized')
        grouped[group].append(product)
    return dict(grouped)

def get_products()-> Dict[str, str]:
    return load_products()

def get_all_orders()-> Dict[str, str]:
    return get_orders()