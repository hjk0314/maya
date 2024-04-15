import re
import pymel.core as pm
import general as hjk


class RowData:
    def __init__(self):
        self.allJnt = [
            'RL_BoneRoot', 
            'CC_Base_Hip', 
            'CC_Base_Pelvis', 
            'CC_Base_L_Thigh', 
            'CC_Base_L_Calf', 
            'CC_Base_L_Foot', 
            'CC_Base_L_ToeBaseShareBone', 
            'CC_Base_L_ToeBase', 
            'CC_Base_L_PinkyToe1', 
            'CC_Base_L_RingToe1', 
            'CC_Base_L_MidToe1', 
            'CC_Base_L_IndexToe1', 
            'CC_Base_L_BigToe1', 
            'CC_Base_L_CalfTwist01', 
            'CC_Base_L_CalfTwist02', 
            'CC_Base_L_KneeShareBone', 
            'CC_Base_L_ThighTwist01', 
            'CC_Base_L_ThighTwist02', 
            'CC_Base_R_Thigh', 
            'CC_Base_R_ThighTwist01', 
            'CC_Base_R_ThighTwist02', 
            'CC_Base_R_Calf', 
            'CC_Base_R_Foot', 
            'CC_Base_R_ToeBase', 
            'CC_Base_R_PinkyToe1', 
            'CC_Base_R_BigToe1', 
            'CC_Base_R_IndexToe1', 
            'CC_Base_R_MidToe1', 
            'CC_Base_R_RingToe1', 
            'CC_Base_R_ToeBaseShareBone', 
            'CC_Base_R_KneeShareBone', 
            'CC_Base_R_CalfTwist01', 
            'CC_Base_R_CalfTwist02', 
            'CC_Base_Waist', 
            'CC_Base_Spine01', 
            'CC_Base_Spine02', 
            'CC_Base_NeckTwist01', 
            'CC_Base_NeckTwist02', 
            'CC_Base_Head', 
            'CC_Base_FacialBone', 
            'CC_Base_JawRoot', 
            'CC_Base_Tongue01', 
            'CC_Base_Tongue02', 
            'CC_Base_Tongue03', 
            'CC_Base_Teeth02', 
            'CC_Base_R_Eye', 
            'CC_Base_L_Eye', 
            'CC_Base_UpperJaw', 
            'CC_Base_Teeth01', 
            'CC_Base_L_Clavicle', 
            'CC_Base_L_Upperarm', 
            'CC_Base_L_Forearm', 
            'CC_Base_L_ForearmTwist01', 
            'CC_Base_L_ForearmTwist02', 
            'CC_Base_L_ElbowShareBone', 
            'CC_Base_L_Hand', 
            'CC_Base_L_Mid1', 
            'CC_Base_L_Mid2', 
            'CC_Base_L_Mid3', 
            'CC_Base_L_Index1', 
            'CC_Base_L_Index2', 
            'CC_Base_L_Index3', 
            'CC_Base_L_Ring1', 
            'CC_Base_L_Ring2', 
            'CC_Base_L_Ring3', 
            'CC_Base_L_Pinky1', 
            'CC_Base_L_Pinky2', 
            'CC_Base_L_Pinky3', 
            'CC_Base_L_Thumb1', 
            'CC_Base_L_Thumb2', 
            'CC_Base_L_Thumb3', 
            'CC_Base_L_UpperarmTwist01', 
            'CC_Base_L_UpperarmTwist02', 
            'CC_Base_R_Clavicle', 
            'CC_Base_R_Upperarm', 
            'CC_Base_R_UpperarmTwist01', 
            'CC_Base_R_UpperarmTwist02', 
            'CC_Base_R_Forearm', 
            'CC_Base_R_ForearmTwist01', 
            'CC_Base_R_ForearmTwist02', 
            'CC_Base_R_ElbowShareBone', 
            'CC_Base_R_Hand', 
            'CC_Base_R_Mid1', 
            'CC_Base_R_Mid2', 
            'CC_Base_R_Mid3', 
            'CC_Base_R_Ring1', 
            'CC_Base_R_Ring2', 
            'CC_Base_R_Ring3', 
            'CC_Base_R_Thumb1', 
            'CC_Base_R_Thumb2', 
            'CC_Base_R_Thumb3', 
            'CC_Base_R_Index1', 
            'CC_Base_R_Index2', 
            'CC_Base_R_Index3', 
            'CC_Base_R_Pinky1', 
            'CC_Base_R_Pinky2', 
            'CC_Base_R_Pinky3', 
            'CC_Base_R_RibsTwist', 
            'CC_Base_R_Breast', 
            'CC_Base_L_RibsTwist', 
            'CC_Base_L_Breast'
            ]
        self.delJnt = [
            'CC_Base_L_ToeBaseShareBone',
            'CC_Base_L_KneeShareBone', 
            'CC_Base_L_PinkyToe1', 
            'CC_Base_L_RingToe1', 
            'CC_Base_L_MidToe1', 
            'CC_Base_L_IndexToe1', 
            'CC_Base_L_BigToe1', 
            'CC_Base_R_ToeBaseShareBone', 
            'CC_Base_R_KneeShareBone', 
            'CC_Base_R_PinkyToe1', 
            'CC_Base_R_BigToe1', 
            'CC_Base_R_IndexToe1', 
            'CC_Base_R_MidToe1', 
            'CC_Base_R_RingToe1', 
            'CC_Base_Tongue03', 
            'CC_Base_Tongue02', 
            'CC_Base_Tongue01', 
            'CC_Base_Teeth02', 
            'CC_Base_JawRoot', 
            'CC_Base_L_Eye', 
            'CC_Base_R_Eye', 
            'CC_Base_Teeth01', 
            'CC_Base_UpperJaw', 
            'CC_Base_FacialBone', 
            'CC_Base_L_ElbowShareBone', 
            'CC_Base_R_ElbowShareBone', 
            'CC_Base_L_Breast', 
            'CC_Base_L_RibsTwist', 
            'CC_Base_R_Breast', 
            'CC_Base_R_RibsTwist', 
            ]
        self.bindJnt = [i for i in self.allJnt if not i in self.delJnt]
        self.unitTimeIndex = {
            'game': 15, 
            'film': 24, 
            'pal': 25, 
            'ntsc': 30, 
            'show': 48, 
            'palf': 50, 
            'ntscf': 60, 
            }
        self.unitLengthIndex = {
            'mm': 0.1, 
            'cm': 1, 
            'm': 100, 
            'km': 100000, 
            'in': 2.54, 
            'ft': 30.48, 
            'yd': 91.44, 
            'mi': 160934, 
            }


    def cleanUp(self):
        # null check
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning("Please, select bodies.")
            return
        # main flows
        self.cutJntKeyframe()
        unBindedJoints = self.unbindSkin(*sel)
        self.deleteBlendShape(*sel)
        self.deleteUselessJnt(*unBindedJoints)
        self.resetRotation(*self.bindJnt)
        self.unitChange()
        # delete "RL_BoneRoot" joint
        pm.parent(self.allJnt[1], w=True)
        pm.delete(self.allJnt[0])


    def cutJntKeyframe(self):
        for i in self.allJnt:
            try:
                pm.cutKey(i, cl=True)
            except:
                continue


    def unbindSkin(self, *arg):
        """ *arg must be mesh type. """
        result = []
        for geo in arg:
            skinClt = pm.listHistory(geo, type="skinCluster")
            skinClt = skinClt[0]
            try:
                for jnt in self.delJnt:
                    pm.skinCluster(skinClt, e=True, ri=jnt)
                    result.append(jnt)
            except:
                continue
        return result


    def deleteUselessJnt(self, *arg):
        for i in arg:
            try:
                pm.delete(i)
            except:
                continue


    def deleteBlendShape(self, *arg):
        for geo in arg:
            bls = pm.listHistory(geo, type="blendShape")
            try:    shp = pm.listHistory(bls, type="mesh")
            except: continue
            target = []
            for i in shp:
                obj = i.getParent()
                if obj == geo:
                    continue
                else:
                    target.append(obj)
            pm.delete(bls, target)


    def resetRotation(self, *arg):
        xyz = ["X", "Y", "Z"]
        for jnt in arg:
            jnt = pm.PyNode(jnt)
            rot = jnt.getRotation()
            for i, r in zip(xyz, rot):
                exists = pm.getAttr(f"{jnt}.jointOrient{i}")
                pm.setAttr(f"{jnt}.jointOrient{i}", r + exists)
                pm.setAttr(f"{jnt}.rotate{i}", 0)
                

    def unitChange(self):
        """ accuRig exports to fbx at 60fps. Fix to 
        - 60fps -> 24fps
        - cm -> cm
        - startFrame, endFrame -> 0, 120
         """
        unitTime = pm.currentUnit(q=True, t=True)
        unitLength = pm.currentUnit(q=True, l=True)
        if unitTime != "film":
            pm.currentUnit(t="film")
        if unitLength != "cm":
            pm.currentUnit(l="cm")
        pm.playbackOptions(min=0, max=120)


class CopyRigJoints:
    def __init__(self):
        self.srcRoot = "CC_Base_Hip"
        self.rigRoot = "rig_Hip"
        self.topGroup = "rigBones"


    def copyHipsJoint(self):
        if not pm.objExists(self.rigRoot):
            pm.duplicate(self.srcRoot, rr=True, n=self.rigRoot)
        pm.parent(self.rigRoot, self.topGroup)
        pm.select(self.rigRoot, hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("CC_Base_", "rig_")
            pm.rename(i, new)


    def copyArmsJoint(self):
        for side in ["L", "R"]:
            for handle in ["IK", "FK"]:
                org = f"rig_{side}_Upperarm"
                new = f"rig_{side}_Upperarm_{handle}"
                if pm.objExists(new):
                    continue
                pm.duplicate(org, rr=True, n=new)
                pm.select(new, hi=True)
                for i in pm.ls(sl=True)[1:]:
                    if handle == i.split("_")[-1]:
                        continue
                    else:
                        pm.rename(i, f"{i}_{handle}")
                deleteIKJnt = [
                    f"rig_{side}_ForearmTwist01_{handle}", 
                    f"rig_{side}_Mid1_{handle}", 
                    f"rig_{side}_Index1_{handle}", 
                    f"rig_{side}_Ring1_{handle}", 
                    f"rig_{side}_Pinky1_{handle}", 
                    f"rig_{side}_Thumb1_{handle}", 
                    f"rig_{side}_UpperarmTwist01_{handle}"
                    ]
                try:
                    pm.delete(deleteIKJnt)
                except:
                    pass


    def copyLegsJoint(self):
        for side in ["L", "R"]:
            for handle in ["IK", "FK"]:
                org = f"rig_{side}_Thigh"
                new = f"rig_{side}_Thigh_{handle}"
                if pm.objExists(new):
                    continue
                pm.duplicate(org, rr=True, n=new)
                pm.select(new, hi=True)
                for i in pm.ls(sl=True)[1:]:
                    if handle == i.split("_")[-1]:
                        continue
                    else:
                        pm.rename(i, f"{i}_{handle}")
                deleteIKJnt = [
                    f"rig_{side}_ThighTwist01_{handle}", 
                    f"rig_{side}_CalfTwist01_{handle}", 
                    ]
                try:
                    pm.delete(deleteIKJnt)
                except:
                    pass


class RigArms:
    def __init__(self):
        self.leftTopGroup = "cc_LeftArm_grp"
        self.rightTopGroup = "cc_RightArm_grp"
        self.leftIKCtrls = [
            "cc_LeftArm_IK", 
            "cc_LeftForeArmPoleVector", 
            "cc_LeftHand_IK", 
            ]
        self.rightIKCtrls = [
            "cc_RightArm_IK", 
            "cc_RightForeArmPoleVector", 
            "cc_RightHand_IK", 
            ]
        self.leftFKCtrls = [
            "cc_LeftArm_FK", 
            "cc_LeftForeArm_FK", 
            "cc_LeftHand_FK"
            ]
        self.rightFKCtrls = [
            "cc_RightArm_FK", 
            "cc_RightForeArm_FK", 
            "cc_RightHand_FK"
            ]
        self.leftIKCtrlsGrp = [
            "cc_LeftArm_IK_grp", 
            "cc_LeftForeArmPoleVector_grp", 
            "cc_LeftHand_IK_grp", 
            ]
        self.rightIKCtrlsGrp = [
            "cc_RightArm_IK_grp", 
            "cc_RightForeArmPoleVector_grp", 
            "cc_RightHand_IK_grp", 
            ]
        self.leftFKCtrlsGrp = [
            "cc_LeftArm_FK_grp", 
            "cc_LeftForeArm_FK_grp", 
            "cc_LeftHand_FK_grp"
            ]
        self.rightFKCtrlsGrp = [
            "cc_RightArm_FK_grp", 
            "cc_RightForeArm_FK_grp", 
            "cc_RightHand_FK_grp"
            ]
        self.ikCtrlsType = [
            "circle", 
            "sphere", 
            "cube"
            ]
        self.fkCtrlsSize = [11, 9, 7]


    def cleanUp(self):
        leftArms = self.leftIKCtrls + self.leftIKCtrlsGrp
        leftArms += self.leftFKCtrls + self.leftFKCtrlsGrp
        rightArms = self.rightIKCtrls + self.rightIKCtrlsGrp
        rightArms += self.rightFKCtrls + self.rightFKCtrlsGrp
        allArms = leftArms + rightArms
        for i in allArms:
            try:
                pm.delete(i)
            except:
                continue


    def rigArmsIK(self, *jnts):
        ikJoints = [pm.PyNode(i) for i in jnts] if jnts else pm.ls(sl=True)
        if len(ikJoints) != 3:
            pm.warning("Three joints needed.")
            return
        side = hjk.getLeftOrRight(*ikJoints)
        if side == "Left":
            topGrp = self.leftTopGroup
            ctrls = self.leftIKCtrls
            ctrlsGrp = self.leftIKCtrlsGrp
        elif side == "Right":
            topGrp = self.rightTopGroup
            ctrls = self.rightIKCtrls
            ctrlsGrp = self.rightIKCtrlsGrp
        else:
            return
        ctrlType = {typ: name for typ, name in zip(self.ikCtrlsType, ctrls)}
        ctrl = hjk.Controllers()
        ccShoulder, ccElbow, ccWrist = ctrl.createControllers(**ctrlType)
        firstJnt, endJnt = ikJoints[::2]
        self.createShoulderIK(firstJnt, ccShoulder)
        ikHandle = self.createElbowIK(ikJoints, ccElbow)
        self.createWristIK(endJnt, ccWrist, ikHandle, side)
        self.topGrouping(topGrp, ctrlsGrp)


    def rigArmsFK(self, *jnts):
        fkJoints = [pm.PyNode(i) for i in jnts] if jnts else pm.ls(sl=True)
        if len(fkJoints) != 3:
            pm.warning("Three joints needed.")
            return
        side = hjk.getLeftOrRight(*fkJoints)
        if side == "Left":
            topGrp = self.leftTopGroup
            ctrls = self.leftFKCtrls
            ctrlsGrp = self.leftFKCtrlsGrp
            mirrorConstant = 1
            rot = 0
        elif side == "Right":
            topGrp = self.rightTopGroup
            ctrls = self.rightFKCtrls
            ctrlsGrp = self.rightFKCtrlsGrp
            mirrorConstant = -1
            rot = 180
        else:
            return
        fkGroups = []
        for ctrl, jnt, size in zip(ctrls, fkJoints, self.fkCtrlsSize):
            cc = pm.circle(ch=False, r=size, nr=(1, 0, 0), n=ctrl)
            cc = cc[0]
            pm.matchTransform(cc, jnt, pos=True, rot=True)
            pm.rotate(cc, [0, 0, mirrorConstant*90], r=True, os=True, fo=True)
            ccGrp = hjk.groupingWithOwnPivot(cc)
            ccGrp = ccGrp[0]
            pm.rotate(ccGrp, [rot, 0, 0], r=True, os=True, fo=True)
            pm.parentConstraint(cc, jnt, mo=True, w=1.0)
            fkGroups.append(ccGrp)
            fkGroups.append(cc)
        hjk.parentHierarchically(fkGroups)
        self.topGrouping(topGrp, ctrlsGrp[:1:])


    def createShoulderIK(self, joint, controller):
        pm.rotate(controller, [0, 0, 90])
        pm.makeIdentity(controller, a=True, t=0, r=1, s=0, jo=0, n=0, pn=1)
        pm.matchTransform(controller, joint, pos=True)
        pm.pointConstraint(controller, joint, mo=True)
        hjk.groupingWithOwnPivot(controller)


    def createElbowIK(self, joints: list, controller: str):
        threeJoints = joints[0:3]
        _1stJnt, _3rdJnt = threeJoints[::2]
        ikH = pm.ikHandle(sj=_1stJnt, ee=_3rdJnt, sol="ikRPsolver")
        ikH = ikH[0]
        polevectorJoints = hjk.createPolevectorJoint(*threeJoints)
        polevectorJoint1, polevectorJoint2 = polevectorJoints
        pm.matchTransform(controller, polevectorJoint2, pos=True)
        pm.delete(polevectorJoint1)
        pm.poleVectorConstraint(controller, ikH, w=1)
        hjk.groupingWithOwnPivot(controller)
        return ikH


    def createWristIK(self, joint, ctrl, ikHandle, side):
        pm.matchTransform(ctrl, joint, pos=True)
        ctrlGrp = hjk.groupingWithOwnPivot(ctrl)
        ctrlGrp = ctrlGrp[0]
        rot = 0 if side=="Left" else 180
        pm.rotate(ctrlGrp, [rot, 0, 0], r=True, os=True, fo=True)
        pm.orientConstraint(ctrl, joint, mo=True, w=1)
        try:
            pm.parent(ikHandle, ctrl)
            pm.setAttr(f"{ikHandle}.visibility", 0)
        except:
            pass


    def topGrouping(self, parents: str, children: list=[]):
        if not pm.objExists(parents):
            pm.group(em=True, n=parents)
        pm.parent(children, parents)


class RigLegs:
    def __init__(self):
        self.leftTopGroup = "cc_LeftLeg_grp"
        self.rightTopGroup = "cc_RightLeg_grp"
        self.leftFootJnt = "rig_L_Foot_IK"
        self.rightFootJnt = "rig_R_Foot_IK"
        self.leftIKCtrls = [
            "cc_LeftUpLeg_IK", 
            "cc_LeftLegPoleVector", 
            "cc_LeftFoot_IK"
            ]
        self.rightIKCtrls = [
            "cc_rightUpLeg_IK", 
            "cc_rightLegPoleVector", 
            "cc_rightFoot_IK"
            ]
        self.leftFKCtrls = [
            "cc_LeftUpLeg_FK", 
            "cc_LeftLeg_FK", 
            "cc_LeftFoot_FK", 
            "cc_LeftToeBase_IK"
            ]
        self.rightFKCtrls = [
            "cc_rightUpLeg_FK", 
            "cc_rightLeg_FK", 
            "cc_rightFoot_FK", 
            "cc_rightToeBase_IK"
            ]
        self.leftIKCtrlsGrp = [
            "cc_LeftUpLeg_IK_grp", 
            "cc_LeftLegPoleVector_grp", 
            "cc_LeftFoot_IK_grp"
            ]
        self.rightIKCtrlsGrp = [
            "cc_rightUpLeg_IK_grp", 
            "cc_rightLegPoleVector_grp", 
            "cc_rightFoot_IK_grp"
            ]
        self.leftFKCtrlsGrp = [
            "cc_LeftUpLeg_FK_grp", 
            "cc_LeftLeg_FK_grp", 
            "cc_LeftFoot_FK_grp", 
            "cc_LeftToeBase_IK_grp"
            ]
        self.rightFKCtrlsGrp = [
            "cc_rightUpLeg_FK_grp", 
            "cc_rightLeg_FK_grp", 
            "cc_rightFoot_FK_grp", 
            "cc_rightToeBase_IK_grp"
            ]
        self.ikCtrlsType = [
            "scapula", 
            "sphere", 
            "foot2"
            ]
        self.fkCtrlsSize = [11, 9, 7]
        self.leftLocators = {
            "loc_LeftHeel_IK": [6, 0, -3], 
            "loc_LeftToe_End_IK": [6, 0, 15], 
            "loc_LeftBankIn_IK": [3, 0, 0], 
            "loc_LeftBankOut_IK": [15, 0, 0], 
            "loc_LeftToeBase_IK": [6, 3, 6], 
            "loc_LeftFoot_IK": [6, 12, -3], 
            }
        self.rightLocators = {
            "loc_RightHeel_IK": [-6, 0, -3], 
            "loc_RightToe_End_IK": [-6, 0, 15], 
            "loc_RightBankIn_IK": [-3, 0, 0], 
            "loc_RightBankOut_IK": [-15, 0, 0], 
            "loc_RightToeBase_IK": [-6, 3, 6], 
            "loc_RightFoot_IK": [-6, 12, -3], 
            }


    def cleanUp(self):
        leftArms = self.leftIKCtrls + self.leftIKCtrlsGrp
        leftArms += self.leftFKCtrls + self.leftFKCtrlsGrp
        rightArms = self.rightIKCtrls + self.rightIKCtrlsGrp
        rightArms += self.rightFKCtrls + self.rightFKCtrlsGrp
        allArms = leftArms + rightArms
        for i in allArms:
            try:
                pm.delete(i)
            except:
                continue


    def locatorPreset(self, locators: dict):
        side = hjk.getLeftOrRight(*locators.keys())
        if side == "Left":
            mirrorConstant = 1
        elif side == "Right":
            mirrorConstant = -1
        else:
            return
        for name, pos in locators.items():
            x, y, z = pos
            pos = [x, y, mirrorConstant*z]
            loc = pm.spaceLocator(p=(0, 0, 0), n=name)
            pm.move(loc, pos)


    def rigLegsIK(self, *jnts):
        ikJoints = [pm.PyNode(i) for i in jnts] if jnts else pm.ls(sl=True)
        if len(ikJoints) != 4:
            pm.warning("Four joints needed.")
            return
        side = hjk.getLeftOrRight(*ikJoints)
        if side == "Left":
            topGrp = self.leftTopGroup
            ctrls = self.leftIKCtrls
            ctrlsGrp = self.leftIKCtrlsGrp
            mirrorConstant = 1
        elif side == "Right":
            topGrp = self.rightTopGroup
            ctrls = self.rightIKCtrls
            ctrlsGrp = self.rightIKCtrlsGrp
            mirrorConstant = -1
        else:
            return
        _1stJnt, _2ndJnt, _3rdJnt, _4thJnt = ikJoints
        # self.updateLocatorsPosition()
        ctrl = hjk.Controllers()
        ctrlType = {t: n for t, n in zip(self.ikCtrlsType, self.leftIKCtrls)}
        ccPelvis, ccKnee, ccFoot = ctrl.createControllers(**ctrlType)
        self.createPelvisIK(_1stJnt, ccPelvis, mirrorConstant)
        ikH = self.createKneeIK(ikJoints, ccKnee)
        self.createFootIK(ccFoot, _3rdJnt)


    def createPelvisIK(self, joint, controller, mirrorConstant=1):
        pm.rotate(controller, [0, 0, mirrorConstant*(-90)])
        pm.makeIdentity(controller, a=True, t=0, r=1, s=0, jo=0, n=0, pn=1)
        pm.matchTransform(controller, joint, pos=True)
        pm.pointConstraint(controller, joint, mo=True)
        hjk.groupingWithOwnPivot(controller)


    def createKneeIK(self, joints: list, controller: str):
        threeJoints = joints[0:3]
        _1stJnt, _3rdJnt = threeJoints[::2]
        ikH = pm.ikHandle(sj=_1stJnt, ee=_3rdJnt, sol="ikRPsolver")
        ikH = ikH[0]
        polevectorJoints = hjk.createPolevectorJoint(*threeJoints)
        polevectorJoint1, polevectorJoint2 = polevectorJoints
        pm.matchTransform(controller, polevectorJoint2, pos=True)
        pm.delete(polevectorJoint1)
        pm.poleVectorConstraint(controller, ikH, w=1)
        hjk.groupingWithOwnPivot(controller)
        return ikH


    def updateLocatorsPosition(self):
        leftLoc = {i: hjk.getPosition(i) for i in self.leftLocators.keys()}
        rightLoc = {i: hjk.getPosition(i) for i in self.rightLocators.keys()}
        self.leftLocators = leftLoc
        self.rightLocators = rightLoc
            

    def createFootIK(self, ctrl, jnt):
        pm.matchTransform(ctrl, jnt, pos=True)
        pm.setAttr(f"{ctrl}.translateY", 0)
        x, y, z = hjk.getPosition(jnt)
        pm.move(x, y, z, [f"{ctrl}.rotatePivot", f"{ctrl}.scalePivot"], ws=1)


    def rigLegsFK(self):
        pass


class RigFingers:
    def __init__(self):
        self.leftTopGroup = "cc_LeftHandFingers_grp"
        self.rightTopGroup = "cc_RightHandFingers_grp"
        self.leftCtrls = [
            "cc_LeftHandThumb1", 
            "cc_LeftHandThumb2", 
            "cc_LeftHandThumb3", 
            "cc_LeftHandIndex1", 
            "cc_LeftHandIndex2", 
            "cc_LeftHandIndex3", 
            "cc_LeftHandMiddle1", 
            "cc_LeftHandMiddle2", 
            "cc_LeftHandMiddle3", 
            "cc_LeftHandRing1", 
            "cc_LeftHandRing2", 
            "cc_LeftHandRing3", 
            "cc_LeftHandPinky1", 
            "cc_LeftHandPinky2", 
            "cc_LeftHandPinky3", 
            ]
        self.leftCtrlsGrp = [
            "cc_LeftHandThumb1_grp", 
            "cc_LeftHandThumb2_grp", 
            "cc_LeftHandThumb3_grp", 
            "cc_LeftHandIndex1_grp", 
            "cc_LeftHandIndex2_grp", 
            "cc_LeftHandIndex3_grp", 
            "cc_LeftHandMiddle1_grp", 
            "cc_LeftHandMiddle2_grp", 
            "cc_LeftHandMiddle3_grp", 
            "cc_LeftHandRing1_grp", 
            "cc_LeftHandRing2_grp", 
            "cc_LeftHandRing3_grp", 
            "cc_LeftHandPinky1_grp", 
            "cc_LeftHandPinky2_grp", 
            "cc_LeftHandPinky3_grp", 
            ]
        self.rightCtrls = [
            "cc_RightHandThumb1", 
            "cc_RightHandThumb2", 
            "cc_RightHandThumb3", 
            "cc_RightHandIndex1", 
            "cc_RightHandIndex2", 
            "cc_RightHandIndex3", 
            "cc_RightHandMiddle1", 
            "cc_RightHandMiddle2", 
            "cc_RightHandMiddle3", 
            "cc_RightHandRing1", 
            "cc_RightHandRing2", 
            "cc_RightHandRing3", 
            "cc_RightHandPinky1", 
            "cc_RightHandPinky2", 
            "cc_RightHandPinky3", 
            ]
        self.rightCtrlsGrp = [
            "cc_RightHandThumb1_grp", 
            "cc_RightHandThumb2_grp", 
            "cc_RightHandThumb3_grp", 
            "cc_RightHandIndex1_grp", 
            "cc_RightHandIndex2_grp", 
            "cc_RightHandIndex3_grp", 
            "cc_RightHandMiddle1_grp", 
            "cc_RightHandMiddle2_grp", 
            "cc_RightHandMiddle3_grp", 
            "cc_RightHandRing1_grp", 
            "cc_RightHandRing2_grp", 
            "cc_RightHandRing3_grp", 
            "cc_RightHandPinky1_grp", 
            "cc_RightHandPinky2_grp", 
            "cc_RightHandPinky3_grp", 
            ]


    def rigFingers(self, *jnts):
        fingerJnt = [pm.PyNode(i) for i in jnts] if jnts else pm.ls(sl=True)
        if len(fingerJnt) != 15:
            pm.warning("15 joints needed.")
            return
        side = hjk.getLeftOrRight(*fingerJnt)
        if side == "Left":
            topGrp = self.leftTopGroup
            ctrls = self.leftCtrls
            size = 1.5
            rot = 0
        elif side == "Right":
            topGrp = self.rightTopGroup
            ctrls = self.rightCtrls
            size = 1.5
            rot = 180
        else:
            return
        if not pm.objExists(topGrp):
            pm.group(em=True, n=topGrp)
        fingerGrp = []
        for ctrl, jnt in zip(ctrls, fingerJnt):
            # size = self.getCtrlSize(ctrl)
            cc = pm.circle(ch=False, r=size, nr=(1, 0, 0), n=ctrl)
            cc = cc[0]
            pm.matchTransform(cc, jnt, pos=True)
            pm.orientConstraint(jnt, cc, o=(0, 0, 90), w=1)
            pm.delete(cc, cn=True)
            ccGrp = hjk.groupingWithOwnPivot(cc)[0]
            pm.rotate(ccGrp, [rot, 0, 0], r=True, os=True, fo=True)
            pm.parentConstraint(cc, jnt, mo=True, w=1.0)
            fingerGrp.append(ccGrp)
            fingerGrp.append(cc)
        for i in range(0, len(fingerGrp), 6):
            hjk.parentHierarchically(fingerGrp[i:i+6])
            pm.parent(fingerGrp[i], topGrp)


    def getCtrlSize(self, word: str) -> int:
            numbers = re.findall(r'\d+', word)
            num = int(numbers[-1])
            if num == 1:
                size = 3
            elif num == 2:
                size = 2
            elif num == 3:
                size = 1
            else:
                size = 0
            return size


    def cleanUp(self):
        leftArms = self.leftCtrls + self.leftCtrlsGrp + [self.leftTopGroup]
        rightArms = self.rightCtrls + self.rightCtrlsGrp + [self.rightTopGroup]
        allArms = leftArms + rightArms
        for i in allArms:
            try:
                pm.delete(i)
            except:
                continue


# ilJ = ['rig_L_Upperarm_IK', 'rig_L_Forearm_IK', 'rig_L_Hand_IK']
# irJ = ['rig_R_Upperarm_IK', 'rig_R_Forearm_IK', 'rig_R_Hand_IK']
# flJ = ['rig_L_Upperarm_FK', 'rig_L_Forearm_FK', 'rig_L_Hand_FK']
# frJ = ['rig_R_Upperarm_FK', 'rig_R_Forearm_FK', 'rig_R_Hand_FK']
# ra = RigArms()
# ra.cleanUp()
# ra.rigArmsIK(*ilJ)
# ra.rigArmsIK(*irJ)
# ra.rigArmsFK(*flJ)
# ra.rigArmsFK(*frJ)

# rl = RigLegs()
# rl.locatorPreset(rl.leftLocators)
# rl.locatorPreset(rl.rightLocators)
# rl.cleanUp()
# rl.rigLegsIK()


# ctrl = hjk.Controllers()
# ctrl.createControllers(foot2="cc_RightFoot_IK")
# hjk.groupingWithOwnPivot()
# hjk.createPolevectorJoint()

# leftFingers = [
#     'rig_L_Thumb1', 'rig_L_Thumb2', 'rig_L_Thumb3', 
#     'rig_L_Index1', 'rig_L_Index2', 'rig_L_Index3', 
#     'rig_L_Mid1', 'rig_L_Mid2', 'rig_L_Mid3', 
#     'rig_L_Ring1', 'rig_L_Ring2', 'rig_L_Ring3', 
#     'rig_L_Pinky1', 'rig_L_Pinky2', 'rig_L_Pinky3'
#     ]
# rightFingers = [
#     'rig_R_Thumb1', 'rig_R_Thumb2', 'rig_R_Thumb3', 
#     'rig_R_Index1', 'rig_R_Index2', 'rig_R_Index3', 
#     'rig_R_Mid1', 'rig_R_Mid2', 'rig_R_Mid3', 
#     'rig_R_Ring1', 'rig_R_Ring2', 'rig_R_Ring3', 
#     'rig_R_Pinky1', 'rig_R_Pinky2', 'rig_R_Pinky3'
#     ]


# rf = RigFingers()
# rf.cleanUp()
# rf.rigFingers(*leftFingers)
# rf.rigFingers(*rightFingers)


# rd = RowData()
# for i in rd.bindJnt[1:]:
#     jnt = i.replace("CC_Base_", "rig_")
#     pm.connectAttr(f"{jnt}.translate", f"{i}.translate", f=True)
#     pm.connectAttr(f"{jnt}.rotate", f"{i}.rotate", f=True)



sel = pm.ls(sl=True)
for i in sel:
    a = pm.spaceLocator(p=(0,0,0))
    pm.matchTransform(a, i, pos=True)
