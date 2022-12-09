import pymel.core as pm
import maya.OpenMaya as om


def mirrorCopy(idx, selection):
    if idx != 'x' and idx != 'z':
        print("X and Z directions are available.")
    elif not selection:
        print("Nothing selected.")
    else:
        grp = pm.group(em=True, n=f'{selection}_mirrorCopy')
        pm.matchTransform(grp, selection, pos=True, rot=True)
        tra = pm.getAttr(f'{grp}.translate')
        rot = pm.getAttr(f'{grp}.rotate')
        tX, tY, tZ = tra
        rX, rY, rZ = rot
        if idx == 'x':
            tX *= -1
            rX += (180 if rX < 0 else -180)
            rY *= -1
            rZ *= -1
        else:
            tZ *= -1
            rZ += (180 if rZ < 0 else -180)
        attr = {'tX': tX, 'tY': tY, 'tZ': tZ, 'rX': rX, 'rY': rY, 'rZ': rZ}
        for j, k in attr.items():
            pm.setAttr(f'{grp}.%s' % j, k)


def renameDup(objName):
    if '_L' in objName:
        result = objName.replace('_L', '_R')
    elif '_R' in objName:
        result = objName.replace('_R', '_L')
    else:
        result = ''
    return result


sel = pm.ls(sl=True)


def temp(selection):
    cuv = selection.getChildren()
    shp = pm.ls(cuv, dag=True, s=True)
    if pm.objectType(shp) == 'nurbsCurve':
        name = renameDup(cuv[0].name())
        copy = pm.duplicate(cuv, rr=True, n=name)
        pm.parent(copy, w=True)
        grp = pm.group(em=True)
        pm.parent(copy, grp)
        # pm.duplicate(grp, rr=True, rc=True)
        pm.scale(grp, [-1, 1, 1], r=True)
    else:
        pass
    print(copy)


for i in sel:
    temp(i)