import hashlib
import logging
import random
from functools import lru_cache
from pathlib import Path
from typing import Optional

import PIL.ImageFont
from PIL import Image, ImageDraw
from transliterate import translit

from pascal.protocols import BndBox, PascalAnnotation
from pascal.protocols import PascalObject as PascalObjectProtocol

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


def is_relative_coords(box: BndBox) -> bool:
    return any(c < 1 for c in [box.xmin, box.ymin, box.xmax, box.ymax])


def _get_rect_coords(text_coord, d):
    x0 = text_coord[0] - d if text_coord[0] - 1 >= 0 else text_coord[0]
    y0 = text_coord[1] - d if text_coord[1] - 1 >= 0 else text_coord[1]
    x1 = text_coord[2] + d
    y1 = text_coord[3] + d
    return x0, y0, x1, y1


class DrawObjectsMixin(PascalAnnotation):
    """
    Draw objects
    """

    _font_path = str(Path(__file__).parent / "fonts/arialmt.ttf")

    def draw_boxes(
        self,
        image: Image.Image,
        width: int = 5,
        color: Optional[tuple[int, int, int]] = None,
        fontsize: int = 10,
        font_path: str = None,
        language_code: Optional[str] = None,
    ) -> Image.Image:
        """
        Draw bounding boxes and obj names

        Parameters
        ----------
        image: Pillow image
        width: The line width, in pixels
        color: bounding box color
        fontsize: requested font size, in pixels
        font_path: path to font
        language_code: str language code if transliteration needs

        Returns
        -------
        Copy of image with rendered boxes
        """
        img_copy = image.copy()
        img_width = img_copy.width
        img_height = img_copy.height
        img_draw = ImageDraw.Draw(img_copy)
        set_color = color is None
        if font_path is not None:
            font = PIL.ImageFont.truetype(font_path, size=fontsize)
        else:
            font = PIL.ImageFont.truetype(self._font_path, size=fontsize)
        for obj in self.objects:
            if not isinstance(obj, PascalObjectProtocol):
                logging.warning("Annotation has object which is not PascalObject")
                continue
            if set_color:
                hash_id = get_name_hash(str(obj.name))
                color = RAND_COLORS[hash_id]
            # draw rectangle
            if is_relative_coords(obj.bndbox):
                p1 = (
                    float(obj.bndbox.xmin * img_width),
                    float(obj.bndbox.ymin * img_height),
                )
                p2 = (
                    float(obj.bndbox.xmax * img_width),
                    float(obj.bndbox.ymax * img_height),
                )
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
                obj_name = str(translit(obj.name, language_code, reversed=True))
            else:
                obj_name = str(obj.name)
            text_box = img_draw.textbbox(text_coord, obj_name, font=font)
            rect_coords = _get_rect_coords(text_box, width // 2)
            img_draw.rectangle(rect_coords, fill=(32, 32, 28))
            img_draw.text(text_coord, obj_name, align="left", font=font)
        return img_copy
