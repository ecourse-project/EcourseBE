import io
import os
from typing import Tuple, List, Dict
from itertools import groupby

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def group_by_font(attrs: List[Dict]):
    attrs.sort(key=lambda x: x["font"])
    return {key: list(group) for key, group in groupby(attrs, key=lambda x: x["font"])}


def draw_string(canvas: Canvas, draw_attr: List[Dict]):
    group_by_font_attrs = group_by_font(draw_attr)

    for font, attrs in group_by_font_attrs.items():
        font_name = os.path.splitext(os.path.basename(font))[0]
        pdfmetrics.registerFont(TTFont(font_name, font))
        for attr in attrs:
            canvas.setFont(font_name, attr["size"])
            canvas.setFillColorRGB(attr["color"][0], attr["color"][1], attr["color"][2])
            if attr["draw_type"].lower() == "right":
                canvas.drawRightString(attr["x"], attr["y"], attr["text"])
            elif attr["draw_type"].lower() == "center":
                canvas.drawCentredString(attr["x"], attr["y"], attr["text"])
            else:
                canvas.drawString(attr["x"], attr["y"], attr["text"])


def insert_text_to_pdf(attrs: List[Dict], input_pdf, pagesize: Tuple):
    # Generate text
    packet = io.BytesIO()
    canvas = Canvas(packet, pagesize=pagesize)
    draw_string(canvas, attrs)
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
