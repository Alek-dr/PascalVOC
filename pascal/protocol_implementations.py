from dataclasses import dataclass
from typing import Union

from xmlobj.xmlmapping import XMLMixin

from pascal.protocols import BndBox as BndBoxProtocol
from pascal.protocols import PascalObject as PascalObjectProtocol
from pascal.protocols import Size as SizeProtocol


@dataclass
class BndBox(BndBoxProtocol, XMLMixin):
    xmin: Union[float, int]
    ymin: Union[float, int]
    xmax: Union[float, int]
    ymax: Union[float, int]


@dataclass
class Object(PascalObjectProtocol, XMLMixin):
    name: str
    bndbox: BndBox


@dataclass
class Size(SizeProtocol, XMLMixin):
    width: Union[float, int]
    height: Union[float, int]
