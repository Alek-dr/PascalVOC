import hashlib
import logging
import random
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from PIL import Image, ImageDraw
from typing_extensions import Protocol, runtime_checkable

from pascal.exceptions import InconsistentAnnotation, ParseException
from pascal.pascal_object import PascalObject
from pascal.utils import _is_primitive, base64img

random.seed(32)

n_colors = 100
RAND_COLORS = [
    (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    for _ in range(n_colors)
]


@lru_cache
def get_name_hash(name: str) -> int:
    """
    https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    """
    return abs(int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % n_colors)


@runtime_checkable
class Size(Protocol):
    width: Union[float, int]
    height: Union[float, int]


def get_shapes(obj_data) -> List[dict]:
    if len(obj_data) == 0:
        return []
    shapes = []
    for obj in obj_data:
        if not isinstance(obj, PascalObject):
            logging.warning("Annotation has object which is not PascalObject")
            continue
        label = obj.name
        points = [
            [obj.bndbox.xmin, obj.bndbox.ymin],
            [obj.bndbox.xmax, obj.bndbox.ymin],
            [obj.bndbox.xmax, obj.bndbox.ymax],
            [obj.bndbox.xmin, obj.bndbox.ymax],
        ]
        obj_flags = {}
        for k, v in obj.__dict__.items():
            if _is_primitive(v) and k != "name":
                obj_flags[k] = v
            if isinstance(v, list):
                shapes.extend(get_shapes(v))
        shape = dict(
            label=label,
            points=points,
            group_id=None,
            shape_type="polygon",
            flags=obj_flags,
        )
        shapes.append(shape)
    return shapes


class PascalAnnotationMixin:
    """
    Provides useful annotation functionality:
        * draw annotations
        * convert to yolo
        * convert to labelme
    """

    def __init__(self):
        self._objects: List[PascalObject] = []
        self._size: Optional[Size] = None
        self.filename: Optional[str] = None

    @property
    def objects(self) -> List:
        return self._objects

    @property
    def size(self) -> Size:
        return self._size

    @size.setter
    def size(self, value):
        if isinstance(value, Size):
            self._size = value
        else:
            raise ParseException(f"Incorrect size block: {value}")

    def __len__(self):
        return len(self._objects)

    def __getitem__(self, item):
        return self._objects[item]

    def draw_boxes(
        self,
        image: Image.Image,
        width: int = 3,
        color: Optional[tuple[int, int, int]] = None,
    ) -> Image.Image:
        """
        Draw bounding boxes and obj names

        Parameters
        ----------
        image: Pillow image
        width: The line width, in pixels.
            specify attribute types to explicitly cast attribute values
        color: bounding box color

        Returns
        -------
        Copy of image with rendered boxes
        """
        img_copy = image.copy()
        img_draw = ImageDraw.Draw(img_copy)
        set_color = color is None
        for obj in self:
            if not isinstance(obj, PascalObject):
                logging.warning("Annotation has object which is not PascalObject")
                continue
            if set_color:
                hash_id = get_name_hash(obj.name)
                color = RAND_COLORS[hash_id]
            # draw rectangle
            p1 = (float(obj.bndbox.xmin), float(obj.bndbox.ymin))
            p2 = (float(obj.bndbox.xmax), float(obj.bndbox.ymax))
            img_draw.rectangle((p1, p2), outline=color, width=width)
            # draw text
            text_coord = (
                float(obj.bndbox.xmin + width + 1),
                float(obj.bndbox.ymin + width + 1),
            )
            text_box = img_draw.textbbox(text_coord, obj.name)
            img_draw.rectangle(text_box, fill=(32, 32, 28))
            img_draw.text(text_coord, obj.name, align="left")
        return img_copy

    def to_yolo(self, labels_map: dict, precision: int = 3) -> str:
        """
        Convert annotation to yolo format str
        Annotation object must have size attribute, which contains fields: width, height

        Parameters
        ----------
        labels_map: dict of label ids
            {"person": 0, "cat": 1, "dog": 2}
        precision: int, coord precision

        Returns
        -------
        Yolo format annotation str
        """
        if not isinstance(self.size, Size):
            raise InconsistentAnnotation(
                "Incorrect size. Size must have width and height attributes"
            )

        objects = []
        for obj in self:
            if not isinstance(obj, PascalObject):
                logging.warning("Annotation has object which is not PascalObject")
                continue
            label = labels_map[obj.name]
            dx = float(obj.bndbox.xmax - obj.bndbox.xmin)
            dy = float(obj.bndbox.ymax - obj.bndbox.ymin)
            x = obj.bndbox.xmin + dx * 0.5
            y = obj.bndbox.ymin + dy * 0.5
            dx /= self.size.width
            dy /= self.size.height
            x /= self.size.width
            y /= self.size.height
            s = f"{label} {x:.{precision}f} {y:.{precision}f} {dx:.{precision}f} {dy:.{precision}f}"
            objects.append(s)
        return "\n".join(objects)

    def to_labelme(
        self,
        img_path: Union[str, Path] = None,
        save_img_data: bool = False,
        label_me_version: str = "5.3.0",
    ) -> dict:
        """
        Convert annotation to labelme format

        Parameters
        ----------
        img_path: path to image
        save_img_data: if true store encoded image in output dict
        label_me_version: version of labelme app

        Returns
        -------
        labelme annotation dict which can be saved as json
        """
        if not img_path.exists():
            raise FileNotFoundError(f"No such file: {img_path}")

        encoded_string = None
        if save_img_data:
            img = Image.open(img_path)
            encoded_string = base64img(img, img_path.suffix)

        shapes = get_shapes(self.objects)

        res = dict(
            version=label_me_version,
            flags={},
            shapes=shapes,
            imagePath=str(img_path),
            imageData=encoded_string,
            imageHeight=self.size.height,
            imageWidth=self.size.width,
        )
        return res


def is_pascal_annotation(obj) -> bool:
    if obj.filename is not None:
        if isinstance(obj.size, Size):
            if len(obj.objects):
                if any(isinstance(obj, PascalObject) for obj in obj):
                    return True
            else:
                return True
    return False
