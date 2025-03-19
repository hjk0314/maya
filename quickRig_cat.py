from hjk import *
import pymel.core as pm


class Cat:
    def __init__(self):
        self.spine = [f"Spine{i}" for i in range(1, 11)]
        self.legs_LB = [
            'LeftBackLeg', 
            'LeftBackKnee', 
            'LeftBackAnkle', 
            'LeftBackToe', 
            'LeftBackToe_End', 
            ]
        self.legs_RB = [
            'RightBackLeg', 
            'RightBackKnee', 
            'RightBackAnkle', 
            'RightBackToe', 
            'RightBackToe_End', 
            ]
        self.index_LB = [f"LeftBackIndex{i}" for i in range(1, 5)]
        self.middle_LB = [f"LeftBackMiddle{i}" for i in range(1, 5)]
        self.ring_LB = [f"LeftBackRing{i}" for i in range(1, 5)]
        self.pinky_LB = [f"LeftBackPinky{i}" for i in range(1, 5)]
        self.index_RB = [f"RightBackIndex{i}" for i in range(1, 5)]
        self.middle_RB = [f"RightBackMiddle{i}" for i in range(1, 5)]
        self.ring_RB = [f"RightBackRing{i}" for i in range(1, 5)]
        self.pinky_RB = [f"RightBackPinky{i}" for i in range(1, 5)]
        self.tail = [f"Tail{i}" for i in range(1, 9)]
        self.jntPosition = {
            'Hips': (0.0, 105.5976, -47.80265), 
            'Spine1': (0.0, 104.81905, -38.40455), 
            'Spine2': (0.0, 104.06719, -29.00845), 
            'Spine3': (0.0, 104.8232, -19.6161), 
            'Spine4': (0.0, 105.64084, -10.22491), 
            'Spine5': (0.0, 105.07111, -0.82225), 
            'Spine6': (0.0, 103.4137, 8.45871), 
            'Spine7': (0.0, 101.54916, 17.70189), 
            'Spine8': (0.0, 100.52465, 27.07221), 
            'Spine9': (0.0, 100.30797, 36.49581), 
            'Spine10': (0.0, 101.12589, 45.88787), 
            'LeftBackLeg': (8.60929, 94.73428, -61.52581), 
            'LeftBackKnee': (12.0, 56.96354, -50.1429), 
            'LeftBackAnkle': (12.0, 25.43732, -80.42925), 
            'LeftBackToe': (12.0, 5.28491, -74.07647), 
            'LeftBackToe_End': (12.0, 0.0, -62.54657), 
            'LeftBackIndex1': (7.52184, 4.14442, -72.46626), 
            'LeftBackIndex2': (6.63325, 4.03951, -68.07547), 
            'LeftBackIndex3': (5.68968, 3.08872, -63.41307), 
            'LeftBackIndex4': (5.29779, 0.07662, -61.47664), 
            'LeftBackMiddle1': (10.19021, 4.55537, -71.47229), 
            'LeftBackMiddle2': (9.94945, 4.33986, -65.65421), 
            'LeftBackMiddle3': (9.74971, 3.73666, -60.8275), 
            'LeftBackMiddle4': (9.69416, 0.07204, -59.48496), 
            'LeftBackRing1': (13.54015, 4.69679, -71.9467), 
            'LeftBackRing2': (14.12033, 4.46423, -65.63917), 
            'LeftBackRing3': (14.58682, 3.72222, -60.56762), 
            'LeftBackRing4': (14.75808, 0.10004, -58.70574), 
            'LeftBackPinky1': (16.14631, 4.12414, -73.42003), 
            'LeftBackPinky2': (17.87145, 3.62354, -67.92649), 
            'LeftBackPinky3': (19.40107, 2.99099, -63.05557), 
            'LeftBackPinky4': (20.03285, 0.04649, -61.04372), 
            'RightBackLeg': (-8.60929, 94.7343, -61.5258), 
            'RightBackKnee': (-12.0, 56.9635, -50.1429), 
            'RightBackAnkle': (-12.0, 25.4373, -80.4292), 
            'RightBackToe': (-12.0, 5.28491, -74.0765), 
            'RightBackToe_End': (-12.0, -0.0, -62.5466), 
            'RightBackIndex1': (-7.52184, 4.14442, -72.4663), 
            'RightBackIndex2': (-6.63325, 4.03951, -68.0755), 
            'RightBackIndex3': (-5.68968, 3.08872, -63.4131), 
            'RightBackIndex4': (-5.29779, 0.07662, -61.4766), 
            'RightBackMiddle1': (-10.1902, 4.55537, -71.4723), 
            'RightBackMiddle2': (-9.94945, 4.33986, -65.6542), 
            'RightBackMiddle3': (-9.74971, 3.73666, -60.8275), 
            'RightBackMiddle4': (-9.69416, 0.07204, -59.485), 
            'RightBackRing1': (-13.5402, 4.69679, -71.9467), 
            'RightBackRing2': (-14.1203, 4.46423, -65.6392), 
            'RightBackRing3': (-14.5868, 3.72222, -60.5676), 
            'RightBackRing4': (-14.7581, 0.10004, -58.7057), 
            'RightBackPinky1': (-16.1463, 4.12414, -73.42), 
            'RightBackPinky2': (-17.8715, 3.62354, -67.9265), 
            'RightBackPinky3': (-19.4011, 2.99099, -63.0556), 
            'RightBackPinky4': (-20.0329, 0.04649, -61.0437), 
            'Tail1': (0.0, 100.30746, -74.3944), 
            'Tail2': (0.0, 97.07727, -90.58436), 
            'Tail3': (0.0, 96.4385, -107.07161), 
            'Tail4': (0.0, 96.3442, -123.58429), 
            'Tail5': (0.0, 96.05397, -140.0973), 
            'Tail6': (0.0, 95.99479, -156.61215), 
            'Tail7': (0.0, 95.73513, -173.12481), 
            'Tail8': (0.0, 95.32285, -189.6359), 
            }
        self.jntHierarchy = {
            'Hips': [self.spine, self.legs_LB, self.legs_RB, self.tail, ], 
            'LeftBackToe': [
                self.index_LB, 
                self.middle_LB, 
                self.ring_LB, 
                self.pinky_LB
                ], 
            'RightBackToe': [
                self.index_RB, 
                self.middle_RB, 
                self.ring_RB, 
                self.pinky_RB
                ]
            }


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
                isLeftArms = any("Left" in i for i in joints)
                isRightArms = any("Right" in i for i in joints)
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


    def createTempJoints(self):
        for jnt, pos in self.jntPosition.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        self.setHierarchy(self.jntHierarchy)


