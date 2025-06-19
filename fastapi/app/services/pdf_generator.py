import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, XPreformatted
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


class PDFGenerator:
    def __init__(self, title: str = "Document"):
        self._pdf_data = None

        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer, pagesize=A4)
        self.elements = []
        self.styles = getSampleStyleSheet()
        self.title = title

    def add_text(self, text, style ="BodyText"):
        paragraph = Paragraph(text, self.styles[style])
        self.elements.append(paragraph)
        self.elements.append(Spacer(1, 12))

    def add_preformatted_text(self, text, style="Code"):
        paragraph = XPreformatted(text, self.styles[style], dedent=3)
        self.elements.append(paragraph)
        self.elements.append(Spacer(1, 12))

    def add_table(self, data: list[list], sum_columns: list[int] = None):
        """
        Adds a table to the PDF.
        :param data: Table data including headers — list of lists.
        :param sum_columns: List of column indices to calculate totals for.
        """
        if not data:
            return

        # Calculate totals for specified columns
        if sum_columns:
            header, *rows = data
            sums = [''] * len(header)
            for col in sum_columns:
                try:
                    total = sum(float(row[col]) for row in rows if row[col] != '')
                    sums[col] = f"{total:.2f}"
                except Exception:
                    sums[col] = "Error"
            data.append(["TOTAL"] + sums[1:])  # Assumes first column is a description
        else:
            header, *rows = data

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def build_pdf(self) -> bytes:
        """
        Finalizes the PDF and returns the binary content.
        """
        self.doc.build(self.elements)
        self._pdf_data = self.buffer.getvalue()
        self.buffer.close()
        return self._pdf_data

    def get_base64(self) -> str:
        """
        Returns the PDF content as a Base64-encoded string.
        """
        if self._pdf_data is None:
            self.build_pdf()
        return base64.b64encode(self._pdf_data).decode('utf-8')