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
# mirrorCopy("cc_LeftEar2")
# groupOwnPivot(null=True)


# createRigGroups("tigerA")
# reName("cc_Tail1_sub_IK")

# a = ['char_tigerA_mdl_v9999:vertebra_23_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_01_bone', 'char_tigerA_mdl_v9999:muscle_R_supraspinatus_tissue', 'char_tigerA_mdl_v9999:vertebra_11_bone', 'char_tigerA_mdl_v9999:scapula_R_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumProfundusBack2_tissue', 'char_tigerA_mdl_v9999:muscle_R_tricepsBrachiiLa_tissue', 'char_tigerA_mdl_v9999:muscle_R_extensorDigitorumLateralisBck_tissue', 'char_tigerA_mdl_v9999:phalange_L_Ft_06_bone', 'char_tigerA_mdl_v9999:sternum_04_bone', 'char_tigerA_mdl_v9999:muscle_L_sternohyoid2_tissue', 'char_tigerA_mdl_v9999:metacarpals_L_Ft_03_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_02_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_03_bone', 'char_tigerA_mdl_v9999:muscle_L_gluteusSuperficialis_tissue', 'char_tigerA_mdl_v9999:muscle_R_sartorius_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_04_bone', 'char_tigerA_mdl_v9999:muscle_L_extensorCarpiRadualisLongus_tissue', 'char_tigerA_mdl_v9999:muscle_L_pectoralisProfundus_tissue', 'char_tigerA_mdl_v9999:ribs_L_012_bone', 'char_tigerA_mdl_v9999:metatarsal_R_Bk_02_bone', 'char_tigerA_mdl_v9999:vertebra_24_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_02_bone', 'char_tigerA_mdl_v9999:vertebra_12_bone', 'char_tigerA_mdl_v9999:tarsal_R_03_bone', 'char_tigerA_mdl_v9999:muscle_R_mylohyoid_tissue', 'char_tigerA_mdl_v9999:muscle_R_rhomboid_tissue', 'char_tigerA_mdl_v9999:cervical_06_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumProfundus2_tissue', 'char_tigerA_mdl_v9999:muscle_R_tricepsBrachiiLo_tissue', 'char_tigerA_mdl_v9999:ribs_R_04_bone', 'char_tigerA_mdl_v9999:tail_caudal_01_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_01_bone', 'char_tigerA_mdl_v9999:sternum_03_bone', 'char_tigerA_mdl_v9999:muscle_L_pronatorTeres_tissue', 'char_tigerA_mdl_v9999:metatarsal_L_Bk_04_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_06_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumProfundus5_tissue', 'char_tigerA_mdl_v9999:muscle_R_rectusFemoris_tissue', 'char_tigerA_mdl_v9999:femur_R_Bk_bone', 'char_tigerA_mdl_v9999:muscle_L_bicepsBrachii_tissue', 'char_tigerA_mdl_v9999:muscle_L_sternohyoid_tissue', 'char_tigerA_mdl_v9999:ribs_L_011_bone', 'char_tigerA_mdl_v9999:tail_caudal_12_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_04_bone', 'char_tigerA_mdl_v9999:muscle_R_latissimusDorsi_tissue', 'char_tigerA_mdl_v9999:vertebra_14_bone', 'char_tigerA_mdl_v9999:ribs_R_011_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumProfundus4_tissue', 'char_tigerA_mdl_v9999:muscle_R_brachioradialis_tissue', 'char_tigerA_mdl_v9999:cervical_01_bone', 'char_tigerA_mdl_v9999:muscle_R_extensordigitorumcommunis_tissue', 'char_tigerA_mdl_v9999:phalange_L_Ft_08_bone', 'char_tigerA_mdl_v9999:sternum_05_bone', 'char_tigerA_mdl_v9999:muscle_L_teresMajor_tissue', 'char_tigerA_mdl_v9999:phalange_L_Ft_01_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_01_bone', 'char_tigerA_mdl_v9999:muscle_L_hyoid_tissue', 'char_tigerA_mdl_v9999:muscle_R_tensorFasciaeLatae_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_05_bone', 'char_tigerA_mdl_v9999:metacarpals_R_Ft_01_bone', 'char_tigerA_mdl_v9999:muscle_L_extensorCarpiUlnaris_tissue', 'char_tigerA_mdl_v9999:muscle_L_sternoOccipitalis_tissue', 'char_tigerA_mdl_v9999:fibula_R_Bk_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_03_bone', 'char_tigerA_mdl_v9999:tarsal_R_01_bone', 'char_tigerA_mdl_v9999:muscle_R_infraspinatus_tissue', 'char_tigerA_mdl_v9999:muscle_R_trapezius_tissue', 'char_tigerA_mdl_v9999:vertebra_02_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorCarpiRadialis_tissue', 'char_tigerA_mdl_v9999:muscle_R_serratusVentralisCervicis_tissue', 'char_tigerA_mdl_v9999:ribs_R_03_bone', 'char_tigerA_mdl_v9999:tail_caudal_03_bone', 'char_tigerA_mdl_v9999:sternum_06_bone', 'char_tigerA_mdl_v9999:muscle_L_tibialisCranialis_tissue', 'char_tigerA_mdl_v9999:metatarsal_L_Bk_02_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_03_bone', 'char_tigerA_mdl_v9999:muscle_L_extensordigitorumcommunis_tissue', 'char_tigerA_mdl_v9999:muscle_R_vastusMedialis_tissue', 'char_tigerA_mdl_v9999:tarsal_L_01_bone', 'char_tigerA_mdl_v9999:muscle_L_extensorDigitorumLateralisBck_tissue', 'char_tigerA_mdl_v9999:muscle_L_tricepsBrachiiLo_tissue', 'char_tigerA_mdl_v9999:humerus_L_bone', 'char_tigerA_mdl_v9999:tail_caudal_13_bone', 'char_tigerA_mdl_v9999:ribs_L_01_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_05_bone', 'char_tigerA_mdl_v9999:vertebra_07_bone', 'char_tigerA_mdl_v9999:ribs_R_09_bone', 'char_tigerA_mdl_v9999:muscle_R_palmarisLongus_tissue', 'char_tigerA_mdl_v9999:muscle_R_vastusLateralis_tissue', 'char_tigerA_mdl_v9999:muscle_R_extensorDigitorumLongus_tissue', 'char_tigerA_mdl_v9999:phalange_L_Ft_07_bone', 'char_tigerA_mdl_v9999:sternum_07_bone', 'char_tigerA_mdl_v9999:muscle_L_tricepsBrachiiLa_tissue', 'char_tigerA_mdl_v9999:metacarpals_L_Ft_05_bone', 'char_tigerA_mdl_v9999:tibia_L_Bk_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_05_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumSuperficialis_tissue', 'char_tigerA_mdl_v9999:muscle_R_semimembranosus_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_07_bone', 'char_tigerA_mdl_v9999:metacarpals_R_Ft_03_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumProfundus4_tissue', 'char_tigerA_mdl_v9999:muscle_L_rectusAbdominis_tissue', 'char_tigerA_mdl_v9999:radius_L_bone', 'char_tigerA_mdl_v9999:tibia_R_Bk_bone', 'char_tigerA_mdl_v9999:muscle_L_rectusFemoris_tissue', 'char_tigerA_mdl_v9999:ribs_L_02_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_06_bone', 'char_tigerA_mdl_v9999:ulna_R_bone', 'char_tigerA_mdl_v9999:muscle_R_peroneusLongus_tissue', 'char_tigerA_mdl_v9999:muscle_R_deltoidAc_tissue', 'char_tigerA_mdl_v9999:vertebra_04_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorCarpiUlnaris_tissue', 'char_tigerA_mdl_v9999:muscle_R_serratus_tissue', 'char_tigerA_mdl_v9999:skull_01_bone', 'char_tigerA_mdl_v9999:ribs_R_01_bone', 'char_tigerA_mdl_v9999:sternum_08_bone', 'char_tigerA_mdl_v9999:muscle_L_palmarisLongus_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_08_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_05_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumProfundusBack2_tissue', 'char_tigerA_mdl_v9999:muscle_R_caudofemoralis_tissue', 'char_tigerA_mdl_v9999:tarsal_L_03_bone', 'char_tigerA_mdl_v9999:metacarpals_R_Ft_04_bone', 'char_tigerA_mdl_v9999:muscle_L_tensorFasciaeLatae_tissue', 'char_tigerA_mdl_v9999:muscle_L_vastusLateralis_tissue', 'char_tigerA_mdl_v9999:scapula_L_bone', 'char_tigerA_mdl_v9999:tail_caudal_14_bone', 'char_tigerA_mdl_v9999:vertebra_22_bone', 'char_tigerA_mdl_v9999:muscle_R_gluteusMedius_tissue', 'char_tigerA_mdl_v9999:muscle_R_extensorDigitorumLateralis_tissue', 'char_tigerA_mdl_v9999:vertebra_08_bone', 'char_tigerA_mdl_v9999:ribs_R_010_bone', 'char_tigerA_mdl_v9999:cervical_02_bone', 'char_tigerA_mdl_v9999:muscle_R_bicepsBrachii_tissue', 'char_tigerA_mdl_v9999:ribs_R_05_bone', 'char_tigerA_mdl_v9999:metacarpals_L_Ft_02_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_07_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_06_bone', 'char_tigerA_mdl_v9999:muscle_L_iliocostalisLong_tissue', 'char_tigerA_mdl_v9999:muscle_R_bicepsFemoris_tissue', 'char_tigerA_mdl_v9999:metatarsal_L_Bk_01_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_08_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumProfundusBack_tissue', 'char_tigerA_mdl_v9999:muscle_L_pectoralisDescendes', 'char_tigerA_mdl_v9999:ulna_L_bone', 'char_tigerA_mdl_v9999:metatarsal_R_Bk_03_bone', 'char_tigerA_mdl_v9999:muscle_L_semimembranosus_tissue', 'char_tigerA_mdl_v9999:ribs_L_03_bone', 'char_tigerA_mdl_v9999:tail_caudal_15_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_07_bone', 'char_tigerA_mdl_v9999:muscle_C_ribCage_tissue', 'char_tigerA_mdl_v9999:tarsal_R_06_bone', 'char_tigerA_mdl_v9999:muscle_R_pronatorTeres_tissue', 'char_tigerA_mdl_v9999:vertebra_01_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumProfundusBack_tissue', 'char_tigerA_mdl_v9999:muscle_R_splenius_tissue', 'char_tigerA_mdl_v9999:ribs_R_06_bone', 'char_tigerA_mdl_v9999:tail_caudal_04_bone', 'char_tigerA_mdl_v9999:phalange_L_Ft_04_bone', 'char_tigerA_mdl_v9999:pelvis_bone', 'char_tigerA_mdl_v9999:muscle_L_mylohyoid_tissue', 'char_tigerA_mdl_v9999:metatarsal_L_Bk_03_bone', 'char_tigerA_mdl_v9999:muscle_L_infraspinatus_tissue', 'char_tigerA_mdl_v9999:muscle_R_semitendinosus_tissue', 'char_tigerA_mdl_v9999:tarsal_L_06_bone', 'char_tigerA_mdl_v9999:muscle_L_gracilis_tissue', 'char_tigerA_mdl_v9999:muscle_L_brachioradialis_tissue', 'char_tigerA_mdl_v9999:ribs_L_08_bone', 'char_tigerA_mdl_v9999:muscle_L_vastusMedialis_tissue', 'char_tigerA_mdl_v9999:vertebra_21_bone', 'char_tigerA_mdl_v9999:phalange_R_Bk_08_bone', 'char_tigerA_mdl_v9999:muscle_C_throat__tissue', 'char_tigerA_mdl_v9999:muscle_R_pectoralisDescendes', 'char_tigerA_mdl_v9999:vertebra_15_bone', 'char_tigerA_mdl_v9999:ribs_R_012_bone', 'char_tigerA_mdl_v9999:muscle_R_gluteusSuperficialis_tissue', 'char_tigerA_mdl_v9999:cervical_04_bone', 'char_tigerA_mdl_v9999:ribs_R_07_bone', 'char_tigerA_mdl_v9999:tail_caudal_05_bone', 'char_tigerA_mdl_v9999:patela_L_Bk__bone', 'char_tigerA_mdl_v9999:metacarpals_L_Ft_04_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_07_bone', 'char_tigerA_mdl_v9999:muscle_L_pectoralisTransversus_tissue', 'char_tigerA_mdl_v9999:muscle_R_gracilis_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_03_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_07_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorDigitorumProfundus2_tissue', 'char_tigerA_mdl_v9999:muscle_L_deltoidAc_tissue1', 'char_tigerA_mdl_v9999:metatarsal_R_Bk_01_bone', 'char_tigerA_mdl_v9999:muscle_L_bicepsFemoris_tissue', 'char_tigerA_mdl_v9999:ribs_L_07_bone', 'char_tigerA_mdl_v9999:tail_caudal_09_bone', 'char_tigerA_mdl_v9999:muscle_R_pectoralisTransversus_tissue', 'char_tigerA_mdl_v9999:muscle_R_rectusAbdominis_tissue', 'char_tigerA_mdl_v9999:vertebra_03_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumProfundus5_tissue', 'char_tigerA_mdl_v9999:muscle_R_sternohyoid2_tissue', 'char_tigerA_mdl_v9999:cervical_05_bone', 'char_tigerA_mdl_v9999:tail_caudal_06_bone', 'char_tigerA_mdl_v9999:phalange_L_Ft_05_bone', 'char_tigerA_mdl_v9999:sternum_01_bone', 'char_tigerA_mdl_v9999:muscle_L_serratus_tissue', 'char_tigerA_mdl_v9999:fibula_L_Bk__bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_02_bone', 'char_tigerA_mdl_v9999:muscle_L_gastrocnemiusLateralhead_tissue', 'char_tigerA_mdl_v9999:tarsal_L_02_bone', 'char_tigerA_mdl_v9999:muscle_L_sartorius_tissue', 'char_tigerA_mdl_v9999:muscle_L_extensorDigitorumLateralis_tissue', 'char_tigerA_mdl_v9999:tail_caudal_16_bone', 'char_tigerA_mdl_v9999:vertebra_20_bone', 'char_tigerA_mdl_v9999:tigerA_fat_tissue', 'char_tigerA_mdl_v9999:vertebra_13_bone', 'char_tigerA_mdl_v9999:muscle_R_gastrocnemiusMedialhead_tissue', 'char_tigerA_mdl_v9999:muscle_R_sternohyoid_tissue', 'char_tigerA_mdl_v9999:muscle_R_extensorCarpiRadualisLongus_tissue', 'char_tigerA_mdl_v9999:tail_caudal_02_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_08_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_02_bone', 'char_tigerA_mdl_v9999:muscle_L_peroneusLongus_tissue', 'char_tigerA_mdl_v9999:muscle_R_Soleus_tissue', 'char_tigerA_mdl_v9999:carpaR_Ft_L_01_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorCarpiRadialis_tissue', 'char_tigerA_mdl_v9999:muscle_L_brachiocephalicus_tissue', 'char_tigerA_mdl_v9999:tarsal_L_05_bone', 'char_tigerA_mdl_v9999:metatarsal_R_Bk_04_bone', 'char_tigerA_mdl_v9999:muscle_L_Soleus_tissue', 'char_tigerA_mdl_v9999:ribs_L_05_bone', 'char_tigerA_mdl_v9999:tail_caudal_08_bone', 'char_tigerA_mdl_v9999:vertebra_16_bone', 'char_tigerA_mdl_v9999:muscle_R_peroneusBrevis_tissue', 'char_tigerA_mdl_v9999:muscle_R_omotranversarius_tissue', 'char_tigerA_mdl_v9999:vertebra_05_bone', 'char_tigerA_mdl_v9999:ribs_R_08_bone', 'char_tigerA_mdl_v9999:muscle_R_flexorDigitorumSuperficialis_tissue', 'char_tigerA_mdl_v9999:muscle_R_tibialisCranialis_tissue', 'char_tigerA_mdl_v9999:tail_caudal_07_bone', 'char_tigerA_mdl_v9999:phalange_L_Ft_02_bone', 'char_tigerA_mdl_v9999:sternum_02_bone', 'char_tigerA_mdl_v9999:muscle_L_serratusVentralisCervicis_tissue', 'char_tigerA_mdl_v9999:femur_L_Bk__bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_06_bone', 'char_tigerA_mdl_v9999:muscle_L_gastrocnemiusMedialhead_tissue', 'char_tigerA_mdl_v9999:muscle_R_abductorDigiLongus_tissue', 'char_tigerA_mdl_v9999:tarsal_L_04_bone', 'char_tigerA_mdl_v9999:metacarpals_R_Ft_02_bone', 'char_tigerA_mdl_v9999:muscle_L_abductorDigiLongus_tissue', 'char_tigerA_mdl_v9999:muscle_L_rhomboid_tissue', 'char_tigerA_mdl_v9999:ribs_L_010_bone', 'char_tigerA_mdl_v9999:tail_caudal_17_bone', 'char_tigerA_mdl_v9999:vertebra_17_bone', 'char_tigerA_mdl_v9999:vertebra_09_bone', 'char_tigerA_mdl_v9999:humerus_R_bone', 'char_tigerA_mdl_v9999:muscle_R_gastrocnemiusLateralhead_tissue', 'char_tigerA_mdl_v9999:muscle_R_sternoOccipitalis_tissue', 'char_tigerA_mdl_v9999:muscle_R_extensorCarpiUlnaris_tissue', 'char_tigerA_mdl_v9999:ribs_R_02_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_05_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_04_bone', 'char_tigerA_mdl_v9999:muscle_L_splenius_tissue', 'char_tigerA_mdl_v9999:muscle_R_anconeus_tissue', 'char_tigerA_mdl_v9999:calcaneum_L_Bk_bone', 'char_tigerA_mdl_v9999:muscle_L_flexorCarpiUlnaris_tissue', 'char_tigerA_mdl_v9999:muscle_L_omotranversarius_tissue', 'char_tigerA_mdl_v9999:calcaneum_R_Bk_bone', 'char_tigerA_mdl_v9999:muscle_L_caudofemoralis_tissue', 'char_tigerA_mdl_v9999:ribs_L_04_bone', 'char_tigerA_mdl_v9999:tail_caudal_10_bone', 'char_tigerA_mdl_v9999:vertebra_18_bone', 'char_tigerA_mdl_v9999:tarsal_R_02_bone', 'char_tigerA_mdl_v9999:muscle_R_pectoralisProfundus_tissue', 'char_tigerA_mdl_v9999:muscle_R_teresMajor_tissue', 'char_tigerA_mdl_v9999:vertebra_06_bone', 'char_tigerA_mdl_v9999:radius_R_bone', 'char_tigerA_mdl_v9999:muscle_R_hyoid_tissue', 'char_tigerA_mdl_v9999:cervical_03_bone', 'char_tigerA_mdl_v9999:phalange_L_Ft_03_bone', 'char_tigerA_mdl_v9999:muscle_L_subscapularis_tissue', 'char_tigerA_mdl_v9999:metacarpals_L_Ft_01_bone', 'char_tigerA_mdl_v9999:carpaL_Ft_L_04_bone', 'char_tigerA_mdl_v9999:phalange_R_Ft_08_bone', 'char_tigerA_mdl_v9999:muscle_L_gluteusMedius_tissue', 'char_tigerA_mdl_v9999:muscle_L_latissimusDorsi_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_01_bone', 'char_tigerA_mdl_v9999:metacarpals_R_Ft_05_bone', 'char_tigerA_mdl_v9999:muscle_L_anconeus_tissue', 'char_tigerA_mdl_v9999:muscle_L_supraspinatus_tissue', 'char_tigerA_mdl_v9999:ribs_L_09_bone', 'char_tigerA_mdl_v9999:muscle_L_semitendinosus_tissue', 'char_tigerA_mdl_v9999:vertebra_19_bone', 'char_tigerA_mdl_v9999:tarsal_R_04_bone', 'char_tigerA_mdl_v9999:vertebra_10_bone', 'char_tigerA_mdl_v9999:tarsal_R_05_bone', 'char_tigerA_mdl_v9999:muscle_R_iliocostalisLong_tissue', 'char_tigerA_mdl_v9999:muscle_R_brachiocephalicus_tissue', 'char_tigerA_mdl_v9999:muscle_R_deltoidSp_tissue', 'char_tigerA_mdl_v9999:muscle_R_subscapularis_tissue', 'char_tigerA_mdl_v9999:carpaL_Ft_L_03_bone', 'char_tigerA_mdl_v9999:muscle_L_peroneusBrevis_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_06_bone', 'char_tigerA_mdl_v9999:carpaR_Ft_L_04_bone', 'char_tigerA_mdl_v9999:muscle_L_extensorDigitorumLongus_tissue', 'char_tigerA_mdl_v9999:muscle_L_trapezius_tissue', 'char_tigerA_mdl_v9999:phalange_L_Bk_02_bone', 'char_tigerA_mdl_v9999:patela_R_Bk_bone', 'char_tigerA_mdl_v9999:muscle_L_deltoidSp_tissue', 'char_tigerA_mdl_v9999:ribs_L_06_bone', 'char_tigerA_mdl_v9999:tail_caudal_11_bone']

# for obj in a:
#     temp = obj.split(":")[-1]
#     objParents = pm.listRelatives(obj, p=True)[0]
#     objParents = objParents.split(":")[-1]
#     try:
#         pm.parent(temp, objParents)
#     except:
#         continue

# selectObjectOnly()

