""" These functions were created to speed up rigging in Maya. """


from typing import Union
import pymel.core as pm
import math


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = []


def sel(func) -> dict:
    """ If there is no argument in the wrapper,
    Pass the selected object as an argument to the wrapper.
     """
    def wrapper(*args):
        selections = args if args else pm.ls(sl=True, fl=True)
        result = {}
        for i in selections:
            temp = i.name() if isinstance(i, pm.PyNode) else i
            result[temp] = func(i)
        return result
    return wrapper


# @sel
def get_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of an object or point.

    Examples
    --------
    >>> get_position("pSphere1")
    >>> get_position("pSphere1.vtx[317]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    
    try:
        position = pm.pointPosition(obj_or_vtx)
    except:
        position = pm.xform(obj_or_vtx, q=1, ws=1, rp=1)
    result = [round(i, 5) for i in position]
    return tuple(result)


# @sel
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
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    result = [round(i, 5) for i in [x, y, z]]
    return tuple(result)


# @sel
def get_boundingBox_size(obj_or_vtx: str) -> tuple:
    """ Get the length, width, and height of the bounding box.

    Args
    ----
    1. Objects
    2. Vertices

    Examples
    --------
    >>> get_boundingBox_size("objectName")
    >>> get_boundingBox_size("objectName.vtx[0:7]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    boundingBox = pm.xform(obj_or_vtx, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMax - xMin) / 2
    y = (yMax - yMin) / 2
    z = (zMax - zMin) / 2
    result = [round(i, 5) for i in [x, y, z]]
    return tuple(result)


def get_flattenList(data, seen=None) -> list:
    """ Flattens a list within a list. 

    Examples
    --------
    >>> get_flattenList(["ab", ["bc"], ["ef"]], [[["gh", ], "ij"], "jk"], ...)
    >>> ['ab', 'bc', 'ef', 'gh', 'ij', 'jk']
     """
    if seen is None:
        seen = set()
    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in seen:
                seen.add(key)
                result.append(key)
            result.extend(get_flattenList(value, seen))
    elif isinstance(data, list):
        for item in data:
            result.extend(get_flattenList(item, seen))
    else:
        if data not in seen:
            seen.add(data)
            result.append(data)
    return result


def get_distance(point1: Union[tuple, list], 
                 point2: Union[tuple, list]) -> float:
    """ Both arguments are coordinates. 
    Returns the distance between the two coordinates.
    
    Examples
    --------
    >>> get_distance((0,0,0), (1,2,3))
    >>> get_distance([0,0,0], [1,2,3])
     """
    result = math.sqrt(sum((a - b)**2 for a, b in zip(point1, point2)))
    result = round(result, 5)
    return result


def get_referencedList() -> list:
    """ Returns a list of groups of referenced. 
    
    Examples
    --------
    >>> get_referencedList()
    >>> [nt.Transform('vhcl_bestaB_mdl_v9999:bestaB'), ...]
     """
    references = pm.listReferences()
    if not references:
        result = []
    else:
        result = [ref.nodes()[0] for ref in references if ref.nodes()]
    return result


def get_subJoints(startJnt: str, endJnt: str) -> list:
    """ Get the sub joints from the start joint to the end joint. 
    The end joint is not included.
     """
    if not isinstance(startJnt, pm.PyNode):
        startJnt = pm.PyNode(startJnt)
    result = [startJnt]
    subJnt = pm.listRelatives(startJnt, c=True, type="joint")
    if subJnt and not (endJnt in subJnt):
        result += get_subJoints(subJnt[0], endJnt)
        # for i in subJnt:
        #     result += getSubJoint(i, endJoint)
    return result


