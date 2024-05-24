from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
from general import *
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Car(QWidget):
    def __init__(self):
        self.rootJnt = "jnt_root"
        self.rootFbx = "fbx_root"
        self.mainCtrl = "cc_main"
        self.ctrlNames = {
            "car": "cc_body", 
            "car2": "cc_sub", 
            "circle": "cc_main", 
            }
        self.jntNameAndPos = {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_bodyEnd": (0, 145, 0), 
            "jnt_wheelLeftFront": (70, 30, 140), 
            "jnt_wheelLeftFrontEnd": (85, 30, 140), 
            "jnt_wheelRightFront": (-70, 30, 140), 
            "jnt_wheelRightFrontEnd": (-85, 30, 140), 
            "jnt_wheelLeftRear": (70, 30, -140), 
            "jnt_wheelLeftRearEnd": (85, 30, -140), 
            "jnt_wheelRightRear": (-70, 30, -140), 
            "jnt_wheelRightRearEnd": (-85, 30, -140), 
            }
        self.hierarchy = {
            "jnt_root": [
                [f"jnt_body{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftRear{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightRear{i}" for i in ["", "End"]], 
                ], 
            }
        super(Car, self).__init__()
        self.sortCount = 0
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()
    

    def setupUI(self):
        pass


    def build(self):
        self.updateJointsPosition()
        # self.updateSameSide()
        self.cleanUp()
        self.createGroups()
        self.createJoints()
        self.createFbxJoints()
        self.createCtrls()
        # self.setControllers()


    def updateJointsPosition(self):
        for jnt in self.jntNameAndPos.keys():
            pos = getPosition(jnt)
            self.jntNameAndPos[jnt] = pos


    def updateSameSide(self, side: str="LeftToRight"):
        """ The default change is from left to right. 
        But the opposite is also possible.
        >>> updateSameSide()
        >>> updateSameSide("RightToLeft")
         """
        A, B = side.split("To")
        aSide = []
        bSide = []
        for jntName in self.jntNameAndPos.keys():
            if A in jntName:
                aSide.append(jntName)
            elif B in jntName:
                bSide.append(jntName)
            else:
                continue
        for idx, aJoint in enumerate(aSide):
            x, y, z = pm.xform(aJoint, q=True, t=True, ws=True)
            bJoint = bSide[idx]
            self.jntNameAndPos[bJoint] = (-1*x, y, z)


    def cleanUp(self):
        listDelete = [
            self.rootJnt, 
            self.rootFbx, 
            self.mainCtrl + "_grp", 
            ]
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue


    def createGroups(self):
        carName = "test"
        rg = RigGroups()
        rg.createRigGroups(carName)


    def createJoints(self):
        for jnt, pos in self.jntNameAndPos.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        for parents, childList in self.hierarchy.items():
            for children in childList:
                parentHierarchically(*children)
                pm.makeIdentity(children, a=1, t=1, r=1, s=1, jo=1)
                pm.parent(children[0], parents)
        self.tryParent(self.rootJnt, "bindBones")


    def createFbxJoints(self):
        fbx = pm.duplicate(self.rootJnt, rr=True, n=self.rootFbx)
        fbx = fbx[0]
        pm.select(cl=True)
        pm.select(fbx, hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("jnt_", "fbx_")
            pm.rename(i, new)
        self.tryParent(self.rootFbx, "rigBones")


    def createCtrls(self):
        cc = Controllers()
        cc.createControllers(**self.ctrlNames)
        ctrl = list(self.ctrlNames.values())
        grps = []
        for i in ctrl:
            if self.mainCtrl == i:
                pm.scale(i, (20, 20, 20))
                pm.makeIdentity(i, a=1, t=0, r=0, s=1, n=0, pn=1)
            grp = groupingWithOwnPivot(i)[0]
            grps.append(grp)
        for child, parents in zip(grps[:2], ctrl[1:]):
            pm.parent(child, parents)
        pm.matchTransform(grps[0], "jnt_body", pos=True)
        self.tryParent(self.mainCtrl + "_grp", "controllers")
        

    def tryParent(self, child: str, parents: str):
        try:
            pm.parent(child, parents)
        except:
            pass


car = Car()
# car.createJoints()
car.build()
