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
        self.jntHips = "Hips"
        self.rgHips = "rig_Hips"
        self.mainCtrls = ["cc_main", "cc_sub", "cc_sub2"]
        groupNames = [
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
        self.legs_L = [
            "LeftUpLeg", 
            "LeftLeg", 
            "LeftFoot", 
            "LeftToeBase", 
            "LeftToe_End"
            ]
        self.thumb_L = [f"LeftHandThumb{i}" for i in range(1, 5)]
        self.index_L = [f"LeftHandIndex{i}" for i in range(1, 5)]
        self.middle_L = [f"LeftHandMiddle{i}" for i in range(1, 5)]
        self.ring_L = [f"LeftHandRing{i}" for i in range(1, 5)]
        self.pinky_L = [f"LeftHandPinky{i}" for i in range(1, 5)]
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
        self.thumb_R = [f"RightHandThumb{i}" for i in range(1, 5)]
        self.index_R = [f"RightHandIndex{i}" for i in range(1, 5)]
        self.middle_R = [f"RightHandMiddle{i}" for i in range(1, 5)]
        self.ring_R = [f"RightHandRing{i}" for i in range(1, 5)]
        self.pinky_R = [f"RightHandPinky{i}" for i in range(1, 5)]
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
        # self.btnCreateCtrls.clicked.connect(self.createCharCtrl)
        # self.btnMirrorCopy.clicked.connect(self.mirrorCopyFootLocator)
        # self.btnRig.clicked.connect(self.rig)
        # self.btnConnect.clicked.connect(self.connectBones)
        # self.btnDisconnect.clicked.connect(self.disConnectBones)
        self.btnClose.clicked.connect(self.close)


    def createTempJoints(self) -> None:
        """ Create temporary joints. """
        # CleanUp
        joints = self.jntPosition.keys()
        joints = list(joints)
        self.cleanUp(*joints)
        # Create Joints
        for jnt, pos in self.jntPosition.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        self.setHierarchy(self.jntHierarchy)
        # Create Main Curve
        if not pm.objExists(self.mainCurve):
            bbSize = getBoundingBoxSize(self.jntHips)
            bbSize = max(bbSize)
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