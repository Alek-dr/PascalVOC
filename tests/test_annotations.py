import pytest

from pascal import annotation_from_xml
from pascal.exceptions import InconsistentAnnotation


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


def test_valid(valid_annotations):
    """
    Проверить параметры валидных аннотаций
    """
    for ann_sample in valid_annotations:
        ann_file = ann_sample.get("file")
        ann = annotation_from_xml(ann_file)
        for attributes in ann_sample.get("attributes"):
            check_attributes(ann, attributes)


def test_invalid_annotations(invalid_ann_files):
    """
    Ошибка парсинга невалидных аннотаций
    """
    for file in invalid_ann_files:
        with pytest.raises(InconsistentAnnotation):
            annotation_from_xml(file)
