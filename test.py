import re
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


