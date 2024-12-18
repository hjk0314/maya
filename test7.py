import pymel.core as pm
import math


def getDistance(xyz1, xyz2):
    """ Both arguments are coordinates. 
    Returns the distance between the two coordinates.
    
    Args: 
        >>> getDistance((0,0,0), (1,2,3))
        >>> getDistance([0,0,0], [1,2,3])
     """
    result = math.sqrt(sum((a - b)**2 for a, b in zip(xyz1, xyz2)))
    return result


def moveNearbyPoint(source: str, *arg):
    """ The selected point moves to the closest point 
    on the source object. This function only works for points on -X.
    The Selected Points move to the closest points possible, 
    the objects should overlap as much as possible.
    
    Examples:
        >>> moveNearbyPoint("pSphere1", "pSphere2.vtx[:23]")
        >>> moveNearbyPoint("pSphere1")
     """
    sel = arg if arg else pm.selected(fl=True)
    if not isinstance(source, pm.PyNode):
        src = pm.PyNode(source)
    sourceVertices = {i.name(): pm.pointPosition(i) for i in src.vtx[:]}
    for i in sel:
        if not isinstance(i, pm.MeshVertex):
            pm.warning("Please, Select a Vertices.")
            continue
        temp = {}
        iPos = pm.pointPosition(i)
        x = iPos[0]
        if x >= 0:
            continue
        else:
            for srcVtx, srcVtxPos in sourceVertices.items():
                temp[srcVtx] = getDistance(iPos, srcVtxPos)
        minimumKey = min(temp, key=temp.get)
        pm.move(i, sourceVertices[minimumKey])





