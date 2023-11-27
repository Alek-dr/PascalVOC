import json
from pathlib import Path

from PIL import Image

from pascal import annotation_from_xml
from pascal.utils import save_xml

ds_path = Path("/home/VOCtest_06-Nov-2007/VOCdevkit/VOC2007")

img_src = ds_path / "JPEGImages"
ann_src = ds_path / "Annotations"

out_labelme = ds_path / "converted_labelme"
out_yolo = ds_path / "yolo"
xml_output = ds_path / "ConvertedAnnotations"

with open("label_map.json", "r") as f:
    label_map = json.load(f)


if __name__ == "__main__":
    for file in img_src.glob("*.jpg"):
        # Get annotation file path
        ann_file = (ann_src / file.name).with_suffix(".xml")
        # Make pascal annotation object
        ann = annotation_from_xml(ann_file)
        # Filter objects
        ann.filter_objects(["person"])
        # Save to xml file (same as ann_file)
        xml = ann.to_xml()
        out_xml_name = xml_output / file.with_suffix(".xml").name
        save_xml(out_xml_name, xml)
        # Save yolo annotation
        yolo_ann = ann.to_yolo(label_map)
        out_yolo_name = (out_yolo / file.name).with_suffix(".txt")
        with open(out_yolo_name, "w") as f:
            f.write(yolo_ann)
        # Convert to labelme and save json file
        res = ann.to_labelme(file, save_img_data=False)
        with open((out_labelme / file.name).with_suffix(".json"), "w") as f:
            json.dump(res, f, indent=2)
        # Draw objects
        img = Image.open(file)
        draw_img = ann.draw_boxes(img)
        draw_img.show()
