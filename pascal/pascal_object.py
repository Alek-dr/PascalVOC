from typing import Union

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class BndBox(Protocol):
    xmin: Union[float, int]
    ymin: Union[float, int]
    xmax: Union[float, int]
    ymax: Union[float, int]


@runtime_checkable
class PascalObject(Protocol):
    name: str
    bndbox: BndBox
