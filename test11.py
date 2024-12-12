import pymel.core as pm
from general import *
from test10 import *


def shipShinanRopeSetting(ropeMesh, cuv, mainCtrl):
    pm.select(cl=True)
    pm.select(cuv)
    joints = createJointOnCurveSameSpacing(20)
    jnts = []
    for idx, jnt in enumerate(joints):
        new = "%s%d" % (cuv.replace("cuv_", "jnt_"), idx+1)
        pm.rename(jnt, new)
        jnts.append(new)
    startJnt = jnts[0]
    endJnt = jnts[-1]
    solver = "ikSplineSolver"
    ikName = cuv.replace("cuv_", "ikH_")
    pm.ikHandle(sj=startJnt, ee=endJnt, sol=solver, n=ikName, c=cuv, ccv=0)
    sjGrp = groupOwnPivot(startJnt)[0]
    pm.parent(sjGrp, "bindBones")
    pm.scaleConstraint("loc_moving", sjGrp, mo=True, w=1.0)
    pm.skinCluster(startJnt, ropeMesh, tsb=False, bm=0, sm=0, nw=1, wd=0, mi=3)


    clt1 = pm.cluster(f"{cuv}.cv[0:1]")[1]
    clt2 = pm.cluster(f"{cuv}.cv[2]")[1]
    clt3 = pm.cluster(f"{cuv}.cv[3]")[1]
    clt4 = pm.cluster(f"{cuv}.cv[4]")[1]
    clt5 = pm.cluster(f"{cuv}.cv[5:6]")[1]
    cltList = [clt1, clt2, clt3, clt4, clt5]
    temp = groupOwnPivot(*cltList)
    cltGrp = [temp[i] for i in range(0, len(temp), 2)]
    startJntPos = getPosition(startJnt)
    endJntPos = getPosition(endJnt)
    ccGrpList = []
    ccList = []
    ctrl = Controllers()
    replaceCC = cuv.replace("cuv_", "cc_")
    for i in range(5):
        cc = "%s%d" % (replaceCC, i+1)
        ccName = ctrl.createControllers(sphere=cc)[0]
        pm.scale(ccName, (5, 5, 5))
        pm.makeIdentity(ccName, a=1, t=1, r=1, s=1, n=0, pn=1)
        shp = ccName.getShape()
        pm.setAttr(f"{shp}.overrideEnabled", 1)
        pm.setAttr(f"{shp}.overrideColor", 21)
        ccGrp = groupOwnPivot(ccName, null=True)[0]
        ccGrpList.append(ccGrp)
        ccList.append(ccName)
    pm.group(ccGrpList, n=replaceCC+"_grp")
    linearCurve = pm.curve(d=1, p=[startJntPos, endJntPos], n="%sGuide" % cuv)
    pm.select(cl=True)
    pm.select(linearCurve)
    createJointOnMotionPath(5, *ccGrpList)
    [pm.scaleConstraint("loc_moving", i, mo=True, w=1.0) for i in ccGrpList]
    for j, k in zip(cltGrp, ccList):
        pm.parent(j, k)
        pm.setAttr(f"{j}.visibility", 0)
    clt6 = pm.cluster(f"{linearCurve}.cv[0]")[1]
    clt6Grp = groupOwnPivot(clt6)[0]
    pm.setAttr(f"{clt6Grp}.visibility", 0)
    pm.parent(clt6Grp, mainCtrl)
    clt7 = pm.cluster(f"{linearCurve}.cv[1]")[1]
    clt7Grp = groupOwnPivot(clt7)[0]
    pm.parent(clt7Grp, "loc_moving")


    mulDvd0 = connectStretchNodeToJointScale(startJnt, endJnt, cuv)
    mulDvd1 = pm.shadingNode("multiplyDivide", au=True)
    mulDvd2 = pm.shadingNode("multiplyDivide", au=True)
    pm.connectAttr(f"{sjGrp}.scale", f"{mulDvd1}.input2", f=True)
    pm.setAttr(f"{mulDvd1}.operation", 2)
    [pm.setAttr(f"{mulDvd1}.input1{i}", 1) for i in ["X", "Y", "Z"]]
    pm.connectAttr(f"{mulDvd1}.output", f"{mulDvd2}.input2", f=True)
    pm.connectAttr(f"{mulDvd0}.outputX", f"{mulDvd2}.input1X", f=True)
    for j in jnts:
        pm.connectAttr(f"{mulDvd2}.outputX", f"{j}.scaleX", f=True)


# mesh = [f"mainMast_rope_{i}" for i in range(1, 9)]
# curves = [f"cuv_mainMastSub{i}_copied" for i in range(1, 9)]
# mainCtrl = "cc_mainMastMain"
mesh = [f"mizzen_rope_{i}" for i in range(1, 5)]
curves = [f"cuv_mizzenSub{i}_copied" for i in range(1, 5)]
mainCtrl = "cc_mizzenMain"


for obj, cuv in zip(mesh, curves):
    shipShinanRopeSetting(obj, cuv, mainCtrl)