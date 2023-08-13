import pytest

annotations = [
    {
        "file": "test_data/000001.xml",
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
        "file": "test_data/000103.xml",
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
    "test_data/books.xml",
    "test_data/cd_catalog.xml",
    "test_data/000103_no_size.xml",
]


@pytest.fixture
def valid_annotations():
    return annotations


@pytest.fixture
def invalid_ann_files():
    return invalid_annotations
