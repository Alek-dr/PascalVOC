from typing import Union, List, Optional
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


@runtime_checkable
class Size(Protocol):
    width: Union[float, int]
    height: Union[float, int]


@runtime_checkable
class PascalAnnotation(Protocol):
    objects: List[PascalObject] = []
    size: Optional[Size] = None
    filename: Optional[str] = None

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, item):
        return self.objects[item]
