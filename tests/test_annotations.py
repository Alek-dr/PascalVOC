import pytest
from xmlobj.xmlmapping import get_xml_obj

from pascal import annotation_from_xml
from pascal.exceptions import InconsistentAnnotation
from pascal.protocols import PascalAnnotation, PascalObject


def check_attributes(obj, attr_params):
    attr_name = attr_params.get("attr_name")
    attr_val = attr_params.get("attr_val")
    assert hasattr(obj, attr_name)
    if isinstance(attr_val, list):
        for item in attr_val:
            check_attributes(getattr(obj, attr_name), item)
    else:
        attr_type = attr_params.get("dtype")
        assert isinstance(getattr(obj, attr_name), attr_type)


def has_object(ann: PascalAnnotation, target_object: dict) -> bool:
    for obj in ann:
        match = True
        for k, v in target_object.items():
            attr_val = getattr(obj, k)
            if k == "bndbox":
                if (
                    v["xmin"] != attr_val.xmin
                    or v["xmax"] != attr_val.xmax
                    or v["ymin"] != attr_val.ymin
                    or v["ymax"] != attr_val.ymax
                ):
                    match = False
                    break
            else:
                if attr_val != v:
                    match = False
                    break
        if match:
            return True
    return False


def test_valid(valid_annotations):
    """
    Проверить параметры валидных аннотаций
    """
    for ann_sample in valid_annotations:
        ann_file = ann_sample.get("file")
        ann = annotation_from_xml(ann_file)
        for attributes in ann_sample.get("attributes"):
            check_attributes(ann, attributes)
        objects = ann_sample.get("objects")
        if objects is not None:
            for obj in objects:
                assert has_object(ann, obj)


def test_invalid_annotations(invalid_ann_files):
    """
    Ошибка парсинга невалидных аннотаций
    """
    for file in invalid_ann_files:
        with pytest.raises(InconsistentAnnotation):
            annotation_from_xml(file)


def test_valid_objects(valid_objects):
    """
    Проверить параметры объектов
    """
    for obj_params in valid_objects:
        objects = get_xml_obj(obj_params.get("file"))
        assert hasattr(objects, "object")
        for obj in objects.object:
            assert isinstance(obj, PascalObject)


def test_invalid_objects(invalid_objects):
    """
    Проверить невалидные объекты
    """
    for obj_params in invalid_objects:
        objects = get_xml_obj(obj_params.get("file"))
        assert hasattr(objects, "object")
        for obj in objects.object:
            assert not isinstance(obj, PascalObject)
