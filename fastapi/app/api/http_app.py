from typing import Dict

from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates

from app.api.http_app_dependencies import get_jinja_template, get_static_file_versions_for_index_page
from app.common.utils import logger
from app.models.order.order_service import create_order, save_order, get_orders, update_order_status_by_row
from app.models.order.order_schema import OrderCreate
from app.models.product.product_service import get_products_group_by_group
from app.models.order.order_invoice import generate_invoice_base64, get_pdf_invoice_by_id

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_products_group_by_group)
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

@router.get("/lending", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_products_group_by_group)
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


@router.get("/get-order-form", response_class=HTMLResponse)
async def render_index_page(
        request: Request,
        templates: Jinja2Templates = Depends(get_jinja_template),
        grouped_products: Dict[str, str] = Depends(get_products_group_by_group)
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

@router.get("/grouped-products", response_class=JSONResponse)
async def get_grouped_products(
        grouped_products: Dict[str, str] = Depends(get_products_group_by_group)
) -> JSONResponse:
    return JSONResponse(content=grouped_products)

@router.post("/order")
async def order(
        data: OrderCreate = Depends(OrderCreate.as_form)
) -> JSONResponse:

    order_data = create_order(data)

    base64_invoice = generate_invoice_base64(order_data)
    order_data.base64_invoice = base64_invoice

    save_order(order_data)

    return JSONResponse(
        {
            "message": "Order received",
            "order_id": order_data.order_id,
            "base64_invoice_url": f"/api/invoice/{order_data.order_id}",
            "base64_invoice": base64_invoice,
        })

@router.get("/order/invoice/{order_id}")
def get_invoice(order_id):

    pdf = get_pdf_invoice_by_id(order_id)

    if not pdf:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=invoice_{order_id}.pdf"
        }
    )

@router.get("/order/orders")
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

@router.post("/order/update_order_status")
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
