import pymel.core as pm
import hjk



class Coordinates:
    HUMAN = {
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
    CAR = {
        "root": {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_body_end": (0, 145, 0), 
        }, 
        "wheel_L_Ft": {
            "jnt_wheel_L_Ft": (70, 30, 140), 
            "jnt_wheel_L_Ft_end": (85, 30, 140), 
        }, 
        "wheel_R_Ft": {
            "jnt_wheel_R_Ft": (-70, 30, 140), 
            "jnt_wheel_R_Ft_end": (-85, 30, 140), 
        }, 
        "wheel_L_Bk": {
            "jnt_wheel_L_Bk": (70, 30, -140), 
            "jnt_wheel_L_Bk_end": (85, 30, -140), 
        }, 
        "wheel_R_Bk": {
            "jnt_wheel_R_Bk": (-70, 30, -140), 
            "jnt_wheel_R_Bk_end": (-85, 30, -140), 
        }, 
    }


class QuickRig_CAR:
    def __init__(self):
        self.circle = "carCircle"
        self.jntList = ["jnt_body", "jnt_wheel"]
        # self.createCarJoints()


    def getRadius(self, obj_sizeUp: dict):
        """ Create the controller 1.2 times the sizeUp of the object.
        If no parameters are given, the selected object is used.
         """
        result = []
        for obj, sizeUp in obj_sizeUp.items():
            bBox = pm.xform(obj, q=True, bb=True)
            xMin, yMin, zMin, xMax, yMax, zMax = bBox
            x = (xMax - xMin) / 2
            y = (yMax - yMin) / 2
            z = (zMax - zMin) / 2
            radius = max([x, y, z])
            radius = round(radius*sizeUp, 3)
            result.append(radius)
        return result


    def createCarJoints(self):
        try: pm.delete(self.circle)
        except: pass
        carJnt = Coordinates.CAR.values()
        branch = []
        for i in carJnt:
            pm.select(cl=True)
            for name, pos in i.items():
                jnt = pm.joint(p=(0, 0, 0), n=name, rad=10)
                pm.move(jnt, pos)
            headJnt = [j for j in i.keys()][0]
            branch.append(headJnt)
        hjk.orientJnt(branch)
        firstJnt = branch.pop(0)
        self.circle = hjk.createCircle("carCircle", 300, y=True)
        pm.parent(branch, firstJnt)
        pm.parent(firstJnt, self.circle)


    def makeWheelList(self):
        pm.select(self.circle, hi=True)
        selAll = pm.ls(sl=True)
        A = "wheel"
        B = "end"
        result = []
        for i in selAll:
            tmp = i.split("_")
            if A in tmp and B not in tmp:
                result.append(i)
            else:
                continue
        return result


    def createCarCtrl(self):
        ccDict = {
            "cc_main": {"car3": True}, 
            "cc_sub": {"car2": True}, 
            "cc_body": {"car": True}, 
        }
        carCircleSize = pm.getAttr(f"{self.circle}.scale")
        result = []
        for ccName, ctrlName in ccDict.items():
            tmp = hjk.ctrl(ctrlName)[0]
            cuv = pm.rename(tmp, ccName)
            pm.scale(cuv, carCircleSize)
            pm.makeIdentity(cuv, t=0, r=0, s=1, n=0, pn=0, a=True)
            if ccName == "cc_body":
                jnt = ccName.replace("cc_", "jnt_")
                pm.matchTransform(ccName, jnt, pos=True)
            result.append(cuv)
        return result


    def createWheelCtrl(self):
        carCircleSize = pm.getAttr(f"{self.circle}.scale")
        s = max(carCircleSize)
        jntWheelList = self.makeWheelList()
        result = []
        for i in jntWheelList:
            cc = i.replace("jnt_", "cc_")
            cc = pm.circle(nr=(1, 0, 0), n=cc, r=40, ch=0)[0]
            pm.scale(cc, [s, s, s])
            pm.makeIdentity(cc, t=0, r=0, s=1, n=0, pn=0, a=True)
            pm.matchTransform(cc, i, pos=True)
            result.append(cc)
        return result
        

    def deleteCarCircle(self):
        pm.delete(self.circle)


    def createGroup(self, ccMain: list, ccWheel: list):
        # Create groups with grpList.
        grpList = ["rig", "MODEL", "controller"]
        grpCtrl = [pm.group(em=True, n=i) for i in grpList].pop()
        # Create cc_main groups.
        grpMain = [hjk.groupingEmpty(i)[0] for i in ccMain]
        init = grpMain.pop(0)
        body = ccMain.pop(-1)
        for idx in range(2):
            pm.parent(grpMain[idx], ccMain[idx])
        pm.parent(init, grpCtrl)
        # Create cc_wheel groups.
        grpWheel = [hjk.groupingEmpty(i)[0] for i in ccWheel]
        pm.parent(grpWheel, grpCtrl)
        



car = QuickRig_CAR()
car.createCarJoints()
ccMain = car.createCarCtrl()
ccWheel = car.createWheelCtrl()
car.createGroup(ccMain, ccWheel)
car.deleteCarCircle()