import maya.OpenMaya as om
import pymel.core as pm
import shutil
import codecs
import filecmp
import subprocess
import os


# Synchronize the dev and pub folders.
# Available in the madmanpost folder tree.
class sync():
    def __init__(self):
        self.setupUI()
        self.setText()
    

    # UI.
    def setupUI(self):
        if pm.window('Modeling_Synchronize', exists=True):
            pm.deleteUI('Modeling_Synchronize')
        win = pm.window('Modeling_Synchronize', t='SynChronize', s=True, rtf=True)
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
            case = "=== Sync complete ===" if cmp else "*** Not synchronized ***"
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
        idx = self.getIndex(fullPath)
        if not idx:
            om.MGlobal.displayError("Check the folder tree with company rules.")
        else:
            # sample : "C:/Users/jkhong/Desktop/bundangA/mdl/pub/scenes/env_bundangA_mdl_v0011.ma"
            dir = os.path.dirname(fullPath) # "C:/Users/jkhong/Desktop/bundangA/mdl/pub/scenes"
            scn = os.path.basename(fullPath) # "env_bundangA_mdl_v0011.ma"
            # nwe = nameWithoutExtension
            nwe, ext = os.path.splitext(scn) # "env_bundangA_mdl_v0011"
            wip = dir.split("/")[idx[0] + 1] # "pub"
            typ = dir.split("/")[idx[0]] # "mdl"
            ver = nwe.split("_")[-1] # "v0011"
            # nwv = nameWithoutVersion
            nwv = nwe.rsplit("_", 1)[0] # "env_bundangA_mdl"
            if wip == 'dev': (dev, pub) = (dir, dir.replace("dev", "pub")) # "C:/Users/jkhong/Desktop/bundangA/mdl/dev"
            if wip == 'pub': (dev, pub) = (dir.replace("pub", "dev"), dir) # "C:/Users/jkhong/Desktop/bundangA/mdl/pub"
            abc = pub.replace('scenes', 'data/abc') # "C:/Users/jkhong/Desktop/bundangA/mdl/pub/data/abc"
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
        mayaList = [i for i in os.listdir(dir) if i.endswith('.ma') or i.endswith('.mb')]
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
            elif not ver[1:].isdigit(): # The rest of the string is digit.
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
        finalString = self.compareVersion(maxVerInDev, maxVerInPub) # 'v0005' <- return the bigger
        finalNumber = int(finalString[1:]) + 1 # 'v0005' -> 6
        result = "v%04d" % finalNumber # 6 -> 'v0006'
        return result


    # Make a sync full path.
    # Return the three path.
    def makeSyncNames(self, fullPath):
        nwv, ext, dev, pub = self.info(fullPath, nwv=True, ext=True, dev=True, pub=True)
        ver = self.makeSyncVersion(dev, pub)
        devPath = f"{dev}/{nwv}_{ver}{ext}"
        pubPath = f"{pub}/{nwv}_{ver}{ext}"
        v9999 = f"{pub}/{nwv}_v9999{ext}"
        result = [devPath, pubPath, v9999]
        return result


    # Compare Two Files.
    # maxNumber in devFolder = maxNumber in pubFolder
    def compareFiles(self, fullPath):
        nwv, ext, dev, pub = self.info(fullPath, nwv=True, ext=True, dev=True, pub=True)
        maxVerInDev = self.getMaxVersion(dev)
        maxVerInPub = self.getMaxVersion(pub)
        # Even if the real file is the same, return False, if the version is simply different.
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
            om.MGlobal.displayError("Unable to extract path from scene file.")
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

