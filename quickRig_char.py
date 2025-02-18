from collections import Iterable
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QFont
from shiboken2 import wrapInstance
from hjk import *
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Character(QWidget):
    def __init__(self):
        self.mainCurve = "mainCurve"
        self.hips = "Hips"
        # Size Ratio
        if pm.objExists(self.hips):
            bbSize = getBoundingBoxSize(self.hips)
            bbSize = max(bbSize)
            self.sr = round(bbSize/90.4, 3)
        else:
            self.sr = 1
        self.spine = [
            "Spine", 
            "Spine1", 
            "Spine2", 
            "Neck", 
            "Head", 
            "HeadTop_End"
            ]
        self.leftArms = [
            "LeftShoulder", 
            "LeftArm", 
            "LeftForeArm", 
            "LeftHand"
            ]
        self.leftLegs = [
            "LeftUpLeg", 
            "LeftLeg", 
            "LeftFoot", 
            "LeftToeBase", 
            "LeftToe_End"
            ]
        self.leftThumb = [
            "LeftHandThumb1", 
            "LeftHandThumb2", 
            "LeftHandThumb3", 
            "LeftHandThumb4"
            ]
        self.leftIndex = [
            "LeftHandIndex1", 
            "LeftHandIndex2", 
            "LeftHandIndex3", 
            "LeftHandIndex4"
            ]
        self.leftMiddle = [
            "LeftHandMiddle1", 
            "LeftHandMiddle2", 
            "LeftHandMiddle3", 
            "LeftHandMiddle4"
            ]
        self.leftRing = [
            "LeftHandRing1", 
            "LeftHandRing2", 
            "LeftHandRing3", 
            "LeftHandRing4"
            ]
        self.leftPinky = [
            "LeftHandPinky1", 
            "LeftHandPinky2", 
            "LeftHandPinky3", 
            "LeftHandPinky4"
            ]
        self.rightArms = [
            "RightShoulder", 
            "RightArm", 
            "RightForeArm", 
            "RightHand"
            ]
        self.rightLegs = [
            "RightUpLeg", 
            "RightLeg", 
            "RightFoot", 
            "RightToeBase", 
            "RightToe_End"
            ]
        self.rightThumb = [
            "RightHandThumb1", 
            "RightHandThumb2", 
            "RightHandThumb3", 
            "RightHandThumb4"
            ]
        self.rightIndex = [
            "RightHandIndex1", 
            "RightHandIndex2", 
            "RightHandIndex3", 
            "RightHandIndex4"
            ]
        self.rightMiddle = [
            "RightHandMiddle1", 
            "RightHandMiddle2", 
            "RightHandMiddle3", 
            "RightHandMiddle4"
            ]
        self.rightRing = [
            "RightHandRing1", 
            "RightHandRing2", 
            "RightHandRing3", 
            "RightHandRing4"
            ]
        self.rightPinky = [
            "RightHandPinky1", 
            "RightHandPinky2", 
            "RightHandPinky3", 
            "RightHandPinky4"
            ]
        self.jntPosition = {
            "Hips": (0.0, 98.223, 1.464), 
            "Spine": (0.0, 107.814, 1.588), 
            "Spine1": (0.0, 117.134, 0.203), 
            "Spine2": (0.0, 125.82, -1.089), 
            "Neck": (0.0, 141.589, -3.019), 
            "Head": (0.0, 150.649, -1.431), 
            "HeadTop_End": (0.0, 171.409, 5.635), 
            "LeftShoulder": (4.305, 136.196, -3.124), 
            "LeftArm": (19.934, 135.702, -5.494), 
            "LeftForeArm": (42.774, 135.702, -6.376), 
            "LeftHand": (63.913, 135.702, -6.131), 
            "LeftHandThumb1": (65.761, 135.008, -2.444), 
            "LeftHandThumb2": (68.495, 133.652, -0.242), 
            "LeftHandThumb3": (70.727, 132.545, 1.556), 
            "LeftHandThumb4": (72.412, 131.709, 2.913), 
            "LeftHandIndex1": (71.683, 134.879, -2.495), 
            "LeftHandIndex2": (74.972, 134.879, -2.495), 
            "LeftHandIndex3": (77.576, 134.879, -2.495), 
            "LeftHandIndex4": (80.181, 134.879, -2.495), 
            "LeftHandMiddle1": (71.566, 134.682, -4.906), 
            "LeftHandMiddle2": (75.085, 134.762, -4.906), 
            "LeftHandMiddle3": (78.171, 134.832, -4.906), 
            "LeftHandMiddle4": (81.57, 134.908, -4.906), 
            "LeftHandRing1": (71.293, 134.575, -6.84), 
            "LeftHandRing2": (74.241, 134.742, -6.84), 
            "LeftHandRing3": (77.231, 134.912, -6.84), 
            "LeftHandRing4": (80.134, 135.078, -6.84), 
            "LeftHandPinky1": (70.702, 134.116, -8.847), 
            "LeftHandPinky2": (73.811, 134.283, -8.847), 
            "LeftHandPinky3": (75.625, 134.38, -8.847), 
            "LeftHandPinky4": (77.461, 134.478, -8.847), 
            "RightShoulder": (-4.305, 136.196, -3.124), 
            "RightArm": (-21.859, 135.702, -5.585), 
            "RightForeArm": (-42.316, 135.702, -6.381), 
            "RightHand": (-63.913, 135.702, -6.131), 
            "RightHandThumb1": (-65.761, 135.008, -2.444), 
            "RightHandThumb2": (-68.495, 133.652, -0.242), 
            "RightHandThumb3": (-70.727, 132.545, 1.556), 
            "RightHandThumb4": (-72.412, 131.709, 2.913), 
            "RightHandIndex1": (-71.683, 134.879, -2.495), 
            "RightHandIndex2": (-74.972, 134.879, -2.495), 
            "RightHandIndex3": (-77.576, 134.879, -2.495), 
            "RightHandIndex4": (-80.181, 134.879, -2.495), 
            "RightHandMiddle1": (-71.565, 134.682, -4.906), 
            "RightHandMiddle2": (-75.085, 134.762, -4.906), 
            "RightHandMiddle3": (-78.171, 134.832, -4.906), 
            "RightHandMiddle4": (-81.569, 134.908, -4.906), 
            "RightHandRing1": (-71.293, 134.575, -6.84), 
            "RightHandRing2": (-74.24, 134.742, -6.84), 
            "RightHandRing3": (-77.231, 134.912, -6.84), 
            "RightHandRing4": (-80.134, 135.078, -6.84), 
            "RightHandPinky1": (-70.702, 134.116, -8.847), 
            "RightHandPinky2": (-73.811, 134.283, -8.847), 
            "RightHandPinky3": (-75.625, 134.38, -8.847), 
            "RightHandPinky4": (-77.461, 134.478, -8.847), 
            "LeftUpLeg": (10.797, 91.863, -1.849), 
            "LeftLeg": (10.797, 50.067, -0.255), 
            "LeftFoot": (10.797, 8.223, -4.39), 
            "LeftToeBase": (10.797, 0.001, 5.7), 
            "LeftToe_End": (10.797, 0.0, 14.439), 
            "RightUpLeg": (-10.797, 91.863, -1.849), 
            "RightLeg": (-10.797, 50.066, -0.255), 
            "RightFoot": (-10.797, 8.223, -4.39), 
            "RightToeBase": (-10.797, 0.001, 5.7), 
            "RightToe_End": (-10.797, 0.0, 14.439), 
            }
        self.jntHierarchy = {
            "Hips": [self.spine, self.leftLegs, self.rightLegs], 
            "Spine2": [self.leftArms, self.rightArms], 
            "LeftHand": [
                self.leftThumb, 
                self.leftIndex, 
                self.leftMiddle, 
                self.leftRing, 
                self.leftPinky
                ], 
            "RightHand": [
                self.rightThumb, 
                self.rightIndex, 
                self.rightMiddle, 
                self.rightRing, 
                self.rightPinky
                ], 
            }
        super(Character, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()


    def setupUI(self):
        self.setWindowTitle(u"Quick Rig for Character")
        self.move(0, 0)
        self.resize(260, 180)
        font = QFont()
        font.setFamily(u"Courier New")
        self.setFont(font)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnCreateTempJnt = QPushButton()
        self.btnCreateTempJnt.setObjectName(u"btnCreateTempJnt")
        self.verticalLayout.addWidget(self.btnCreateTempJnt)
        self.btnAlignCenterJnt = QPushButton()
        self.btnAlignCenterJnt.setObjectName(u"btnAlignCenterJnt")
        self.verticalLayout.addWidget(self.btnAlignCenterJnt)
        self.btnSynchronizeBothJnt = QPushButton()
        self.btnSynchronizeBothJnt.setObjectName(u"btnSynchronizeBothJnt")
        self.verticalLayout.addWidget(self.btnSynchronizeBothJnt)
        self.fldCreateRigGrp = QLineEdit()
        self.fldCreateRigGrp.setObjectName(u"fldCreateRigGrp")
        self.fldCreateRigGrp.setClearButtonEnabled(True)
        self.verticalLayout.addWidget(self.fldCreateRigGrp)
        self.btnCreateRigGrp = QPushButton()
        self.btnCreateRigGrp.setObjectName(u"btnCreateRigGrp")
        self.verticalLayout.addWidget(self.btnCreateRigGrp)
        self.line = QFrame()
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.btnCreateCtrls = QPushButton()
        self.btnCreateCtrls.setObjectName(u"btnCreateCtrls")
        self.verticalLayout.addWidget(self.btnCreateCtrls)
        self.btnMirrorCopy = QPushButton()
        self.btnMirrorCopy.setObjectName(u"btnMirrorCopy")
        self.verticalLayout.addWidget(self.btnMirrorCopy)
        self.btnRig = QPushButton()
        self.btnRig.setObjectName(u"btnRig")
        self.verticalLayout.addWidget(self.btnRig)
        self.btnClose = QPushButton()
        self.btnClose.setObjectName(u"btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.retranslateUi()
        self.buttonsLink()


    def retranslateUi(self):
        self.btnCreateTempJnt.setText(QCoreApplication.translate("Form", u"Create temp Joints", None))
        self.btnAlignCenterJnt.setText(QCoreApplication.translate("Form", u"Align the Center Joints", None))
        self.btnSynchronizeBothJnt.setText(QCoreApplication.translate("Form", u"Synchronize both Joints", None))
        self.btnCreateRigGrp.setText(QCoreApplication.translate("Form", u"Create Rig Group", None))
        self.btnCreateCtrls.setText(QCoreApplication.translate("Form", u"Create Controllers", None))
        self.btnMirrorCopy.setText(QCoreApplication.translate("Form", u"Mirror Copy Foot Locators", None))
        self.btnRig.setText(QCoreApplication.translate("Form", u"Rig", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"Close", None))


    def buttonsLink(self):
        self.btnCreateTempJnt.clicked.connect(self.createTempJnt)
        self.btnAlignCenterJnt.clicked.connect(self.alignCenterJnt)
        self.btnSynchronizeBothJnt.clicked.connect(self.syncBothJnt)
        self.btnCreateRigGrp.clicked.connect(self.createGroups)
        self.fldCreateRigGrp.returnPressed.connect(self.createGroups)
        self.btnCreateCtrls.clicked.connect(self.createCharCtrl)
        self.btnMirrorCopy.clicked.connect(self.mirrorCopyFootLocator)
        self.btnRig.clicked.connect(self.rig)
        self.btnClose.clicked.connect(self.close)
    

    def createTempJnt(self) -> None:
        """ Create temporary joints. """
        # CleanUp
        temp = list(self.jntPosition.keys())
        temp.append(self.mainCurve)
        self.cleanUp(*temp)
        # Create Joints
        for jnt, pos in self.jntPosition.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        # Set Hierarchy
        self.setHierarchy(self.jntHierarchy)
        # Create Main Curve
        cuv = self.createMainCurve(self.hips)
        pm.parent(self.hips, cuv)


    def alignCenterJnt(self) -> None:
        """ Align the spine line to the center of the grid. """
        self.update()
        temp = self.spine + [self.hips]
        for jnt in temp:
            x, y, z = getPosition(jnt)
            self.jntPosition[jnt] = (0, y, z)
        self.createTempJnt()


    def syncBothJnt(self) -> None:
        """ The Right Joint has a mirror position to the left. """
        self.update()
        leftGroup = []
        leftGroup += self.leftArms
        leftGroup += self.leftLegs
        leftGroup += self.leftIndex
        leftGroup += self.leftMiddle
        leftGroup += self.leftRing
        leftGroup += self.leftPinky
        leftGroup += self.leftThumb
        for i in leftGroup:
            x, y, z = getPosition(i)
            right = changeLeftToRight(i)
            self.jntPosition[right] = (x*-1, y, z)
        self.createTempJnt()


    def createGroups(self):
        groupName = self.fldCreateRigGrp.text()
        if not groupName:
            pm.warning("There is no Rig Group Name in field.")
            return
        else:
            self.update()
            self.createTempJnt()
            groups = createRigGroups(groupName)
            try:
                pm.parent(self.hips, groups[-2])
                pm.delete(self.mainCurve)
            except:
                pass


    def createRigJnt(self) -> None:
        """ To create the rig joint by copying the original joint. """
        if not pm.objExists(self.hips) or pm.objExists("rig_Hips"):
            return
        # Duplicate All.
        result = duplicateObj(self.hips, "rig_", "")
        typ = ["_FK", "_IK"]
        # Delete list after copying
        uselessSpine = []
        uselessSpine += self.spine[3:]
        uselessSpine += self.leftArms[:1]
        uselessSpine += self.rightArms[:1]
        uselessLeftArm = []
        uselessLeftArm += self.leftIndex
        uselessLeftArm += self.leftMiddle
        uselessLeftArm += self.leftRing
        uselessLeftArm += self.leftPinky
        uselessLeftArm += self.leftThumb
        uselessRightArm = []
        uselessRightArm += self.rightIndex
        uselessRightArm += self.rightMiddle
        uselessRightArm += self.rightRing
        uselessRightArm += self.rightPinky
        uselessRightArm += self.rightThumb
        joints = {
            "rig_Spine": uselessSpine, 
            "rig_LeftUpLeg": [], 
            "rig_RightUpLeg": [], 
            "rig_LeftArm": uselessLeftArm, 
            "rig_RightArm": uselessRightArm, 
            }
        # Main process
        for jnt, usl in joints.items():
            for k in typ:
                duplicateObj(jnt, "", k)
                useless = [f"rig_{i}{k}" for k in typ for i in usl]
                self.cleanUp(useless)
        # Final Touch
        try:
            pm.parent(result, "rigBones")
        except:
            pass


    def createCharCtrl(self):
        if not pm.objExists("rig_Hips"):
            self.createRigJnt()
        self.createMainCtrl()
        self.createHipsCtrl()
        self.createSpineCtrl()
        self.createShoulderCtrl()
        self.createArmsCtrl()
        self.createLegsCtrl()
        self.createFingerCtrl()


    def mirrorCopyFootLocator(self):
        locators_L = [
            "loc_LeftHeel_IK", 
            "loc_LeftToe_End_IK", 
            "loc_LeftBankIn_IK", 
            "loc_LeftBankOut_IK", 
            "loc_LeftToeBase_IK_grp", 
            "loc_LeftFoot_IK", 
            ]
        locators_R = [changeLeftToRight(i) for i in locators_L]
        for l, r in zip(locators_L, locators_R):
            x, y, z = pm.xform(l, q=1, ws=1, rp=1)
            pm.move(r, (-1*x, y, z))
        

    def rig(self):
        self.rigMainCtrl()
        self.rigHipsCtrl()
        self.rigSpineCtrl()
        self.rigShoulderCtrl()
        self.rigArmsCtrl()
        self.rigLegsCtrl()
        self.rigFingerCtrl()


    def createMainCtrl(self) -> None:
        """ Create Main Controllers. """
        # Args
        ccMain = "cc_main"
        ccSub = "cc_sub"
        ccSub2 = "cc_sub2"
        nullSpace = "null_worldSpace"
        ctrls = [ccMain, ccSub, ccSub2]
        ccColor = ["yellow", "pink", "red2"]
        ccSize = [70, 58, 50]
        # Check
        if any([pm.objExists(i) for i in ctrls]):
            return
        # Create and Colorize
        for cc, col, scl in zip(ctrls, ccColor, ccSize):
            cuv = pm.circle(nr=(0,1,0), r=scl*self.sr, n=cc, ch=False)[0]
            colorize(cuv, **{col: True})
        ctrlGrp = groupOwnPivot(*ctrls)
        nullGrp = pm.group(em=True, n=nullSpace)
        # Grouping
        parentHierarchically(*ctrlGrp)
        pm.parent(nullGrp, ctrlGrp[-1])


    def createHipsCtrl(self) -> None:
        """ Create Hip's Controllers.

        Process
        -------
        - Args
        - Create Controllers
        - Moving and Grouping
        - Colorize
        - Add Attributes
         """
        # Args
        ccMain = "cc_HipsMain"
        ccSub = "cc_HipsSub"
        ccIKFK = "cc_IKFK"
        nullSpace = "null_rootSpace"
        # Check
        if pm.objExists(ccMain) or pm.objExists(ccSub):
            return
        # Create Controllers
        ctrl = Controllers()
        ccs = ctrl.createControllers(cube=ccMain, arrow4=ccSub, IKFK=ccIKFK)
        nullSpace = pm.group(em=True, n=nullSpace)
        # Move
        pm.scale(ccs[0], (5*self.sr, 0.4*self.sr, 5*self.sr))
        pm.makeIdentity(ccs[0], a=1, s=1, jo=0, n=0, pn=1)
        pm.rotate(ccs[2], (90, 0, 0))
        pm.move(ccs[2], (40*self.sr, 0, 0))
        for i in ccs[1:]:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, t=1, r=1, s=1, jo=0, n=0, pn=1)
        # Grouping
        grp = groupOwnPivot(*ccs)
        pm.makeIdentity(ccs[2], a=1, t=1, jo=0, n=0, pn=1)
        # Main
        ccGroups = parentHierarchically(*grp)
        pm.parent(nullSpace, ccs[1])
        pm.matchTransform(ccGroups[0], self.hips, pos=True)
        # Color
        colorize(ccMain, ccIKFK, yellow=True)
        colorize(ccSub, pink=True)
        # Add Attributes
        attrName = [
            "Spine_IK0_FK1", 
            "Left_Arm_IK0_FK1", 
            "Right_Arm_IK0_FK1", 
            "Left_Leg_IK0_FK1", 
            "Right_Leg_IK0_FK1", 
            ]
        for i in attrName:
            pm.addAttr(ccIKFK, ln=i, at="double", min=0, max=1, dv=0)
            pm.setAttr(f'{ccIKFK}.{i}', e=True, k=True)


    def createSpineCtrl(self) -> None:
        """ Creates Spine, Neck, Head Controllers.

        Process
        -------
        - Create a Spine Curve.
            - cuv_Spine
            - clusters
            - ikHandle
        - Create IK controllers.
        - Create FK controllers. 
        - Create Neck, Head controllers. 
        - Finally,
            - Colorize.
            - Group the IK, FK and Neck together.
         """
        # Create a Spine Curve
        cuvName = "cuv_Spine"
        sp, sp1, sp2 = self.spine[:3]
        ccSp, ccSp2 = addPrefix([sp, sp2], ["cc_"], ["_IK"])
        ccFKs = addPrefix(self.spine[:3], ["cc_"], ["_FK"])
        isExist = [pm.objExists(i) for i in ccFKs + [cuvName, ccSp, ccSp2]]
        if any(isExist):
            return
        # rsp, rsp1, rsp2 = addPrefix(self.spine[:3], ["rig_"], ["_IK"])
        spPos = self.jntPosition[sp]
        sp1Pos = self.jntPosition[sp1]
        sp2Pos = self.jntPosition[sp2]
        cuv = pm.curve(d=3, ep=[spPos, sp1Pos, sp2Pos], n=cuvName)
        # ikH = pm.ikHandle(sj=rsp, ee=rsp2, 
        #                   sol="ikSplineSolver", 
        #                   name=f"ikH_{sp}", 
        #                   curve=cuv, 
        #                   createCurve=0, 
        #                   parentCurve=0, 
        #                   numSpans=3)[0]
        # Create Clusters
        clt1 = pm.cluster(f"{cuv}.cv[:1]", n=f"clt_{sp}")[1]
        clt1Grp = groupOwnPivot(clt1)[0]
        clt2 = pm.cluster(f"{cuv}.cv[2:]", n=f"clt_{sp2}")[1]
        clt2Grp = groupOwnPivot(clt2)[0]
        # Create IK Ctrls
        ctrl = Controllers()
        ccSp = ctrl.createControllers(circle=ccSp)[0]
        pm.scale(ccSp, (1.3*self.sr, 1.3*self.sr, 1.3*self.sr))
        pm.makeIdentity(ccSp, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSp, sp, pos=True)
        pm.parent(clt1Grp, ccSp)
        ccSpGrp = groupOwnPivot(ccSp)
        ccSp2 = ctrl.createControllers(circle=ccSp2)[0]
        pm.scale(ccSp2, (1.5*self.sr, 1.5*self.sr, 1.5*self.sr))
        pm.makeIdentity(ccSp2, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSp2, clt2, pos=True)
        pm.parent(clt2Grp, ccSp2)
        ccSp2Grp = groupOwnPivot(ccSp2)
        parentHierarchically(*ccSpGrp+ccSp2Grp)
        # try:
        #     pm.parent([cuv, ikH], "extraNodes")
        # except:
        #     pass
        # Create FK Ctrls
        FKSize = [17, 18.5, 21]
        createdFK = []
        for ccName, jnt, scl in zip(ccFKs, self.spine[:3], FKSize):
            cc = pm.circle(nr=(0,1,0), r=scl*self.sr, n=ccName, ch=0)[0]
            pm.matchTransform(cc, jnt, pos=True)
            createdFK.append(cc)
        createdFKGrp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFKGrp)
        # Create Neck, Head Ctrls
        ccNeck, ccHead = addPrefix(self.spine[3:5], ["cc_"], [])
        ccNeck = pm.circle(nr=(0,1,0), r=10*self.sr, n=ccNeck, ch=0)[0]
        ccHead = ctrl.createControllers(head=ccHead)[0]
        pm.scale(ccHead, (self.sr, self.sr, self.sr))
        pm.makeIdentity(ccHead, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccNeck, self.spine[3], pos=True)
        pm.matchTransform(ccHead, self.spine[4], pos=True)
        grpNeckHead = groupOwnPivot(ccNeck, ccHead)
        parentHierarchically(*grpNeckHead)
        # Color
        colorize(ccSp, ccSp2, red2=True)
        colorize(*createdFK, blue2=True)
        colorize(ccNeck, ccHead, yellow=True)
        # Grouping
        grpName = "cc_Spine_grp"
        if not pm.objExists("cc_Spine_grp"):
            grpName = pm.group(em=True, n=grpName)
        try:
            for i in [ccSpGrp[0], createdFKGrp[0], grpNeckHead[0]]:
                pm.parent(i, grpName)
        except:
            pass


    def createShoulderCtrl(self) -> None:
        """ Creates a Scapula's Controller.

        Process
        -------
        - Create the names of the controllers.
            - cc_shoulder
        - Finally
            - Colorize.
            - Grouping.
         """
        jntShoulder_L = self.leftArms[0]
        jntShoulder_R = self.rightArms[0]
        ccShoulder_L = "cc_" + jntShoulder_L
        ccShoulder_R = "cc_" + jntShoulder_R
        if pm.objExists(ccShoulder_L) or pm.objExists(ccShoulder_R):
            return
        ctrl = Controllers()
        jntShoulder = [jntShoulder_L, jntShoulder_R]
        ccShoulder = [ccShoulder_L, ccShoulder_R]
        ccSize= 0.8*self.sr
        for jnt, cc in zip(jntShoulder, ccShoulder):
            cc = ctrl.createControllers(scapula=cc)[0]
            pm.scale(cc, (ccSize, ccSize, ccSize))
            rotZ = 135 if "Right" in jnt else -45
            pm.rotate(cc, (0, 0, rotZ))
            pm.makeIdentity(cc, a=1, r=1, s=1, pn=1)
            if "Right" in jnt:
                pm.rotate(cc, (180, 0, 0))
            nullShoulderSpace = f"null_{jnt}Space"
            nullShoulderSpace = pm.group(em=True, n=nullShoulderSpace)
            pm.parent(nullShoulderSpace, cc)
            pm.matchTransform(cc, jnt, pos=True)
            groupOwnPivot(cc)
            # color
            colorBar = {"blue": True} if "Right" in jnt else {"red": True}
            colorize(cc, **colorBar)


    def createArmsCtrl(self) -> None:
        """ Creates a Arm's Controller.

        Process
        -------
        - Create the names of the controllers.
            - cc_shoulder
            - cc_jointName_FK, 
            - cc_jointName_IK
        - Create an FK controller. 
            - If the "Right" joint, rotateX the controller -180 degrees.
        - Create an IK controller.
            - Create a arm controller,
            - Create a poleVector controller.
            - Create a hand controller.
        - Finally,
            - Colorize.
            - Add attributes
            - Group the FK and IK together.
         """
        ctrl = Controllers()
        FKSize = [9.3, 8, 6.8]
        IKSize = [0.75, 0.75, 0.75]
        for joints in [self.leftArms, self.rightArms]:
            jntArm = joints[1:]
            ccArmFK = addPrefix(jntArm, ["cc_"], ["_FK"])
            ccArmIK = addPrefix(jntArm, ["cc_"], ["_IK"])
            isFKExist = any([pm.objExists(i) for i in ccArmFK])
            isIKExist = any([pm.objExists(i) for i in ccArmIK])
            if isFKExist or isIKExist:
                continue
            # Create FK
            createdFK = []
            for cc, jnt, scl in zip(ccArmFK, jntArm, FKSize):
                scl *= self.sr
                cuv = pm.circle(nr=(1,0,0), r=scl, n=cc, ch=False)[0]
                if "Right" in jnt:
                    pm.rotate(cuv, (-180, 0, 0))
                pm.matchTransform(cuv, jnt, pos=True)
                createdFK.append(cuv)
            for idx, cc in enumerate(createdFK):
                flipFactor = -1 if "Right" in jnt else 1
                if (idx+1) < len(createdFK):
                    pm.aimConstraint(createdFK[idx+1], cc, 
                                    aimVector=(flipFactor,0,0), 
                                    upVector=(0,flipFactor,0), 
                                    worldUpType="vector", 
                                    worldUpVector=(0,1,0), 
                                    mo=False, w=1.0
                                    )
                    pm.delete(cc, cn=True)
                elif (idx+1) == len(createdFK):
                    pm.orientConstraint(createdFK[idx-1], cc, mo=False, w=1.0)
                    pm.delete(cc, cn=True)
                else:
                    continue
            grpCreatedFK = groupOwnPivot(*createdFK)
            parentHierarchically(*grpCreatedFK)
            # Create IK
            arm, elbow, hand = jntArm
            cir, sph, cub = ccArmIK
            createdIK = ctrl.createControllers(circle=cir, sphere=sph, cube=cub)
            cir, sph, cub = createdIK
            for i in createdIK:
                pm.scale(i, (self.sr, self.sr, self.sr))
                pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
            # Create IK - Arm
            pm.scale(cir, IKSize)
            pm.rotate(cir, (0, 0, -90))
            pm.makeIdentity(cir, a=1, r=1, s=1, pn=1)
            nullArmSpace = f"null_{arm}Space"
            nullArmSpace = pm.group(em=True, n=nullArmSpace)
            pm.parent(nullArmSpace, cir)
            pm.matchTransform(cir, arm, pos=True)
            cirGrouping = groupOwnPivot(cir)
            # Create IK - ForeArm
            jnt1, jnt2 = createPolevectorJoint(*jntArm)
            pm.matchTransform(sph, jnt2, pos=True)
            sphGrouping = groupOwnPivot(sph)
            pm.delete(jnt1)
            # Create IK - Hand
            nullHandSpace = f"null_{hand}Space"
            nullHandSpace = pm.group(em=True, n=nullHandSpace)
            pm.parent(nullHandSpace, cub)
            pm.matchTransform(cub, hand, pos=True)
            cubGrouping = groupOwnPivot(cub)
            # Colorize
            ctrls = createdFK + createdIK
            colorBar = {"blue": True} if "Right" in jnt else {"red": True}
            colorize(*ctrls, **colorBar)
            # Add Attributes
            attrForeArmIK = "World:Root:Chest:Arm:Hand"
            pm.addAttr(sph, ln="Space", at="enum", en=attrForeArmIK)
            pm.setAttr(f"{sph}.Space", e=True, k=True)
            attrHandIK = "World0_Shoulder1"
            pm.addAttr(cub, ln=attrHandIK, at="double", min=0, max=1, dv=0)
            pm.setAttr(f'{cub}.{attrHandIK}', e=True, k=True)
            # Final Touch
            result = [
                cirGrouping[0], 
                sphGrouping[0], 
                cubGrouping[0], 
                grpCreatedFK[0], 
                ]
            newGroup = "cc_%sArm_grp" % ("Left" if "Left" in arm else "Right")
            pm.group(result, n=newGroup)


    def createLegsCtrl(self) -> None:
        """ Creates a Leg's Controller.

        Process
        -------
        - Create the names of the controllers.
            - cc_jointName_FK, 
            - cc_jointName_IK
        - Create an FK controller. 
            - If the "Right" joint, rotateX the controller 180 degrees.
        - Create an IK controller.
            - Create a pelvis controller,
            - Create a poleVector controller.
            - Create a foot controller.
                - Create locators.
                - Each locator is organized into its own hierarchy.
        - Finally,
            - Colorize.
            - Add attributes
            - Group the FK and IK together.
         """
        ctrl = Controllers()
        FKSize = [13, 10, 9, 7, 1]
        for joints in [self.leftLegs, self.rightLegs]:
            ccLegFK = addPrefix(joints, ["cc_"], ["_FK"])
            ccLegIK = addPrefix(joints, ["cc_"], ["_IK"])
            # Check
            isFKExist = any([pm.objExists(i) for i in ccLegFK])
            isIKExist = any([pm.objExists(i) for i in ccLegIK])
            if isFKExist or isIKExist:
                continue
            # Create FK
            createdFK = []
            for cc, jnt, scl in zip(ccLegFK, joints, FKSize):
                if "Toe_End" in cc:
                    continue
                normalAxis = (0, 0, 1) if "ToeBase" in cc else (0, 1, 0)
                scl *= self.sr
                cuv = pm.circle(nr=normalAxis, r=scl, n=cc, ch=False)[0]
                if "Right" in jnt:
                    pm.rotate(cuv, (180, 0, 0))
                pm.matchTransform(cuv, jnt, pos=True)
                createdFK.append(cuv)
            grpCreatedFK = groupOwnPivot(*createdFK)
            parentHierarchically(*grpCreatedFK)
            # Create IK
            pelvis, knee, foot, ball, toe = joints
            side = "Right" if "Right" in pelvis else "Left"
            sca, sph, cub = ccLegIK[:3]
            createdIK = ctrl.createControllers(scapula=sca, 
                                               sphere=sph, foot2=cub)
            sca, sph, cub = createdIK
            for i in createdIK:
                pm.scale(i, (self.sr, self.sr, self.sr))
                pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
            # Create IK - UpLeg
            rotation = (0, 0, 90) if "Right" == side else (0, 0, -90)
            pm.rotate(sca, rotation)
            pm.scale(sca, (0.9, 0.9, 0.9))
            pm.makeIdentity(sca, a=1, r=1, s=1, pn=1)
            pm.matchTransform(sca, pelvis, pos=True)
            scaGrouping = groupOwnPivot(sca)
            # Create IK - Knee
            jnt1, jnt2 = createPolevectorJoint(*joints[:3])
            pm.matchTransform(sph, jnt2, pos=True)
            sphGrouping = groupOwnPivot(sph)
            pm.delete(jnt1)
            # Create IK - Foot
            locators = [
                f"loc_{side}Heel_IK", 
                f"loc_{side}Toe_End_IK", 
                f"loc_{side}BankIn_IK", 
                f"loc_{side}BankOut_IK", 
                f"loc_{side}ToeBase_IK", 
                f"loc_{side}Foot_IK", 
                ]
            for i in locators:
                pm.spaceLocator(p=(0, 0, 0), n=i)
            groupingOrder = []
            pm.matchTransform(cub, foot, pos=True)
            pm.setAttr(f"{cub}.translateY", 0)
            getPivot = pm.xform(foot, q=True, ws=True, rp=True)
            pm.xform(cub, ws=True, piv=getPivot)
            cubGrouping = groupOwnPivot(cub)
            pm.makeIdentity(cub, a=1, t=1, pn=1)
            groupingOrder.append(cub)
            # locators[0] : heel
            pm.matchTransform(locators[0], foot, pos=True)
            pm.setAttr(f"{locators[0]}.translateY", 0)
            tmp = pm.getAttr(f"{locators[0]}.translateZ") - (8*self.sr)
            pm.setAttr(f"{locators[0]}.translateZ", tmp)
            groupingOrder.append(locators[0])
            # locators[1] : toe
            pm.matchTransform(locators[1], toe, pos=True)
            pm.setAttr(f"{locators[1]}.translateY", 0)
            groupingOrder.append(locators[1])
            # locators[2] : bankIn
            pm.matchTransform(locators[2], ball, pos=True)
            pm.setAttr(f"{locators[2]}.translateY", 0)
            tmp = pm.getAttr(f"{locators[2]}.translateX") - (5*self.sr)
            pm.setAttr(f"{locators[2]}.translateX", tmp)
            groupingOrder.append(locators[2])
            # locators[3] : bankOut
            pm.matchTransform(locators[3], ball, pos=True)
            pm.setAttr(f"{locators[3]}.translateY", 0)
            tmp = pm.getAttr(f"{locators[3]}.translateX") + (5*self.sr)
            pm.setAttr(f"{locators[3]}.translateX", tmp)
            groupingOrder.append(locators[3])
            # locators[4] : ball
            pm.matchTransform(locators[4], ball, pos=True)
            pm.aimConstraint(foot, locators[4], 
                             aimVector=(0,0,-1), 
                             upVector=(0,1,0), 
                             worldUpType="vector", 
                             worldUpVector=(0,1,0), 
                             mo=False, w=1.0
                             )
            pm.delete(locators[4], cn=True)
            groupingOrder += groupOwnPivot(locators[4])
            # locators[5] : ankle
            pm.matchTransform(locators[5], foot, pos=True)
            groupingOrder.append(locators[5])
            # Color
            ctrls = createdFK + createdIK
            colorBar = {"red": True} if "Left" == side else {"blue": True}
            colorize(*ctrls, **colorBar)
            # Add Attributes
            attrLegIK = "World:Root:Hip:Foot"
            pm.addAttr(createdIK[1], ln="Space", at="enum", en=attrLegIK)
            pm.setAttr(f"{createdIK[1]}.Space", e=True, k=True)
            attrFootIK = [
                "Ball_Down", 
                "Ball_Up", 
                "Bank", 
                "Heel_Twist", 
                "Heel_Up", 
                "Toe_Twist", 
                "Toe_Up", 
                ]
            for i in attrFootIK:
                pm.addAttr(createdIK[2], ln=i, at="double", dv=0)
                pm.setAttr(f"{createdIK[2]}.{i}", e=True, k=True)
            attrFootIK2 = "World0_Root1"
            pm.addAttr(cub, ln=attrFootIK2, at="double", min=0, max=1, dv=0)
            pm.setAttr(f'{cub}.{attrFootIK2}', e=True, k=True)
            # Final Touch
            parentHierarchically(*groupingOrder)
            result = [
                scaGrouping[0], 
                sphGrouping[0], 
                cubGrouping[0], 
                grpCreatedFK[0], 
                ]
            pm.group(result, n=f"cc_{side}Leg_grp")


    def createFingerCtrl(self) -> None:
        """ Creates a Finger's Controller.

        Process
        -------
        - Create the names of the controllers from Joint.
        - Colorize.
        - Grouping.
         """
        # Create Names
        jntFinger = []
        jntFinger += self.leftThumb[:-1]
        jntFinger += self.leftIndex[:-1]
        jntFinger += self.leftMiddle[:-1]
        jntFinger += self.leftRing[:-1]
        jntFinger += self.leftPinky[:-1]
        jntFinger += self.rightThumb[:-1]
        jntFinger += self.rightIndex[:-1]
        jntFinger += self.rightMiddle[:-1]
        jntFinger += self.rightRing[:-1]
        jntFinger += self.rightPinky[:-1]
        ccFinger = addPrefix(jntFinger, ["cc_"], [])
        FKSize = [2, 1.6, 1.3]
        # Check
        if any([pm.objExists(i) for i in ccFinger]):
            return
        # Create Ctrls
        for idx, (cc, jnt) in enumerate(zip(ccFinger, jntFinger)):
            scl = FKSize[idx%3]
            cc = pm.circle(nr=(1,0,0), r=scl*self.sr, n=cc, ch=False)[0]
            pm.matchTransform(cc, jnt, pos=True, rot=True)
            tmp = -1 if "Right" in cc.name() else 1
            pm.rotate(cc, (0, 0, tmp*90), r=True, os=True, fo=True)
            pm.rotate(cc, (tmp*-90, 0, 0), r=True, os=True, fo=True)
            # Color
            color = {"blue2": True} if "Right" in cc.name() else {"red2": True}
            colorize(cc, **color)
        # Grouping
        grpFinger = groupOwnPivot(*ccFinger)
        result = []
        for idx, num in enumerate(range(0, len(grpFinger), 6)):
            tmp = parentHierarchically(*grpFinger[num:6*(idx+1)])[0]
            result.append(tmp)
        pm.group(result[:5], n="cc_LeftHandFingers_grp")
        pm.group(result[5:], n="cc_RightHandFingers_grp")
        

    def rigMainCtrl(self):
        pass


    def rigHipsCtrl(self):
        pass


    def rigSpineCtrl(self):
        pass


    def rigShoulderCtrl(self):
        pass


    def rigArmsCtrl(self):
        pass


    def rigLegsCtrl(self):
        for leg in [self.leftLegs, self.rightLegs]:
            side = "Left" if "Left" in leg[0] else "Right"
            jnt = addPrefix(leg, ["rig_"], [])
            jntFK = addPrefix(leg, ["rig_"], ["_FK"])
            jntIK = addPrefix(leg, ["rig_"], ["_IK"])
            ctrlAttr = f"cc_IKFK.{side}_Leg_IK0_FK1"
            # Create IK Handle
            pelvis, knee, foot, ball, toe = jntIK
            ikH_pelvis = createIKHandle(pelvis, foot, rp=True)[0]
            ikH_foot = createIKHandle(foot, ball, sc=True)[0]
            ikH_ball = createIKHandle(ball, toe, sc=True)[0]
            ikH_pelvisGrp = groupOwnPivot(ikH_pelvis)
            pm.parent(ikH_pelvisGrp[0], f"loc_{side}Foot_IK")
            pm.parent(ikH_foot, ikH_pelvisGrp[0])
            ikH_ballGrp = pm.group(em=True, n=f"{ikH_ball}_grp")
            ikH_ballNull = pm.group(em=True, n=f"{ikH_ball}_null")
            pm.parent(ikH_ballNull, ikH_ballGrp)
            pm.matchTransform(ikH_ballGrp, ball, pos=True)
            pm.parent(ikH_ballGrp, f"loc_{side}BankOut_IK")
            pm.parent(ikH_ball, ikH_ballNull)

            
            # Create Blend Color Node
            # createBlendColor(ctrlAttr, jnt, jntFK, jntIK, t=True, r=True)
            # # Connect Foot Attr to Locators
            # ctrl = f"cc_{side}Foot_IK"
            # locHeel = f"loc_{side}Heel_IK"
            # locToe = f"loc_{side}Toe_End_IK"
            # locBankIn = f"loc_{side}BankIn_IK"
            # locBankOut = f"loc_{side}BankOut_IK"
            # locBall = f"loc_{side}ToeBase_IK"
            # grpBall = f"ikH_{side}ToeBase_IK_null"
            # rx, ry, rz = ["rotateX", "rotateY", "rotateZ"]
            # pm.connectAttr(f"{ctrl}.Heel_Up", f"{locHeel}.{rx}", f=1)
            # pm.connectAttr(f"{ctrl}.Heel_Twist", f"{locHeel}.{ry}", f=1)
            # pm.connectAttr(f"{ctrl}.Toe_Up", f"{locToe}.{rx}", f=1)
            # pm.connectAttr(f"{ctrl}.Toe_Twist", f"{locToe}.{ry}", f=1)
            # pm.connectAttr(f"{ctrl}.Ball_Up", f"{locBall}.{rx}", f=1)
            # pm.connectAttr(f"{ctrl}.Ball_Down", f"{grpBall}.{rx}", f=1)
            # clampNode = pm.shadingNode("clamp", au=True)
            # pm.setAttr(f"{clampNode}.minR", -180)
            # pm.setAttr(f"{clampNode}.maxG", 180)
            # output1 = "outputR" if "Left" == side else "outputG"
            # output2 = "outputG" if "Left" == side else "outputR"
            # pm.connectAttr(f"{clampNode}.{output1}", f"{locBankOut}.{rz}", f=1)
            # pm.connectAttr(f"{clampNode}.{output2}", f"{locBankIn}.{rz}", f=1)
            # pm.connectAttr(f"{ctrl}.Bank", f"{clampNode}.inputR", f=1)
            # pm.connectAttr(f"{ctrl}.Bank", f"{clampNode}.inputG", f=1)
            # Connect polevector space


        



    def rigFingerCtrl(self):
        pass


    def update(self) -> None:
        """ Update the joint position. """
        result = {i: getPosition(i) for i in self.jntPosition.keys()}
        self.jntPosition = result


    def cleanUp(self, *args) -> None:
        """ Try to clear every argument. """
        for arg in args:
            isStr = isinstance(arg, str)
            isIter = isinstance(arg, Iterable)
            if not isStr and isIter:
                for i in arg:
                    self.cleanUp(i)
            else:
                try:
                    pm.delete(arg)
                except:
                    pass


    def setHierarchy(self, boneTree: dict) -> None:
        """ Set the hierarchy.
        
        Args
        ----
        boneTree = {
            "Hips": [["Spine", "Spine1"], ["LeftUpLeg", "LeftLeg"], ...], 
            "Spine2": [["LeftShoulder", "LeftArm"], ["RightShoulder", ...]], 
            }
        
        Descriptions
        ------------
        - The Left hand has primaryAxis as 'yxz' and secondaryAxis as 'zdown'.
        - The Right hand has primaryAxis as 'yxz' and secondaryAxis as 'zup'.
        - The Rest have primaryAxis as 'yzx' and secondaryAxis as 'zup'.
         """
        for parents, jointGroup in boneTree.items():
            for joints in jointGroup:
                isLeftArms = any(i in joints[0] for i in self.leftArms)
                isRightArms = any(i in joints[0] for i in self.rightArms)
                if isLeftArms:
                    primaryAxis = 'yxz'
                    secondaryAxis = 'zdown'
                elif isRightArms:
                    primaryAxis = 'yxz'
                    secondaryAxis = 'zup'
                else:
                    primaryAxis = 'yzx'
                    secondaryAxis = 'zup'
                parentHierarchically(*joints)
                orientJoints(*joints, p=primaryAxis, s=secondaryAxis)
                parentHierarchically(parents, joints[0])


    def createMainCurve(self, object: str="") -> str:
        """ Create a circle called "mainCurve". 
        Make it the size of the input object.
         """
        if pm.objExists("mainCurve"):
            return
        else:
            if not object:
                bbSize = 1
            else:
                bbSize = getBoundingBoxSize(object)
                bbSize = max(bbSize)
                self.sr = round(bbSize/90.4, 3)
            result = pm.circle(nr=(0, 1, 0), n="mainCurve", ch=0, r=bbSize)
        return result[0]


if __name__ == "__main__":
    try:
        char.close()
        char.deleteLater()
    except:
        pass
    char = Character()
    char.show()

