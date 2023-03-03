"""File formats supported by meshio."""

DEFAULT_MESH_FORMAT = (
    ".ply"  # Default mesh file format for writing surfaces to file.
)

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
