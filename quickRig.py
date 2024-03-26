from general import pm, parentHierarchically, getBoundingBoxSize, \
    getFlattenList, RigGroups, Controllers, groupingWithOwnPivot
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

