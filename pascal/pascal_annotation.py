import logging
from pathlib import Path
from typing import List, Optional, Union

from xmlobj.xmlmapping import XMLMixin

from pascal.draw_objects import DrawObjectsMixin
from pascal.exceptions import InconsistentAnnotation
from pascal.protocol_implementations import BBox, PascalObject, Size


class PascalAnnotation(DrawObjectsMixin, XMLMixin):
    def __init__(
        self, filename: Union[Path, str], objects: List[PascalObject], size: Size
    ):
        self.filename = filename
        self.objects = objects
        self.size = size


def annotation_from_yolo(
    ann_path: Union[str, Path],
    img_w: int = 1,
    img_h: int = 1,
    label_map: Optional[dict] = None,
) -> PascalAnnotation:
    """
    Get annotation object from yolo ann file

    Parameters
    ----------
    ann_path: path to yolo annotation
    img_w: image width, px
    img_h: image height, px
    label_map: dict of labels and correspond ids, example:
        label_map = {0: "person", 1: "dog"}
    Returns
    -------
    PascalAnnotation object
    """
    objects = []
    has_label_map = label_map is not None
    with open(ann_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        vals = line.split(" ")
        class_id = int(vals[0])
        x = float(vals[1])
        y = float(vals[2])
        dx = float(vals[3]) * 0.5
        dy = float(vals[4]) * 0.5
        x1 = x - dx
        x2 = x + dx
        y1 = y - dy
        y2 = y + dy
        x1 *= img_w
        x2 *= img_w
        y1 *= img_h
        y2 *= img_h
        if has_label_map:
            try:
                name = label_map[class_id]
            except KeyError:
                name = str(class_id)
                logging.warning(f"No id {class_id} in label map")
        else:
            name = str(class_id)
        box = BBox(x1, y1, x2, y2)
        pobj = PascalObject(name, box)
        objects.append(pobj)
    ann = PascalAnnotation(Path(ann_path).stem, objects, Size(img_w, img_h))
    if not isinstance(ann, PascalAnnotation):
        raise InconsistentAnnotation(f"Cannot make annotation from file: {ann_path}")
    return ann
