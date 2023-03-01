"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
import pathlib

import meshio
import numpy as np

MESHIO_FILE_FORMATS = [
    ".inp",  # Abaqus http://abaqus.software.polimi.it/v6.14/index.html
    ".msh",  # ANSYS msh
    ".avs",  # AVS-UCD https://lanl.github.io/LaGriT/pages/docs/read_avs.html
    ".cgns",  # CGNS https://cgns.github.io/
    ".xml",  # DOLFIN XML https://manpages.ubuntu.com/manpages/jammy/en/man1/dolfin-convert.1.html  # noqa: E501
    ".e",  # Exodus https://nschloe.github.io/meshio/exodus.pdf
    ".exo",  # Exodus https://nschloe.github.io/meshio/exodus.pdf
    ".f3grid",  # FLAC3D https://www.itascacg.com/software/flac3d
    ".h5m",  # H5M https://www.mcs.anl.gov/~fathom/moab-docs/h5mmain.html
    ".mdpa",  # Kratos/MDPA https://github.com/KratosMultiphysics/Kratos/wiki/Input-data  # noqa: E501
    ".mesh",  # Medit https://people.sc.fsu.edu/~jburkardt/data/medit/medit.html  # noqa: E501
    ".meshb",  # Medit https://people.sc.fsu.edu/~jburkardt/data/medit/medit.html  # noqa: E501
    ".med",  # MED/Salome https://docs.salome-platform.org/latest/dev/MEDCoupling/developer/med-file.html  # noqa: E501
    ".bdf",  # Nastran https://help.autodesk.com/view/NSTRN/2019/ENU/?guid=GUID-42B54ACB-FBE3-47CA-B8FE-475E7AD91A00  # noqa: E501
    ".fem",  # Nastran https://help.autodesk.com/view/NSTRN/2019/ENU/?guid=GUID-42B54ACB-FBE3-47CA-B8FE-475E7AD91A00  # noqa: E501
    ".nas",  # Nastran https://help.autodesk.com/view/NSTRN/2019/ENU/?guid=GUID-42B54ACB-FBE3-47CA-B8FE-475E7AD91A00  # noqa: E501
    ".vol",  # Netgen https://github.com/ngsolve/netgen
    ".vol.gz",  # Netgen https://github.com/ngsolve/netgen
    # ?? "", # Neuroglancer precomputed format https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed#mesh-representation-of-segmented-object-surfaces  # noqa: E501
    ".msh",  # Gmsh (format versions 2.2, 4.0, and 4.1) https://gmsh.info/doc/texinfo/gmsh.html#File-formats  # noqa: E501
    ".obj",  # CBJ https://en.wikipedia.org/wiki/Wavefront_.obj_file
    ".off",  # OFF https://segeval.cs.princeton.edu/public/off_format.html
    ".post",  # PERMAS https://www.intes.de
    ".post.gz",  # PERMAS https://www.intes.de
    ".dato",  # PERMAS https://www.intes.de
    ".dato.gz",  # PERMAS https://www.intes.de
    ".ply",  # PLY (Polygon file format) https://en.wikipedia.org/wiki/PLY_(file_format)  # noqa: E501
    ".stl",  # STL https://en.wikipedia.org/wiki/STL_(file_format)
    ".dat",  # Tecplot http://paulbourke.net/dataformats/tp/
    ".node",  # TetGen https://wias-berlin.de/software/tetgen/fformats.html
    ".ele",  # TetGen https://wias-berlin.de/software/tetgen/fformats.html
    # ".svg", # SVG (2D output only) https://www.w3.org/TR/SVG/
    ".su2",  # SU2 https://su2code.github.io/docs_v7/Mesh-File/
    ".ugrid",  # UGRID https://www.simcenter.msstate.edu/software/documentation/ug_io/3d_grid_file_type_ugrid.html  # noqa: E501
    ".vtk",  # VTK https://vtk.org/wp-content/uploads/2015/04/file-formats.pdf
    ".vtu",  # VTU https://vtk.org/Wiki/VTK_XML_Formats
    ".wkt",  # WKT (TIN) https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry  # noqa: E501
    ".xdmf",  # XDMF https://xdmf.org/index.php/XDMF_Model_and_Format
    ".xmf",  # XDMF https://xdmf.org/index.php/XDMF_Model_and_Format
]


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
    import pdb

    pdb.set_trace()
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    if isinstance(path, str):
        path = pathlib.Path(path)
    suffix = path.suffix

    if suffix in MESHIO_FILE_FORMATS:
        return reader_function
    elif suffix in [".xyz"]:
        return points_reader_function
    elif suffix in [".npy"]:
        return single_numpy_reader_function
    else:
        # if we know we cannot read the file, return None.
        return None


def points_reader_function(path):
    if isinstance(path, list):
        path = path[0]
    data = np.genfromtxt(path)
    data = np.fliplr(data)  # switch from xyz to zyx axes order napari expects

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "points"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]


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
    # handle both a string and a list of strings
    # paths = [path] if isinstance(path, str) else path
    mesh = meshio.read(path)
    data = (mesh.points, mesh.cells[0].data)

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "surface"
    return (data, [add_kwargs, [layer_type]])


def numpy_reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.
    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.
    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.
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
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path
    # load all files into array
    arrays = [np.load(_path) for _path in paths]
    # stack arrays into single array
    data = np.squeeze(np.stack(arrays))

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "image"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]


def single_numpy_reader_function(path):
    print("single_numpy_reader_function")
    data = np.load(path)
    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "labels"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]
