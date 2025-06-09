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
    """Return (u, v) on 'mesh' where 'locator' touches."""
    loc = pm.PyNode(locator)
    point = om.MPoint(*pm.xform(loc, q=True, ws=True, t=True))

    shape = pm.PyNode(mesh).getShape()
    sel = om.MSelectionList()
    sel.add(shape.name())
    dag = sel.getDagPath(0)

    # dag = shape.__apimdagpath__()
    fn_mesh = om.MFnMesh(dag)

    ray_dir = om.MVector(0, -1, 0)               # ray direction toward mesh
    hit = fn_mesh.closestIntersection(
        om.MFloatPoint(point), 
        om.MFloatVector(ray_dir),
        None, 
        None, 
        False,
        om.MSpace.kWorld, 
        1e6, 
        False,
        None, 
        False)

    if not hit[0]:
        return None                              # no intersection

    hit_point, hit_ray, hit_face, hit_triangle, bary1, bary2 = hit[:6]
    u, v = fn_mesh.getUVAtPoint(hit_point, om.MSpace.kWorld, uv_set)
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


