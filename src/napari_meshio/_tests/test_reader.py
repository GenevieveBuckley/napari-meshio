import os

import meshio
import numpy as np
import pytest

from napari_meshio import napari_get_reader


@pytest.mark.parametrize("suffix", [".ply", ".stl", ".vol", ".vtk"])
def test_reader(tmp_path, suffix):  # tmp_path is a pytest fixture
    """Test meshio reader plugin.

    Tests a small subset of meshio available file formats.
    See more details of available file formats here:
    https://github.com/nschloe/meshio
    """
    # Make test mesh data
    points = [[0, 0, 0], [0, 20, 20], [10, 0, 0], [10, 10, 10]]
    cells = [[0, 1, 2], [1, 2, 3]]
    face_data = [("triangle", cells)]
    mesh = meshio.Mesh(points, face_data)

    # Save test mesh data
    my_test_file = os.path.join(tmp_path, "test-mesh" + suffix)
    mesh.write(my_test_file)

    # try to read it back in
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure it's the same as it started
    data, kwargs, layer_type = layer_data_tuple
    assert layer_type == "surface"
    saved_points, saved_cells = data
    np.testing.assert_allclose(points, saved_points)
    np.testing.assert_allclose(cells, saved_cells)


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None


def test_get_reader_from_list():
    path_list = ["test_file_1.ply", "test_file_2.ply"]
    reader = napari_get_reader(path_list)
    assert callable(reader)
    assert reader.__module__ == "napari_meshio._reader"
    assert reader.__name__ == "reader_function"
