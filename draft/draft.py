from pathlib import Path
from PIL import Image
from pypdf import PdfReader, PdfWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch, cm


def convert_to_webp(image_path: Path):
    destination = image_path.with_suffix(".webp")
    image = Image.open(image_path)
    image.save(destination, format="webp")
    return destination

# path = Path("D:\EcourseBE\image.png")
# convert_to_webp(path)

# ==============================================================================> draw text
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

pagesize = (33.867 * cm, 19.05 * cm)
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=pagesize)

svg_file = "5.svg"
drawing = svg2rlg(svg_file)
drawing.scale(0.2, 0.2)  # Adjust the scale as needed
drawing.width *= 0.2  # Adjust the width of the drawing
drawing.height *= 0.2  # Adjust the height of the drawing

renderPDF.draw(drawing, can, 100, 100)

# can.drawCentredString(100, 100, "diep hai binh")
can.save()

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open("pdf_file.pdf", "rb"))
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real file
output_stream = open("destination.pdf", "wb")
output.write(output_stream)
output_stream.close()




