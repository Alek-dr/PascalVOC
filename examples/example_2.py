from pathlib import Path

from PIL import Image

from pascal import annotation_from_yolo

ds_path = Path("/home/VOCtest_06-Nov-2007/VOCdevkit/VOC2007")

label_map = {0: "dog", 1: "car", 2: "person", 3: "train", 4: "chair", 5: "sofa"}

if __name__ == "__main__":
    for file in (ds_path / "yolo").glob("*.txt"):
        ann = annotation_from_yolo(file, label_map=label_map)
        ann.filter_objects(["person"])
        img_file = file.with_suffix(".jpg")
        img = Image.open(img_file)
        draw_img = ann.draw_boxes(img)
        draw_img.show()
