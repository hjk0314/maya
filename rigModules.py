import maya.cmds as cmds
import maya.OpenMaya as om


def createCurveUsingLocator(closedCurve): # input : True or False
    sel = cmds.ls(sl=True) # select locators
    if not sel:
        om.MGlobal.displayWarning('Nothing selected.')
    else:
        chk = closedCurve
        locatorPosition = [cmds.xform(i, q=True, ws=True, rp=True) for i in sel] # every position of locators
        if not chk:
            cmds.curve(p=locatorPosition)
        else:
            # create circle first, and change their shape.
            circleName = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ch=False, s=len(sel))[0]
            for j, k in enumerate(locatorPosition):
                cmds.move(k[0], k[1], k[2], '%s.cv[%d]' % (circleName, j), ws=True)


def getMiddlePoint(sel): # sel : tuple in list
    allPoints = [cmds.xform(i, q=True, t=True, ws=True) for i in sel]
    try:
        middlePoints = [(allPoints[0][i] + allPoints[1][i]) / 2 for i in range(3)] # x, y, z coordinates
        return middlePoints
    except:
        return False


def createLocatorMidpoint():
    sel = cmds.ls(sl=True, fl=True)
    selNumber = len(sel)
    if selNumber == 1: # Select One point.
        position = cmds.xform(sel[0], q=True, t=True, ws=True)
    elif selNumber == 2: # Select Two points.
        position = getMiddlePoint(sel)
    else:
        position = (0, 0, 0)
    locator = cmds.spaceLocator()
    cmds.xform(locator, t=position, ws=True)


def grpOwnName(): # grouping itself and named own
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.group(em=True) # em : empty
    else:
        for i in sel:
            cmds.group(i, n="%s_GRP" % i)


grpOwnName()