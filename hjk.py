# import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.core as pm
import json
import os
import codecs


# Export to json file and shading networks. And assign to them.
class abc():
    def __init__(self):
        min = pm.playbackOptions(q=True, min=True)
        max = pm.playbackOptions(q=True, max=True)
        self.setupUI(min, max)


    # UI.
    def setupUI(self, min, max):
        if pm.window('exportABC_withShader', exists=True):
            pm.deleteUI('exportABC_withShader')
        else:
            win = pm.window('exportABC_withShader', t='Export to Alembic with Shader', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=380)
            pm.separator(h=10)
            pm.button(l='Create JSON and export shadingEngines', c=lambda x: self.jsonButton())
            self.frameRange = pm.intFieldGrp(l='Range : ', nf=2, v1=min, v2=max)
            self.oneFileCheck = pm.checkBoxGrp(l='One File : ', ncb=1, v1=True)
            pm.button(l='Export ABC', c=lambda x: self.exportButton())
            pm.button(l='Import ABC', c=lambda x: self.importButton())
            pm.button(l='Assign shaders to objects', c=lambda x: self.assignButton())
            pm.separator(h=10)
            pm.showWindow(win)


    # This function works when the json button is pressed.
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
                self.writeJson(shdEngList, jsonPath)
                self.exportShader(shdEngList, jsonPath)


    # If there is a "|" in the object name, it is considered a duplicate name.
    def checkSameName(self, nameList):
        sameName = [i for i in nameList if "|" in i]
        return sameName


    # If the object is connected to the shading engine, it is returned as a dictionary.
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


    # Create a json file.
    def writeJson(self, dic, jsonPath):
        with open(jsonPath, 'w') as JSON:
            json.dump(dic, JSON, indent=4)


    # Export the shading network and save it as a .ma file.
    def exportShader(self, dic, fullPath):
        (dir, ext) = os.path.splitext(fullPath)
        exportPath = "%s_shader" % dir
        shdEngList = list(set(dic.values()))
        pm.select(cl=True)
        pm.select(shdEngList, ne=True)
        pm.exportSelected(exportPath, type="mayaAscii", f=True)


    # This function works when the Export button is pressed.
    def exportButton(self):
        sel = pm.ls(sl=True, long=True)
        # multiple abc files or one abc file. If True then one file.
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


    # Select a folder or specify a file name.
    def getExportPath(self, oneFileCheck):
        if oneFileCheck:
            abcPath = pm.fileDialog2(fm=0, ff='Alembic (*.abc);; All Files (*.*)')
        else:
            abcPath = pm.fileDialog2(fm=2, ds=1)
        return abcPath


    # Jstring is required to export.
    def createJstring(self, fullPath, selection):
        startFrame = pm.intFieldGrp(self.frameRange, q=True, v1=True)
        endFrame = pm.intFieldGrp(self.frameRange, q=True, v2=True)
        abc = " -file %s" % fullPath
        frameRange = "-frameRange %s %s" % (str(startFrame), str(endFrame))
        # ======= options start ==================================
        exportOpt = frameRange
        # exportOpt += " -noNormals"
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


    # This function works when the Import button is pressed. 
    def importButton(self):
        importDir = pm.fileDialog2(fm=1, ff='Alembic (*.abc);; All Files (*.*)')
        if importDir:
            pm.AbcImport(importDir, m='import')
        else:
            om.MGlobal.displayInfo("Canceled.")


    # This function works when the Assign button is pressed.
    # "_shader.ma" is loaded as a reference and associated with the selected object.
    def assignButton(self):
        sel = pm.ls(sl=True, dag=True, s=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            jsonPath = pm.fileDialog2(fm=1, ff='json (*.json);; All Files (*.*)')
            shaderPath = self.getShaderPath(jsonPath)
            if not jsonPath:
                om.MGlobal.displayInfo("Canceled.")
            elif not shaderPath:
                om.MGlobal.displayError('There are no "_shader.ma" files.')
            else:
                self.makeReference(shaderPath)
                jsonDic = self.readJson(jsonPath)
                failLst = self.assignShd(sel, jsonDic)
                message = "Some objects failed to connect." if failLst else "Completed successfully."
                om.MGlobal.displayInfo(message)


    # Attempts to assign, and returns a list that fails.
    def assignShd(self, sel, jsonDic):
        assignFailed = []
        for i in sel:
            objName = i.getParent().name()
            sepName = objName.split(":")[-1] if ":" in objName else objName
            if sepName in jsonDic:
                try:
                    pm.sets(jsonDic[sepName], fe=objName)
                except:
                    assignFailed.append(objName)
            else:
                continue
        return assignFailed


    # Load Reference "_shader.ma" file.
    def makeReference(self, shaderPath):
        try:
            # If a reference aleady exists, get reference's node name.
            referenceName = pm.referenceQuery(shaderPath, referenceNode=True)
        except:
            referenceName = False
        if referenceName:
            # This is a replacement reference.
            # cmds.file(shaderPath, lr=referenceName, op='v=0')   # lr=loadReference
            pm.loadReference(shaderPath, op='v=0')
        else:
            # This is a new reference.
            # r=reference, iv=ignoreVersion, gl=groupLocator, mnc=mergeNamespacesOnClash, op=option, v=verbose, ns=nameSpace
            # cmds.file(shaderPath, r=True, typ='mayaAscii', iv=True, gl=True, mnc=True, op='v=0', ns=':')
            pm.createReference(shaderPath, r=True, typ='mayaAscii', iv=True, gl=True, mnc=True, op='v=0', ns=':')


    # Read shading information from Json file.
    def readJson(self, jsonPath):
        try:
            with open(jsonPath[0], 'r') as JSON:
                jsonDic = json.load(JSON)
            return jsonDic
        except:
            return False


    # There should be a "_shader.ma" file in the same folder as the json file.
    def getShaderPath(self, jsonPath):
        try:
            (dir, ext) = os.path.splitext(jsonPath[0])
            shaderPath = dir + "_shader.ma"
            checkFile = os.path.isfile(shaderPath)
            return shaderPath if checkFile else False
        except:
            return False


# Got this code from the internet.
# Modified to class.
class softSel():
    def __init__(self):
        self.createSoftCluster()
    
    
    def softSelection(self):
        selection = om.MSelectionList()
        softSelection = om.MRichSelection()
        om.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)
        dagPath = om.MDagPath()
        component = om.MObject()
        iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        elements = []
        while not iter.isDone(): 
            iter.getDagPath(dagPath, component)
            dagPath.pop()
            node = dagPath.fullPathName()
            fnComp = om.MFnSingleIndexedComponent(component)   
            for i in range(fnComp.elementCount()):
                elements.append([node, fnComp.element(i), fnComp.weight(i).influence()])
            iter.next()
        return elements
        
    
    def createSoftCluster(self):
        softElementData = self.softSelection()
        selection = ["%s.vtx[%d]" % (el[0], el[1]) for el in softElementData] 
        pm.select(selection, r=True)
        cluster = pm.cluster(relative=True)
        for i in range(len(softElementData)):
            pm.percent(cluster[0], selection[i], v=softElementData[i][2])
        pm.select(cluster[1], r=True)


class rename():
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('Re_name', exists=True):
            pm.deleteUI('Re_name')
        else:
            win = pm.window('Re_name', t='rename', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=391)
            pm.separator(h=10)
            self.new = pm.textFieldGrp(l="New name : ", ed=True)
            self.chk = pm.checkBoxGrp(l='Replace : ', ncb=1, v1=False, cc=lambda x: self.updateUI())
            self.rep = pm.textFieldGrp(l="Replace to this : ", ed=True, en=False)
            self.end = pm.textFieldGrp(l="End : ", ed=True, tcc=lambda x: self.updateUI())
            self.btn = pm.button(l='New', c=lambda x: self.reName())
            pm.separator(h=10)
            pm.showWindow(win)
    

    def updateUI(self):
        chk = self.chk.getValue1()
        end = '' if chk else self.end.getText()
        newlbl = "Find : " if chk else "New name : "
        btnlbl = "Rename" if chk else "New"
        self.end.setText(end)
        self.new.setLabel(newlbl)
        self.btn.setLabel(btnlbl)
        self.new.setEnable(not end)
        self.rep.setEnable(chk)
        self.end.setEnable(not chk)


    # The number is last one in name.
    # This function is Only works for strings sliced with underscores.
    # Return index and its number.
    def getNumberInName(self, name): # input example : 'pCube1_22_obj_22_a2'
        nameSlice = name.split("_") # ['pCube1', '22', 'obj', '22', 'a2']
        digitList = [(j, k) for j, k in enumerate(nameSlice) if k.isdigit()] # [(1, '22'), (3, '22')]
        try:
            idx, num = digitList[-1]
            return idx, int(num)
        except:
            return False


    def reName(self):
        sel = pm.ls(sl=True)
        chk = self.chk.getValue1()
        new = self.new.getText()
        if chk:
            rep = self.rep.getText()
            for i in sel:
                pm.rename(i, i.replace(new, rep))
        else:
            end = self.end.getText()
            for i in sel:
                pm.rename(i, i + end if end else new)


# Delete the node named 'vaccine_gene' and "breed_gene" in the <.ma> file.
# It is related to mayaScanner distributed by autodesk.
class vaccine():
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('Delete_vaccine', exists=True):
            pm.deleteUI('Delete_vaccine')
        else:
            win = pm.window('Delete_vaccine', t='Clean Malware called vaccine', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rs=2, columnWidth=200)
            # pm.separator(h=10)
            # pm.text("--- Select a File or Folder ---", h=23)
            pm.separator(h=10)
            pm.button(l='File', c=lambda x: self.deleteMain(one=True))
            pm.button(l='Clean All Files in Folder', c=lambda x: self.deleteMain(one=False))
            pm.separator(h=10)
            pm.showWindow(win)


    # Delete below strings in ASCII file.
    def deleteVaccineString(self, fullPath):
        vcc = "vaccine_gene"
        brd = "breed_gene"
        crt = "createNode"
        with open(fullPath, "r") as txt:
            lines = txt.readlines()
        vccList = [j for j, k in enumerate(lines) if vcc in k and crt in k] # List up the line numbers containing 'vaccine_gene'
        brdList = [j for j, k in enumerate(lines) if brd in k and crt in k] # List up the line numbers containing 'breed_gene'
        crtList = [j for j, k in enumerate(lines) if crt in k] # List up the line numbers containing 'createNode'
        sum = vccList + brdList # ex) [16, 21, 84, 105]
        deleteList = []
        # List lines to delete consecutively
        for min in sum:
            max = crtList[crtList.index(min) + 1]
            deleteList += [i for i in range(min, max)]
        new, ext = os.path.splitext(fullPath)
        new += "_cleaned" + ext
        # When creating a new file, delete the 'vaccine_gene' or 'breed_gene' paragraph.
        # Write '//Deleted here' instead of the deleted line.
        with open(new, "w") as txt:
            for j, k in enumerate(lines):
                if j in deleteList:
                    txt.write("// Deleted here.\n")
                else:
                    txt.write(k)
        return new


    # Delete the files : "vaccine.py", "vaccine.pyc", "userSetup.py"
    def deleteVaccineFiles(self):
        dir = pm.internalVar(uad=True) + "scripts/" # Folder with that files.
        fileList = ["vaccine.py", "vaccine.pyc", "userSetup.py"]
        for i in fileList:
            try:
                os.remove(dir + i)
            except:
                pass


    # Checking First, if the file is infected or not.
    def checkVaccineString(self, fullPath):        
        with open(fullPath, "r") as txt:
            lines = txt.readlines()
        for i in lines:
            if "vaccine_gene" in i or "breed_gene" in i:
                result = fullPath
                break
            else:
                result = False
        return result


    # retrun <.ma> file list.
    def getMaFile(self, one):
        fileTypes = 'Infected Files (*.ma);; All Files (*.*)'
        selection = pm.fileDialog2(fm=0, ff=fileTypes) if one else pm.fileDialog2(fm=2, ds=1)
        if selection:
            ext = os.path.splitext(selection[0])[-1]
            if ext:
                result = selection if ext == ".ma" else []
            else:
                dir = os.listdir(selection[0])
                result = [selection[0] + "/" + i for i in dir if os.path.splitext(i)[-1] == ".ma"]
        else:
            result = []
        return result


    # This is the main function.
    def deleteMain(self, one):
        maFileList = self.getMaFile(one)
        infectedFile = [i for i in maFileList if self.checkVaccineString(i)]
        if infectedFile:
            for j, k in enumerate(infectedFile):
                result = self.deleteVaccineString(k)
                om.MGlobal.displayInfo(f"{j} : {result}")
            self.deleteVaccineFiles()
        else:
            om.MGlobal.displayInfo("No infected files were found.")


# Transform HanGeul unicode to bytes. Otherside too.
class han():
    def __init__(self):
        self.btnHan1 = b'\xec\x9d\xb8\xec\xbd\x94\xeb\x94\xa9'
        self.btnHan2 = b'\xec\xa7\x80\xec\x9a\xb0\xea\xb8\xb0'
        self.HanGeul = b'\xed\x95\x9c\xea\xb8\x80'
        self.setupUI()


    # UI.
    def setupUI(self):
        if pm.window('HanGeul', exists=True):
            pm.deleteUI('HanGeul')
        else:
            win = pm.window('HanGeul', t='Encode / Decode', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=240)
            pm.separator(h=10)
            self.hanField = pm.textField(ed=True, pht=self.HanGeul)
            self.utfField = pm.textField(ed=True, pht="Bytes")
            self.btn = pm.button(l=self.btnHan1, c=lambda x: self.transform())
            pm.separator(h=10)
            pm.showWindow(win)


    # The field value is returned as a string type.
    def transform(self):
        A = self.hanField.getText()
        B = self.utfField.getText()
        if A and not B:
            result = r"%s" % (str(A).encode("utf-8"))
            self.utfField.setText(result)
            self.btn.setLabel(self.btnHan2)
        elif B and not A:
            result = eval(B)
            self.hanField.setText(result.decode("utf-8", "strict"))
            self.btn.setLabel(self.btnHan2)
        else:
            self.hanField.setText("")
            self.utfField.setText("")
            self.btn.setLabel(self.btnHan1)


# Class end. ====================================================================================================================


# Grouping itself and named own
def grp(cp=False):
    sel = pm.ls(sl=True)
    grpList = []
    for i in sel:
        grp = pm.group(i, n="%s_grp" % i)
        if not cp:
            pm.move(0, 0, 0, grp + ".scalePivot", grp + ".rotatePivot", rpr=True)
        grpList.append(grp)
    return grpList


# Create three types of locators.
# When you select two objects, a locator is created at the midpoint.
def loc():
    sel = pm.ls(sl=True)
    num = len(sel)
    if num == 1: # Select One point.
        position = pm.xform(sel[0], q=True, t=True, ws=True)
        position = tuple(position)
    elif num == 2: # Select Two points.
        twoPoint = [pm.xform(i, q=True, t=True, ws=True) for i in sel]
        position = tuple((twoPoint[0][i] + twoPoint[1][i]) / 2 for i in range(3))
    else:
        position = (0, 0, 0)
    loc = pm.spaceLocator(p=position)
    pm.xform(loc, t=position, ws=True)
    return position


# Create a curve controller.
def ctrl(**kwargs):
    ctrl = {
    "cub": [
        (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), 
        (-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), 
        (1, 1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1)], 
    "sph": [
        (0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), (0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), 
        (0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), (-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), 
        (0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), 
        (-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), (0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), (0, 1, 0)], 
    "cyl": [
        (-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), (0.7, 1, -0.7), 
        (0, 1, -1), (0, 1, 1), (0, -1, 1), (-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), 
        (0, -1, -1), (0.7, -1, -0.7), (1, -1, 0), (0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), 
        (0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)], 
    "pip": [
        (0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), (1, -1, 0), (1, 1, 0), (0.7, 1, -0.7), 
        (0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), (-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), 
        (0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), (1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), 
        (0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), (-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1)], 
    "con": [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), (0, 2, 0), (0, 0, 1), (-0.87, 0, -0), (0.87, 0, 0), (0, 0, 1)], 
    "ar1": [(0, 0, 2), (2, 0, 1), (1, 0, 1), (1, 0, -2), (-1, 0, -2), (-1, 0, 1), (-2, 0, 1), (0, 0, 2)], 
    "ar2": [
        (0, 1, 4), (4, 1, 2), (2, 1, 2), (2, 1, -4), (-2, 1, -4), (-2, 1, 2), (-4, 1, 2), (0, 1, 4), (0, -1, 4), 
        (4, -1, 2), (2, -1, 2), (2, -1, -4), (-2, -1, -4), (-2, -1, 2), (-4, -1, 2), (0, -1, 4), (4, -1, 2), 
        (4, 1, 2), (2, 1, 2), (2, 1, -4), (2, -1, -4), (-2, -1, -4), (-2, 1, -4), (-2, 1, 2), (-4, 1, 2), (-4, -1, 2)]
    }
    if kwargs:
        coordinate = [ctrl[i] for i in kwargs if kwargs[i]]
        for i in coordinate:
            pm.curve(d=1, p=i)
    else:
        shapes = list(ctrl.keys())
        om.MGlobal.displayInfo(f"Shape list : {shapes}")
        om.MGlobal.displayInfo(f"How to use : ctrl(cub=True, sph=True, ...)")


# This function works even if you select a point.
def cuvPath(startFrame, endFrame):
    sel = pm.ls(sl=True, fl=True)
    for j in sel:
        pointList = []
        for k in range(startFrame, endFrame + 1):
            pm.currentTime(k)
            try:
                pointList.append(pm.pointPosition(j)) # vtx position
            except:
                pointList.append(pm.xform(j, q=True, ws=True, rp=True)) # obj position
        pm.curve(p=pointList)


# Creates a curve along the locator's points.
# Place locators first, and select them, and call this function.
def cuvLoc(cl=False): # cl = closed
    sel = pm.ls(sl=True) # select locators
    locatorPosition = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
    if cl:
        # if closed : first, creates a circle, and change its shape.
        cuvName = pm.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ch=False, s=len(sel))[0]
        for j, k in enumerate(locatorPosition):
            pm.move(k[0], k[1], k[2], '%s.cv[%d]' % (cuvName, j), ws=True)
    else:
        print("# ex : cuvLoc(cl=True)")
        cuvName = pm.curve(p=locatorPosition)


# Attempt to delete unused plugins.
def delPlugin():
    unknownList = pm.ls(type="unknown")
    pm.delete(unknownList) # Just delete Unknown type list.
    pluginList = pm.unknownPlugin(q=True, l=True)
    if pluginList:
        for j, k in enumerate(pluginList):
            pm.unknownPlugin(k, r=True)
            print("%d : %s" % (j, k)) # Print deleted plugin's names and number
        print('Delete completed.')
    else:
        om.MGlobal.displayWarning("There are no unknown plugins.")


# Offset the Keys
def keyOff(i=1): # i : interval
    sel = pm.ls(sl=True, fl=True)
    for j, k in enumerate(sel):
        pm.keyframe(k, e=True, r=True, tc = j * i)


# Create an empty group and match the pivot with the selector.
def grpEmpty():
    sel = pm.ls(sl=True)
    for i in sel:
        grp = pm.group(em=True, n=i + "_offset")
        pm.matchTransform(grp, i, pos=True, rot=True)
        try:
            iParent = "".join(pm.listRelatives(i, p=True)) # Selector's mom group.
            pm.parent(grp, iParent)
        except:
            pass
        pm.parent(i, grp)


# Select groups only.
def selGrp():
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    grp = []
    for i in sel:
        A = pm.listRelatives(i, s=True)
        B = pm.ls(i, type='joint')
        C = pm.ls(i, type='parentConstraint')
        if not (A or B or C):
            grp.append(i)
        else:
            continue
    pm.select(grp)
    return grp


# Select mesh only.
def selObj():
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    obj = []
    for i in sel:
        A = pm.listRelatives(i, s=True)
        B = pm.ls(i, type='joint')
        C = pm.ls(i, type='parentConstraint')
        if not (not A or B or C):
            obj.append(i)
        else:
            continue
    pm.select(obj)
    return obj


# Select objects with duplicate names.
def sameName():
    sel = pm.ls(tr=True)
    dup = [i for i in sel if "|" in i]
    if dup:
        pm.select(dup)
        om.MGlobal.displayError("Same name selected in outliner.")
    else:
        om.MGlobal.displayInfo("No duplicated names.")


# Return scene's infomations.
# Parameter : dir, sceneName, name, ext, dir, typ, ver
# How to use : info(fullPath, ver=True, dir=True, ...)
def info(fullPath="", **kwargs):
    if not kwargs:
        om.MGlobal.displayInfo("How to use : info(fullPath, dir=True, ver=True...")
        om.MGlobal.displayInfo("Parameters : dir, sceneName, name, ext, dir, typ, ver")
    elif not fullPath:
        om.MGlobal.displayError("The fullPath parameter is missing.")
    else:
        # values
        dir = os.path.dirname(fullPath)
        sceneName = os.path.basename(fullPath)
        name, ext = os.path.splitext(sceneName)
        wip = dir.split("/")[-2]
        typ = dir.split("/")[-3]
        ver = name.split("_")[-1]
        # keys
        result = {
            # 'fullPath': fullPath, 
            'dir': dir, 
            'sceneName': sceneName, 
            'name': name, 
            'ext': ext, 
            'wip': wip, 
            'typ': typ, 
            'ver': ver
        }
        # return
        return (result[i] for i in kwargs if kwargs[i])

