from pathlib import Path

from PIL import Image

from pascal import annotation_from_xml

ds_path = Path(
    "/media/alexander/D/datasets/Public/VOCtest_06-Nov-2007/VOCdevkit/VOC2007"
)
img_src = ds_path / "JPEGImages"
ann_src = ds_path / "Annotations"

attr_type_spec = {"truncated": bool, "difficult": bool}

if __name__ == "__main__":
    for file in ann_src.glob("*.xml"):
        img_file = (img_src / file.name).with_suffix(".jpg")
        ann = annotation_from_xml(file, attr_type_spec)
        ann.to_yolo({"car": 1, "dog": 0, "person": 2, "train": 3})
        ann.to_labelme(img_file, save_img_data=True)
        img = Image.open(img_file)
        draw_img = ann.draw_boxes(img)
        draw_img.show()
