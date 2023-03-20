
import pymel.core as pm


class Coordinates:
    CTRL = {
        "cub": [
            (-1, 1, -1), (-1, 1, 1), (1, 1, 1), 
            (1, 1, -1), (-1, 1, -1), (-1, -1, -1), 
            (-1, -1, 1), (1, -1, 1), (1, -1, -1), 
            (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), 
            (1, 1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1), 
        ], 
        "sph": [
            (0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), 
            (0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), 
            (0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), 
            (-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), 
            (0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), 
            (0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), 
            (-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), 
            (0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), (0, 1, 0), 
        ], 
        "head": [
            (13, 0, -11), (0, 10, -15), (-13, 0, -11), 
            (-14, -9, 0), (-13, 0, 11), (0, 10, 15), 
            (13, 0, 11), (14, -9, 0)
        ], 
        "scapula": [
            (2, 10, -11), (0, 0, -11), (-2, 10, -11), 
            (-3, 18, 0), (-2, 10, 11), (0, 0, 11), 
            (2, 10, 11), (3, 18, 0)
        ], 
        "foot": [
            (-6, 12, -14), (-6, 12, 6), (6, 12, 6), 
            (6, 12, -14), (-6, 12, -14), (-6, 0, -14), 
            (-6, 0, 18), (6, 0, 18), (6, 0, -14), 
            (-6, 0, -14), (-6, 0, 18), (-6, 12, 6), 
            (6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14), 
        ], 
        "car": [
            (81, 70, 119), (89, 56, 251), (89, -12, 251), 
            (89, -12, 117), (89, -12, -117), (89, -12, -229), 
            (81, 70, -229), (81, 70, -159), (69, 111, -105), 
            (69, 111, 63), (81, 70, 119), (-81, 70, 119), 
            (-89, 56, 251), (-89, -12, 251), (-89, -12, 117), 
            (-89, -12, -117), (-89, -12, -229), (-81, 70, -229), 
            (-81, 70, -159), (-69, 111, -105), (69, 111, -105), 
            (81, 70, -159), (-81, 70, -159), (-81, 70, -229), 
            (81, 70, -229), (89, -12, -229), (-89, -12, -229), 
            (-89, -12, -117), (-89, -12, 117), (-89, -12, 251), 
            (89, -12, 251), (89, 56, 251), (-89, 56, 251), 
            (-81, 70, 119), (-69, 111, 63), (-69, 111, -105), 
            (69, 111, -105), (69, 111, 63), (-69, 111, 63)
        ], 
        "car2": [
            (165, 0, -195), (0, 0, -276), (-165, 0, -195), 
            (-97, 0, -0), (-165, -0, 195), (-0, -0, 276), 
            (165, -0, 195), (97, -0, 0), (165, 0, -195), 
        ], 
    }
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


def tempJnt() -> str:
    all = Coordinates.jnt
    head = [list(i.keys())[0] for i in all.values()]
    for jntDict in all.values():
        pm.select(cl=True)
        for name, pos in jntDict.items():
            jnt = pm.joint(p=(0, 0, 0), n=name, rad=10)
            pm.move(jnt, pos)
        jntList = list(jntDict)
        Tools().orientJnt(jntList)
    cuv = Tools().createCuv(50)
    pm.parent(head, cuv)
    return cuv


class Tools:
    def __init__(self):
        pass


    def orientJnt(self, jnt: list) -> None:
        init = jnt[0]
        last = jnt[-1]
        pm.makeIdentity(jnt, a=True, jo=True, n=0)
        pm.joint(init, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(last, e=True, oj='none', ch=True, zso=True)


    def createCuv(self, size: float, **kwargs) -> str:
        nor = {
            "x": (1, 0, 0), 
            "y": (0, 1, 0), 
            "z": (0, 0, 1), 
        }
        if not kwargs:
            axis = (0, 1, 0)
        else:
            for k, v in kwargs.items():
                if not k in nor.keys():
                    axis = (0, 1, 0)
                    continue
                elif not v:
                    axis = (0, 1, 0)
                    continue
                else:
                    axis = nor[k]
        cuv = pm.circle(nr=axis, ch=False)[0]
        pm.scale(cuv, [size, size, size])
        pm.makeIdentity(cuv, a=True, n=0)
        return cuv


    def getHeadJnt(self, *arg):
        sel = pm.ls(arg, dag=True, type=['transform'])
        jnt = []
        for i in sel:
            typ = pm.objectType(i)
            if typ != 'joint' or i.endswith("_end"):
                continue
            else:
                jnt.append(i)
        return jnt


class quickRig_CAR:
    def __init__(self):
        self.setupUI()
        # self.createJoint()
        # self.createCtrl()


    def setupUI(self):
        winName = 'QuickRig_CAR'
        if pm.window(winName, exists=True):
            pm.deleteUI(winName)
        win = pm.window(winName, t='Car Rig', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=178)
        pm.separator(h=10)
        self.tempCircle = pm.textField(ed=True)
        pm.button(l="Create Joints", c=lambda x: self.createJoint())
        pm.button(l="Create Ctrls", c=lambda x: self.createCtrl())
        pm.button(l="Close", c=lambda x: pm.deleteUI(winName))
        pm.separator(h=10)
        pm.showWindow(win)


    def createJoint(self):
        branch = []
        for i in Coordinates.CAR.values():
            pm.select(cl=True)
            for name, pos in i.items():
                jnt = pm.joint(p=(0, 0, 0), n=name, rad=10)
                pm.move(jnt, pos)
            jntList = list(i.keys())
            branch.append(jntList[0])
            Tools().orientJnt(jntList)
        init = branch.pop(0)
        for j in branch:
                pm.parent(j, init)
        cuv = Tools().createCuv(300, y=True)
        self.tempCircle.setText(cuv)
        pm.parent(init, cuv)
        

    def createCtrl(self):
        cir = self.tempCircle.getText()
        pos = Coordinates.CTRL
        jnt = Tools().getHeadJnt(cir)
        ccList = []
        for i in jnt:
            if i == "jnt_root":
                cc_main = pm.circle(nr=(0, 1, 0), n="cc_main", r=300, ch=0)
                cc_main = cc_main[0]
                cc_sub = pm.curve(d=1, p=pos["car2"], n="cc_sub")
                ccList.append(cc_main)
                ccList.append(cc_sub)
            elif i == "jnt_body":
                cc_body = pm.curve(d=1, p=pos["car"], n="cc_body")
                ccList.append(cc_body)
                pm.matchTransform(cc_body, i, pos=True)
            else:
                ccName = i.replace("jnt_", "cc_")
                cc_etc = pm.circle(nr=(1, 0, 0), n=ccName, r=40, ch=0)
                ccList.append(cc_etc)
                pm.matchTransform(cc_etc, i, pos=True)


        # cirScale = pm.getAttr(f"{cir}.scale")
        
        # print(cc_body, cc_sub, cc_main)
        # pm.makeIdentity(cc_main, a=True, n=0)
        # pm.scale(cc_body, cirScale)
        # pm.scale(cc_sub, cirScale)
        # pm.delete(cir)
        



    


