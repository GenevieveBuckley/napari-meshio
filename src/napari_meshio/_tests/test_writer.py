import os

import meshio
import numpy as np
import pytest
from napari.layers import Surface

from napari_meshio import write_single_image


@pytest.mark.parametrize("suffix", [".ply", ".stl", ".vol", ".vtk"])
def test_writer(tmp_path, suffix):  # tmp_path is a pytest fixture
    """Test meshio writer function."""
    # Create some test data
    original_points = np.array(
        [[0, 0, 0], [100, 0, 0], [0, 100, 0], [0, 0, 100]]
    )
    original_cells = np.array([[0, 1, 2], [1, 2, 3], [1, 2, 3], [0, 2, 3]])
    original_data = (original_points, original_cells)
    surface_layer = Surface(original_data)
    # Test writing a single mesh file
    filename = os.path.join(tmp_path, "test-output" + suffix)
    write_single_image(path=filename, data=surface_layer, meta={})
    assert os.path.exists(filename)
    # Test you can read the file back in and the data looks good
    mesh = meshio.read(filename)
    np.testing.assert_allclose(original_points, mesh.points)
    np.testing.assert_allclose(original_cells, mesh.cells[0].data)
