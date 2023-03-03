import os
from pathlib import Path

import meshio
import numpy as np
import pytest
from napari.layers import Surface

from napari_meshio import (
    DEFAULT_MESH_FORMAT,
    write_multiple,
    write_single_surface,
)


@pytest.mark.parametrize("suffix", ["", ".ply", ".stl", ".vol", ".vtk"])
def test_writer(tmp_path, suffix):  # tmp_path is a pytest fixture
    """Test meshio writer function for a single file."""
    # Create some test surface data
    original_points = np.array(
        [[0, 0, 0], [100, 0, 0], [0, 100, 0], [0, 0, 100]]
    )
    original_cells = np.array([[0, 1, 2], [1, 2, 3], [1, 2, 3], [0, 2, 3]])
    surface_layer = Surface((original_points, original_cells))
    filename = os.path.join(tmp_path, "test-output" + suffix)
    write_single_surface(path=filename, data=surface_layer.data, meta={})
    if suffix == "":
        expected_filename = filename + DEFAULT_MESH_FORMAT
    else:
        expected_filename = filename
    assert os.path.exists(expected_filename)
    # Test you can read the file back in and the data looks good
    mesh = meshio.read(expected_filename)
    np.testing.assert_allclose(original_points, mesh.points)
    np.testing.assert_allclose(original_cells, mesh.cells[0].data)


@pytest.mark.parametrize("suffix", ["", ".ply", ".stl", ".vol", ".vtk"])
def test_write_multiple(tmp_path, suffix):  # tmp_path is a pytest fixture
    """Test meshio multiple writer function."""
    # Create some test data
    original_points = np.array(
        [[0, 0, 0], [100, 0, 0], [0, 100, 0], [0, 0, 100]]
    )
    original_cells = np.array([[0, 1, 2], [1, 2, 3], [1, 2, 3], [0, 2, 3]])
    surface_layer_1 = Surface(
        (original_points, original_cells), name="Surface1"
    )
    surface_layer_2 = Surface(
        (np.fliplr(original_points), original_cells), name="Surface2"
    )
    list_of_layer_tuples = [
        (surface_layer_1.data, {"name": "Surface_1"}, "surface"),
        (surface_layer_2.data, {"name": "Surface_2"}, "surface"),
    ]
    # Test writing multiple surfaces to mesh files
    basefilename = os.path.join(tmp_path, "test-multiple" + suffix)
    write_multiple(basefilename, list_of_layer_tuples)
    # Expected filename
    if suffix == "":
        expected_suffix = DEFAULT_MESH_FORMAT
    else:
        expected_suffix = suffix
    path = Path(basefilename)
    expected_filename_1 = path.with_name(
        path.stem + "-Surface_1" + expected_suffix
    )
    expected_filename_2 = path.with_name(
        path.stem + "-Surface_2" + expected_suffix
    )
    assert os.path.exists(expected_filename_1)
    assert os.path.exists(expected_filename_2)
    # Test you can read the file back in and the data looks good
    mesh_1 = meshio.read(expected_filename_1)
    np.testing.assert_allclose(original_points, mesh_1.points)
    np.testing.assert_allclose(original_cells, mesh_1.cells[0].data)
    mesh_2 = meshio.read(expected_filename_2)
    np.testing.assert_allclose(np.fliplr(original_points), mesh_2.points)
    np.testing.assert_allclose(original_cells, mesh_2.cells[0].data)


def test_unsupported_file_format():
    """Test invaild file format raises RuntimeError."""
    # Create some test surface data
    original_points = np.array(
        [[0, 0, 0], [100, 0, 0], [0, 100, 0], [0, 0, 100]]
    )
    original_cells = np.array([[0, 1, 2], [1, 2, 3], [1, 2, 3], [0, 2, 3]])
    surface_layer = Surface((original_points, original_cells))
    # Attempt to write to an unsuppported file format
    filename = "fakefile.unsupported_extension"
    with pytest.raises(RuntimeError):
        write_single_surface(path=filename, data=surface_layer.data, meta={})
