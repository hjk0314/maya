import pymel.core as pm


# 79 char line ================================================================
# 72 docstring or comments line ========================================


class AutoWheel():
    def __init__(self):
        self.setupUI()


    def setupUI(self):
        if pm.window('Auto_Wheel', exists=True):
            pm.deleteUI('Auto_Wheel')
        ttl = 'Automatically_rotate_the_wheel'
        win = pm.window('Auto_Wheel', t=ttl, s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=295)
        self.dic = {}
        for i in range(4):
            wheelStr = 'wheel_%d' % i
            ctrlStr = 'ctrl_%d' % i
            pm.separator(h=10)
            pm.rowColumnLayout(nc=2, cw=[(1, 60), (2, 226)])
            pm.text(f'{wheelStr} :  ', al='right')
            wheelField = pm.textField(ed=False, pht='wheel\'s name')
            pm.text(f'{ctrlStr} :  ', al='right')
            ctrlField = pm.textField(ed=True, pht='controller\'s name')
            pm.setParent("..", u=True)
            self.dic[wheelField] = ctrlField
        pm.separator(h=10)
        self.conditions = pm.textField(ed=False)
        pm.separator(h=10)
        pm.button(l='Fill the blanks', c=lambda x: self.fill())
        pm.button(l='Create', c=lambda x: self.main())
        pm.separator(h=10)
        pm.showWindow(win)


    def fill(self):
        sel = pm.ls(sl=True)
        num = len(sel)
        for j, k in enumerate(self.dic):
            if j < num:
                obj = sel[j]
                k.setText(obj)
                self.dic[k].setText(f'cc_{obj}')
            else:
                break


    def main(self):
        # cc: Curve Controller
        ccDic = self.check()
        print(ccDic)
        # for i in ccDic:
            # ccDic = {cuvName: wheelRadius, ...}
            # self.createCC(i, ccDic[i])


    def check(self):
        result = {}
        for i in self.dic:
            wheel = i.getText()
            curve = self.dic[i].getText()
            colon = ':' in curve
            dup = '|' in curve
            rad = self.getRadius(wheel)
            if not wheel: # is or not
                msg = 'Nothing selected.'
                bgColor = (0.839, 0.422, 0.176)
                break
            elif not curve: # is or not
                msg = 'The Curve Controller Name field is empty.'
                bgColor = (0.839, 0.422, 0.176)
                break
            elif not rad: # zero or not
                msg = 'The radius must be non-zero.'
                bgColor = (0.839, 0.422, 0.176)
                break
            elif colon: # is colon included or not
                msg = 'The controllers name contains a colon.'
                bgColor = (0.839, 0.422, 0.176)
                break
            elif dup: # is duplicated or not
                msg = 'You should check for duplicate names.'
                bgColor = (0.839, 0.422, 0.176)
                break
            else:
                msg = 'Successfully added it to the dictionary.'
                bgColor = (0.269, 0.509, 0.617)
                result[curve] = rad
        self.conditions.setText(msg)
        self.conditions.setBackgroundColor(bgColor)
        return result


    def getRadius(self, obj: str) -> float:
        bbWheel = pm.xform(obj, q=True, bb=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bbWheel
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        bbList = [x, y, z]
        bbList.sort(reverse=True)
        bb = bbList[0] # biggest
        result = round(bb, 3)
        return result


    # Create curve Controllers, joints, and groups.
    def createCC(self, cuv: str, rad: float) -> None:
        # Variables
        jnt, nullGrp, prevGrp, orntGrp, exprStr = self.createVar(cuv)
        # Create in maya
        pm.circle(n=cuv, nr=(1,0,0), r=rad, ch=False)
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


AutoWheel()