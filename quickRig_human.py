import pymel.core as pm
import statistics


class QHGeneral:
    def __init__(self):
        self.rootJnt = 'Hips'
        self.sizeCuv = 'mixamo_boneSample'
        self.cuvScale = 1
        self.position = {
            'Hips': (0.0, 98.223, 1.464), 
            'Spine': (0.0, 107.814, 1.588), 
            'Spine1': (0.0, 117.134, 0.203), 
            'Spine2': (0.0, 125.82, -1.089), 
            'Neck': (0.0, 141.589, -3.019), 
            'Head': (0.0, 150.649, -1.431), 
            'HeadTop_End': (0.0, 171.409, 5.635), 
            'LeftShoulder': (4.305, 136.196, -3.124), 
            'LeftArm': (19.934, 135.702, -5.494), 
            'LeftForeArm': (42.774, 135.702, -6.376), 
            'LeftHand': (63.913, 135.702, -6.131), 
            'LeftHandThumb1': (65.761, 135.008, -2.444), 
            'LeftHandThumb2': (68.495, 133.652, -0.242), 
            'LeftHandThumb3': (70.727, 132.545, 1.556), 
            'LeftHandThumb4': (72.412, 131.709, 2.913), 
            'LeftHandIndex1': (71.683, 134.879, -2.495), 
            'LeftHandIndex2': (74.972, 134.879, -2.495), 
            'LeftHandIndex3': (77.576, 134.879, -2.495), 
            'LeftHandIndex4': (80.181, 134.879, -2.495), 
            'LeftHandMiddle1': (71.566, 134.682, -4.906), 
            'LeftHandMiddle2': (75.085, 134.762, -4.906), 
            'LeftHandMiddle3': (78.171, 134.832, -4.906), 
            'LeftHandMiddle4': (81.57, 134.908, -4.906), 
            'LeftHandRing1': (71.293, 134.575, -6.84), 
            'LeftHandRing2': (74.241, 134.742, -6.84), 
            'LeftHandRing3': (77.231, 134.912, -6.84), 
            'LeftHandRing4': (80.134, 135.078, -6.84), 
            'LeftHandPinky1': (70.702, 134.116, -8.847), 
            'LeftHandPinky2': (73.811, 134.283, -8.847), 
            'LeftHandPinky3': (75.625, 134.38, -8.847), 
            'LeftHandPinky4': (77.461, 134.478, -8.847), 
            'RightShoulder': (-4.305, 136.196, -3.124), 
            'RightArm': (-21.859, 135.702, -5.585), 
            'RightForeArm': (-42.316, 135.702, -6.381), 
            'RightHand': (-63.913, 135.702, -6.131), 
            'RightHandThumb1': (-65.761, 135.008, -2.444), 
            'RightHandThumb2': (-68.495, 133.652, -0.242), 
            'RightHandThumb3': (-70.727, 132.545, 1.556), 
            'RightHandThumb4': (-72.412, 131.709, 2.913), 
            'RightHandIndex1': (-71.683, 134.879, -2.495), 
            'RightHandIndex2': (-74.972, 134.879, -2.495), 
            'RightHandIndex3': (-77.576, 134.879, -2.495), 
            'RightHandIndex4': (-80.181, 134.879, -2.495), 
            'RightHandMiddle1': (-71.565, 134.682, -4.906), 
            'RightHandMiddle2': (-75.085, 134.762, -4.906), 
            'RightHandMiddle3': (-78.171, 134.832, -4.906), 
            'RightHandMiddle4': (-81.569, 134.908, -4.906), 
            'RightHandRing1': (-71.293, 134.575, -6.84), 
            'RightHandRing2': (-74.24, 134.742, -6.84), 
            'RightHandRing3': (-77.231, 134.912, -6.84), 
            'RightHandRing4': (-80.134, 135.078, -6.84), 
            'RightHandPinky1': (-70.702, 134.116, -8.847), 
            'RightHandPinky2': (-73.811, 134.283, -8.847), 
            'RightHandPinky3': (-75.625, 134.38, -8.847), 
            'RightHandPinky4': (-77.461, 134.478, -8.847), 
            'LeftUpLeg': (10.797, 91.863, -1.849), 
            'LeftLeg': (10.797, 50.067, -0.255), 
            'LeftFoot': (10.797, 8.223, -4.39), 
            'LeftToeBase': (10.797, 0.001, 5.7), 
            'LeftToe_End': (10.797, 0.0, 14.439), 
            'RightUpLeg': (-10.797, 91.863, -1.849), 
            'RightLeg': (-10.797, 50.066, -0.255), 
            'RightFoot': (-10.797, 8.223, -4.39), 
            'RightToeBase': (-10.797, 0.001, 5.7), 
            'RightToe_End': (-10.797, 0.0, 14.439), 
            }
        self.hierarchy1 = {
            "spineGroup": [
                'Hips', 
                'Spine', 'Spine1', 'Spine2', 
                'Neck', 
                'Head', 'HeadTop_End'
                ], 
            "L_armGroup": [
                'LeftShoulder', 
                'LeftArm', 
                'LeftForeArm', 
                'LeftHand'
                ], 
            "R_armGroup": [
                'RightShoulder', 
                'RightArm', 
                'RightForeArm', 
                'RightHand'
                ], 
            "L_legGroup": [
                'LeftUpLeg', 
                'LeftLeg', 
                'LeftFoot', 
                'LeftToeBase', 
                'LeftToe_End'
                ], 
            "R_legGroup": [
                'RightUpLeg', 
                'RightLeg', 
                'RightFoot', 
                'RightToeBase', 
                'RightToe_End'
                ], 
            "L_thumbGroup": ['LeftHandThumb%d'%i for i in range(1, 5)], 
            "L_indexGroup": ['LeftHandIndex%d'%i for i in range(1, 5)], 
            "L_middleGroup": ['LeftHandMiddle%d'%i for i in range(1, 5)], 
            "L_ringGroup": ['LeftHandRing%d'%i for i in range(1, 5)], 
            "L_pinkyGroup": ['LeftHandPinky%d'%i for i in range(1, 5)], 
            "R_thumbGroup": ['RightHandThumb%d'%i for i in range(1, 5)], 
            "R_indexGroup": ['RightHandIndex%d'%i for i in range(1, 5)], 
            "R_middleGroup": ['RightHandMiddle%d'%i for i in range(1, 5)], 
            "R_ringGroup": ['RightHandRing%d'%i for i in range(1, 5)], 
            "R_pinkyGroup": ['RightHandPinky%d'%i for i in range(1, 5)], 
        }
        self.hierarchy2 = {
            'Hips': ['LeftUpLeg', 'RightUpLeg'], 
            'Spine2': ['LeftShoulder', 'RightShoulder'], 
            'LeftHand': [
                'LeftHandThumb1', 
                'LeftHandIndex1', 
                'LeftHandMiddle1', 
                'LeftHandRing1', 
                'LeftHandPinky1'
                ], 
            'RightHand': [
                'RightHandThumb1', 
                'RightHandIndex1', 
                'RightHandMiddle1', 
                'RightHandRing1', 
                'RightHandPinky1'
                ], 
        }
        self.curveControllers = {
            "cc_Main": ["cir", (19, 19, 19)], 
            "cc_Sub": ["cir", (15, 15, 15)], 
            "cc_Hips": ["cub", (25, 2, 25)], 
            "cc_HipsSub": ["cir", (8.3, 8.3, 8.3)], 
            "cc_Spline_IK": ["cir", (5, 5, 5)], 
            "cc_Spline1_IK": ["cir", (6, 6, 6)], 
            "cc_Spine_FK": ["cir", (6, 6, 6)], 
            "cc_Spine1_FK": ["cir", (5, 5, 5)], 
            "cc_Spine2_FK": ["cir", (7, 7, 7)], 
            "cc_Neck": ["cir", (4, 4, 4)], 
            "cc_Head": ["head", (1, 1, 1)], 
            "cc_LeftShoulder": ["scapula", (1, 1, 1)], 
            "cc_LeftArm_FK": ["cir", (4, 4, 4)], 
            "cc_LeftForeArm_FK": ["cir", (2.5, 2.5, 2.5)], 
            "cc_LeftHand_FK": ["cir", (2, 2, 2)], 
            "cc_LeftHandThumb1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_LeftHandThumb2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_LeftHandThumb3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_LeftHandIndex1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_LeftHandIndex2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_LeftHandIndex3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_LeftHandMiddle1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_LeftHandMiddle2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_LeftHandMiddle3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_LeftHandRing1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_LeftHandRing2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_LeftHandRing3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_LeftHandPinky1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_LeftHandPinky2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_LeftHandPinky3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_RightShoulder": ["scapula", (1, 1, 1)], 
            "cc_RightArm_FK": ["cir", (4, 4, 4)], 
            "cc_RightForeArm_FK": ["cir", (2.5, 2.5, 2.5)], 
            "cc_RightHand_FK": ["cir", (2, 2, 2)], 
            "cc_RightToeBase_FK": ["cir", (2.5, 2.5, 2.5)], 
            "cc_RightHandThumb1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_RightHandThumb2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_RightHandThumb3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_RightHandIndex1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_RightHandIndex2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_RightHandIndex3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_RightHandMiddle1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_RightHandMiddle2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_RightHandMiddle3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_RightHandRing1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_RightHandRing2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_RightHandRing3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_RightHandPinky1": ["cir", (0.71, 0.71, 0.71)], 
            "cc_RightHandPinky2": ["cir", (0.68, 0.68, 0.68)], 
            "cc_RightHandPinky3": ["cir", (0.65, 0.65, 0.65)], 
            "cc_LeftUpLeg_FK": ["cir", (5, 5, 5)], 
            "cc_LeftLeg_FK": ["cir", (3.5, 3.5, 3.5)], 
            "cc_LeftFoot_FK": ["cir", (3, 3, 3)], 
            "cc_LeftToeBase_FK": ["cir", (2.5, 2.5, 2.5)], 
            "cc_RightUpLeg_FK": ["cir", (5, 5, 5)], 
            "cc_RightLeg_FK": ["cir", (3.5, 3.5, 3.5)], 
            "cc_RightFoot_FK": ["cir", (3, 3, 3)], 
            "cc_LeftArm_IK": ["sqr", (8, 8, 8)], 
            "cc_LeftForeArm_IK": ["sph", (4, 4, 4)], 
            "cc_LeftHand_IK": ["cub", (4, 4, 4)], 
            "cc_RightArm_IK": ["sqr", (8, 8, 8)], 
            "cc_RightForeArm_IK": ["sph", (4, 4, 4)], 
            "cc_RightHand_IK": ["cub", (4, 4, 4)], 
            "cc_LeftUpLeg_IK": ["sqr", (10, 10, 10)], 
            "cc_LeftLeg_IK": ["sph", (4, 4, 4)], 
            "cc_LeftFoot_IK": ["foot", (1.4, 1.4, 1.4)], 
            "cc_RightUpLeg_IK": ["sqr", (10, 10, 10)], 
            "cc_RightLeg_IK": ["sph", (4, 4, 4)], 
            "cc_RightFoot_IK": ["foot", (1.4, 1.4, 1.4)], 
        }


    def checkSameNameCurve(self):
        obj = pm.ls()
        if self.sizeCuv in obj:
            return True
        else:
            return False


    def orientJoints(self):
        for lst in self.hierarchy1.values():
            jntList = pm.ls(lst)
            initJnt = jntList[0]
            jntName = initJnt.name()
            if "LeftShoulder" in jntName or "LeftHand" in jntName:
                pri = 'yxz'
                sec = 'zdown'
            elif "RightShoulder" in jntName or "RightHand" in jntName:
                pri = 'yxz'
                sec = 'zup'
            else:
                pri = 'yzx'
                sec = 'zup'
            pm.makeIdentity(jntList, a=True, jo=True, n=0)
            pm.joint(initJnt, e=True, oj=pri, sao=sec, ch=True, zso=True)
            endJoint = [i for i in jntList if not i.getChildren()]
            for i in endJoint:
                pm.joint(i, e=True, oj='none', ch=True, zso=True)


    def parentParts(self):
        """ Combine the torso, arms, legs, and finger groups 
        to make them one body. 
         """
        for j, k in self.hierarchy2.items():
            for i in k:
                pm.parent(i, j)


    # def getScaleAverage(self, obj=None):
    #     """ Returns the scale average of the given argument. """
    #     if not obj:
    #         return
    #     else:
    #         tmp = pm.getAttr(f"{obj}.scale")
    #         result = statistics.mean(tmp)
    #         result = round(result, 3)
    #         return result


    def finish(self):
        if self.checkSameNameCurve():
            cuv = self.sizeCuv
        else:
            cuv = pm.circle(nr=(0, 1, 0), n=self.sizeCuv, ch=0, r=50)
        pm.parent(self.rootJnt, cuv)
        pm.select(cl=True)


    def seperateParts(self):
        """ Separate the torso, arms, legs, and finger groups 
        to make them unparent. 
         """
        pm.makeIdentity(self.sizeCuv, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(self.rootJnt, w=True)
        for i in self.hierarchy2.values():
            for j in i:
                pm.parent(j, w=True)


    def ctrl(self, ccName, ccType):
        """ Create a controller,
        "cir": cir, 
        "cub": cub, 
        "foot": foot, 
        "hat": hat, 
        "head": head, 
        "scapula": scapula, 
        "sph": sph, 
        "sqr": sqr, 
        """
        # Circle
        cir = [(0, 0, -3), (-2, 0, -2), (-3, 0, 0), ]
        cir += [(-2, 0, 2), (0, 0, 3), (2, 0, 2), ]
        cir += [(3, 0, 0), (2, 0, -2), (0, 0, -3), ]
        # Cube
        cub = [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), ]
        cub += [(1, 1, -1), (-1, 1, -1), (-1, -1, -1), ]
        cub += [(-1, -1, 1), (1, -1, 1), (1, -1, -1), ]
        cub += [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), ]
        cub += [(1, 1, 1), (1, -1, 1), (1, -1, -1), ]
        cub += [(1, 1, -1), ]
        # Foot
        foot = [(-4, 0, -4), (-4, 0, -7), (-3, 0, -11), ]
        foot += [(-1, 0, -12), (0, 0, -12), (1, 0, -12), ]
        foot += [(3, 0, -11), (4, 0, -7), (4, 0, -4), ]
        foot += [(-4, 0, -4), (-5, 0, 1), (-5, 0, 6), ]
        foot += [(-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), ]
        foot += [(2, 0, 15), (4, 0, 12), (5, 0, 6), ]
        foot += [(5, 0, 1), (4, 0, -4), (-4, 0, -4), ]
        foot += [(4, 0, -4), ]
        # hat
        hat = [(14, 9, 0), (0, 15, 0), (-14, 9, 0), ]
        hat += [(-7, -5, 0), (-29, -7, 0), (0, -7, 0), ]
        hat += [(29, -7, 0), (7, -5, 0), (14, 9, 0), ]
        # head
        head = [(13, 15, -11), (0, 25, -15), (-13, 15, -11), ]
        head += [(-14, 6, 0), (-13, 15, 11), (0, 25, 15), ]
        head += [(13, 15, 11), (14, 6, 0), (13, 15, -11), ]
        # scapula
        scapula = [(2, 10, -11), (0, 0, -11), (-2, 10, -11), ]
        scapula += [(-3, 18, 0), (-2, 10, 11), (0, 0, 11), ]
        scapula += [(2, 10, 11), (3, 18, 0), (2, 10, -11), ]
        # Sphere
        sph = [(0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), ]
        sph += [(0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), ]
        sph += [(0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), ]
        sph += [(-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), ]
        sph += [(0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), ]
        sph += [(0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), ]
        sph += [(-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), ]
        sph += [(0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), ]
        sph += [(0, 1, 0), ]
        # Square
        sqr = [(1, 0, 1), (1, 0, -1), (-1, 0, -1), ]
        sqr += [(-1, 0, 1), (1, 0, 1)]
        # Dictionary
        ctrl = {
            "cir": cir, 
            "cub": cub, 
            "sph": sph, 
            "foot": foot, 
            "hat": hat, 
            "head": head, 
            "scapula": scapula, 
            "sqr": sqr, 
        }
        coordinate = []
        if not ccType in ctrl.keys():
            return
        else:
            coordinate.append(ctrl[ccType])
            result = [pm.curve(d=1, p=i, n=ccName) for i in coordinate]
            return result
            

    def groupingEmpty(self, obj=None):
        """ Create an empty group and match the position. """
        if not obj:
            return
        result = pm.group(em=True, n = obj + "_grp")
        pm.matchTransform(result, obj, pos=True, rot=True)
        pm.parent(obj, result)
        return result


class CreateMixamoBones(QHGeneral):
    def __init__(self):
        super().__init__()


    def main(self):
        if self.checkSameNameCurve():
            return
        else:
            self.createJoints()
            self.makeHierarchy()
            self.orientJoints()
            self.parentParts()
            self.finish()


    def createJoints(self):
        for j, k in self.position.items():
            pm.select(cl=True)
            pm.joint(p=k, n=j)


    def makeHierarchy(self):
        for lst in self.hierarchy1.values():
            num = len(lst) - 1
            for i in range(num):
                pm.parent(lst[i+1], lst[i])


class SymmetryBothSide(QHGeneral):
    def __init__(self, LR=None):
        """ L or R as a parameter """
        super().__init__()
        self.LR = LR
        if not self.LR:
            pass
        elif self.LR == "L":
            self.side = "Left"
            self.otherSide = "Right"
        elif self.LR == "R":
            self.side = "Right" 
            self.otherSide = "Left"
        else:
            pass


    def main(self):
        self.seperateParts()
        if self.LR:
            self.mirrorPosition()
        self.orientJoints()
        self.parentParts()
        self.finish()
        
    
    def mirrorPosition(self):
        grp = ["arm", "leg", "thumb", "index", "middle", "ring", "pinky"]
        for i in grp:
            sideList = self.hierarchy1[f"{self.LR}_{i}Group"]
            for j in sideList:
                sidePos = pm.xform(j, q=True, ws=True, rp=True)
                x, y, z = sidePos
                _x = x * -1
                otherSidePos = [_x, y, z]
                otherSideJnt = j.replace(self.side, self.otherSide)
                pm.move(otherSideJnt, otherSidePos)


class AlignBonesCenter(QHGeneral):
    def __init__(self):
        super().__init__()
        self.centeredBones = self.hierarchy1["spineGroup"]
        self.centeredBones.append(self.sizeCuv)
    

    def main(self):
        self.seperateParts()
        locators = self.attachLocator()
        notCenteredLoc = self.notCenteredLocator(locators)
        self.arrangeCenter(notCenteredLoc)
        self.orientJoints()
        self.parentParts()
        pm.makeIdentity(self.sizeCuv, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.delete(locators)
        pm.parent(self.rootJnt, self.sizeCuv)


    def attachLocator(self) -> list:
        allObjects = pm.ls()
        result = []
        for boneName in self.centeredBones:
            bn = f"loc_{boneName}"
            if bn in allObjects:
                loc = pm.PyNode(bn)
            else:
                loc = pm.spaceLocator(n=bn)
            pm.matchTransform(loc, boneName, pos=True)
            result.append(loc)
        return result


    def notCenteredLocator(self, locators: list):
        result = []
        for loc in locators:
            x = loc.getTranslation()[0]
            x = round(x, 3)
            if x:
                result.append(loc)
            else:
                continue
        return result


    def arrangeCenter(self, lst: list):
        if not lst:
            return
        else:
            for loc in lst:
                x, y, z = loc.getTranslation()
                pm.move(loc, (0, y, z))
            for i in self.centeredBones:
                pm.matchTransform(i, f"loc_{i}", pos=True)


class CreateControllers(QHGeneral):
    def __init__(self):
        super().__init__()
        self.main()


    def main(self):
        self.createCC(self.curveControllers)
        self.matchPosition(self.curveControllers)


    def createCC(self, ccDict):
        """ Create a curve control, 
        name it, set its type, and group it.
         """
        for ccName, info in ccDict.items():
            if pm.objExists(ccName):
                continue
            ccType, ccSize = info
            cc = self.ctrl(ccName, ccType)
            if not cc:
                continue
            cc = cc[0]
            grp = self.groupingEmpty(cc)
            pm.scale(grp, ccSize)
            pm.makeIdentity(grp, a=1, s=1, n=0, pn=1)


    def rigHips(self):
        """ 1. Create a rig joint by copying the Hips joint.
        2. Place the controller at the joint's position.
        3. Match sub-controllers to Hips main controller and include.
        4. Set parent and scale between controllers and joints.
         """
        pass


    def rigSpine(self):
        pass


    def rigHead(self):
        pass


    def rigNeck(self):
        pass


    def rigScapula(self):
        pass


    def rigFingers(self):
        pass


    def rigArms(self):
        pass


    def rigLegs(self):
        pass


    def matchPosition(self, ccDict):
        for ccName in ccDict.keys():
            boneName = ccName.split("_")[1]
            if not boneName in self.position:
                continue
            grpName = ccName + "_grp"
            pm.matchTransform(grpName, boneName, pos=True, rot=True)



# 79 char line ================================================================
# 72 docstring or comments line ========================================


# cmb = CreateMixamoBones()
# cmb.main()


# ac = AlignBonesCenter()
# ac.main()


# sbs = SymmetryBothSide("L")
# sbs.main()


# cc = CreateControllers()


