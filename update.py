import maya.OpenMaya as om
import pymel.core as pm
import shutil
import codecs
import filecmp
import subprocess
import os


class mdlSync():
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
            pm.textField(ed=True)
            pm.text("pub : ")
            pm.textField(ed=True)
            pm.text(" ")
            pm.textField(ed=True)
            pm.text("abc : ")
            pm.textField(ed=True)
            pm.setParent("..", u=True)
            self.memo = pm.scrollField(ed=True, ww=True, h=100)
            pm.separator(h=10)
            pm.button(l='Synchronize', c=lambda x: self.makeText())
            pm.separator(h=10)
            pm.showWindow(win)


    # Return scene's infomations.
    def info(self, fullPath='', **kwargs):
        if not fullPath:
            om.MGlobal.displayError('Need to get the fullPath.')
        else:
            # values
            dir = os.path.dirname(fullPath)
            scnName = os.path.basename(fullPath)
            name, ext = os.path.splitext(scnName)
            wip = dir.split("/")[-2]
            typ = dir.split("/")[-3]
            ver = name.split("_")[-1]
            # keys
            result = {
                # 'fullPath': fullPath, 
                'dir': dir, 
                'scnName': scnName, 
                'name': name, 
                'ext': ext, 
                'wip': wip, 
                'typ': typ, 
                'ver': ver
            }
            # return
            return [result[i] for i in kwargs if kwargs[i]]
    

    def info2(self, **kwargs):
        # values
        fullPath = pm.Env().sceneName()
        dir, wip = self.info(fullPath, dir=True, wip=True)
        abc = dir.replace('scenes', 'data/abc')
        if wip == 'dev':
            dev = dir
            pub = dir.replace("dev", "pub")
        elif wip == 'pub':
            dev = dir.replace("pub", "dev")
            pub = dir
        else:
            om.MGlobal.displayError("This scene doesn't belong to dev or pub.")
        # keys
        result = {
            'dev': dev, 
            'pub': pub, 
            'abc': abc
        }
        # return
        return [result[i] for i in kwargs if kwargs[i]]


    # Returns the maximum version number of the input directory.
    def getMaxVersion(self, dir):
        mayaList = [i for i in os.listdir(dir) if i.endswith('.ma') or i.endswith('.mb')]
        verList = []
        for i in mayaList:
            fullPath = (dir + "/" + i)
            ver = self.info(fullPath, ver=True)[0]
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
        return verList[0]


    def makeNames(self):
        pass


    def makeText(self):
        textPath = self.info2(pub=True)[0]
        user = pm.internalVar(uad=True).split("/")[2]
        date = pm.date()
        memo = self.memo.getText()
        with codecs.open(textPath, 'a', 'utf-8-sig') as txt:
            textLine = f"{user}" + "\n"
            textLine += f"{date}" + "\n"
            textLine += f"{memo}" + "\n"
            txt.write(textLine)


    def main(self):
        pass


    def compareFiles(self):
        pass


    def oldVersion(self):
        pass


    def makeAbc(self, fullPath):
        sel = pm.ls(sl=True, long=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            dir = self.info2(abc=True)[0] # "Y:/Project/Assets/Env/sceneName/mdl/pub/data/abc"
            if not os.path.isdir(dir): os.makedirs(dir)
            name = self.info(fullPath, name=True)[0] # without extension
            abcPath = dir + "/" + name + ".abc"
            # Alembic Export Option start =================================
            abc = " -file " + abcPath
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
            exportOpt += abc
            # Alembic Export Option end ===================================
            pm.AbcExport(j = exportOpt)


mdlSync()

