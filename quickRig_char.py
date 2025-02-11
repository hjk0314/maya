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
        self.sr = 1 # sizeRatio
        self.mainCurve = "mainCurve"
        self.hips = "Hips"
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
        self.btnConfirm = QPushButton()
        self.btnConfirm.setObjectName(u"btnConfirm")
        self.verticalLayout.addWidget(self.btnConfirm)
        self.line = QFrame()
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.btnDuplicateRigJnt = QPushButton()
        self.btnDuplicateRigJnt.setObjectName(u"btnDuplicateRigJnt")
        self.verticalLayout.addWidget(self.btnDuplicateRigJnt)
        self.line_2 = QFrame()
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.btnCreateCtrls = QPushButton()
        self.btnCreateCtrls.setObjectName(u"btnCreateCtrls")
        self.verticalLayout.addWidget(self.btnCreateCtrls)
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
        self.btnConfirm.setText(QCoreApplication.translate("Form", u"Confirm", None))
        self.btnDuplicateRigJnt.setText(QCoreApplication.translate("Form", u"Duplicate Rig Joints", None))
        self.btnCreateCtrls.setText(QCoreApplication.translate("Form", u"Create Controllers", None))
        self.btnRig.setText(QCoreApplication.translate("Form", u"Rig", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"Close", None))


    def buttonsLink(self):
        self.btnCreateTempJnt.clicked.connect(self.createTempJnt)
        self.btnAlignCenterJnt.clicked.connect(self.alignCenterJnt)
        self.btnSynchronizeBothJnt.clicked.connect(self.syncBothJnt)
        self.btnConfirm.clicked.connect(self.confirm)
        self.btnDuplicateRigJnt.clicked.connect(self.createRigJnt)
        self.btnCreateCtrls.clicked.connect(self.createCharCtrl)
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


    def confirm(self):
        self.update()
        self.createTempJnt()


    def createRigJnt(self) -> None:
        """ To create the rig joint by copying the original joint. """
        if not pm.objExists(self.hips) or pm.objExists("rig_Hips"):
            return
        # Duplicate All.
        result = duplicateObj(self.hips, "rig_", "")
        # Create IK, FK joints.
        handle = ["_FK", "_IK"]
        joints = [
            "rig_LeftUpLeg", 
            "rig_RightUpLeg", 
            "rig_LeftArm", 
            "rig_RightArm"
            ]
        for jnt in joints:
            for h in handle:
                duplicateObj(jnt, "", h)
        # Delete useless joints.
        useless = []
        useless += self.leftIndex
        useless += self.leftMiddle
        useless += self.leftRing
        useless += self.leftPinky
        useless += self.leftThumb
        useless += self.rightIndex
        useless += self.rightMiddle
        useless += self.rightRing
        useless += self.rightPinky
        useless += self.rightThumb
        uselessGrp = [f"rig_{i}{h}" for h in handle for i in useless]
        self.cleanUp(uselessGrp)
        try:
            pm.parent(result, "rigBones")
        except:
            pass


    def rig(self):
        pass


    def createCharCtrl(self):
        if not pm.objExists("rig_Hips"):
            pm.warning("There is no \"rig_Hips\" joint.")
            return
        self.createMainCtrl()
        self.createHipsCtrl()
        self.createLegsCtrl(self.leftLegs)
        self.createLegsCtrl(self.rightLegs)
        self.createShoulderCtrl()
        self.createArmsCtrl(self.leftArms)
        self.createArmsCtrl(self.rightArms)


    def createShoulderCtrl(self):
        jntShoulder_L = self.leftArms[0]
        jntShoulder_R = self.rightArms[0]
        ccShoulder_L = "cc_" + jntShoulder_L
        ccShoulder_R = "cc_" + jntShoulder_R
        if pm.objExists(ccShoulder_L) or pm.objExists(ccShoulder_R):
            return
        ctrl = Controllers()
        jntShoulder = [jntShoulder_L, jntShoulder_R]
        ccShoulder = [ccShoulder_L, ccShoulder_R]
        for jnt, cc in zip(jntShoulder, ccShoulder):
            cc = ctrl.createControllers(scapula=cc)[0]
            pm.scale(cc, (self.sr, self.sr, self.sr))
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


    def createArmsCtrl(self, armJoint: list):
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
        # Create Ctrl Name
        ccArmFK_L = stringConcatenation(self.leftArms[1:], ["cc_"], ["_FK"])
        ccArmIK_L = stringConcatenation(self.leftArms[1:], ["cc_"], ["_IK"])
        ccArmFK_R = stringConcatenation(self.rightArms[1:], ["cc_"], ["_FK"])
        ccArmIK_R = stringConcatenation(self.rightArms[1:], ["cc_"], ["_IK"])
        FKsize = [9.3, 8, 6.8]
        ctrl = Controllers()
        isFKExist = any([pm.objExists(i) for i in ccArmFK_L + ccArmFK_R])
        isIKExist = any([pm.objExists(i) for i in ccArmIK_L + ccArmIK_R])
        if isFKExist or isIKExist:
            return
        # Create Ctrl Name
        # joint = stringConcatenation(armJoint, ["rig_"], [])
        # shoulderJnt = joint[0]
        # ccShoulder = shoulderJnt.replace("rig_", "cc_")
        # rigJnt = joint[1:]
        # cc_FK = stringConcatenation(armJoint[1:], ["cc_"], ["_FK"])
        # cc_IK = stringConcatenation(armJoint[1:], ["cc_"], ["_IK"])
        # side = "Left" if "Left" in shoulderJnt else "Right"
        # size_FK = [9.3, 8, 6.8]
        # ctrl = Controllers()
        # Check
        # Create FK
        createdFK = []
        for cc, rg, scl in zip(cc_FK, rigJnt, size_FK):
            scl *= self.sr
            cuv = pm.circle(nr=(1,0,0), r=scl, n=cc, ch=False)[0]
            if "Right" == side:
                pm.rotate(cuv, (-180, 0, 0))
            pm.matchTransform(cuv, rg, pos=True)
            createdFK.append(cuv)
        for idx, cc in enumerate(createdFK):
            flipFactor = -1 if "Right" == side else 1
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
        createdFK_grp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFK_grp)
        # Create IK
        createdIK = ctrl.createControllers(circle=cc_IK[0], 
                                           sphere=cc_IK[1], cube=cc_IK[2])
        for i in createdIK:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        # Arm_IK
        pm.scale(createdIK[0], (0.75, 0.75, 0.75))
        pm.rotate(createdIK[0], (0, 0, -90))
        pm.makeIdentity(createdIK[0], a=1, r=1, s=1, pn=1)
        nullArmSpace = f"null_{armJoint[1]}Space"
        nullArmSpace = pm.group(em=True, n=nullArmSpace)
        pm.parent(nullArmSpace, createdIK[0])
        pm.matchTransform(createdIK[0], rigJnt[0], pos=True)
        createdIK_grp1 = groupOwnPivot(createdIK[0])
        # ForeArm_IK
        jnt1, jnt2 = createPolevectorJoint(*rigJnt)
        pm.matchTransform(createdIK[1], jnt2, pos=True)
        createdIK_grp2 = groupOwnPivot(createdIK[1])
        pm.delete(jnt1)
        # Hand_IK
        nullHandSpace = f"null_{armJoint[3]}Space"
        nullHandSpace = pm.group(em=True, n=nullHandSpace)
        pm.parent(nullHandSpace, createdIK[2])
        pm.matchTransform(createdIK[2], rigJnt[2], pos=True)
        createdIK_grp3 = groupOwnPivot(createdIK[2])
        # Colorize
        ctrls = createdFK + createdIK
        ctrls.append(ccShoulder)
        colorBar = {"red": True} if "Left" == side else {"blue": True}
        colorize(*ctrls, **colorBar)
        # Add Attributes
        attrLegIK = "World:Root:Chest:Arm:Hand"
        pm.addAttr(createdIK[1], ln="Space", at="enum", en=attrLegIK)
        pm.setAttr(f"{createdIK[1]}.Space", e=True, k=True)
        # Final Touch
        resultGroup = [
            createdIK_grp1[0], 
            createdIK_grp2[0], 
            createdIK_grp3[0], 
            createdFK_grp[0], 
            ]
        pm.group(resultGroup, n=f"cc_{side}Arm_grp")


    def createMainCtrl(self):
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


    def createHipsCtrl(self):
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


    def createLegsCtrl(self, legJoint: list) -> None:
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
        # Create Ctrl names
        joint = stringConcatenation(legJoint, ["rig_"], [])
        cc_FK = stringConcatenation(legJoint, ["cc_"], ["_FK"])
        cc_IK = stringConcatenation(legJoint, ["cc_"], ["_IK"])
        side = "Left" if "Left" in legJoint[0] else "Right"
        size_FK = [13, 10, 9, 7, 1]
        # Check
        isFKExist = any([pm.objExists(i) for i in cc_FK])
        isIKExist = any([pm.objExists(i) for i in cc_IK])
        if isFKExist or isIKExist:
            return
        # Create FK
        createdFK = []
        for cc, rg, scl in zip(cc_FK, joint, size_FK):
            if "Toe_End" in cc:
                continue
            normalAxis = (0, 0, 1) if "ToeBase" in cc else (0, 1, 0)
            scl *= self.sr
            cuv = pm.circle(nr=normalAxis, r=scl, n=cc, ch=False)[0]
            if "Right" == side:
                pm.rotate(cuv, (180, 0, 0))
            pm.matchTransform(cuv, rg, pos=True)
            createdFK.append(cuv)
        createdFK_grp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFK_grp)
        # Create IK
        ctrl = Controllers()
        createdIK = ctrl.createControllers(scapula=cc_IK[0], 
                                           sphere=cc_IK[1], foot2=cc_IK[2])
        for i in createdIK:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        # UpLeg_IK
        rot = -90 if "Left" == side else 90
        pm.rotate(createdIK[0], (0, 0, rot))
        pm.makeIdentity(createdIK[0], a=1, r=1, pn=1)
        pm.matchTransform(createdIK[0], joint[0], pos=True)
        createdIK_grp1 = groupOwnPivot(createdIK[0])
        # Leg_IK
        jnt1, jnt2 = createPolevectorJoint(*joint[:3])
        pm.matchTransform(createdIK[1], jnt2, pos=True)
        createdIK_grp2 = groupOwnPivot(createdIK[1])
        pm.delete(jnt1)
        # Foot_IK
        locs = [
            f"loc_{side}Heel_IK", 
            f"loc_{side}Toe_End_IK", 
            f"loc_{side}BankIn_IK", 
            f"loc_{side}BankOut_IK", 
            f"loc_{side}ToeBase_IK", 
            f"loc_{side}Foot_IK", 
            ]
        for i in locs:
            pm.spaceLocator(p=(0, 0, 0), n=i)
        temp = []
        # createdIK[2]
        pm.matchTransform(createdIK[2], joint[2], pos=True)
        pm.setAttr(f"{createdIK[2]}.translateY", 0)
        getPivot = pm.xform(joint[2], q=True, ws=True, rp=True)
        pm.xform(createdIK[2], ws=True, piv=getPivot)
        createdIK_grp3 = groupOwnPivot(createdIK[2])
        pm.makeIdentity(createdIK[2], a=1, t=1, pn=1)
        temp.append(createdIK_grp3[-1])
        # locs[0] : heel
        pm.matchTransform(locs[0], joint[2], pos=True)
        pm.setAttr(f"{locs[0]}.translateY", 0)
        tmp = pm.getAttr(f"{locs[0]}.translateZ") - (8*self.sr)
        pm.setAttr(f"{locs[0]}.translateZ", tmp)
        temp.append(locs[0])
        # locs[1] : toe
        pm.matchTransform(locs[1], joint[-1], pos=True)
        pm.setAttr(f"{locs[1]}.translateY", 0)
        temp.append(locs[1])
        # locs[2] : bankIn
        pm.matchTransform(locs[2], joint[3], pos=True)
        pm.setAttr(f"{locs[2]}.translateY", 0)
        tmp = pm.getAttr(f"{locs[2]}.translateX") - (5*self.sr)
        pm.setAttr(f"{locs[2]}.translateX", tmp)
        temp.append(locs[2])
        # locs[3] : bankOut
        pm.matchTransform(locs[3], joint[3], pos=True)
        pm.setAttr(f"{locs[3]}.translateY", 0)
        tmp = pm.getAttr(f"{locs[3]}.translateX") + (5*self.sr)
        pm.setAttr(f"{locs[3]}.translateX", tmp)
        temp.append(locs[3])
        # locs[4] : ball
        pm.matchTransform(locs[4], joint[3], pos=True)
        pm.aimConstraint(joint[2], locs[4], 
                         aimVector=(0,0,-1), 
                         upVector=(0,1,0), 
                         worldUpType="vector", 
                         worldUpVector=(0,1,0), 
                         mo=False, w=1.0
                         )
        pm.delete(locs[4], cn=True)
        temp += groupOwnPivot(locs[4])
        # locs[5] : ankle
        pm.matchTransform(locs[5], joint[2], pos=True)
        temp.append(locs[5])
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
        # Final Touch
        parentHierarchically(*temp)
        resultGroup = [
            createdIK_grp1[0], 
            createdIK_grp2[0], 
            createdIK_grp3[0], 
            createdFK_grp[0], 
            ]
        pm.group(resultGroup, n=f"cc_{side}Leg_grp")


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

