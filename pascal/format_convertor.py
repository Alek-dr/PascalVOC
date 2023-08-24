import logging
from pathlib import Path
from typing import List, Union

from PIL import Image

from pascal.exceptions import InconsistentAnnotation
from pascal.protocols import PascalAnnotation, PascalObject, Size
from pascal.utils import _is_primitive, base64img


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


class FormatConvertorMixin(PascalAnnotation):
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
            try:
                label = labels_map[obj.name]
            except KeyError:
                logging.warning(f"No label {obj.name} in label map. Skip object")
                continue
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
        if save_img_data:
            img_path = Path(img_path)
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
