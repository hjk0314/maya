import pymel.core as pm
from general import *


def mirrorCopy(obj: str, mirrorPlane: str="YZ") -> list:
    """ Mirror copy based on 'YZ' or 'XY'. Default mirrorPlane is "YZ".
    This function is shown below.
    - First, Check Selection.
    - Duplicate and Grouping own Pivot.
    - Move Groups to Other Side.
    - Creates a Mirror Shape.
    - Finish and Clean up. 

    >>> mirrorCopy()
    >>> -> Error Message.
    >>> mirrorCopy('pCube1')
    >>> ['pCube1_grp', 'pCube1_null', 'pCube2']
    >>> mirrorCopy('cc_doorLeftFront')
    >>> ['cc_doorRight_grp', 'cc_doorRight_null', 'cc_doorRight']
    >>> mirrorCopy('lever_R', 'XY')
    >>> ['lever_L_grp', 'lever_L_null', 'lever_L']
     """
    # Check Selection
    if not obj:
        pm.warning("Nothing Selected.")
        return
    # Duplicate and Grouping own Pivot
    replaced = replaceLeftRight(obj)
    copied = pm.duplicate(obj, rr=True, n=replaced)[0]
    pm.parent(copied, w=True)
    result = groupOwnPivot(copied, null=True, n=replaced)
    topGrp, nullGrp, copied = result
    pm.parent(copied, w=True)
    # Move Groups to Other Side.
    pos = pm.getAttr(f'{topGrp}.translate')
    rot = pm.getAttr(f'{topGrp}.rotate')
    tx, ty, tz = pos
    rx, ry, rz = rot
    if mirrorPlane == "YZ":
        tx *= -1
        rx += (180 if rx < 0 else -180)
        ry *= -1
        rz *= -1
    else:
        tz *= -1
        rz += (180 if rz < 0 else -180)
    attr = {'tx': tx, 'ty': ty, 'tz': tz, 'rx': rx, 'ry': ry, 'rz': rz}
    for key, value in attr.items():
        pm.setAttr(f'{topGrp}.{key}', value)
    # Creates a Mirror Shape.
    tempGrp = pm.group(em=True)
    pm.parent(copied, tempGrp)
    if mirrorPlane == "XY":
        direction = [1, 1, -1]
    elif mirrorPlane == "YZ":
        direction = [-1, 1, 1]
    else:
        return
    pm.scale(tempGrp, direction, r=True)
    # Finish and Clean up.
    pm.parent(copied, nullGrp)
    pm.makeIdentity(copied, a=True, t=1, r=1, s=1, n=0, pn=1)
    pm.delete(tempGrp)
    return result


