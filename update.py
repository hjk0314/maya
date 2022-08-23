import maya.OpenMaya as om
import pymel.core as pm
import shutil
import codecs
import filecmp
import subprocess
import os


class sync():
    def __init__(self):
        self.setupUI()
    

    # UI.
    def setupUI(self):
        if pm.window('Modeling_Synchronize', exists=True):
            pm.deleteUI('Modeling_Synchronize')
        else:
            win = pm.window('Modeling_Synchronize', t='SynChronize', s=True, rtf=True)
            pm.columnLayout(cat=('both', 4), rowSpacing=2, columnWidth=285)
            pm.separator(h=10)
            pm.text("Model Synchronize", h=23)
            pm.separator(h=10)
            pm.rowColumnLayout(nc=2, cw=[(1, 40), (2, 236)])
            pm.text("dev : ")
            self.devField = pm.textField(ed=True)
            pm.text("pub : ")
            self.pubField = pm.textField(ed=True)
            pm.text(" ")
            self.v9999Field = pm.textField(ed=True)
            pm.setParent("..", u=True)
            pm.rowColumnLayout(nc=4, cw=[(1, 40), (2, 170), (3, 8), (4, 60)])
            pm.text("abc : ")
            self.abcField = pm.textField(ed=True)
            pm.text(" ")
            self.abcCheck = pm.checkBox(l="export", v=False)
            pm.setParent("..", u=True)
            self.memo = pm.scrollField(ed=True, ww=True, h=100)
            pm.separator(h=10)
            pm.button(l='Synchronize', c=lambda x: self.main())
            pm.separator(h=10)
            pm.showWindow(win)


    def checkPath(self, fullPath):
        typeList = ["mdl", "ldv", "rig"]
        nameList = fullPath.split("/")
        result = [nameList.index(i) for i in typeList if i in nameList]
        return result


    # Return scene's infomations.
    def info(self, fullPath, **kwargs):
        idx = self.checkPath(fullPath)
        if not idx:
            om.MGlobal.displayError("Check the File Path.")
        else:
            # values
            dir = os.path.dirname(fullPath)
            sceneName = os.path.basename(fullPath)
            name, ext = os.path.splitext(sceneName)
            wip = dir.split("/")[idx[0] + 1] # dev or pub
            typ = dir.split("/")[idx[0]] # mdl or rig or ldv
            ver = name.split("_")[-1] # v0001 or v9999
            nwv = name.rsplit("_", 1)[0] # nwv : name without version
            # keys
            result = {
                'dir': dir, 
                'sceneName': sceneName, 
                'name': name, 
                'ext': ext, 
                'wip': wip, 
                'typ': typ, 
                'ver': ver,
                'nwv': nwv
            }
            return [result[i] for i in kwargs if kwargs[i]]
    

    def info2(self, fullPath, **kwargs):
        # values
        dir, wip = self.info(fullPath, dir=True, wip=True)
        if wip == 'dev': (dev, pub) = (dir, dir.replace("dev", "pub"))
        elif wip == 'pub': (dev, pub) = (dir.replace("pub", "dev"), dir)
        else: om.MGlobal.displayError("This scene doesn't belong to dev or pub.")
        # keys
        result = {
            'dev': dev, 
            'pub': pub, 
            'abc': pub.replace('scenes', 'data/abc')
        }
        # return
        return [result[i] for i in kwargs if kwargs[i]]


    # Returns the maximum version number of the input directory.
    def getMaxVersion(self, dir):
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


    def compareVersion(self, ver1, ver2):
        if not ver1: ver1 = 'v0000' # if False is input
        if not ver2: ver2 = 'v0000' # if False is input
        verList = [ver1, ver2]
        result = sorted(verList, reverse=True)[0]
        return result


    def finalVersion(self, dev, pub):
        if not os.path.isdir(dev): os.makedirs(dev)
        if not os.path.isdir(pub): os.makedirs(pub)
        maxVerInDev = self.getMaxVersion(dev) # 'v0005'
        maxVerInPub = self.getMaxVersion(pub) # 'v0004'
        finalString = self.compareVersion(maxVerInDev, maxVerInPub) # 'v0005'
        finalNumber = int(finalString[1:]) + 1 # 'v0005' -> 6
        result = "v%04d" % finalNumber # 6 -> 'v0006'
        return result


    def makeNames(self, fullPath):
        nwv, ext = self.info(fullPath, nwv=True, ext=True)
        dev, pub = self.info2(fullPath, dev=True, pub=True)
        ver = self.finalVersion(dev, pub)
        devPath = f"{dev}/{nwv}_{ver}{ext}"
        pubPath = f"{pub}/{nwv}_{ver}{ext}"
        v9999 = f"{pub}/{nwv}_v9999{ext}"
        result = [devPath, pubPath, v9999]
        return result


    def compareFiles(self, fullPath):
        nwv, ext = self.info(fullPath, nwv=True, ext=True)
        dev, pub = self.info2(fullPath, dev=True, pub=True)
        maxVerInDev = self.getMaxVersion(dev)
        maxVerInPub = self.getMaxVersion(pub)
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


    def makeFiles(self, fullPath, dev, pub, v9999):
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


    def makeAbcPath(self, fullPath):
        name = self.info(fullPath, name=True)[0] # without extension
        dir = self.info2(fullPath, abc=True)[0] # "Y:/Project/Assets/Env/sceneName/mdl/pub/data/abc"
        if not os.path.isdir(dir): os.makedirs(dir)
        result = f"{dir}/{name}.abc"
        return result


    def makeAbc(self, abcPath):
        sel = pm.ls(sl=True, long=True)
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


    def makeTextPath(self, fullPath):
        fileName = b'\xec\x9e\x91\xec\x97\x85\xec\x9e\x90'.decode("utf-8", "strict")
        dir = self.info2(fullPath, pub=True)[0]
        result = dir + '/' + fileName + '.txt'
        return result


    # Make Korean document.
    def makeText(self, textPath):
        # bytes, Korean
        user = b'\xec\x9e\x91\xec\x97\x85\xec\x9e\x90 : '.decode("utf-8", "strict")
        user += pm.internalVar(uad=True).split("/")[2]
        date = b'\xeb\x82\xa0\xec\xa7\x9c : '.decode("utf-8", "strict")
        date += pm.date()
        memo = b'\xeb\xa9\x94\xeb\xaa\xa8 : '.decode("utf-8", "strict")
        memo += self.memo.getText().replace("\n", "\n" + "#" + " " * 9)
        version = b'\xeb\xb2\x84\xec\xa0\x84 : '.decode("utf-8", "strict")
        version += 'dev) v0004 = pub) v9999'
        with codecs.open(textPath, 'a', 'utf-8-sig') as txt:
            line = "# " + "=" * 40 + " #" + "\n"
            line += "# " + f"{user}" + "\n"
            line += "# " + f"{date}" + "\n"
            line += "# " + f"{memo}" + "\n"
            line += "# " + f"{version}" + "\n"
            line += "# " + "=" * 40 + " #" + "\n"
            txt.write(line)


    def main(self):
        sel = pm.ls(sl=True)
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("Save scene, First.")
        elif not sel:
            print("Nothing selected.")
        else:
            cmp = self.compareFiles(fullPath)
            if cmp:
                print("All files are synchronized.")
            else:
                # Save and Copy
                dev, pub, v9999 = self.makeNames(fullPath)
                self.makeFiles(fullPath, dev, pub, v9999)
                # Alembic
                abcPath = self.makeAbcPath(fullPath)
                self.makeAbc(abcPath)
                # Write down notes
                textPath = self.makeTextPath(fullPath)
                self.makeText(textPath)


sync()

