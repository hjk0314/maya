from collections import Iterable
import pymel.core as pm


class QuickRig_Mixamo:
    def __init__(self):
        self.side = ["Left", "Right"]
        self.arms = ["Shoulder", "Arm", "ForeArm", "Hand"]
        self.legs = ["UpLeg", "Leg", "Foot", "ToeBase", "Toe_End"]
        finger = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        self.finger = [f"Hand{i}" for i in finger]
        self.spines = ["Spine", "Spine1", "Spine2"]
        self.spines += ["Neck", "Head", "HeadTop_End"]
        self.mainCurve = "mainCurve"
        self.rootJoint = "Hips"
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
            "Hips": 
                [self.spines] + [[i+g for g in self.legs] for i in self.side], 
            "Spine2": 
                [[i+j for j in self.arms] for i in self.side],  
            "LeftHand": 
                [[f"Left{i}{n}" for n in range(1, 5)] for i in self.finger], 
            "RightHand": 
                [[f"Right{i}{n}" for n in range(1, 5)] for i in self.finger], 
        }


    def createMixamoBones(self):
        self.cleanObjects(self.mainCurve, self.jointPosition.keys())
        self.createJointWithName(self.jointPosition)
        self.buildJointsHumanStructure(self.hierarchy)
        self.matchMainCurveToJointSize(self.rootJoint, self.mainCurve)
        pm.parent(self.rootJoint, self.mainCurve)


    def alignSpinesCenter(self):
        spineJoints = [self.rootJoint] + self.spines
        self.updateAllJointPositions()
        self.moveJointsGridZero(spineJoints)
        self.createMixamoBones()


    def sameBothSide(self, direction: str="LeftToRight"):
        self.updateAllJointPositions()
        sideA, sideB = self.getJointNameBothSide(direction)
        self.updateBothSideToSame(sideA, sideB)
        self.createMixamoBones()


    def createAllRigJoints(self):
        self.updateAllJointPositions()
        positions = self.jointPosition
        hierarchy = self.hierarchy
        data = self.getDataWithNewName(positions, hierarchy, "rig_")
        rigPositions, rigHierarchy = data
        self.cleanObjects(rigPositions)
        self.createJointWithName(rigPositions)
        self.buildJointsHumanStructure(rigHierarchy)


    def createIKFKSpinesJoints(self, *arg):
        self.updateAllJointPositions()
        spinesPositions, spinesHierarchy = self.getDataIKFKSpines(arg)
        self.cleanObjects(spinesHierarchy.values())
        self.createJointWithName(spinesPositions)
        self.buildJointsHumanStructure(spinesHierarchy)


    def createIKFKArmsJoints(self, *arg):
        self.updateAllJointPositions()
        armsPositions, armsHierarchy = self.getDataIKFKArms(arg)
        self.cleanObjects(armsHierarchy.values())
        self.createJointWithName(armsPositions)
        self.buildJointsHumanStructure(armsHierarchy)


    def createIKFKLegsJoints(self, *arg):
        self.updateAllJointPositions()
        legsPositions, legsHierarchy = self.getDataIKFKLegs(arg)
        self.cleanObjects(legsHierarchy.values())
        self.createJointWithName(legsPositions)
        self.buildJointsHumanStructure(legsHierarchy)


    def createIKArmsControllers(self, *arg):
        # self.getFlattenList(arg)
        # used class
        ctrl = Controllers()
        jnt = Joints()
        grp = Grouping()
        # input joints name
        firstJoint = "rig_LeftArm_IK"
        middleJoint = "rig_LeftForeArm_IK"
        endJoint = "rig_LeftHand_IK"
        # Create ctrl name and check exists
        ccNames = [i.replace("rig_", "cc_") for i in [firstJoint, middleJoint, endJoint]]
        isCCExist = [pm.objExists(i) for i in ccNames]
        if any(isCCExist):
            pm.warning("Same contollers aleady exist.")
            return
        rowCtrl = ctrl.createControllers("circle", "sphere", "cube")
        print(rowCtrl)
        ccCircle, ccSphere, ccCube = ccNames
        for row, new in zip(rowCtrl, ccNames):
            pm.rename(row, new)
        # Rig - firstJoint
        ikH = pm.ikHandle(sj=firstJoint, ee=endJoint, sol="ikRPsolver")[0]
        pm.rotate(ccCircle, [0, 0, 90])
        pm.makeIdentity(ccCircle, a=True, t=0, r=1, s=0, jo=0, n=0, pn=1)
        pm.matchTransform(ccCircle, firstJoint, pos=True)
        pm.pointConstraint(ccCircle, firstJoint, mo=True)
        # Rig - middleJoint
        polevectorJoints = jnt.createPolevectorJoint([firstJoint, middleJoint, endJoint])
        startJointOfPolevector, endJointOfPolevector = polevectorJoints
        pm.matchTransform(ccSphere, endJointOfPolevector, pos=True)
        # pm.delete(startJointOfPolevector)
        pm.poleVectorConstraint(ccSphere, ikH, w=1)
        # Rig - endJoint
        pm.matchTransform(ccCube, endJoint, pos=True)
        pm.orientConstraint(endJoint, ccCube, o=(-90, 0, 90), w=1)
        pm.delete(ccCube, cn=True)
        pm.orientConstraint(ccCube, endJoint, mo=True, w=1)
        # Rig - cleanUp
        ccNamesGroup = grp.groupingWithOwnPivot(ccNames)
        armGroupName = ccCircle.rsplit("_", 1)[0]
        pm.group(em=True, n=armGroupName)
        for i in ccNamesGroup:
            pm.parent(i, armGroupName)
        pm.setAttr(f"{ikH}.visibility", 0)
        pm.parent(ikH, ccCube)




# 79 char line ================================================================
# 72 docstring or comments line ======================================== 


    def cleanObjects(self, *args):
        for element in args:
            isStr = isinstance(element, str)
            isIter = isinstance(element, Iterable)
            if not isStr and isIter:
                for i in element:
                    self.cleanObjects(i)
            else:
                try:
                    pm.delete(element)
                except:
                    pass


    def updateAllJointPositions(self):
        allJoints = self.jointPosition.keys()
        for joint in allJoints:
            position = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = tuple(position)


    def updateBothSideToSame(self, sideA, sideB):
        for idx, joint in enumerate(sideA):
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[sideB[idx]] = (x*-1, y, z)


    # def createJointWithName(self, nameAndPosition: dict):
    #     for jointName, position in nameAndPosition.items():
    #         pm.select(cl=True)
    #         pm.joint(p=position, n=jointName)


    def buildJointsHumanStructure(self, hierarchyStructure: dict):
        for parents, bothSideList in hierarchyStructure.items():
            for jointList in bothSideList:
                self.parentHierarchically(jointList)
                self.orientJointsMixamoType(jointList)
                self.parentHierarchically([parents, jointList[0]])


    def matchMainCurveToJointSize(self, object: str, curveName: str):
        objectBoundingBox = pm.xform(object, q=True, bb=True, ws=True)
        x1, y1, z1, x2, y2, z2 = objectBoundingBox
        x = (x2 - x1) / 2
        y = (y2 - y1) / 2
        z = (z2 - z1) / 2
        objectSize = max(x, z)
        objectSize = round(objectSize, 3)
        pm.circle(nr=(0, 1, 0), n=curveName, ch=0, r=objectSize)


    def moveJointsGridZero(self, joints: list):
        for joint in joints:
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = (0, y, z)


    def getJointNameBothSide(self, twoOptions: str) -> list:
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


    def parentHierarchically(self, selections: list=[]):
        if not selections:
            selections = pm.selected()
        for idx, upper in enumerate(selections):
            try:
                lower = selections[idx + 1]
                pm.parent(lower, upper)
            except:
                continue


    def orientJointsMixamoType(self, jointList=[]):
        firstJoint = jointList[0]
        ls = "LeftShoulder"
        la = "LeftArm"
        lh = "LeftHand"
        rs = "RightShoulder"
        ra = "RightArm"
        rh = "RightHand"
        if ls in firstJoint or la in firstJoint or lh in firstJoint:
            primaryAxis = 'yxz'
            secondaryAxis = 'zdown'
        elif rs in firstJoint or ra in firstJoint or rh in firstJoint:
            primaryAxis = 'yxz'
            secondaryAxis = 'zup'
        else:
            primaryAxis = 'yzx'
            secondaryAxis = 'zup'
        orientJoints(jointList, primaryAxis, secondaryAxis)


    def selectJointOnly(self) -> list:
        transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
        result = []
        for i in transformNodes:
            iType = pm.objectType(i)
            if iType == 'joint':
                result.append(i)
            else:
                continue
        pm.select(result)
        return result


    def getPosition(self, selection) -> list:
        try:
            position = pm.pointPosition(selection)
        except:
            position = pm.xform(selection, q=1, ws=1, rp=1)
        return position


    def getDataWithNewName(self, positions: dict, hierarchy: dict, \
        foreword="", tailword=""):
        """ Returns the data with a new name. 
        - positions = {str: (float, float, float), ...}
        - hierarchy = {str: [[ ],[ ]], ...}
         """
        result1 = {}
        for jnt, pos in positions.items():
            result1[f"{foreword}{jnt}{tailword}"] = pos 
        result2 = {}
        for parents, hierarchy in hierarchy.items():
            key = f"{foreword}{parents}{tailword}"
            val = [[f"{foreword}{j}{tailword}" for j in i] for i in hierarchy]
            result2[key] = val
        return result1, result2


    def getDataIKFKSpines(self, *IKFK):
        IKFK = self.getFlattenList(IKFK)
        sourceSpines = self.spines[:3]
        sourceHierarchy = {"Hips": [sourceSpines]}
        spinesPositions = {}
        for i in sourceSpines:
            for k in IKFK:
                spinesPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        spinesHierarchy = {}
        for parents, c in sourceHierarchy.items():
            key = f"rig_{parents}"
            value = [[f"rig_{i}_{k}" for i in h] for h in c for k in IKFK]
            spinesHierarchy[key] = value
        return spinesPositions, spinesHierarchy


    def getDataIKFKArms(self, *args):
        """ Creates a joint with the input string, 
        Returns positions and hierarchy.
        >>> self.getDataIKFKArms("IK", "FK", ...)
        >>> rig_Hand_IK, rig_Hand_FK, rig_Hand_...
        >>> armsPositions = {"rig_Hand_IK": (0, 1, 2), "rig_Hand_FK": (3, 4, 5), ...}
        >>> armsHierarchy = {"rig_ForeArm": ["rig_Hand_IK", "rig_Hand_FK"]}
         """
        ikOrFk = self.getFlattenList(args)
        sourceArms = [i + m for m in self.arms[1:] for i in self.side]
        sourceHierarchy = {i[0]: [i[1:]] for i in self.hierarchy["Spine2"]}
        armsPositions = {}
        for i in sourceArms:
            for k in ikOrFk:
                armsPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        armsHierarchy = {}
        for parents, hierarchy in sourceHierarchy.items():
            for h in hierarchy:
                key = f"rig_{parents}"
                value = [[f"rig_{i}_{k}" for i in h] for k in ikOrFk]
                armsHierarchy[key] = value
        return armsPositions, armsHierarchy


    def getDataIKFKLegs(self, *IKFK):
        IKFK = self.getFlattenList(IKFK)
        sourceLegs = [i + g for g in self.legs for i in self.side]
        sourceHierarchy = {"Hips": self.hierarchy["Hips"][1:]}
        legsPositions = {}
        for i in sourceLegs:
            for k in IKFK:
                legsPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        legsHierarchy = {}
        for parents, c in sourceHierarchy.items():
            key = f"rig_{parents}"
            value = [[f"rig_{i}_{k}" for i in h] for h in c for k in IKFK]
            legsHierarchy[key] = value
        return legsPositions, legsHierarchy


    def getFlattenList(self, *args):
        result = []
        for arg in args:
            if not isinstance(arg, str) and isinstance(arg, Iterable):
                for i in arg:
                    result.extend(self.getFlattenList(i))
            else:
                result.append(arg)
        return result


    def createRigGroup(self, assetName: str):
        topGroupName = assetName if assetName else "assetName"
        rigGroupHierarchy = {
            topGroupName: ["rig", "MODEL"], 
            "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
            "skeletons": ["bindBones", "rigBones"]
            }
        for parent, children in rigGroupHierarchy.items():
            if not pm.objExists(parent):
                pm.group(em=True, n=parent)
            for child in children:
                if not pm.objExists(child):
                    pm.group(em=True, n=child)
                pm.parent(child, parent)

