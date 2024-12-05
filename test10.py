import pymel.core as pm
from general import *


def connectNodeToNode(srcNode, joint, endJnt, directionList):
    for i in directionList:
        pm.connectAttr(f"{srcNode}.outputX", f"{joint}.scale{i}", f=True)
    subJnt = pm.listRelatives(joint, c=True, type="joint")
    if subJnt and not (endJnt in subJnt):
        connectNodeToNode(srcNode, subJnt[0], endJnt, directionList)
    else:
        return


def createJointOnMotionPath(numberOfJoints: int) -> None:
    """ Create a number of joints and 
    apply a motionPath on the curve.
     """
    mod = 1/(numberOfJoints-1) if numberOfJoints > 1 else 0
    sel = pm.selected()
    if sel:
        cuv = sel[0]
    else:
        return
    result = []
    for i in range(numberOfJoints):
        pm.select(cl=True)
        jnt = pm.joint(p=(0,0,0))
        uValue = i * mod
        motionPath = pm.pathAnimation(jnt, \
            c=cuv, 
            fractionMode=True, 
            follow=True, 
            followAxis='x', 
            upAxis='y', 
            worldUpType='vector', 
            worldUpVector=(0,1,0)
            )
        pm.cutKey(motionPath, cl=True, at='u')
        pm.setAttr(f"{motionPath}.uValue", uValue)
        result.append(jnt)
    return result


def ConnectStretchNodeToJointScale(*args, **kwargs):
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


def createJointOnCurveSameIntervals():
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


