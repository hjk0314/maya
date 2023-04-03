import pymel.core as pm
import hjk

# 79 char line ================================================================
# 72 docstring or comments line ========================================

class QuickRig_Human:
    def __init__(self):
        self.circle = "humanCircle"
        self.parentDict = {
            "jnt_root": ['jnt_spine_1', 'jnt_hip_L', 'jnt_hip_R'], 
            "jnt_spine_4": ['jnt_neck_1', 'jnt_scapula_L', 'jnt_scapula_R'], 
            "jnt_neck_2": ['jnt_head'], 
            "jnt_parm_L": [
                'jnt_thumb_L_1', 
                'jnt_index_L_1', 
                'jnt_middle_L_1', 
                'jnt_ring_L_1', 
                'jnt_pinky_L_1', 
            ], 
            "jnt_parm_R": [
                'jnt_thumb_R_1', 
                'jnt_index_R_1', 
                'jnt_middle_R_1', 
                'jnt_ring_R_1', 
                'jnt_pinky_R_1', 
            ], 
        }
        self.point = {
            'root': {
                'jnt_root': (0.0, 91.146, -2.311)
            }, 
            'spine': {
                'jnt_spine_1': (0.0, 101.79, -0.828), 
                'jnt_spine_2': (-0.0, 112.04, -0.291), 
                'jnt_spine_3': (-0.0, 121.978, -0.795), 
                'jnt_spine_4': (-0.0, 130.703, -2.506), 
            }, 
            'neck': {
                'jnt_neck_1': (-0.0, 139.579, -5.133), 
                'jnt_neck_2': (-0.0, 143.202, -3.147), 
            }, 
            'head': {
                'jnt_head': (-0.0, 151.415, -0.776), 
                'jnt_head_end': (-0.0, 164.146, -0.776), 
            }, 
            'arm_L': {
                'jnt_scapula_L': (7.581, 133.499, -4.058), 
                'jnt_shoulder_L': (16.671, 129.738, -3.624), 
                'jnt_elbow_L': (41.006, 127.424, -4.551), 
                'jnt_wrist_L': (66.078, 125.041, -4.841), 
                'jnt_parm_L': (71.356, 124.058, -4.841), 
            }, 
            'arm_R': {
                'jnt_scapula_R': (-7.581, 133.499, -4.058), 
                'jnt_shoulder_R': (-16.671, 129.738, -3.624), 
                'jnt_elbow_R': (-41.006, 127.424, -4.551), 
                'jnt_wrist_R': (-66.078, 125.041, -4.841), 
                'jnt_parm_R': (-71.356, 124.058, -4.841), 
            }, 
            'leg_L': {
                'jnt_hip_L': (10.968, 82.407, -0.453), 
                'jnt_knee_L': (13.083, 45.307, -1.572), 
                'jnt_ankle_L': (14.812, 8.647, -4.123), 
                'jnt_ball_L': (17.597, 1.022, 5.062), 
                'jnt_toe_L': (19.642, 0.075, 13.005), 
            }, 
            'leg_R': {
                'jnt_hip_R': (-10.968, 82.407, -0.453), 
                'jnt_knee_R': (-13.082, 45.307, -1.572), 
                'jnt_ankle_R': (-14.812, 8.647, -4.123), 
                'jnt_ball_R': (-17.597, 1.022, 5.062), 
                'jnt_toe_R': (-19.642, 0.075, 13.005), 
            }, 
            'thumb_L': {
                'jnt_thumb_L_1': (69.91, 123.216, -2.033), 
                'jnt_thumb_L_2': (71.54, 122.745, -0.221), 
                'jnt_thumb_L_3': (73.169, 122.275, 1.591), 
                'jnt_thumb_L_4': (74.799, 121.804, 3.403), 
            }, 
            'index_L': {
                'jnt_index_L_1': (74.697, 123.363, -2.847), 
                'jnt_index_L_2': (77.057, 123.282, -2.082), 
                'jnt_index_L_3': (79.417, 123.2, -1.318), 
                'jnt_index_L_4': (81.777, 123.119, -0.554), 
            }, 
            'middle_L': {
                'jnt_middle_L_1': (75.236, 123.622, -4.757), 
                'jnt_middle_L_2': (77.687, 123.519, -5.131), 
                'jnt_middle_L_3': (80.139, 123.415, -5.505), 
                'jnt_middle_L_4': (82.59, 123.312, -5.88), 
            }, 
            'ring_L': {
                'jnt_ring_L_1': (74.493, 123.638, -6.872), 
                'jnt_ring_L_2': (76.437, 123.465, -8.164), 
                'jnt_ring_L_3': (78.381, 123.293, -9.456), 
                'jnt_ring_L_4': (80.324, 123.12, -10.749), 
            }, 
            'pinky_L': {
                'jnt_pinky_L_1': (72.929, 123.458, -8.344), 
                'jnt_pinky_L_2': (73.715, 123.357, -10.018), 
                'jnt_pinky_L_3': (74.501, 123.257, -11.692), 
                'jnt_pinky_L_4': (75.286, 123.158, -13.366), 
            }, 
            'thumb_R': {
                'jnt_thumb_R_1': (-69.91, 123.216, -2.033), 
                'jnt_thumb_R_2': (-71.54, 122.745, -0.221), 
                'jnt_thumb_R_3': (-73.169, 122.275, 1.591), 
                'jnt_thumb_R_4': (-74.799, 121.804, 3.403), 
            }, 
            'index_R': {
                'jnt_index_R_1': (-74.697, 123.363, -2.847), 
                'jnt_index_R_2': (-77.057, 123.282, -2.082), 
                'jnt_index_R_3': (-79.417, 123.2, -1.318), 
                'jnt_index_R_4': (-81.777, 123.119, -0.554), 
            }, 
            'middle_R': {
                'jnt_middle_R_1': (-75.236, 123.622, -4.757), 
                'jnt_middle_R_2': (-77.687, 123.519, -5.131), 
                'jnt_middle_R_3': (-80.139, 123.415, -5.505), 
                'jnt_middle_R_4': (-82.59, 123.312, -5.88), 
            }, 
            'ring_R': {
                'jnt_ring_R_1': (-74.493, 123.638, -6.872), 
                'jnt_ring_R_2': (-76.437, 123.465, -8.164), 
                'jnt_ring_R_3': (-78.381, 123.293, -9.456), 
                'jnt_ring_R_4': (-80.324, 123.12, -10.749), 
            }, 
            'pinky_R': {
                'jnt_pinky_R_1': (-72.929, 123.458, -8.344), 
                'jnt_pinky_R_2': (-73.715, 123.357, -10.018), 
                'jnt_pinky_R_3': (-74.501, 123.257, -11.692), 
                'jnt_pinky_R_4': (-75.285, 123.158, -13.366), 
            }, 
        }


    def createTempJoints(self):
        try: pm.delete(self.circle)
        except: pass
        humanJnt = self.point.values()
        branch = []
        for i in humanJnt:
            pm.select(cl=True)
            for name, pos in i.items():
                jnt = pm.joint(p=(0, 0, 0), n=name, rad=10)
                pm.move(jnt, pos)
            headJnt = [j for j in i.keys()][0]
            branch.append(headJnt)
        hjk.orientJnt(branch)
        self.circle = hjk.createCircle(self.circle, 60, y=True)
        tmp = [pm.parent(k, j) for j, k in self.parentDict.items()]
        pm.parent(branch[0], self.circle)


    def createCtrls(self):
        pass
        # self.createMainCtrl()
        # self.createRootCtrl()
        # self.createSpineCtrl()
        # self.createNeckCtrl()
        # self.createHeadCtrl()
        # self.createEyeCtrl()
        # self.createArmCtrl()
        # self.createLegCtrl()
        # self.createFingerCtrl()


human = QuickRig_Human()
human.createTempJoints()
