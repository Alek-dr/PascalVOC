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
        assert attr_params.get("attr_val") == getattr(obj, attr_name)
        assert isinstance(getattr(obj, attr_name), attr_type)


def check_bbox(target_values, bbox, clip_zero):
    target_values = target_values.copy()
    if clip_zero:
        for k, v in target_values.items():
            target_values[k] = max(0, v)
    if (
        target_values["xmin"] != bbox.xmin
        or target_values["xmax"] != bbox.xmax
        or target_values["ymin"] != bbox.ymin
        or target_values["ymax"] != bbox.ymax
    ):
        return False
    return True


def has_object(ann: PascalAnnotation, target_object: dict, clip_zero: bool) -> bool:
    for obj in ann:
        match = True
        for k, v in target_object.items():
            attr_val = getattr(obj, k)
            if k == "bndbox":
                if not check_bbox(v, attr_val, clip_zero):
                    match = False
                    break
            elif k == "attributes":
                attr_val = getattr(obj, k)
                attributes = getattr(attr_val, "attribute")
                if isinstance(attributes, list) and len(attributes) == len(v):
                    for a, item in zip(attributes, v):
                        for t in item:
                            check_attributes(a, t)
                else:
                    for attr in v:
                        for item in attr:
                            check_attributes(attributes, item)
            else:
                if attr_val != v:
                    match = False
                    break
        if match:
            return True
    return False


@pytest.mark.parametrize(
    "clip_zero",
    [True, False],
)
def test_valid(valid_annotations, clip_zero):
    """
    Проверить параметры валидных аннотаций
    """
    for ann_sample in valid_annotations:
        ann_file = ann_sample.get("file")
        ann = annotation_from_xml(ann_file, clip_zero=clip_zero)
        for attributes in ann_sample.get("attributes"):
            check_attributes(ann, attributes)
        objects = ann_sample.get("objects")
        if objects is not None:
            for obj in objects:
                assert has_object(ann, obj, clip_zero)


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
