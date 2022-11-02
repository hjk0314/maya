import re
from hjk import grpEmpty
import maya.OpenMaya as om
import pymel.core as pm


# rename function used in maya
def rename(txt: str) -> None:
    """ Rename by incrementing the last digit in the string. """
    # txt -> 'testName23_17_grp'
    # txtList -> ['testName', '23', '_', '17', '_grp']
    txtList = re.split(r'([^0-9]+)([0-9]*)', txt)
    txtList = [i for i in txtList if i]
    # txtDict -> {1: 23, 3: 17}
    txtDict = {i: int(n) for i, n in enumerate(txtList) if n.isdigit()}
    # sel: The selected object.
    sel = pm.ls(sl=True)
    if len(txtDict):
        # idx -> 3
        idx = max(txtDict)
        # num -> 17
        num = txtDict[max(txtDict)]
        for j, k in enumerate(sel):
            txtList[idx] = str(num + j)
            # new -> 'testName23_17_grp'
            new = ''.join(txtList)
            pm.rename(k, new)
    else:
        for j, k in enumerate(sel):
            new = ''.join(txtList) + str(j)
            pm.rename(k, new)


# Get the position of the poleVector in maya.
def pvp():
    '''Create temporary joints, and use aimConstraint's worldUpObject 
    to find the position of the poleVector.'''
    sel = pm.ls(sl=True)
    if len(sel) != 3:
        om.MGlobal.displayError('Select three objects.')
    else:
        midJnt = sel[1]
        endJnt = sel[2]
        # List the coordinates of the joint
        points = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
        p1, p2, p3 = [i for i in points]
        # It's good to clear the selection before creating the joint.
        pm.select(cl=True)
        # Temporarily create two joints.
        temp1 = pm.joint(p=p1)
        temp2 = pm.joint(p=p3)
        # Use Maya's <Orient joint> menu.
        pm.joint(temp1, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(temp2, e=True, oj='none', ch=True, zso=True)
        # o: offset, wut: worldUpType, wuo: worldUpObject
        pm.aimConstraint(endJnt, temp1, o=(0,0,90), wut='object', wuo=midJnt)
        # cn: constraint
        pm.delete(temp1, cn=True)
        # Position to the middle joint.
        pm.matchTransform(temp1, midJnt, pos=True)
        # Create a locator and 
        loc = pm.spaceLocator()
        # place it at the poleVector position.
        pm.matchTransform(loc, temp2, pos=True, rot=True)
        # Delete temporarily used joints.
        pm.delete(temp1)


# 79 char line ================================================================
# 72 docstring or comments line ========================================


class A2B:
    def __init__(self):
        self.main()


    # Number of Object's cv.
    def numberOfCV(self, obj: str) -> int:
        '''Number of object's cv'''
        cv = f'{obj}.cv[0:]'
        pm.select(cv)
        cvSel = pm.ls(sl=True, fl=True)
        cvNum = len(cvSel)
        result = cvNum
        pm.select(cl=True)
        return result

        
    # Match the point to point.
    def matchShape(self, obj: list) -> list:
        '''Change the shape of the curve controller from A to B'''
        A_list = obj[0:-1]
        B = obj[-1] # The last selection is Base.
        numB = self.numberOfCV(B) # number of B.cv
        failed = []
        for A in A_list:
            numA = self.numberOfCV(A)
            if numA == numB > 0:
                for k in range(numA):
                    cvA = f'{A}.cv[{k}]'
                    cvB = f'{B}.cv[{k}]'
                    p1, p2, p3 = pm.pointPosition(cvB)
                    pm.move(p1, p2, p3, cvA, a=True)
            else:
                failed.append(A)
        return failed


    def main(self):
        '''Select only "nurbsCurve" and match the shape.'''
        sel = pm.ls(sl=True, dag=True, type=['nurbsCurve'])
        # Select at least 2.
        if len(sel) < 2:
            om.MGlobal.displayError('Select two or more "nurbsCurves".')
        else:
            result = self.matchShape(sel)
            failed = 'Check this objects : %s' % result
            success = 'Successfully done.'
            message = failed if result else success
            om.MGlobal.displayInfo(message)


# sel = pm.ls(sl=True, fl=True)
# jnt = sel[0]
# org = sel[1]
# new = pm.circle(c=(0,0,0), nr=(1,0,0), ch=False)
# pm.matchTransform(new, jnt, pos=True, rot=True)
# pm.select(cl=True)
# pm.select(new)
# pm.select(org, tgl=True)
A2B()
# pm.select(new)
# grpEmpty()
