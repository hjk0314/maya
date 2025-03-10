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
        self.defaultSize = 90.4
        self.mainCurve = "mainCurve"
        self.jntHips = "Hips"
        self.rgHips = "rig_Hips"
        self.rgSpine2 = "rig_Spine2"
        self.worldSpace = "null_worldSpace"
        self.rootSpace = "null_rootSpace"
        self.mainCtrls = ["cc_main", "cc_sub", "cc_sub2"]
        self.groupNames = [
            'MODEL', 
            'controllers', 
            'skeletons', 
            'geoForBind', 
            'extraNodes', 
            'bindBones', 
            'rigBones'
            ]
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
        self.arms_R = [
            "RightShoulder", 
            "RightArm", 
            "RightForeArm", 
            "RightHand"
            ]
        self.legs_L = [
            "LeftUpLeg", 
            "LeftLeg", 
            "LeftFoot", 
            "LeftToeBase", 
            "LeftToe_End"
            ]
        self.legs_R = [
            "RightUpLeg", 
            "RightLeg", 
            "RightFoot", 
            "RightToeBase", 
            "RightToe_End"
            ]
        self.thumb_L = [f"LeftHandThumb{i}" for i in range(1, 5)]
        self.index_L = [f"LeftHandIndex{i}" for i in range(1, 5)]
        self.middle_L = [f"LeftHandMiddle{i}" for i in range(1, 5)]
        self.ring_L = [f"LeftHandRing{i}" for i in range(1, 5)]
        self.pinky_L = [f"LeftHandPinky{i}" for i in range(1, 5)]
        self.finger_L = self.thumb_L + self.index_L + self.middle_L + self.ring_L + self.pinky_L
        self.thumb_R = [f"RightHandThumb{i}" for i in range(1, 5)]
        self.index_R = [f"RightHandIndex{i}" for i in range(1, 5)]
        self.middle_R = [f"RightHandMiddle{i}" for i in range(1, 5)]
        self.ring_R = [f"RightHandRing{i}" for i in range(1, 5)]
        self.pinky_R = [f"RightHandPinky{i}" for i in range(1, 5)]
        self.finger_R = self.thumb_R + self.index_R + self.middle_R + self.ring_R + self.pinky_R
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
        self.btnCreateRigGrp.setEnabled(False)
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
        self.btnConnect = QPushButton()
        self.btnConnect.setObjectName(u"btnConnect")
        self.verticalLayout.addWidget(self.btnConnect)
        self.btnDisconnect = QPushButton()
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.verticalLayout.addWidget(self.btnDisconnect)
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
        self.btnConnect.setText(QCoreApplication.translate("Form", u"Connect", None))
        self.btnDisconnect.setText(QCoreApplication.translate("Form", u"Disconnect", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"Close", None))


    def buttonsLink(self):
        self.btnCreateTempJnt.clicked.connect(self.createTempJoints)
        self.btnAlignCenterJnt.clicked.connect(self.alignCenterJnt)
        self.btnSynchronizeBothJnt.clicked.connect(self.syncBothJnt)
        self.btnCreateRigGrp.clicked.connect(self.createGroups)
        self.fldCreateRigGrp.textChanged.connect(self.buttonUnlock)
        self.fldCreateRigGrp.returnPressed.connect(self.createGroups)
        self.btnCreateCtrls.clicked.connect(self.createCharCtrl)
        self.btnMirrorCopy.clicked.connect(self.mirrorCopyFootLocator)
        self.btnRig.clicked.connect(self.rig)
        # self.btnConnect.clicked.connect(self.connectBones)
        # self.btnDisconnect.clicked.connect(self.disConnectBones)
        self.btnClose.clicked.connect(self.close)


    def createTempJoints(self) -> None:
        """ Create temporary joints. """
        # CleanUp
        joints = self.jntPosition.keys()
        joints = list(joints)
        self.cleanUp(*joints, self.mainCurve)
        # Create Joints
        for jnt, pos in self.jntPosition.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        self.setHierarchy(self.jntHierarchy)
        # Create Main Curve
        bbSize = self.getDefaultSize(self.jntHips)
        bbSize = bbSize[0]
        pm.circle(nr=(0, 1, 0), n=self.mainCurve, ch=0, r=bbSize)
        try:
            pm.parent(self.jntHips, self.mainCurve)
        except:
            pass


    def alignCenterJnt(self) -> None:
        """ Align the spine line to the center of the grid. """
        self.update()
        temp = []
        temp.append(self.jntHips)
        temp += self.spine
        for jnt in temp:
            x, y, z = getPosition(jnt)
            self.jntPosition[jnt] = (0, y, z)
        self.createTempJoints()


    def syncBothJnt(self) -> None:
        """ The Right Joint has a mirror position to the left. """
        self.update()
        leftSide = []
        leftSide += self.arms_L
        leftSide += self.legs_L
        leftSide += self.index_L
        leftSide += self.middle_L
        leftSide += self.ring_L
        leftSide += self.pinky_L
        leftSide += self.thumb_L
        for i in leftSide:
            x, y, z = getPosition(i)
            rightSide = changeLeftToRight(i)
            self.jntPosition[rightSide] = (x*-1, y, z)
        self.createTempJoints()


    def createGroups(self):
        self.update()
        self.createTempJoints()
        createdGroup = createRigGroups(self.fldCreateRigGrp.text())
        if pm.objExists(self.jntHips):
            pm.parent(self.jntHips, createdGroup[-2])
        if pm.objExists(self.rgHips):
            pm.parent(self.rgHips, createdGroup[-1])


    def createCharCtrl(self):
        self.update()
        if not pm.objExists(self.rgHips):
            self.createRigJnt()
        # Run
        g1 = self.createMainCtrl()
        g2 = self.createHipsCtrl()
        g3 = self.createSpineCtrl()
        g4 = self.createShoulderCtrl(self.arms_L[0])
        g5 = self.createShoulderCtrl(self.arms_R[0])
        g6 = self.createArmsCtrl(self.arms_L[1:])
        g7 = self.createArmsCtrl(self.arms_R[1:])
        g8 = self.createLegsCtrl(self.legs_L)
        g9 = self.createLegsCtrl(self.legs_R)
        g10 = self.createFingerCtrl(self.finger_L)
        g11 = self.createFingerCtrl(self.finger_R)
        results = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11]
        try:
            pm.parent(results, self.groupNames[1])
        except:
            pass


    def mirrorCopyFootLocator(self) -> None:
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
        self.rigShoulderCtrl(self.arms_L[0])
        self.rigShoulderCtrl(self.arms_R[0])
        self.rigArmsCtrl(self.arms_L[1:])
        self.rigArmsCtrl(self.arms_R[1:])
        self.rigLegsCtrl(self.legs_L)
        self.rigLegsCtrl(self.legs_R)
        self.rigFingerCtrl(self.finger_L)
        self.rigFingerCtrl(self.finger_R)
        self.finalTouch()


# ==============================================================================


    def createRigJnt(self) -> None:
        """ To create the rig joint by copying the original joint. """
        if not pm.objExists(self.jntHips):
            return
        rigJoints = duplicateRange(self.jntHips, "", "rig_", "")
        rgHips = rigJoints[0]
        try:
            pm.parent(rgHips, self.groupNames[-1])
        except:
            pass
        startEndJoint = {
            rigJoints[11]: rigJoints[13],   # rig_Spine: rig_Spine2
            rigJoints[6]: "",               # rig_LeftUpLeg: ""
            rigJoints[1]: "",               # rig_RightUpLeg: ""
            rigJoints[39]: rigJoints[41],   # rig_LeftArm: rig_LeftHand
            rigJoints[15]: rigJoints[17],   # rig_RightArm: rig_RightHand
            }
        types = ["_FK", "_IK"]
        for start, end in startEndJoint.items():
            for typ in types:
                duplicateRange(start, end, "", typ)


# ==============================================================================

    def createMainCtrl(self) -> str:
        """ Create Main Controllers. """
        ctrlSize = [70, 58, 50]
        ctrlColor = ["yellow", "pink", "red2"]
        scaleRatio = self.getDefaultSize(self.jntHips)[-1]
        if any([pm.objExists(i) for i in self.mainCtrls]):
            return
        for cc, scl, color in zip(self.mainCtrls, ctrlSize, ctrlColor):
            cuv = pm.circle(nr=(0, 1, 0), r=scl*scaleRatio, n=cc, ch=False)
            cuv = cuv[0]
            colorize(cuv, **{color: True})
        ctrls_grp = groupOwnPivot(*self.mainCtrls)
        ctrls_grp = parentHierarchically(*ctrls_grp)
        nullSpace = pm.group(em=True, n=self.worldSpace)
        pm.parent(nullSpace, ctrls_grp[-1])
        return ctrls_grp[0]


    def createHipsCtrl(self) -> str:
        """ Create Hip's Controllers.

        Process
        -------
        - Variables
        - Create Controllers
        - Colorize
        - Add Attributes
         """
        # Variables
        ccMain = "cc_%sMain" % self.jntHips
        ccSub = "cc_%sSub" % self.jntHips
        ccIKFK = "cc_IKFK"
        ccMain_size = [5, 0.4, 5]
        scaleRatio = self.getDefaultSize(self.jntHips)[-1]
        attrName = [
            "Spine_IK0_FK1", 
            "Left_Arm_IK0_FK1", 
            "Right_Arm_IK0_FK1", 
            "Left_Leg_IK0_FK1", 
            "Right_Leg_IK0_FK1", 
            ]
        # Run
        if pm.objExists(ccMain):
            return
        ctrl = Controllers()
        ctrls = ctrl.createControllers(cube=ccMain, arrow4=ccSub, IKFK=ccIKFK)
        ccMain, ccSub, ccIKFK = ctrls
        pm.scale(ccMain, (i*scaleRatio for i in ccMain_size))
        pm.makeIdentity(ccMain, a=1, s=1, jo=0, n=0, pn=1)
        pm.rotate(ccIKFK, (90, 0, 0))
        pm.move(ccIKFK, (40*scaleRatio, 0, 0))
        for i in [ccSub, ccIKFK]:
            pm.scale(i, (scaleRatio, scaleRatio, scaleRatio))
            pm.makeIdentity(i, a=1, t=1, r=1, s=1, jo=0, n=0, pn=1)
        ctrls_grp = groupOwnPivot(*ctrls)
        ctrls_grp = parentHierarchically(*ctrls_grp)
        nullSpace = pm.group(em=True, n=self.rootSpace)
        pm.parent(nullSpace, ccSub)
        pm.matchTransform(ctrls_grp[0], self.jntHips, pos=True)
        pm.makeIdentity(ccIKFK, a=1, t=1, jo=0, n=0, pn=1)
        # Color
        colorize(ccMain, ccIKFK, yellow=True)
        colorize(ccSub, pink=True)
        # Add Attributes
        for i in attrName:
            pm.addAttr(ccIKFK, ln=i, at="double", min=0, max=1, dv=0)
            pm.setAttr(f'{ccIKFK}.{i}', e=True, k=True)
        return ctrls_grp[0]


    def createSpineCtrl(self) -> str:
        """ Creates Spine, Neck, Head Controllers.

        Process
        -------
        - Declaring variables.
        - Create Spine IK controllers.
        - Create Spine FK controllers. 
        - Create Neck, Head controllers. 
        - Finally,
            - Colorize.
            - Grouping.
         """
        # Variables
        joints = {i: self.jntPosition[i] for i in self.spine[:3]}
        spine0, spine1, spine2 = joints.keys()
        spineCurve = "cuv_%s" % spine0
        finalGroup = "cc_%s_grp" % spine0
        ccSpines_IK = addPrefix(self.spine[:3:2], ["cc_"], ["_IK"])
        ccSpines_FK = addPrefix(self.spine[:3], ["cc_"], ["_FK"])
        ccNeck, ccHead = addPrefix(self.spine[3:5], ["cc_"], [])
        ccSpine0_IK, ccSpine2_IK = ccSpines_IK
        neck, head = self.spine[3:5]
        scaleRatio = self.getDefaultSize(self.jntHips)[1]
        ccSpine0_IKSize = (1.3*scaleRatio, ) * 3
        ccSpine2_IKSize = (1.5*scaleRatio, ) * 3
        FKSize = [i*scaleRatio for i in [17, 18.5, 21]]
        ccNeckSize = 10 * scaleRatio
        ccHeadSize = (scaleRatio, ) * 3
        # Run
        isExist = [pm.objExists(i) for i in ccSpines_FK + ccSpines_IK]
        if any(isExist):
            return
        # IK
        spineCurve = pm.curve(d=3, ep=list(joints.values()), n=spineCurve)
        pm.setAttr(f"{spineCurve}.visibility", 0)
        try:    pm.parent(spineCurve, self.groupNames[4])
        except: pass
        clt1 = pm.cluster(f"{spineCurve}.cv[:1]", n=f"clt_{spine0}")[1]
        clt1_grp = groupOwnPivot(clt1)[0]
        pm.setAttr(f"{clt1_grp}.visibility", 0)
        clt2 = pm.cluster(f"{spineCurve}.cv[2:]", n=f"clt_{spine2}")[1]
        clt2_grp = groupOwnPivot(clt2)[0]
        pm.setAttr(f"{clt2_grp}.visibility", 0)
        ctrl = Controllers()
        ccSpine0_IK = ctrl.createControllers(circle=ccSpine0_IK)[0]
        pm.scale(ccSpine0_IK, ccSpine0_IKSize)
        pm.makeIdentity(ccSpine0_IK, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSpine0_IK, spine0, pos=True)
        ccSpine0_IK_grp = groupOwnPivot(ccSpine0_IK)
        pm.parent(clt1_grp, ccSpine0_IK)
        ccSpine2_IK = ctrl.createControllers(circle=ccSpine2_IK)[0]
        pm.scale(ccSpine2_IK, ccSpine2_IKSize)
        pm.makeIdentity(ccSpine2_IK, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccSpine2_IK, clt2, pos=True)
        ccSpine2_IK_grp = groupOwnPivot(ccSpine2_IK)
        pm.parent(clt2_grp, ccSpine2_IK)
        parentHierarchically(*ccSpine0_IK_grp + ccSpine2_IK_grp)
        # FK
        for cc, jnt, scl in zip(ccSpines_FK, joints.keys(), FKSize):
            cc = pm.circle(nr=(0, 1, 0), r=scl, n=cc, ch=0)[0]
            pm.matchTransform(cc, jnt, pos=True)
        ccSpines_FK_grp = groupOwnPivot(*ccSpines_FK)
        ccSpines_FK_grp = parentHierarchically(*ccSpines_FK_grp)
        # Neck, Head
        ccNeck = pm.circle(nr=(0, 1, 0), r=ccNeckSize, n=ccNeck, ch=0)[0]
        ccHead = ctrl.createControllers(head=ccHead)[0]
        pm.scale(ccHead, ccHeadSize)
        pm.makeIdentity(ccHead, a=1, s=1, jo=0, n=0, pn=1)
        pm.matchTransform(ccNeck, neck, pos=True)
        pm.matchTransform(ccHead, head, pos=True)
        ccNeck_grp = groupOwnPivot(ccNeck)
        ccHead_grp = groupOwnPivot(ccHead)
        ccNeckHead_grp = parentHierarchically(*ccNeck_grp + ccHead_grp)
        # Color
        colorize(ccSpine0_IK, ccSpine2_IK, red2=True)
        colorize(*ccSpines_FK, blue2=True)
        colorize(ccNeck, ccHead, yellow=True)
        # Grouping
        if not pm.objExists(finalGroup):
            finalGroup = pm.group(em=True, n=finalGroup)
        temp = [ccSpine0_IK_grp[0], ccSpines_FK_grp[0], ccNeckHead_grp[0]]
        pm.parent(temp, finalGroup)
        return finalGroup


    def createShoulderCtrl(self, shoulderJnt: str) -> str:
        """ Creates a Scapula's Controller.

        Process
        -------
        - Create a cc_shoulder
        - Colorize.
         """
        # Variables
        scaleRatio = self.getDefaultSize(self.jntHips)[1]
        ccShoulder = "cc_%s" % shoulderJnt
        ccShoulderSize = (0.8*scaleRatio, ) * 3
        rotateZ = 135 if "Right" in shoulderJnt else -45
        nullSpace = "null_%sSpace" % shoulderJnt
        # Run
        if pm.objExists(ccShoulder):
            return
        ctrl = Controllers()
        ccShoulder = ctrl.createControllers(scapula=ccShoulder)[0]
        pm.scale(ccShoulder, ccShoulderSize)
        pm.rotate(ccShoulder, (0, 0, rotateZ))
        pm.makeIdentity(ccShoulder, a=1, r=1, s=1, pn=1)
        if "Right" in shoulderJnt:
            pm.rotate(ccShoulder, (180, 0, 0))
        nullSpace = pm.group(em=True, n=nullSpace)
        pm.parent(nullSpace, ccShoulder)
        pm.matchTransform(ccShoulder, shoulderJnt, pos=True)
        ccShoulder_grp = groupOwnPivot(ccShoulder)
        # color
        colorBar = {"blue": True} if "Right" in shoulderJnt else {"red": True}
        colorize(ccShoulder, **colorBar)
        return ccShoulder_grp[0]


    def createArmsCtrl(self, joints: list) -> str:
        """ Creates a Arm's Controller.

        Process
        -------
        - Declaring variables.
        - FK
            - If the "Right" joint, rotateX the controller -180 degrees.
        - IK
            - Shoulder controller,
            - Elbow poleVector controller.
            - Hand controller.
        - Finally,
            - Colorize.
            - Add attributes
            - Grouping.
         """
        # Variables
        shoulder, elbow, hand = joints
        ccArm_IK = addPrefix(joints, ["cc_"], ["_IK"])
        ccArm_FK = addPrefix(joints, ["cc_"], ["_FK"])
        ccShoulder_IK, ccElbow_IK, ccHand_IK = ccArm_IK
        nullSpace = "null_%sSpace" % shoulder
        handSpace = "null_%sSpace" % hand
        side = "Left" if "Left" in shoulder else "Right"
        finalGroup = "cc_%sArm_grp" % side
        scaleRatio = self.getDefaultSize(self.jntHips)[1]
        FKSize = (i*scaleRatio for i in [9.3, 8, 6.8])
        # Run
        isFKExist = any([pm.objExists(i) for i in ccArm_FK])
        isIKExist = any([pm.objExists(i) for i in ccArm_IK])
        if isFKExist or isIKExist:
            return
        # FK
        for cc, jnt, scl in zip(ccArm_FK, joints, FKSize):
            cc = pm.circle(nr=(1,0,0), r=scl, n=cc, ch=False)[0]
            if "Right" in jnt:
                pm.rotate(cc, (-180, 0, 0))
            pm.matchTransform(cc, jnt, pos=True)
        for idx, cc in enumerate(ccArm_FK):
            flipFactor = -1 if "Right" in jnt else 1
            if (idx+1) < len(ccArm_FK):
                pm.aimConstraint(ccArm_FK[idx+1], cc, 
                                aimVector=(flipFactor,0,0), 
                                upVector=(0,flipFactor,0), 
                                worldUpType="vector", 
                                worldUpVector=(0,1,0), 
                                mo=False, w=1.0
                                )
                pm.delete(cc, cn=True)
            elif (idx+1) == len(ccArm_FK):
                pm.orientConstraint(ccArm_FK[idx-1], cc, mo=False, w=1.0)
                pm.delete(cc, cn=True)
            else:
                continue
        ccArm_FK_grp = groupOwnPivot(*ccArm_FK)
        ccArm_FK_grp = parentHierarchically(*ccArm_FK_grp)
        # IK
        ctrl = Controllers()
        ccArm_IK = ctrl.createControllers(circle=ccShoulder_IK, 
                                           sphere=ccElbow_IK, 
                                           cube=ccHand_IK)
        ccShoulder_IK, ccElbow_IK, ccHand_IK = ccArm_IK
        for i in ccArm_IK:
            pm.scale(i, (scaleRatio, )*3)
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        pm.scale(ccShoulder_IK, (0.75,)*3)
        pm.rotate(ccShoulder_IK, (0, 0, -90))
        pm.makeIdentity(ccShoulder_IK, a=1, r=1, s=1, pn=1)
        nullSpace = pm.group(em=True, n=nullSpace)
        pm.parent(nullSpace, ccShoulder_IK)
        pm.matchTransform(ccShoulder_IK, shoulder, pos=True)
        ccShoulder_IK_grp = groupOwnPivot(ccShoulder_IK)
        jnt1, jnt2 = createPolevectorJoint(*joints)
        pm.matchTransform(ccElbow_IK, jnt2, pos=True)
        ccElbow_IK_grp = groupOwnPivot(ccElbow_IK)
        pm.delete(jnt1)
        handSpace = pm.group(em=True, n=handSpace)
        pm.parent(handSpace, ccHand_IK)
        pm.matchTransform(ccHand_IK, hand, pos=True)
        ccHand_IK_grp = groupOwnPivot(ccHand_IK)
        # Color
        ctrls = ccArm_FK + ccArm_IK
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
            ccArm_FK_grp[0], 
            ]
        pm.group(ctrls_grp, n=finalGroup)
        return finalGroup


    def createLegsCtrl(self, joints: list) -> str:
        """ Creates a Leg's Controller.

        Args
        ----
        - joints
            - ["UpLeg", "Leg", "Foot", "ToeBase", "Toe_End"]

        Process
        -------
        - Declaring variables.
        - FK
            - If the "Right" joint, rotateX the controller 180 degrees.
        - IK
            - Pelvis controller,
            - PoleVector controller.
            - Foot controller.
                - Create locators.
                - Each locator is organized into its own hierarchy.
        - Finally,
            - Colorize.
            - Add attributes
            - Grouping
         """
        # Variables
        pelvis, knee, foot, ball, toe = joints
        ccLegs_IK = addPrefix(joints, ["cc_"], ["_IK"])
        ccLegs_FK = addPrefix(joints, ["cc_"], ["_FK"])
        ccPelvis_IK, ccKnee_IK, ccFoot_IK = ccLegs_IK[:3]
        FKSize = [13, 10, 9, 7, 1]
        scaleRatio = self.getDefaultSize(self.jntHips)[1]
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
        pelvisSpace = f"null_{pelvis}Space"
        footSpace = f"null_{foot}Space"
        finalGroup = f"cc_{side}Leg_grp"
        # Run
        isIKExist = any([pm.objExists(i) for i in ccLegs_IK])
        isFKExist = any([pm.objExists(i) for i in ccLegs_FK])
        isLocExist = any([pm.objExists(i) for i in locators])
        if isFKExist or isIKExist or isLocExist:
            return
        # FK
        for cc, jnt, scl in zip(ccLegs_FK, joints, FKSize):
            if "Toe_End" in cc:
                continue
            normalAxis = (0, 0, 1) if "ToeBase" in cc else (0, 1, 0)
            scl *= scaleRatio
            cc = pm.circle(nr=normalAxis, r=scl, n=cc, ch=False)[0]
            if "Right" in jnt:
                pm.rotate(cc, (180, 0, 0))
            pm.matchTransform(cc, jnt, pos=True)
        ccLegs_FK_grp = groupOwnPivot(*ccLegs_FK[:-1])
        ccLegs_FK_grp = parentHierarchically(*ccLegs_FK_grp)
        # IK
        ctrl = Controllers()
        ccLegs_IK = ctrl.createControllers(scapula=ccPelvis_IK, 
                                           sphere=ccKnee_IK, foot2=ccFoot_IK)
        ccPelvis_IK, ccKnee_IK, ccFoot_IK = ccLegs_IK
        for i in ccLegs_IK:
            pm.scale(i, (scaleRatio, )*3)
            pm.makeIdentity(i, a=1, s=1, jo=0, n=0, pn=1)
        # IK - UpLeg
        ccPelvisRotation = (0, 0, 90) if "Right" == side else (0, 0, -90)
        pm.rotate(ccPelvis_IK, ccPelvisRotation)
        pm.scale(ccPelvis_IK, (0.9, )*3)
        pm.makeIdentity(ccPelvis_IK, a=1, r=1, s=1, pn=1)
        pm.matchTransform(ccPelvis_IK, pelvis, pos=True)
        # IK - Space group
        pelvisSpace = pm.group(em=True, n=pelvisSpace)
        pm.matchTransform(pelvisSpace, ccPelvis_IK, pos=True)
        pm.parent(pelvisSpace, ccPelvis_IK)
        ccPelvis_IK_grp = groupOwnPivot(ccPelvis_IK)
        # IK - Knee
        jnt1, jnt2 = createPolevectorJoint(*joints[:3])
        pm.matchTransform(ccKnee_IK, jnt2, pos=True)
        ccKnee_IK_grp = groupOwnPivot(ccKnee_IK)
        pm.delete(jnt1)
        # IK - Foot
        groupingOrder = []
        pm.matchTransform(ccFoot_IK, foot, pos=True)
        pm.setAttr(f"{ccFoot_IK}.translateY", 0)
        footPivot = pm.xform(foot, q=True, ws=True, rp=True)
        pm.xform(ccFoot_IK, ws=True, piv=footPivot)
        ccFoot_IK_grp = groupOwnPivot(ccFoot_IK)
        pm.makeIdentity(ccFoot_IK, a=1, t=1, pn=1)
        groupingOrder.append(ccFoot_IK)
        # IK - Locators
        for i in locators:
            pm.spaceLocator(p=(0, 0, 0), n=i)
        # locators[0] : heel
        pm.matchTransform(locators[0], foot, pos=True)
        pm.setAttr(f"{locators[0]}.translateY", 0)
        tmp = pm.getAttr(f"{locators[0]}.translateZ") - (8*scaleRatio)
        pm.setAttr(f"{locators[0]}.translateZ", tmp)
        groupingOrder.append(locators[0])
        # locators[1] : toe
        pm.matchTransform(locators[1], toe, pos=True)
        pm.setAttr(f"{locators[1]}.translateY", 0)
        groupingOrder.append(locators[1])
        # locators[2] : bankIn
        pm.matchTransform(locators[2], ball, pos=True)
        pm.setAttr(f"{locators[2]}.translateY", 0)
        tmp = pm.getAttr(f"{locators[2]}.translateX") - (5*scaleRatio)
        pm.setAttr(f"{locators[2]}.translateX", tmp)
        groupingOrder.append(locators[2])
        # locators[3] : bankOut
        pm.matchTransform(locators[3], ball, pos=True)
        pm.setAttr(f"{locators[3]}.translateY", 0)
        tmp = pm.getAttr(f"{locators[3]}.translateX") + (5*scaleRatio)
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
        # Foot's Space
        footSpace = pm.group(em=True, n=footSpace)
        pm.matchTransform(footSpace, ccFoot_IK, pos=True)
        pm.parent(footSpace, ccFoot_IK)
        # Color
        ctrls = ccLegs_FK + ccLegs_IK
        colorBar = {"red": True} if "Left" == side else {"blue": True}
        colorize(*ctrls, **colorBar)
        # Add Attributes
        pm.addAttr(ccLegs_IK[1], ln="Space", at="enum", en=attrLeg_IK)
        pm.setAttr(f"{ccLegs_IK[1]}.Space", e=True, k=True)
        for i in attrFoot_IK_enum:
            pm.addAttr(ccLegs_IK[2], ln=i, at="double", dv=0)
            pm.setAttr(f"{ccLegs_IK[2]}.{i}", e=True, k=True)
        pm.addAttr(ccFoot_IK, ln=attrFoot_IK_float, at="double", min=0, max=1, dv=0)
        pm.setAttr(f'{ccFoot_IK}.{attrFoot_IK_float}', e=True, k=True)
        # Final Touch
        parentHierarchically(*groupingOrder)
        groups = [
            ccPelvis_IK_grp[0], 
            ccKnee_IK_grp[0], 
            ccFoot_IK_grp[0], 
            ccLegs_FK_grp[0], 
            ]
        pm.group(groups, n=finalGroup)
        return finalGroup


    def createFingerCtrl(self, joints: list) -> str:
        """ Creates a Finger's Controller.

        Args
        ----
        - joints
            - ["Thumb1", "Thumb2", "Thumb3", "Thumb4"]
            - ["Index1", "Index2", "Index3"]

        Process
        -------
        - Create the names of the controllers from Joint.
        - Colorize.
        - Grouping.
         """
        # Variables
        ccFinger = addPrefix(joints, ["cc_"], [])
        ccFingerSize = [2, 1.6, 1.3, 1]
        scaleRatio = self.getDefaultSize(self.jntHips)[1]
        side = "Right" if "Right" in ccFinger[0] else "Left"
        finalGroup = f"cc_{side}HandFingers_grp"
        # Run
        if any([pm.objExists(i) for i in ccFinger]):
            return
        # Create Ctrls
        ccFinger_FK = []
        for idx, (cc, jnt) in enumerate(zip(ccFinger, joints)):
            if idx%4 == 3:
                continue
            scl = scaleRatio * ccFingerSize[idx%4]
            cc = pm.circle(nr=(1, 0, 0), r=scl, n=cc, ch=0)[0]
            pm.matchTransform(cc, jnt, pos=True, rot=True)
            rot = -1 if "Right" in cc.name() else 1
            pm.rotate(cc, (0, 0, rot*90), r=True, os=True, fo=True)
            pm.rotate(cc, (rot*-90, 0, 0), r=True, os=True, fo=True)
            ccFinger_FK.append(cc)
            # Color
            color = {"blue2": True} if "Right" in cc.name() else {"red2": True}
            colorize(cc, **color)
        # Grouping
        ccFinger_FK_grp = groupOwnPivot(*ccFinger_FK)
        temp = []
        for idx, num in enumerate(range(0, len(ccFinger_FK_grp), 6)):
            tmp = parentHierarchically(*ccFinger_FK_grp[num:6*(idx+1)])[0]
            temp.append(tmp)
        finalGroup = pm.group(temp, n=finalGroup)
        return finalGroup


# ==============================================================================


    def rigMainCtrl(self):
        pass


    def rigHipsCtrl(self):
        # Variables
        ccHipsMain_grp = "cc_%sMain_grp" % self.jntHips
        ccHipsSub = "cc_%sSub" % self.jntHips
        if not pm.objExists(ccHipsMain_grp):
            return
        if not pm.objExists(ccHipsSub):
            return
        if pm.listConnections(ccHipsMain_grp, type="constraint"):
            return
        # cc_sub2 -> rig_Hips
        pm.parentConstraint(self.mainCtrls[2], ccHipsMain_grp, mo=1, w=1)
        pm.scaleConstraint(self.mainCtrls[2], ccHipsMain_grp, mo=1, w=1)
        # cc_HipsSub -> rig_Hips
        pm.parentConstraint(ccHipsSub, self.rgHips, mo=1, w=1)


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
        # Run
        if not pm.objExists(ccHipsSub) or not pm.objExists(cuvName):
            return
        isIKHandle = pm.objExists(ikhName)
        if isIKHandle:
            if "ikHandle" == pm.objectType(ikhName):
                return
        # IK
        ikHandle = pm.ikHandle(sj=rgSpineJnt_IK[0], ee=rgSpineJnt_IK[2], 
                          sol="ikSplineSolver", 
                          name=ikhName, 
                          curve=cuvName, 
                          createCurve=0, 
                          parentCurve=0, 
                          numSpans=3)
        ikHandle = ikHandle[0]
        pm.setAttr(f"{ikHandle}.visibility", 0)
        try:
            pm.parent(ikHandle, "extraNodes")
        except:
            pass
        pm.connectAttr(f"{ccSpine_IK[0]}.rotateY", f"{ikHandle}.roll", f=1)
        pm.connectAttr(f"{ccSpine_IK[2]}.rotateY", f"{ikHandle}.twist", f=1)
        # FK
        for cc, jnt in zip(ccSpine_FK, rgSpineJnt_FK):
            pm.parentConstraint(cc, jnt, mo=True, w=1)
        # Connect : FK + IK -> BlendColor -> Original
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
        pm.scaleConstraint(ccHipsSub, ccSpine_IK_grp, mo=True, w=1)
        pm.parentConstraint(ccHipsSub, ccSpine_FK_grp, mo=True, w=1)
        pm.scaleConstraint(ccHipsSub, ccSpine_FK_grp, mo=True, w=1)
        pm.parentConstraint(rgSpineJnt[-1], ccNeck_grp, mo=True, w=1)
        pm.scaleConstraint(rgSpineJnt[-1], ccNeck_grp, mo=True, w=1)


    def rigShoulderCtrl(self, joint: str):
        # Variables
        side = "Left" if "Left" in joint else "Right"
        shoulderSpace = f"null_{side}ShoulderSpace"
        rgShoulder = "rig_" + joint
        ccShoulder_grp = "cc_" + joint + "_grp"
        rgSpine2 = "rig_" + self.spine[2]
        # Run
        if not pm.objExists(ccShoulder_grp):
            return
        if pm.listConnections(ccShoulder_grp, type="constraint"):
            return
        # Constraint
        pm.parentConstraint(shoulderSpace, rgShoulder, mo=True, w=1)
        pm.parentConstraint(rgSpine2, ccShoulder_grp, mo=True, w=1)
        pm.scaleConstraint(rgSpine2, ccShoulder_grp, mo=True, w=1)


    def rigArmsCtrl(self, joints: list):
        # Variables
        rgArms = addPrefix(joints, ["rig_"], [])
        ccArms_IK = addPrefix(joints, ["cc_"], ["_IK"])
        rgArms_IK = addPrefix(joints, ["rig_"], ["_IK"])
        ccArms_FK = addPrefix(joints, ["cc_"], ["_FK"])
        rgArms_FK = addPrefix(joints, ["rig_"], ["_FK"])
        ccShoulder_IK, ccElbow_IK, ccHand_IK = ccArms_IK
        rgShoulder_IK, rgElbow_IK, rgHand_IK = rgArms_IK
        side = "Left" if "Left" in ccShoulder_IK else "Right"
        ccIKFK = f"cc_IKFK.{side}_Arm_IK0_FK1"
        shoulderSpace = f"null_{side}ShoulderSpace"
        handMenu = self.getSpaceMenu(side, hand=True)
        elbowMenu = self.getSpaceMenu(side, elbow=True)
        # Run
        if not pm.objExists(ccShoulder_IK):
            return
        if pm.listConnections(rgShoulder_IK, type="constraint"):
            return
        createBlendColor(ccIKFK, rgArms, rgArms_FK, rgArms_IK, t=1, r=1)
        # IK - Shoulder
        pm.pointConstraint(ccShoulder_IK, rgShoulder_IK, mo=True, w=1)
        # IK - Hand
        ikHandle = createIKHandle(rgShoulder_IK, rgHand_IK, rp=True)[0]
        pm.orientConstraint(ccHand_IK, rgHand_IK, mo=True, w=1)
        pm.parent(ikHandle, ccHand_IK)
        connectSpace(ccHand_IK, handMenu, float=True)
        # IK - Polevector
        pm.poleVectorConstraint(ccElbow_IK, ikHandle, w=1.0)
        connectSpace(ccElbow_IK, elbowMenu, enum=True)
        anno = createAnnotation(rgElbow_IK, ccElbow_IK)
        anno_grp = groupOwnPivot(anno)
        pm.parentConstraint(rgElbow_IK, anno_grp[0], mo=True, w=1)
        pm.scaleConstraint(rgElbow_IK, anno_grp[0], mo=True, w=1)
        try:
            pm.parent(anno_grp[0], "extraNodes")
        except:
            pass
        # FK
        for cc, jnt in zip(ccArms_FK, rgArms_FK):
            pm.parentConstraint(cc, jnt, mo=True, w=1)
        # Setting Visibility
        pm.setAttr(f"{ikHandle}.visibility", 0)
        ccShoulder_FK_grp = pm.listRelatives(ccArms_FK[0], p=True)[0]
        pm.connectAttr(ccIKFK, f"{ccShoulder_FK_grp}.visibility", f=1)
        revNode = pm.shadingNode("reverse", au=True)
        pm.connectAttr(ccIKFK, f"{revNode}.inputX", f=1)
        for cc in ccArms_IK:
            cc_grp = pm.listRelatives(cc, p=True)[0]
            pm.connectAttr(f"{revNode}.outputX", f"{cc_grp}.visibility", f=1)
        # Constraint
        pm.parentConstraint(shoulderSpace, ccShoulder_FK_grp, mo=True, w=1)
        pm.scaleConstraint(shoulderSpace, ccShoulder_FK_grp, mo=True, w=1)
        ccShoulder_IK_grp = pm.listRelatives(ccShoulder_IK, p=True)[0]
        pm.parentConstraint(shoulderSpace, ccShoulder_IK_grp, mo=True, w=1)
        pm.scaleConstraint(shoulderSpace, ccShoulder_IK_grp, mo=True, w=1)


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
        # Run
        if not pm.objExists(ccPelvis_IK):
            return
        if pm.listConnections(rgPelvisJnt, type="constraint"):
            return
        if pm.listConnections(rgFootJnt, type="ikHandle"):
            return
        # IK - UpLeg
        pm.pointConstraint(ccPelvis_IK, rgPelvisJnt, mo=True, w=1)
        # IK - ikHandle
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
        # IK - Connect blendColorNode
        createBlendColor(ccIKFK, 
                         rgLegsJnt, rgLegsJnt_FK, rgLegsJnt_IK, 
                         t=True, r=True)
        # IK - Connect Foot's Attr
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
        # IK - polevector
        pm.poleVectorConstraint(ccKnee_IK, ikhPelvis, w=1)
        ano = createAnnotation(rgKneeJnt, ccKnee_IK)
        anoGrp = groupOwnPivot(ano)
        pm.parentConstraint(rgKneeJnt, anoGrp[0], mo=True, w=1)
        pm.scaleConstraint(rgKneeJnt, anoGrp[0], mo=True, w=1)
        try:
            pm.parent(anoGrp[0], "extraNodes")
        except:
            pass
        connectSpace(ccKnee_IK, legMenu, enum=True)
        # FK
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
            pm.scaleConstraint(ccSub, i, mo=True, w=1)


    def rigFingerCtrl(self, joints: list):
        ctrls = addPrefix(joints, ["cc_"], [])
        rgJoints = addPrefix(joints, ["rig_"], [])
        for cc, jnt in zip(ctrls, rgJoints):
            if pm.objExists(cc) and pm.objExists(jnt):
                pm.parentConstraint(cc, jnt, mo=True, w=1.0)
            else:
                continue
        for i in ["Left", "Right"]:
            finger_grp = f"cc_{i}HandFingers_grp"
            rgJnt = f"rig_{i}Hand"
            try:
                pm.parentConstraint(rgJnt, finger_grp, mo=True, w=1.0)
                pm.scaleConstraint(rgJnt, finger_grp, mo=True, w=1.0)
            except:
                continue


# ==============================================================================


    def getDefaultSize(self, object: str) -> tuple:
        """ Get Object's BoundingBox Size and (90.4 Ratio) 
        Return
        ------
        >>> getDefaultSize(object)
        >>> (bbSize, bbRatio)
        >>> (180.8, 2)
         """
        bbSize = getBoundingBoxSize(object)
        bbSize = max(bbSize)
        bbRatio = round(bbSize/self.defaultSize, 3)
        return bbSize, bbRatio


    def getSpaceMenu(self, side="", hand=False, elbow=False, 
                     foot=False, knee=False) -> dict:
        if foot:
            result = {
                "World0": self.worldSpace, 
                "Root1": self.rootSpace, 
                }
        elif side and knee:
            result = {
                "World": self.worldSpace, 
                "Root": self.rootSpace, 
                "Hip": "null_%sUpLegSpace" % side, 
                "Foot": "null_%sFootSpace" % side, 
                }
        elif side and hand:
            result = {
                "World0": self.worldSpace, 
                "Shoulder1": "null_%sShoulderSpace" % side, 
                }
        elif side and elbow:
            result = {
                "World": self.worldSpace, 
                "Root": self.rootSpace, 
                "Chest": "rig_Spine2", 
                "Arm": "null_%sArmSpace" % side, 
                "Hand": "null_%sHandSpace" % side, 
                }
        else:
            return
        return result


    def finalTouch(self):
        ccSub2 = self.mainCtrls[2]
        skeltonGroup = self.groupNames[2]
        rigBoneGroup = self.groupNames[-1]
        try:
            pm.delete(self.mainCurve)
        except:
            pass
        try:
            pm.scaleConstraint(ccSub2, skeltonGroup)
        except:
            pass
        pm.setAttr(f"{skeltonGroup}.visibility", 0)
        pm.setAttr(f"{rigBoneGroup}.visibility", 0)


    def buttonUnlock(self):
        isText = self.fldCreateRigGrp.text()
        isText.strip()
        isText = bool(isText)
        self.btnCreateRigGrp.setEnabled(isText)


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


# if __name__ == "__main__":
#     try:
#         char.close()
#         char.deleteLater()
#     except:
#         pass
#     char = Character()
#     char.show()

