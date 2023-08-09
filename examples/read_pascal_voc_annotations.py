from pathlib import Path

from pascal.pascal_annotation import annotation_from_xml

ds_path = Path("/media/alexander/D/datasets/Public/VOCtest_06-Nov-2007/VOCdevkit/VOC2007")
img_src = ds_path / "JPEGImages"
ann_src = ds_path / "Annotations"

attr_type_spec = {
    "truncated": bool,
    "difficult": bool
}

if __name__ == '__main__':
    for file in ann_src.glob("*.xml"):
        ann = annotation_from_xml(file, attr_type_spec)