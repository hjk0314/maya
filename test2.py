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
    """Return ``(u, v)`` of ``mesh`` corresponding to ``locator``.

    The locator is assumed to lie on the surface (e.g. via *Make Live*).
    Compatible with Maya API version 20220300.
    """

    # World-space location of the locator
    loc = pm.PyNode(locator)
    pos = om.MPoint(*pm.xform(loc, q=True, ws=True, t=True))

    # Build an API 2.0 dag path for the mesh
    shape = pm.PyNode(mesh).getShape()
    sel = om.MSelectionList()
    sel.add(shape.name())
    dag = sel.getDagPath(0)
    fn_mesh = om.MFnMesh(dag)

    # Find the nearest point on the mesh
    closest_point, _ = fn_mesh.getClosestPoint(pos, om.MSpace.kWorld)

    # Query UV coordinates at that point
    u, v = fn_mesh.getUVAtPoint(closest_point, om.MSpace.kWorld, uv_set)
    return u, v


sel = pm.ls(sl=True, fl=True)
# for i in sel:
#     pf = pm.PyNode(i)
#     pfShp = pf.node()
#     folShp = pm.createNode("follicle")
#     fol = folShp.getParent()
#     pm.connectAttr(f"{folShp}.outTranslate", f"{fol}.translate", f=1)
#     pm.connectAttr(f"{folShp}.outRotate", f"{fol}.rotate", f=1)
#     pm.connectAttr(f"{pfShp}.outMesh", f"{folShp}.inputMesh", f=1)
#     pm.connectAttr(f"{pfShp}.worldMatrix[0]", f"{folShp}.inputWorldMatrix", f=1)
#     uValue, vValue = getUVcoordinates(i.name())
#     pm.setAttr(f"{folShp}.parameterU", uValue)
#     pm.setAttr(f"{folShp}.parameterV", vValue)


mesh = "pSphere1"
pyMesh = pm.PyNode(mesh)
pyMeshShape = pyMesh.getShapes()
pyMeshShape = pyMeshShape[0]
for i in sel:
    folShp = pm.createNode("follicle")
    fol = folShp.getParent()
    pm.connectAttr(f"{folShp}.outTranslate", f"{fol}.translate", f=1)
    pm.connectAttr(f"{folShp}.outRotate", f"{fol}.rotate", f=1)
    pm.connectAttr(f"{pyMeshShape}.outMesh", f"{folShp}.inputMesh", f=1)
    pm.connectAttr(f"{pyMeshShape}.worldMatrix[0]", f"{folShp}.inputWorldMatrix", f=1)
    uValue, vValue = locator_uv(i, pyMesh)
    pm.setAttr(f"{folShp}.parameterU", uValue)
    pm.setAttr(f"{folShp}.parameterV", vValue)


