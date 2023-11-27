from pascal import annotation_from_xml


def test_yolo_convertation(yolo_data):
    """
    Проверить правильность конвертации
        Правильная yolo разметка получена через labelimg
    """
    for pairs in yolo_data:
        ann_file = pairs.get("xml_ann_file")
        ann = annotation_from_xml(ann_file)
        yolo_file = pairs.get("yolo_ann_file")
        with open(yolo_file, "r") as f:
            yolo_true_ann = f.readlines()
        yolo_true_ann = "".join(yolo_true_ann).strip()
        label_map = pairs.get("label_map")
        yolo_convert = ann.to_yolo(label_map, precision=6)
        assert yolo_convert == yolo_true_ann
