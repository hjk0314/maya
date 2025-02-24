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
        self.arms_L = [
            "LeftShoulder", 
            "LeftArm", 
            "LeftForeArm", 
            "LeftHand"
            ]
        self.legs_L = [
            "LeftUpLeg", 
            "LeftLeg", 
            "LeftFoot", 
            "LeftToeBase", 
            "LeftToe_End"
            ]
        self.thumb_L = [
            "LeftHandThumb1", 
            "LeftHandThumb2", 
            "LeftHandThumb3", 
            "LeftHandThumb4"
            ]
        self.index_L = [
            "LeftHandIndex1", 
            "LeftHandIndex2", 
            "LeftHandIndex3", 
            "LeftHandIndex4"
            ]
        self.middle_L = [
            "LeftHandMiddle1", 
            "LeftHandMiddle2", 
            "LeftHandMiddle3", 
            "LeftHandMiddle4"
            ]
        self.ring_L = [
            "LeftHandRing1", 
            "LeftHandRing2", 
            "LeftHandRing3", 
            "LeftHandRing4"
            ]
        self.pinky_L = [
            "LeftHandPinky1", 
            "LeftHandPinky2", 
            "LeftHandPinky3", 
            "LeftHandPinky4"
            ]
        self.arms_R = [
            "RightShoulder", 
            "RightArm", 
            "RightForeArm", 
            "RightHand"
            ]
        self.legs_R = [
            "RightUpLeg", 
            "RightLeg", 
            "RightFoot", 
            "RightToeBase", 
            "RightToe_End"
            ]
        self.thumb_R = [
            "RightHandThumb1", 
            "RightHandThumb2", 
            "RightHandThumb3", 
            "RightHandThumb4"
            ]
        self.index_R = [
            "RightHandIndex1", 
            "RightHandIndex2", 
            "RightHandIndex3", 
            "RightHandIndex4"
            ]
        self.middle_R = [
            "RightHandMiddle1", 
            "RightHandMiddle2", 
            "RightHandMiddle3", 
            "RightHandMiddle4"
            ]
        self.ring_R = [
            "RightHandRing1", 
            "RightHandRing2", 
            "RightHandRing3", 
            "RightHandRing4"
            ]
        self.pinky_R = [
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
            "Hips": [self.spine, self.legs_L, self.legs_R], 
            "Spine2": [self.arms_L, self.arms_R], 
            "LeftHand": [
                self.thumb_L, 
                self.index_L, 
                self.middle_L, 
                self.ring_L, 
                self.pinky_L
                ], 
            "RightHand": [
                self.thumb_R, 
                self.index_R, 
                self.middle_R, 
                self.ring_R, 
                self.pinky_R
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
        leftGroup += self.arms_L
        leftGroup += self.legs_L
        leftGroup += self.index_L
        leftGroup += self.middle_L
        leftGroup += self.ring_L
        leftGroup += self.pinky_L
        leftGroup += self.thumb_L
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
        uselessSpine += self.arms_L[:1]
        uselessSpine += self.arms_R[:1]
        uselessLeftArm = []
        uselessLeftArm += self.index_L
        uselessLeftArm += self.middle_L
        uselessLeftArm += self.ring_L
        uselessLeftArm += self.pinky_L
        uselessLeftArm += self.thumb_L
        uselessRightArm = []
        uselessRightArm += self.index_R
        uselessRightArm += self.middle_R
        uselessRightArm += self.ring_R
        uselessRightArm += self.pinky_R
        uselessRightArm += self.thumb_R
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
        self.update()
        # Check "rig_Hips" Joint
        if not pm.objExists("rig_Hips"):
            self.createRigJnt()
        # Main Ctrl
        self.createMainCtrl()
        # Body
        self.createHipsCtrl()
        self.createSpineCtrl()
        # Shoulders
        for i in [self.arms_L[0], self.arms_R[0]]:
            self.createShoulderCtrl(i)
        # Arms
        for i in [self.arms_L[1:], self.arms_R[1:]]:
            self.createArmsCtrl(i)
        # Legs
        for i in [self.legs_L, self.legs_R]:
            self.createLegsCtrl(i)
        # Fingers
        finger_L = []
        finger_L += self.thumb_L[:-1]
        finger_L += self.index_L[:-1]
        finger_L += self.middle_L[:-1]
        finger_L += self.ring_L[:-1]
        finger_L += self.pinky_L[:-1]
        finger_R = []
        finger_R += self.thumb_R[:-1]
        finger_R += self.index_R[:-1]
        finger_R += self.middle_R[:-1]
        finger_R += self.ring_R[:-1]
        finger_R += self.pinky_R[:-1]
        for i in [finger_L, finger_R]:
            self.createFingerCtrl(i)


    def mirrorCopyFootLocator(self):
        locators_L = [
            "loc_LeftHeel", 
            "loc_LeftToe_End", 
            "loc_LeftBankIn", 
            "loc_LeftBankOut", 
            "loc_LeftToeBase_grp", 
            "loc_LeftFoot", 
            ]
        locators_R = [changeLeftToRight(i) for i in locators_L]
        for l, r in zip(locators_L, locators_R):
            x, y, z = pm.xform(l, q=1, ws=1, rp=1)
            pm.move(r, (-1*x, y, z))
        

    def rig(self):
        self.rigMainCtrl()
        self.rigHipsCtrl()
        self.rigSpineCtrl()
        for i in [self.arms_L[0], self.arms_R[0]]:
            self.rigShoulderCtrl(i)
        for i in [self.arms_L, self.arms_R]:
            self.rigArmsCtrl(i)
        for i in [self.legs_L, self.legs_R]:
            self.rigLegsCtrl(i)
        self.rigFingerCtrl()


    def createMainCtrl(self) -> None:
        """ Create Main Controllers. """
        # Args
        space = "null_worldSpace"
        ctrls = ["cc_main", "cc_sub", "cc_sub2"]
        ccColor = ["yellow", "pink", "red2"]
        ccSize = [70, 58, 50]
        # Check
        if any([pm.objExists(i) for i in ctrls]):
            return
        # Create and Colorize
        for cc, col, scl in zip(ctrls, ccColor, ccSize):
            cuv = pm.circle(nr=(0,1,0), r=scl*self.sr, n=cc, ch=False)[0]
            colorize(cuv, **{col: True})
        ctrls_grp = groupOwnPivot(*ctrls)
        space_grp = pm.group(em=True, n=space)
        # Grouping
        parentHierarchically(*ctrls_grp)
        pm.parent(space_grp, ctrls_grp[-1])


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
        space = "null_rootSpace"
        ccMainSize = [i*self.sr for i in [5, 0.4, 5]]
        attrName = [
            "Spine_IK0_FK1", 
            "Left_Arm_IK0_FK1", 
            "Right_Arm_IK0_FK1", 
            "Left_Leg_IK0_FK1", 
            "Right_Leg_IK0_FK1", 
            ]
        # Check
        if pm.objExists(ccMain) or pm.objExists(ccSub):
            return
        # Create all Ctrls
        ctrl = Controllers()
        ctrls = ctrl.createControllers(cube=ccMain, arrow4=ccSub, IKFK=ccIKFK)
        ccMain, ccSub, ccIKFK = ctrls
        space = pm.group(em=True, n=space)
        pm.scale(ccMain, ccMainSize)
        pm.makeIdentity(ccMain, a=1, s=1, jo=0, n=0, pn=1)
        pm.rotate(ccIKFK, (90, 0, 0))
        pm.move(ccIKFK, (40*self.sr, 0, 0))
        for i in [ccSub, ccIKFK]:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, t=1, r=1, s=1, jo=0, n=0, pn=1)
        # Color
        colorize(ccMain, ccIKFK, yellow=True)
        colorize(ccSub, pink=True)
        # Grouping
        ctrls_grp = groupOwnPivot(*ctrls)
        pm.makeIdentity(ccIKFK, a=1, t=1, jo=0, n=0, pn=1)
        parentHierarchically(*ctrls_grp)
        pm.parent(space, ccSub)
        pm.matchTransform(ctrls_grp[0], self.hips, pos=True)
        # Add Attributes
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
        # Variables
        cuvName = "cuv_Spine"
        finalGroup = "cc_Spine_grp"
        jntSpine0, jntSpine1, jntSpine2 = self.spine[:3]
        jntSpine0Pos = self.jntPosition[jntSpine0]
        jntSpine1Pos = self.jntPosition[jntSpine1]
        jntSpine2Pos = self.jntPosition[jntSpine2]
        ccSpines_IK = addPrefix([jntSpine0, jntSpine2], ["cc_"], ["_IK"])
        ccSpine0_IK, ccSpine2_IK = ccSpines_IK
        ccSpines_FK = addPrefix(self.spine[:3], ["cc_"], ["_FK"])
        jntNeck, jntHead = self.spine[3:5]
        ccNeck, ccHead = addPrefix(self.spine[3:5], ["cc_"], [])
        ccNeckSize = 10*self.sr
        FKSize = [17, 18.5, 21]
        IKSize = [1.3, 1.5]
        ccSpine0Size, ccSpine2Size = [i*self.sr for i in IKSize]
        # Check
        isExist = [pm.objExists(i) for i in ccSpines_FK + ccSpines_IK]
        if any(isExist):
            return
        cuv = pm.curve(d=3, ep=[jntSpine0Pos, jntSpine1Pos, jntSpine2Pos], 
                       n=cuvName)
        # Create Clusters
        clt1 = pm.cluster(f"{cuv}.cv[:1]", n=f"clt_{jntSpine0}")[1]
        clt1_grp = groupOwnPivot(clt1)[0]
        pm.setAttr(f"{clt1_grp}.visibility", 0)
        clt2 = pm.cluster(f"{cuv}.cv[2:]", n=f"clt_{jntSpine2}")[1]
        clt2_grp = groupOwnPivot(clt2)[0]
        pm.setAttr(f"{clt2_grp}.visibility", 0)
        # Create IK Ctrls
        ctrl = Controllers()
        ccSpine0_IK = ctrl.createControllers(circle=ccSpine0_IK)[0]
        pm.scale(ccSpine0_IK, (ccSpine0Size, ccSpine0Size, ccSpine0Size))
        pm.makeIdentity(ccSpine0_IK, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSpine0_IK, jntSpine0, pos=True)
        pm.parent(clt1_grp, ccSpine0_IK)
        ccSpine0_IK_grp = groupOwnPivot(ccSpine0_IK)
        ccSpine2_IK = ctrl.createControllers(circle=ccSpine2_IK)[0]
        pm.scale(ccSpine2_IK, (ccSpine2Size, ccSpine2Size, ccSpine2Size))
        pm.makeIdentity(ccSpine2_IK, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSpine2_IK, clt2, pos=True)
        pm.parent(clt2_grp, ccSpine2_IK)
        ccSpine2_IK_grp = groupOwnPivot(ccSpine2_IK)
        parentHierarchically(*ccSpine0_IK_grp + ccSpine2_IK_grp)
        # Create FK Ctrls
        createdFK = []
        for cc, jnt, scl in zip(ccSpines_FK, self.spine[:3], FKSize):
            cc_FK = pm.circle(nr=(0,1,0), r=scl*self.sr, n=cc, ch=0)[0]
            pm.matchTransform(cc_FK, jnt, pos=True)
            createdFK.append(cc_FK)
        createdFK_grp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFK_grp)
        # Create Neck, Head Ctrls
        ccNeck = pm.circle(nr=(0,1,0), r=ccNeckSize, n=ccNeck, ch=0)[0]
        ccHead = ctrl.createControllers(head=ccHead)[0]
        pm.scale(ccHead, (self.sr, self.sr, self.sr))
        pm.makeIdentity(ccHead, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccNeck, jntNeck, pos=True)
        pm.matchTransform(ccHead, jntHead, pos=True)
        ccNeck_ccHead_grp = groupOwnPivot(ccNeck, ccHead)
        parentHierarchically(*ccNeck_ccHead_grp)
        # Color
        colorize(ccSpine0_IK, ccSpine2_IK, red2=True)
        colorize(*createdFK, blue2=True)
        colorize(ccNeck, ccHead, yellow=True)
        # Grouping
        if not pm.objExists(finalGroup):
            finalGroup = pm.group(em=True, n=finalGroup)
        try:
            temp = [ccSpine0_IK_grp[0], createdFK_grp[0], ccNeck_ccHead_grp[0]]
            for i in temp:
                pm.parent(i, finalGroup)
        except:
            pass


    def createShoulderCtrl(self, shoulderJnt: str) -> None:
        """ Creates a Scapula's Controller.

        Process
        -------
        - Create the names of the controllers.
            - cc_shoulder
        - Finally
            - Colorize.
            - Grouping.
         """
        # Variables
        ccShoulder = "cc_" + shoulderJnt
        ccShoulderSize = (0.8*self.sr, 0.8*self.sr, 0.8*self.sr)
        rotateZ = 135 if "Right" in shoulderJnt else -45
        space = f"null_{shoulderJnt}Space"
        # Check
        if pm.objExists(ccShoulder):
            return
        # Create a Shoulder ctrl
        ctrl = Controllers()
        ccShoulder = ctrl.createControllers(scapula=ccShoulder)[0]
        pm.scale(ccShoulder, ccShoulderSize)
        pm.rotate(ccShoulder, (0, 0, rotateZ))
        pm.makeIdentity(ccShoulder, a=1, r=1, s=1, pn=1)
        if "Right" in shoulderJnt:
            pm.rotate(ccShoulder, (180, 0, 0))
        space = pm.group(em=True, n=space)
        pm.parent(space, ccShoulder)
        pm.matchTransform(ccShoulder, shoulderJnt, pos=True)
        groupOwnPivot(ccShoulder)
        # color
        colorBar = {"blue": True} if "Right" in shoulderJnt else {"red": True}
        colorize(ccShoulder, **colorBar)


    def createArmsCtrl(self, joints: list) -> None:
        """ Creates a Arm's Controller.

        Args
        ----
        - joints : shoulder, elbow, hand
            - Not include scapula joint

        Description
        -----------
        - Create the names of the controllers.
            - cc_shoulder
            - cc_jointName_FK, 
            - cc_jointName_IK
        - Create an FK controller. 
            - If the "Right" joint, rotateX the controller -180 degrees.
        - Create an IK controller.
            - Create a shoulder controller,
            - Create a elbow poleVector controller.
            - Create a hand controller.
        - Finally,
            - Colorize.
            - Add attributes
            - Group the FK and IK together.
         """
        # Variables
        shoulder, elbow, hand = joints
        ccArm_IK = addPrefix(joints, ["cc_"], ["_IK"])
        ccShoulder_IK, ccElbow_IK, ccHand_IK = ccArm_IK
        ccArm_FK = addPrefix(joints, ["cc_"], ["_FK"])
        FKSize = [9.3, 8, 6.8]
        IKSize = [0.75, 0.75, 0.75]
        # Check
        isFKExist = any([pm.objExists(i) for i in ccArm_FK])
        isIKExist = any([pm.objExists(i) for i in ccArm_IK])
        if isFKExist or isIKExist:
            return
        # Create FK
        createdFK = []
        for cc, jnt, scl in zip(ccArm_FK, joints, FKSize):
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
        createdFK_grp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFK_grp)
        # Create IK
        ctrl = Controllers()
        createdIK = ctrl.createControllers(circle=ccShoulder_IK, 
                                           sphere=ccElbow_IK, 
                                           cube=ccHand_IK)
        ccShoulder_IK, ccElbow_IK, ccHand_IK = createdIK
        for i in createdIK:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        # Create IK - Arm
        pm.scale(ccShoulder_IK, IKSize)
        pm.rotate(ccShoulder_IK, (0, 0, -90))
        pm.makeIdentity(ccShoulder_IK, a=1, r=1, s=1, pn=1)
        shoulderSpace = f"null_{shoulder}Space"
        shoulderSpace = pm.group(em=True, n=shoulderSpace)
        pm.parent(shoulderSpace, ccShoulder_IK)
        pm.matchTransform(ccShoulder_IK, shoulder, pos=True)
        ccShoulder_IK_grp = groupOwnPivot(ccShoulder_IK)
        # Create IK - ForeArm
        jnt1, jnt2 = createPolevectorJoint(*joints)
        pm.matchTransform(ccElbow_IK, jnt2, pos=True)
        ccElbow_IK_grp = groupOwnPivot(ccElbow_IK)
        pm.delete(jnt1)
        # Create IK - Hand
        handSpace = f"null_{hand}Space"
        handSpace = pm.group(em=True, n=handSpace)
        pm.parent(handSpace, ccHand_IK)
        pm.matchTransform(ccHand_IK, hand, pos=True)
        ccHand_IK_grp = groupOwnPivot(ccHand_IK)
        # Color
        ctrls = createdFK + createdIK
        colorBar = {"blue": True} if "Right" in jnt else {"red": True}
        colorize(*ctrls, **colorBar)
        # Add Attributes
        attrForeArm_IK = "World:Root:Chest:Arm:Hand"
        pm.addAttr(ccElbow_IK, ln="Space", at="enum", en=attrForeArm_IK)
        pm.setAttr(f"{ccElbow_IK}.Space", e=True, k=True)
        attrHand_IK = "World0_Shoulder1"
        pm.addAttr(ccHand_IK, ln=attrHand_IK, at="double", min=0, max=1, dv=0)
        pm.setAttr(f'{ccHand_IK}.{attrHand_IK}', e=True, k=True)
        # Grouping
        ctrls_grp = [
            ccShoulder_IK_grp[0], 
            ccElbow_IK_grp[0], 
            ccHand_IK_grp[0], 
            createdFK_grp[0], 
            ]
        side = "Left" if "Left" in shoulder else "Right"
        finalGroup = "cc_%sArm_grp" % side
        pm.group(ctrls_grp, n=finalGroup)


    def createLegsCtrl(self, joints: list) -> None:
        """ Creates a Leg's Controller.

        Args
        ----
        - joints
            - ["LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", "LeftToe_End"]

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
        # Variables
        pelvis, knee, foot, ball, toe = joints
        ccLegs_IK = addPrefix(joints, ["cc_"], ["_IK"])
        ccPelvis_IK, ccKnee_IK, ccFoot_IK = ccLegs_IK[:3]
        ccLegs_FK = addPrefix(joints, ["cc_"], ["_FK"])
        FKSize = [13, 10, 9, 7, 1]
        side = "Right" if "Right" in pelvis else "Left"
        locators = [
            f"loc_{side}Heel", 
            f"loc_{side}Toe_End", 
            f"loc_{side}BankIn", 
            f"loc_{side}BankOut", 
            f"loc_{side}ToeBase", 
            f"loc_{side}Foot", 
            ]
        attrLeg_IK = "World:Root:Hip:Foot"
        attrFoot_IK_enum = [
            "Ball_Down", 
            "Ball_Up", 
            "Bank", 
            "Heel_Twist", 
            "Heel_Up", 
            "Toe_Twist", 
            "Toe_Up", 
            ]
        attrFoot_IK_float = "World0_Root1"
        # Check
        isFKExist = any([pm.objExists(i) for i in ccLegs_FK])
        isIKExist = any([pm.objExists(i) for i in ccLegs_IK])
        if isFKExist or isIKExist:
            return
        # Create FK
        createdFK = []
        for cc, jnt, scl in zip(ccLegs_FK, joints, FKSize):
            if "Toe_End" in cc:
                continue
            normalAxis = (0, 0, 1) if "ToeBase" in cc else (0, 1, 0)
            scl *= self.sr
            cuv = pm.circle(nr=normalAxis, r=scl, n=cc, ch=False)[0]
            if "Right" in jnt:
                pm.rotate(cuv, (180, 0, 0))
            pm.matchTransform(cuv, jnt, pos=True)
            createdFK.append(cuv)
        createdFK_grp = groupOwnPivot(*createdFK)
        parentHierarchically(*createdFK_grp)
        # Create IK
        ctrl = Controllers()
        createdIK = ctrl.createControllers(scapula=ccPelvis_IK, 
                                            sphere=ccKnee_IK, foot2=ccFoot_IK)
        ccPelvis_IK, ccKnee_IK, ccFoot_IK = createdIK
        for i in createdIK:
            pm.scale(i, (self.sr, self.sr, self.sr))
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        # IK - UpLeg
        ccPelvisRotation = (0, 0, 90) if "Right" == side else (0, 0, -90)
        pm.rotate(ccPelvis_IK, ccPelvisRotation)
        pm.scale(ccPelvis_IK, (0.9, 0.9, 0.9))
        pm.makeIdentity(ccPelvis_IK, a=1, r=1, s=1, pn=1)
        pm.matchTransform(ccPelvis_IK, pelvis, pos=True)
        # IK - UpLeg space group
        pelvisSpace = pm.group(em=True, n=f"null_{pelvis}Space")
        pm.matchTransform(pelvisSpace, ccPelvis_IK, pos=True)
        pm.parent(pelvisSpace, ccPelvis_IK)
        ccPelvis_IK_grp = groupOwnPivot(ccPelvis_IK)
        # IK - Knee
        jnt1, jnt2 = createPolevectorJoint(*joints[:3])
        pm.matchTransform(ccKnee_IK, jnt2, pos=True)
        ccKnee_IK_grp = groupOwnPivot(ccKnee_IK)
        pm.delete(jnt1)
        # IK - Foot
        for i in locators:
            pm.spaceLocator(p=(0, 0, 0), n=i)
        groupingOrder = []
        pm.matchTransform(ccFoot_IK, foot, pos=True)
        pm.setAttr(f"{ccFoot_IK}.translateY", 0)
        getPivot = pm.xform(foot, q=True, ws=True, rp=True)
        pm.xform(ccFoot_IK, ws=True, piv=getPivot)
        ccFoot_IK_grp = groupOwnPivot(ccFoot_IK)
        pm.makeIdentity(ccFoot_IK, a=1, t=1, pn=1)
        groupingOrder.append(ccFoot_IK)
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
        # foot's space group
        footSpace = pm.group(em=True, n=f"null_{foot}Space")
        pm.matchTransform(footSpace, ccFoot_IK, pos=True)
        pm.parent(footSpace, ccFoot_IK)
        # Color
        ctrls = createdFK + createdIK
        colorBar = {"red": True} if "Left" == side else {"blue": True}
        colorize(*ctrls, **colorBar)
        # Add Attributes
        pm.addAttr(createdIK[1], ln="Space", at="enum", en=attrLeg_IK)
        pm.setAttr(f"{createdIK[1]}.Space", e=True, k=True)
        for i in attrFoot_IK_enum:
            pm.addAttr(createdIK[2], ln=i, at="double", dv=0)
            pm.setAttr(f"{createdIK[2]}.{i}", e=True, k=True)
        pm.addAttr(ccFoot_IK, ln=attrFoot_IK_float, at="double", min=0, max=1, dv=0)
        pm.setAttr(f'{ccFoot_IK}.{attrFoot_IK_float}', e=True, k=True)
        # Final Touch
        parentHierarchically(*groupingOrder)
        finalGroup = [
            ccPelvis_IK_grp[0], 
            ccKnee_IK_grp[0], 
            ccFoot_IK_grp[0], 
            createdFK_grp[0], 
            ]
        pm.group(finalGroup, n=f"cc_{side}Leg_grp")


    def createFingerCtrl(self, joints: list) -> None:
        """ Creates a Finger's Controller.

        Args
        ----
        - joints
            - ["LeftHandThumb1", "LeftHandThumb2", "LeftHandThumb3"]
            - ["LeftHandIndex1", "LeftHandIndex2", "LeftHandIndex3"]

        Process
        -------
        - Create the names of the controllers from Joint.
        - Colorize.
        - Grouping.
         """
        # Variables
        ccFinger = addPrefix(joints, ["cc_"], [])
        ccFingerSize = [2, 1.6, 1.3]
        # Check
        if any([pm.objExists(i) for i in ccFinger]):
            return
        # Create Ctrls
        for idx, (cc, jnt) in enumerate(zip(ccFinger, joints)):
            scl = ccFingerSize[idx%3]
            cc = pm.circle(nr=(1,0,0), r=scl*self.sr, n=cc, ch=0)[0]
            pm.matchTransform(cc, jnt, pos=True, rot=True)
            rot = -1 if "Right" in cc.name() else 1
            pm.rotate(cc, (0, 0, rot*90), r=True, os=True, fo=True)
            pm.rotate(cc, (rot*-90, 0, 0), r=True, os=True, fo=True)
            # Color
            color = {"blue2": True} if "Right" in cc.name() else {"red2": True}
            colorize(cc, **color)
        # Grouping
        ccFinger_grp = groupOwnPivot(*ccFinger)
        temp = []
        for idx, num in enumerate(range(0, len(ccFinger_grp), 6)):
            tmp = parentHierarchically(*ccFinger_grp[num:6*(idx+1)])[0]
            temp.append(tmp)
        for i in temp:
            side = "Left" if "Left" in i.name() else "Right"
            finalGroup = f"cc_{side}HandFingers_grp"
            if pm.objExists(finalGroup):
                pm.parent(i, finalGroup)
            else:
                pm.group(i, n=finalGroup)
        

    def rigMainCtrl(self):
        pass


    def rigHipsCtrl(self):
        # Variables
        ccSub2 = "cc_sub2"
        ccHipsMain_grp = "cc_HipsMain_grp"
        ccHipsSub = "cc_HipsSub"
        rgHipsJnt = "rig_Hips"
        # cc_sub2 -> rig_Hips
        pm.parentConstraint(ccSub2, ccHipsMain_grp, mo=True, w=1)
        pm.scaleConstraint(ccSub2, ccHipsMain_grp, mo=True, w=1)
        # cc_HipsSub -> rig_Hips
        pm.parentConstraint(ccHipsSub, rgHipsJnt, mo=True, w=1)


    def rigSpineCtrl(self) -> None:
        # Variables
        ccHipsSub = "cc_HipsSub"
        cuvName = "cuv_Spine"
        ccIKFK = "cc_IKFK.Spine_IK0_FK1"
        spineJnt = self.spine[:3]
        ikhName = f"ikh_{spineJnt[0]}"
        neckJnt = self.spine[3:5]
        rgSpineJnt = addPrefix(spineJnt, ["rig_"], [])
        rgSpineJnt_IK = addPrefix(spineJnt, ["rig_"], ["_IK"])
        rgSpineJnt_FK = addPrefix(spineJnt, ["rig_"], ["_FK"])
        ccSpine_IK = addPrefix(spineJnt, ["cc_"], ["_IK"])
        ccSpine_IK_grp = f"{ccSpine_IK[0]}_grp"
        ccSpine_FK = addPrefix(spineJnt, ["cc_"], ["_FK"])
        ccSpine_FK_grp = f"{ccSpine_FK[0]}_grp"
        rgNeckJnt = addPrefix(neckJnt, ["rig_"], [])
        ccNeck = addPrefix(neckJnt, ["cc_"], [])
        ccNeck_grp = f"{ccNeck[0]}_grp"
        # Check
        isIKHandle = pm.objExists(ikhName)
        if isIKHandle:
            if "ikHandle" == pm.objectType(ikhName):
                return
        # Create IK Ctrls
        ikHandle = pm.ikHandle(sj=rgSpineJnt_IK[0], ee=rgSpineJnt_IK[2], 
                          sol="ikSplineSolver", 
                          name=ikhName, 
                          curve=cuvName, 
                          createCurve=0, 
                          parentCurve=0, 
                          numSpans=3)
        ikHandle = ikHandle[0]
        pm.connectAttr(f"{ccSpine_IK[0]}.rotateY", f"{ikHandle}.roll", f=1)
        pm.connectAttr(f"{ccSpine_IK[2]}.rotateY", f"{ikHandle}.twist", f=1)
        # Create FK Ctrls
        for cc, jnt in zip(ccSpine_FK, rgSpineJnt_FK):
            pm.parentConstraint(cc, jnt, mo=True, w=1)
        # Connect : FK, IK -> BlendColor -> Original
        createBlendColor(ccIKFK, 
                         rgSpineJnt, rgSpineJnt_FK, rgSpineJnt_IK, 
                         t=True, r=True)
        # Create Neck Ctrls
        for cc, jnt in zip(ccNeck, rgNeckJnt):
            pm.parentConstraint(cc, jnt, mo=True, w=1)
        # Setting Visibility
        pm.connectAttr(ccIKFK, f"{ccSpine_FK_grp}.visibility", f=1)
        rev = pm.shadingNode("reverse", au=True)
        pm.connectAttr(ccIKFK, f"{rev}.inputX", f=1)
        pm.connectAttr(f"{rev}.outputX", f"{ccSpine_IK_grp}.visibility", f=1)
        # Constraint
        pm.parentConstraint(ccHipsSub, ccSpine_IK_grp, mo=True, w=1)
        pm.parentConstraint(ccHipsSub, ccSpine_FK_grp, mo=True, w=1)
        pm.parentConstraint(rgSpineJnt[-1], ccNeck_grp, mo=True, w=1)


    def rigShoulderCtrl(self, joint: str):
        # Variables
        side = "Left" if "Left" in joint else "Right"
        shoulderSpace = f"null_{side}ShoulderSpace"
        rgShoulder = "rig_" + joint
        ccShoulder_grp = "cc_" + joint + "_grp"
        rgSpine2 = "rig_" + self.spine[2]
        # Constraint
        pm.parentConstraint(shoulderSpace, rgShoulder, mo=True, w=1)
        pm.parentConstraint(rgSpine2, ccShoulder_grp, mo=True, w=1)


    def rigArmsCtrl(self, joints: list):
        # Variables
        jntArms = self.arms_L
        ccArms_IK = addPrefix(jntArms, ["cc_"], ["_IK"])
        rgArms_IK = addPrefix(jntArms, ["rig_"], ["_IK"])
        ccScapula_IK, ccShoulder_IK, ccElbow_IK, ccHand_IK = ccArms_IK
        rgScapula_IK, rgShoulder_IK, rgElbow_IK, rgHand_IK = rgArms_IK
        ccArms_FK = addPrefix(jntArms, ["cc_"], ["_FK"])
        # Check
        # Create IK Ctrls
        ikHandle = createIKHandle(rgShoulder_IK, rgHand_IK, rp=True)
        # Create FK Ctrls
        # Setting Visibility
        # Constraint


    def rigLegsCtrl(self, joints: list) -> None:
        # Variables
        side = "Left" if "Left" in joints[0] else "Right"
        locHeel = f"loc_{side}Heel"
        locToe = f"loc_{side}Toe_End"
        locBankIn = f"loc_{side}BankIn"
        locBankOut = f"loc_{side}BankOut"
        locBall = f"loc_{side}ToeBase"
        locFoot = f"loc_{side}Foot"
        ccSub = "cc_HipsSub"
        ccIKFK = f"cc_IKFK.{side}_Leg_IK0_FK1"
        footMenu = {
            "World0": "null_worldSpace", 
            "Root1": "null_rootSpace", 
            }
        legMenu = {
            "World": "null_worldSpace", 
            "Root": "null_rootSpace", 
            "Hip": f"null_{side}UpLegSpace", 
            "Foot": f"null_{side}FootSpace", 
            }
        rx, ry, rz = ["rotateX", "rotateY", "rotateZ"]
        rgLegsJnt = addPrefix(joints, ["rig_"], [])
        rgLegsJnt_FK = addPrefix(joints, ["rig_"], ["_FK"])
        rgLegsJnt_IK = addPrefix(joints, ["rig_"], ["_IK"])
        rgPelvisJnt, rgKneeJnt, rgFootJnt, rgBallJnt, rgToeJnt = rgLegsJnt_IK
        ccLegs_IK = addPrefix(joints, ["cc_"], ["_IK"])
        ccPelvis_IK, ccKnee_IK, ccFoot_IK = ccLegs_IK[:3]
        ccPelvis_IK_grp = f"{ccPelvis_IK}_grp"
        ccKnee_IK_grp = f"{ccKnee_IK}_grp"
        ccFoot_IK_grp = f"{ccFoot_IK}_grp"
        ccLegs_FK = addPrefix(joints, ["cc_"], ["_FK"])
        ccPelvis_FK_grp = f"{ccLegs_FK[0]}_grp"
        # Check
        isIKHandle = pm.listConnections(rgFootJnt, type="ikHandle")
        if isIKHandle:
            return
        # Create IK Ctrl - UpLeg
        pm.pointConstraint(ccPelvis_IK, rgPelvisJnt, mo=True, w=1)
        # Create IK Ctrl - ikHandle
        ikhPelvis = createIKHandle(rgPelvisJnt, rgFootJnt, rp=True)[0]
        ikhFoot = createIKHandle(rgFootJnt, rgBallJnt, sc=True)[0]
        ikhBall = createIKHandle(rgBallJnt, rgToeJnt, sc=True)[0]
        ikhPelvis_grp = groupOwnPivot(ikhPelvis)[0]
        pm.parent(ikhPelvis_grp, locFoot)
        pm.parent(ikhFoot, ikhPelvis_grp)
        ikhBall_grp = groupOwnPivot(ikhBall, null=True)
        rgBallJnt_pos = pm.xform(rgBallJnt, q=True, ws=True, rp=True)
        for idx, i in enumerate(ikhBall_grp):
            if idx == 0:
                pm.parent(i, locBankOut)
            if i != ikhBall:
                pm.xform(i, ws=True, piv=rgBallJnt_pos)
        # Create IK Ctrl - Connect blendColorNode
        createBlendColor(ccIKFK, 
                         rgLegsJnt, rgLegsJnt_FK, rgLegsJnt_IK, 
                         t=True, r=True)
        # Create IK Ctrl - Connect Foot's Attr
        pm.connectAttr(f"{ccFoot_IK}.Heel_Up", f"{locHeel}.{rx}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Heel_Twist", f"{locHeel}.{ry}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Toe_Up", f"{locToe}.{rx}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Toe_Twist", f"{locToe}.{ry}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Ball_Up", f"{locBall}.{rx}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Ball_Down", f"{ikhBall_grp[1]}.{rx}", f=1)
        clampNode = pm.shadingNode("clamp", au=True)
        pm.setAttr(f"{clampNode}.minR", -180)
        pm.setAttr(f"{clampNode}.maxG", 180)
        pm.connectAttr(f"{clampNode}.outputR", f"{locBankOut}.{rz}", f=1)
        pm.connectAttr(f"{clampNode}.outputG", f"{locBankIn}.{rz}", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Bank", f"{clampNode}.inputR", f=1)
        pm.connectAttr(f"{ccFoot_IK}.Bank", f"{clampNode}.inputG", f=1)
        connectSpace(ccFoot_IK, footMenu, float=True)
        # Create IK Ctrl - polevector
        pm.poleVectorConstraint(ccKnee_IK, ikhPelvis, w=1)
        ano = createAnnotation(rgKneeJnt, ccKnee_IK)
        anoGrp = groupOwnPivot(ano)
        pm.parentConstraint(rgKneeJnt, anoGrp[0], mo=True, w=1)
        connectSpace(ccKnee_IK, legMenu, enum=True)
        # Create FK Ctrl
        for cc, jnt in zip(ccLegs_FK, rgLegsJnt_FK):
            try:
                pm.parentConstraint(cc, jnt, mo=True, w=1)
            except:
                continue
        # Setting Visibility
        pm.connectAttr(ccIKFK, f"{ccPelvis_FK_grp}.visibility", f=1)
        revNode = pm.shadingNode("reverse", au=True)
        pm.connectAttr(ccIKFK, f"{revNode}.inputX", f=1)
        for i in [ccPelvis_IK_grp, ccKnee_IK_grp, ccFoot_IK_grp]:
            pm.connectAttr(f"{revNode}.outputX", f"{i}.visibility", f=1)
        pm.setAttr(f"{locHeel}.visibility", 0)
        # Grouping
        for i in [ccPelvis_IK_grp, ccPelvis_FK_grp]:
            pm.parentConstraint(ccSub, i, mo=True, w=1)


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
                isLeftArms = any(i in joints[0] for i in self.arms_L)
                isRightArms = any(i in joints[0] for i in self.arms_R)
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

