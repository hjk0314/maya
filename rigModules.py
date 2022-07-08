import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.core as pm
import os


# Creates a curve along the locator's trajectory.
# Place locators to create trajectories.
# If True is given to the closedCurve parameter, a circle is created.
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


# Returns the midpoint between two objects.
def getMiddlePoint(sel): # sel : tuple in list
    allPoints = [cmds.xform(i, q=True, t=True, ws=True) for i in sel]
    try:
        middlePoints = [(allPoints[0][i] + allPoints[1][i]) / 2 for i in range(3)] # ex) [1.0, -2.3, -0.4]
        return middlePoints
    except:
        return False


# Create a locator based on selection.
# This function uses the <getMiddlePoint> function.
# Create a locator at the origin if nothing is selected.
# Selecting one obj creates a locator in its place.
# When you select two obj, a locator is created at the midpoint.
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


# Add the name '_GRP' to the name and group it.
def grpOwnName(): # grouping itself and named own
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.group(em=True) # em : empty
    else:
        for i in sel:
            cmds.group(i, n="%s_GRP" % i)


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


# This function is Only works for strings sliced with underscores.
# When given a name like this : 'pCube1_22_obj_22_a2'
# Return index and its number.
# The number is last one in name.
def getNumberFromName(name): # input -> 'pCube1_22_obj_22_a2'
    nameSlice = name.split("_") # ['pCube1', '22', 'obj', '22', 'a2']
    digitList = [(j, k) for j, k in enumerate(nameSlice) if k.isdigit()] # [(1, '22'), (3, '22')]
    try:
        idx, num = digitList[-1]
        return idx, int(num)
    except:
        return False


# Attempt to delete unused plugins.
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


# Create Curve on Path.
# This function works even if you select a point.
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


# Move the key of the camera with the imagePlane, and adjust the frame offset to show the imagePlane accordingly.
def mapCameraKeyImage(destinationKey):
    sel = cmds.ls(sl=True, dag=True, type=['camera']) # ['cameraShape1']
    cam = cmds.listRelatives(sel, p=True) # ['camera1']
    try:
        currentKey = min(cmds.keyframe(cam, q=True)) # Smallest key value in camera.
        value = destinationKey - currentKey
    except:
        value = 0 # Nothing happens
        om.MGlobal.displayError("The camera has no keyframes.")
    img = cmds.listRelatives(sel, c=True) # ['imagePlane1']
    imgShape = cmds.listRelatives(img, c=True) # ['imagePlaneShape1']
    if img:
        cmds.keyframe(cam, e=True, r=True, tc=value)
        frameOffset = cmds.getAttr(imgShape[0] + ".frameOffset")
        cmds.setAttr(imgShape[0] + ".frameOffset", frameOffset - value)
    else:
        om.MGlobal.displayError("There is no imagePlane.")


# Create a curve controller.
# Create a shape with given arguments
def createCtrl(shape):
    ctrl = {
    "cub": [(-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5)], 
    "sph": [(0.0, 1.0, 0.0), (0.0, 0.707, 0.707), (0.0, 0.0, 1.0), (0.0, -0.707, 0.707), (0.0, -1.0, 0.0), (0.0, -0.707, -0.707), (0.0, 0.0, -1.0), (0.0, 0.707, -0.707), (0.0, 1.0, 0.0), (-0.707, 0.707, 0.0), (-1.0, 0.0, 0.0), (-0.707, 0.0, 0.707), (0.0, 0.0, 1.0), (0.707, 0.0, 0.707), (1.0, 0.0, 0.0), (0.707, 0.0, -0.707), (0.0, 0.0, -1.0), (-0.707, 0.0, -0.707), (-1.0, 0.0, 0.0), (-0.707, -0.707, 0.0), (0.0, -1.0, 0.0), (0.707, -0.707, 0.0), (1.0, 0.0, 0.0), (0.707, 0.707, 0.0), (0.0, 1.0, 0.0)], 
    "cyl": [(-1.0, 1.0, 0.0), (-0.707, 1.0, 0.707), (0.0, 1.0, 1.0), (0.707, 1.0, 0.707), (1.0, 1.0, 0.0), (0.707, 1.0, -0.707), (0.0, 1.0, -1.0), (0.0, 1.0, 1.0), (0.0, -1.0, 1.0), (-0.707, -1.0, 0.707), (-1.0, -1.0, 0.0), (-0.707, -1.0, -0.707), (0.0, -1.0, -1.0), (0.707, -1.0, -0.707), (1.0, -1.0, 0.0), (0.707, -1.0, 0.707), (0.0, -1.0, 1.0), (0.0, -1.0, -1.0), (0.0, 1.0, -1.0), (-0.7071, 1.0, -0.707), (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0)], 
    "pip": [(0.0, 1.0, 1), (0.0, -1.0, 1), (0.707, -1.0, 0.707), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (0.707, 1.0, -0.707), (0.0, 1.0, -1), (0.0, -1.0, -1), (-0.707, -1.0, -0.707), (-1, -1.0, 0.0), (-1, 1.0, 0.0), (-0.707, 1.0, 0.707), (0.0, 1.0, 1), (0.707, 1.0, 0.707), (1.0, 1.0, 0.0), (1.0, -1.0, 0.0), (0.707, -1.0, -0.707), (0.0, -1.0, -1), (0.0, 1.0, -1), (-0.707, 1.0, -0.707), (-1, 1.0, 0.0), (-1, -1.0, 0.0), (-0.707, -1.0, 0.707), (0.0, -1.0, 1)], 
    "con": [(0.0, 2.0, 0.0), (-0.866, 0.0, -0.0), (0.866, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 1.0), (-0.866, 0.0, -0.0), (0.866, 0.0, 0.0), (0.0, 0.0, 1.0)], 
    "cir1": [(1.0, 1.0, 0.0), (0.924, 1.0, -0.383), (0.707, 1.0, -0.707), (0.383, 1.0, -0.924), (0, 1.0, -1.0), (0.226, 1.0, -1.075), (0.172, 1.0, -0.834), (0, 1.0, -1.0)], 
    "cir2": [(1.0, 1.0, 0.0), (0.866, 1.0, -0.5), (0.5, 1.0, -0.866), (0.0, 1.0, -1.0), (-0.5, 1.0, -0.866), (-0.866, 1.0, -0.5), (-1.0, 1.0, 0.0), (-1.087, 1.0, -0.299), (-0.772, 1.0, -0.204), (-1.0, 1.0, 0.0)], 
    "cir3": [(0.866, 1.0, -0.5), (0.5, 1.0, -0.866), (0.0, 1.0, -1.0), (-0.5, 1.0, -0.866), (-0.866, 1.0, -0.5), (-1.0, 1.0, 0.0), (-0.866, 1.0, 0.5), (-0.5, 1.0, 0.866), (0.0, 1.0, 1.0), (0.5, 1.0, 0.866), (0.866, 1.0, 0.5), (0.949, 1.0, 0.19), (0.949, 1.0, 0.19), (0.816, 1.0, 0.15), (1.0, 1.0, 0.0), (1.086, 1.0, 0.231), (0.949, 1.0, 0.19)], 
    "arr1": [(0.0, 0.0, 2.0), (2.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, -2.0), (-1.0, 0.0, -2.0), (-1.0, 0.0, 1.0), (-2.0, 0.0, 1.0), (0.0, 0.0, 2.0)], 
    "arr2": [(0.0, 0.5, 2.0), (2.0, 0.5, 1.0), (1.0, 0.5, 1.0), (1.0, 0.5, -2.0), (-1.0, 0.5, -2.0), (-1.0, 0.5, 1.0), (-2.0, 0.5, 1.0), (0.0, 0.5, 2.0), (0.0, -0.5, 2.0), (2.0, -0.5, 1.0), (1.0, -0.5, 1.0), (1.0, -0.5, -2.0), (-1.0, -0.5, -2.0), (-1.0, -0.5, 1.0), (-2.0, -0.5, 1.0), (0.0, -0.5, 2.0), (2.0, -0.5, 1.0), (2.0, 0.5, 1.0), (1.0, 0.5, 1.0), (1.0, 0.5, -2.0), (1.0, -0.5, -2.0), (-1.0, -0.5, -2.0), (-1.0, 0.5, -2.0), (-1.0, 0.5, 1.0), (-2.0, 0.5, 1.0), (-2.0, -0.5, 1.0)]
    }
    try:
        cmds.curve(d=1, p=ctrl[shape])
    except:
        keyList = list(ctrl.keys())
        om.MGlobal.displayInfo(f"As input factors : {keyList}")


# Delete the node named 'vaccine_gene' and "breed_gene" in the <.ma> file.
# It is related to mayaScanner distributed by autodesk.
def deleteVaccineString(fullPath):
    vcc = "vaccine_gene"
    brd = "breed_gene"
    crt = "createNode"
    with open(fullPath, "r") as txt:
        lines = txt.readlines()
    vccList = [j for j, k in enumerate(lines) if vcc in k and crt in k] # List up the line numbers containing 'vaccine_gene'.
    brdList = [j for j, k in enumerate(lines) if brd in k and crt in k] # List up the line numbers containing 'breed_gene'.
    crtList = [j for j, k in enumerate(lines) if crt in k] # List up the line numbers containing 'createNode'.
    sum = vccList + brdList # ex) [16, 21, 84, 105]
    deleteList = []
    # List lines to delete consecutively
    for min in sum:
        max = crtList[crtList.index(min) + 1]
        deleteList += [i for i in range(min, max)]
    new, ext = os.path.splitext(fullPath)
    new += "_fixed" + ext
    # When creating a new file, delete the 'vaccine_gene' or 'breed_gene' paragraph.
    # Write '//Deleted here' instead of the deleted line.
    with open(new, "w") as txt:
        for j, k in enumerate(lines):
            if j in deleteList:
                txt.write("// Deleted here.\n")
            else:
                txt.write(k)


# Delete this file : "vaccine.py", "vaccine.pyc", "userSetup.py" in "C:/Users/user/Documents/maya/scripts/"
def deleteVaccineFiles():
    dir = cmds.internalVar(uad=True) + "scripts/"
    fileList = [dir + i for i in ["vaccine.py", "vaccine.pyc", "userSetup.py"]]
    for i in fileList:
        if os.path.isfile(i):
            os.remove(i)
        else:
            pass


# Checking First, if the file is infected or not.
def checkVaccineString(fullPath):        
    with open(fullPath, "r") as txt:
        lines = txt.readlines()
    result = ''
    for i in lines:
        if "vaccine_gene" in i or "breed_gene" in i:
            result = fullPath
            break
        else:
            pass
    return result

