import pymel.core as pm


class AutoWheel():
    def __init__(self):
        self.setupUI()


    # maya UI
    def setupUI(self):
        if pm.window('Auto_Wheel', exists=True):
            pm.deleteUI('Auto_Wheel')
        # title
        ttl = 'Automatically_rotate_the_wheel'
        win = pm.window('Auto_Wheel', t=ttl, s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=295)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=2, cw=[(1, 60), (2, 226)])
        pm.text('wheel_0 :  ', al='right')
        self.wheelField = pm.textField(ed=False, pht='Nothing selected')
        pm.text('ctrl_0 :  ', al='right')
        self.ctrlField = pm.textField(ed=True)
        pm.setParent("..", u=True)
        pm.separator(h=10)
        self.conditions = pm.textField(ed=False)
        pm.separator(h=10)
        pm.button(l='Fill the blanks', c=lambda x: self.fill())
        # create button
        self.crtBtn = pm.button(l='Create', en=False, c=lambda x: self.main())
        pm.separator(h=10)
        pm.showWindow(win)


    # fill the blanks
    def fill(self):
        sel = pm.ls(sl=True)
        if not sel:
            obj = ''
            cuv = ''
            msg = 'Nothing Selected.'
            enb = False
            bgColor = (0.839, 0.422, 0.176)
        else:
            obj = sel[0]
            cuv = 'cc_' + obj
            msg = 'Ready'
            enb = True
            bgColor = (0.269, 0.509, 0.617)
        # Some fields are changed.
        self.wheelField.setText(obj)
        self.ctrlField.setText(cuv)
        self.conditions.setText(msg)
        self.conditions.setBackgroundColor(bgColor)
        self.crtBtn.setEnable(enb)


    # check the field.
    def check(self) -> dict:
        result = {}
        wheel = self.wheelField.getText()
        curve = self.ctrlField.getText()
        colon = ':' in curve
        dup = '|' in curve
        rad = self.getRadius(wheel)
        bgColor = (0.839, 0.422, 0.176) # This is red
        if not wheel: # is or not
            msg = 'Nothing selected.'
        elif not curve: # is or not
            msg = 'is empty.'
        elif not rad: # zero or not
            msg = 'The radius must be non-zero.'
        elif colon: # is colon included or not
            msg = 'Contains a colon.'
        elif dup: # is duplicated or not
            msg = 'check the duplicate names.'
        else:
            msg = 'Successfully done.'
            bgColor = (0.269, 0.509, 0.617) # This is blue.
            result[curve] = rad
        self.conditions.setText(msg)
        self.conditions.setBackgroundColor(bgColor)
        return result


    # Return wheel's radius.
    def getRadius(self, obj: str) -> float:
        # bb: bounding box
        bbWheel = pm.xform(obj, q=True, bb=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bbWheel
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        bbList = [x, y, z]
        bbList.sort(reverse=True)
        bb = bbList[0] # biggest: 0.12345678
        result = round(bb, 3) # 0.123
        return result


    # Create curve Controllers, joints, and groups.
    def createCC(self, cc: str, rad: float) -> None:
        # Create in maya
        cuv = pm.circle(n=cc, nr=(1,0,0), r=rad, ch=False)[0]
        jnt, nullGrp, prevGrp, orntGrp, exprStr = self.createVar(cuv)
        pm.addAttr(cuv, ln='Radius', at='double', dv=1)
        pm.setAttr(f'{cuv}.Radius', e=True, k=True)
        pm.setAttr(f'{cuv}.Radius', rad)
        pm.addAttr(cuv, ln='AutoRoll', at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{cuv}.AutoRoll', e=True, k=True)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(cuv, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{cuv}.PrevPos{i}', e=True, k=True)
        pm.joint(n=jnt, p=(0,0,0))
        pm.group(n=nullGrp, em=True, p=cuv)
        pm.group(n=prevGrp, em=True, w=True)
        pm.group(n=orntGrp, em=True, p=prevGrp)
        pm.aimConstraint(cuv, prevGrp, mo=False)
        pm.orientConstraint(nullGrp, orntGrp, mo=False)
        pm.expression(s=exprStr, o='', ae=1, uc='all')


    # Return variables.
    def createVar(self, cuv: str) -> tuple:
        jnt = cuv + '_jnt'
        nullGrp = cuv + '_nullGrp'
        prevGrp = cuv + '_prevGrp'
        orntGrp = cuv + '_orntGrp'
        # expression1 ==================================================
        expr1 = f'float $R = {cuv}.Radius;'
        expr1 += f'float $A = {cuv}.AutoRoll;'
        expr1 += f'float $J = {jnt}.rotateX;'
        expr1 += f'float $C = 2 * 3.141 * $R;' # 2*pi*r
        expr1 += f'float $O = {orntGrp}.rotateY;'
        expr1 += f'float $S = 1;' # Connect the global scale.
        expr1 += f'float $pX = {cuv}.PrevPosX;'
        expr1 += f'float $pY = {cuv}.PrevPosY;'
        expr1 += f'float $pZ = {cuv}.PrevPosZ;'
        expr1 += f'{prevGrp}.translateX = $pX;'
        expr1 += f'{prevGrp}.translateY = $pY;'
        expr1 += f'{prevGrp}.translateZ = $pZ;'
        expr1 += f'float $nX = {cuv}.translateX;'
        expr1 += f'float $nY = {cuv}.translateY;'
        expr1 += f'float $nZ = {cuv}.translateZ;'
        # expression2: Distance between two points.
        expr2 = 'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{jnt}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Switch
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += ' / $S;' # Resizing the global scale.
        # expression4
        expr4 = f'{cuv}.PrevPosX = $nX;'
        expr4 += f'{cuv}.PrevPosY = $nY;'
        expr4 += f'{cuv}.PrevPosZ = $nZ;'
        # Final expression string
        exprStr = expr1 + expr2 + expr3 + expr4
        # expression end ===============================================
        result = (jnt, nullGrp, prevGrp, orntGrp, exprStr)
        return result


    def main(self):
        dic = self.check()
        for i in dic:
            self.createCC(i, dic[i])


# 79 char line ================================================================
# 72 docstring or comments line ========================================


AutoWheel()