import hashlib
import random
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from PIL import Image, ImageDraw

from pascal.exceptions import InconsistentAnnotation
from pascal.utils import base64img

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


class PascalAnnotationMixin:
    """
    Provides useful annotation functionality:
        * draw annotations
        * convert to yolo
    """

    def __init__(self):
        self._objects = []

    @property
    def objects(self) -> List:
        return self._objects

    # TODO: refactor iterator
    def __iter__(self):
        self._n = 0
        return self

    def __len__(self):
        return len(self._objects)

    def __next__(self):
        if self._n < len(self):
            obj = self.objects[self._n]
            self._n += 1
            return obj
        else:
            raise StopIteration

    def check_annotation(self):
        if not hasattr(self, "size"):
            raise InconsistentAnnotation("Annotation has no attribute size")
        if not hasattr(self.size, "width"):
            raise InconsistentAnnotation("Annotation has no attribute size.width")
        if not hasattr(self.size, "height"):
            raise InconsistentAnnotation("Annotation has no attribute size.height")

    def check_objects(self):
        for obj in self:
            if not hasattr(obj, "name"):
                raise InconsistentAnnotation("Object has no attribute name")
            if not hasattr(obj, "bndbox"):
                raise InconsistentAnnotation("Object has no attribute bndbox")
            if not hasattr(obj.bndbox, "xmin"):
                raise InconsistentAnnotation("Object has no attribute bndbox.xmin")
            if not hasattr(obj.bndbox, "ymin"):
                raise InconsistentAnnotation("Object has no attribute bndbox.ymin")
            if not hasattr(obj.bndbox, "xmax"):
                raise InconsistentAnnotation("Object has no attribute bndbox.xmax")
            if not hasattr(obj.bndbox, "ymax"):
                raise InconsistentAnnotation("Object has no attribute bndbox.ymax")

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
        self.check_annotation()
        self.check_objects()
        objects = []
        for obj in self.objects:
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
        label_me_version: str = "4.5.6",
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
        self.check_annotation()
        self.check_objects()
        if not img_path.exists():
            raise FileNotFoundError(f"There no file: {img_path}")

        encoded_string = None
        if save_img_data:
            img = Image.open(img_path)
            encoded_string = base64img(img, img_path.suffix)

        shapes = []
        for obj in self:
            label = obj.name
            points = [
                [obj.bndbox.xmin, obj.bndbox.ymin],
                [obj.bndbox.xmax, obj.bndbox.ymin],
                [obj.bndbox.xmax, obj.bndbox.ymax],
                [obj.bndbox.xmin, obj.bndbox.ymax],
            ]
            shape = dict(
                label=label,
                points=points,
                group_id=None,
                shape_type="polygon",
                flags={},
            )
            shapes.append(shape)

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
