from dataclasses import dataclass
from pathlib import Path
from typing import Union, List

from pascal.exceptions import InconsistentAnnotation
from xmlobj.xmlmapping import XMLMixin

from pascal.draw_objects import DrawObjectsMixin
from pascal.protocols import PascalObject as PascalObjectProtocol
from pascal.protocols import BndBox as BndBoxProtocol
from pascal.protocols import Size as SizeProtocol



@dataclass
class BBox(BndBoxProtocol, XMLMixin):
    xmin: Union[float, int]
    ymin: Union[float, int]
    xmax: Union[float, int]
    ymax: Union[float, int]


@dataclass
class PascalObject(PascalObjectProtocol, XMLMixin):
    name: str
    bndbox: BBox


@dataclass
class Size(SizeProtocol, XMLMixin):
    width: Union[float, int]
    height: Union[float, int]


class PascalAnnotation(DrawObjectsMixin, XMLMixin):

    def __init__(self, filename: Union[Path, str], objects: List[PascalObject], size: Size):
        self.filename = filename
        self.objects = objects
        self.size = size

    @classmethod
    def from_yolo(cls, ann_path: Union[str, Path], label_map: dict, img_w: int = 1, img_h: int = 1):
        objects = []
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
            name = label_map[class_id]
            box = BBox(x1, y1, x2, y2)
            pobj = PascalObject(name, box)
            objects.append(pobj)
        ann = cls(Path(ann_path).stem, objects, Size(img_w, img_h))
        if not isinstance(ann, PascalAnnotation):
            raise InconsistentAnnotation(f"Cannot make annotation from file: {ann_path}")
        return ann
