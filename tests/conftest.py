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
                        "attr_val": "Jinky the Fruit Bat",
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
        "objects": [
            {
                "name": "dog",
                "pose": "Left",
                "truncated": 1,
                "difficult": 0,
                "bndbox": {
                    "xmin": 48,
                    "ymin": 240,
                    "xmax": 195,
                    "ymax": 371,
                },
            },
            {
                "name": "person",
                "pose": "Left",
                "truncated": 1,
                "difficult": 0,
                "bndbox": {
                    "xmin": 8,
                    "ymin": 12,
                    "xmax": 352,
                    "ymax": 498,
                },
            },
        ],
        "obj_info": {"names": ["dog", "person"], "count": {"dog": 1, "person": 1}},
    },
    {
        "file": "test_data/valid_annotations/000103.xml",
        "n_objects": 9,
        "attributes": [
            {"attr_name": "folder", "attr_val": "VOC2007", "dtype": str},
            {"attr_name": "filename", "attr_val": "000103.jpg", "dtype": str},
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
        "objects": [
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 1,
                "difficult": 0,
                "bndbox": {
                    "xmin": 1,
                    "ymin": 241,
                    "xmax": 47,
                    "ymax": 276,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": 26,
                    "ymin": 234,
                    "xmax": 85,
                    "ymax": 265,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": 98,
                    "ymin": 222,
                    "xmax": 143,
                    "ymax": 252,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 1,
                "bndbox": {
                    "xmin": 183,
                    "ymin": 217,
                    "xmax": 203,
                    "ymax": 230,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 1,
                "bndbox": {
                    "xmin": 201,
                    "ymin": 211,
                    "xmax": 213,
                    "ymax": 223,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 1,
                "bndbox": {
                    "xmin": 160,
                    "ymin": 218,
                    "xmax": 179,
                    "ymax": 229,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 1,
                "bndbox": {
                    "xmin": 55,
                    "ymin": 223,
                    "xmax": 93,
                    "ymax": 238,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 1,
                "bndbox": {
                    "xmin": 29,
                    "ymin": 227,
                    "xmax": 61,
                    "ymax": 236,
                },
            },
            {
                "name": "car",
                "pose": "Unspecified",
                "truncated": 1,
                "difficult": 1,
                "bndbox": {
                    "xmin": 1,
                    "ymin": 230,
                    "xmax": 30,
                    "ymax": 242,
                },
            },
        ],
        "obj_info": {
            "names": ["car"],
            "count": {
                "car": 9,
            },
        },
    },
    {
        "file": "test_data/valid_annotations/000010.xml",
        "n_objects": 2,
        "attributes": [
            {"attr_name": "folder", "attr_val": "VOC2007", "dtype": str},
            {"attr_name": "filename", "attr_val": "000010.jpg", "dtype": str},
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
                    {"attr_name": "flickrid", "attr_val": 227250080, "dtype": int},
                ],
            },
            {
                "attr_name": "owner",
                "attr_val": [
                    {"attr_name": "flickrid", "attr_val": "genewolf", "dtype": str},
                    {
                        "attr_name": "name",
                        "attr_val": "whiskey kitten",
                        "dtype": str,
                    },
                ],
            },
            {
                "attr_name": "size",
                "attr_val": [
                    {"attr_name": "width", "attr_val": 354, "dtype": int},
                    {"attr_name": "height", "attr_val": 480, "dtype": int},
                    {"attr_name": "depth", "attr_val": 3, "dtype": int},
                ],
            },
            {"attr_name": "segmented", "attr_val": 0, "dtype": int},
        ],
        "objects": [
            {
                "name": "horse",
                "pose": "Rear",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": 87,
                    "ymin": 97,
                    "xmax": 258,
                    "ymax": 427,
                },
            },
            {
                "name": "person",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": 133,
                    "ymin": 72,
                    "xmax": 245,
                    "ymax": 284,
                },
            },
        ],
        "obj_info": {
            "names": ["horse", "person"],
            "count": {
                "horse": 1,
                "person": 1,
            },
        },
    },
    {
        "file": "test_data/valid_annotations/bool_attributes.xml",
        "n_objects": 6,
        "attributes": [
            {"attr_name": "folder", "attr_val": "test_attr", "dtype": str},
            {"attr_name": "filename", "attr_val": "frame.jpg", "dtype": str},
            {
                "attr_name": "source",
                "attr_val": [
                    {
                        "attr_name": "database",
                        "attr_val": "Unknown",
                        "dtype": str,
                    },
                    {
                        "attr_name": "annotation",
                        "attr_val": "Unknown",
                        "dtype": str,
                    },
                    {"attr_name": "image", "attr_val": "Unknown", "dtype": str},
                ],
            },
            {
                "attr_name": "size",
                "attr_val": [
                    {"attr_name": "width", "attr_val": 1920, "dtype": int},
                    {"attr_name": "height", "attr_val": 1080, "dtype": int},
                    # {"attr_name": "depth", "attr_val": None, "dtype": int},
                ],
            },
            {"attr_name": "segmented", "attr_val": 0, "dtype": int},
        ],
        "objects": [
            {
                "name": "handheld_scanner",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 743.53,
                    "ymin": 99.46,
                    "xmax": 797.5,
                    "ymax": 207.56,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ]
                ],
            },
            {
                "name": "products",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 740.99,
                    "ymin": 385.75,
                    "xmax": 821.4,
                    "ymax": 456.3,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "products", "dtype": str},
                        {"attr_name": "value", "attr_val": True, "dtype": bool},
                    ],
                    [
                        {
                            "attr_name": "name",
                            "attr_val": "empty_transparent_packet",
                            "dtype": str,
                        },
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {
                            "attr_name": "name",
                            "attr_val": "filled_transparent_packet",
                            "dtype": str,
                        },
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ],
                ],
            },
            {
                "name": "client_things",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 826.8,
                    "ymin": 383.97,
                    "xmax": 892.9,
                    "ymax": 495.1,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "bags", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "wallets", "dtype": str},
                        {"attr_name": "value", "attr_val": True, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "plastic_card", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "phones", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "clients_food", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "other_things", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "shop_receipt", "dtype": str},
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ],
                ],
            },
            {
                "name": "hands",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 799.88,
                    "ymin": 392.4,
                    "xmax": 875.13,
                    "ymax": 547.38,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ]
                ],
            },
            {
                "name": "products",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 701.29,
                    "ymin": 373.46,
                    "xmax": 755.1,
                    "ymax": 426.7,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "products", "dtype": str},
                        {"attr_name": "value", "attr_val": True, "dtype": bool},
                    ],
                    [
                        {
                            "attr_name": "name",
                            "attr_val": "empty_transparent_packet",
                            "dtype": str,
                        },
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {
                            "attr_name": "name",
                            "attr_val": "filled_transparent_packet",
                            "dtype": str,
                        },
                        {"attr_name": "value", "attr_val": False, "dtype": bool},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ],
                ],
            },
            {
                "name": "person",
                "truncated": 0,
                "difficult": 0,
                "occluded": 0,
                "bndbox": {
                    "xmin": 629.63,
                    "ymin": 396.7,
                    "xmax": 1200.0,
                    "ymax": 923.66,
                },
                "attributes": [
                    [
                        {"attr_name": "name", "attr_val": "rotation", "dtype": str},
                        {"attr_name": "value", "attr_val": 0.0, "dtype": float},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "track_id", "dtype": str},
                        {"attr_name": "value", "attr_val": 0, "dtype": int},
                    ],
                    [
                        {"attr_name": "name", "attr_val": "keyframe", "dtype": str},
                        {"attr_name": "value", "attr_val": True, "dtype": bool},
                    ],
                ],
            },
        ],
        "obj_info": {
            "names": [
                "handheld_scanner",
                "products",
                "client_things",
                "hands",
                "person",
            ],
            "count": {
                "handheld_scanner": 1,
                "products": 2,
                "client_things": 1,
                "hands": 1,
                "person": 1,
            },
        },
    },
    {
        "file": "test_data/valid_annotations/neg_bbox_val.xml",
        "n_objects": 2,
        "attributes": [
            {"attr_name": "folder", "attr_val": "folder", "dtype": str},
            {"attr_name": "filename", "attr_val": "test.jpg", "dtype": str},
            {
                "attr_name": "source",
                "attr_val": [
                    {
                        "attr_name": "database",
                        "attr_val": "Unspecified",
                        "dtype": str,
                    },
                ],
            },
            {
                "attr_name": "size",
                "attr_val": [
                    {"attr_name": "width", "attr_val": 355, "dtype": int},
                    {"attr_name": "height", "attr_val": 539, "dtype": int},
                    {"attr_name": "depth", "attr_val": 3, "dtype": int},
                ],
            },
        ],
        "objects": [
            {
                "name": "cat1",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": -2,
                    "ymin": -3,
                    "xmax": 355,
                    "ymax": 333,
                },
            },
            {
                "name": "cat2",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0,
                "bndbox": {
                    "xmin": 230,
                    "ymin": 441,
                    "xmax": 336,
                    "ymax": 525,
                },
            },
        ],
        "obj_info": {
            "names": ["cat1", "cat2"],
            "count": {
                "cat1": 1,
                "cat2": 1,
            },
        },
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
