import base64
from io import BytesIO

from PIL import Image


def _is_primitive(obj):
    """
    https://stackoverflow.com/questions/6391694/how-to-check-if-a-variables-type-is-primitive
    """
    return not hasattr(obj, "__dict__")


def base64img(img: Image.Image, img_suffix: str) -> str:
    """
    Convert image to base64
    """
    buffered = BytesIO()
    if img_suffix in [".JPG", ".jpg", ".JPEG", ".jpeg"]:
        format_ = "JPEG"
    elif img_suffix in [".PNG", ".png"]:
        format_ = "PNG"
    else:
        format_ = "PNG"
    img.save(buffered, format=format_)
    buffered.seek(0)
    img_byte = buffered.getvalue()
    encoded_string = base64.b64encode(img_byte).decode("utf-8")
    return encoded_string
