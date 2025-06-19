from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from io import BytesIO
import base64

from premailer import transform
from datetime import timedelta

from weasyprint import HTML

from typing import Optional

from app.models.order.order import Order
from app.models.order.order_service import get_order
from app.services.pdf_generator import PDFGenerator
from app.common.utils import get_template

def _generate_invoice_base64(order_data: Order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, f"INVOICE{order_data.order_id}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {order_data.order_time}")

    c.drawString(50, height - 110, "From: {Coffee_Company}")
    c.drawString(300, height - 110, f"To: {order_data.name} ({order_data.email})")

    y = height - 160
    total = 0
    for item in order_data.order_items:
        c.drawString(50, y, item.name)
        c.drawString(300, y, str(item.quantity))
        c.drawString(400, y, f"${item.price:.2f}")
        c.drawString(500, y, f"${item.summ:.2f}")
        total += item.summ
        y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, y - 20, "Total:")
    c.drawString(400, y - 20, f"${total:.2f}")

    c.save()

    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Convert to base64
    encoded = base64.b64encode(pdf_bytes).decode("utf-8")
    return encoded

def __generate_invoice_base64(order_data: Order):
    pdf_gen = PDFGenerator("Invoice")

    pdf_gen.add_text(f"INVOICE {order_data.order_id}", "Title")
    pdf_gen.add_text(f"Date: {order_data.order_time}", "Heading2")

    pdf_gen.add_text("From: {Coffee_Company}", "Heading4")
    pdf_gen.add_text(f"To: {order_data.name} ({order_data.email})", "Heading4")

    pdf_gen.add_preformatted_text('''

    This is a non rearranging form of the <b>Paragraph</b> class;
   <b><font color=red>XML</font></b> tags are allowed in <i>text</i> and
    have the same meanings as for the <b>Paragraph</b> class.
   As for <b>Preformatted</b>, if dedent is non zero
    <font color="red" size="+1">dedent</font>
       common leading spaces will be removed from the
   front of each line.
   You can have &amp;amp; style entities as well for &amp; &lt; &gt; and &quot;.
   
    ''')

    pdf_gen.add_table(order_data.order_items_to_table(), sum_columns=[4])
    pdf_base64 = pdf_gen.get_base64()

    return pdf_base64

def get_invoice_data(order_data: Order):

    dt = order_data.order_time
    due_date = dt + timedelta(days=15)

    context = {
        "logo_base64": encode_image_base64("app/templates/logo.png"),
        "format_data_1": dt.strftime("%b '%Y"),
        "format_data_2": dt.strftime("%d%m%y"),
        "format_data_3": dt.strftime("%d %b %Y"),
        "due_date_format_data_3": due_date.strftime("%d %b %Y"),
        "client":    {
                    "company": order_data.name,
                    "registration": order_data.email,
                    "address": order_data.address,
                    "postcode": order_data.phone
                    },
        "services": order_data.order_items,
        "total_amount": format_number(order_data.cart_total),
    }

    return context

def encode_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

def format_number(value):
    return f"{value:,.2f}"

def generate_invoice_html(order_data: Order):

    context = get_invoice_data(order_data)

    template = get_template('invoice_template.html')

    html_content = template.render(
        format_number=format_number,
        **context
    )

    return html_content

def generate_invoice_base64(order_data: Order):

    html_content = generate_invoice_html(order_data)

    html_content_inlined = transform(html_content)

    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)

    pdf_base64 = base64.b64encode(pdf_io.read()).decode('utf-8')

    return pdf_base64

def get_pdf_invoice_by_id(invoice_id: int) -> Optional[bytes]:
    """
    Retrieves and decodes the base64-encoded PDF invoice for a given order ID.

    Args:
        invoice_id (int): The unique ID of the invoice (same as order_id).

    Returns:
        bytes | None: The decoded PDF data if found, else None.
    """
    order = get_order(invoice_id)

    if not order:
        return None

    encoded_invoice = order.base64_invoice
    if not encoded_invoice:
        return None

    try:
        pdf_data = base64.b64decode(encoded_invoice)
        return pdf_data
    except:
        return None
