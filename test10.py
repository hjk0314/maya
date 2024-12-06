import pymel.core as pm
from general import *


def connectNodeToNode(multiplyDivideNode: str, \
                      startJoint: str, endJoint: str, directionList: list):
    """ Connect the outputX of the multiplyDivide to the scale of the joint. 
    If there are subjoints of the joint, it works as a recursive function.
     """
    for i in directionList:
        pm.connectAttr(f"{multiplyDivideNode}.outputX", f"{startJoint}.scale{i}", f=True)
    subJnt = pm.listRelatives(startJoint, c=True, type="joint")
    if subJnt and not (endJoint in subJnt):
        connectNodeToNode(multiplyDivideNode, subJnt[0], endJoint, directionList)
    else:
        return


def connectStretchNodeToJointScale(*args, **kwargs):
    """ As the length of the curve increases, 
    the length of the joint also increases.
    Select at least 3 or more.

    Usage: 
     - Select the start joint
     - Select the end joint
     - Select the curve

    Example: 
    >>> connectStretchNodeToJointScale()
    >>> connectStretchNodeToJointScale("startJnt", "endJnt", "curve1", x=True)
    >>> connectStretchNodeToJointScale(*["startJnt", "endJnt", "curve1"])
     """
    sel = args if args else pm.selected()
    if len(sel) < 3:
        return
    startJnt = sel[0]
    endJnt = sel[-2]
    directionList = []
    if kwargs:
        for i in kwargs.keys():
            if (i == "x" or i == "X") and kwargs[i]:
                directionList.append("X")
            if (i == "y" or i == "Y") and kwargs[i]:
                directionList.append("Y")
            if (i == "z" or i == "Z") and kwargs[i]:
                directionList.append("Z")
    else:
        directionList.append("X")
    cuv = pm.ls(sel, dag=True, type=["nurbsCurve"])[0]
    cuvInf = pm.shadingNode("curveInfo", au=True)
    pm.connectAttr(f"{cuv}.worldSpace[0]", f"{cuvInf}.inputCurve", f=True)
    cuvLen = pm.getAttr(f"{cuvInf}.arcLength")
    muldvd = pm.shadingNode("multiplyDivide", au=True)
    pm.setAttr(f"{muldvd}.operation", 2)
    pm.setAttr(f"{muldvd}.input2X", cuvLen)
    pm.connectAttr(f"{cuvInf}.arcLength", f"{muldvd}.input1X", f=True)
    connectNodeToNode(muldvd, startJnt, endJnt, directionList)


def createJointOnCurveSameSpacing():
    """ Create joints with Same Spacing on the curve. """
    joints = createJointOnMotionPath(10)
    newJoints = []
    for i in joints:
        pm.select(cl=True)
        jnt = pm.joint(p=(0,0,0))
        pm.matchTransform(jnt, i, pos=True, rot=True, scl=True)
        newJoints.append(jnt)
    parentHierarchically(*newJoints)
    pm.makeIdentity(newJoints, t=1, r=1, s=1, n=0, pn=1, jo=1, a=1)
    orientJoints(newJoints, "xyz", "yup")
    pm.delete(joints)


# ConnectStretchNodeToJointScale()
createRigGroups("shipShinanA")

