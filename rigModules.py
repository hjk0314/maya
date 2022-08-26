import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.core as pm
import json
import os


# Returns the midpoint between two objects.
def getMiddlePoint(sel): # sel : tuple in list
    allPoints = [cmds.xform(i, q=True, t=True, ws=True) for i in sel]
    try:
        middlePoints = [(allPoints[0][i] + allPoints[1][i]) / 2 for i in range(3)] # ex) [1.0, -2.3, -0.4]
        return middlePoints
    except:
        return False


# Create channel attributes on a controller or group.
def createChannel(name, typ):
    sel = cmds.ls(sl=True)
    channelName = name
    channelType = typ # ex) "bool", "double"
    for ctrl in sel:
        channelChek = cmds.attributeQuery(channelName, node=ctrl, ex=True) # ex = exist
        if not channelChek:
            cmds.addAttr(ctrl, ln=channelName, at=channelType, dv=0)
            cmds.setAttr("%s.%s" % (ctrl, channelName), e=True, k=True)
        else:
            pass


 # input elements is fullPath or string.
 # ex1) "C:/Users/userName/Desktop/expressionSource.txt"
 # ex2) "tx = sin(time);"
def writeExpression(fullPath):
    ext = os.path.splitext(fullPath)[-1] # .txt
    chk = os.path.isfile(fullPath)
    if ext == ".txt" and chk: # ex1) fullPath
        with open(fullPath, 'r') as txt:
            srcList = txt.readlines()
        src = "".join(srcList)
    else: # ex2) string
        src = fullPath
    try:
        # s=string, o=object, ae=alwaysEvaluate, uc=unitConversion
        cmds.expression(s=src, o='', ae=1, uc='all')
    except:
        om.MGlobal.displayError('Fail to write expressions.')


# Delete Constraints and Break Connections scale and visibility.
def deleteConstraintAndConnection():
    sel = pm.ls(sl=True, type=["transform"])
    sel2 = [i for i in sel if not "Constraint" in pm.nodeType(i)]
    channelList = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]
    for i in sel2:
        for j in channelList:
            pm.setAttr(i + j, k=True, l=False)
            try:
                pm.disconnectAttr(i + j) # Break connections : scale, visibility
            except:
                pass
        pm.delete(i, cn=True)


# show drawStyle in joint attributes.
def setBoneDrawStyle(attr="drawStyle"):
    sel = pm.ls(sl=True)
    for i in sel:
        chkAttr = pm.attributeQuery(attr, node=i, ex=True)
        if chkAttr:
            pm.setAttr("%s.%s" % (i, attr), 0)
        else:
            pass


# return last number from name.
def getNumberFromName(name): # Input -> 'pCube1_22_obj_22_a2'
    nameList = name.split('_') # ['pCube1', '22', 'obj', '22', 'a2']
    digitLst = [(j, k) for j, k in enumerate(nameList) if k.isdigit()] # [(1, '22'), (3, '22')]
    try:
        index, number = digitLst[-1] # index = 3, number = '22'
        return int(number)
    except:
        return False


# Sets the color of the controller.
# idx : blue=6, red=13, yellow=17
def setColorRed(idx=13):
    sel = cmds.ls(sl=True, dag=True, s=True, type=["mesh"])
    for i in sel:
        cmds.setAttr(i + ".overrideEnabled", 1)
        cmds.setAttr(i + ".overrideColor", idx)

