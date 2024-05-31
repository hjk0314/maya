import pymel.core as pm
from general import *


class temp:
    def createWheelCtrl(self, obj, ccName, parentsGroup="") -> str:
        cc = [
            f"{ccName}_upDownMain", 
            f"{ccName}_upDownSub", 
            f"{ccName}_Main", 
            f"{ccName}_Sub"
        ]
        ccGrp = []
        sizeRatio = [14, 18, 9, 11]
        ctrl = Controllers()
        rad = getBoundingBoxSize(obj)
        for ccName, sr in zip(cc[:2], sizeRatio[:2]):
            cuv = ctrl.createControllers(square=ccName)[0]
            pm.scale(cuv, (rad/(sr*2), rad/sr, rad/sr))
            pm.matchTransform(cuv, obj, pos=True)
            pm.setAttr(f"{cuv}.translateY", 0)
        for ccName, sr in zip(cc[2:], sizeRatio[2:]):
            cuv = ctrl.createControllers(circle=ccName)[0]
            pm.scale(cuv, (rad/sr, rad/sr, rad/sr))
            pm.rotate(cuv, (0, 0, 90))
            pm.matchTransform(cuv, obj, pos=True)
        for i in cc:
            pm.makeIdentity(i, a=1, t=0, r=1, s=1, n=0, pn=1)
            cuvGrp = groupingWithOwnPivot(i)[0]
            ccGrp.append(cuvGrp)
        for parents, child in zip(cc[:3], ccGrp[1:]):
            parentHierarchically(parents, child)
        ccSub = cc[-1]
        ccUpDownMainGrp = ccGrp[0]
        if pm.objExists(parentsGroup):
            parentHierarchically(parentsGroup, ccUpDownMainGrp)
        # Create wheel controllers channel.
        attrRad = "Radius"
        pm.addAttr(ccSub, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ccSub}.{attrRad}', e=True, k=True)
        attrAuto = 'AutoRoll'
        pm.addAttr(ccSub, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ccSub}.{attrAuto}', e=True, k=True)
        pm.setAttr(f"{ccSub}.Radius", rad)
        return ccSub


