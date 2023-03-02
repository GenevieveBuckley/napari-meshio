from napari_meshio import make_sample_data


def test_sample_data():
    """Test Stanford Bunny example data."""
    bunny = make_sample_data()
    data, kwargs, layer_type = bunny[0]
    assert layer_type == "surface"
    assert kwargs.get("name") == "bunny"
    points, cells = data
    assert points.shape == (35947, 3)  # vertices
    assert cells.shape == (69451, 3)  # faces
