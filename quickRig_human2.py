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
        self.line = QFrame()
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.btnAlignCenterJnt = QPushButton()
        self.btnAlignCenterJnt.setObjectName(u"btnAlignCenterJnt")
        self.verticalLayout.addWidget(self.btnAlignCenterJnt)
        self.btnSynchronizeBothJnt = QPushButton()
        self.btnSynchronizeBothJnt.setObjectName(u"btnSynchronizeBothJnt")
        self.verticalLayout.addWidget(self.btnSynchronizeBothJnt)
        self.line_2 = QFrame()
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
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
        self.btnRig.setText(QCoreApplication.translate("Form", u"Rig", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"Close", None))


    def buttonsLink(self):
        self.btnCreateTempJnt.clicked.connect(self.createTempJnt)
        self.btnAlignCenterJnt.clicked.connect(self.alignCenterJnt)
        self.btnSynchronizeBothJnt.clicked.connect(self.syncBothJnt)
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


    def rig(self):
        self.createRigJnt()
        self.createCharCtrl()


    def createCharCtrl(self):
        pass


    def createHipsCtrl(self):
        # Args
        ccMain = "cc_HipsMain"
        ccSub = "cc_HipsSub"
        ccIKFK = "cc_IKFK"
        nullSpace = "null_rootSpace"
        # Create Controllers
        ctrl = Controllers()
        ccs = ctrl.createControllers(cube=ccMain, arrow4=ccSub, IKFK=ccIKFK)
        nullSpace = pm.group(em=True, n=nullSpace)
        # Move
        pm.scale(ccs[0], (5, 0.4, 5))
        pm.makeIdentity(ccs[0], a=1, s=1, jo=0, n=0, pn=1)
        pm.rotate(ccs[2], (90, 0, 0))
        pm.move(ccs[2], (40, 0, 0))
        pm.makeIdentity(ccs[2], a=1, r=1, jo=0, n=0, pn=1)
        # Grouping
        grp = groupOwnPivot(*ccs)
        pm.makeIdentity(ccs[2], a=1, t=1, jo=0, n=0, pn=1)
        # Structure
        ccGroups = parentHierarchically(*grp)
        pm.parent(nullSpace, ccSub)
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


    def connectBlendColor(self, ctrl: str, joints: list, \
                      t=False, r=False, s=False, v=False) -> None:
        """ Create a <blendColorNode>.
        - Connect FK, IK to color1, color2 of the <blendColorNode>.
        - Connect the output of the <blendColorNode> to the joint.
        - Connect the controller to the blender. 
        
        Args
        ----
        - ctrl : str
            - "cc_IKFK.Spine_IK0_FK1", 
            - "cc_IKFK.Left_Arm_IK0_FK1", 
            - "cc_IKFK.Right_Arm_IK0_FK1", 
            - "cc_IKFK.Left_Leg_IK0_FK1", 
            - "cc_IKFK.Right_Leg_IK0_FK1"
        - joints : list
            - sample = [
                'rig_RightUpLeg', 
                'rig_RightLeg', 
                'rig_RightFoot', 
                'rig_RightToeBase', 
                'rig_RightToe_End', 
                'rig_RightUpLeg_FK', 
                'rig_RightLeg_FK', 
                'rig_RightFoot_FK', 
                'rig_RightToeBase_FK', 
                'rig_RightToe_End_FK', 
                'rig_RightUpLeg_IK', 
                'rig_RightLeg_IK', 
                'rig_RightFoot_IK', 
                'rig_RightToeBase_IK', 
                'rig_RightToe_End_IK', 
                ]
        - t : bool (translate)
        - r : bool (rotate)
        - s : bool (scale)
        - v : bool (visibility)

        Examples
        --------
        >>> connectBlendColor("cc_IKFK.Spine_IK0_FK1", t=1, r=1)
        >>> connectBlendColor("cc_IKFK.Left_Arm_IK0_FK1", t=1, r=1)
        >>> connectBlendColor("cc_IKFK.Right_Arm_IK0_FK1", t=1, r=1)
        >>> connectBlendColor("cc_IKFK.Left_Leg_IK0_FK1", joints, t=1, r=1)
        >>> connectBlendColor("cc_IKFK.Right_Leg_IK0_FK1", joints, t=1, r=1)
         """
        sel = joints if joints else pm.selected()
        if len(sel) % 3:
            return
        else:
            mod = len(sel) // 3
            joint = sel[0 : mod*1]
            jntFK = sel[mod : mod*2]
            jntIK = sel[mod*2 : mod*3]
        attr = []
        if t:   attr.append("translate")
        if r:   attr.append("rotate")
        if s:   attr.append("scale")
        if v:   attr.append("visibility")
        for i in attr:
            for fk, ik, jnt in zip(jntFK, jntIK, joint):
                blColor = pm.shadingNode("blendColors", au=True)
                pm.connectAttr(f"{fk}.{i}", f"{blColor}.color1", f=True)
                pm.connectAttr(f"{ik}.{i}", f"{blColor}.color2", f=True)
                pm.connectAttr(f"{blColor}.output", f"{jnt}.{i}", f=True)
                pm.connectAttr(ctrl, f"{blColor}.blender")


    def createRigJnt(self) -> None:
        """ To create the rig joint by copying the original joint. """
        if pm.objExists("rig_Hips"):
            return
        # Duplicate All.
        duplicateObj(self.hips, "rig_", "")
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
            result = pm.circle(nr=(0, 1, 0), n="mainCurve", ch=0, r=bbSize)
        return result[0]


# if __name__ == "__main__":
#     try:
#         char.close()
#         char.deleteLater()
#     except:
#         pass
#     char = Character()
#     char.show()

