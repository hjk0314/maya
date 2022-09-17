import maya.OpenMaya as om
import pymel.core as pm


class AutoWheel():
    def __init__(self):
        self.main()
    

    def main(self):
        sel = pm.ls(sl=True)
        if not sel:
            om.MGlobal.displayError('Nothing selected.')
        else:
            for i in sel:
                rad = self.createRad(i)
                var = self.createVar(rad)
                self.createRig(i, var, rad)
    

    # Return obj's radius.
    def createRad(self, obj: str) -> float:
        # bb: bounding box
        bbObj = pm.xform(obj, q=True, bb=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bbObj
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        bbList = [x, y, z]
        bbList.sort(reverse=True) # biggest
        bb = bbList[0] # 0.12345678
        result = round(bb, 3) # 0.123
        return result


    # Create variables.
    def createVar(self, rad: float) -> tuple:
        rad *= 1.1
        cuv = pm.circle(nr=(1,0,0), r=rad, ch=False)
        cuv = cuv[0]
        jnt = cuv + '_jnt'
        null = cuv + '_null_grp'
        prev = cuv + '_prev_grp'
        orient = cuv + '_orient_Grp'
        # expression1 ==================================================
        expr1 = f'float $R = {cuv}.Radius;'
        expr1 += f'float $A = {cuv}.AutoRoll;'
        expr1 += f'float $J = {jnt}.rotateX;'
        expr1 += f'float $C = 2 * 3.141 * $R;' # 2*pi*r
        expr1 += f'float $O = {orient}.rotateY;'
        expr1 += f'float $S = 1;' # Connect the global scale.
        expr1 += f'float $pX = {cuv}.PrevPosX;'
        expr1 += f'float $pY = {cuv}.PrevPosY;'
        expr1 += f'float $pZ = {cuv}.PrevPosZ;'
        expr1 += f'{prev}.translateX = $pX;'
        expr1 += f'{prev}.translateY = $pY;'
        expr1 += f'{prev}.translateZ = $pZ;'
        expr1 += f'float $nX = {cuv}.translateX;'
        expr1 += f'float $nY = {cuv}.translateY;'
        expr1 += f'float $nZ = {cuv}.translateZ;'
        # expression2: Distance between two points.
        expr2 = 'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;'
        # expression3: Insert value into jonit rotation.
        expr3 = f'{jnt}.rotateX = $J' # Original rotation value.
        expr3 += ' + ($D/$C) * 360' # Proportional: (d / 2*pi*r) * 360
        expr3 += ' * $A' # Auto roll switch.
        expr3 += ' * 1' # Create other switches.
        expr3 += ' * sin(deg_to_rad($O))' # When the wheel turns.
        expr3 += ' / $S;' # Resizing the global scale.
        # expression4
        expr4 = f'{cuv}.PrevPosX = $nX;'
        expr4 += f'{cuv}.PrevPosY = $nY;'
        expr4 += f'{cuv}.PrevPosZ = $nZ;'
        # expression Final =============================================
        exprFinal = expr1 + expr2 + expr3 + expr4
        # Result
        result = (cuv, jnt, null, prev, orient, exprFinal)
        return result


    # Construct a rig inside maya.
    def createRig(self, obj: str, var: tuple, rad: float) -> None:
        # variables
        cuv, jnt, null, prev, orient, expr = var
        # channel to cuv
        pm.addAttr(cuv, ln='Radius', at='double', dv=1)
        pm.setAttr(f'{cuv}.Radius', e=True, k=True)
        pm.setAttr(f'{cuv}.Radius', rad)
        pm.addAttr(cuv, ln='AutoRoll', at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{cuv}.AutoRoll', e=True, k=True)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(cuv, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{cuv}.PrevPos{i}', e=True, k=True)
        # create joint inside cuv
        pm.joint(n=jnt, p=(0,0,0))
        # create groups
        pm.group(n=null, em=True, p=cuv)
        pm.group(n=prev, em=True, w=True)
        pm.group(n=orient, em=True, p=prev)
        grp = pm.group(cuv, prev)
        pm.matchTransform(grp, obj, pos=True)
        # create constraints
        pm.aimConstraint(cuv, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)
        pm.expression(s=expr, o='', ae=1, uc='all')