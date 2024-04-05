from collections import Counter
import pymel.core as pm
import general as hjk


class Clean:
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
        self.resetRotation()
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


    def resetRotation(self):
        xyz = ["X", "Y", "Z"]
        for jnt in self.bindJnt:
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


class Copy:
    def __init__(self):
        self.srcRoot = "CC_Base_Hip"
        self.rigRoot = "rig_Hip"
        self.topGroup = "rigBones"


    def copyHip(self):
        if not pm.objExists(self.rigRoot):
            pm.duplicate(self.srcRoot, rr=True, n=self.rigRoot)
        pm.parent(self.rigRoot, self.topGroup)
        pm.select(self.rigRoot, hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("CC_Base_", "rig_")
            pm.rename(i, new)


    def copyArms(self):
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


    def copyLegs(self):
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
        pass


    def getLeftOrRight(self, objName: str):
        if not objName or not isinstance(objName, str):
            result = ""
        elif "Left" in objName:
            result = "Left"
        elif "L_" in objName:
            result = "Left"
        elif "Right" in objName:
            result = "Right"
        elif "R_" in objName:
            result = "Right"
        else:
            result = ""
        return result


    def rigArmsIK(self, *jnts):
        # check joint's numbers
        ikJoints = [pm.PyNode(i) for i in jnts] if jnts else pm.ls(sl=True)
        if len(ikJoints) < 3:
            pm.warning("Please, Select three joints.")
            return
        # check Left or Right
        jntsSide = [self.getLeftOrRight(i.name()) for i in ikJoints]
        count = Counter(jntsSide).most_common(1)[0]
        num = count[1]
        if num == 3:
            side = count[0]
            print(side)
        else:
            pm.warning("All joints must have a left or right side.")
            return
        # create controllers
        ctrlsName = [
            f"cc_{side}Arm_IK", 
            f"cc_{side}ForeArmPoleVector", 
            f"cc_{side}Hand_IK", 
            ]
        ctrlsType = [
            "circle", 
            "sphere", 
            "cube"
            ]
        ctrlsDict = {t: n for t, n in zip(ctrlsType, ctrlsName)}
        for i in ctrlsName:
            if pm.objExists(i):
                pm.delete(i)
            else:
                continue
        ctrl = hjk.Controllers()
        ccNames = ctrl.createControllers(**ctrlsDict)
        firstJnt, endJnt = ikJoints[::2]
        ccCircle, ccSphere, ccCube = ccNames
        # Rig - firstJoint
        ikH = pm.ikHandle(sj=firstJnt, ee=endJnt, sol="ikRPsolver")[0]
        pm.rotate(ccCircle, [0, 0, 90])
        pm.makeIdentity(ccCircle, a=True, t=0, r=1, s=0, jo=0, n=0, pn=1)
        pm.matchTransform(ccCircle, firstJnt, pos=True)
        pm.pointConstraint(ccCircle, firstJnt, mo=True)
        if pm.objExists(f"{ccCircle}_grp"):
            pm.delete(f"{ccCircle}_grp")
        ccCircleGrp = hjk.groupingWithOwnPivot(ccCircle)[0]
        # Rig - middleJoint
        polevectorJoints = hjk.createPolevectorJoint(ikJoints)
        startJointOfPolevector, endJointOfPolevector = polevectorJoints
        pm.matchTransform(ccSphere, endJointOfPolevector, pos=True)
        pm.delete(startJointOfPolevector)
        pm.poleVectorConstraint(ccSphere, ikH, w=1)
        if pm.objExists(f"{ccSphere}_grp"):
            pm.delete(f"{ccSphere}_grp")
        ccSphereGrp = hjk.groupingWithOwnPivot(ccSphere)[0]
        # Rig - endJoint
        pm.matchTransform(ccCube, endJnt, pos=True)
        if pm.objExists(f"{ccCube}_grp"):
            pm.delete(f"{ccCube}_grp")
        ccCubeGrp = hjk.groupingWithOwnPivot(ccCube)[0]
        if side == "Right":
            pm.rotate(ccCubeGrp, [180, 0, 0], r=True, os=True, fo=True)
        pm.orientConstraint(ccCube, endJnt, mo=True, w=1)
        # Rig - grouping
        topGroupName = ccCircle.rsplit("_", 1)[0]
        if pm.objExists(topGroupName):
            pm.delete(topGroupName)
        pm.group(em=True, n=topGroupName)
        for i in [ccCircleGrp, ccSphereGrp, ccCubeGrp]:
            pm.parent(i, topGroupName)
        pm.setAttr(f"{ikH}.visibility", 0)
        pm.parent(ikH, ccCube)
        pm.select(cl=True)


    def cleanUp(self, *arg):
        delList = []
        for i in arg:
            if pm.objExists(i):
                delList.append(i)
            if pm.objExists(f"{i}_g"):
                delList.append(f"{i}_g")
        for i in delList:
            try:
                pm.delete(i)
            except:
                continue
        return delList


    def rigArmsFK(self, *jnts):
        fkJoints = jnts if jnts else pm.ls(sl=True)
        if len(fkJoints) < 3:
            pm.warning("Please, Select three joints.")
            return
        # firstJnt, middleJnt, endJnt = fkJoints
        ctrlsName = [
            "cc_LeftArm_FK", 
            "cc_LeftForeArm_FK", 
            "cc_LeftHand_FK"
            ]
        ctrlsSize = [11, 9, 7]
        for ccName, size in zip(ctrlsName, ctrlsSize):
            if pm.objExists(ccName):
                pm.delete(ccName)
            pm.circle(ch=False, r=size, nr=(1, 0, 0), n=ccName)
        for ccName, jnt in zip(ctrlsName, fkJoints):
            pm.matchTransform(ccName, jnt, pos=True, rot=True)
            pm.rotate(ccName, [0, 0, 90], r=True, os=True, fo=True)
            pm.parentConstraint(ccName, jnt, mo=True, w=1.0)
        fkGroups = []
        for ccName in ctrlsName:
            ccNameGrp = hjk.groupingWithOwnPivot(ccName)
            ccNameGrp = ccNameGrp[0]
            fkGroups.append(ccNameGrp)
            fkGroups.append(ccName)
        hjk.parentHierarchically(fkGroups)
        



ra = RigArms()
ra.rigArmsIK("rig_R_Upperarm_IK", "rig_R_Forearm_IK", "rig_R_Hand_IK")