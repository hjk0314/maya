from hjk import *



class QuickRig_Car:
    def __init__(self):
        self.topGroup = "vhcl_bestaB_mdl_v9999:bestaB"
        self.bodyGroup = "vhcl_bestaB_mdl_v9999:bestaB_body_grp"
        self.doorGroup = [
            "vhcl_bestaB_mdl_v9999:bestaB_body_door_Ft_L_grp", 
            "", 
            "vhcl_bestaB_mdl_v9999:bestaB_body_door_Ft_R_grp", 
            ""
            ]
        self.doorName = [
            "cc_doorLeftFront", 
            "cc_doorLeftBack", 
            "cc_doorRightFront", 
            "cc_doorRightBack"
            ]
        self.wheelGroup = [
            "vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_L_grp", 
            "vhcl_bestaB_mdl_v9999:bestaB_wheel_Bk_L_grp", 
            "vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_R_grp", 
            "vhcl_bestaB_mdl_v9999:bestaB_wheel_Bk_R_grp"
            ]
        self.wheelName = [
            "cc_wheelLeftFront", 
            "cc_wheelLeftBack", 
            "cc_wheelRightFront", 
            "cc_wheelRightBack"
            ]
        self.colorBar = {
            "cc_main": "yellow", 
            "cc_sub": "pink", 
            "cc_body": "yellow", 
            "cc_doorLeftFront": "red", 
            "cc_doorLeftBack": "red", 
            "cc_doorRightFront": "blue", 
            "cc_doorRightBack": "blue", 
            "cc_wheelLeftFront_upDownMain": "yellow", 
            "cc_wheelLeftFront_upDownSub": "pink", 
            "cc_wheelLeftFront_main": "red", 
            "cc_wheelLeftFront_sub": "red2", 
            "cc_wheelLeftBack_upDownMain": "yellow", 
            "cc_wheelLeftBack_upDownSub": "pink", 
            "cc_wheelLeftBack_main": "red", 
            "cc_wheelLeftBack_sub": "red2", 
            "cc_wheelRightFront_upDownMain": "yellow", 
            "cc_wheelRightFront_upDownSub": "pink", 
            "cc_wheelRightFront_main": "blue", 
            "cc_wheelRightFront_sub": "blue2", 
            "cc_wheelRightBack_upDownMain": "yellow", 
            "cc_wheelRightBack_upDownSub": "pink", 
            "cc_wheelRightBack_main": "blue", 
            "cc_wheelRightBack_sub": "blue2", 
            }
        self.locators = []


    def run(self):
        self.createGlobalCtrl(self.topGroup)
        self.createBodyCtrl(self.bodyGroup)
        self.buildDoorCtrl()


    def createGlobalCtrl(self, objectGroup: str) -> list:
        """ Create a global controller. 
        Take the Arguments that can be used to estimate 
        the overall size of the model.

        Examples: 
        >>> createGlobalCtrl("vhcl_bestaB_mdl_v9999:bestaB_body_grp")
        >>> ["cc_main_grp", "cc_main", "cc_sub_grp", "cc_sub"]
        """
        ccMain = "cc_main"
        ccSub = "cc_sub"
        if pm.objExists(ccMain) or pm.objExists(ccSub):
            pm.warning("Controllers Aleady exists.")
            return
        a, b, c = getBoundingBoxSize(objectGroup)
        x, y, z = 100, 100, 250
        cc = Controllers()
        ccs = cc.createControllers(car3=ccMain, car2=ccSub)
        for i in ccs:
            pm.scale(i, [a/x, b/y, c/z])
            pm.makeIdentity(i, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccsGroup = groupOwnPivot(*ccs)
        result = parentHierarchically(*ccsGroup)
        locator = createSubLocator(ccs[-1])
        result.append(locator)
        pm.parentConstraint(ccSub, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(ccSub, objectGroup, mo=True, w=1.0)
        return result


    def createBodyCtrl(self, objectGroup: str) -> list:
        """ Create the Body Controller. 
        Take the Arguments that can be used to estimate 
        the overall size of the body.

        Examples: 
        >>> createBodyCtrl("body")
        >>> ['cc_body_grp', 'cc_body_null', 'cc_body', 'loc_body']
        """
        ccBody = "cc_body"
        if pm.objExists(ccBody):
            pm.warning(f"{ccBody} Aleady exists.")
            return
        defaultScale = 240
        bodySize = max(getBoundingBoxSize(objectGroup)) / defaultScale
        cc = Controllers()
        ctrl = cc.createControllers(car=ccBody)
        pm.scale(ctrl, [bodySize, bodySize, bodySize])
        pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.matchTransform(ctrl, objectGroup, pos=True, rot=True)
        bodyGroups = groupOwnPivot(ctrl[0], null=True)
        locator = createSubLocator(ctrl[0])
        bodyGroups.append(locator)
        pm.parentConstraint(locator, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(locator, objectGroup, mo=True, w=1.0)
        return bodyGroups


    def createDoorCtrl(self, objectGroup: str, doorName: str):
        """ Create a door controller. 
        - When the doorName contains the word "Right", "right", "_R", 
            - set the group's rotateX to -180 in the YZ plane.
        - When the doorName contains the word "Back", "back", "Bk",
            - the door controller shape changes to door2 type.

        Examples: 
        >>> createDoorCtrl("bestaB_body_door_Ft_L_grp", "cc_door_L_Ft")
        >>> ["cc_door_L_Ft_grp", ..., "cc_door_L_Ft", "loc_door_L_Ft"]
        >>> createDoorCtrl("bestaB_body_door_Ft_L_grp", "cc_door_R_Bk")
        >>> ["cc_door_R_Bk_grp", ..., "cc_door_R_Bk", "loc_door_R_Bk"]
        """
        defaultScale = 58
        Back = "Back" in doorName
        back = "back" in doorName
        Bk = "Bk" in doorName
        Right = "Right" in doorName
        right = "right" in doorName
        _R = "_R" in doorName
        _rt = "_rt" in doorName
        doorType = "door2" if any([Back, back, Bk]) else "door"
        ctrls = Controllers().createControllers(**{doorType: doorName})
        ctrl = ctrls[0]
        doorSize = max(getBoundingBoxSize(objectGroup)) / defaultScale
        pm.scale(ctrl, [doorSize, doorSize, doorSize])
        pm.matchTransform(ctrl, objectGroup, pos=True, rot=True)
        doorGroup = groupOwnPivot(ctrl, null=True)
        if any([Right, right, _R, _rt]):
            pm.setAttr(f"{ctrl}.rotateX", -180)
            pm.setAttr(f"{doorGroup[0]}.rotateX", -180)
        pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
        loc = createSubLocator(doorGroup[-1])
        doorGroup.append(loc)
        pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
        pm.parentConstraint(loc, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(loc, objectGroup, mo=True, w=1.0)
        return doorGroup


    def createWheelCtrl(self, ctrlName: str, obj: str) -> list:
        """ Create a wheel controller.

        Examples: 
        >>> createWheelCtrl("cc_wheelLeftFront", "pCylinder")
        >>> ['cc_wheelLeftFront_upDownMain_grp', ...]
        """
        ctrls = [
            f"{ctrlName}_upDownMain", 
            f"{ctrlName}_upDownSub", 
            f"{ctrlName}_main", 
            f"{ctrlName}_sub"
        ]
        sizeRatio = [14, 18, 9, 11]
        cc = Controllers()
        rad = max(getBoundingBoxSize(obj))
        for ctrlName, sr in zip(ctrls[:2], sizeRatio[:2]):
            cuv = cc.createControllers(square=ctrlName)[0]
            pm.scale(cuv, (rad/(sr*2), rad/sr, rad/sr))
            pm.matchTransform(cuv, obj, pos=True)
            pm.setAttr(f"{cuv}.translateY", 0)
        for ctrlName, sr in zip(ctrls[2:], sizeRatio[2:]):
            cuv = cc.createControllers(circle=ctrlName)[0]
            pm.scale(cuv, (rad/sr, rad/sr, rad/sr))
            pm.rotate(cuv, (0, 0, 90))
            pm.matchTransform(cuv, obj, pos=True)
        ccGrp = groupOwnPivot(*ctrls, null=True)
        parentHierarchically(*ccGrp)
        pm.makeIdentity(ccGrp, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccMain = ctrls[2]
        pm.addAttr(ccMain, ln="Radius", at="double", min=0.0001, dv=1)
        pm.setAttr(f"{ccMain}.Radius", e=True, k=True)
        pm.setAttr(f"{ccMain}.Radius", rad)
        locator = createSubLocator(ctrls[-1])
        ccGrp.append(locator)
        return ccGrp


    def createWheelExpressionGroups(self, ctrlName: str) -> list:
        """ Create groups for the expression. """
        grpNames = [
            f"{ctrlName}_grp", 
            f"{ctrlName}_offset", 
            f"{ctrlName}_offsetNull", 
            f"{ctrlName}_offsetPrevious", 
            f"{ctrlName}_offsetOrient"
            ]
        result = [pm.group(n=i, em=True) for i in grpNames]
        grp, offset, offsetNull, offsetPrevious, offsetOrient = result
        pm.parent(offset, grp)
        pm.parent(offsetNull, offset)
        pm.parent(offsetPrevious, grp)
        pm.parent(offsetOrient, offsetPrevious)
        offsetOrient.translate.set([-0.001, -0.001, -0.001])
        pm.aimConstraint(offset, offsetPrevious, mo=False)
        pm.orientConstraint(offsetNull, offsetOrient, mo=False)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PreviousPosition{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PreviousPosition{i}', e=True, k=True)
        return result


    def createWheelExpression(self, wheelGroups: list) -> list:
        """ Rotate the locator by the moving distance of offset_grp.

        Args: 
        >>> wheelGroups = [
            'cc_wheelLeftFront_upDownMain_grp', 
            'cc_wheelLeftFront_upDownMain_null', 
            'cc_wheelLeftFront_upDownMain', 
            'cc_wheelLeftFront_upDownSub_grp', 
            'cc_wheelLeftFront_upDownSub_null', 
            'cc_wheelLeftFront_upDownSub', 
            'cc_wheelLeftFront_main_grp', 
            'cc_wheelLeftFront_main_null', 
            'cc_wheelLeftFront_main', 
            'cc_wheelLeftFront_sub_grp', 
            'cc_wheelLeftFront_sub_null', 
            'cc_wheelLeftFront_sub', 
            'loc_wheelLeftFront_sub', 
            ]
        """
        firstGroup = wheelGroups[0]
        ctrlMain = wheelGroups[8]
        ctrlName = ctrlMain.rsplit("_", 1)[0]
        locator = wheelGroups[-1]
        if not pm.attributeQuery("AutoRoll", node=ctrlMain, ex=True):
            attrAuto = 'AutoRoll'
            pm.addAttr(ctrlMain, ln=attrAuto, at='long', min=0, max=1, dv=1)
            pm.setAttr(f'{ctrlMain}.{attrAuto}', e=True, k=True)
        br = '\n'
        groupNames = self.createWheelExpressionGroups(ctrlName)
        offset = groupNames[1]
        previous, orient = groupNames[3:]
        pm.parent(firstGroup, offset)
        # expression1
        expr1 = f'float $rad = {ctrlMain}.Radius;{br}'
        expr1 += f'float $auto = {ctrlMain}.AutoRoll;{br}'
        expr1 += f'float $locator = {locator}.rotateX;{br}'
        expr1 += f'float $circleLength = 2 * 3.141 * $rad;{br}'
        expr1 += f'float $orientRotY = {orient}.rotateY;{br}'
        expr1 += f'float $offsetScale = {offset}.scaleY;{br}'
        expr1 += f'float $pointX1 = {offset}.PreviousPositionX;{br}'
        expr1 += f'float $pointY1 = {offset}.PreviousPositionY;{br}'
        expr1 += f'float $pointZ1 = {offset}.PreviousPositionZ;{br}'
        expr1 += f'{previous}.translateX = $pointX1;{br}'
        expr1 += f'{previous}.translateY = $pointY1;{br}'
        expr1 += f'{previous}.translateZ = $pointZ1;{br}'
        expr1 += f'float $pointX2 = {offset}.translateX;{br}'
        expr1 += f'float $pointY2 = {offset}.translateY;{br}'
        expr1 += f'float $pointZ2 = {offset}.translateZ;{br*2}'
        # expression2
        pointsGap = '$pointX2-$pointX1, $pointY2-$pointY1, $pointZ2-$pointZ1'
        expr2 = f'float $distance = `mag<<{pointsGap}>>`;{br*2}'
        # expression3
        expr3 = f'{locator}.rotateX = $locator'
        expr3 += ' + ($distance/$circleLength) * 360'
        expr3 += ' * $auto'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($orientRotY))'
        expr3 += f' / $offsetScale;{br*2}'
        # expression4
        expr4 = f'{offset}.PreviousPositionX = $pointX2;{br}'
        expr4 += f'{offset}.PreviousPositionY = $pointY2;{br}'
        expr4 += f'{offset}.PreviousPositionZ = $pointZ2;{br}'
        # final expression
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')
        return groupNames


    def buildDoorCtrl(self) -> list:
        result = []
        for grp, dn in zip(self.doorGroup, self.doorName):
            if not grp or pm.objExists(dn):
                continue
            else:
                doorGroup = self.createDoorCtrl(grp, dn)
                result += doorGroup
        return result



