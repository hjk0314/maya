import re
import os
import json
import subprocess
import maya.OpenMaya as om
import pymel.core as pm
import maya.mel as mel


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


# Got this code from the internet.
# Modified to class.
class SoftSel:
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
                elem = fnComp.element(i)
                infl = fnComp.weight(i).influence()
                elements.append([node, elem, infl])
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


# Transform HanGeul unicode to bytes. Otherside too.
class Han:
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


# Create wheels that rotate automatically
class AutoWheel:
    def __init__(self):
        self.main()
    

    def main(self):
        sel = pm.ls(sl=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            for i in sel:
                rad = self.createRad(i)
                var = self.createVar(rad)
                self.createRig(i, var, rad)
    

    # Return obj's radius.
    def createRad(self, obj: str) -> float:
        # bb: bounding box
        bbObj = pm.xform(obj, q=True, bb=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bbObj
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        bbList = [x, y, z]
        bbList.sort(reverse=True) # biggest
        bb = bbList[0] # 0.12345678
        result = round(bb, 3) # 0.123
        return result


    # Create variables.
    def createVar(self, rad: float) -> tuple:
        rad *= 1.1
        cuv = pm.circle(nr=(1,0,0), r=rad, ch=False, n='cc_Ft_wheel_mid_R_3')
        cuv = cuv[0]
        jnt = cuv + '_jnt'
        null = cuv + '_null_grp'
        prev = cuv + '_prev_grp'
        orient = cuv + '_orient_Grp'
        br = '\n'
        # expression1 ==================================================
        expr1 = f'float $R = {cuv}.Radius;{br}'
        expr1 += f'float $A = {cuv}.AutoRoll;{br}'
        expr1 += f'float $J = {jnt}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}' # 2*pi*r
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = 1;{br}' # Connect the global scale.
        expr1 += f'float $pX = {cuv}.PrevPosX;{br}'
        expr1 += f'float $pY = {cuv}.PrevPosY;{br}'
        expr1 += f'float $pZ = {cuv}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {cuv}.translateX;{br}'
        expr1 += f'float $nY = {cuv}.translateY;{br}'
        expr1 += f'float $nZ = {cuv}.translateZ;{br*2}'
        # expression2: Distance between two points.
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{jnt}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Auto roll switch.
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += f' / $S;{br*2}' # Resizing the global scale.
        # expression4
        expr4 = f'{cuv}.PrevPosX = $nX;{br}'
        expr4 += f'{cuv}.PrevPosY = $nY;{br}'
        expr4 += f'{cuv}.PrevPosZ = $nZ;{br}'
        # expression Final =============================================
        exprFinal = expr1 + expr2 + expr3 + expr4
        # Result
        result = (cuv, jnt, null, prev, orient, exprFinal)
        return result


    # Construct a rig inside maya.
    def createRig(self, obj: str, var: tuple, rad: float) -> None:
        # variables
        cuv, jnt, null, prev, orient, expr = var
        # channel to cuv
        pm.addAttr(cuv, ln='Radius', at='double', dv=1)
        pm.setAttr(f'{cuv}.Radius', e=True, k=True)
        pm.setAttr(f'{cuv}.Radius', rad)
        pm.addAttr(cuv, ln='AutoRoll', at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{cuv}.AutoRoll', e=True, k=True)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(cuv, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{cuv}.PrevPos{i}', e=True, k=True)
        # create joint inside cuv
        pm.joint(n=jnt, p=(0,0,0))
        # create groups
        pm.group(n=null, em=True, p=cuv)
        pm.group(n=prev, em=True, w=True)
        pm.group(n=orient, em=True, p=prev)
        grp = pm.group(cuv, prev)
        pm.matchTransform(grp, obj, pos=True)
        # create constraints
        pm.aimConstraint(cuv, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)
        pm.expression(s=expr, o='', ae=1, uc='all')


# Matching the direction of the pivot.
class MatchPivot:
    def __init__(self):
        self.main()


    # Check if selected is a point.
    def check(self, sel: list) -> bool:
        vtxList = [i for i in sel if isinstance(i, pm.MeshVertex)]
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
            result = False
        elif len(sel) != 3 or len(vtxList) != 3:
            om.MGlobal.displayError('Select 3 points.')
            result = False
        else:
            result = True
        return result


    # Decide the direction.
    # Input is a list of 3 points.
    def select3Points(self, sel: list) -> str:
        # shp: shape
        shp = sel[0].split('.')[0]
        # Object's name
        obj = pm.listRelatives(shp, p=True)
        obj = obj[0]
        # pPlane's name
        pPlane = pm.polyPlane(sx=1, sy=1, ax=(0, 1, 0), cuv=2, ch=False)
        pPlane = pPlane[0]
        vtx = pm.ls(f"{pPlane}.vtx[0:2]", fl=True)
        all = vtx + sel
        pm.select(all)
        mel.eval("snap3PointsTo3Points(0);")
        pm.select(cl=True)
        return pPlane

    
    def main(self) -> None:
        sel = pm.ls(sl=True, fl=True)
        chk = self.check(sel)
        if not chk:
            pass
        else:
            obj = self.select3Points(sel)
            loc = pm.spaceLocator()
            pm.matchTransform(loc, obj, pos=True, rot=True)
            pm.delete(obj)


# Create mirror copy of selection with group.
# Example: mirrorCopy(x=True or z=True)
class MirrorCopy:
    def __init__(self, **kwargs):
        self.sel = pm.ls(sl=True)
        self.dir = [i.lower() for i in kwargs if kwargs[i]]
        self.main()


    def mirrorCopy(self, idx):
        for i in self.sel:
            if idx == 'x':
                grp = pm.group(em=True, n=f'{i}_mirrorCopy')
                pm.matchTransform(grp, i, pos=True, rot=True)
                t = pm.getAttr(f'{grp}.translate')
                r = pm.getAttr(f'{grp}.rotate')
                tX = t[0] * -1
                rX = r[0] + (180 if r[0] < 0 else -180)
                rY = r[1] * -1
                rZ = r[2] * -1
                pm.setAttr(f'{grp}.translateX', tX)
                pm.setAttr(f'{grp}.rotateX', rX)
                pm.setAttr(f'{grp}.rotateY', rY)
                pm.setAttr(f'{grp}.rotateZ', rZ)
            elif idx == 'z':
                grp = pm.group(em=True, n=f'{i}_mirrorCopy')
                pm.matchTransform(grp, i, pos=True, rot=True)
                t = pm.getAttr(f'{grp}.translate')
                r = pm.getAttr(f'{grp}.rotate')
                grp = pm.group(em=True, n=f'{i}_mirrorCopy')
                pm.matchTransform(grp, i, pos=True, rot=True)
                t = pm.getAttr(f'{grp}.translate')
                r = pm.getAttr(f'{grp}.rotate')
                tZ = t[2] * -1
                rZ = r[2] + (180 if r[2] < 0 else -180)
                pm.setAttr(f'{grp}.translateZ', tZ)
                pm.setAttr(f'{grp}.rotateZ', rZ)
            else:
                continue


    def main(self):
        if not self.sel:
            om.MGlobal.displayError("Nothing selected.")
        elif not self.dir:
            om.MGlobal.displayError("Direction is required.")
        elif not self.dir:
            om.MGlobal.displayError("X and Z directions are available.")
        elif 'x' in self.dir:
            self.mirrorCopy('x')
        elif 'z' in self.dir:
            self.mirrorCopy('y')
        else:
            om.MGlobal.displayError("Example: mirrorCopy(x=True or z=True)")


# Create a through curve or joint.
class PenetratingCurve:
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
            om.MGlobal.displayError("Nothing selected.")
        else:
            num = self.getEdgeNumber(edg)
            min = {self.getSmallNumber(obj, i) for i in num}
            min = list(min)
            min.sort()
            edges = pm.polySelect(obj, erp=(min[0], min[-1]))
            check = pm.radioButtonGrp(self.chk, q=True, sl=True)
            if edges == None:
                msg = 'The "starting edges" should be a loop.'
                om.MGlobal.displayError(msg)
            else:
                point = self.getCoordinates(obj, edges)
                self.create(point, check)


# Match the curve shape from A to B.
class MatchCurveShape:
    def __init__(self):
        self.main()


    # Number of Object's cv.
    def numberOfCV(self, obj: str) -> int:
        '''Number of object's cv'''
        cv = f'{obj}.cv[0:]'
        pm.select(cv)
        cvSel = pm.ls(sl=True, fl=True)
        cvNum = len(cvSel)
        result = cvNum
        pm.select(cl=True)
        return result

        
    # Match the point to point.
    def matchShape(self, obj: list) -> list:
        '''Change the shape of the curve controller from A to B'''
        A_list = obj[0:-1]
        B = obj[-1] # The last selection is Base.
        numB = self.numberOfCV(B) # number of B.cv
        failed = []
        for A in A_list:
            numA = self.numberOfCV(A)
            if numA == numB > 0:
                for k in range(numA):
                    cvA = f'{A}.cv[{k}]'
                    cvB = f'{B}.cv[{k}]'
                    p1, p2, p3 = pm.pointPosition(cvB)
                    pm.move(p1, p2, p3, cvA, a=True)
            else:
                failed.append(A)
        return failed


    def main(self):
        '''Select only "nurbsCurve" and match the shape.'''
        sel = pm.ls(sl=True, dag=True, type=['nurbsCurve'])
        # Select at least 2.
        if len(sel) < 2:
            om.MGlobal.displayError('Select two or more "nurbsCurves".')
        else:
            result = self.matchShape(sel)
            failed = 'Check this objects : %s' % result
            success = 'Successfully done.'
            message = failed if result else success
            om.MGlobal.displayInfo(message)


# Grouping itself and named own
# cp is centerPivot
def grp(cp=False):
    sel = pm.ls(sl=True)
    for i in sel:
        grp = pm.group(i, n="%s_grp" % i)
        if not cp:
            pm.move(0,0,0, grp+".scalePivot", grp+".rotatePivot", rpr=True)


# Create a curve controller.
def ctrl(**kwargs):
    # Cube shape coordinates
    cub = [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), ]
    cub += [(1, 1, -1), (-1, 1, -1), (-1, -1, -1), ]
    cub += [(-1, -1, 1), (1, -1, 1), (1, -1, -1), ]
    cub += [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), ]
    cub += [(1, 1, 1), (1, -1, 1), (1, -1, -1), ]
    cub += [(1, 1, -1), ]
    # Sphere shape coordinates
    sph = [(0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), ]
    sph += [(0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), ]
    sph += [(0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), ]
    sph += [(-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), ]
    sph += [(0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), ]
    sph += [(0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), ]
    sph += [(-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), ]
    sph += [(0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), ]
    sph += [(0, 1, 0), ]
    # Cylinder shape coordinates
    cyl = [(-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), ]
    cyl += [(0.7, 1, 0.7), (1, 1, 0), (0.7, 1, -0.7), ]
    cyl += [(0, 1, -1), (0, 1, 1), (0, -1, 1), ]
    cyl += [(-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), ]
    cyl += [(0, -1, -1), (0.7, -1, -0.7), (1, -1, 0), ]
    cyl += [(0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), ]
    cyl += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
    cyl += [(1, 1, 0), (1, -1, 0), (-1, -1, 0), ]
    cyl += [(-1, 1, 0), ]
    # Pipe shape coordinates
    pip = [(0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), ]
    pip += [(1, -1, 0), (1, 1, 0), (0.7, 1, -0.7), ]
    pip += [(0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), ]
    pip += [(-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), ]
    pip += [(0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), ]
    pip += [(1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), ]
    pip += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
    pip += [(-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1), ]
    # Cone shape coordinates
    con = [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), ]
    con += [(0, 2, 0), (0, 0, 1), (-0.87, 0, -0), ]
    con += [(0.87, 0, 0), (0, 0, 1), ]
    # Arrow1 shape coordinates
    ar1 = [(0, 0, 2), (2, 0, 1), (1, 0, 1), ]
    ar1 += [(1, 0, -2), (-1, 0, -2), (-1, 0, 1), ]
    ar1 += [(-2, 0, 1), (0, 0, 2), ]
    # Arrow2 shape coordinates
    ar2 = [(0, 1, 4), (4, 1, 2), (2, 1, 2), ]
    ar2 += [(2, 1, -4), (-2, 1, -4), (-2, 1, 2), ]
    ar2 += [(-4, 1, 2), (0, 1, 4), (0, -1, 4), ]
    ar2 += [(4, -1, 2), (2, -1, 2), (2, -1, -4), ]
    ar2 += [(-2, -1, -4), (-2, -1, 2), (-4, -1, 2), ]
    ar2 += [(0, -1, 4), (4, -1, 2), (4, 1, 2), ]
    ar2 += [(2, 1, 2), (2, 1, -4), (2, -1, -4), ]
    ar2 += [(-2, -1, -4), (-2, 1, -4), (-2, 1, 2), ]
    ar2 += [(-4, 1, 2), (-4, -1, 2), ]
    # Arrow3 shape coordinates
    ar3 = [(7, 0, 0), (5, 0, -5), (0, 0, -7), ]
    ar3 += [(-5, 0, -5), (-7, 0, 0), (-5, 0, 5), ]
    ar3 += [(0, 0, 7), (5, 0, 5), (7, 0, 0), ]
    ar3 += [(5, 0, 2), (7, 0, 3), (7, 0, 0), ]
    # Arrow4 shape coordinates
    ar4 = [(0, 0, -11), (-3, 0, -8), (-2.0, 0, -8), ]
    ar4 += [(-2, 0, -6), (-5, 0, -5), (-6, 0, -2), ]
    ar4 += [(-8, 0, -2), (-8, 0, -3), (-11, 0, 0), ]
    ar4 += [(-8, 0, 3), (-8, 0, 2), (-6, 0, 2), ]
    ar4 += [(-5, 0, 5), (-2, 0, 6), (-2, 0, 8), ]
    ar4 += [(-3, 0, 8), (0, 0, 11), (3, 0, 8), ]
    ar4 += [(2, 0, 8), (2, 0, 6), (5, 0, 5), ]
    ar4 += [(6, 0, 2), (8, 0, 2), (8, 0, 3), ]
    ar4 += [(11, 0, 0), (8, 0, -3), (8, 0, -2), ]
    ar4 += [(6, 0, -2), (5, 0, -5), (2, 0, -6), ]
    ar4 += [(2, 0, -8), (3, 0, -8), (0, 0, -11), ]
    # Pointer shape
    pointer = [(-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), ]
    pointer += [(0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), ]
    pointer += [(0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), ]
    pointer += [(0, 0, 0), (0, 2, 0), ]
    # Foot shape
    foot = [[-4, 0, -4], [-4, 0, -7], [-3, 0, -11], ]
    foot += [[-1, 0, -12], [0, 0, -12], [1, 0, -12], ]
    foot += [[3, 0, -11], [4, 0, -7], [4, 0, -4], ]
    foot += [[-4, 0, -4], [-5, 0, 1], [-5, 0, 6], ]
    foot += [[-4, 0, 12], [-2, 0, 15], [0, 0, 15.5], ]
    foot += [[2, 0, 15], [4, 0, 12], [5, 0, 6], ]
    foot += [[5, 0, 1], [4, 0, -4], [-4, 0, -4], ]
    foot += [[4, 0, -4], ]
    # Hoof shape
    hoof = [[-6, 0, -5], [-6.5, 0, -1], [-6, 0, 3], ]
    hoof += [[-5.2, 0, 5.5], [-3, 0, 7.5], [0, 0, 8.2], ]
    hoof += [[3, 0, 7.5], [5.2, 0, 5.5], [6, 0, 3], ]
    hoof += [[6.5, 0, -1], [6, 0, -5], [4, 0, -5], ]
    hoof += [[4.5, 0, -1], [4, 0, 3], [3.5, 0, 4.5], ]
    hoof += [[2, 0, 6], [0, 0, 6.5], [-2, 0, 6], ]
    hoof += [[-3.5, 0, 4.5], [-4, 0, 3], [-4.5, 0, -1], ]
    hoof += [[-4, 0, -5], [-6, 0, -5], [-5.5, 0, -6.5], ]
    hoof += [[5.5, 0, -6.5], [4.5, 0, -10], [2.2, 0, -12.2], ]
    hoof += [[0, 0, -12.2], [-2.2, 0, -12.2], [-4.5, 0, -10], ]
    hoof += [[-5.5, 0, -6.5], ]
    # Hoof2 shape
    hoof2 = [[6, 6, -12], [0, 8, -12], [-6, 6, -12], ]
    hoof2 += [[-8, 3, -13], [-8, 0, -12], [-7, 0, -10], ]
    hoof2 += [[-8, 0, -6], [-9, 0, -1], [-8, 0, 4], ]
    hoof2 += [[-5, 0, 9], [0, 0, 10], [5, 0, 9], ]
    hoof2 += [[8, 0, 4], [9, 0, -1], [8, 0, -6], ]
    hoof2 += [[7, 0, -10], [8, 0, -12], [8, 3, -13], ]
    hoof2 += [[6, 6, -12], ]
    # Dictionary
    ctrl = {
        "cub": cub, 
        "sph": sph, 
        "cyl": cyl, 
        "pip": pip, 
        "con": con, 
        "ar1": ar1, 
        "ar2": ar2, 
        "ar3": ar3, 
        "ar4": ar4, 
        "pointer": pointer, 
        "foot": foot, 
        "hoof": hoof, 
        "hoof2": hoof2, 
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
                # vtx position
                pointList.append(pm.pointPosition(j))
            except:
                # obj position
                pointList.append(pm.xform(j, q=True, ws=True, rp=True))
        pm.curve(p=pointList)


# Creates a curve along the locator's points.
# Place locators first, and select them, and call this function.
def cuvLoc(cl=False): # cl = closed
    sel = pm.ls(sl=True) # select locators
    posLocator = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
    if cl:
        # if closed : first, creates a circle, and change its shape.
        cuvName = pm.circle(nr=(0, 1, 0), ch=False, s=len(sel))[0]
        for j, k in enumerate(posLocator):
            pm.move(k[0], k[1], k[2], '%s.cv[%d]' % (cuvName, j), ws=True)
    else:
        print("# ex : cuvLoc(cl=True)")
        cuvName = pm.curve(p=posLocator)


# Attempt to delete unused plugins.
def delPlugin():
    unknownList = pm.ls(type="unknown")
    pm.delete(unknownList) # Just delete Unknown type list.
    pluginList = pm.unknownPlugin(q=True, l=True)
    if pluginList:
        for j, k in enumerate(pluginList):
            pm.unknownPlugin(k, r=True)
            # Print deleted plugin's names and number
            print("%d : %s" % (j, k))
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
        grp = pm.group(em=True, n=i + "_grp")
        pm.matchTransform(grp, i, pos=True, rot=True)
        try:
            # Selector's mom group.
            iParent = "".join(pm.listRelatives(i, p=True))
            pm.parent(grp, iParent)
        except:
            pass
        pm.parent(i, grp)


# Select mesh only.
def selObj():
    sel = pm.ls(sl=True, s=True, dag=True)
    meshList = {i.getParent() for i in sel if pm.objectType(i) == "mesh"}
    result = list(meshList)
    pm.select(result)
    return result


# Select groups only.
def selGrp():
    '''If there is no shape and the object type is not 
    'joint', 'ikEffector', 'ikHandle', 'Constraint', ...
    then it is most likely a group.'''
    sel = pm.ls(sl=True, dag=True, type=['transform'])
    grp = []
    for i in sel:
        typ = pm.objectType(i)
        A = pm.listRelatives(i, s=True)
        B = typ in ['joint', 'ikEffector', 'ikHandle',]
        C = 'Constraint' in typ
        if not (A or B or C):
            grp.append(i)
        else:
            continue
    pm.select(grp)
    return grp


# Select objects with duplicate names.
def sameName():
    sel = pm.ls(tr=True)
    dup = [i for i in sel if "|" in i]
    if dup:
        pm.select(dup)
        om.MGlobal.displayError("Same name selected in outliner.")
    else:
        om.MGlobal.displayInfo("No duplicated names.")


# Moving pivot to zero.
def zeroPivot():
    sel = pm.ls(sl=True)
    for i in sel:
        j = f"{i}.scalePivot"
        k = f"{i}.rotatePivot"
        pm.move(0, 0, 0, j, k, rpr=True)


# rename function used in maya
# txt -> 'testName23_17_grp'
def rename(*arg: str) -> None:
    """ Rename by incrementing the last digit in the string. """
    numArg = len(arg)
    sel = pm.ls(sl=True)
    # Given a single argument, create a new name.
    if numArg == 1:
        txt = arg[0]
        # txtList -> ['testName', '23', '_', '17', '_grp']
        txtList = re.split(r'([^0-9]+)([0-9]*)', txt)
        txtList = [i for i in txtList if i]
        # txtDict -> {1: (23, 2), 3: (17, 2)}
        txtDict = {}
        for i, n in enumerate(txtList):
            if n.isdigit():
                txtDict[i] = (int(n), len(n))
            else:
                continue
        if len(txtDict):
            idx = max(txtDict) # idx -> 3
            numTuple = txtDict[idx] # numTuple -> (17, 2)
            num = numTuple[0] # num -> 17
            numDigit = numTuple[1] # numDigit -> 2
            for j, k in enumerate(sel):
                numStr = str(num + j) # increase by j
                numLen = len(numStr) # digit of numStr
                # Match <numStr> with the input <numDigit>
                if numLen < numDigit:
                    sub = numDigit - numLen
                    numStr = '0'*sub + numStr
                txtList[idx] = numStr
                new = ''.join(txtList) # new -> 'testName23_17_grp'
                pm.rename(k, new)
        else:
            for j, k in enumerate(sel):
                new = ''.join(txtList) + str(j)
                pm.rename(k, new)
    # Two arguments replace words.
    elif numArg == 2:
        before = arg[0]
        after = arg[1]
        for obj in sel:
            new = obj.replace(before, after)
            pm.rename(obj, new)
    else:
        msg = "Given a single argument, create a new name. "
        msg += "Two arguments replace words."
        om.MGlobal.displayError(msg)


# Get the poleVector's position in maya.
def poleVector():
    '''Create temporary joints, and use aimConstraint's worldUpObject 
    to find the position of the poleVector.'''
    sel = pm.ls(sl=True) # Select three objects.
    if len(sel) != 3:
        om.MGlobal.displayError('Select three objects.')
    else:
        midJnt = sel[1]
        endJnt = sel[2]
        # List the coordinates of the joint
        points = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
        p1, p2, p3 = [i for i in points]
        # It's good to clear the selection before creating the joint.
        pm.select(cl=True)
        # Temporarily create two joints.
        temp1 = pm.joint(p=p1)
        temp2 = pm.joint(p=p3)
        # Use Maya's <Orient joint> menu.
        pm.joint(temp1, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(temp2, e=True, oj='none', ch=True, zso=True)
        # o: offset, wut: worldUpType, wuo: worldUpObject
        pm.aimConstraint(endJnt, temp1, o=(0,0,90), wut='object', wuo=midJnt)
        # cn: constraint
        pm.delete(temp1, cn=True)
        # Position to the middle joint.
        pm.matchTransform(temp1, midJnt, pos=True)
        # Create a locator and 
        loc = pm.spaceLocator()
        # place it at the poleVector position.
        pm.matchTransform(loc, temp2, pos=True, rot=True)
        # Delete temporarily used joints.
        pm.delete(temp1)


# Change the color of the controllers.
def color(**kwargs):
    sel = pm.ls(sl=True, dag=True, s=True)
    colors = {
        "blue": 6, 
        "pink": 9, 
        "red": 13, 
        "green": 14, 
        "yellow": 17, 
    }
    idxList = [colors[i] for i in kwargs if kwargs[i]]
    enb = 1 if idxList else 0
    idx = idxList[0] if idxList else 0
    for i in sel:
        pm.setAttr(f"{i}.overrideEnabled", enb)
        pm.setAttr(f"{i}.overrideColor", idx)


# Open the Windows folder and copy the fullPath to the clipboard.
def openSaved():
    fullPath = pm.Env().sceneName()
    dir = os.path.dirname(fullPath)
    # copy the fullPath to the clipboard.
    subprocess.run("clip", text=True, input=fullPath)
    # Open the Windows folder
    os.startfile(dir)


# Create locators in boundingBox.
# 'jnt=True' option available.
def createLoc(**kwargs):
    sel = pm.ls(sl=True)
    if not sel:
        pass
    else:
        # bb is boundingBox
        bb = pm.xform(sel, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMin + xMax) / 2
        y = (yMin + yMax) / 2
        z = (zMin + zMax) / 2
        loc = pm.spaceLocator()
        pm.move(loc, x, y, z)
        if not kwargs:
            pass
        else:
            for key, value in kwargs.items():
                if key == "jnt" and value:
                    pm.select(cl=True)
                    jnt = pm.joint(p=(0,0,0), rad=10)
                    pm.matchTransform(jnt, loc, pos=True)
                    pm.delete(loc)
                else:
                    pass


# 79 char line ================================================================
# 72 docstring or comments line ========================================


# createLoc(jnt=True)
# grp(cp=True)
# rename('jnt_R_1')
# selObj()
grpEmpty()