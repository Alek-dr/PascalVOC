from pathlib import Path

import pytest

annotations = [
    {
        "file": "test_data/valid_annotations/000001.xml",
        "n_objects": 2,
        "attributes": [
            {"attr_name": "folder", "attr_val": "VOC2007", "dtype": str},
            {"attr_name": "filename", "attr_val": "000001.jpg", "dtype": str},
            {
                "attr_name": "source",
                "attr_val": [
                    {
                        "attr_name": "database",
                        "attr_val": "The VOC2007 Database",
                        "dtype": str,
                    },
                    {
                        "attr_name": "annotation",
                        "attr_val": "PASCAL VOC2007",
                        "dtype": str,
                    },
                    {"attr_name": "image", "attr_val": "flickr", "dtype": str},
                    {"attr_name": "flickrid", "attr_val": 341012865, "dtype": int},
                ],
            },
            {
                "attr_name": "owner",
                "attr_val": [
                    {"attr_name": "flickrid", "attr_val": "Fried Camels", "dtype": str},
                    {
                        "attr_name": "name",
                        "attr_val": "Jinky the Fruit Ba",
                        "dtype": str,
                    },
                ],
            },
            {
                "attr_name": "size",
                "attr_val": [
                    {"attr_name": "width", "attr_val": 353, "dtype": int},
                    {"attr_name": "height", "attr_val": 500, "dtype": int},
                    {"attr_name": "depth", "attr_val": 3, "dtype": int},
                ],
            },
            {"attr_name": "segmented", "attr_val": 0, "dtype": int},
        ],
    },
    {
        "file": "test_data/valid_annotations/000103.xml",
        "n_objects": 9,
        "attributes": [
            {"attr_name": "folder", "attr_val": "VOC2007", "dtype": str},
            {"attr_name": "filename", "attr_val": "000001.jpg", "dtype": str},
            {
                "attr_name": "source",
                "attr_val": [
                    {
                        "attr_name": "database",
                        "attr_val": "The VOC2007 Database",
                        "dtype": str,
                    },
                    {
                        "attr_name": "annotation",
                        "attr_val": "PASCAL VOC2007",
                        "dtype": str,
                    },
                    {"attr_name": "image", "attr_val": "flickr", "dtype": str},
                    {"attr_name": "flickrid", "attr_val": 341439304, "dtype": int},
                ],
            },
            {
                "attr_name": "owner",
                "attr_val": [
                    {"attr_name": "flickrid", "attr_val": "mgmakati", "dtype": str},
                    {"attr_name": "name", "attr_val": "?", "dtype": str},
                ],
            },
            {
                "attr_name": "size",
                "attr_val": [
                    {"attr_name": "width", "attr_val": 500, "dtype": int},
                    {"attr_name": "height", "attr_val": 375, "dtype": int},
                    {"attr_name": "depth", "attr_val": 3, "dtype": int},
                ],
            },
            {"attr_name": "segmented", "attr_val": 0, "dtype": int},
        ],
    },
]

invalid_annotations = [
    "test_data/invalid_annotations/books.xml",
    "test_data/invalid_annotations/cd_catalog.xml",
    "test_data/invalid_annotations/000103_no_size.xml",
]

valid_objects_list = [
    {
        "file": "test_data/valid_objects/000001.xml",
    }
]
invalid_objects_list = [
    {
        "file": "test_data/invalid_objects/000001.xml",
    }
]


@pytest.fixture
def valid_annotations():
    return annotations


@pytest.fixture
def invalid_ann_files():
    return invalid_annotations


@pytest.fixture
def valid_objects():
    return valid_objects_list


@pytest.fixture
def invalid_objects():
    return invalid_objects_list


@pytest.fixture
def yolo_data():
    data = Path("test_data/yolo_data")
    files = []
    with open(data / "classes.txt", "r") as f:
        labels = f.readlines()
    label_map = {name.strip(): i for i, name in enumerate(labels)}
    for file in data.glob("*.xml"):
        yolo_file = file.with_suffix(".txt")
        files.append(
            {
                "xml_ann_file": str(file),
                "yolo_ann_file": str(yolo_file),
                "label_map": label_map,
            }
        )
    return files
