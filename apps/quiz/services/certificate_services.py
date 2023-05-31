import io
import os
from typing import Tuple

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def insert_text_to_pdf(x, y, font_path, text, input_pdf, pagesize: Tuple):
    # Generate text
    packet = io.BytesIO()
    canvas = Canvas(packet, pagesize=pagesize)
    font_name = os.path.splitext(os.path.basename(font_path))[0]
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    canvas.setFont(font_name, 20)
    canvas.drawCentredString(x, y, text)
    canvas.save()

    # Merge text + template
    input = PdfReader(open(input_pdf, "rb"))
    canvas_pdf = PdfReader(packet)
    page = input.pages[0]
    page.merge_page(canvas_pdf.pages[0])

    # Output stream
    output = PdfWriter()
    output.add_page(page)
    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)

    return output_stream
