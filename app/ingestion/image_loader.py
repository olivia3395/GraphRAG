from PIL import Image
from pathlib import Path


def load_image(path: Path):
    return Image.open(path).convert("RGB")
