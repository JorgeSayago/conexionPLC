from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import io

# 📌 Base genérica para tablas
def _crear_pdf_tabla(data, titulo="Reporte", img_bytes=None):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"📄 {titulo}")
    y -= 30

    if img_bytes:
        try:
            imagen = ImageReader(io.BytesIO(img_bytes))
            c.drawImage(imagen, 50, y - 250, width=500, preserveAspectRatio=True)
            y -= 270
        except:
            y -= 20

    if data:
        headers = list(data[0].keys())
        rows = [headers] + [list(d.values()) for d in data]

        table = Table(rows, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        w, h = table.wrapOn(c, width - 100, height)
        table.drawOn(c, 50, y - h)

    c.save()
    buffer.seek(0)
    return buffer
