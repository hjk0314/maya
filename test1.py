
import pymel.core as pm


class AutoWheel_Rig:
    def __init__(self, arg=None):
        self.sel = self.checkParam(arg)
        self.wheelCtrl = self.createWheelCtrl()
        self.offsetGrp = self.createOffsetGrp()
        print(self.sel, self.wheelCtrl, self.offsetGrp)
        # self.main()


    def checkParam(self, obj):
        if obj and isinstance(obj, list):
            for j, k in enumerate(obj):
                if isinstance(k, pm.PyNode):
                    continue
                else:
                    obj[j] = pm.PyNode(k)
            result = obj
        else:
            result = pm.ls(sl=True)
        return result


    def createWheelCtrl(self):
        sizeUp = 1.2
        result = []
        for obj in self.sel:
            bb = pm.xform(obj, q=True, bb=True, ws=True)
            xMin, yMin, zMin, xMax, yMax, zMax = bb
            x = (xMax - xMin) / 2
            y = (yMax - yMin) / 2
            z = (zMax - zMin) / 2
            rad = max(x, y, z)
            rad = round(rad, 3) * sizeUp
            cuv = pm.circle(nr=(1, 0, 0), r=rad, n=f"cc_{obj}", ch=False)
            cuv = cuv[0]
            pm.matchTransform(cuv, obj, pos=True)
            result.append(cuv)
        return result


    def createOffsetGrp(self):
        result = []
        for i in self.wheelCtrl:
            off = pm.group(i, n=f"{i}_offset")
            pm.xform(off, os=True, piv=(0,0,0))
            result.append(off)
        return result


    def main(self):
        for ctrl, offset in self.ccDict.items():
            var = self.createVariables(ctrl, offset)
            self.createCtrlChannel(ctrl, offset)
            self.createCtrlGroup(offset, var)
            self.createExpression(offset, var)


    def createCtrlChannel(self, ctrl, offset):
        # Creates a Radius channel.
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        # Creates a AutoRoll channel.
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)
        # Creates a PrePos channel.
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, var):
        null, prev, orient, expr = var
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)


    def createExpression(self, offset, var):
        null, prev, orient, expr = var
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)
        pm.expression(s=expr, o='', ae=1, uc='all')


    def createCtrlLocator(self, ctrl):
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createVariables(self, ctrl, offset):
        loc = self.createCtrlLocator(ctrl)
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
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


ar = AutoWheel_Rig()
