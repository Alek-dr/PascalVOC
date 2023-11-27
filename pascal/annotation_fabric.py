from copy import deepcopy
from pathlib import Path
from typing import Optional, Union

from xmlobj import get_xml_obj
from xmlobj.xmlmapping import XMLMixin

from pascal.draw_objects import DrawObjectsMixin
from pascal.exceptions import InconsistentAnnotation, ParseException
from pascal.format_convertor import FormatConvertorMixin
from pascal.protocols import PascalAnnotation, Size
from pascal.utils import _is_primitive


def annotation_from_xml(
    file_path: Union[str, Path], attr_type_spec: Optional[dict] = None
) -> Union[PascalAnnotation, DrawObjectsMixin, FormatConvertorMixin, XMLMixin]:
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
            file_path,
            mixin_clsasses=[DrawObjectsMixin, FormatConvertorMixin],
            attr_type_spec=attr_type_spec,
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
        setattr(obj, "objects", objects)
        delattr(obj, "object")
    if isinstance(obj, PascalAnnotation):
        if (obj.filename is None and len(obj.objects) == 0) or not isinstance(
            obj.size, Size
        ):
            raise InconsistentAnnotation(f"File {file_path} is not PascalVOCAnnotation")
    return obj
