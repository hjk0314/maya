import pymel.core as pm


class BoneNames:
    def __init__(self):
        self.rootJnt = 'Hips'
        self.sizeCuv = 'mixamo_boneSample'
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


class CreateMixamoBones(BoneNames):
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


    def parentParts(self):
        """ Combine the torso, arms, legs, and finger groups 
        to make them one body. 
         """
        for j, k in self.hierarchy2.items():
            for i in k:
                pm.parent(i, j)


    def checkSameNameCurve(self):
        obj = pm.ls()
        if self.sizeCuv in obj:
            return True
        else:
            return False


    def makeHierarchy(self):
        for lst in self.hierarchy1.values():
            num = len(lst) - 1
            for i in range(num):
                pm.parent(lst[i+1], lst[i])


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


    def finish(self):
        if self.checkSameNameCurve():
            cuv = self.sizeCuv
        else:
            cuv = pm.circle(nr=(0, 1, 0), n=self.sizeCuv, ch=0, r=50)
        pm.parent(self.rootJnt, cuv)
        pm.select(cl=True)


class SymmetryBothSide(CreateMixamoBones):
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


    def seperateParts(self):
        """ Separate the torso, arms, legs, and finger groups 
        to make them unparent. 
         """
        pm.makeIdentity(self.sizeCuv, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(self.rootJnt, w=True)
        for i in self.hierarchy2.values():
            for j in i:
                pm.parent(j, w=True)


class AlignBonesCenter(SymmetryBothSide):
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
        



# 79 char line ================================================================
# 72 docstring or comments line ========================================


# cmb = CreateMixamoBones()
# cmb.main()


sbs = SymmetryBothSide("R")
sbs.main()


ac = AlignBonesCenter()
ac.main()


