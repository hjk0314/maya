
from hjk import *

def growingJoint():
    sel = pm.ls(sl=True)
    pointList = []
    jointList = []
    pm.select(cl=True)
    for i in sel:
        jntName = i.replace('loc_', 'jnt_')
        print(jntName)
        point = pm.xform(i, q=1, ws=1, rp=1)
        joint = pm.joint(p=point, n=jntName, rad=50)
        pointList.append(point)
        jointList.append(joint)
    pm.select(jointList[0])
    orientJnt()
    ikHName = jointList[0].replace('jnt_', 'ikH_')
    pm.ikHandle(sj=jointList[0], ee=jointList[1], sol='ikSCsolver', n=ikHName)
    Dimension = pm.distanceDimension(sp=pointList[0], ep=pointList[1])
    Distance = pm.getAttr(f"{Dimension}.distance")
    Distance = round(Distance, 3)
    expr = f"{jointList[0]}.scaleX = {Dimension}.distance / {Distance};"
    pm.expression(s=expr, o='', ae=1, uc='all')


# growingJoint()
# rename('spoiler_L', 'spoiler_R')


# grpNull()
# ctrl(pointer=True)
# color(red=True)
# color(blue=True)
# color(blue2=True)
# color(pink=True)
# color(green=True)
# color(green2=True)
# color(red2=True)
# color(yellow=True)


# 79 char line ================================================================
# 72 docstring or comments line ========================================


def cleanFBX():
    sel = pm.ls(sl=True)
    obj, jnt = sel
    fullPath = pm.Env().sceneName()
    bName = os.path.basename(fullPath)
    name, ext = os.path.splitext(bName)
    pm.rename(obj, name)
    pm.select(jnt, hi=True)
    pm.delete(sc=True, uac=False, hi=0, cp=0, s=0)
    rename("Bip01FBXASC032", "jnt_")
    rename("FBXASC032", "_")
    pm.rename(jnt, 'jnt_root')
    pm.currentUnit(t="film")


# a = om.MFileIO_currentFile()
# om.MFileIO_open('C:/users/jkhong/Desktop/a.ma')


# cleanFBX()


def tmpGrp():
    sel = pm.ls(sl=True)
    nameList = ["skeleton", "MODEL", "controller"]
    for j, k in enumerate(sel):
        pm.group(k, n=nameList[j])
    rigGrp = pm.group(nameList[0], nameList[2], n="rig")
    pm.group(rigGrp, nameList[1], n=f"{sel[1]}_rig")


tmpGrp()
