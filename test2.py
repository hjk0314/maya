import pymel.core as pm
from general import *


def mirrorCopy(obj, mirrorPlane="YZ"):
    changedName = replaceLeftRight(obj)
    copied = pm.duplicate(obj, rr=True, n=changedName)
    pm.parent(copied, w=True)
    grp = pm.group(em=True)
    pm.parent(copied, grp)
    if mirrorPlane == "XY":
        direction = [1, 1, -1]
    elif mirrorPlane == "YZ":
        direction = [-1, 1, 1]
    else:
        return
    pm.scale(grp, direction, r=True)
    mirrorGrp = mirrorGrouping(obj)
    pm.parent(copied, mirrorGrp)
    pm.makeIdentity(copied, a=True, t=1, r=1, s=1, n=0, pn=1)
    pm.delete(grp)



def mirrorGrouping(obj, mirrorPlane="YZ"):
    changedName = replaceLeftRight(obj)
    grp = pm.group(em=True, n=changedName)
    pm.matchTransform(grp, obj, pos=True, rot=True)
    pos = pm.getAttr(f'{grp}.translate')
    rot = pm.getAttr(f'{grp}.rotate')
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
        pm.setAttr(f'{grp}.{key}', value)
    return grp
