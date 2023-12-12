import base64
import xml.etree.ElementTree as xml
from io import BytesIO
from pathlib import Path
from typing import Union

from PIL import Image
from xmlobj import XMLMixin


def _is_primitive(obj):
    """
    https://stackoverflow.com/questions/6391694/how-to-check-if-a-variables-type-is-primitive
    """
    return not hasattr(obj, "__dict__") and not isinstance(obj, list)


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


def save_xml(output: Union[str, Path], xml_obj):
    """
    Save object to output file
    """
    tree = xml.ElementTree(xml_obj)
    xml.indent(tree, space="    ", level=0)
    with open(output, "w") as out:
        tree.write(out, encoding="unicode", method="xml")


def _set_attr(box, obj_type, clip_zero: bool = True):
    for attr_name, attr_val in box.__dict__.items():
        attr_val = obj_type(attr_val)
        if clip_zero:
            attr_val = obj_type(max(0, attr_val))
        setattr(box, attr_name, attr_val)
    return box


def _check_bnd_box(box: XMLMixin, clip_zero: bool = True):
    attr_types = [type(attr) for attr in box.__dict__.values()]
    if all(attr is int or attr is float for attr in attr_types):
        return box
    if any(attr is float for attr in attr_types):
        val_type = float
    else:
        val_type = int
    box = _set_attr(box, val_type, clip_zero)
    return box
