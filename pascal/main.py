import base64
from collections import namedtuple
from io import BytesIO

import xml.etree.ElementTree as xml
from lxml import etree
from pathlib import Path
from PIL import Image
from typing import List, Union

size_block = namedtuple("size", "width,height,depth")


def _add_tab(str):
    """Add tab to each line"""
    lines = str.split("\n")
    lines = "\n\t".join(lines)
    return f"\t{lines}"


class ParseException(Exception):
    pass


class BndBox(namedtuple("BndBox", ["xmin", "ymin", "xmax", "ymax"])):
    __slots__ = ()

    def __str__(self):
        return f"<bndbox>\n\t<xmin>{self.xmin}</xmin>\n" \
               f"\t<ymin>{self.ymin}</ymin>\n\t<xmax>{self.xmax}" \
               f"</xmax>\n\t<ymax>{self.ymax}</ymax>\n</bndbox>"

    def to_xml(self):
        bndbox = xml.Element("bndbox")
        xmin = xml.Element("xmin")
        xmin.text = str(self.xmin)
        ymin = xml.Element("ymin")
        ymin.text = str(self.ymin)
        xmax = xml.Element("xmax")
        xmax.text = str(self.xmax)
        ymax = xml.Element("ymax")
        ymax.text = str(self.ymax)
        bndbox.append(xmin)
        bndbox.append(ymin)
        bndbox.append(xmax)
        bndbox.append(ymax)
        return bndbox


class PascalObject:

    def __init__(self, name: str = str(),
                 pose: str = "Unspecified",
                 truncated: bool = False,
                 difficult: bool = False,
                 bndbox: BndBox = None, **kwargs):
        self._name = name
        self._pose = pose
        self._truncated = truncated
        self._difficult = difficult
        self._bndbox = bndbox
        self._other_fields = kwargs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, pose):
        self._pose = str(pose)

    @property
    def truncated(self):
        return self._truncated

    @truncated.setter
    def truncated(self, truncated: Union[bool, str, int]):
        if isinstance(truncated, bool):
            self._truncated = truncated
        elif isinstance(truncated, str):
            self._truncated = False if truncated == "0" else True
        elif isinstance(truncated, int):
            self._truncated = False if truncated == 0 else True
        else:
            raise ParseException(
                f"Cannot understand truncated field of type: {type(truncated)}. truncated one of type: bool. str, int")

    @property
    def difficult(self):
        return self._difficult

    @difficult.setter
    def difficult(self, difficult: Union[bool, str, int]):
        if isinstance(difficult, bool):
            self._truncated = difficult
        elif isinstance(difficult, str):
            self._truncated = False if difficult == "0" else True
        elif isinstance(difficult, int):
            self._truncated = False if difficult == 0 else True
        else:
            raise ParseException(
                f"Cannot understand difficult field of type: {type(difficult)}. truncated one of type: bool. str, int")

    @property
    def bndbox(self):
        return self._bndbox

    @bndbox.setter
    def bndbox(self, bnd_block: BndBox):
        self._bndbox = bnd_block

    def __str__(self):
        name = f"<name>{self.name}</name>"
        pose = f"<pose>{self.pose}</pose>"
        truncated_value = "1" if self._truncated else "0"
        truncated = f"<truncated>{truncated_value}</truncated>"
        difficult_value = "1" if self._difficult else "0"
        difficult = f"<difficult>{difficult_value}</difficult>"
        other_attributes = []
        for k, v in self._other_fields.items():
            line = f"<{k}>{v}</{k}>"
            other_attributes.append(line)
        attributes = [name, pose, truncated, difficult, *other_attributes, str(self.bndbox)]
        s_attributes = list(map(_add_tab, attributes))
        s = "\n".join(s_attributes)
        h = f"<object>\n{s}\n</object>"
        return h

    def to_xml(self):
        obj = xml.Element("object")
        name = xml.Element("name")
        name.text = str(self.name)
        pose = xml.Element("pose")
        pose.text = str(self.pose)
        truncated = xml.Element("truncated")
        truncated.text = "1" if self.truncated else "0"
        difficult = xml.Element("difficult")
        difficult.text = "1" if self.truncated else "0"
        bnd_box = self.bndbox.to_xml()
        add_features = []
        for k, v in self._other_fields.items():
            f = xml.Element(str(k))
            f.text = str(v)
            add_features.append(f)
        obj.append(name)
        obj.append(pose)
        obj.append(truncated)
        obj.append(difficult)
        for feature in add_features:
            obj.append(feature)
        obj.append(bnd_box)
        return obj

    def add_feature(self, fname: str, fvalue):
        self._other_fields[fname] = fvalue

    def remove_feature(self, fname: str):
        if self._other_fields.get(fname):
            del self._other_fields[fname]


class PascalVOC:

    def __init__(self, filename: Union[Path, str],
                 size: size_block,
                 objects: List[PascalObject] = None,
                 path: Path = None,
                 folder: str = None,
                 segmented: int = 0,
                 database: str = "Unknown"):
        if isinstance(filename, Path):
            self.filename = filename.name
        else:
            self.filename = filename
        self.folder = folder
        self.path = path
        self.database = database
        self.size = size
        self.segmented = segmented
        self.objects = objects if objects is not None else []

    @classmethod
    def _parse(cls, doc):
        try:
            filename = doc.find("filename").text
            path_ = doc.find("path")
            path = Path(path_.text) if path_ is not None else None
            folder_ = doc.find("folder")
            folder = folder_.text if folder_ is not None else None
            source = doc.find("source")
            if source:
                database = source.find("database").text
            else:
                database = str()
            size_tag = doc.find("size")
            width = size_tag.find("width").text
            height = size_tag.find("height").text
            depth = size_tag.find("depth").text
            size = size_block(width, height, depth)
            segmented_ = doc.find("segmented")
            if segmented_:
                segmented = segmented_.text
            else:
                segmented = 0
            objects = doc.findall("object")
            objects_ = []
            for obj in objects:
                obj_ = PascalObject()
                for field in obj:
                    if field.tag != 'bndbox':
                        if hasattr(obj_, field.tag):
                            setattr(obj_, field.tag, field.text)
                box_tag = obj.find("bndbox")
                xmin = int(box_tag.find("xmin").text)
                ymin = int(box_tag.find("ymin").text)
                xmax = int(box_tag.find("xmax").text)
                ymax = int(box_tag.find("ymax").text)
                obj_.bndbox = BndBox(xmin, ymin, xmax, ymax)
                objects_.append(obj_)
        except IndexError as ex:
            raise ParseException(ex)
        return PascalVOC(filename, size, objects_, path, folder, segmented, database)

    @classmethod
    def from_xml(cls, path: Union[Path, str]):
        """
        Read xml annotation file by path
        """
        doc = xml.parse(str(path))
        return PascalVOC._parse(doc)

    @classmethod
    def from_bytes(cls, bdata):
        doc = etree.XML(bdata)
        return PascalVOC._parse(doc)

    def __str__(self):
        head = f"\n\t<folder>{self.folder}</folder>" \
               f"\n\t<filename>{self.filename}</filename>" \
               f"\n\t<path>{str(self.path)}</path>" \
               f"\n\t<source>" \
               f"\n\t\t<database>{self.database}</database>" \
               f"\n\t</source>\n" \
               f"\t<size>" \
               f"\n\t\t<width>{self.size.width}</width>" \
               f"\n\t\t<height>{self.size.height}</height>" \
               f"\n\t\t<depth>{self.size.depth}" \
               f"</depth>" \
               f"\n\t</size>" \
               f"\n\t<segmented>{self.segmented}</segmented>\n"
        objects = "\n".join([str(obj) for obj in self.objects])
        objects = _add_tab(objects)
        s = f"<annotation>{head}{objects}\n</annotation>"
        return s

    def to_xml(self, drop_path: bool = False,
               drop_folder: bool = False,
               drop_source: bool = False,
               drop_pose: bool = False,
               drop_segmented: bool = False,
               drop_truncated: bool = False) -> xml.Element:
        root = xml.Element("annotation")
        if not drop_folder:
            folder = xml.Element("folder")
            folder.text = str(self.folder)
            root.append(folder)
        filename = xml.Element("filename")
        filename.text = self.filename
        root.append(filename)
        if not drop_path:
            path = xml.Element("path")
            path.text = str(self.path)
            root.append(path)
        if not drop_source:
            source = xml.Element("source")
            database = xml.Element("database")
            database.text = self.database
            source.append(database)
            root.append(source)
        size = xml.Element("size")
        width = xml.Element("width")
        width.text = str(self.size.width)
        height = xml.Element("height")
        height.text = str(self.size.height)
        depth = xml.Element("depth")
        depth.text = str(self.size.depth)
        size.append(width)
        size.append(height)
        size.append(depth)
        root.append(size)
        if not drop_segmented:
            segmented = xml.Element("segmented")
            segmented.text = str(self.segmented)
            root.append(segmented)
        for obj in self.objects:
            obj_xml = obj.to_xml()
            if drop_pose:
                pose = obj_xml.find("pose")
                obj_xml.remove(pose)
            if drop_truncated:
                truncated = obj_xml.find("truncated")
                obj_xml.remove(truncated)
            root.append(obj_xml)
        return root

    @staticmethod
    def base64img(img, img_path) -> str:
        buffered = BytesIO()
        suffix = img_path.suffix
        if suffix in ['.JPG', ".jpg", '.JPEG', '.jpeg']:
            format = "JPEG"
        elif suffix in ['.PNG', ".png"]:
            format = "PNG"
        else:
            format = "PNG"
        img.save(buffered, format=format)
        buffered.seek(0)
        img_byte = buffered.getvalue()
        encoded_string = base64.b64encode(img_byte).decode("utf-8")
        return encoded_string

    def to_labelme(self, path_to_img: Path = None, save_img_data=False) -> dict:
        encoded_string = None
        if (path_to_img is None) and (self.path is None):
            raise Exception("No path to image. path_to_img or self.path must exists")
        if (path_to_img is None) and (self.path is not None):
            path_to_img = Path(self.path)
        img_path = path_to_img / self.filename
        if not img_path.exists():
            raise FileNotFoundError(f"There no file: {img_path}")

        if save_img_data:
            img = Image.open(img_path)
            encoded_string = PascalVOC.base64img(img, img_path)

        shapes = []
        for obj in self.objects:
            label = obj.name
            points = [[obj.bndbox.xmin, obj.bndbox.ymin],
                      [obj.bndbox.xmax, obj.bndbox.ymin],
                      [obj.bndbox.xmax, obj.bndbox.ymax],
                      [obj.bndbox.xmin, obj.bndbox.ymax]]
            shape = dict(
                label=label,
                points=points,
                group_id=None,
                shape_type="polygon",
                flags={}
            )
            shapes.append(shape)

        res = dict(
            version="4.5.6",
            flags={},
            shapes=shapes,
            imagePath=str(img_path),
            imageData=encoded_string,
            imageHeight=self.size.height,
            imageWidth=self.size.width
        )
        return res

    def save(self, output: Union[Path, str],
             drop_all=False,
             drop_path: bool = False,
             drop_folder: bool = False,
             drop_source: bool = False,
             drop_pose: bool = False,
             drop_segmented: bool = False,
             drop_truncated: bool = False) -> None:
        """Save pascal annotation to xml file"""
        if drop_all:
            drop_path = True,
            drop_folder = True,
            drop_source = True,
            drop_pose = True,
            drop_segmented = True,
            drop_truncated = True
        doc = self.to_xml(drop_path, drop_folder, drop_source, drop_pose, drop_segmented, drop_truncated)
        tree = xml.ElementTree(doc)
        with open(output, "w") as out:
            tree.write(out, encoding='unicode', method='xml')

    def add_object(self, obj: PascalObject) -> None:
        self.objects.append(obj)

    def add_feature(self, fname: str, fvalue):
        """Add feature <fname> with <fvalue> to each object"""
        for obj in self.objects:
            obj.add_feature(fname, fvalue)

    def remove_feature(self, fname: str):
        for obj in self.objects:
            obj.remove_feature(fname)
