from typing import Dict, List

from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates

from app.api.dependencies import get_jinja_template, get_static_file_versions_for_index_page, get_orders, \
    get_group_products
from app.utils import logger
from app.model.sheets import update_order_status_by_row
from app.services.order_service import create_order, save_order

app_router = APIRouter()

@app_router.get("/api/", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_group_products)
) -> HTMLResponse:
    try:
        versions = get_static_file_versions_for_index_page()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "grouped_products": grouped_products,
            **versions
        })
    except FileNotFoundError:
        logger.error("index.html not found")
        return HTMLResponse(content="index.html not found", status_code=404)

@app_router.get("/api/lending", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_group_products)
) -> HTMLResponse:
    try:
        versions = get_static_file_versions_for_index_page()
        return templates.TemplateResponse("lending.html", {
            "request": request,
            "grouped_products": grouped_products,
            **versions
        })
    except FileNotFoundError:
        logger.error("index.html not found")
        return HTMLResponse(content="index.html not found", status_code=404)


@app_router.get("/api/get-order-form", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_group_products)
) -> HTMLResponse:
    try:
        versions = get_static_file_versions_for_index_page()
        return templates.TemplateResponse("order_form.html", {
            "request": request,
            "grouped_products": grouped_products,
            **versions
        })
    except FileNotFoundError:
        logger.error("order_form.html not found")
        return HTMLResponse(content="index.html not found", status_code=404)

@app_router.get("/api/grouped-products", response_class=JSONResponse)
async def get_grouped_products(
        request: Request,
        grouped_products: Dict[str, str] = Depends(get_group_products)
) -> JSONResponse:
    return JSONResponse(content=grouped_products)

@app_router.route("/api/order", methods=["POST"])
async def order(
        request: Request,
) -> JSONResponse:
    form = await request.form()

    order = create_order(
        name=form.get("name"),
        phone=form.get("phone"),
        email=form.get("email", ""),
        address=form.get("address", ""),
        cart_raw=form.get("cart_data")
    )

    save_order(order)

    return JSONResponse(
        {
            "message": "Order received",
            "order_id": order.order_id
        })

@app_router.get("/api/orders")
def orders(
        request: Request,
        page: int = 1,
        per_page:
        int = 10,
        templates: Jinja2Templates = Depends(get_jinja_template),
        all_orders: Dict[str, str] = Depends(get_orders)
):
    total_orders = len(all_orders)
    start = (page - 1) * per_page
    end = start + per_page
    page_orders = all_orders[start:end]

    total_pages = (total_orders + per_page - 1) // per_page

    return templates.TemplateResponse("orders.html", {
            "request": request,
            "orders": page_orders,
            "page": page,
            "total_pages": total_pages}
    )

@app_router.post("/api/update_order_status")
async def update_order_status(
        request: Request,
        all_rows = Depends(get_orders)
):
    form = await request.form()
    order_id = form.get("order_id")
    new_status = form.get("status")

    if not order_id or not new_status:
        return PlainTextResponse("Missing order_id or status", status_code=400)

    order_row = None

    for i, row in enumerate(all_rows, start=2):
        if row['order_id'] == order_id:
            order_row = i
            break

    if order_row:
        update_order_status_by_row(order_row, new_status)
        return PlainTextResponse(f"Order status updated to: {new_status}")
    else:
        return PlainTextResponse("Order not found", status_code=404)
