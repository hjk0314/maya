import os
import json
import maya.OpenMaya as om
import pymel.core as pm


# Export to json file and shading networks. And assign to them.
class Abc():
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
class SoftSel():
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


class Rename():
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
            # new field
            self.new = pm.textFieldGrp(l="New name : ", ed=True)
            # check field
            chkStr = 'Replace : '
            chkFn = lambda x: self.updateUI()
            self.chk = pm.checkBoxGrp(l=chkStr, ncb=1, v1=False, cc=chkFn)
            # replace field
            repStr = "Replace to this : "
            self.rep = pm.textFieldGrp(l=repStr, ed=True, en=False)
            # endfield
            endFn = lambda x: self.updateUI()
            self.end = pm.textFieldGrp(l="End : ", ed=True, tcc=endFn)
            # button
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
    def getNumberInName(self, name: str) -> tuple:
        # sample string: 'Cube1_22_obj_22_a2'
        nameSlice = name.split("_")
        # nameSlice: ['Cube1', '22', 'obj', '22', 'a2']
        digitList = []
        # digitList: [(1, '22'), (3, '22')]
        for j, k in enumerate(nameSlice):
            if k.isdigit():
                digitList.append((j, k))
        try:
            result = digitList[-1] # last one
            return result
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


# Delete the node named 'vaccine_gene' and "breed_gene" in the ma file.
# It is related to mayaScanner distributed by autodesk.
class Vaccine():
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


# Create wheels that rotate automatically
class AutoWheel():
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
        cuv = pm.circle(nr=(1,0,0), r=rad, ch=False)
        cuv = cuv[0]
        jnt = cuv + '_jnt'
        null = cuv + '_null_grp'
        prev = cuv + '_prev_grp'
        orient = cuv + '_orient_Grp'
        # expression1 ==================================================
        expr1 = f'float $R = {cuv}.Radius;'
        expr1 += f'float $A = {cuv}.AutoRoll;'
        expr1 += f'float $J = {jnt}.rotateX;'
        expr1 += f'float $C = 2 * 3.141 * $R;' # 2*pi*r
        expr1 += f'float $O = {orient}.rotateY;'
        expr1 += f'float $S = 1;' # Connect the global scale.
        expr1 += f'float $pX = {cuv}.PrevPosX;'
        expr1 += f'float $pY = {cuv}.PrevPosY;'
        expr1 += f'float $pZ = {cuv}.PrevPosZ;'
        expr1 += f'{prev}.translateX = $pX;'
        expr1 += f'{prev}.translateY = $pY;'
        expr1 += f'{prev}.translateZ = $pZ;'
        expr1 += f'float $nX = {cuv}.translateX;'
        expr1 += f'float $nY = {cuv}.translateY;'
        expr1 += f'float $nZ = {cuv}.translateZ;'
        # expression2: Distance between two points.
        expr2 = 'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{jnt}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Auto roll switch.
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += ' / $S;' # Resizing the global scale.
        # expression4
        expr4 = f'{cuv}.PrevPosX = $nX;'
        expr4 += f'{cuv}.PrevPosY = $nY;'
        expr4 += f'{cuv}.PrevPosZ = $nZ;'
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


# Class end. ==================================================================


# Grouping itself and named own
# cp is centerPivot
def grp(cp=False):
    sel = pm.ls(sl=True)
    for i in sel:
        grp = pm.group(i, n="%s_grp" % i)
        if not cp:
            pm.move(0,0,0, grp+".scalePivot", grp+".rotatePivot", rpr=True)


# Create locators in boundingBox.
# Default parameter is True.
def loc(bb=True):
    sel = pm.ls(sl=True)
    for i in sel:
        loc = pm.spaceLocator(p=(0, 0, 0), n=f"loc_{i}")
        # bb is boundingBox
        if bb:
            bbCoordinate = pm.xform(i, q=True, boundingBox=True)
            xMin, yMin, zMin, xMax, yMax, zMax = bbCoordinate
            x = (xMin + xMax) / 2
            y = (yMin + yMax) / 2
            z = (zMin + zMax) / 2
            pos = (x, y, z)
        else:
            pos = pm.xform(i, q=True, t=True, ws=True)
        pm.xform(loc, t=pos, ws=True)
        pm.matchTransform(loc, i, rot=True)


# Create a curve controller.
def ctrl(**kwargs):
    ctrl = {
    "cub": [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1), 
        (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1), 
        (-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1)
    ], 
    "sph": [(0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), (0, -0.7, 0.7), (0, -1, 0), 
        (0, -0.7, -0.7), (0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), (-0.7, 0.7, 0), 
        (-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), 
        (0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), 
        (-0.7, -0.7, 0), (0, -1, 0), (0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), 
        (0, 1, 0)
    ], 
    "cyl": [(-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), 
        (0.7, 1, -0.7), (0, 1, -1), (0, 1, 1), (0, -1, 1), (-0.7, -1, 0.7), 
        (-1, -1, 0), (-0.7, -1, -0.7), (0, -1, -1), (0.7, -1, -0.7), 
        (1, -1, 0), (0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), (0, 1, -1), 
        (-0.7, 1, -0.7), (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), 
        (-1, 1, 0)
    ], 
    "pip": [(0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), (1, -1, 0), (1, 1, 0), 
        (0.7, 1, -0.7), (0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), 
        (-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), (0.7, 1, 0.7), 
        (1, 1, 0), (1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), (0, 1, -1), 
        (-0.7, 1, -0.7), (-1, 1, 0), (-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1)
    ], 
    "con": [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), (0, 2, 0), (0, 0, 1), 
        (-0.87, 0, -0), (0.87, 0, 0), (0, 0, 1)
    ], 
    "ar1": [(0, 0, 2), (2, 0, 1), (1, 0, 1), (1, 0, -2), (-1, 0, -2), 
        (-1, 0, 1), (-2, 0, 1), (0, 0, 2)
    ], 
    "ar2": [(0, 1, 4), (4, 1, 2), (2, 1, 2), (2, 1, -4), (-2, 1, -4), 
        (-2, 1, 2), (-4, 1, 2), (0, 1, 4), (0, -1, 4), (4, -1, 2), (2, -1, 2), 
        (2, -1, -4), (-2, -1, -4), (-2, -1, 2), (-4, -1, 2), (0, -1, 4), 
        (4, -1, 2), (4, 1, 2), (2, 1, 2), (2, 1, -4), (2, -1, -4), 
        (-2, -1, -4), (-2, 1, -4), (-2, 1, 2), (-4, 1, 2), (-4, -1, 2)
    ]
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
    locatorPosition = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
    if cl:
        # if closed : first, creates a circle, and change its shape.
        cuvName = pm.circle(nr=(0, 1, 0), ch=False, s=len(sel))[0]
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
        grp = pm.group(em=True, n=i + "_offset")
        pm.matchTransform(grp, i, pos=True, rot=True)
        try:
            # Selector's mom group.
            iParent = "".join(pm.listRelatives(i, p=True))
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


# is group or not
def isGrp():
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


# 79 char line ================================================================
# 72 docstring or comments line ========================================

