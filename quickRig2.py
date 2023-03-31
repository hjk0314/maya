
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


class Tools:
    def __init__(self):
        pass


    def orientJnt(self, jnt: list) -> None:
        init = jnt[0]
        last = jnt[-1]
        pm.makeIdentity(jnt, a=True, jo=True, n=0)
        pm.joint(init, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(last, e=True, oj='none', ch=True, zso=True)


    def createCuv(self, name: str, size: float, **kwargs) -> str:
        normal = {
            "x": (1, 0, 0), 
            "y": (0, 1, 0), 
            "z": (0, 0, 1), 
        }
        if not kwargs:
            axis = (0, 1, 0)
        else:
            for k, v in kwargs.items():
                if not k in normal.keys():
                    axis = (0, 1, 0)
                    continue
                elif not v:
                    axis = (0, 1, 0)
                    continue
                else:
                    axis = normal[k]
        cuv = pm.circle(nr=axis, n=name, ch=False, r=size)[0]
        # pm.scale(cuv, [size, size, size])
        # pm.makeIdentity(cuv, a=True, n=0)
        return cuv


    def getHeadJntName(self, *arg):
        sel = pm.ls(arg, dag=True, type=['transform'])
        jnt = []
        for i in sel:
            typ = pm.objectType(i)
            if typ != 'joint' or i.endswith("_end"):
                continue
            else:
                jnt.append(i)
        return jnt


    def groupingEmpty(self, *arg) -> list:
        """ Create an empty group and match the pivot with the selector. """
        sel = arg if arg else pm.ls(sl=True)
        grpName = []
        for i in sel:
            grp = pm.group(em=True, n = i + "_grp")
            grpName.append(grp)
            pm.matchTransform(grp, i, pos=True, rot=True)
            try:
                mom = i.getParent()
                pm.parent(grp, mom)
            except:
                pass
            pm.parent(i, grp)
        return grpName


    def groupingOffset(self, *arg):
        """ Grouping itself and named offset """
        sel = arg if arg else pm.ls(sl=True)
        result = []
        for i in sel:
            grp = pm.group(i, n="%s_offset" % i)
            pm.xform(grp, os=True, piv=(0,0,0))
            result.append(grp)
        return result
    

    def grouping(self):
        nameList = ["rig", "MODEL", "controller", ]#"skeleton", "extraNode"]
        for i in nameList:
            pm.group(em=True, n=i)
        pm.parent(nameList[2:], "rig")
        return nameList[2]


    def createRadius(self, *arg):
        attr = "Radius"
        ctrl = arg[0]
        pm.addAttr(ctrl, ln=attr, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attr}', e=True, k=True)


    def createAutoRoll(self, *arg):
        attr = 'AutoRoll'
        ctrl = arg[0]
        pm.addAttr(ctrl, ln=attr, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attr}', e=True, k=True)


    # This is Main function.
    def colors(self, obj, **kwargs):
        sel = pm.ls(obj)
        colors = {
            "blue": 6, 
            "blue2": 18, 
            "pink": 9, 
            "red": 13, 
            "red2": 21, 
            "green": 14, 
            "green2": 23, 
            "yellow": 17, 
        }
        idxs = [colors[i] for i in kwargs if kwargs[i]]
        enb = 1 if idxs else 0
        idx = idxs[0] if idxs else 0
        for i in sel:
            shp = i.getShape()
            pm.setAttr(f"{shp}.overrideEnabled", enb)
            pm.setAttr(f"{shp}.overrideColor", idx)


class AutoWheel:
    def __init__(self, *arg: list):
        sel = arg if arg else pm.ls(sl=True)
        for i in sel:
            self.main(i)


    def main(self, ctrl: str):
        offset = ctrl.getParent()
        tmp = self.createVariables(ctrl, offset)
        self.createCtrlChannel(offset)
        self.createCtrlGroup(offset, tmp)
        self.createExpression(offset, tmp)


    def createCtrlChannel(self, obj: str) -> None:
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(obj, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{obj}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset: str, tmp: list):
        null, prev, orient, expr = tmp
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        pm.group(n=orient, em=True, p=prev)


    def createExpression(self, offset: str, tmp: list):
        null, prev, orient, expr = tmp
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)
        pm.expression(s=expr, o='', ae=1, uc='all')


    def createCtrlLocator(self, ctrl):
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createVariables(self, ctrl: str, offset: str) -> list:
        loc = self.createCtrlLocator(ctrl)
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_Grp'
        br = '\n'
        # expression1 ==================================================
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}' # 2*pi*r
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}' # Connect the global scale.
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2: Distance between two points.
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{loc}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Auto roll switch.
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += f' / $S;{br*2}' # Resizing the global scale.
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # expression Final =============================================
        expr = expr1 + expr2 + expr3 + expr4
        # Result
        result = [null, prev, orient, expr]
        return result


class QuickRig_CAR:
    def __init__(self):
        self.setupUI()


    def setupUI(self):
        winName = 'QuickRig_CAR'
        if pm.window(winName, exists=True):
            pm.deleteUI(winName)
        win = pm.window(winName, t='Car Rig', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=178)
        pm.separator(h=10)
        self.txt1 = pm.textField(ed=True, en=0)
        self.txt2 = pm.textField(ed=True, pht="wheel's Radius")
        pm.button(l="Create Joints", c=lambda x: self.createJoint())
        pm.button(l="Create Ctrls", c=lambda x: self.createCtrl())
        pm.button(l="Get Radius", c=lambda x: self.getRadius())
        pm.button(l="Close", c=lambda x: pm.deleteUI(winName))
        pm.separator(h=10)
        pm.showWindow(win)


    def createJoint(self):
        carJnt = Coordinates.CAR.values()
        branch = []
        for i in carJnt:
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
        cuv = Tools().createCuv('tempCircle', 300, y=True)
        self.txt1.setText(cuv)
        pm.parent(init, cuv)
        

    # Return obj's radius.
    def getRadius(self, *arg):
        sel = arg if arg else pm.ls(sl=True)
        result = {}
        radius = []
        for obj in sel:
            bbObj = pm.xform(obj, q=True, bb=True)
            xMin, yMin, zMin, xMax, yMax, zMax = bbObj
            x = (xMax - xMin) / 2
            y = (yMax - yMin) / 2
            z = (zMax - zMin) / 2
            bb = max([x, y, z])
            bb = round(bb, 3)
            result[obj] = bb
            # print(f"{obj} -> {bb}")
        for i, rad in result.items():
            obj = i.split("_")
            L = "_L" if "L" in obj else ''
            R = "_R" if "R" in obj else ''
            Ft = "_Ft" if "Ft" in obj else ''
            Bk = "_Bk" if "Bk" in obj else ''
            tmp = L + R + Ft + Bk
            try:
                pm.setAttr(f"cc_wheel{tmp}.Radius", rad)
            except:
                pass
            radius.append(rad)
        txt = [str(i) for i in radius]
        self.txt2.setText(str(' '.join(txt)))


    def createCtrl(self):
        cir = self.txt1.getText()
        pos = Coordinates.CTRL
        jnt = Tools().getHeadJntName(cir)
        controllerGrp = Tools().grouping()
        wheelList = []
        for i in jnt:
            cc = i.replace("jnt_", "cc_")
            typ = i.split("_")[1]
            if typ == "root":
                cc_main = pm.circle(nr=(0, 1, 0), n="cc_main", r=300, ch=0)[0]
                pm.matchTransform(cc_main, cir, scl=True)
                pm.makeIdentity(cc_main, a=True, t=0, r=0, s=1, n=0, pn=1)
                cc_sub = pm.curve(d=1, p=pos["car2"], n="cc_sub")
                pm.matchTransform(cc_sub, cir, scl=True)
                pm.makeIdentity(cc_sub, a=True, t=0, r=0, s=1, n=0, pn=1)
                mainGrp, subGrp = Tools().groupingEmpty(cc_main, cc_sub)
                pm.parent(subGrp, cc_main)
                pm.parent(mainGrp, controllerGrp)
                Tools().colors(cc_main, yellow=True)
                Tools().colors(cc_sub, pink=True)
            elif typ == "body":
                cc_body = pm.curve(d=1, p=pos["car"], n="cc_body")
                pm.matchTransform(cc_body, i, pos=True, scl=True)
                pm.makeIdentity(cc_body, a=True, t=0, r=0, s=1, n=0, pn=1)
                bodyGrp = Tools().groupingEmpty(cc_body)
                pm.parent(bodyGrp, "cc_sub")
                Tools().colors(cc_body, yellow=True)
            elif typ == "wheel":
                ccWheel = pm.circle(nr=(1, 0, 0), n=cc, r=40, ch=0)[0]
                Tools().createRadius(ccWheel)
                Tools().createAutoRoll(ccWheel)
                pm.matchTransform(ccWheel, i, pos=True, scl=True)
                pm.makeIdentity(ccWheel, a=True, t=0, r=0, s=1, n=0, pn=1)
                wheelGrp = Tools().groupingEmpty(ccWheel)
                Tools().groupingOffset(ccWheel)
                pm.parent(wheelGrp, controllerGrp)
                wheelList.append(ccWheel)
            else:
                continue
        AutoWheel(wheelList)
        # self.constraint(wheelList)
        pm.delete(cir)


    def constraint(self, wheelList: list):
        parent = "cc_sub"
        for i in wheelList:
            child = i.getParent()
            pm.parentConstraint(parent, child, mo=True, w=1)
            pm.scaleConstraint(parent, child, mo=True, w=1)


QuickRig_CAR()



