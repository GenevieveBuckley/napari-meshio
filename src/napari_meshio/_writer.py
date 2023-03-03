"""
This module is an example of a barebones writer plugin for napari.

It implements the Writer specification.
see: https://napari.org/stable/plugins/guides.html?#writers

Replace code below according to your needs.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Sequence, Tuple, Union

import meshio

from napari_meshio import DEFAULT_MESH_FORMAT, MESHIO_FILE_FORMATS

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = Tuple[DataType, dict, str]


def write_single_surface(path: str, data: Any, meta: dict) -> List[str]:
    """Writes a single surface to mesh file.

    If no file extension is given, default saves meshes to .ply files.

    Parameters
    ----------
    path : str
    data : The surface layer data.
           A tuple containing three numpy arrays (points, cells, values)

    Returns
    -------
    [path] : A list containing the string path to the saved file.
    """
    path = Path(path)
    # Create meshio Mesh from napari Surface layer
    points, cells, values = data
    if cells.shape[-1] == 3:
        face_data = [("triangle", cells)]
    elif cells.shape[-1] == 4:
        face_data = [("quad", cells)]
    else:
        raise ValueError(
            "napari-meshio only supports triangle or quad face cells in meshes."  # noqa: E501
        )
    mesh = meshio.Mesh(points, face_data)
    # Write mesh data to file
    suffix = path.suffix
    if suffix not in MESHIO_FILE_FORMATS:
        if suffix == "":
            path = path.with_suffix(DEFAULT_MESH_FORMAT)
        else:
            raise RuntimeError(
                f"napari-meshio does not suuport file format '{suffix}'."
                f"Supported file extensions include: {MESHIO_FILE_FORMATS}"
            )
    mesh.write(path)
    # return path to any file(s) that were successfully written
    return [path]


def write_multiple(path: str, data: List[FullLayerData]) -> List[str]:
    """Writes multiple surface layers to individual mesh files.

    Parameters
    ----------
    path : str
    data : A layer tuple.
           A tuple containing three elements: (data, kwargs, layer_type)
           For surface layers, `data` is another nested tuple,
           and this is what is passed to the `write_single_surface` function.

    Returns
    -------
    [path] : A list containing multiple string paths to the saved mesh files.
    """
    path = Path(path)
    output_paths = []
    for layer in data:
        layer_name = layer[1]["name"]
        output_path = path.with_name(
            path.stem + "-" + layer_name + path.suffix
        )
        write_single_surface(output_path, layer[0], meta={})
        output_paths.append(str(output_path))
    # return path to any file(s) that were successfully written
    return output_paths
