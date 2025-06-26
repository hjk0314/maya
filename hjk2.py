""" These functions were created to speed up rigging in Maya. """


import pymel.core as pm


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = []


def get_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of an object or point.

    Examples
    --------
    >>> getPosition("pSphere1")
    >>> getPosition("pSphere1.vtx[317]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    
    try:
        position = pm.pointPosition(obj_or_vtx)
    except:
        position = pm.xform(obj_or_vtx, q=1, ws=1, rp=1)
    result = [round(i, 5) for i in position]
    return tuple(result)


def get_boundingBox_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of the center pivot of the boundingBox.

    Args
    ----
    1. Objects
    2. Vertices

    Examples
    --------
    >>> get_boundingBox_position("objectName")
    >>> get_boundingBox_position("objectName.vtx[0:7]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    boundingBox = pm.xform(obj_or_vtx, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    result = ((xMin+xMax)/2, (yMin+yMax)/2, (zMin+zMax)/2)
    return result


