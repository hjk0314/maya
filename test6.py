from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
# from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
from general import *
# import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as omui


class MixamoCharacter(QWidget):
    def __init__(self):
        self.mainCurve = "mainCurve"
        self.spine = [
            "Hips", 
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
        self.jointPosition = {
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
        self.hierarchy = {
            "Hips": [self.spine[1:], self.leftLegs, self.rightLegs], 
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
        # self.setupUI()
    

    def setupUI(self):
        # super(Car, self).__init__()
        # self.setParent(mayaMainWindow())
        # self.setWindowFlags(Qt.Window)
        self.buttonsLink()


    def buttonsLink(self):
        pass


    def createBones(self):
        self.cleanUp(self.mainCurve, self.jointPosition.keys())
        self.createJointAndNameIt(self.jointPosition)
        self.buildHierarchy(self.hierarchy)
        self.createMainCurve()


    def alignBonesCenter(self):
        self.updateAllJointPositions()
        self.updatePositionGridCenter(self.spine)
        self.createBones()


    def alignBonesSameSide(self):
        AtoB = "LeftToRight"
        # AtoB = "RightToLeft"
        self.updateAllJointPositions()
        sideA, sideB = self.seperateLeftAndRight(AtoB)
        self.updateBothSideToSame(sideA, sideB)
        self.createBones()


    def createRig_All(self):
        self.updateAllJointPositions()
        jntPos = self.jointPosition
        hiraky = self.hierarchy
        data = self.copyBonesForRig(jntPos, hiraky, "rig_", "")
        rigJntPos, rigHiraky = data
        self.cleanUp(rigJntPos.keys())
        self.createJointAndNameIt(rigJntPos)
        self.buildHierarchy(rigHiraky)


    def createRig_IKFK(self):
        self.createIKFK(self.spine[0], self.spine[1:4])
        self.createIKFK(self.leftArms[0], self.leftArms[1:])
        self.createIKFK(self.rightArms[0], self.rightArms[1:])
        self.createIKFK(self.spine[0], self.leftLegs)
        self.createIKFK(self.spine[0], self.rightLegs)


# ==============================================================================


    def createIKFK(self, parents: str, joints: list):
        self.updateAllJointPositions()
        jntPos = {i: self.jointPosition[i] for i in joints}
        hiraky = {parents: [joints]}
        for i in ["_FK", "_IK"]:
            data = self.copyBonesForRig(jntPos, hiraky, "rig_", i)
            rigJntPos, temp = data
            rigHiraky = {k.rsplit("_", 1)[0]: v for k, v in temp.items()}
            self.cleanUp(rigJntPos.keys())
            self.createJointAndNameIt(rigJntPos)
            self.buildHierarchy(rigHiraky)


    def copyBonesForRig(self, jointPosition, hierarchy, fore="", tail=""):
        """ Returns the data with a new name. 
        - positions = {str: (float, float, float), ...}
        - hierarchy = {str: [[ ],[ ]], ...}
         """
        rigJointPosition = {}
        for jnt, pos in jointPosition.items():
            rigJointPosition[f"{fore}{jnt}{tail}"] = pos 
        rigHierarchy = {}
        for parents, children in hierarchy.items():
            key = f"{fore}{parents}{tail}"
            value = [[f"{fore}{j}{tail}" for j in i] for i in children]
            rigHierarchy[key] = value
        return rigJointPosition, rigHierarchy


    def updateBothSideToSame(self, sideA, sideB):
        for idx, joint in enumerate(sideA):
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[sideB[idx]] = (x*-1, y, z)


    def seperateLeftAndRight(self, twoOptions: str) -> list:
        """ Direction has one of the options: 
        >>> "LeftToRight" or "RightToLeft" 
         """
        allJoints = self.jointPosition.keys()
        A, B = twoOptions.split("To")
        side = []
        otherSide = []
        for jointName in allJoints:
            if A in jointName:
                side.append(jointName)
            elif B in jointName:
                otherSide.append(jointName)
            else:
                continue
        return side, otherSide


    def updateAllJointPositions(self):
        allJoints = self.jointPosition.keys()
        for joint in allJoints:
            position = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = tuple(position)


    def updatePositionGridCenter(self, joints: list):
        for joint in joints:
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = (0, y, z)


    def createMainCurve(self):
        rootJnt = self.spine[0]
        if not pm.objExists(rootJnt):
            return
        else:
            bbSize = getBoundingBoxSize(rootJnt)
            pm.circle(nr=(0, 1, 0), n=self.mainCurve, ch=0, r=bbSize)
            pm.parent(rootJnt, self.mainCurve)


    def getPrimaryAndSecondaryAxis(self, jnt=[]):
        isLeft = any(i in jnt[0] for i in self.leftArms)
        isRight = any(i in jnt[0] for i in self.rightArms)
        if isLeft:
            primaryAxis = 'yxz'
            secondaryAxis = 'zdown'
        elif isRight:
            primaryAxis = 'yxz'
            secondaryAxis = 'zup'
        else:
            primaryAxis = 'yzx'
            secondaryAxis = 'zup'
        return primaryAxis, secondaryAxis


    def buildHierarchy(self, hierarchyStructure: dict):
        for parents, bothSideList in hierarchyStructure.items():
            for jointList in bothSideList:
                parentHierarchically(*jointList)
                priAxis, secAxis = self.getPrimaryAndSecondaryAxis(jointList)
                orientJoints(jointList, priAxis, secAxis)
                parentHierarchically(*[parents, jointList[0]])


    def createJointAndNameIt(self, nameAndPosition: dict):
        for jointName, position in nameAndPosition.items():
            pm.select(cl=True)
            pm.joint(p=position, n=jointName)


    def cleanUp(self, *args):
        for element in args:
            isStr = isinstance(element, str)
            isIter = isinstance(element, Iterable)
            if not isStr and isIter:
                for i in element:
                    self.cleanUp(i)
            else:
                try:
                    pm.delete(element)
                except:
                    pass


# mc = MixamoCharacter()
# mc.createBones()
# mc.alignBonesCenter()
# mc.alignBonesSameSide()
# mc.createRig_All()
# mc.createRig_IKFK()


def connectAttributes(source: str, destination: str, \
                    t=False, r=False, s=False, v=False) -> None:
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        try:
            pm.connectAttr(f"{source}.{i}", f"{destination}.{i}", f=True)
        except:
            continue


def disConnectAttributes(source: str, destination: str, \
                    t=False, r=False, s=False, v=False) -> None:
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        try:
            pm.disconnectAttr(f"{source}.{i}", f"{destination}.{i}")
        except:
            continue


def connectBlendColorsNode(blender: str, objects: list=[], \
                            t=False, r=False, s=False, v=False) -> None:
    """ Create a blendColors node and 
    connect FK to colors1 and IK to colors2.
    
    Args: 
        blender: This is Switch.
            "cc_IKFK.Spine_IK0FK1", 
            "cc_IKFK.LArm_IK0FK1", 
            "cc_IKFK.RArm_IK0FK1", 
            "cc_IKFK.LLeg_IK0FK1", 
            "cc_IKFK.RLeg_IK0FK1", 
        objects: The list have destination, FK, and IK elements.
            objects = ["destination", "FK", "IK"]

    Options: 
        -- t: translate, 
        -- r: rotate, 
        -- s: scale, 
        -- v: visibility

    Examples:
        >>> connectBlendColorsNode("cc_IKFK.Spine_IK0FK1", t=1)
        >>> connectBlendColorsNode("cc_IKFK.LArm_IK0FK1", r=1)
        >>> connectBlendColorsNode("cc_IKFK.RArm_IK0FK1", s=1)
        >>> connectBlendColorsNode("cc_IKFK.LLeg_IK0FK1", v=1)
        >>> connectBlendColorsNode("cc_IKFK.RLeg_IK0FK1", t=1, v=1)
     """
    args = objects if objects else pm.ls(sl=True)
    if len(args) % 3:
        return
    else:
        quotient = len(args) // 3
        destination = args[0 : quotient*1]
        source1 = args[quotient : quotient*2]
        source2 = args[quotient*2 : quotient*3]
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        for s1, s2, fin in zip(source1, source2, destination):
            blColor = pm.shadingNode("blendColors", au=True)
            pm.connectAttr(f"{s1}.{i}", f"{blColor}.color1", f=True)
            pm.connectAttr(f"{s2}.{i}", f"{blColor}.color2", f=True)
            pm.connectAttr(f"{blColor}.output", f"{fin}.{i}", f=True)
            pm.connectAttr(blender, f"{blColor}.blender")


def createIKHandle(*args, rp=False, sc=False, spl=False, spr=False):
    """ Create a ikHandle and return names.

    Args: 
        startJoint = ["joint1", "joint2", ..., "joint27"][0]
        endJoint = ["joint1", "joint2", ..., "joint27"][-1]

    Options:
        --rp: "ikRPsolver"
        --sc: "ikSCsolver"
        --spl: "ikSplineSolver"
        --spr: "ikSpringSolver"
    
    Return: 
        Created ikHandle name.
    """
    sel = args if args else pm.ls(sl=True)
    if rp:
        solver = "ikRPsolver"
    elif sc:
        solver = "ikSCsolver"
    elif spl:
        solver = "ikSplineSolver"
    elif spr:
        solver = "ikSpringSolver"
    else:
        return
    try:
        start = sel[0]
        end = sel[-1]
    except:
        return
    temp = start.split("_")
    temp[0] = "ikH"
    ikHandleName = "_".join(temp)
    result = pm.ikHandle(sj=start, ee=end, sol=solver, n=ikHandleName)
    return result


def connectLegAttributes(*args: list):
    """ Connect the leg's locators to the controller's attributes.

    Args: 
        The elements of the list are 
        ctrl, locHeel, locToe, locBankIn, locBankOut, locBall, grpBall.
        locators = [
            "cc_LeftFoot_IK", 
            "loc_LeftHeel_IK", 
            "loc_LeftToe_End_IK", 
            "loc_LeftBankIn_IK", 
            "loc_LeftBankOut_IK", 
            "loc_LeftToeBase_IK", 
            "ikH_LeftToeBase_IK_null"
            ]

    Examples:
        >>> connectLegAttributes(*locators)
     """
    sel = args if args else pm.ls(sl=True)
    ctrl, locHeel, locToe, locBankIn, locBankOut, locBall, grpBall = sel
    rx, ry, rz = ["rotateX", "rotateY", "rotateZ"]
    pm.connectAttr(f"{ctrl}.heelUp", f"{locHeel}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.heelTwist", f"{locHeel}.{ry}", f=True)
    pm.connectAttr(f"{ctrl}.toeUp", f"{locToe}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.toeTwist", f"{locToe}.{ry}", f=True)
    pm.connectAttr(f"{ctrl}.ballUp", f"{locBall}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.ballDown", f"{grpBall}.{rx}", f=True)
    clampNode = pm.shadingNode("clamp", au=True)
    pm.setAttr(f"{clampNode}.minR", -180)
    pm.setAttr(f"{clampNode}.maxG", 180)
    output1 = "outputR" if "Left" in locBankOut else "outputG"
    output2 = "outputG" if "Left" in locBankIn else "outputR"
    pm.connectAttr(f"{clampNode}.{output1}", f"{locBankOut}.{rz}", f=True)
    pm.connectAttr(f"{clampNode}.{output2}", f"{locBankIn}.{rz}", f=True)
    pm.connectAttr(f"{ctrl}.bank", f"{clampNode}.inputR", f=True)
    pm.connectAttr(f"{ctrl}.bank", f"{clampNode}.inputG", f=True)


def constraintParent_asJointName(*args):
    """ Make a constraint parent with the same controller name as the joint. 
     """
    fkJoints = args if args else pm.ls(sl=True)
    for jnt in fkJoints:
        ctrl = jnt.replace("rig_", "cc_")
        if pm.objExists(ctrl) and pm.objExists(jnt):
            pm.parentConstraint(ctrl, jnt, mo=True, w=1.0)
        else:
            continue


def connectSpaceEnum(ctrl: str, enumMenu: dict) -> None:
    isAttr = pm.attributeQuery("Space", node=ctrl, exists=True)
    if isAttr:
        pm.deleteAttr(ctrl, at="Space")
    ctrlGrp = pm.listRelatives(ctrl, p=True)[0]
    dropMenu = list(enumMenu.keys())
    parents = list(enumMenu.values())
    pm.addAttr(ctrl, ln="Space", at="enum", en=":".join(dropMenu))
    pm.setAttr(f'{ctrl}.Space', e=True, k=True)
    for idx, name in enumerate(dropMenu):
        nodeName = f"{ctrl}_space{name}"
        animCurve = pm.shadingNode("animCurveTL", au=True, n=nodeName)
        for i in range(len(dropMenu)):
            num = 1 if idx==i else 0
            pm.setKeyframe(animCurve, time=i, value=num)
        pm.keyTangent(animCurve, ott="step")
        parentConstraintName = pm.parentConstraint(parents[idx], ctrlGrp, \
                                             mo=True, w=1.0)
        scaleConstraintName = pm.scaleConstraint(parents[idx], ctrlGrp, \
                                             mo=True, w=1.0)
        pm.connectAttr(f"{ctrl}.Space", f"{animCurve}.input", f=True)
        pm.connectAttr(f"{animCurve}.output", \
                       f"{parentConstraintName}.{parents[idx]}W{idx}", f=True)
        pm.connectAttr(f"{animCurve}.output", \
                       f"{scaleConstraintName}.{parents[idx]}W{idx}", f=True)


def connectSpaceFloat(ctrl: str, floatMenu: dict) -> None:
    menuName = list(floatMenu.keys())
    if len(menuName) != 2:
        return
    attr = "_".join(menuName)
    isAttr = pm.attributeQuery(attr, node=ctrl, exists=True)
    if isAttr:
        pm.deleteAttr(ctrl, at=attr)
    pm.addAttr(ctrl, ln=attr, at="double", min=0, max=1, dv=0)
    pm.setAttr(f'{ctrl}.{attr}', e=True, k=True)
    ctrlGrp = pm.listRelatives(ctrl, p=True)[0]
    parents = list(floatMenu.values())
    for idx, name in enumerate(parents):
        pConstName = pm.parentConstraint(name, ctrlGrp, mo=True, w=1.0)
        sConstName = pm.scaleConstraint(name, ctrlGrp, mo=True, w=1.0)
        if idx == 0:
            reverseNode = pm.shadingNode("reverse", au=True)
            pm.connectAttr(f"{ctrl}.{attr}", f"{reverseNode}.inputX", f=1)
            pm.connectAttr(f"{reverseNode}.outputX", \
                           f"{pConstName}.{name}W{idx}", f=True)
            pm.connectAttr(f"{reverseNode}.outputX", \
                           f"{sConstName}.{name}W{idx}", f=True)
        else:
            pm.connectAttr(f"{ctrl}.{attr}", \
                           f"{pConstName}.{name}W{idx}", f=True)
            pm.connectAttr(f"{ctrl}.{attr}", \
                           f"{sConstName}.{name}W{idx}", f=True)


def setDirection_fingerCtrl(*args):
    """ Select 4 or more joints. Joint names must be prefixed with "rig_". 
    The parent group of the controller must already be created.
     """
    joints = args if args else pm.ls(sl=True)
    if len(joints) < 4:
        return
    startJnt, endJnt = createPolevectorJoint(*joints[:3])
    for idx, jnt in enumerate(joints):
        if idx == len(joints) - 1:
            continue
        ctrlGrp = jnt.replace("rig_", "cc_") + "_grp"
        pm.matchTransform(ctrlGrp, jnt, pos=True)
        factor = -1 if "Right" in ctrlGrp else 1
        aimNode = pm.aimConstraint(joints[idx+1], ctrlGrp, \
                                   aim=(factor,0,0), u=(0,factor,0), \
                                    wut="object", wuo=endJnt)
        pm.delete(aimNode)
    # pm.delete(startJnt)


# ==============================================================================
# joints = [
#     'rig_RightUpLeg', 
#     'rig_RightLeg', 
#     'rig_RightFoot', 
#     'rig_RightToeBase', 
#     'rig_RightToe_End', 
#     'rig_RightUpLeg_FK', 
#     'rig_RightLeg_FK', 
#     'rig_RightFoot_FK', 
#     'rig_RightToeBase_FK', 
#     'rig_RightToe_End_FK', 
#     'rig_RightUpLeg_IK', 
#     'rig_RightLeg_IK', 
#     'rig_RightFoot_IK', 
#     'rig_RightToeBase_IK', 
#     'rig_RightToe_End_IK'
#     ]
# connectBlendColorsNode("cc_IKFK.Spine_IK0FK1", t=1, r=1)
# connectBlendColorsNode("cc_IKFK.LArm_IK0FK1", t=1, r=1)
# connectBlendColorsNode("cc_IKFK.RArm_IK0FK1", t=1, r=1)
# connectBlendColorsNode("cc_IKFK.LLeg_IK0FK1", t=1, r=1)
# connectBlendColorsNode("cc_IKFK.RLeg_IK0FK1", t=1, r=1)


# ==============================================================================
# createIKHandle(rp=True)
# createIKHandle(sc=True)


# ==============================================================================
# locators = [
#     "cc_LeftFoot_IK", 
#     "loc_LeftHeel_IK", 
#     "loc_LeftToe_End_IK", 
#     "loc_LeftBankIn_IK", 
#     "loc_LeftBankOut_IK", 
#     "loc_LeftToeBase_IK", 
#     "ikH_LeftToeBase_IK_null"
#     ]
# locators = [
#     "cc_RightFoot_IK", 
#     "loc_RightHeel_IK", 
#     "loc_RightToe_End_IK", 
#     "loc_RightBankIn_IK", 
#     "loc_RightBankOut_IK", 
#     "loc_RightToeBase_IK", 
#     "ikH_RightToeBase_IK_null"
#     ]
# connectLegAttributes(*locators)


# ==============================================================================
# createPolevectorJoint()


# ==============================================================================
# fkJoints = [
#     'rig_LeftUpLeg_FK', 
#     'rig_LeftLeg_FK', 
#     'rig_LeftFoot_FK', 
#     'rig_LeftToeBase_FK', 
#     'rig_LeftToe_End_FK'
#     ]
# constraintParent_asJointName()


# ==============================================================================
# ctrl = "cc_LeftLegPoleVector"
# enumMenu = {
#     "World": "null_worldSpace", 
#     "Root": "null_rootSpace", 
#     "Hip": "null_leftPelvisSpace", 
#     "Foot": "null_leftFootSpace"
#     }
# ctrl = "cc_RightLegPoleVector"
# enumMenu = {
#     "World": "null_worldSpace", 
#     "Root": "null_rootSpace", 
#     "Hip": "null_rightPelvisSpace", 
#     "Foot": "null_rightFootSpace"
#     }
# ctrl = "cc_LeftForeArmPoleVector"
# enumMenu = {
#     "World": "null_worldSpace", 
#     "Root": "null_rootSpace", 
#     "Chest": "rig_Spine2", 
#     "Arm": "null_leftArmSpace", 
#     "Hand": "null_leftHandSpace"
#     }
# ctrl = "cc_RightForeArmPoleVector"
# enumMenu = {
#     "World": "null_worldSpace", 
#     "Root": "null_rootSpace", 
#     "Chest": "rig_Spine2", 
#     "Arm": "null_rightArmSpace", 
#     "Hand": "null_rightHandSpace"
#     }
# connectSpaceEnum(ctrl, enumMenu)


# ==============================================================================
# ctrl = "cc_LeftFoot_IK"
# floatMenu = {
#     "world0": "null_worldSpace", 
#     "root1": "null_rootSpace"
#     }
# ctrl = "cc_RightFoot_IK"
# floatMenu = {
#     "world0": "null_worldSpace", 
#     "root1": "null_rootSpace"
#     }
# ctrl = "cc_LeftHand_IK"
# floatMenu = {
#     "world0": "null_worldSpace", 
#     "shoulder1": "null_leftShoulderSpace"
#     }
# ctrl = "cc_RightHand_IK"
# floatMenu = {
#     "world0": "null_worldSpace", 
#     "shoulder1": "null_rightShoulderSpace"
#     }
# ctrl = "cc_Eyes"
# floatMenu = {
#     "world0": "null_worldSpace", 
#     "head1": "null_headSpace"
#     }
# connectSpaceFloat(ctrl, floatMenu)


# ==============================================================================
# constraintList = {
#     "null_worldSpace": ["skeletons", "cc_HipsMain_grp"], 
#     "null_rootSpace": [
#         "cc_LeftUpLeg_IK_grp", 
#         "cc_LeftUpLeg_FK_grp", 
#         "cc_RightUpLeg_IK_grp", 
#         "cc_RightUpLeg_FK_grp", 
#         "rig_Hips", 
#         "cc_Spine_IK_grp", 
#         "cc_Spine_FK_grp"
#         ], 
#     "rig_Spine2": [
#         "cc_LeftShoulder_grp", 
#         "cc_RightShoulder_grp", 
#         "cc_Neck_grp"
#         ], 
#     "null_leftShoulderSpace": ["cc_LeftArm_IK_grp", "cc_LeftArm_FK_grp"], 
#     "null_rightShoulderSpace": ["cc_RightArm_IK_grp", "cc_RightArm_FK_grp"], 
#     "rig_LeftHand": ["cc_LeftHandFingers_grp"], 
#     "rig_RightHand": ["cc_RightHandFingers_grp"], 
#     }
# for parents, child in constraintList.items():
#     for i in child:
#         if i != "skeletons":
#             pm.parentConstraint(parents, i, mo=True, w=1.0)
#         pm.scaleConstraint(parents, i, mo=True, w=1.0)


# ==============================================================================
# showHide = {
#     "cc_IKFK.Spine_IK0FK1": [
#         'cc_Spine_FK_grp', 
#         'cc_Spine_IK_grp', 
#         ], 
#     "cc_IKFK.LArm_IK0FK1": [
#         'cc_LeftArm_FK_grp', 
#         'cc_LeftArm_IK_grp', 
#         'cc_LeftForeArmPoleVector_grp', 
#         'cc_LeftHand_IK_grp', 
#         ], 
#     "cc_IKFK.RArm_IK0FK1": [
#         'cc_RightArm_FK_grp', 
#         'cc_RightArm_IK_grp', 
#         'cc_RightForeArmPoleVector_grp', 
#         'cc_RightHand_IK_grp', 
#         ], 
#     "cc_IKFK.LLeg_IK0FK1": [
#         'cc_LeftUpLeg_FK_grp', 
#         'cc_LeftUpLeg_IK_grp', 
#         'cc_LeftLegPoleVector_grp', 
#         'cc_LeftFoot_IK_grp', 
#         ], 
#     "cc_IKFK.RLeg_IK0FK1": [
#         'cc_RightUpLeg_FK_grp', 
#         'cc_RightUpLeg_IK_grp', 
#         'cc_RightLegPoleVector_grp', 
#         'cc_RightFoot_IK_grp', 
#         ], 
#     }
# for switch, lst in showHide.items():
#     pm.connectAttr(switch, f"{lst[0]}.visibility", f=True)
#     reverseNodeName = pm.shadingNode("reverse", au=True)
#     pm.connectAttr(switch, f"{reverseNodeName}.inputX", f=True)
#     for i in lst[1:]:
#         pm.connectAttr(f"{reverseNodeName}.outputX", f"{i}.visibility", f=True)
        

# ==============================================================================
# connect rigJoints to bindJoints
# for destination in mc.jointPosition.keys():
#     source1 = f"rig_{destination}"
#     connectAttributes(source1, destination, t=True, r=True)


# ==============================================================================
# setDirection_fingerCtrl()


# ==============================================================================
# createRigGroups("pomfretFishC")
# groupOwnPivot()
# sel = pm.ls(sl=True, fl=True)
# print([i.name() for i in sel])
# selectConstraintOnly()
# ctrl = Controllers()
# ctrl.createControllers(sphere="")
# for i in sel:
#     x, y, z = pm.pointPosition(i)
#     print((round(x, 3), round(y, 3), round(z, 3)))
# for i in range(3, 25):
#     pm.connectAttr("plusMinusAverage3.output1D", f"AirTankHose{i}.scaleX", f=True)