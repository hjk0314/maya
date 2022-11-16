import re
import os
import subprocess
import maya.OpenMaya as om
import pymel.core as pm


# 79 char line ================================================================
# 72 docstring or comments line ========================================


def cPoint():
    sel = pm.ls(sl=True, fl=True)
    for j in [pm.pointPosition(i) for i in sel]:
        print(j)


def createCircle():
    sel = pm.ls(sl=True)
    for i in sel:
        cc = pm.circle(c=(0,0,0), nr=(1,0,0), ch=False, sw=180)
        pm.matchTransform(cc, i, pos=True, rot=True)


def matchLoc():
    sel = pm.ls(sl=True)
    for i in sel:
        loc = pm.spaceLocator()
        pm.matchTransform(loc, i, pos=True)


# Seperate with Material Name.
def seperateMat():
    sel = pm.ls(sl=True)
    for j in sel:
        sepList = pm.polySeparate(j, ch=False)
        for k in sepList:
            shd = k.shadingGroups()[0] # shading engine
            all = pm.listConnections(shd) # All connecting list
            mat = pm.ls(all, mat=True)[0] # Only Material name
            pm.rename(k, f"{k}_{mat}")


# Put the joint or locator at the cluster location.
def clt(**kwargs):
    sel = pm.ls(sl=True, fl=True)
    for key, value in kwargs.items():
        pm.select(sel)
        clt = pm.cluster(sel,relative=True)
        if not sel:
            om.MGlobal.displayError("Nothing selected.")
        elif key == "loc" and value:
            loc = pm.spaceLocator()
            pm.matchTransform(loc, clt, pos=True)
        elif key == "jnt" and value:
            pm.select(cl=True)
            jnt = pm.joint(p=(0,0,0))
            pm.matchTransform(jnt, clt, pos=True)
        else:
            om.MGlobal.displayWarning("Select 'jnt' or 'loc' to create.")
        pm.delete(clt)
            

sel = pm.ls(sl=True, dag=True, s=True)
print(sel)
for i in sel:
    result = pm.listAttr(i, r=True, sa=True, lf=True, fp=True)
    print('\n'.join(result))
    print(len(result))


sel = pm.ls(sl=True)
bb = pm.xform(sel, q=True, boundingBox=True)

print(bb)