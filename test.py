import pymel.core as pm
import codecs


# 79 char line ================================================================
# 72 docstring or comments line ========================================


class AutoWheel():
    def __init__(self):
        # inputs
        self.obj = 'pony2_wheel_Ft_L'
        self.ccSize = 3
        # self.variables
        self.setupUI()
        self.fill()


    def setupUI(self):
        if pm.window('Auto_Wheel', exists=True):
            pm.deleteUI('Auto_Wheel')
        titleStr = 'Automatically_rotate_the_wheel'
        win = pm.window('Auto_Wheel', t=titleStr, s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=285)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=2, cw=[(1, 50), (2, 226)])
        pm.text('cuvCtrl :')
        self.ctrlName = pm.textField(ed=True, pht='Controller\'s name')
        pm.text('Radius :')
        self.wheelRadius = pm.textField(ed=True, pht='Size of wheel')
        pm.setParent("..", u=True)
        self.conditions = pm.textField(ed=False)
        pm.separator(h=10)
        pm.button(l='Create', c=lambda x: self.main())
        pm.separator(h=10)
        pm.showWindow(win)


    def fill(self):
        sel = pm.ls(sl=True)
        if not sel:
            self.conditions.setText('Nothing selected.')
        elif pm.ls(sel, dag=True, type=['nurbsCurve']):
            print('goto curve')
        elif pm.ls(sel, dag=True, type=['mesh']):
            objList = [i.name() for i in sel]
            objStr = ', '.join(objList)
            radList = self.getRadius(objList)
            radStr = [str(i) for i in radList]
            radStr = ', '.join(radStr)
            self.ctrlName.setText(objStr)
            self.wheelRadius.setText(radStr)
        else:
            self.conditions.setText('Unknown objects.')


    def getRadius(self, obj: list) -> list:
        result = []
        for i in obj:
            bbWheel = pm.xform(i, q=True, bb=True)
            xMin, yMin, zMin, xMax, yMax, zMax = bbWheel
            x = (xMax - xMin) / 2
            y = (yMax - yMin) / 2
            z = (zMax - zMin) / 2
            bbList = [x, y, z]
            bbList.sort(reverse=True)
            bb = bbList[0] # biggest
            bb = round(bb, 3) # bb: float
            result.append(bb)
        return result


    def main(self):
        a = self.ctrlName.getText()
        print(a)


    def createCC(self, obj: str, rad: float) -> None:
        cuv = 'cc_' + obj
        jnt = cuv + '_jnt'
        nullGrp = cuv + '_nullGrp'
        prevGrp = obj + '_prevGrp'
        orntGrp = obj + '_orntGrp'
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

        cuv = pm.circle(n=cuv, nr=(1,0,0), r=rad, ch=False)
        cuv = cuv[0]
        pm.addAttr(cuv, ln='Radius', at='double', dv=1)
        pm.setAttr(f'{cuv}.Radius', e=True, k=True)
        pm.addAttr(cuv, ln='AutoRoll', at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{cuv}.AutoRoll', e=True, k=True)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(cuv, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{cuv}.PrevPos{i}', e=True, k=True)
        pm.joint(n=jnt, p=(0,0,0))
        nullGrp = pm.group(n=nullGrp, em=True, p=cuv)
        # nextGrp = pm.group(n=nextGrp, em=True, w=True)
        prevGrp = pm.group(n=prevGrp, em=True, w=True)
        orntGrp = pm.group(n=orntGrp, em=True, p=prevGrp)
        # pm.connectAttr(f'{cuv}.translate', f'{nextGrp}.translate', f=True)
        pm.aimConstraint(cuv, prevGrp, mo=False)
        pm.orientConstraint(nullGrp, orntGrp, mo=False)
        pm.expression(s=exprStr, o='', ae=1, uc='all')


AutoWheel()