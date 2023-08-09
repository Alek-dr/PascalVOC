from copy import deepcopy
from pathlib import Path
from typing import List, Union, Optional

from xmlobj import get_xml_obj
from xmlobj.xmlmapping import XMLMixin

from pascal import ParseException
from pascal.utils import _is_primitive


class PascalAnnotationMixin:

    def __init__(self):
        self._objects = []

    @property
    def objects(self) -> List:
        return self._objects

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


ann_type = type('Annotation', (XMLMixin, PascalAnnotationMixin), {})


def annotation_from_xml(file_path: Union[str, Path], attr_type_spec: Optional[dict] = None) -> ann_type:
    obj = get_xml_obj(file_path, mixin_cls=PascalAnnotationMixin, attr_type_spec=attr_type_spec)
    if hasattr(obj, "object"):
        obj_ = getattr(obj, "object")
        if isinstance(obj_, list):
            objects = [deepcopy(obj) for obj in obj_]
        elif not _is_primitive(obj_):
            objects = [deepcopy(obj_)]
        else:
            raise ParseException("Cannot parse objects")
        setattr(obj, "_objects", objects)
        delattr(obj, "object")
    return obj
