import hashlib
import logging
import random
from functools import lru_cache
from typing import Optional

from transliterate import translit
from PIL import Image, ImageDraw
from pascal.protocols import PascalObject as PascalObjectProtocol, PascalAnnotation, BndBox

random.seed(32)

n_colors = 100
RAND_COLORS = [
    (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    for _ in range(n_colors)
]


# TODO: add font, font size

@lru_cache
def get_name_hash(name: str) -> int:
    """
    https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    """
    return abs(int(hashlib.sha1(name.encode("utf-8")).hexdigest(), 16) % n_colors)


def is_reletive_coords(box: BndBox) -> bool:
    return any(c < 1 for c in [box.xmin, box.ymin, box.xmax, box.ymax])


class DrawObjectsMixin(PascalAnnotation):
    """
    Draw objects
    """

    def draw_boxes(
            self,
            image: Image.Image,
            width: int = 3,
            color: Optional[tuple[int, int, int]] = None,
            language_code: Optional[str] = None
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
        img_width = img_copy.width
        img_height = img_copy.height
        img_draw = ImageDraw.Draw(img_copy)
        set_color = color is None
        for obj in self.objects:
            if not isinstance(obj, PascalObjectProtocol):
                logging.warning("Annotation has object which is not PascalObject")
                continue
            if set_color:
                hash_id = get_name_hash(obj.name)
                color = RAND_COLORS[hash_id]
            # draw rectangle
            if is_reletive_coords(obj.bndbox):
                p1 = (float(obj.bndbox.xmin * img_width), float(obj.bndbox.ymin * img_height))
                p2 = (float(obj.bndbox.xmax * img_width), float(obj.bndbox.ymax * img_height))
            else:
                p1 = (float(obj.bndbox.xmin), float(obj.bndbox.ymin))
                p2 = (float(obj.bndbox.xmax), float(obj.bndbox.ymax))
            img_draw.rectangle((p1, p2), outline=color, width=width)
            # draw text
            text_coord = (
                float(p1[0] + width + 1),
                float(p1[1] + width + 1),
            )
            if language_code is not None:
                obj_name = translit(obj.name, language_code, reversed=True)
            else:
                obj_name = obj.name
            text_box = img_draw.textbbox(text_coord, obj_name)
            img_draw.rectangle(text_box, fill=(32, 32, 28))
            img_draw.text(text_coord, obj_name, align="left")
        return img_copy
