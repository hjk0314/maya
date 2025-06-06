"""Utilities for retrieving UV coordinates using PyMel."""

import pymel.core as pm


def get_component_uv_coordinates(component):
    """Return the UV coordinates for a mesh component.

    Parameters
    ----------
    component : str or pm.PyNode
        Mesh component such as a face, vertex, edge or uv.

    Returns
    -------
    list of tuple
        List of ``(u, v)`` values for each UV found on the component.
    """
    uv_comp = pm.polyListComponentConversion(component, toUV=True)
    uv_comp = pm.ls(uv_comp, fl=True)

    result = []
    for uv in uv_comp:
        u, v = pm.polyEditUV(uv, query=True)
        result.append((u, v))
    return result


def get_uv_coords_from_faces(mesh, face_indices, uv_set=None):
    """Collect UV coordinates for specific faces of a mesh.

    Parameters
    ----------
    mesh : str or pm.nt.Mesh
        Target mesh object or its transform.
    face_indices : iterable of int
        The face indices to query.
    uv_set : str, optional
        Name of the UV set. If ``None`` the current UV set is used.

    Returns
    -------
    dict
        Mapping of face index to a list of ``(u, v)`` coordinates.
    """
    node = pm.PyNode(mesh)
    shape = node.getShape() if node.nodeType() != 'mesh' else node

    if uv_set is None:
        uv_set = shape.getCurrentUVSetName()

    result = {}
    for index in face_indices:
        face = shape.f[index]
        uv_coords = get_component_uv_coordinates(face)
        result[index] = uv_coords
    return result



def get_face_center(face):
    """Return the centroid of a polygon face.

    Parameters
    ----------
    face : str or pm.MeshFace
        Mesh face component to query.

    Returns
    -------
    tuple
        Coordinates ``(x, y, z)`` of the face center in world space.
    """
    comp = pm.PyNode(face)
    verts = pm.polyListComponentConversion(comp, toVertex=True)
    verts = pm.ls(verts, fl=True)

    if not verts:
        return (0.0, 0.0, 0.0)

    positions = [pm.pointPosition(v, world=True) for v in verts]
    avg = [sum(vals) / len(positions) for vals in zip(*positions)]
    return tuple(avg)
