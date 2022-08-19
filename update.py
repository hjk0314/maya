from filecmp import cmp
import maya.cmds as cmds
import maya.OpenMaya as om
import os
import shutil
import codecs
import subprocess


class UpdateVersion():
    def __init__(self):
        self.sceneName = cmds.file(q=True, sn=True)
        if not self.sceneName:
            om.MGlobal.displayWarning('The file must be saved.')
        else:
            self.dir = os.path.dirname(self.sceneName)
            self.scn = os.path.basename(self.sceneName)
            self.tsk = self.findTask(self.dir)
            self.ver = self.sliceVersion(self.scn)
            self.ext = 'ma' # os.path.splitext(self.scn)[1]
            self.lastVerInPub = self.returnLastVer(self.dir if self.tsk[1] == 'pub' else self.dir.replace('dev', 'pub'))
            self.lastVerInDev = self.returnLastVer(self.dir if self.tsk[1] == 'dev' else self.dir.replace('pub', 'dev'))
            self.synchronize()


    def sliceVersion(self, baseName):
        version = baseName.split('.')[0].split('_')[-1]
        if not version[0] == 'v' or not len(version[1:]) == 4:
            return False
        else:
            try:
                num = int(version[1:])
            except:
                return False
        return num
    
    
    def findTask(self, directory):
        taskArtist = ['anim', 'lkd', 'mdl', 'rig']
        taskFolder = ['dev', 'pub']
        artist = [i for i in taskArtist if i in directory]
        folder = [i for i in taskFolder if i in directory]
        return artist + folder # [mdl, pub]


    def returnLastVer(self, dirPath):
        try:
            scnList = [i for i in os.listdir(dirPath) if i.endswith('ma') or i.endswith('mb')]
            verHash = {self.sliceVersion(i):i for i in scnList if self.sliceVersion(i) < 9999}
            verLast = sorted(list(verHash.keys()), reverse=True)
            verLastFullPath = '%s/%s' % (dirPath, verHash[verLast[0]])
        except:
            verLastFullPath = False
        return verLastFullPath


    def returnCopyName(self):
        try:
            scnPub = os.path.basename(self.lastVerInPub)
            verPub = self.sliceVersion(scnPub)
        except:
            verPub = 1
        try:
            scnDev = os.path.basename(self.lastVerInDev)
            verDev = self.sliceVersion(scnDev)
        except:
            verDev = 1
        if self.ver == 9999:
            if self.lastVerInPub or self.lastVerInDev:
                nameToPub = self.sceneName.replace('v9999', 'v%04d' % (max([verPub, verDev]) + 1))
            else:
                nameToPub = self.sceneName.replace('v9999', 'v0001')
            ver9999 = self.sceneName
        else:
            if self.tsk[1] == 'dev':
                ver9999 = '{}/{}'.format(self.dir.replace('dev', 'pub'), self.scn.replace('v%04d' % self.ver, 'v9999'))
                nameToPub = ver9999.replace('v9999', 'v%04d' % (max([verPub, verDev]) + 1))
            else:
                ver9999 = '%s/%s' % (self.dir, self.scn.replace('v%04d' % self.ver, 'v9999'))
                nameToPub = ver9999.replace('v9999', 'v%04d' % (max([verPub, verDev]) + 1))
        nameToDev = nameToPub.replace('pub', 'dev')
        return [ver9999, nameToPub, nameToDev]


    def compareFiles(self):
        if self.ver == 9999:
            if self.lastVerInPub and self.lastVerInDev:
                return cmp(self.sceneName, self.lastVerInPub) and cmp(self.sceneName, self.lastVerInDev)
            else:
                return False
        else:
            if self.tsk[1] == 'dev':
                ver9999 = self.sceneName.replace('dev', 'pub').replace('v%04d' % self.ver, 'v9999')
                if os.path.isfile(ver9999) and self.lastVerInPub:
                    return cmp(self.sceneName, ver9999) and cmp(self.sceneName, self.lastVerInPub)
                else:
                    return False
            else:
                ver9999 = self.sceneName.replace('v%04d' % self.ver, 'v9999')
                if os.path.isfile(ver9999) and self.lastVerInDev:
                    return cmp(self.sceneName, ver9999) and cmp(self.sceneName, self.lastVerInDev)
                else:
                    return False


    def synchronize(self):
        if not self.tsk[0] == 'mdl':
            om.MGlobal.displayError('This button is for modelers.')
        elif self.compareFiles():
            om.MGlobal.displayInfo('All files are already synced.')
        else:
            self.copyList = self.returnCopyName()
            ver999 = self.copyList[0]
            verPub = self.copyList[1]
            verDev = self.copyList[2]
            if self.ver == 9999:
                cmds.file(f=True, s=True)
                shutil.copy(self.sceneName, verPub)
                shutil.copy(self.sceneName, verDev)
            else:
                if self.tsk[1] == 'dev':
                    cmds.file(rn=verDev)
                    cmds.file(f=True, s=True)
                    shutil.copy(verDev, verPub)
                    shutil.copy(verDev, ver999)
                else:
                    cmds.file(rn=verPub)
                    cmds.file(f=True, s=True)
                    shutil.copy(verPub, ver999)
                    shutil.copy(verPub, verDev)
            #self.deleteOldVer(verPub)
            self.syncWindow()


    def deleteOldVer(self, fullPath):
        dir = os.path.dirname(fullPath)
        scn = os.path.basename(fullPath)
        ver = self.sliceVersion(scn)
        v99 = scn.replace('v%04d' % ver, 'v9999')
        scnList = [i for i in os.listdir(dir) if i.endswith(self.ext)]
        delList = [j for j in scnList if j != scn and j != v99]
        if not delList:
            pass
        else:
            for k in delList:
                if 'PROXY' in k or 'proxy' in k:
                    pass
                else:
                    os.remove(dir + '/' + k)


    def syncWindow(self):
        if cmds.window('syncMemo', exists=True):
            cmds.deleteUI('syncMemo')
        else:
            result = self.resultString()
            userName = cmds.internalVar(uad=True).split('/')[2]
            win = cmds.window('syncMemo', t='Memo', s=True, rtf=True)
            cmds.columnLayout(cat=('both',2), rs=5, cw=500)
            cmds.separator(h=10)
            self.user = cmds.textFieldGrp(l='User : ', ed=True, tx=userName)
            # self.chkB = cmds.checkBoxGrp(l='Alembic : ', ncb=1, ed=True, v1=False)
            self.memo = cmds.scrollField(ed=True, ww=True, h=100)
            cmds.separator(h=10)
            cmds.text(l = result, al='left')
            cmds.separator(h=10)
            cmds.button(l='Check the text file after saving.', c=lambda x: self.writeTxt(result, 'yes'))
            cmds.button(l="Text doesn't open after saving.", c=lambda x: self.writeTxt(result, 'no'))
            cmds.separator(h=10)
            cmds.showWindow(win)


    def resultString(self):
        ver999 = self.resultParsing(self.copyList[0])
        verPub = self.resultParsing(self.copyList[1])
        verDev = self.resultParsing(self.copyList[2])
        result = '# Result : '
        result += '%s) %s    =    ' % (ver999[0], ver999[1])
        result += '%s) %s    =    ' % (verPub[0], verPub[1])
        result += '%s) %s' % (verDev[0], verDev[1])
        return result
        

    def resultParsing(self, fullPath):
        dir = os.path.dirname(fullPath)
        scn = os.path.basename(fullPath)
        tsk = self.findTask(dir)
        ver = self.sliceVersion(scn)
        return [tsk[1], 'v%04d'%ver]


    def writeTxt(self, result, yesOrNo):
        abc = self.abcToData()
        if not abc:
            pass
        else:
            time = cmds.date()
            user = cmds.textFieldGrp(self.user, q=True, tx=True)
            memo = cmds.scrollField(self.memo, q=True, tx=True)
            data = result
            path = os.path.dirname(self.copyList[0])
            name = os.path.basename(self.copyList[0])
            name = os.path.splitext(name)[0]
            name = name.replace('_v9999', '')
            textPath = '%s/%s.txt' % (path, name)
            with codecs.open(textPath, 'a', 'utf-8-sig') as txt:
                total = '# %s' % time
                total += ' ' * 4
                total += '# %s\n' % user
                total += memo + '\n'
                total += data + '\n'
                total += '=' * 40 + '\n'
                txt.write(total)
            if yesOrNo == 'yes':
                self.openNotepad(textPath)
            else:
                pass
            cmds.deleteUI('syncMemo')


    def abcToData(self):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            dir = os.path.dirname(self.copyList[0])
            dir = dir.replace('scenes', 'data/abc')
            if not os.path.isdir(dir):
                os.mkdir(dir)
            else:
                pass
            try:
                scn = os.path.basename(self.copyList[0])
                scn = os.path.splitext(scn)[0]
                scn += '.abc'
                filePath = '%s/%s' % (dir, scn)
                abc = " -file " + filePath
                frameRange = "-frameRange %d %d" % (1, 1)
                selection = ''
                for i in sel:
                    selection += " -root " + i
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
                cmds.AbcExport(j = exportOpt)
                om.MGlobal.displayInfo('Successfully done.')
                return filePath
            except:
                return False


    def openNotepad(self, fullPath):
        progName = "Notepad.exe"
        subprocess.Popen([progName, fullPath])