"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

import os
import tarfile

import meshio
import pooch


def bunny():
    """The Stanford Bunny surface mesh.

    Details
    -------
    Website: http://graphics.stanford.edu/data/3Dscanrep/

    Direct download link (4.9 MB compressed, 22 MB uncompressed):
    http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz

    Stanford Bunny
    Source: Stanford University Computer Graphics Laboratory
    Scanner: Cyberware 3030 MS
    Number of scans: 10
    Total size of scans: 362,272 points (about 725,000 triangles)
    Reconstruction: zipper
    Size of reconstruction: 35947 vertices, 69451 triangles
    Comments: contains 5 holes in the bottom

    Note about the bunny photograph:
    The bunny was bought and scanned in 1993-94.
    The color photograph (above) was taken on April 1, 2003.
    The bits of gray plaster on the sides of the bunny's feet
    somehow appeared since the bunny was scanned;
    they are not present in the 3D model.
    The chip on his left ear, however, is present in the
    model as well, although degraded in resolution.
    """
    bunny_tarball = pooch.retrieve(
        url="http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz",
        known_hash="a5720bd96d158df403d153381b8411a727a1d73cff2f33dc9b212d6f75455b84",  # noqa: E501
        progressbar=True,
    )
    extract_location = os.path.dirname(bunny_tarball)
    with tarfile.open(bunny_tarball) as file:
        file.extractall(extract_location)

    bunny_filename = os.path.join(
        extract_location, "reconstruction" + os.sep + "bun_zipper.ply"
    )
    mesh = meshio.read(bunny_filename)
    data = (mesh.points, mesh.cells[0].data)

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "surface"
    return [(data, add_kwargs, layer_type)]
