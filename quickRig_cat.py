from hjk import *
import pymel.core as pm


class Cat:
    def __init__(self):
        self.hips = "Hips"
        self.spine = [f"Spine{i}" for i in range(1, 10)]
        self.neck = [f"Neck{i}" for i in range(1, 4)]
        self.head = ["Head", "HeadTop_End"]
        self.jaw = ["Jaw", "Jaw_End"]
        self.ear_L = [f"LeftEar{i}" for i in range(1, 4)]
        self.ear_R = [f"RightEar{i}" for i in range(1, 4)]
        self.eye_L = ["LeftEye", "LeftEye_End"]
        self.eye_R = ["RightEye", "RightEye_End"]
        self.legs_LF = [
            'LeftFrontShoulder', 
            'LeftFrontLeg', 
            'LeftFrontKnee', 
            'LeftFrontAnkle', 
            'LeftFrontToe', 
            'LeftFrontToe_End', 
            ]
        self.legs_RF = [
            'RightFrontShoulder', 
            'RightFrontLeg', 
            'RightFrontKnee', 
            'RightFrontAnkle', 
            'RightFrontToe', 
            'RightFrontToe_End', 
            ]
        self.legs_LB = [
            'LeftBackShoulder', 
            'LeftBackLeg', 
            'LeftBackKnee', 
            'LeftBackAnkle', 
            'LeftBackToe', 
            'LeftBackToe_End', 
            ]
        self.legs_RB = [
            'RightBackShoulder', 
            'RightBackLeg', 
            'RightBackKnee', 
            'RightBackAnkle', 
            'RightBackToe', 
            'RightBackToe_End', 
            ]
        self.index_LF = [f"LeftFrontIndex{i}" for i in range(1, 5)]
        self.middle_LF = [f"LeftFrontMiddle{i}" for i in range(1, 5)]
        self.ring_LF = [f"LeftFrontRing{i}" for i in range(1, 5)]
        self.pinky_LF = [f"LeftFrontPinky{i}" for i in range(1, 5)]
        self.index_RF = [f"RightFrontIndex{i}" for i in range(1, 5)]
        self.middle_RF = [f"RightFrontMiddle{i}" for i in range(1, 5)]
        self.ring_RF = [f"RightFrontRing{i}" for i in range(1, 5)]
        self.pinky_RF = [f"RightFrontPinky{i}" for i in range(1, 5)]
        self.index_LB = [f"LeftBackIndex{i}" for i in range(1, 5)]
        self.middle_LB = [f"LeftBackMiddle{i}" for i in range(1, 5)]
        self.ring_LB = [f"LeftBackRing{i}" for i in range(1, 5)]
        self.pinky_LB = [f"LeftBackPinky{i}" for i in range(1, 5)]
        self.index_RB = [f"RightBackIndex{i}" for i in range(1, 5)]
        self.middle_RB = [f"RightBackMiddle{i}" for i in range(1, 5)]
        self.ring_RB = [f"RightBackRing{i}" for i in range(1, 5)]
        self.pinky_RB = [f"RightBackPinky{i}" for i in range(1, 5)]
        self.tail = [f"Tail{i}" for i in range(1, 10)]
        self.jntPosition = {
            'Hips': (0.0, 105.5976, -47.80265), 
            'Spine1': (0.0, 105.5976, -47.80265), 
            'Spine2': (0.0, 104.56808, -36.06098), 
            'Spine3': (0.0, 104.29889, -24.30194), 
            'Spine4': (0.0, 105.53652, -12.58076), 
            'Spine5': (0.0, 105.07111, -0.82225), 
            'Spine6': (0.0, 102.91921, 10.76383), 
            'Spine7': (0.0, 100.92647, 22.37477), 
            'Spine8': (0.0, 100.26311, 34.13868), 
            'Spine9': (0.0, 101.12589, 45.88787), 
            'Neck1': (0.0, 102.38305, 56.65433), 
            'Neck2': (0.0, 104.84668, 67.21273), 
            'Neck3': (0.0, 107.67955, 77.68039), 
            'Head': (0.0, 111.09206, 87.97162), 
            'HeadTop_End': (0.0, 117.10147, 101.49742), 
            'Jaw': (0.0, 103.1242, 97.66678), 
            'Jaw_End': (0.0, 80.59933, 115.17514), 
            'LeftEar1': (9.80007, 116.56773, 95.2822), 
            'LeftEar2': (14.86112, 119.76161, 98.98467), 
            'LeftEar3': (18.24246, 121.19656, 102.42661), 
            'RightEar1': (-9.80007, 116.568, 95.2822), 
            'RightEar2': (-14.8611, 119.762, 98.9847), 
            'RightEar3': (-18.2425, 121.197, 102.427), 
            'LeftEye': (7.51407, 104.15134, 112.95457), 
            'LeftEye_End': (7.51407, 104.15134, 115.18304), 
            'RightEye': (-7.51407, 104.151, 112.955), 
            'RightEye_End': (-7.51407, 104.151, 115.183), 
            'LeftFrontShoulder': (6.34422, 107.83035, 47.43926), 
            'LeftFrontLeg': (10.93067, 84.97193, 57.50794), 
            'LeftFrontKnee': (12.65204, 55.24576, 43.64996), 
            'LeftFrontAnkle': (12.65204, 16.06096, 47.16916), 
            'LeftFrontToe': (12.65204, 5.82732, 50.73547), 
            'LeftFrontToe_End': (12.65204, -0.0, 61.0), 
            'LeftFrontIndex1': (8.05349, 4.2806, 51.28584), 
            'LeftFrontIndex2': (6.63646, 3.99462, 55.03125), 
            'LeftFrontIndex3': (4.81825, 2.59692, 59.837), 
            'LeftFrontIndex4': (4.19337, -2e-05, 61.48865), 
            'LeftFrontMiddle1': (10.95358, 4.57888, 51.83132), 
            'LeftFrontMiddle2': (10.56243, 4.36345, 56.54168), 
            'LeftFrontMiddle3': (10.0478, 3.36558, 62.73908), 
            'LeftFrontMiddle4': (9.91442, -2e-05, 64.34537), 
            'LeftFrontRing1': (13.89453, 4.52929, 51.30716), 
            'LeftFrontRing2': (14.99425, 4.43558, 56.32907), 
            'LeftFrontRing3': (16.25926, 3.30058, 62.10575), 
            'LeftFrontRing4': (16.62691, 0.00055, 63.7846), 
            'LeftFrontPinky1': (17.0, 3.88854, 49.67239), 
            'LeftFrontPinky2': (18.65164, 3.58846, 53.73807), 
            'LeftFrontPinky3': (20.82748, 2.5276, 59.09414), 
            'LeftFrontPinky4': (21.43522, -0.00669, 60.59015), 
            'RightFrontShoulder': (-6.34422, 107.83035, 47.43926), 
            'RightFrontLeg': (-10.93067, 84.97193, 57.50794), 
            'RightFrontKnee': (-12.65204, 55.24576, 43.64996), 
            'RightFrontAnkle': (-12.65204, 16.06096, 47.16916), 
            'RightFrontToe': (-12.65204, 5.82732, 50.73547), 
            'RightFrontToe_End': (-12.65204, -0.0, 61.0), 
            'RightFrontIndex1': (-8.05349, 4.2806, 51.28584), 
            'RightFrontIndex2': (-6.63646, 3.99462, 55.03125), 
            'RightFrontIndex3': (-4.81825, 2.59692, 59.837), 
            'RightFrontIndex4': (-4.19337, -2e-05, 61.48865), 
            'RightFrontMiddle1': (-10.95358, 4.57888, 51.83132), 
            'RightFrontMiddle2': (-10.56243, 4.36345, 56.54168), 
            'RightFrontMiddle3': (-10.0478, 3.36558, 62.73908), 
            'RightFrontMiddle4': (-9.91442, -2e-05, 64.34537), 
            'RightFrontRing1': (-13.89453, 4.52929, 51.30716), 
            'RightFrontRing2': (-14.99425, 4.43558, 56.32907), 
            'RightFrontRing3': (-16.25926, 3.30058, 62.10575), 
            'RightFrontRing4': (-16.62691, 0.00055, 63.7846), 
            'RightFrontPinky1': (-17.0, 3.88854, 49.67239), 
            'RightFrontPinky2': (-18.65164, 3.58846, 53.73807), 
            'RightFrontPinky3': (-20.82748, 2.5276, 59.09414), 
            'RightFrontPinky4': (-21.43522, -0.00669, 60.59015), 
            'LeftBackShoulder': (6.05402, 104.45178, -47.98636), 
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
            'RightBackShoulder': (-6.05402, 104.45178, -47.98636), 
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
            'Tail2': (0.0, 97.34935, -88.53353), 
            'Tail3': (0.0, 96.44871, -102.94353), 
            'Tail4': (0.0, 96.40904, -117.39394), 
            'Tail5': (0.0, 96.19063, -131.84264), 
            'Tail6': (0.0, 96.01854, -146.29217), 
            'Tail7': (0.0, 95.95709, -160.74193), 
            'Tail8': (0.0, 95.68791, -175.18998), 
            'Tail9': (0.0, 95.32285, -189.63589), 
            }
        self.jntHierarchy = {
            self.hips: [self.spine, self.legs_LB, self.legs_RB, self.tail, ], 
            self.spine[-1]: [self.neck, self.legs_LF, self.legs_RF, ], 
            self.head[0]: [
                self.jaw, 
                self.ear_L, 
                self.ear_R, 
                self.eye_L, 
                self.eye_R
                ], 
            self.neck[-1]: [self.head, ], 
            self.legs_LF[-2]: [
                self.index_LF, 
                self.middle_LF, 
                self.ring_LF, 
                self.pinky_LF
                ], 
            self.legs_RF[-2]: [
                self.index_RF, 
                self.middle_RF, 
                self.ring_RF, 
                self.pinky_RF
                ], 
            self.legs_LB[-2]: [
                self.index_LB, 
                self.middle_LB, 
                self.ring_LB, 
                self.pinky_LB
                ], 
            self.legs_RB[-2]: [
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


    def createRigJnt(self) -> None:
        """ To create the rig joint by copying the original joint. """
        if not pm.objExists(self.hips):
            return
        rigJoints = duplicateRange(self.hips, "", "rig_", "")
        rgHips = rigJoints[0]
        try:
            pm.parent(rgHips, "rigBones")
        except:
            pass
        startEndJoint = {
            "rig_Spine1": "rig_Spine9", 
            "rig_LeftBackShoulder": "rig_LeftBackToe_End", 
            "rig_RightBackShoulder": "rig_RightBackToe_End", 
            "rig_LeftFrontShoulder": "rig_LeftFrontToe_End", 
            "rig_RightFrontShoulder": "rig_RightFrontToe_End", 
            }
        types = ["_FK", "_IK"]
        for start, end in startEndJoint.items():
            for typ in types:
                duplicateRange(start, end, "", typ)


    def reOrientJnt(self):
        sel = [self.hips] + self.spine + self.neck + self.head
        for i in sel:
            try:
                obj = pm.PyNode(i)
            except:
                continue
            worldMatrix = obj.getMatrix(worldSpace=True)
            x = worldMatrix[0][:3]
            y = worldMatrix[1][:3]
            z = worldMatrix[2][:3]
            x = round(x, 5)
            y = round(y, 5)
            z = round(z, 5)
            if x[0] >= 0:
                pm.joint(i, e=True, oj="yzx", sao="zdown", zso=True)
            else:
                pm.joint(i, e=True, oj="yzx", sao="zup", zso=True)




# cat = Cat()
# cat.createTempJoints()
# cat.reOrientJnt()
# cat.createRigJnt()

# print({i.name(): getPosition(i) for i in pm.selected()})


# createJointOnCurveSameSpacing(num=9, cuv="curve16")


# for i in pm.selected():
#     try:
#         obj = pm.PyNode(i)
#     except:
#         continue
#     worldMatrix = obj.getMatrix(worldSpace=True)
#     x = worldMatrix[0][:3]
#     y = worldMatrix[1][:3]
#     z = worldMatrix[2][:3]
#     x = round(x, 5)
#     y = round(y, 5)
#     z = round(z, 5)
#     if x[0] >= 0:
#         pm.joint(i, e=True, oj="yzx", sao="zdown", zso=True)
#     else:
#         pm.joint(i, e=True, oj="yzx", sao="zup", zso=True)


# for i in selectJointOnly():
#     setJointsStyle(i, b=True)


# createPolevectorJoint()
# lineUpObjectsOnOnePlane("LeftBackPinky11", "LeftBackPinky12", "LeftBackPinky13", "LeftBackPinky14")
# reName("Back", "Front")
# groupOwnPivot()


# ctrl = Controllers()
# ctrl.createControllers(square="")
# mirrorCopy("cc_LeftBackKnee_FK1")
# groupOwnPivot(null=True)


# createRigGroups("tigerA")
# reName("cc_Tail1_sub_IK")


# selectObjectOnly()


# groupOwnPivot(null=True)
