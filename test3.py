import pymel.core as pm
from general import *

class AccuRig:
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


# acc = AccuRig()
# acc.cleanUp()
rigGrp = RigGroups()
rigGrp.createRigGroups("sachaenamA")

