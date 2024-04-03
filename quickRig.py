from general import *
import os


class Car:
    def __init__(self):
        self.assetName = "assetName"
        self.sizeRatio = 1
        self.sizeCtrl = "cc_sizeController"
        self.mainCtrl = "cc_main"
        self.subCtrl = "cc_sub"
        self.rootJoint = "jnt_root"
        self.ctrlNames = {
            "car": "cc_body", 
            "car2": "cc_sub", 
            "car3": "cc_main", 
        }
        self.jntNameAndPos = {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_bodyEnd": (0, 145, 0), 
            "jnt_wheelLeftFront": (70, 30, 140), 
            "jnt_wheelLeftFrontEnd": (85, 30, 140), 
            "jnt_wheelRightFront": (-70, 30, 140), 
            "jnt_wheelRightFrontEnd": (-85, 30, 140), 
            "jnt_wheelLeftRear": (70, 30, -140), 
            "jnt_wheelLeftRearEnd": (85, 30, -140), 
            "jnt_wheelRightRear": (-70, 30, -140), 
            "jnt_wheelRightRearEnd": (-85, 30, -140), 
        }
        self.hierarchy = {
            "jnt_root": [
                [f"jnt_body{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftRear{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightRear{i}" for i in ["", "End"]], 
                ], 
            }


    def createJoints(self):
        # CleanUp first
        self.cleanUp()
        # Create joints
        for jnt, pos in self.jntNameAndPos.items():
            pm.select(cl=True)
            pm.joint(p=pos, n=jnt)
        # Set hierarchy
        for parents, childList in self.hierarchy.items():
            for children in childList:
                parentHierarchically(children)
                pm.makeIdentity(children, a=1, t=1, r=1, s=1, jo=1)
                pm.parent(children[0], parents)


    def createSizeController(self):
        self.sizeRatio = getBoundingBoxSize(self.rootJoint)
        pm.circle(nr=(0,1,0), ch=0, n=self.sizeCtrl, r=self.sizeRatio)
        pm.parent(self.rootJoint, self.sizeCtrl)


    def cleanUp(self):
        delGroups = [self.sizeCtrl, self.assetName]
        joints = list(self.jntNameAndPos.keys())
        grpNames = list(RigGroups().groupNames.keys())[1:]
        grpNames += getFlattenList(list(RigGroups().groupNames.values())[1:])
        ctrls = list(self.ctrlNames.values())
        delGroups += joints + grpNames + ctrls
        for i in delGroups:
            try:
                pm.delete(i)
            except:
                continue


    def updatePosition(self):
        for jnt in self.jntNameAndPos.keys():
            pos = pm.xform(jnt, q=True, t=True, ws=True)
            self.jntNameAndPos[jnt] = tuple(pos)


    def sameBothSide(self, side: str="LeftToRight"):
        """ The default change is from left to right. 
        But the opposite is also possible.
        >>> sameBothSide()
        >>> sameBothSide("RightToLeft")
         """
        # Update first
        self.updatePosition()
        # Split both side
        A, B = side.split("To")
        aSide = []
        bSide = []
        for jntName in self.jntNameAndPos.keys():
            if A in jntName:
                aSide.append(jntName)
            elif B in jntName:
                bSide.append(jntName)
            else:
                continue
        # Update opposite
        for idx, aJoint in enumerate(aSide):
            x, y, z = pm.xform(aJoint, q=True, t=True, ws=True)
            bJoint = bSide[idx]
            self.jntNameAndPos[bJoint] = (-1*x, y, z)
        # Create joints again
        self.createJoints()


    def build(self):
        # Update first
        self.updatePosition()
        self.createJoints()
        # create rig groups
        self.createRigGroups()
        self.createBasicCtrls()
        # createWheelCtrls


    def createRigGroups(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            self.assetName = "assetName"
        else:
            sceneName = os.path.basename(fullPath)
            self.assetName = sceneName.split("_")[1]
        rigGrp = RigGroups()
        rigGrp.createRigGroups(self.assetName)


    def createBasicCtrls(self):
        # create controllers
        ctrl = Controllers()
        ctrls = ctrl.createControllers(**self.ctrlNames)
        ccBody, ccSub, ccMain = ctrls
        # match position
        pm.matchTransform(ccBody, "jnt_body", pos=True)
        # grouping
        ccBodyGrp, ccSubGrp, ccMainGrp = groupingWithOwnPivot(*ctrls)
        rootJntGrp = groupingWithOwnPivot(self.rootJoint)
        # relationship
        pm.parent(ccSubGrp, ccMain)
        pm.parentConstraint(ccSub, ccBodyGrp, mo=True, w=1)
        pm.scaleConstraint(ccSub, ccBodyGrp, mo=True, w=1)
        try:
            pm.parent(ccMainGrp, "controllers")
            pm.parent(ccBodyGrp, "controllers")
            pm.parent(rootJntGrp, "rigBones")
        except:
            pm.warning("There are no basic rigging groups.")
        
        
    def createWheelCtrls(self):
        pass


class Wheel:
    def __init__(self, arg=None):
        self.sel = self.checkParam(arg)
        self.main()


    def main(self):
        for obj in self.sel:
            ctrl = self.createWheelCtrl(obj)
            off = self.createOffsetGrp(ctrl)
            loc = self.createCtrlLocator(ctrl)
            null, prev, orient = self.createGroupNames(off)
            self.createCtrlChannel(ctrl)
            self.createOffsetChannel(off)
            self.createCtrlGroup(off, null, prev, orient)
            self.createExpression(ctrl, off, loc, orient, prev)


    def checkParam(self, obj):
        """ Checks if there is an argument 
        and creates the argument as PyNode.
         """
        if obj and isinstance(obj, list):
            for j, k in enumerate(obj):
                if isinstance(k, pm.PyNode):
                    continue
                else:
                    obj[j] = pm.PyNode(k)
            result = obj
        else:
            result = pm.ls(sl=True)
        return result


    def createWheelCtrl(self, obj, sizeUp=1.2):
        """ Create a controller 1.2 times larger than 
        the boundingBox size of the selected object.
         """
        bb = pm.xform(obj, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        rad = max(x, y, z)
        rad = round(rad, 3) * sizeUp
        cuv = pm.circle(nr=(1, 0, 0), r=rad, n=f"cc_{obj}", ch=False)
        cuv = cuv[0]
        pm.matchTransform(cuv, obj, pos=True)
        return cuv


    def createOffsetGrp(self, obj):
        """ Create a parent group for the controller. """
        result = pm.group(obj, n=f"{obj}_offset")
        pm.xform(result, os=True, piv=(0,0,0))
        return result


    def createCtrlLocator(self, ctrl):
        """ Place the locator under the controller. """
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createGroupNames(self, offset):
        """ Create another group name. """
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
        return null, prev, orient


    def createCtrlChannel(self, ctrl):
        """ Creates a Radius channel and AutoRoll channel. """
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)


    def createOffsetChannel(self, offset):
        """ Create a PrePos channel in the offset group. """
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, null, prev, orient):
        """ Determine group relationships. """
        if offset.getParent():
            pm.parent(offset, offset.getParent())
        else:
            tempGrp = pm.group(em=True)
            pm.parent(offset, tempGrp)
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)


    def createExpression(self, ctrl, offset, loc, orient, prev):
        """ Create an expression. """
        br = '\n'
        # expression1
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}'
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}'
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3
        expr3 = f'{loc}.rotateX = $J'
        expr3 += ' + ($D/$C) * 360'
        expr3 += ' * $A'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($O))'
        expr3 += f' / $S;{br*2}'
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # final
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')


# car = Car()
# car.cleanUp()
# car.createJoints()
# car.sameBothSide()
# car.build()
# car.createRigGroups()


# wh = Wheel()
def createWheelCtrl(**kwargs):
    """ kwargs = {"wheelName1": (0, 0, 0), "wheelName2": (0, 0, 0), } """
    ctrl = Controllers()
    for wheelName, pos in kwargs.items():
        ccWheel = ctrl.createControllers(circle=wheelName)
        pm.rotate(ccWheel, (0, 0, 90))
        pm.makeIdentity(ccWheel, a=1, t=1, r=1, s=1, jo=0)
        print(pos)
        pm.move(ccWheel, (0, 5, 0))


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


    def duplicateHip(self):
        if not pm.objExists("rig_Hip"):
            pm.duplicate("CC_Base_Hip", rr=True, n="rig_Hip")
        pm.parent("rig_Hip", "rigBones")
        pm.select("rig_Hip", hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("CC_Base_", "rig_")
            pm.rename(i, new)


    def duplicateArms(self):
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


    def duplicateLegs(self):
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



# acc = AccuRig()
# acc.cleanUp()
# rigGrp = RigGroups()
# rigGrp.createRigGroups("sachaenamA")
# acc.duplicateHip()
# acc.duplicateArms()
# acc.duplicateLegs()


def rigArms():
    ctrl = Controllers()
    ctrlLeftIK = {
        "circle":"cc_LeftArm_IK", 
        "sphere": "cc_LeftForeArmPoleVector", 
        "cube": "cc_LeftHand_IK"
        }
    ccNames = ctrl.createControllers(**ctrlLeftIK)
    if not ccNames:
        return
    ccCircle, ccSphere, ccCube = ccNames
    jntIK = [
        "rig_L_Upperarm_IK", 
        "rig_L_Forearm_IK", 
        "rig_L_Hand_IK"
        ]
    firstJnt, middleJnt, endJnt = jntIK
    # Rig - firstJoint
    ikH = pm.ikHandle(sj=firstJnt, ee=endJnt, sol="ikRPsolver")[0]
    pm.rotate(ccCircle, [0, 0, 90])
    pm.makeIdentity(ccCircle, a=True, t=0, r=1, s=0, jo=0, n=0, pn=1)
    pm.matchTransform(ccCircle, firstJnt, pos=True)
    pm.pointConstraint(ccCircle, firstJnt, mo=True)
    # Rig - middleJoint
    polevectorJoints = createPolevectorJoint([firstJnt, middleJnt, endJnt])
    startJointOfPolevector, endJointOfPolevector = polevectorJoints
    pm.matchTransform(ccSphere, endJointOfPolevector, pos=True)
    pm.delete(startJointOfPolevector)
    pm.poleVectorConstraint(ccSphere, ikH, w=1)
    # Rig - endJoint
    pm.matchTransform(ccCube, endJnt, pos=True)
    pm.orientConstraint(endJnt, ccCube, o=(-90, 0, 90), w=1)
    pm.delete(ccCube, cn=True)
    pm.orientConstraint(ccCube, endJnt, mo=True, w=1)
    # Rig - cleanUp
    ccNamesGroup = groupingWithOwnPivot(*ccNames)
    armGroupName = ccCircle.rsplit("_", 1)[0]
    pm.group(em=True, n=armGroupName)
    for i in ccNamesGroup:
        pm.parent(i, armGroupName)
    pm.setAttr(f"{ikH}.visibility", 0)
    pm.parent(ikH, ccCube)


jntFK = [
    "rig_L_Upperarm_FK", 
    "rig_L_Forearm_FK", 
    "rig_L_Hand_FK"
    ]
ctrlLeftFK = {
    "cc_LeftArm_FK": 11, 
    "cc_LeftForeArm_FK": 9, 
    "cc_LeftHand_FK": 7, 
}
for ccName, size in ctrlLeftFK.items():
    pm.circle(ch=False, r=size, nr=(1, 0, 0), n=ccName)


    

