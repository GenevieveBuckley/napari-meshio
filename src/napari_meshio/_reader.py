"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
import pathlib

import meshio

from napari_meshio import MESHIO_FILE_FORMATS


def napari_get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or os.PathLike
        Path to file.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    if isinstance(path, str):
        path = pathlib.Path(path)
    suffix = path.suffix

    if suffix not in MESHIO_FILE_FORMATS:
        # if we know we cannot read the file, immediately return None.
        return None

    return reader_function


def reader_function(path):
    """Take a path and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or os.PathLike
        Path to file.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    mesh = meshio.read(path)
    data = (mesh.points, mesh.cells[0].data)

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "surface"
    return [(data, add_kwargs, layer_type)]
