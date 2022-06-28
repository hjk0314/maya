import maya.cmds as cmds
import maya.OpenMaya as om
import os


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


# This function is Only works for strings sliced with underscores.
def getNumberFromName(name): # input -> 'pCube1_22_obj_22_a2'
    nameSlice = name.split("_") # ['pCube1', '22', 'obj', '22', 'a2']
    digitList = [(j, k) for j, k in enumerate(nameSlice) if k.isdigit()] # [(1, '22'), (3, '22')]
    try:
        idx, num = digitList[-1]
        return idx, int(num)
    except:
        return False


def deleteUnknownPlugins():
    cmds.delete(cmds.ls(type="unknown")) # Just delete Unknown type lists.
    pluginsList = cmds.unknownPlugin(q=True, l=True)
    if pluginsList:
        for j, k in enumerate(pluginsList):
            cmds.unknownPlugin(k, r=True)
            print("%d : %s" % (j, k)) # Print deleted plugin's names and number
        print('Delete completed.')
    else:
        om.MGlobal.displayWarning("There are no unknown plugins.")


# Create Curve on Path
def createCurvePath(startFrame, endFrame):
    sel = cmds.ls(sl=True, fl=True)
    for j in sel:
        pointList = []
        for k in range(startFrame, endFrame + 1):
            cmds.currentTime(k)
            try:
                pointList.append(cmds.pointPosition(j)) # vtx position
            except:
                pointList.append(cmds.xform(j, q=True, ws=True, rp=True)) # obj position
        cmds.curve(p=pointList) # make Curves


# Offset the Keys
def offsetKey(interval):
    sel = cmds.ls(sl=True, fl=True)
    for j, k in enumerate(sel):
        cmds.keyframe(k, e=True, r=True, tc = j * interval)


def delVaccine(fullPath):
    vcc = "vaccine_gene"
    brd = "breed_gene"
    crt = "createNode"
    with open(fullPath, "r") as txt:
        lines = txt.readlines()
    # for p, q in enumerate(lines):
    #     print(p, q.rstrip())
    vccList = [j for j, k in enumerate(lines) if vcc in k and crt in k]
    brdList = [j for j, k in enumerate(lines) if brd in k and crt in k]
    crtList = [j for j, k in enumerate(lines) if crt in k]
    # print(vccList)
    # print(brdList)
    # print(crtList)
    sum = vccList + brdList
    deleteList = []
    for min in sum:
        max = crtList[crtList.index(min) + 1]
        deleteList += [i for i in range(min, max)]
    # print(deleteList)
    new, ext = os.path.splitext(fullPath)
    new += "_fix" + ext
    # print(new)
    with open(new, "w") as txt:
        for j, k in enumerate(lines):
            if j in deleteList:
                txt.write("// Deleted here.\n")
            else:
                txt.write(k)

