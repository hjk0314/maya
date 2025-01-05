import pymel.core as pm
from general import *


def getSubJoint(startJnt: str, endJoint: str) -> list:
    """ Get the sub joints from the start joint to the end joint. 
    The end joint is not included.
     """
    if not isinstance(startJnt, pm.PyNode):
        startJnt = pm.PyNode(startJnt)
    result = [startJnt]
    subJnt = pm.listRelatives(startJnt, c=True, type="joint")
    if subJnt and not (endJoint in subJnt):
        result += getSubJoint(subJnt[0], endJoint)
        # for i in subJnt:
        #     result += getSubJoint(i, endJoint)
    return result


def createJointScaleIncrease(*args, **kwargs) -> str:
    """ As the length of the curve increases, 
    the length of the joint also increases.
    Select at least 3 or more.

    Usage: 
     - Select the start joint
     - Select the end joint
     - Select the curve

    Example: 
    >>> createJointScaleIncrease()
    >>> createJointScaleIncrease("startJnt", "endJnt", "curve1", x=True)
    >>> createJointScaleIncrease(x=True, y=True)
    >>> createJointScaleIncrease(*["startJnt", "endJnt", "curve1"])
     """
    sel = args if args else pm.selected()
    if len(sel) < 3:
        return
    startJnt = sel[0]
    endJnt = sel[-2]
    cuv = pm.ls(sel, dag=True, type=["nurbsCurve"])
    if cuv:
        cuv = cuv[0]
    else:
        pm.warning("There is no Curve.")
        return
    scales = []
    if kwargs:
        for i in kwargs.keys():
            if (i == "x" or i == "X") and kwargs[i]:
                scales.append("X")
            if (i == "y" or i == "Y") and kwargs[i]:
                scales.append("Y")
            if (i == "z" or i == "Z") and kwargs[i]:
                scales.append("Z")
    else:
        scales.append("X")
    cuvInf = pm.shadingNode("curveInfo", au=True)
    pm.connectAttr(f"{cuv}.worldSpace[0]", f"{cuvInf}.inputCurve", f=True)
    cuvLen = pm.getAttr(f"{cuvInf}.arcLength")
    muldvd = pm.shadingNode("multiplyDivide", au=True)
    pm.setAttr(f"{muldvd}.operation", 2)
    pm.setAttr(f"{muldvd}.input2X", cuvLen)
    pm.connectAttr(f"{cuvInf}.arcLength", f"{muldvd}.input1X", f=True)
    joints = getSubJoint(startJnt, endJnt)
    for jnt in joints:
        for scl in scales:
            pm.connectAttr(f"{muldvd}.outputX", f"{jnt}.scale{scl}", f=True)
    return muldvd


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
    

