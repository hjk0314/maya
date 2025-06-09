import pymel.core as pm
import maya.api.OpenMaya as om


def getUVcoordinates(face, uvSet=None):
    """Return the UV-space ``Center`` of a polygon face.

    Parameters
    ----------
    face : str or pm.MeshFace
        Mesh face component to query.
    uvSet : str, optional
        UV set name to use. Defaults to the current set.

    Examples    
    --------
    getUVcoordinates("pSphere1.f[279]")
    
    Returns
    -------
    tuple
        Coordinates ``(u, v)`` of the face center in UV space.
    """
    temp = pm.PyNode(face)
    tempShape = temp.node()
    if uvSet:
        pm.polyUVSet(tempShape, currentUVSet=True, uvSet=uvSet)
    uvs = pm.polyListComponentConversion(temp, toUV=True)
    uvs = pm.ls(uvs, fl=True)
    if not uvs:
        return (0.0, 0.0)
    coords = [pm.polyEditUV(uv, query=True) for uv in uvs]
    mean_u = sum(u for u, _ in coords) / len(coords)
    mean_v = sum(v for _, v in coords) / len(coords)
    return (mean_u, mean_v)


def locator_uv(locator, mesh, uv_set="map1"):
    """Return the UV coordinates on ``mesh`` where ``locator`` lies.

    Parameters
    ----------
    locator : str or pm.PyNode
        Locator snapped onto the mesh (for example via *Make Live*).
    mesh : str or pm.PyNode
        Mesh on which the locator is positioned.
    uv_set : str, optional
        Name of the UV set to sample from. ``"map1"`` by default.

    Returns
    -------
    tuple
        ``(u, v)`` coordinates on ``mesh`` corresponding to the locator's
        world-space position.

    Notes
    -----
    Uses Maya API 2.0 (tested with version 20220300).
    """

    loc = pm.PyNode(locator)
    pos = om.MPoint(*pm.xform(loc, q=True, ws=True, t=True))

    shape = pm.PyNode(mesh).getShape()
    sel = om.MSelectionList()
    sel.add(shape.name())
    dag = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)

    closest_point, _ = fn_mesh.getClosestPoint(pos, om.MSpace.kWorld)
    uv = fn_mesh.getUVAtPoint(closest_point, om.MSpace.kWorld, uv_set)
    u, v = uv[:2]
    return u, v


def create_follicles(mesh, locators, uv_set="map1"):
    """Create follicles on ``mesh`` at the positions of ``locators``.

    Parameters
    ----------
    mesh : str or pm.PyNode
        Mesh used to host the follicles.
    locators : iterable
        Locators whose positions should be converted to UV coordinates.
    uv_set : str, optional
        UV set to query. ``"map1"`` by default.

    Returns
    -------
    list of pm.PyNode
        The created follicle transform nodes.
    """

    py_mesh = pm.PyNode(mesh)
    mesh_shape = py_mesh.getShape()
    follicles = []

    for loc in locators:
        fol_shape = pm.createNode("follicle")
        fol = fol_shape.getParent()

        pm.connectAttr(f"{fol_shape}.outTranslate", f"{fol}.translate", f=1)
        pm.connectAttr(f"{fol_shape}.outRotate", f"{fol}.rotate", f=1)
        pm.connectAttr(f"{mesh_shape}.outMesh", f"{fol_shape}.inputMesh", f=1)
        pm.connectAttr(
            f"{mesh_shape}.worldMatrix[0]", f"{fol_shape}.inputWorldMatrix", f=1
        )

        u, v = locator_uv(loc, py_mesh, uv_set)
        pm.setAttr(f"{fol_shape}.parameterU", u)
        pm.setAttr(f"{fol_shape}.parameterV", v)

        follicles.append(fol)

    return follicles




if __name__ == "__main__":
    sel = pm.ls(sl=True, fl=True)
    mesh = "pSphere1"
    create_follicles(mesh, sel)


