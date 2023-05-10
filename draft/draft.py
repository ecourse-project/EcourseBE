from pathlib import Path
from PIL import Image


def convert_to_webp(image_path: Path):
    destination = image_path.with_suffix(".webp")
    image = Image.open(image_path)
    image.save(destination, format="webp")
    return destination

path = Path("D:\EcourseBE\image.png")
convert_to_webp(path)