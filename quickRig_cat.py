from hjk import *
import pymel.core as pm


class Cat:
    def __init__(self):
        self.hips = "Hips"
        self.spine = ["Spine%s" % (i if i else "") for i in range(9)]
        self.neck = ["Neck%s" % (i if i else "") for i in range(3)]
        self.tail = ["Tail%s" % (i if i else "") for i in range(9)]
        self.head = ["Head", "HeadTop_End"]
        self.jaw = ["Jaw", "Jaw_End"]
        self.ear_L = ["LeftEar%s" % (i if i else "") for i in range(3)]
        self.ear_R = ["RightEar%s"% (i if i else "") for i in range(3)]
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
        self.index_LF += ["LeftFrontIndexClaw", "LeftFrontIndexClawEnd"]
        self.middle_LF = [f"LeftFrontMiddle{i}" for i in range(1, 5)]
        self.middle_LF += ["LeftFrontMiddleClaw", "LeftFrontMiddleClawEnd"]
        self.ring_LF = [f"LeftFrontRing{i}" for i in range(1, 5)]
        self.ring_LF += ["LeftFrontRingClaw", "LeftFrontRingClawEnd"]
        self.pinky_LF = [f"LeftFrontPinky{i}" for i in range(1, 5)]
        self.pinky_LF += ["LeftFrontPinkyClaw", "LeftFrontPinkyClawEnd"]
        self.index_RF = [f"RightFrontIndex{i}" for i in range(1, 5)]
        self.index_RF += ["RightFrontIndexClaw", "RightFrontIndexClawEnd"]
        self.middle_RF = [f"RightFrontMiddle{i}" for i in range(1, 5)]
        self.middle_RF += ["RightFrontMiddleClaw", "RightFrontMiddleClawEnd"]
        self.ring_RF = [f"RightFrontRing{i}" for i in range(1, 5)]
        self.ring_RF += ["RightFrontRingClaw", "RightFrontRingClawEnd"]
        self.pinky_RF = [f"RightFrontPinky{i}" for i in range(1, 5)]
        self.pinky_RF += ["RightFrontPinkyClaw", "RightFrontPinkyClawEnd"]
        self.index_LB = [f"LeftBackIndex{i}" for i in range(1, 5)]
        self.index_LB += ["LeftBackIndexClaw", "LeftBackIndexClawEnd"]
        self.middle_LB = [f"LeftBackMiddle{i}" for i in range(1, 5)]
        self.middle_LB += ["LeftBackMiddleClaw", "LeftBackMiddleClawEnd"]
        self.ring_LB = [f"LeftBackRing{i}" for i in range(1, 5)]
        self.ring_LB += ["LeftBackRingClaw", "LeftBackRingClawEnd"]
        self.pinky_LB = [f"LeftBackPinky{i}" for i in range(1, 5)]
        self.pinky_LB += ["LeftBackPinkyClaw", "LeftBackPinkyClawEnd"]
        self.index_RB = [f"RightBackIndex{i}" for i in range(1, 5)]
        self.index_RB += ["RightBackIndexClaw", "RightBackIndexClawEnd"]
        self.middle_RB = [f"RightBackMiddle{i}" for i in range(1, 5)]
        self.middle_RB += ["RightBackMiddleClaw", "RightBackMiddleClawEnd"]
        self.ring_RB = [f"RightBackRing{i}" for i in range(1, 5)]
        self.ring_RB += ["RightBackRingClaw", "RightBackRingClawEnd"]
        self.pinky_RB = [f"RightBackPinky{i}" for i in range(1, 5)]
        self.pinky_RB += ["RightBackPinkyClaw", "RightBackPinkyClawEnd"]
        self.chest_A = ["Spine8_A"]
        self.chest_BC = ["Spine8_BC"]
        self.chest_BL = ["Spine8_BL"]
        self.chest_BR = ["Spine8_BR"]
        self.rear = [f"Spine_C{i}" for i in range(1, 4)]
        self.ribs2_L = [f"Spine2_L{i}" for i in range(1, 4)]
        self.ribs2_R = [f"Spine2_R{i}" for i in range(1, 4)]
        self.ribs4_L = [f"Spine4_L{i}" for i in range(1, 4)]
        self.ribs4_R = [f"Spine4_R{i}" for i in range(1, 4)]
        self.ribs6_L = [f"Spine6_L{i}" for i in range(1, 4)]
        self.ribs6_R = [f"Spine6_R{i}" for i in range(1, 4)]
        self.subLeg1_LFU = [f"LeftFrontLeg_{i}" for i in ["A", "B"]]
        self.subLeg2_LFU = [f"LeftFrontLeg_B{i}" for i in ["C", "L", "R"]]
        self.subLeg1_RFU = [f"RightFrontLeg_{i}" for i in ["A", "B"]]
        self.subLeg2_RFU = [f"RightFrontLeg_B{i}" for i in ["C", "L", "R"]]
        self.subLeg1_LFD = [f"LeftFrontKnee_{i}" for i in ["A", "B"]]
        self.subLeg2_LFD = [f"LeftFrontKnee_B{i}" for i in ["C", "L", "R"]]
        self.subLeg1_RFD = [f"RightFrontKnee_{i}" for i in ["A", "B"]]
        self.subLeg2_RFD = [f"RightFrontKnee_B{i}" for i in ["C", "L", "R"]]
        self.subLeg1_LBU = [f"LeftBackLeg_A{i}" for i in ["", "_End"]]
        self.subLeg2_LBU = [f"LeftBackLeg_{i}" for i in ["B", "C"]]
        self.subLeg3_LBU = [f"LeftBackLeg_C{i}" for i in ["C", "L", "R"]]
        self.subLeg1_LBD = [f"LeftBackKnee_{i}" for i in ["A", "B"]]
        self.subLeg2_LBD = [f"LeftBackKnee_B{i}" for i in ["C", "L", "R"]]
        self.subLeg1_RBU = [f"RightBackLeg_A{i}" for i in ["", "_End"]]
        self.subLeg2_RBU = [f"RightBackLeg_{i}" for i in ["B", "C"]]
        self.subLeg3_RBU = [f"RightBackLeg_C{i}" for i in ["C", "L", "R"]]
        self.subLeg1_RBD = [f"RightBackKnee_{i}" for i in ["A", "B"]]
        self.subLeg2_RBD = [f"RightBackKnee_B{i}" for i in ["C", "L", "R"]]


        self.jntPosition = {
            'Hips': (0.0, 105.5976, -47.80265), 
            'Spine': (0.0, 105.7347, -46.19885), 
            'Spine1': (0.0, 105.81381, -36.03417), 
            'Spine2': (0.0, 105.88847, -24.30194), 
            'Spine3': (0.0, 105.74386, -12.58076), 
            'Spine4': (0.0, 104.80744, -0.82225), 
            'Spine5': (0.0, 102.91921, 10.76383), 
            'Spine6': (0.0, 100.92647, 22.37477), 
            'Spine7': (0.0, 100.26311, 34.13868), 
            'Spine8': (0.0, 101.12589, 45.88787), 
            'Neck': (0.0, 102.38305, 56.65433), 
            'Neck1': (0.0, 104.84668, 67.21273), 
            'Neck2': (0.0, 107.67955, 77.68039), 
            'Head': (0.0, 111.09206, 87.97162), 
            'HeadTop_End': (0.0, 117.10147, 101.49742), 
            'Jaw': (0.0, 103.1242, 97.66678), 
            'Jaw_End': (0.0, 80.59933, 115.17514), 
            "LeftEar": (9.80007, 116.56776, 95.28221), 
            "LeftEar1": (13.00385, 119.239, 99.07684), 
            "LeftEar2": (16.17083, 122.76902, 101.9936), 
            "RightEar": (-9.80007, 116.568, 95.2822), 
            "RightEar1": (-13.0039, 119.239, 99.0768), 
            "RightEar2": (-16.1708, 122.769, 101.994), 
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
            'LeftFrontIndex3': (5.33999, 2.998, 58.45802), 
            "LeftFrontIndex4": (4.96698, 0.51659, 59.44393), 
            "LeftFrontIndexClaw": (4.90726, 2.51888, 59.6018), 
            "LeftFrontIndexClawEnd": (4.34124, 0.35807, 61.09785), 
            'LeftFrontMiddle1': (10.95358, 4.57888, 51.83132), 
            'LeftFrontMiddle2': (10.56243, 4.36345, 56.54168), 
            'LeftFrontMiddle3': (10.22265, 3.70462, 60.63353), 
            "LeftFrontMiddle4": (10.09611, 0.68552, 62.15742), 
            "LeftFrontMiddleClaw": (10.08238, 2.68508, 62.32273), 
            "LeftFrontMiddleClawEnd": (9.93488, 0.27728, 64.09901), 
            'LeftFrontRing1': (13.89453, 4.52929, 51.30716), 
            'LeftFrontRing2': (14.99425, 4.43558, 56.32907), 
            'LeftFrontRing3': (15.81403, 3.70006, 60.07263), 
            "LeftFrontRing4": (16.0479, 0.92329, 61.1406), 
            "LeftFrontRingClaw": (16.08252, 2.86464, 61.29869), 
            "LeftFrontRingClawEnd": (16.45288, 0.52579, 62.98996), 
            'LeftFrontPinky1': (17.0, 3.88854, 49.67239), 
            'LeftFrontPinky2': (18.65164, 3.58846, 53.73807), 
            'LeftFrontPinky3': (20.07594, 2.89403, 57.24418), 
            "LeftFrontPinky4": (20.25231, 0.60535, 57.67835), 
            "LeftFrontPinkyClaw": (20.31314, 2.54671, 57.82808), 
            "LeftFrontPinkyClawEnd": (20.85223, 0.61177, 59.1551), 
            'RightFrontShoulder': (-6.34422, 107.83035, 47.43926), 
            'RightFrontLeg': (-10.93067, 84.97193, 57.50794), 
            'RightFrontKnee': (-12.65204, 55.24576, 43.64996), 
            'RightFrontAnkle': (-12.65204, 16.06096, 47.16916), 
            'RightFrontToe': (-12.65204, 5.82732, 50.73547), 
            'RightFrontToe_End': (-12.65204, -0.0, 61.0), 
            'RightFrontIndex1': (-8.05349, 4.2806, 51.28584), 
            'RightFrontIndex2': (-6.63646, 3.99462, 55.03125), 
            'RightFrontIndex3': (-5.33999, 2.998, 58.45802), 
            "RightFrontIndex4": (-4.96223, 0.5241, 59.45649), 
            "RightFrontIndexClaw": (-4.8359, 2.50153, 59.7904), 
            "RightFrontIndexClawEnd": (-4.34457, 0.1994, 61.08904), 
            'RightFrontMiddle1': (-10.95358, 4.57888, 51.83132), 
            'RightFrontMiddle2': (-10.56243, 4.36345, 56.54168), 
            'RightFrontMiddle3': (-10.22265, 3.70462, 60.63353), 
            "RightFrontMiddle4": (-10.10632, 0.63246, 62.03434), 
            "RightFrontMiddleClaw": (-10.0926, 2.63203, 62.19964), 
            "RightFrontMiddleClawEnd": (-9.9451, 0.22423, 63.97592), 
            'RightFrontRing1': (-13.89453, 4.52929, 51.30716), 
            'RightFrontRing2': (-14.99425, 4.43558, 56.32907), 
            'RightFrontRing3': (-15.81403, 3.70006, 60.07263), 
            "RightFrontRing4": (-16.03228, 0.77917, 61.06931), 
            "RightFrontRingClaw": (-16.0669, 2.72052, 61.2274), 
            "RightFrontRingClawEnd": (-16.43727, 0.38168, 62.91867), 
            'RightFrontPinky1': (-17.0, 3.88854, 49.67239), 
            'RightFrontPinky2': (-18.65164, 3.58846, 53.73807), 
            'RightFrontPinky3': (-20.07594, 2.89403, 57.24418), 
            "RightFrontPinky4": (-20.23687, 0.58762, 57.64033), 
            "RightFrontPinkyClaw": (-20.29769, 2.52898, 57.79005), 
            "RightFrontPinkyClawEnd": (-20.83678, 0.59404, 59.11708), 
            'LeftBackShoulder': (6.05402, 104.45178, -47.98636), 
            'LeftBackLeg': (8.60929, 94.73428, -61.52581), 
            'LeftBackKnee': (12.0, 56.96354, -50.1429), 
            'LeftBackAnkle': (12.0, 25.43732, -80.42925), 
            'LeftBackToe': (12.0, 5.28491, -74.07647), 
            'LeftBackToe_End': (12.0, 0.0, -62.54657), 
            'LeftBackIndex1': (7.52184, 4.14442, -72.46626), 
            'LeftBackIndex2': (6.63325, 4.03951, -68.07547), 
            'LeftBackIndex3': (6.02132, 3.4229, -65.0518), 
            "LeftBackIndex4": (5.6025, 1.30866, -62.98227), 
            "LeftBackIndexClaw": (5.53682, 3.31922, -62.65774), 
            "LeftBackIndexClawEnd": (5.2617, 1.01619, -61.29834), 
            'LeftBackMiddle1': (10.19021, 4.55537, -71.47229), 
            'LeftBackMiddle2': (9.94945, 4.33986, -65.65421), 
            'LeftBackMiddle3': (9.83661, 3.99909, -62.92745), 
            "LeftBackMiddle4": (9.73306, 1.83989, -60.42521), 
            "LeftBackMiddleClaw": (9.72728, 3.87273, -60.28546), 
            "LeftBackMiddleClawEnd": (9.65365, 1.46376, -58.50617), 
            'LeftBackRing1': (13.54015, 4.69679, -71.9467), 
            'LeftBackRing2': (14.12033, 4.46423, -65.63917), 
            'LeftBackRing3': (14.43758, 3.9596, -62.19006), 
            "LeftBackRing4": (14.51209, 1.59993, -61.38008), 
            "LeftBackRingClaw": (14.52453, 3.57455, -61.24479), 
            "LeftBackRingClawEnd": (14.68297, 1.23457, -59.52225), 
            'LeftBackPinky1': (16.14631, 4.12414, -73.42003), 
            'LeftBackPinky2': (17.87145, 3.62354, -67.92649), 
            'LeftBackPinky3': (18.88605, 3.20397, -64.69559), 
            "LeftBackPinky4": (19.02818, 1.04085, -64.243), 
            "LeftBackPinkyClaw": (19.06889, 3.01547, -64.11338), 
            "LeftBackPinkyClawEnd": (19.49764, 1.07959, -62.74804), 
            'RightBackShoulder': (-6.05402, 104.45178, -47.98636), 
            'RightBackLeg': (-8.60929, 94.7343, -61.5258), 
            'RightBackKnee': (-12.0, 56.9635, -50.1429), 
            'RightBackAnkle': (-12.0, 25.4373, -80.4292), 
            'RightBackToe': (-12.0, 5.28491, -74.0765), 
            'RightBackToe_End': (-12.0, -0.0, -62.5466), 
            'RightBackIndex1': (-7.52184, 4.14442, -72.4663), 
            'RightBackIndex2': (-6.63325, 4.03951, -68.0755), 
            'RightBackIndex3': (-6.02133, 3.4229, -65.0518), 
            "RightBackIndex4": (-5.59209, 1.30999, -62.93084), 
            "RightBackIndexClaw": (-5.52641, 3.32056, -62.60631), 
            "RightBackIndexClawEnd": (-5.2513, 1.01752, -61.24691), 
            'RightBackMiddle1': (-10.1902, 4.55537, -71.4723), 
            'RightBackMiddle2': (-9.94945, 4.33986, -65.6542), 
            'RightBackMiddle3': (-9.83661, 3.99909, -62.92745), 
            "RightBackMiddle4": (-9.73454, 1.78832, -60.46098), 
            "RightBackMiddleClaw": (-9.72876, 3.82116, -60.32122), 
            "RightBackMiddleClawEnd": (-9.65513, 1.41219, -58.54193), 
            'RightBackRing1': (-13.5402, 4.69679, -71.9467), 
            'RightBackRing2': (-14.1203, 4.46423, -65.6392), 
            'RightBackRing3': (-14.43758, 3.9596, -62.19006), 
            "RightBackRing4": (-14.50997, 1.42813, -61.40306), 
            "RightBackRingClaw": (-14.52242, 3.40275, -61.26777), 
            "RightBackRingClawEnd": (-14.68086, 1.06277, -59.54523), 
            'RightBackPinky1': (-16.1463, 4.12414, -73.42), 
            'RightBackPinky2': (-17.8715, 3.62354, -67.9265), 
            'RightBackPinky3': (-18.88605, 3.20397, -64.69559), 
            "RightBackPinky4": (-19.04469, 1.05647, -64.19041), 
            "RightBackPinkyClaw": (-19.0854, 3.03109, -64.06078), 
            "RightBackPinkyClawEnd": (-19.51416, 1.09521, -62.69545), 
            'Tail': (0.0, 100.30746, -74.3944), 
            'Tail1': (0.0, 97.34935, -88.53353), 
            'Tail2': (0.0, 96.44871, -102.94353), 
            'Tail3': (0.0, 96.40904, -117.39394), 
            'Tail4': (0.0, 96.19063, -131.84264), 
            'Tail5': (0.0, 96.01854, -146.29217), 
            'Tail6': (0.0, 95.95709, -160.74193), 
            'Tail7': (0.0, 95.68791, -175.18998), 
            'Tail8': (0.0, 95.32285, -189.63589), 

            "Spine_C1": (-0.0, 72.88544, -39.96708), 
            "Spine_C2": (-0.0, 68.22187, -56.0271), 
            "Spine_C3": (1e-05, 81.01084, -68.12268), 
            "Spine2_L1": (7.52758, 97.25383, -24.30194), 
            "Spine2_L2": (9.18641, 84.61341, -24.30194), 
            "Spine2_L3": (4.83188, 73.38406, -24.30194), 
            "Spine2_R1": (-7.52758, 97.2538, -24.3019), 
            "Spine2_R2": (-9.18641, 84.6134, -24.3019), 
            "Spine2_R3": (-4.83188, 73.3841, -24.3019), 
            "Spine4_L1": (10.52829, 93.97967, -1.93604), 
            "Spine4_L2": (12.9616, 77.73764, -1.93604), 
            "Spine4_L3": (6.51446, 63.81112, -1.93604), 
            "Spine4_R1": (-10.5283, 93.9797, -1.93604), 
            "Spine4_R2": (-12.9616, 77.7376, -1.93604), 
            "Spine4_R3": (-6.51446, 63.8111, -1.93604), 
            "Spine6_L1": (10.87371, 90.89452, 22.37477), 
            "Spine6_L2": (13.46106, 74.84851, 22.37477), 
            "Spine6_L3": (6.59603, 61.39651, 22.37477), 
            "Spine6_R1": (-10.8737, 90.8945, 22.3748), 
            "Spine6_R2": (-13.4611, 74.8485, 22.3748), 
            "Spine6_R3": (-6.59603, 61.3965, 22.3748), 
            "Spine8_A": (-0.0, 71.65236, 63.94878), 
            "Spine8_BC": (0.0, 54.76612, 45.86158), 
            "Spine8_BL": (4.8019, 57.29316, 45.86302), 
            "Spine8_BR": (-4.8019, 57.2932, 45.863), 
            "LeftFrontLeg_A": (12.65204, 77.05088, 60.99702), 
            "LeftFrontLeg_B": (12.65204, 59.7314, 55.7013), 
            "LeftFrontLeg_BC": (12.65204, 57.90855, 57.80343), 
            "LeftFrontLeg_BL": (16.83342, 59.7314, 55.7013), 
            "LeftFrontLeg_BR": (8.24673, 59.7314, 55.7013), 
            "RightFrontLeg_A": (-12.652, 77.0509, 60.997), 
            "RightFrontLeg_B": (-12.652, 59.7314, 55.7013), 
            "RightFrontLeg_BC": (-12.652, 57.9085, 57.8034), 
            "RightFrontLeg_BL": (-16.8334, 59.7314, 55.7013), 
            "RightFrontLeg_BR": (-8.24673, 59.7314, 55.7013), 
            "LeftFrontKnee_A": (12.652, 25.46658, 48.47807), 
            "LeftFrontKnee_B": (12.652, 53.70987, 54.09675), 
            "LeftFrontKnee_BC": (12.65201, 54.09386, 56.86319), 
            "LeftFrontKnee_BL": (16.86978, 53.70987, 54.09674), 
            "LeftFrontKnee_BR": (9.90926, 53.70986, 54.09676), 
            "RightFrontKnee_A": (-12.652, 25.4666, 48.4781), 
            "RightFrontKnee_B": (-12.652, 53.7099, 54.0967), 
            "RightFrontKnee_BC": (-12.652, 54.0939, 56.8632), 
            "RightFrontKnee_BL": (-16.8698, 53.7099, 54.0967), 
            "RightFrontKnee_BR": (-9.90926, 53.7099, 54.0968), 
            "LeftBackLeg_A": (8.61483, 94.74344, -47.35054), 
            "LeftBackLeg_A_End": (12.00254, 59.89025, -47.35066), 
            "RightBackLeg_A": (-8.61483, 94.7434, -47.3505), 
            "RightBackLeg_A_End": (-12.0025, 59.8902, -47.3507), 
            "LeftBackLeg_B": (8.61483, 87.56935, -71.51873), 
            "LeftBackLeg_C": (8.61483, 64.30238, -67.89892), 
            "LeftBackLeg_CC": (8.61483, 61.43716, -71.57153), 
            "LeftBackLeg_CL": (12.94021, 64.30238, -67.89892), 
            "LeftBackLeg_CR": (4.36273, 64.30238, -67.89892), 
            "RightBackLeg_B": (-8.61483, 87.5693, -71.5187), 
            "RightBackLeg_C": (-8.61483, 64.3024, -67.8989), 
            "RightBackLeg_CC": (-8.61483, 61.4372, -71.5715), 
            "RightBackLeg_CL": (-12.9402, 64.3024, -67.8989), 
            "RightBackLeg_CR": (-4.36273, 64.3024, -67.8989), 
            "LeftBackKnee_A": (11.04193, 33.12261, -77.52138), 
            "LeftBackKnee_B": (11.04328, 52.66147, -68.12061), 
            "LeftBackKnee_BC": (11.04344, 56.07758, -71.71784), 
            "LeftBackKnee_BL": (14.13597, 52.66122, -68.12058), 
            "LeftBackKnee_BR": (7.12123, 52.66177, -68.12065), 
            "RightBackKnee_A": (-11.0419, 33.1226, -77.5214), 
            "RightBackKnee_B": (-11.0433, 52.6615, -68.1206), 
            "RightBackKnee_BC": (-11.0434, 56.0776, -71.7178), 
            "RightBackKnee_BL": (-14.136, 52.6612, -68.1206), 
            "RightBackKnee_BR": (-7.12123, 52.6618, -68.1207), 
            }
        self.jntHierarchy = {
            self.hips: [self.spine, self.legs_LB, self.legs_RB, self.tail, ], 
            self.spine[0]: [self.rear, ], 
            self.spine[2]: [self.ribs2_L, self.ribs2_R, ], 
            self.spine[4]: [self.ribs4_L, self.ribs4_R, ], 
            self.spine[6]: [self.ribs6_L, self.ribs6_R, ], 
            self.spine[-1]: [
                self.neck, 
                self.legs_LF, self.legs_RF, 
                self.chest_A, self.chest_BC, self.chest_BL, self.chest_BR
                ], 
            self.neck[-1]: [self.head, ], 
            self.head[0]: [
                self.jaw, 
                self.ear_L, 
                self.ear_R, 
                self.eye_L, 
                self.eye_R
                ], 
            self.legs_LF[1]: [self.subLeg1_LFU, ], 
            self.subLeg1_LFU[-1]: [[i] for i in self.subLeg2_LFU], 
            self.legs_LF[2]: [self.subLeg1_LFD, ], 
            self.subLeg1_LFD[-1]: [[i] for i in self.subLeg2_LFD], 
            self.legs_LF[-2]: [
                self.index_LF, 
                self.middle_LF, 
                self.ring_LF, 
                self.pinky_LF
                ], 
            self.legs_RF[1]: [self.subLeg1_RFU, ], 
            self.subLeg1_RFU[-1]: [[i] for i in self.subLeg2_RFU], 
            self.legs_RF[2]: [self.subLeg1_RFD, ], 
            self.subLeg1_RFD[-1]: [[i] for i in self.subLeg2_RFD], 
            self.legs_RF[-2]: [
                self.index_RF, 
                self.middle_RF, 
                self.ring_RF, 
                self.pinky_RF
                ], 
            self.legs_LB[1]: [self.subLeg1_LBU, self.subLeg2_LBU, ], 
            self.subLeg2_LBU[-1]: [[i] for i in self.subLeg3_LBU], 
            self.legs_LB[2]: [self.subLeg1_LBD, ], 
            self.subLeg1_LBD[-1]: [[i] for i in self.subLeg2_LBD], 
            self.legs_LB[-2]: [
                self.index_LB, 
                self.middle_LB, 
                self.ring_LB, 
                self.pinky_LB
                ], 
            self.legs_RB[1]: [self.subLeg1_RBU, self.subLeg2_RBU, ], 
            self.subLeg2_RBU[-1]: [[i] for i in self.subLeg3_RBU], 
            self.legs_RB[2]: [self.subLeg1_RBD, ], 
            self.subLeg1_RBD[-1]: [[i] for i in self.subLeg2_RBD], 
            self.legs_RB[-2]: [
                self.index_RB, 
                self.middle_RB, 
                self.ring_RB, 
                self.pinky_RB
                ]
            }


    def createTempJoints(self):
        for jnt, pos in self.jntPosition.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        self.setHierarchy(self.jntHierarchy)
        try:
            pm.parent(self.hips, "bindBones")
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
                pm.joint(obj, e=True, oj="yzx", sao="zdown", zso=True)
            else:
                pm.joint(obj, e=True, oj="yzx", sao="zup", zso=True)
            if not obj.getChildren():
                pm.joint(obj, e=True, oj='none', ch=True, zso=True)


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
            self.spine[0]: self.spine[-1], 
            self.neck[0]: self.head[0], 
            self.tail[0]: self.tail[-1], 
            self.legs_LF[0]: self.legs_LF[-1], 
            self.legs_RF[0]: self.legs_RF[-1], 
            self.legs_LB[0]: self.legs_LB[-1], 
            self.legs_RB[0]: self.legs_RB[-1], 
            }
        types = ["_FK", "_IK"]
        for start, end in startEndJoint.items():
            for typ in types:
                duplicateRange(f"rig_{start}", f"rig_{end}", "", typ)


cat = Cat()
# createRigGroups("tigerA")
# cat.createTempJoints()
# cat.reOrientJnt()
# cat.createRigJnt()


# ===========================================================================


def createLocatorsOnCurvePoint(curve:str, name: str) -> list:
    """ Create Locators on Curve Point.
    Examples
    --------
    >>> createLocatorsOnCurvePoint("cuv_Neck", "Neck")
    >>> createLocatorsOnCurvePoint("cuv_Spine", "Spine")
    >>> createLocatorsOnCurvePoint("cuv_Tail", "Tail")

    Return
    ------
    >>> ["loc_NeckCurvePoint", "loc_NeckCurvePoint1", ...]
     """
    cuv = pm.PyNode(curve)
    curveShape = cuv.getShape()
    curvePosition = curveShape.getCVs(space="world")
    locators = []
    for idx, pos in enumerate(curvePosition):
        num = "%s" % (idx if idx else "")
        loc = pm.spaceLocator(p=(0, 0, 0), n=f"loc_{name}CurvePoint{num}")
        pm.move(loc, pos)
        locators.append(loc)
    for i, loc in enumerate(locators):
        locShape = loc.getShape()
        pm.connectAttr(f"{locShape}.worldPosition[0]", 
                       f"{curveShape}.controlPoints[{i}]", f=True)
    locators_grp = groupOwnPivot(*locators)
    pm.group(locators_grp[::2], n=f"{locators[0]}s")
    return locators_grp


# locatorGroups = createLocatorsOnCurvePoint("cuv_Tail", "Tail")
# locatorGroups = ["loc_SpineCurvePoint%s" % (i if i else "") for i in range(6)]
# locatorGroups = ["loc_SpineCurvePoint%s" % (i if i else "") for i in range(5, 11)]


def constraintParentByDistance(ctrl1, ctrl2, locatorGroups):
    pos1, pos2 = [getPosition(i) for i in [ctrl1, ctrl2]]
    totalRange = getDistance(pos1, pos2)
    for i in locatorGroups:
        unitRange = getDistance(pos1, getPosition(i))
        dRatio = round(unitRange/totalRange, 5)
        pm.parentConstraint(ctrl1, i, mo=1, w=0 if 1-dRatio < 0 else 1-dRatio)
        pm.parentConstraint(ctrl2, i, mo=1, w=1 if dRatio >= 1 else dRatio)


# constraintParentByDistance("cc_Spine_IK_sub", "cc_Spine4_IK_sub", locatorGroups)
# constraintParentByDistance("cc_Spine4_IK_sub", "cc_Spine8_IK_sub", locatorGroups)


# ctrl1 = "cc_Tail6_IK_sub"
# ctrl2 = "cc_Tail8_IK_sub"
# locatorGroups = []
# for i in range(7, 11):
#     grpName = "loc_TailCurvePoint%s_grp" % (i if i else "")
#     locatorGroups.append(grpName)
# constraintParentByDistance(ctrl1, ctrl2, locatorGroups)


# ikHandle -> manually


# startJoint = "rig_Tail_IK"
# endJoint = "rig_Tail8_IK"
# curveName = "cuv_Tail"
# createJointScaleExpression(startJoint, endJoint, curveName, y=True)


# selectFKCtrls = pm.selected()
# for cc in selectFKCtrls:
#     jnt = cc.replace("cc_", "rig_")
#     pm.parentConstraint(cc, jnt, mo=True, w=1.0)


# ctrlAttr = "cc_Hips_main.%s_IK0_FK1" % "Left_Arm"
# joints = cat.legs_LF
# rg = addPrefix(joints, ["rig_"], [])
# fk = addPrefix(joints, ["rig_"], ["_FK"])
# ik = addPrefix(joints, ["rig_"], ["_IK"])
# createBlendColor2(ctrlAttr, rg, fk, ik, s=True)


# Show and Hide Ctrls and Connect Stretch -> Manually


# =========================================================================


def createLegsFK():
    """ Select FKs Controllers """
    sel_ccFK = pm.selected()
    ccFK_grp = groupOwnPivot()
    for cc in sel_ccFK:
        jnt = cc.replace("cc_", "rig_")
        pm.parentConstraint(cc, jnt, mo=True, w=1.0)
    for idx, cc in enumerate(sel_ccFK):
        if idx+1 >= len(sel_ccFK):
            continue
        else:
            pm.parent(ccFK_grp[::2][idx+1], cc)
    

def createLegsIK():
    """ Select Legs Joints. """
    sel_jntIK = pm.selected()
    if not sel_jntIK:
        return
    sel_jntSpring = duplicateRange(sel_jntIK[0].name(), sel_jntIK[3], "", "_spring")
    A = "L" if "Left" in sel_jntIK[0].name() else "R"
    B = "F" if "Front" in sel_jntIK[0].name() else "B"
    AB = f"{A}{B}"
    ikH_spring = pm.ikHandle(sj=sel_jntSpring[0], ee=sel_jntSpring[3], 
                             sol="ikSpringSolver", n=f"ikHandle_{AB}_spring")
    ikH_rp = pm.ikHandle(sj=sel_jntIK[1], ee=sel_jntIK[3], 
                             sol="ikRPsolver", n=f"ikHandle_{AB}_rp")
    ikH_sc = pm.ikHandle(sj=sel_jntIK[3], ee=sel_jntIK[4], 
                             sol="ikSCsolver", n=f"ikHandle_{AB}_sc")
    ikH_sc1 = pm.ikHandle(sj=sel_jntIK[4], ee=sel_jntIK[5], 
                             sol="ikSCsolver", n=f"ikHandle_{AB}_sc1", )
    pm.parent(ikH_rp[0], ikH_spring[0])
    groupOwnPivot(ikH_sc1[0])
    pm.parent(sel_jntIK[0].name(), sel_jntSpring[0])
    for i in sel_jntSpring:
        setJointsStyle(i, n=True)
    createPolevectorJoint(sel_jntIK[1], sel_jntIK[2], sel_jntIK[3])
    ccShoulder = sel_jntIK[0].name()
    ccShoulder = ccShoulder.replace("rig_", "cc_")
    pm.pointConstraint(ccShoulder, sel_jntSpring[0], mo=True, w=1.0)
    pm.connectAttr(f"{ccShoulder}.rotate", f"{sel_jntIK[0]}.rotate", f=True)


def createLegsAttrs(ccLegsIK: str):
    """ 
    Args
    ----
    >>> createLegsAttrs(cc_LeftFrontToe_IK)
    >>> createLegsAttrs(cc_RightFrontToe_IK)
    >>> createLegsAttrs(cc_LeftBackToe_IK)
    >>> createLegsAttrs(cc_RightBackToe_IK)
     """
    if not ccLegsIK:
        return
    attr = ["Bank", "Spring", "Up_Spring", "Down_Spring"]
    pm.addAttr(ccLegsIK, ln=attr[0], at="double", dv=0)
    pm.setAttr(f"{ccLegsIK}.{attr[0]}", e=True, k=True)
    pm.addAttr(ccLegsIK, ln=attr[1], at="bool", dv=1)
    pm.setAttr(f"{ccLegsIK}.{attr[1]}", e=True, k=True)
    pm.addAttr(ccLegsIK, ln=attr[2], at="double", dv=0.5, min=0, max=1)
    pm.setAttr(f"{ccLegsIK}.{attr[2]}", e=True, k=True)
    pm.addAttr(ccLegsIK, ln=attr[3], at="double", dv=0.5, min=0, max=1)
    pm.setAttr(f"{ccLegsIK}.{attr[3]}", e=True, k=True)
    A = "L" if "Left" in ccLegsIK else "R"
    B = "F" if "Front" in ccLegsIK else "B"
    AB = "%s%s" % (A, B)
    pm.connectAttr(f"{ccLegsIK}.Spring", f"ikHandle_{AB}_spring.ikBlend")
    pm.connectAttr(f"{ccLegsIK}.Up_Spring", f"ikHandle_{AB}_spring.springAngleBias[0].springAngleBias_FloatValue")
    pm.connectAttr(f"{ccLegsIK}.Down_Spring", f"ikHandle_{AB}_spring.springAngleBias[1].springAngleBias_FloatValue")
    clampNode = pm.shadingNode("clamp", au=True)
    pm.setAttr(f"{clampNode}.minR", -180)
    pm.setAttr(f"{clampNode}.maxG", 180)
    pm.connectAttr(f"{ccLegsIK}.Bank", f"{clampNode}.inputR")
    pm.connectAttr(f"{ccLegsIK}.Bank", f"{clampNode}.inputG")
    C = "Left" if A == "L" else "Right"
    D = "Front" if B == "F" else "Back"
    if A == "L":
        I = "BankIn"
        O = "BankOut"
    else:
        I = "BankOut"
        O = "BankIn"
    pm.connectAttr(f"{clampNode}.outputR", f"grp_{C}{D}{O}_IK.rotateZ")
    pm.connectAttr(f"{clampNode}.outputG", f"grp_{C}{D}{I}_IK.rotateZ")


def connectLegsJoints(attr: str, joints: list):
    """ Main Controller is "cc_Hips_main"
    Examples
    --------
    >>> connectLegsJoints("Left_Leg", cat.legs_LB)
     """
    ctrlAttr = "cc_Hips_main.%s_IK0_FK1" % attr
    Org = addPrefix(joints, ["rig_"], [])
    FKs = addPrefix(joints, ["rig_"], ["_FK"])
    IKs = addPrefix(joints, ["rig_"], ["_IK"])
    setRangeNode = createBlendColor2(ctrlAttr, Org, FKs, IKs, s=True)
    reverseNode = pm.shadingNode("reverse", au=True)
    pm.connectAttr(f"{setRangeNode}.outValueX", f"{reverseNode}.inputX", f=True)
    for rg, fk, ik in zip(Org, FKs, IKs):
        fkConstraint = pm.parentConstraint(fk, rg, mo=True, w=1.0)
        ikConstraint = pm.parentConstraint(ik, rg, mo=True, w=1.0)
        pm.connectAttr(f"{setRangeNode}.outValueX", f"{fkConstraint}.{fk}W0", f=True)
        pm.connectAttr(f"{reverseNode}.outputX", f"{ikConstraint}.{ik}W1", f=True)


# createLegsFK()
# createLegsIK()
# createLegsAttrs("cc_RightBackToe_IK")
# connectLegsJoints("Right_Leg", cat.legs_RB)


# ===========================================================================


def connectBones():
    joints = cat.jntPosition.keys()
    joints = list(joints)
    rgJoints = addPrefix(joints, ["rig_"], [])
    for rgJnt, jnt in zip(rgJoints, joints):
        for attr in ["translate", "rotate", "scale"]:
            pm.connectAttr(f"{rgJnt}.{attr}", f"{jnt}.{attr}", f=1)


def disConnectBones():
    joints = cat.jntPosition.keys()
    joints = list(joints)
    rgJoints = addPrefix(joints, ["rig_"], [])
    for rgJnt, jnt in zip(rgJoints, joints):
        for attr in ["translate", "rotate", "scale"]:
            pm.disconnectAttr(f"{rgJnt}.{attr}", f"{jnt}.{attr}")


# connectBones()
# disConnectBones()


# ===========================================================================


sel = pm.selected()
# for cc in sel:
#     cc_grp = f"{cc}_grp"
#     copied = pm.duplicate(cc_grp, rr=True)[0]
#     pm.select(cl=True)
#     pm.select(copied, hi=True)
#     reName("2", "3")
#     tmp = reName("grp1", "grp")[0]
#     bone = tmp.split("_")[1]
#     pm.matchTransform(copied, bone, pos=True)
#     pm.parent(copied, cc)


# for cc in sel:
#     jnt = cc.replace("cc_", "rig_")
#     pm.parentConstraint(cc, jnt, mo=True, w=1.0)


# for cc in sel:
#     pm.addAttr(cc, ln="Finger_Controllers", at="enum", en="Off:On:")
#     pm.setAttr(f"{cc}.Finger_Controllers", e=True, keyable=True)
#     pm.addAttr(cc, ln="Spread_Finger", at="double", min=0, max=10, dv=0)
#     pm.setAttr(f"{cc}.Spread_Finger", e=True, keyable=True)
#     pm.addAttr(cc, ln="Claw_Controllers", at="enum", en="Off:On:")
#     pm.setAttr(f"{cc}.Claw_Controllers", e=True, keyable=True)
#     pm.addAttr(cc, ln="Index_Out", at="double", min=0, max=10, dv=0)
#     pm.setAttr(f"{cc}.Index_Out", e=True, keyable=True)
#     pm.addAttr(cc, ln="Middle_Out", at="double", min=0, max=10, dv=0)
#     pm.setAttr(f"{cc}.Middle_Out", e=True, keyable=True)
#     pm.addAttr(cc, ln="Ring_Out", at="double", min=0, max=10, dv=0)
#     pm.setAttr(f"{cc}.Ring_Out", e=True, keyable=True)
#     pm.addAttr(cc, ln="Pinky_Out", at="double", min=0, max=10, dv=0)
#     pm.setAttr(f"{cc}.Pinky_Out", e=True, keyable=True)


def reNameClaws(key, side):
    sel = pm.selected()
    name = [
        "geo_clawsNail_%s_%s_1" % (key, side), 
        "geo_clawsNail_%s_%s_2" % (key, side), 
        "geo_clawsTissue_%s_%s_1" % (key, side), 
        ]
    for obj, objName in zip(sel, name):
        pm.select(cl=True)
        pm.select(obj)
        reName(objName)
    pm.group(sel[:2], n="geo_clawsNail_%s_%s_grp" % (key, side))
    pm.group(sel[-1], n="geo_clawsTissue_%s_%s_grp" % (key, side))


# reNameClaws("pinky", "RB")


# for i in sel:
#     pm.select(cl=True)
#     pm.select(i)
#     reName("cc_", "cc_claws_")


# for i in sel:
#     pm.setAttr(f"{i}.displayRotatePivot", 1)


# a, b, c, d = sel
# aP = a.getParent()
# cn = a.replace("4", "Claw")
# dn = a.replace("4", "ClawEnd")
# firstJnt = a.replace("4", "1")
# new = a + "temp"
# e = pm.rename(a, new)
# f = pm.rename(b, a)
# pm.delete(e)
# pm.rename(c, cn)
# pm.rename(d, dn)
# pm.parent(f, aP)
# pm.rename(f, f.replace("temp", ""))
# pm.joint(firstJnt, e=True, oj="yzx", secondaryAxisOrient="yup", ch=True, zso=True)
# pm.joint(dn, e=True, oj="none", ch=True, zso=True)


# result = []
# for i in sel:
#     new = i.replace("rig_", "")
#     pm.duplicate(i, rr=True, n=new)
#     result.append(new)
# pm.parent(result, w=True)
# pm.select(result)
# sel = pm.selected()
# print(sel)
# for i in sel:
#     pm.select(i, hi=True)
#     for j in pm.selected():
#         new = j.replace("rig_", "")
#         try:
#             pm.rename(j, new)
#         except:
#             continue


# Controllers().createControllers(square="")
# Controllers().createControllers(pointer2="")

# for i in sel:
#     cc = pm.duplicate("curve1", rr=True)[0]
#     pm.matchTransform(cc, i, pos=True, rot=True)
#     if "Claw" in i.name():
#         pm.scale(cc, (0.4, 0.4, 0.4))
#         pm.rotate(cc, (90, 0, 0), r=True, os=True, fo=True)
#         pm.rotate(cc, (0, -90, 0), r=True, os=True, fo=True)
#         pm.rotate(cc, (0, -90, 0), r=True, os=True, fo=True)
#     else:
#         pm.scale(cc, (0.6, 0.6, 0.6))
#         pm.rotate(cc, (0, 90, 0), r=True, os=True, fo=True)
#         pm.rotate(cc, (0, 90, 0), r=True, os=True, fo=True)
#     ccName = i.replace("rig_", "cc_")
#     pm.rename(cc, ccName)




# for i in range(0, len(sel), 2):
#     o = sel[i]
#     n = sel[i+1]
#     pm.parentConstraint(o, n, mo=True, w=1.0)
#     pm.currentTime(0)
#     pm.setKeyframe(n, at=["translateX","translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])
#     pm.setAttr(f"{n}.blendParent1", 1)
#     pm.currentTime(10)
#     pm.setKeyframe(n, at=["translateX","translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])
#     pm.currentTime(0)


# reName("cc_clawIndex_LF_grp")
# showNameAndPosition()
joints = [
    'Hips', 
    'Spine2', 'Spine4', 'Spine6', 'Spine8', 
    'Neck', 'Neck1', 'Neck2', 
    'Head', 
    'Jaw', 'Jaw_End', 
    'LeftEar', 'LeftEar1', 'RightEar', 'RightEar1', 
    'LeftFrontShoulder', 
    'LeftFrontLeg', 
    'LeftFrontKnee', 
    'LeftFrontAnkle', 
    'LeftFrontToe', 
    'LeftFrontIndex1', 'LeftFrontIndex2', 'LeftFrontIndex3', 
    'LeftFrontMiddle1', 'LeftFrontMiddle2', 'LeftFrontMiddle3', 
    'LeftFrontRing1', 'LeftFrontRing2', 'LeftFrontRing3', 
    'LeftFrontPinky1', 'LeftFrontPinky2', 'LeftFrontPinky3', 
    'RightFrontShoulder', 
    'RightFrontLeg', 
    'RightFrontKnee', 
    'RightFrontAnkle', 
    'RightFrontToe', 
    'RightFrontIndex1', 'RightFrontIndex2', 'RightFrontIndex3', 
    'RightFrontMiddle1', 'RightFrontMiddle2', 'RightFrontMiddle3', 
    'RightFrontRing1', 'RightFrontRing2', 'RightFrontRing3', 
    'RightFrontPinky1', 'RightFrontPinky2', 'RightFrontPinky3', 
    'LeftBackShoulder', 
    'LeftBackLeg', 
    'LeftBackKnee', 
    'LeftBackAnkle', 
    'LeftBackToe', 
    'LeftBackIndex1', 'LeftBackIndex2', 'LeftBackIndex3', 
    'LeftBackMiddle1', 'LeftBackMiddle2', 'LeftBackMiddle3', 
    'LeftBackRing1', 'LeftBackRing2', 'LeftBackRing3', 
    'LeftBackPinky1', 'LeftBackPinky2', 'LeftBackPinky3', 
    'RightBackShoulder', 
    'RightBackLeg', 
    'RightBackKnee', 
    'RightBackAnkle', 
    'RightBackToe', 
    'RightBackIndex1', 'RightBackIndex2', 'RightBackIndex3', 
    'RightBackMiddle1', 'RightBackMiddle2', 'RightBackMiddle3', 
    'RightBackRing1', 'RightBackRing2', 'RightBackRing3', 
    'RightBackPinky1', 'RightBackPinky2', 'RightBackPinky3', 
    'Tail', 
    'Tail1', 
    'Tail2', 
    'Tail3', 
    'Tail4', 
    'Tail5', 
    'Tail6', 
    'Tail7', 
    'Tail8', 
    "Spine8_A", 
    "Spine8_BC", 
    "Spine8_BL", 
    "Spine8_BR", 
    "Spine_C1", 
    "Spine_C2", 
    "Spine_C3", 
    "Spine2_L1", 
    "Spine2_L2", 
    "Spine2_L3", 
    "Spine2_R1", 
    "Spine2_R2", 
    "Spine2_R3", 
    "Spine4_L1", 
    "Spine4_L2", 
    "Spine4_L3", 
    "Spine4_R1", 
    "Spine4_R2", 
    "Spine4_R3", 
    "Spine6_L1", 
    "Spine6_L2", 
    "Spine6_L3", 
    "Spine6_R1", 
    "Spine6_R2", 
    "Spine6_R3", 
    ]
# objects = ["geo_middle"]
# jointsAndObjects = joints + objects
# createPaintWeightToOne(5, *jointsAndObjects)
# sel = pm.select(joints)
# deletePlugins()
# Controllers().createControllers(cube="")
# a = "prop_scissorsA_mdl_v9999:scissorsA_C_spring.vtx[0:7]"
# pos = getBoundingBoxPosition(a)
# loc = pm.spaceLocator(p=(0,0,0))
# pm.move(loc, pos)
# getBoundingBoxPosition()

# curvePoints = []
# reName("jnt_Sping1")
# groupOwnPivot()
# createRigGroups("scissorsA")
# createJointScaleExpression("jnt_Sping1", "jnt_Sping56", "cuv_Spring", x=True)
# colorize(yellow=True)

# def createCurveAndJointsThroughTheTube(tubeName, 
#                                        firstPointNumber, 
#                                        lastPointNumber, 
#                                        numberOfPointGroup, 
#                                        numberOfJoints):
#     firstPointGroup = tubeName.vtx[%d:%d]
#     for i in range(0, 4401, 80):
#         vtx = "prop_scissorsA_mdl_v9999:scissorsA_C_spring.vtx[%d:%d]" % (i, i+7)
#         pos = getBoundingBoxPosition(vtx)
#         jnt = pm.joint(p=(0, 0, 0))
#         pm.move(jnt, pos)
#         curvePoints.append(pos)
#     pm.curve(d=3, ep=curvePoints)


# for i in sel:
#     pm.connectAttr("Main_Control.Skeletons", f"{i}.visibility", f=True)
# selectJointOnly()
# colorize(yellow=True)


def bindSkin_claws():
    clawsDict = {
        'LeftFrontIndex4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_D_2_tissue'], 
        'LeftFrontIndexClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_D_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_L_D_1_bone'], 
        'LeftFrontMiddle4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_C_2_tissue'], 
        'LeftFrontMiddleClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_C_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_L_C_1_bone'], 
        'LeftFrontRing4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_B_2_tissue'], 
        'LeftFrontRingClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_B_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_L_B_1_bone'], 
        'LeftFrontPinky4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_A_2_tissue'], 
        'LeftFrontPinkyClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_L_A_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_L_A_1_bone'], 
        'RightFrontIndex4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_D_2_tissue'], 
        'RightFrontIndexClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_D_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_R_D_3_int'], 
        'RightFrontMiddle4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_C_2_tissue'], 
        'RightFrontMiddleClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_C_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_R_C_3_int'], 
        'RightFrontRing4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_B_2_tissue'], 
        'RightFrontRingClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_B_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_R_B_1_bone'], 
        'RightFrontPinky4': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_A_2_tissue'], 
        'RightFrontPinkyClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Ft_R_A_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Ft_R_A_3_int'], 
        'LeftBackIndex4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_D_2_tissue'], 
        'LeftBackIndexClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_D_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_L_D_3_int'], 
        'LeftBackMiddle4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_C_2_tissue'], 
        'LeftBackMiddleClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_C_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_L_C_1_bone'], 
        'LeftBackRing4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_B_2_tissue'], 
        'LeftBackRingClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_B_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_L_B_1_bone'], 
        'LeftBackPinky4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_A_2_tissue'], 
        'LeftBackPinkyClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_L_A_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_L_A_3_int'], 
        'RightBackIndex4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_D_2_tissue'], 
        'RightBackIndexClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_D_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_R_D_1_bone'], 
        'RightBackMiddle4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_C_2_tissue'], 
        'RightBackMiddleClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_C_3_int', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_R_C_1_bone'], 
        'RightBackRing4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_B_2_tissue'], 
        'RightBackRingClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_B_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_R_B_3_int'], 
        'RightBackPinky4': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_A_2_tissue'], 
        'RightBackPinkyClaw': ['char_tigerA_mdl_v9999:tigerA_claws_Bk_R_A_1_bone', 'char_tigerA_mdl_v9999:tigerA_claws_Bk_R_A_3_int'], 
        }
    for jnt, objList in clawsDict.items():
        for obj in objList:
            pm.skinCluster(jnt, obj, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=1, foc=True)


def bindSkin_thumbClaw():
    jnt_thumbClaw_L = [f"LeftFront{i}" for i in ["Ankle", "Toe", "Index1", "Index2"]]
    obj_thumbClaw_L = ["char_tigerA_mdl_v9999:tigerA_claws_Ft_L_E_2_tissue", "char_tigerA_mdl_v9999:tigerA_claws_Ft_L_E_1_bone", "char_tigerA_mdl_v9999:tigerA_claws_Ft_L_E_3_int"]
    for obj in obj_thumbClaw_L:
        pm.skinCluster(jnt_thumbClaw_L, obj, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=4, foc=True)
    jnt_thumbClaw_R = [f"RightFront{i}" for i in ["Ankle", "Toe", "Index1", "Index2"]]
    obj_thumbClaw_R = ["char_tigerA_mdl_v9999:tigerA_claws_Ft_R_E_2_tissue", "char_tigerA_mdl_v9999:tigerA_claws_Ft_R_E_1_bone", "char_tigerA_mdl_v9999:tigerA_claws_Ft_R_E_3_int"]
    for obj in obj_thumbClaw_R:
        pm.skinCluster(jnt_thumbClaw_R, obj, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=4, foc=True)


# bindSkin_claws()
# bindSkin_thumbClaw()


# sel = pm.selected()
# for num, obj in enumerate(sel):
#     tx = 100*num + 100
#     pm.setAttr(f"{obj}.translateX", -1*tx)


def createBlendShapeDict():
    sel = pm.selected()
    result = {}
    for i in sel:
        temp = i.split("_")[1]
        if "Lt" in temp:
            objName = temp.replace("Lt", "")
            side = "_L"
        elif "Rt" in temp:
            objName = temp.replace("Rt", "")
            side = "_R"
        else:
            objName = temp
            side = ""
        objList = []
        for j in pm.ls():
            if objName in j.name() and "tigerA" in j.name() and side in j.name() and not "Shape" in j.name():
                objList.append(j.name())
        result[i.name()] = objList
    print(result)


# createBlendShapeDict()


blendShapedict = {
    'faceControlUI_NSsnarlLt_NSSLL_CON': ['char_tigerA_mdl_v9999:NSsnarl_L'], 
    'faceControlUI_MOnarrowRt_MONR_CON': ['char_tigerA_mdl_v9999:MOnarrow_R'], 
    'faceControlUI_EYsquintLt_EYSL_CON': ['char_tigerA_mdl_v9999:EYsquint_L'], 
    'faceControlUI_CKsuckPuffLt_CKSPL_CON': ['char_tigerA_mdl_v9999:CKsuckPuff_1_L', 'char_tigerA_mdl_v9999:CKsuckPuff_2_L'], 
    'faceControlUI_NSsneerLt_NSSRL_CON': ['char_tigerA_mdl_v9999:NSsneer_L'], 
    'faceControlUI_SPscalpForwardBackLt_SPSFBL_CON': ['char_tigerA_mdl_v9999:SPscalpForwardBack_1_L', 'char_tigerA_mdl_v9999:SPscalpForwardBack_2_L'], 
    'faceControlUI_NSsnarlRt_NSSLR_CON': ['char_tigerA_mdl_v9999:NSsnarl_R'], 
    'faceControlUI_MOsmileLt_MOSLL_CON': ['char_tigerA_mdl_v9999:MOsmile_L'], 
    'faceControlUI_NEtenseLt_NETL_CON': ['char_tigerA_mdl_v9999:NEtense_L'], 
    'faceControlUI_JWclenchLt_JWCHL_CON': ['char_tigerA_mdl_v9999:JWclench_L'], 
    'faceControlUI_EBinnerUpRt_EBIUR_CON': ['char_tigerA_mdl_v9999:EBinnerUp_R'], 
    'faceControlUI_MOgrimaceRt_MOGR_CON': ['char_tigerA_mdl_v9999:MOgrimace_R'], 
    'faceControlUI_MOlipCornerOpenCloseRt_MOLCOCR_CON': ['char_tigerA_mdl_v9999:MOlipCornerOpenClose_1_R', 'char_tigerA_mdl_v9999:MOlipCornerOpenClose_2_R'], 
    'faceControlUI_EYtightenRt_EYTR_CON': ['char_tigerA_mdl_v9999:EYtighten_R'], 
    'faceControlUI_EBouterUpRt_EBOUR_CON': ['char_tigerA_mdl_v9999:EBouterUp_R'], 
    'faceControlUI_NSdownRt_NSDR_CON': ['char_tigerA_mdl_v9999:NSdown_R'], 
    'faceControlUI_NSwrinkleRt_NSWR_CON': ['char_tigerA_mdl_v9999:NSwrinkle_R'], 
    'faceControlUI_NEtenseRt_NETR_CON': ['char_tigerA_mdl_v9999:NEtense_R'], 
    'faceControlUI_EBfurrowBottomRt_EBFBTR_CON': ['char_tigerA_mdl_v9999:EBfurrowBottom_R'], 
    'faceControlUI_NEtongueFlick_NETF_CON': ['char_tigerA_mdl_v9999:NEtongueFlick'], 
    'faceControlUI_NEswallow_NES_CON': ['char_tigerA_mdl_v9999:NEswallow'], 
    'faceControlUI_MOlipDepressorLt_MOLDL_CON': ['char_tigerA_mdl_v9999:MOlipDepressor_L'], 
    'faceControlUI_CHupLt_CHUL_CON': ['char_tigerA_mdl_v9999:CHup_L'], 
    'faceControlUI_CHupRt_CHUR_CON': ['char_tigerA_mdl_v9999:CHup_R'], 
    'faceControlUI_MOtogetherLt_MOTL_CON': ['char_tigerA_mdl_v9999:MOtogether_L'], 
    'faceControlUI_NSdownLt_NSDL_CON': ['char_tigerA_mdl_v9999:NSdown_L'], 
    'faceControlUI_MOmuzzlePuffLt_MOMPL_CON': ['char_tigerA_mdl_v9999:MOmuzzlePuff_L'], 
    'faceControlUI_NSflareInOutLt_NSFIOL_CON': ['char_tigerA_mdl_v9999:NSflareInOut_1_L', 'char_tigerA_mdl_v9999:NSflareInOut_2_L'], 
    'faceControlUI_MOlipCornerOpenCloseLt_MOLCOCL_CON': ['char_tigerA_mdl_v9999:MOlipCornerOpenClose_1_L', 'char_tigerA_mdl_v9999:MOlipCornerOpenClose_2_L'], 
    'faceControlUI_ERforwardBackLt_ERFBL_CON': ['char_tigerA_mdl_v9999:ERforwardBack_1_L', 'char_tigerA_mdl_v9999:ERforwardBack_2_L'], 
    'faceControlUI_NSwrinkleLt_NSWL_CON': ['char_tigerA_mdl_v9999:NSwrinkle_L'], 
    'faceControlUI_MOwideLt_MOWL_CON': ['char_tigerA_mdl_v9999:MOwide_L'], 
    'faceControlUI_MOnarrowLt_MONL_CON': ['char_tigerA_mdl_v9999:MOnarrow_L'], 
    'faceControlUI_EBdownLt_EBDL_CON': ['char_tigerA_mdl_v9999:EBdown_L'], 
    'faceControlUI_EBfurrowTopLt_EBFTPL_CON': ['char_tigerA_mdl_v9999:EBfurrowTop_L'], 
    'faceControlUI_MOmuzzlePuffRt_MOMPR_CON': ['char_tigerA_mdl_v9999:MOmuzzlePuff_R'], 
    'faceControlUI_EYtightenLt_EYTL_CON': ['char_tigerA_mdl_v9999:EYtighten_L'], 
    'faceControlUI_SPscalpForwardBackRt_SPSFBR_CON': ['char_tigerA_mdl_v9999:SPscalpForwardBack_1_R', 'char_tigerA_mdl_v9999:SPscalpForwardBack_2_R'], 
    'faceControlUI_MOtogetherRt_MOTR_CON': ['char_tigerA_mdl_v9999:MOtogether_R'], 
    'faceControlUI_EYcloseWideLt_EYBWL_CON': ['char_tigerA_mdl_v9999:EYcloseWide_1_L', 'char_tigerA_mdl_v9999:EYcloseWide_2_L'], 
    'faceControlUI_NSflareInOutRt_NSFIOR_CON': ['char_tigerA_mdl_v9999:NSflareInOut_1_R', 'char_tigerA_mdl_v9999:NSflareInOut_2_R'], 
    'faceControlUI_MOupperLipRaiserRt_MOULRR_CON': ['char_tigerA_mdl_v9999:MOupperLipRaiser_R'], 
    'faceControlUI_ERforwardBackRt_ERFBR_CON': ['char_tigerA_mdl_v9999:ERforwardBack_1_R', 'char_tigerA_mdl_v9999:ERforwardBack_2_R'], 
    'faceControlUI_EBinnerUpLt_EBIUL_CON': ['char_tigerA_mdl_v9999:EBinnerUp_L'], 
    'faceControlUI_EYcloseWideRt_EYBWR_CON': ['char_tigerA_mdl_v9999:EYcloseWide_1_R', 'char_tigerA_mdl_v9999:EYcloseWide_2_R'], 
    'faceControlUI_MOsmirkLt_MOSRL_CON': ['char_tigerA_mdl_v9999:MOsmirk_L'], 
    'faceControlUI_EBfurrowBottomLt_EBFBTL_CON': ['char_tigerA_mdl_v9999:EBfurrowBottom_L'], 
    'faceControlUI_NSsneerRt_NSSRR_CON': ['char_tigerA_mdl_v9999:NSsneer_R'], 
    'faceControlUI_EYsquintRt_EYSR_CON': ['char_tigerA_mdl_v9999:EYsquint_R'], 
    'faceControlUI_CKupRt_CKUR_CON': ['char_tigerA_mdl_v9999:CKup_R'], 
    'faceControlUI_CKupLt_CKUL_CON': ['char_tigerA_mdl_v9999:CKup_L'], 
    'faceControlUI_MOsmirkRt_MOSRR_CON': ['char_tigerA_mdl_v9999:MOsmirk_R'], 
    'faceControlUI_EBfurrowTopRt_EBFTPR_CON': ['char_tigerA_mdl_v9999:EBfurrowTop_R'], 
    'faceControlUI_JWclenchRt_JWCHR_CON': ['char_tigerA_mdl_v9999:JWclench_R'], 
    'faceControlUI_MOwideRt_MOWR_CON': ['char_tigerA_mdl_v9999:MOwide_R'], 
    'faceControlUI_CKsuckPuffRt_CKSPR_CON': ['char_tigerA_mdl_v9999:CKsuckPuff_1_R', 'char_tigerA_mdl_v9999:CKsuckPuff_2_R'], 
    'faceControlUI_NSupRt_NSUR_CON': ['char_tigerA_mdl_v9999:NSup_R'], 
    'faceControlUI_MOsmileRt_MOSLL_CON': ['char_tigerA_mdl_v9999:MOsmile_R'], 
    'faceControlUI_EBdownRt_EBDR_CON': ['char_tigerA_mdl_v9999:EBdown_R'], 
    'faceControlUI_MOupperLipRaiserLt_MOULRL_CON': ['char_tigerA_mdl_v9999:MOupperLipRaiser_L'], 
    'faceControlUI_MOlipDepressorLt_MOLDR_CON': ['char_tigerA_mdl_v9999:MOlipDepressor_L'], 
    'faceControlUI_NSupLt_NSUL_CON': ['char_tigerA_mdl_v9999:NSup_L'], 
    'faceControlUI_MOgrimaceLt_MOGL_CON': ['char_tigerA_mdl_v9999:MOgrimace_L'], 
    'faceControlUI_EBouterUpLt_EBOUL_CON': ['char_tigerA_mdl_v9999:EBouterUp_L']
    }


def connectBlendShapeToController(ctrl=str, bls1=str, bls2=""):
    blsNode = "blendShape1"
    if not bls2:
        pm.connectAttr(f"{ctrl}.translateZ", f"{blsNode}.{bls1}", f=True)
    else:
        clp = pm.shadingNode("clamp", asUtility=True)
        pm.setAttr(f"{clp}.maxR", 1)
        pm.setAttr(f"{clp}.minG", -1)
        mld = pm.shadingNode("multiplyDivide", asUtility=True)
        pm.setAttr(f"{mld}.input2X", -1)
        pm.connectAttr(f"{ctrl}.translateZ", f"{clp}.inputR", f=True)
        pm.connectAttr(f"{ctrl}.translateZ", f"{clp}.inputG", f=True)
        pm.connectAttr(f"{clp}.outputR", f"{blsNode}.{bls1}", f=True)
        pm.connectAttr(f"{clp}.outputG", f"{mld}.input1X", f=True)
        pm.connectAttr(f"{mld}.outputX", f"{blsNode}.{bls2}", f=True)
    rmv = pm.shadingNode("remapValue", asUtility=True)
    pm.setAttr(f"{rmv}.inputMin", -0.01)
    pm.setAttr(f"{rmv}.inputMax", 0.01)
    pm.setAttr(f"{rmv}.outputMin", 6)
    pm.setAttr(f"{rmv}.outputMax", 13)
    pm.setAttr(f"{rmv}.value[0].value_FloatValue", 1)
    pm.setAttr(f"{rmv}.value[2].value_Position", 0.5)
    pm.setAttr(f"{rmv}.value[2].value_FloatValue", 0)
    pm.connectAttr(f"{ctrl}.translateZ", f"{rmv}.inputValue", f=True)
    pm.connectAttr(f"{rmv}.outValue", f"{ctrl}Shape.overrideColor", f=True)


# for ctrl, objList in blendShapedict.items():
#     tmp = [i.split(":")[-1] for i in objList]
#     if len(tmp) == 1:
#         connectBlendShapeToController(ctrl, tmp[0])
#     elif len(tmp) == 2:
#         connectBlendShapeToController(ctrl, tmp[0], tmp[1])
#     else:
#         pm.warning("objList number is incorrect.")

boneInfulenced = [
    'Hips', 
    'Spine', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Spine5', 'Spine6', 'Spine7', 'Spine8', 
    'Neck', 'Neck1', 'Neck2', 
    'Head', 
    'Jaw', 
    'LeftFrontShoulder', 'LeftFrontLeg', 'LeftFrontKnee', 'LeftFrontAnkle', 'LeftFrontToe', 
    'LeftFrontIndex1', 'LeftFrontIndex2', 
    'LeftFrontMiddle1', 'LeftFrontMiddle2', 
    'LeftFrontRing1', 'LeftFrontRing2', 
    'LeftFrontPinky1', 'LeftFrontPinky2', 
    'RightFrontShoulder', 'RightFrontLeg', 'RightFrontKnee', 'RightFrontAnkle', 'RightFrontToe', 
    'RightFrontIndex1', 'RightFrontIndex2', 
    'RightFrontMiddle1', 'RightFrontMiddle2', 
    'RightFrontRing1', 'RightFrontRing2', 
    'RightFrontPinky1', 'RightFrontPinky2', 
    'LeftBackShoulder', 'LeftBackLeg', 'LeftBackKnee', 'LeftBackAnkle', 'LeftBackToe', 
    'LeftBackIndex1', 'LeftBackIndex2', 
    'LeftBackMiddle1', 'LeftBackMiddle2', 
    'LeftBackRing1', 'LeftBackRing2', 
    'LeftBackPinky1', 'LeftBackPinky2', 
    'RightBackShoulder', 'RightBackLeg', 'RightBackKnee', 'RightBackAnkle', 'RightBackToe', 
    'RightBackIndex1', 'RightBackIndex2', 
    'RightBackMiddle1', 'RightBackMiddle2', 
    'RightBackRing1', 'RightBackRing2', 
    'RightBackPinky1', 'RightBackPinky2', 
    'Tail', 'Tail1', 'Tail2', 'Tail3', 'Tail4', 'Tail5', 'Tail6', 'Tail7', 'Tail8', 
    ]


