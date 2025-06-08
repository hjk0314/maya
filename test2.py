import pymel.core as pm


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


sel = pm.ls(sl=True, fl=True)
for i in sel:
    pf = pm.PyNode(i)
    pfShp = pf.node()
    folShp = pm.createNode("follicle")
    fol = folShp.getParent()
    pm.connectAttr(f"{folShp}.outTranslate", f"{fol}.translate", f=1)
    pm.connectAttr(f"{folShp}.outRotate", f"{fol}.rotate", f=1)
    pm.connectAttr(f"{pfShp}.outMesh", f"{folShp}.inputMesh", f=1)
    pm.connectAttr(f"{pfShp}.worldMatrix[0]", f"{folShp}.inputWorldMatrix", f=1)
    uValue, vValue = getUVcoordinates(i.name())
    pm.setAttr(f"{folShp}.parameterU", uValue)
    pm.setAttr(f"{folShp}.parameterV", vValue)
