from pathlib import Path
from PIL import Image
import io

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm

def convert_to_webp(image_path: Path):
    destination = image_path.with_suffix(".webp")
    image = Image.open(image_path)
    image.save(destination, format="webp")
    return destination

# path = Path("D:\EcourseBE\image.png")
# convert_to_webp(path)

# ==============================================================================> draw text
def draw_svg(svg_file_path):
    pagesize = (33.867 * cm, 19.05 * cm)
    packet = io.BytesIO()
    can = Canvas(packet, pagesize=pagesize)

    drawing = svg2rlg(svg_file_path)
    drawing.scale(0.2, 0.2)  # Adjust the scale as needed
    drawing.width *= 0.2  # Adjust the width of the drawing
    drawing.height *= 0.2  # Adjust the height of the drawing
    renderPDF.draw(drawing, can, 100, 100)

    can.drawCentredString(100, 100, "diep hai binh")
    can.save()


