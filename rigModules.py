import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.core as pm
import json
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


# using pymel.core
# Grabs only the given type from the selected group and returns the list.
def getTypeOnly(typ = "mesh"):
    if typ == "joint":
        shp = pm.ls(sl=True, dag=True, type=["joint"])
        obj = [i.name() for i in shp]
    else:
        shp = pm.ls(sl=True, dag=True, s=True)
        obj = [i.getParent().name() for i in shp if pm.nodeType(i) == "mesh"]
    pm.select(obj)
    lst = pm.ls(sl=True)
    return lst


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


# Create a locator at the selected joint location.
# And return the locators list.
def createLocatorObjPosition():
    sel = pm.ls(sl=True)
    locatorList = []
    for i in sel:
        locator = pm.spaceLocator(n="%s_locator" % i, p=(0, 0, 0))
        pm.matchTransform(locator, i, pos=True)
        locatorList.append(locator)
    return locatorList


# Create an empty group and match the pivot with the selector.
def createEmptyGroup():
    sel = cmds.ls(sl=True)
    for i in sel:
        grp = cmds.group(em=True, n=i + "_offset")
        cmds.matchTransform(grp, i, pos=True, rot=True)
        try:
            iParent = "".join(cmds.listRelatives(i, p=True)) # Selector's mom group.
            cmds.parent(grp, iParent)
        except:
            pass
        cmds.parent(i, grp)


# Sets the color of the controller.
# idx : blue=6, red=13, yellow=17
def setColorRed(idx=13):
    sel = cmds.ls(sl=True, dag=True, s=True, type=["mesh"])
    for i in sel:
        cmds.setAttr(i + ".overrideEnabled", 1)
        cmds.setAttr(i + ".overrideColor", idx)


class abc():
    def __init__(self):
        min = pm.playbackOptions(q=True, min=True)
        max = pm.playbackOptions(q=True, max=True)
        self.setupUI(min, max)


    def setupUI(self, min, max):
        if pm.window('exportABC_withShader', exists=True):
            pm.deleteUI('exportABC_withShader')
        else:
            win = pm.window('exportABC_withShader', t='Export to Alembic with Shader', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=380)
            pm.separator(h=10)
            pm.button(l='JSON and shadingEngine', c=lambda x: self.jsonButton())
            self.frameRange = pm.intFieldGrp(l='Range : ', nf=2, v1=min, v2=max)
            self.oneFileCheck = pm.checkBoxGrp(l='One File : ', ncb=1, v1=True)
            pm.button(l='Export ABC', c=lambda x: self.exportButton())
            pm.button(l='Import ABC', c=lambda x: print('import ABC'))
            pm.button(l='Assign', c=lambda x: print('assign'))
            pm.separator(h=10)
            pm.showWindow(win)


    def jsonButton(self):
        sel = pm.ls(sl=True, dag=True, s=True)
        if not sel:
            om.MGlobal.displayError("Nothing Selected.")
        elif self.checkSameName(sel):
            om.MGlobal.displayError("Same name exists.")
        else:
            shdEngList = self.getShadingEngine(sel)
            jsonPath = pm.fileDialog2(fm=0, ff='json (*.json);; All Files (*.*)')
            if not jsonPath:
                om.MGlobal.displayInfo('Canceled.')
            else:
                jsonPath = ''.join(jsonPath)
                self.createJson(shdEngList, jsonPath)
                self.exportShader(shdEngList, jsonPath)


    def checkSameName(self, nameList):
        sameName = [i for i in nameList if "|" in i]
        return sameName


    def getShadingEngine(self, sel):
        dic = {}
        for i in sel:
            try:
                shadingEngine = i.shadingGroups()[0].name()
            except:
                continue
            objName = i.getParent().name()
            objName = objName.split(":")[-1] if ":" in objName else objName
            dic[objName] = shadingEngine
        return dic


    def createJson(self, dic, jsonPath):
        with open(jsonPath, 'w') as JSON:
            json.dump(dic, JSON, indent=4)


    def exportShader(self, dic, fullPath):
        (dir, ext) = os.path.splitext(fullPath)
        exportPath = "%s_shader%s" % (dir, ext)
        shdEngList = list(set(dic.values()))
        pm.select(cl=True)
        pm.select(shdEngList, ne=True)
        pm.exportSelected(exportPath, type="mayaAscii", f=True)


    def exportButton(self):
        sel = pm.ls(sl=True, long=True)
        oneFileCheck = pm.checkBoxGrp(self.oneFileCheck, q=True, v1=True)
        fullPath = self.getExportPath(oneFileCheck)
        if not fullPath:
            om.MGlobal.displayInfo("Canceled.")
        else:
            if oneFileCheck:
                selection = ""
                for i in sel:
                    selection += " -root " + i
                exportOpt = self.createJstring(fullPath[0], selection)
                pm.AbcExport(j=exportOpt)
            else:
                for i in sel:
                    selection = " -root " + i
                    newPath = fullPath[0] + "/" + i + ".abc"
                    exportOpt = self.createJstring(newPath, selection)
                    pm.AbcExport(j=exportOpt)


    def getExportPath(self, oneFileCheck):
        if oneFileCheck:
            abcPath = pm.fileDialog2(fm=0, ff='Alembic (*.abc);; All Files (*.*)')
        else:
            abcPath = pm.fileDialog2(fm=2, ds=1)
        return abcPath


    def createJstring(self, fullPath, selection):
        startFrame = pm.intFieldGrp(self.frameRange, q=True, v1=True)
        endFrame = pm.intFieldGrp(self.frameRange, q=True, v2=True)
        abc = " -file %s" % fullPath
        frameRange = "-frameRange %s %s" % (str(startFrame), str(endFrame))
        # ======= options start ==================================
        exportOpt = frameRange
        exportOpt += " -noNormals"
        exportOpt += " -ro"
        exportOpt += " -stripNamespaces"
        exportOpt += " -uvWrite"
        exportOpt += " -writeColorSets"
        exportOpt += " -writeFaceSets"
        exportOpt += " -wholeFrameGeo"
        exportOpt += " -worldSpace"
        exportOpt += " -writeVisibility"
        exportOpt += " -eulerFilter"
        exportOpt += " -autoSubd"
        exportOpt += " -writeUVSets"
        exportOpt += " -dataFormat ogawa"
        exportOpt += selection
        exportOpt += abc
        # ======= options end ====================================
        return exportOpt


