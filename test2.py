import re
import os
import shutil
import filecmp
import subprocess
import codecs
import maya.OpenMaya as om
import pymel.core as pm


# Synchronize the dev and pub folders.
# Available in the madmanpost folder tree.
class sync():
    def __init__(self):
        self.setupUI()
        self.setText()
    

    # UI.
    def setupUI(self):
        winStr = 'Modeling_Synchronize'
        if pm.window(winStr, exists=True):
            pm.deleteUI(winStr)
        win = pm.window(winStr, t='SynChronize', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=285)
        pm.separator(h=10)
        self.caseText = pm.text(h=23)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=2, cw=[(1, 50), (2, 226)])
        pm.text('User : ')
        user = pm.internalVar(uad=True).split('/')[2]
        self.userField = pm.textField(ed=True, tx=user)
        pm.setParent("..", u=True)
        self.memoField = pm.scrollField(ed=True, ww=True, h=100)
        self.syncField = pm.textField(ed=False)
        pm.button('Refresh', c=lambda x: self.setText())
        pm.separator(h=10)
        pm.button('Synchronize', c=lambda x: self.syncMain())
        pm.button('Open the pub folder', c=lambda x: self.openPubFolder())
        pm.button('Export to Alembic', c=lambda x: self.makeAbc())
        pm.button('Open the note', c=lambda x: self.openNotepad())
        pm.separator(h=10)
        pm.showWindow(win)


    # Fill in the text.
    def setText(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            case = "___ Unknown File ___"
            ver = ''
        else:
            # set values
            cmp = self.compareFiles(fullPath)
            dev, pub, nwe = self.info(fullPath, dev=True, pub=True, nwe=True)
            if cmp:
                case = "=== Sync complete ==="
            else:
                case = "*** Not synchronized ***"
            case += "\n" + nwe
            verDev = self.getMaxVersion(dev)
            verDev = verDev if verDev else "_____"
            verPub = self.getMaxVersion(pub)
            verPub = verPub if verPub else "_____"
            ver = f"dev) {verDev}    /    pub) {verPub}"
        # set text
        self.caseText.setLabel(case)
        self.syncField.setText(ver)


    # Two steps : Synchronize and write Korean text.
    def syncMain(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            om.MGlobal.displayError("Save scene, first.")
        else:
            cmp = self.compareFiles(fullPath)
            if cmp:
                om.MGlobal.displayInfo("All Files are synchronized.")
            else:
                # Save and Copy
                dev, pub, v9999 = self.makeSyncNames(fullPath)
                self.makeSyncFiles(fullPath, dev, pub, v9999)
                # Write down notes
                textPath = self.makeTextPath(fullPath)
                verInfo = self.makeTextVersionInfo(dev, pub, v9999)
                self.makeText(textPath, verInfo)
                # reStart UI
                self.syncField.setText(verInfo)
                self.setText()


    # Make the text fields.
    def makeTextVersionInfo(self, devPath, pubPath, v9999Path):
        dev = self.info(devPath, ver=True)[0]
        pub = self.info(pubPath, ver=True)[0]
        v9999 = self.info(v9999Path, ver=True)[0]
        result = f"dev) {dev} = pub) {pub}, {v9999}"
        return result


    # Returns index number and check the company folder tree, too.
    def getIndex(self, fullPath):
        typList = ["mdl", "ldv", "rig"]
        dirList = fullPath.split("/")
        result = [dirList.index(i) for i in typList if i in dirList]
        return result


    # Return scene's infomations.
    def info(self, fullPath, **kwargs):
        # fullPath: "Y:/project/folder/mdl/pub/scenes/file_mdl_v0011.ma"
        idx = self.getIndex(fullPath)
        if not idx:
            msg = "Check the folder tree with company rules."
            om.MGlobal.displayError(msg)
        else:
            # dir: "Y:/project/folder/mdl/pub/scenes"
            dir = os.path.dirname(fullPath)
            # "file_mdl_v0011.ma"
            scn = os.path.basename(fullPath) 
            # nwe: Name Without Extension
            # nwe: "file_mdl_v0011"
            # ext: ".ma"
            nwe, ext = os.path.splitext(scn)
            # wip: "pub"
            wip = dir.split("/")[idx[0] + 1]
            # typ: "mdl"
            typ = dir.split("/")[idx[0]]
            # ver: "v0011"
            ver = nwe.split("_")[-1]
            # nwv: Name Without Version
            # nwv: file_mdl
            nwv = nwe.rsplit("_", 1)[0]
            # dev: "Y:/project/folder/mdl/dev"
            # pub: "Y:/project/folder/mdl/pub"
            if wip == 'dev':
                (dev, pub) = (dir, dir.replace("dev", "pub"))
            if wip == 'pub':
                (dev, pub) = (dir.replace("pub", "dev"), dir)
            # "Y:/project/folder/mdl/pub/data/abc"
            abc = pub.replace('scenes', 'data/abc')
            # keys
            result = {
                'dir': dir, 
                'scn': scn, 
                'nwe': nwe, 
                'ext': ext, 
                'wip': wip, 
                'typ': typ, 
                'ver': ver, 
                'nwv': nwv, 
                'dev': dev, 
                'pub': pub, 
                'abc': abc
            }
            return [result[i] for i in kwargs if kwargs[i]]
    

    # Returns the maximum version of the input directory.
    def getMaxVersion(self, dir):
        # File types are ".ma" or ".mb"
        mayaList = []
        Files = os.listdir(dir)
        for i in Files:
            ma = i.endswith('.ma')
            mb = i.endswith('.mb')
            if ma or mb:
                mayaList.append(i)
        verList = []
        for i in mayaList:
            fullPath = (dir + "/" + i)
            ver = self.info(fullPath, ver=True)
            ver = ''.join(ver)
            if not ver:
                continue
            elif ver == 'v9999': # 'v9999' doesn't count.
                continue
            elif not ver.startswith('v'): # The first string is 'v'.
                continue
            elif not ver[1:].isdigit(): # EveryThing except 'v' is digit
                continue
            elif len(ver[1:]) != 4: # Digit Length is 4.
                continue
            else:
                verList.append(ver)
        verList.sort(reverse=True)
        result = verList[0] if verList else False
        return result


    # Return the bigger of the two versions.
    def compareVersion(self, ver1, ver2):
        if not ver1: ver1 = 'v0000' # False to 'v0000'
        if not ver2: ver2 = 'v0000' # False to 'v0000'
        verList = [ver1, ver2]
        result = sorted(verList, reverse=True)[0]
        return result


    # Return the maxVersion + 1
    def makeSyncVersion(self, dev, pub):
        if not os.path.isdir(dev): os.makedirs(dev)
        if not os.path.isdir(pub): os.makedirs(pub)
        maxVerInDev = self.getMaxVersion(dev) # 'v0005' <- example
        maxVerInPub = self.getMaxVersion(pub) # 'v0004' <- example
        # 'v0005' <- return the bigger
        finalString = self.compareVersion(maxVerInDev, maxVerInPub)
        finalNumber = int(finalString[1:]) + 1 # 'v0005' -> 6
        result = "v%04d" % finalNumber # 6 -> 'v0006'
        return result


    # Make a sync full path.
    # Return the three path.
    def makeSyncNames(self, fullPath):
        Info = self.info(fullPath, nwv=True, ext=True, dev=True, pub=True)
        nwv, ext, dev, pub = Info
        ver = self.makeSyncVersion(dev, pub)
        devPath = f"{dev}/{nwv}_{ver}{ext}"
        pubPath = f"{pub}/{nwv}_{ver}{ext}"
        v9999 = f"{pub}/{nwv}_v9999{ext}"
        result = [devPath, pubPath, v9999]
        return result


    # Compare Two Files.
    # maxNumber in devFolder = maxNumber in pubFolder
    def compareFiles(self, fullPath):
        Info = self.info(fullPath, nwv=True, ext=True, dev=True, pub=True)
        nwv, ext, dev, pub = Info
        maxVerInDev = self.getMaxVersion(dev)
        maxVerInPub = self.getMaxVersion(pub)
        # Even if the real file is the same, return False
        if maxVerInDev != maxVerInPub:
            result = False
        else:
            devPath = f"{dev}/{nwv}_{maxVerInDev}{ext}"
            pubPath = f"{pub}/{nwv}_{maxVerInPub}{ext}"
            v9999 = f"{pub}/{nwv}_v9999{ext}"
            try:
                A = filecmp.cmp(devPath, pubPath)
                B = filecmp.cmp(pubPath, v9999)
                if A and B:
                    result = True
                else:
                    result = False
            except:
                result = False
        return result


    # Different case depending on open file.
    # Just save and copy.
    def makeSyncFiles(self, fullPath, dev, pub, v9999):
        wip, ver = self.info(fullPath, wip=True, ver=True)
        if wip == 'dev':
            pm.saveAs(dev)
            shutil.copy(dev, pub)
            shutil.copy(dev, v9999)
        else:
            if ver == 'v9999':
                pm.saveFile()
                shutil.copy(v9999, dev)
                shutil.copy(v9999, pub)
            else:
                pm.saveAs(pub)
                shutil.copy(pub, dev)
                shutil.copy(pub, v9999)

    # Create an alembic path.
    def makeAbcPath(self):
        fullPath = pm.Env().sceneName()
        nwv, dir = self.info(fullPath, nwv=True, abc=True)
        if not os.path.isdir(dir): os.makedirs(dir)
        abcPath = f"{dir}/{nwv}_v9999.abc"
        return abcPath, dir


    # Normal is unchecked in export options.
    def makeAbc(self):
        sel = pm.ls(sl=True, long=True)
        if not sel:
            om.MGlobal.displayError("Nothing selected.")
        else:
            abcPath, dir = self.makeAbcPath()
            os.startfile(dir)
            abcFile = " -file " + abcPath
            start_end = "-frameRange %d %d" % (1, 1)
            selection = ''.join([" -root " + i for i in sel])
            exportOpt = start_end
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
            exportOpt += abcFile
            pm.AbcExport(j = exportOpt)


    # Make the path of notepad.
    def makeTextPath(self, fullPath):
        fileName = 'readme'
        pubFolder = self.info(fullPath, pub=True)
        pubFolder = ''.join(pubFolder)
        result = pubFolder + '/' + fileName + '.txt'
        return result


    # Write down notepad.
    def makeText(self, textPath, verInfo):
        user = "User : "
        user += self.userField.getText()
        date = "Date : "
        date += pm.date()
        memo = "Memo : "
        memo += self.memoField.getText().replace("\n", "\n#         ")
        version = "version : "
        version += verInfo
        with codecs.open(textPath, 'a', 'utf-8-sig') as txt:
            line = "# " + "=" * 40 + " #" + "\n"
            line += "# " + f"{user}" + "\n"
            line += "# " + f"{date}" + "\n"
            line += "# " + f"{memo}" + "\n"
            line += "# " + f"{version}" + "\n"
            line += "# " + "=" * 40 + " #" + "\n"
            txt.write(line)


    # Open Note.
    def openNotepad(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            msg = "Unable to extract path from scene file."
            om.MGlobal.displayError(msg)
        else:
            notePath = self.makeTextPath(fullPath)
            if not os.path.isfile(notePath):
                om.MGlobal.displayError("There is no readme.txt.")
            else:
                progName = "Notepad.exe"
                subprocess.Popen([progName, notePath])

    # Open the publish folder of this file.
    def openPubFolder(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            om.MGlobal.displayError("The scene must be saved.")
        else:
            pubFolder = self.info(fullPath, pub=True)
            os.startfile(pubFolder)


# Match attributes of referenced shape to deformed shape's attributes.
class MatchCatclark:
    def __init__(self):
        """ When you apply a deformer to a referenced object, 
        a deformed node is created in this scene. 
        There are some cases 
        below to apply 'anorld catclark attribute' to the deformed node.
        Case 1 : When 'referenced' and 'deformed' are together
        Case 2 : When 'referenced' and not 'deformed'
        Case 3 : when not 'referenced' and 'deformed'
        Case 4 : When it is an object created in this scene.
         """
        self.attrName = {
            'aiSubdivType': 1, 
            'aiSubdivIterations': 1, 
        }
        self.conditions()


    def conditions(self):
        """ 1. Select only objects that object type is mesh, 
        2. Determines the referenced and Deformed created in this scene. 
        3. And compare the names and match, 
        4. For use 'pm.setAttr()', 'pm.rename()' in pymel's commands, 
        5. get attribute infomations from the Referenced shape.
        6. And match the attributes to Deformed. 
        7. Finally, rename it by deleting 'Deformed' from the name.
         """
        objs = self.selObj()
        allShape = pm.ls(objs, dag=True, s=True)
        referenced = pm.ls(allShape, rn=True)
        notReferenced = [i for i in allShape if not i in referenced]
        deformed = [i for i in notReferenced if re.search('.*Deformed', i.name())]
        created = [i for i in notReferenced if not i in deformed]
        if not objs:
            print("Nothing selected.")
        else:
            """ Case 1 """
            if referenced and deformed:
                attrInfo = self.getAttrInfo(referenced)
                result = self.syncAttrDeformed(attrInfo, deformed)
                print('\n'.join(result))
            """ Case 2 """
            if referenced and (not deformed):
                pass
                # attrInfo = self.getAttrInfo(referenced)
                # result = [f"{name}: {attr}" for name, attr in attrInfo.items()]
                # print('\n'.join(result))
            """ Case 3 """
            if (not referenced) and deformed:
                result = self.setCatclark(deformed)
                print('\n'.join(result))
            """ Case 4 """
            if created:
                result = self.setCatclark(created)
                print('\n'.join(result))


    # Select only objects that object type is mesh,
    def selObj(self) -> list:
        sel = pm.ls(sl=True, s=True, dag=True)
        objList = []
        for i in sel:
            if pm.objectType(i) == "mesh":
                obj = i.getParent()
                objList.append(obj)
            else:
                continue
        objSet = set(objList)
        result = list(objSet)
        return result


    # Get attributes infomations from the Referenced shape.
    def getAttrInfo(self, shape: list) -> dict:
        result = {}
        for shapeName in shape:
            attr = {i: pm.getAttr(f"{shapeName}.{i}") for i in self.attrName}
            result[shapeName] = attr
        return result


    # And match the attributes to Deformed.
    def syncAttrDeformed(self, attrInfo: dict, deformed: list) -> list:
        """ First, remove the 'Deformed' letter from the shape. 
        Compares the name of the reference. 
        Get attributes information, applied to deformed shape.
         """
        result = []
        for shapeDeformed in deformed:
            removeDeformed = shapeDeformed.rsplit("Deformed", 1)[0]
            for shapeReferenced, attrs in attrInfo.items():
                chk = re.search(f'.*[:]{removeDeformed}', shapeReferenced.name())
                if chk:
                    for attrName, attrValue in attrs.items():
                        pm.setAttr(f"{shapeDeformed}.{attrName}", attrValue)
                else:
                    continue
                result.append(f"{shapeDeformed} -> {removeDeformed} = {attrs}")
            '''I don't want to change the word 'Deformed'. 
            If you remove the word 'Deformed' from the name, 
            you'll have to do something else next time 
            to match the 'Original modeling attribute'.'''
            # pm.rename(shapeDeformed, removeDeformed)
        return result


    # Put a value in the attribute.
    def setCatclark(self, shape: list) -> list:
        result = []
        for shapeName in shape:
            for attr, value in self.attrName.items():
                pm.setAttr(f"{shapeName}.{attr}", value)
                result.append(f"{shapeName}.{attr} = {value}")
        return result


# pep8: 79 char line ==========================================================
# pep8: 72 docstring or comments line ==================================


