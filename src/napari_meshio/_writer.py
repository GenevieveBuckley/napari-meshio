"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

import meshio

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def write_single_image(path: str, data: Any, meta: dict) -> List[str]:
    """Writes a single image layer"""

    # Create meshio Mesh from napari Surface layer
    points, cells, values = data.data
    if cells.shape[-1] == 3:
        face_data = [("triangle", cells)]
    elif cells.shape[-1] == 4:
        face_data = [("quad", cells)]
    else:
        raise ValueError("")
    mesh = meshio.Mesh(points, face_data)
    # Write mesh data to file
    mesh.write(path)
    # return path to any file(s) that were successfully written
    return [path]


def write_multiple(path: str, data: List[FullLayerData]) -> List[str]:
    """Writes multiple layers of different types."""

    # implement your writer logic here ...

    # return path to any file(s) that were successfully written
    return [path]
