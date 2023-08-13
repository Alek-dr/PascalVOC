from copy import deepcopy
from pathlib import Path
from typing import Optional, Union

from xmlobj import get_xml_obj
from xmlobj.xmlmapping import XMLMixin

from pascal.exceptions import InconsistentAnnotation, ParseException
from pascal.pascal_annotation import (PascalAnnotationMixin,
                                      is_pascal_annotation)
from pascal.utils import _is_primitive


def annotation_from_xml(
    file_path: Union[str, Path], attr_type_spec: Optional[dict] = None
) -> Union[XMLMixin, PascalAnnotationMixin]:
    """
    Make annotation object from PascalVOC annotation file

    Parameters
    ----------
    file: path to xml file
    attr_type_spec: dict, optional
        specify attribute types to explicitly cast attribute values

    Returns
    -------
    Annotation object
    """
    try:
        obj = get_xml_obj(
            file_path, mixin_cls=PascalAnnotationMixin, attr_type_spec=attr_type_spec
        )
    except Exception as ex:
        raise ParseException(ex)
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
    if not is_pascal_annotation(obj):
        raise InconsistentAnnotation(f"File {file_path} is not PascalVOCAnnotation")
    return obj
