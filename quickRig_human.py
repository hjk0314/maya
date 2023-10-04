import pymel.core as pm


class QHGeneral:
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


class CreateControllers:
    def __init__(self):
        pass


    def ctrl(self, **kwargs):
        """ Create a controller,
        "cir": cir, 
        "cub": cub, 
        "sph": sph, 
        "cyl": cyl, 
        "pip": pip, 
        "con1": con1, 
        "con2" : con2, 
        "car": car, 
        "car2": car2, 
        "car3": car3, 
        "ar1": ar1, 
        "ar2": ar2, 
        "ar3": ar3, 
        "ar4": ar4, 
        "ar5": ar5, 
        "pointer": pointer, 
        "foot": foot, 
        "foot2": foot2, 
        "hoof": hoof, 
        "hoof2": hoof2, 
        "sqr": sqr, 
        "cross": cross, 
        "hat": hat, 
        "head": head, 
        "scapula": scapula, 
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
        # Cylinder
        cyl = [(-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), ]
        cyl += [(0.7, 1, 0.7), (1, 1, 0), (0.7, 1, -0.7), ]
        cyl += [(0, 1, -1), (0, 1, 1), (0, -1, 1), ]
        cyl += [(-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), ]
        cyl += [(0, -1, -1), (0.7, -1, -0.7), (1, -1, 0), ]
        cyl += [(0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), ]
        cyl += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
        cyl += [(1, 1, 0), (1, -1, 0), (-1, -1, 0), ]
        cyl += [(-1, 1, 0), ]
        # Pipe
        pip = [(0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), ]
        pip += [(1, -1, 0), (1, 1, 0), (0.7, 1, -0.7), ]
        pip += [(0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), ]
        pip += [(-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), ]
        pip += [(0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), ]
        pip += [(1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), ]
        pip += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
        pip += [(-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1), ]
        # Cone1
        con1 = [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), ]
        con1 += [(0, 2, 0), (0, 0, 1), (-0.87, 0, -0), ]
        con1 += [(0.87, 0, 0), (0, 0, 1), ]
        # Cone2
        con2 = [(-1, 0, -0), (-0, 0, 1), (1, 0, 0), ]
        con2 += [(0, 0, -1), (-1, 0, -0), (0, 2, 0), ]
        con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0), ]
        con2 += [(0, 0, -1), (0, 0, -1), (-1, 0, -0), ]
        con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0)]
        # car
        car = [(81, 70, 119), (89, 56, 251), (89, -12, 251), ]
        car += [(89, -12, 117), (89, -12, -117), (89, -12, -229), ]
        car += [(81, 70, -229), (81, 70, -159), (69, 111, -105), ]
        car += [(69, 111, 63), (81, 70, 119), (-81, 70, 119), ]
        car += [(-89, 56, 251), (-89, -12, 251), (-89, -12, 117), ]
        car += [(-89, -12, -117), (-89, -12, -229), (-81, 70, -229), ]
        car += [(-81, 70, -159), (-69, 111, -105), (69, 111, -105), ]
        car += [(81, 70, -159), (-81, 70, -159), (-81, 70, -229), ]
        car += [(81, 70, -229), (89, -12, -229), (-89, -12, -229), ]
        car += [(-89, -12, -117), (-89, -12, 117), (-89, -12, 251), ]
        car += [(89, -12, 251), (89, 56, 251), (-89, 56, 251), ]
        car += [(-81, 70, 119), (-69, 111, 63), (-69, 111, -105), ]
        car += [(69, 111, -105), (69, 111, 63), (-69, 111, 63), ]
        # car2
        car2 = [(165, 0, -195), (0, 0, -276), (-165, 0, -195), ]
        car2 += [(-97, 0, -0), (-165, -0, 195), (-0, -0, 276), ]
        car2 += [(165, -0, 195), (97, -0, 0), (165, 0, -195), ]
        # Car3
        car3 = [(212, 0, -212), (0, 0, -300), (-212, 0, -212), ]
        car3 += [(-300, 0, 0), (-212, 0, 212), (0, 0, 300), ]
        car3 += [(212, 0, 212), (300, 0, 0), (212, 0, -212), ]
        # Arrow1
        ar1 = [(0, 0, 2), (2, 0, 1), (1, 0, 1), ]
        ar1 += [(1, 0, -2), (-1, 0, -2), (-1, 0, 1), ]
        ar1 += [(-2, 0, 1), (0, 0, 2), ]
        # Arrow2
        ar2 = [(0, 1, 4), (4, 1, 2), (2, 1, 2), ]
        ar2 += [(2, 1, -4), (-2, 1, -4), (-2, 1, 2), ]
        ar2 += [(-4, 1, 2), (0, 1, 4), (0, -1, 4), ]
        ar2 += [(4, -1, 2), (2, -1, 2), (2, -1, -4), ]
        ar2 += [(-2, -1, -4), (-2, -1, 2), (-4, -1, 2), ]
        ar2 += [(0, -1, 4), (4, -1, 2), (4, 1, 2), ]
        ar2 += [(2, 1, 2), (2, 1, -4), (2, -1, -4), ]
        ar2 += [(-2, -1, -4), (-2, 1, -4), (-2, 1, 2), ]
        ar2 += [(-4, 1, 2), (-4, -1, 2), ]
        # Arrow3
        ar3 = [(7, 0, 0), (5, 0, -5), (0, 0, -7), ]
        ar3 += [(-5, 0, -5), (-7, 0, 0), (-5, 0, 5), ]
        ar3 += [(0, 0, 7), (5, 0, 5), (7, 0, 0), ]
        ar3 += [(5, 0, 2), (7, 0, 3), (7, 0, 0), ]
        # Arrow4
        ar4 = [(0, 0, -11), (-3, 0, -8), (-2.0, 0, -8), ]
        ar4 += [(-2, 0, -6), (-5, 0, -5), (-6, 0, -2), ]
        ar4 += [(-8, 0, -2), (-8, 0, -3), (-11, 0, 0), ]
        ar4 += [(-8, 0, 3), (-8, 0, 2), (-6, 0, 2), ]
        ar4 += [(-5, 0, 5), (-2, 0, 6), (-2, 0, 8), ]
        ar4 += [(-3, 0, 8), (0, 0, 11), (3, 0, 8), ]
        ar4 += [(2, 0, 8), (2, 0, 6), (5, 0, 5), ]
        ar4 += [(6, 0, 2), (8, 0, 2), (8, 0, 3), ]
        ar4 += [(11, 0, 0), (8, 0, -3), (8, 0, -2), ]
        ar4 += [(6, 0, -2), (5, 0, -5), (2, 0, -6), ]
        ar4 += [(2, 0, -8), (3, 0, -8), (0, 0, -11), ]
        # Arrow5
        ar5 = [(-2, 0, -1), (2, 0, -1), (2, 0, -2), ]
        ar5 += [(4, 0, 0), (2, 0, 2), (2, 0, 1), ]
        ar5 += [(-2, 0, 1), (-2, 0, 2), (-4, 0, 0), ]
        ar5 += [(-2, 0, -2), (-2, 0, -1), ]
        # Arrow6
        ar6 = [(-6.3, 6, 0), (-6.5, 4, 0), (-5, 5, 0)]
        ar6 += [(-6.3, 6, 0), (-6, 5, 0), (-5, 3, 0)]
        ar6 += [(-3, 1, 0), (0, 0, 0), (3, 1, 0)]
        ar6 += [(5, 3, 0), (6, 5, 0), (6.3, 6, 0)]
        ar6 += [(5, 5, 0), (6.5, 4, 0), (6.3, 6, 0), ]
        # Pointer
        pointer = [(-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), ]
        pointer += [(0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), ]
        pointer += [(0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), ]
        pointer += [(0, 0, 0), (0, 2, 0), ]
        # Foot
        foot = [(-4, 0, -4), (-4, 0, -7), (-3, 0, -11), ]
        foot += [(-1, 0, -12), (0, 0, -12), (1, 0, -12), ]
        foot += [(3, 0, -11), (4, 0, -7), (4, 0, -4), ]
        foot += [(-4, 0, -4), (-5, 0, 1), (-5, 0, 6), ]
        foot += [(-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), ]
        foot += [(2, 0, 15), (4, 0, 12), (5, 0, 6), ]
        foot += [(5, 0, 1), (4, 0, -4), (-4, 0, -4), ]
        foot += [(4, 0, -4), ]
        # foot2
        foot2 = [(-6, 12, -14), (-6, 12, 6), (6, 12, 6), ]
        foot2 += [(6, 12, -14), (-6, 12, -14), (-6, 0, -14), ]
        foot2 += [(-6, 0, 18), (6, 0, 18), (6, 0, -14), ]
        foot2 += [(-6, 0, -14), (-6, 0, 18), (-6, 12, 6), ]
        foot2 += [(6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14), ]
        # Hoof
        hoof = [(-6, 0, -5), (-6.5, 0, -1), (-6, 0, 3), ]
        hoof += [(-5.2, 0, 5.5), (-3, 0, 7.5), (0, 0, 8.2), ]
        hoof += [(3, 0, 7.5), (5.2, 0, 5.5), (6, 0, 3), ]
        hoof += [(6.5, 0, -1), (6, 0, -5), (4, 0, -5), ]
        hoof += [(4.5, 0, -1), (4, 0, 3), (3.5, 0, 4.5), ]
        hoof += [(2, 0, 6), (0, 0, 6.5), (-2, 0, 6), ]
        hoof += [(-3.5, 0, 4.5), (-4, 0, 3), (-4.5, 0, -1), ]
        hoof += [(-4, 0, -5), (-6, 0, -5), (-5.5, 0, -6.5), ]
        hoof += [(5.5, 0, -6.5), (4.5, 0, -10), (2.2, 0, -12.2), ]
        hoof += [(0, 0, -12.2), (-2.2, 0, -12.2), (-4.5, 0, -10), ]
        hoof += [(-5.5, 0, -6.5), ]
        # Hoof2
        hoof2 = [(6, 6, -12), (0, 8, -12), (-6, 6, -12), ]
        hoof2 += [(-8, 3, -13), (-8, 0, -12), (-7, 0, -10), ]
        hoof2 += [(-8, 0, -6), (-9, 0, -1), (-8, 0, 4), ]
        hoof2 += [(-5, 0, 9), (0, 0, 10), (5, 0, 9), ]
        hoof2 += [(8, 0, 4), (9, 0, -1), (8, 0, -6), ]
        hoof2 += [(7, 0, -10), (8, 0, -12), (8, 3, -13), ]
        hoof2 += [(6, 6, -12), ]
        # Square
        sqr = [(0, 1, 1), (0, 1, -1), (0, -1, -1), ]
        sqr += [(0, -1, 1), (0, 1, 1)]
        # Cross
        cross = [(0, 5, 1), (0, 5, -1), (0, 1, -1), ]
        cross += [(0, 1, -5), (0, -1, -5), (0, -1, -1), ]
        cross += [(0, -5, -1), (0, -5, 1), (0, -1, 1), ]
        cross += [(0, -1, 5), (0, 1, 5), (0, 1, 1), ]
        cross += [(0, 5, 1), ]
        # hat
        hat = [(14, 9, 0), (0, 15, 0), (-14, 9, 0), ]
        hat += [(-7, -5, 0), (-29, -7, 0), (0, -7, 0), ]
        hat += [(29, -7, 0), (7, -5, 0), (14, 9, 0), ]
        # head
        head = [(13, 0, -11), (0, 10, -15), (-13, 0, -11), ]
        head += [(-14, -9, 0), (-13, 0, 11), (0, 10, 15), ]
        head += [(13, 0, 11), (14, -9, 0), ]
        # scapula
        scapula = [(2, 10, -11), (0, 0, -11), (-2, 10, -11), ]
        scapula += [(-3, 18, 0), (-2, 10, 11), (0, 0, 11), ]
        scapula += [(2, 10, 11), (3, 18, 0), (2, 10, -11), ]
        # Dictionary
        ctrl = {
            "cir": cir, 
            "cub": cub, 
            "sph": sph, 
            "cyl": cyl, 
            "pip": pip, 
            "con1": con1, 
            "con2": con2, 
            "car": car, 
            "car2": car2, 
            "car3": car3, 
            "ar1": ar1, 
            "ar2": ar2, 
            "ar3": ar3, 
            "ar4": ar4, 
            "ar5": ar5, 
            "ar6": ar6, 
            "pointer": pointer, 
            "foot": foot, 
            "foot2": foot2, 
            "hoof": hoof, 
            "hoof2": hoof2, 
            "sqr": sqr, 
            "cross": cross, 
            "hat": hat, 
            "head": head, 
            "scapula": scapula, 
        }
        coordinate = [ctrl[i] for i in kwargs if kwargs[i]]
        for i in coordinate:
            pm.curve(d=1, p=i)


# 79 char line ================================================================
# 72 docstring or comments line ========================================


# cmb = CreateMixamoBones()
# cmb.main()


# sbs = SymmetryBothSide("L")
# sbs.main()


# ac = AlignBonesCenter()
# ac.main()


a = CreateControllers()
a.ctrl(scapula=True, cub=True, foot=True, sph=True, cir=True)


