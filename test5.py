import maya.standalone
import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import re
import os
import json
from math import *


# Export to json file and shading networks. And assign to them.
class Abc:
    def __init__(self):
        min = pm.playbackOptions(q=True, min=True)
        max = pm.playbackOptions(q=True, max=True)
        self.setupUI(min, max)


    # UI.
    def setupUI(self, min, max):
        winStr = 'exportABC_withShader'
        ttl = 'Export to Alembic with Shader'
        if pm.window(winStr, exists=True):
            pm.deleteUI(winStr)
        else:
            win = pm.window(winStr, t=ttl, s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=380)
            pm.separator(h=10)
            btnStr = 'Create JSON and export shadingEngines'
            pm.button(l=btnStr, c=lambda x: self.jsonButton())
            rStr = 'Range : '
            self.frameRange = pm.intFieldGrp(l=rStr, nf=2, v1=min, v2=max)
            oStr = 'One File : '
            self.oneFileCheck = pm.checkBoxGrp(l=oStr, ncb=1, v1=True)
            pm.button(l='Export ABC', c=lambda x: self.exportButton())
            pm.button(l='Import ABC', c=lambda x: self.importButton())
            btnStr = 'Assign shaders to objects'
            pm.button(l=btnStr, c=lambda x: self.assignButton())
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
            ffStr = 'json (*.json);; All Files (*.*)'
            jsonPath = pm.fileDialog2(fm=0, ff=ffStr)
            if not jsonPath:
                om.MGlobal.displayInfo('Canceled.')
            else:
                jsonPath = ''.join(jsonPath)
                self.writeJson(shdEngList, jsonPath)
                self.exportShader(shdEngList, jsonPath)


    # If there is a "|" in the object name, 
    # It is considered a duplicate name.
    def checkSameName(self, nameList):
        sameName = [i for i in nameList if "|" in i]
        return sameName


    # If the object is connected to the shading engine,
    # It is returned as a dictionary.
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
        ffStr = 'Alembic (*.abc);; All Files (*.*)'
        if oneFileCheck:
            abcPath = pm.fileDialog2(fm=0, ff=ffStr)
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
        ffStr = 'Alembic (*.abc);; All Files (*.*)'
        importDir = pm.fileDialog2(fm=1, ff=ffStr)
        if importDir:
            pm.AbcImport(importDir, m='import')
        else:
            om.MGlobal.displayInfo("Canceled.")


    # This function works when the Assign button is pressed.
    # "_shader.ma" is loaded as a reference and associated with objects.
    def assignButton(self):
        sel = pm.ls(sl=True, dag=True, s=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            ffStr = 'json (*.json);; All Files (*.*)'
            jsonPath = pm.fileDialog2(fm=1, ff=ffStr)
            shaderPath = self.getShaderPath(jsonPath)
            if not jsonPath:
                om.MGlobal.displayInfo("Canceled.")
            elif not shaderPath:
                om.MGlobal.displayError('There are no "_shader.ma" files.')
            else:
                self.makeReference(shaderPath)
                jsonDic = self.readJson(jsonPath)
                failLst = self.assignShd(sel, jsonDic)
                if failLst:
                    msg = "Some objects failed to connect."
                else:
                    msg =  "Completed successfully."
                om.MGlobal.displayInfo(msg)


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
            pm.loadReference(shaderPath, op='v=0')
        else:
            # This is a new reference.
            pm.createReference(shaderPath, 
                r=True, # r=reference
                typ='mayaAscii', 
                iv=True, # iv=ignoreVersion
                gl=True, # gl=groupLocator
                mnc=True, # mnc=mergeNamespacesOnClash
                op='v=0', # op=option
                ns=':' # ns=nameSpace
            )


    # Read shading information from Json file.
    def readJson(self, jsonPath):
        try:
            with open(jsonPath[0], 'r') as JSON:
                jsonDic = json.load(JSON)
            return jsonDic
        except:
            return False


    # There should be a "_shader.ma" file in the json's same folder.
    def getShaderPath(self, jsonPath):
        try:
            (dir, ext) = os.path.splitext(jsonPath[0])
            shaderPath = dir + "_shader.ma"
            checkFile = os.path.isfile(shaderPath)
            return shaderPath if checkFile else False
        except:
            return False


# Delete the node named 'vaccine_gene' and "breed_gene" in the ma file.
# It is related to mayaScanner distributed by autodesk.
class Vaccine:
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        winStr = 'Delete_vaccine'
        ttl = 'Clean Malware called vaccine'
        if pm.window(winStr, exists=True):
            pm.deleteUI(winStr)
        else:
            win = pm.window(winStr, t=ttl, s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rs=2, columnWidth=200)
            # pm.separator(h=10)
            # pm.text("--- Select a File or Folder ---", h=23)
            pm.separator(h=10)
            pm.button(l='File', c=lambda x: self.deleteMain(one=True))
            btnStr = 'Clean All Files in Folder'
            pm.button(l=btnStr, c=lambda x: self.deleteMain(one=False))
            pm.separator(h=10)
            pm.showWindow(win)


    # Delete below strings in ASCII file.
    def deleteVaccineString(self, fullPath):
        vcc = "vaccine_gene"
        brd = "breed_gene"
        crt = "createNode"
        with open(fullPath, "r") as txt:
            lines = txt.readlines()
        # List up the line numbers containing 'vaccine_gene'
        vccList = [j for j, k in enumerate(lines) if vcc in k and crt in k]
        # List up the line numbers containing 'breed_gene'
        brdList = [j for j, k in enumerate(lines) if brd in k and crt in k]
        # List up the line numbers containing 'createNode'
        crtList = [j for j, k in enumerate(lines) if crt in k]
        sum = vccList + brdList # ex) [16, 21, 84, 105]
        deleteList = []
        # List lines to delete consecutively
        for min in sum:
            max = crtList[crtList.index(min) + 1]
            deleteList += [i for i in range(min, max)]
        new, ext = os.path.splitext(fullPath)
        new += "_cleaned" + ext
        # Delete the 'vaccine_gene' or 'breed_gene' paragraph in .ma
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
        # Folder with that files.
        dir = pm.internalVar(uad=True) + "scripts/"
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
        fileType = 'Infected Files (*.ma);; All Files (*.*)'
        if one:
            sel = pm.fileDialog2(fm=0, ff=fileType)
        else:
            sel = pm.fileDialog2(fm=2, ds=1)
        if sel:
            selStr = ''.join(sel)
            ext = os.path.splitext(selStr)[-1]
            if ext:
                result = sel if ext == ".ma" else []
            else:
                dir = os.listdir(selStr)
                result = []
                for i in dir:
                    chk = os.path.splitext(i)[-1]
                    if chk == ".ma":
                        result.append(f'{selStr}/{i}')
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


# Create a through curve or joint.
class ThroughCurve:
    def __init__(self):
        self.setupUI()


    # UI.
    def setupUI(self):
        id = "Penetrating_Curve"
        tt = "Creates curves or joints through the edge loop"
        if pm.window(id, exists=True):
            pm.deleteUI(id)
        else:
            win = pm.window(id, t=tt, s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=180)
            pm.separator(h=8)
            self.chk = pm.radioButtonGrp(la2=['Curve', 'Joint'], nrb=2, sl=1)
            pm.separator(h=8)
            pm.button(l='Create', c=lambda x: self.main())
            pm.separator(h=8)
            pm.showWindow(win)


    # Get the edge number.
    def getEdgeNumber(self, edg: str) -> int:
        '''polygon.e[123] -> 123'''
        result = []
        for i in edg:
            num = re.search(r"\[([0-9]+)\]", i.name())
            num = num.group(1)
            num = int(num)
            result.append(num)
        return result


    # Get the smallest number in the list.
    def getSmallNumber(self, obj: str, num: int) -> int:
        '''When getting the edge loop information, 
        it is necessary to match the starting number.'''
        # el: edgeLoop, ns: noSelection
        edgeLoop = pm.polySelect(obj, el=num, ns=True)
        # Ignore the first number because it is the selected edge number.
        edgeLoop = sorted(edgeLoop[1:])
        result = edgeLoop[0] if edgeLoop else num
        return result


    # Get the coordinates of the cluster.
    def getCoordinates(self, obj: str, edges: list) -> list:
        '''Create a cluster for every edge loop 
        and get the coordinates of its center.'''
        points = []
        for i in edges:
            pm.polySelect(obj, el=i)
            clt = pm.cluster()
            cltHandle = clt[0].name() + 'HandleShape.origin'
            pos = pm.getAttr(cltHandle)
            points.append(pos)
            # After getting the coordinates, the cluster is deleted.
            pm.delete(clt)
        return points


    # Creates curves or joints.
    def create(self, point: list, check: int) -> None:
        '''check: 1=curve, 2=joint'''
        if check == 2:
            for i in point:
                pm.joint(p=i)
        else:
            pm.curve(p=point)


    def main(self) -> None:
        '''Variables
        1. edg: Edge is selected.
        2. obj: Object name is returned even when edge is selected.
        3. num: Get only numbers from string.
        4. min: Get the smallest number in the list.
        5. edges: All edge numbers between start and end.
        6. check: Curve or Joint.
        7. point: Center pivots of every edge loop.
        '''
        edg = pm.ls(os=True, fl=True)
        obj = pm.ls(sl=True, o=True)
        if not obj:
            print("Nothing selected.")
        else:
            num = self.getEdgeNumber(edg)
            min = {self.getSmallNumber(obj, i) for i in num}
            min = list(min)
            min.sort()
            edges = pm.polySelect(obj, erp=(min[0], min[-1]))
            check = pm.radioButtonGrp(self.chk, q=True, sl=True)
            if edges == None:
                msg = 'The "starting edges" should be a loop.'
                print(msg)
            else:
                point = self.getCoordinates(obj, edges)
                self.create(point, check)


# Get a human dummy to determine size.
class Human:
    def __init__(self):
        '''When to start modeling in Maya, 
        Load a human character into the scene 
        to compare the size of the modeling to be made.
        1. human()
        2. human().remove()
        '''
        # src is the path for human modeling.
        src = "T:/AssetTeam/Share/WorkSource/human/human176.obj"
        assert os.path.isfile(src)
        self.src = src
        self.main()


    # Maya default settings when fetching references.
    def createReference(self) -> None:
        fileName = os.path.basename(self.src)
        name, ext = os.path.splitext(fileName)
        pm.createReference(
            self.src, # full path
            gl=True, # groupLocator
            shd="shadingNetworks", # sharedNodes
            mnc=False, # mergeNamespacesOnClash
            ns=name # namespace
        )


    # Remove human character
    def remove(self) -> None:
        pm.FileReference(self.src).remove()


    # Check the reference with the same path as "src" in the scene.
    def main(self) -> None:
        ref = pm.ls(rn = True, type=["transform"])
        tmp = [i for i in ref if self.src == pm.referenceQuery(i, f=True)]
        # If the same file does not exist, the human character is loaded.
        if not tmp:
            self.createReference()



def standalone_template():
    # Start in batch mode
    maya.standalone.initialize(name='python')
 
    cmds.file("C:/Users/hjk03/Desktop/a.ma", f=True, o=True)
    print(cmds.ls(dag=True, s=True))
 
    # Do your magic here
 
    # Save it
    # cmds.file(s=True, f=True)


def createChannels():
    sel = pm.ls(sl=True)
    channelList = [
        "Toe", 
        "Bank", 
        "Twist", 
        "Heel", 
        "Ball", 
        "Down", 
        ]
    # channelList = [
    #     "FKIK_L_F", 
    #     "FKIK_R_F", 
    #     "FKIK_L_B", 
    #     "FKIK_R_B", 
    #     ]
    for i in sel:
        for cName in channelList:
            pm.addAttr(i, ln=cName, at='double', dv=0)
            pm.setAttr(f'{i}.{cName}', e=True, k=True)


def connectBlendColors():
    sel = pm.ls(sl=True)
    tmp = int(len(sel) / 3)
    IK = [sel[i] for i in range(tmp)]
    FK = [sel[i] for i in range(tmp, (tmp*2))]
    FBX = [sel[i] for i in range((tmp*2), (tmp*3))]
    SWITCH = "cc_global.FKIK_Tail"
    setR = pm.shadingNode("setRange", au=True)
    pm.connectAttr(SWITCH, f"{setR}.valueX", f=True)
    for i in range(tmp):
        createBlendColors(SWITCH, setR, IK[i], FK[i], FBX[i])


def createBlendColors(SWITCH, setR, IK, FK, FBX):
    bls = pm.shadingNode("blendColors", au=True)
    pm.connectAttr(f"{FK}.rotate", f"{bls}.color1", f=True)
    pm.connectAttr(f"{IK}.rotate", f"{bls}.color2", f=True)
    pm.connectAttr(f"{bls}.output", f"{FBX}.rotate", f=True)
    pm.setAttr(f"{setR}.oldMaxX", 10)
    pm.setAttr(f"{setR}.maxX", 1)
    pm.connectAttr(f"{setR}.outValueX", f"{bls}.blender", f=True)


def getDistance(sp: list, ep: list):
    x1, y1, z1 = sp
    x2, y2, z2 = ep
    result = sqrt(pow(x1-x2, 2) + pow(y1-y2, 2) + pow(z1-z2, 2))
    result = round(result, 3)
    return result


# Point position to create a controller
def pointPosition():
    sel = pm.ls(sl=True, fl=True)
    pos = [pm.pointPosition(i) for i in sel]
    point = [tuple([round(j, 3) for j in i]) for i in pos]
    print(point)
    return point


def createBones():
    sel = pm.ls(sl=True)
    for i in sel:
        pm.select(d=True)
        jnt = pm.joint(p=(0,0,0), rad=3)
        pm.matchTransform(jnt, i, pos=True)


def parentBone():
    sel = pm.ls(sl=True)
    for j, k in enumerate(sel):
        if (j + 1) < len(sel):
            pm.parent(sel[j+1], k)
        else:
            continue


