from hjk import *


topGroup = "vhcl_bestaB_mdl_v9999:bestaB"
bodyGroup = "vhcl_bestaB_mdl_v9999:bestaB_body_grp"
doorGroup = [
    "vhcl_bestaB_mdl_v9999:bestaB_body_door_Ft_L_grp", 
    "", 
    "vhcl_bestaB_mdl_v9999:bestaB_body_door_Ft_R_grp", 
    ""
    ]
doorName = [
    "cc_doorLeftFront", 
    "cc_doorLeftBack", 
    "cc_doorRightFront", 
    "cc_doorRightBack"
    ]
wheelGroup = [
    "vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_L_grp", 
    "vhcl_bestaB_mdl_v9999:bestaB_wheel_Bk_L_grp", 
    "vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_R_grp", 
    "vhcl_bestaB_mdl_v9999:bestaB_wheel_Bk_R_grp"
    ]
wheelName = [
    "cc_wheelLeftFront", 
    "cc_wheelLeftBack", 
    "cc_wheelRightFront", 
    "cc_wheelRightBack"
    ]
colorBar = {
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
locators = []


# Source
def createSubLocator(ctrlName: str) -> str:
    """ Create a rotation locator that turns a wheel.

    Examples: 
    >>> createWheelLocator("cc_wheelLeftFront_sub")
    >>> loc_wheelLeftFront_sub
     """
    ctrlName = ctrlName.name() if isinstance(ctrlName, pm.PyNode) else ctrlName
    if "cc_" in ctrlName:
        locName = ctrlName.replace("cc_", "loc_")
    else:
        locName = f"{ctrlName}_exprLocator"
    if pm.objExists(locName):
        return locName
    else:
        locator = pm.spaceLocator(n=locName)
        pm.matchTransform(locator, ctrlName, pos=True)
        pm.parent(locator, ctrlName)
        pm.makeIdentity(locator, a=1, t=1, r=1, s=1, n=0, pn=1)
        return locator


def createWheelExpressionGroups(ctrlName: str) -> list:
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


def getTopGroup(*args) -> str:
    """ Get the top group containing arguments such as 'body' 
    among the subgroups of the selected group.

    Examples: 
    >>> getTopGroup("wheel", "_L", "_Ft")
    >>> "vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_L_grp"
     """
    sel = selectGroupOnly(topGroup)
    pm.select(cl=True)
    groups = [i for i in sel if all([arg in i.name() for arg in args])]
    for grp in groups:
        if not any(j in groups for j in grp.listRelatives(p=True)):
            pm.select(grp)
            return grp
    return


# Process
def createWheelCtrl(ctrlName: str, obj: str) -> list:
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


def createWheelExpression(wheelGroups: list) -> list:
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
    groupNames = createWheelExpressionGroups(ctrlName)
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


def createDoorCtrl(doorGroup, doorName) -> list:
    """ Create a door controller to rotate the mirror.
    The door on the right is created automatically. 
    The shapes of the front and back doors are different.

    Examples: 
    >>> createDoorCtrl("cc_doorLeftFront", "car_doorLeftFront_grp")
    >>> ["cc_doorLeftFront_grp", ..., "cc_doorRightFront", "loc_doorLeftFront"]
    >>> createDoorCtrl("cc_doorLeftBack", "car_doorLeftBack_grp")
    >>> ["cc_doorLeftBack_grp", ..., "cc_doorRightBack", "loc_doorLeftBack"]
     """
    result = []
    for grp, dn in zip(doorGroup, doorName):
        if not grp:
            continue
        cc = Controllers()
        defaultScale = 58
        if "cc_doorLeftFront" == dn:
            ctrls = cc.createControllers(**{"door": dn})
            ctrl = ctrls[0]
            doorSize = max(getBoundingBoxSize(grp)) / defaultScale
            pm.scale(ctrl, [doorSize, doorSize, doorSize])
            pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            pm.matchTransform(ctrl, grp, pos=True, rot=True)
            doorGroup = groupOwnPivot(ctrl, null=True)
            loc = createSubLocator(doorGroup[-1])
            doorGroup.append(loc)
            result += doorGroup
            pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
            pm.parentConstraint(loc, grp, mo=True, w=1.0)
            pm.scaleConstraint(loc, grp, mo=True, w=1.0)
        if "cc_doorLeftBack" == dn:
            ctrls = cc.createControllers(**{"door2": dn})
            ctrl = ctrls[0]
            doorSize = max(getBoundingBoxSize(grp)) / defaultScale
            pm.scale(ctrl, [doorSize, doorSize, doorSize])
            pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            pm.matchTransform(ctrl, grp, pos=True, rot=True)
            doorGroup = groupOwnPivot(ctrl, null=True)
            loc = createSubLocator(doorGroup[-1])
            doorGroup.append(loc)
            result += doorGroup
            pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
            pm.parentConstraint(loc, grp, mo=True, w=1.0)
            pm.scaleConstraint(loc, grp, mo=True, w=1.0)
        if "cc_doorRightFront" == dn:
            ctrls = cc.createControllers(**{"door": dn})
            ctrl = ctrls[0]
            doorSize = max(getBoundingBoxSize(grp)) / defaultScale
            pm.scale(ctrl, [doorSize, doorSize, doorSize])
            # pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            pm.matchTransform(ctrl, grp, pos=True, rot=True)
            doorGroup = groupOwnPivot(ctrl, null=True)
            pm.setAttr(f"{ctrl}.rotateX", -180)
            pm.setAttr(f"{doorGroup[0]}.rotateX", -180)
            pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            loc = createSubLocator(doorGroup[-1])
            doorGroup.append(loc)
            result += doorGroup
            pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
            pm.parentConstraint(loc, grp, mo=True, w=1.0)
            pm.scaleConstraint(loc, grp, mo=True, w=1.0)
        if "cc_doorRightBack" == dn:
            ctrls = cc.createControllers(**{"door2": dn})
            ctrl = ctrls[0]
            doorSize = max(getBoundingBoxSize(grp)) / defaultScale
            pm.scale(ctrl, [doorSize, doorSize, doorSize])
            # pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            pm.matchTransform(ctrl, grp, pos=True, rot=True)
            doorGroup = groupOwnPivot(ctrl, null=True)
            pm.setAttr(f"{ctrl}.rotateX", -180)
            pm.setAttr(f"{doorGroup[0]}.rotateX", -180)
            pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
            loc = createSubLocator(doorGroup[-1])
            doorGroup.append(loc)
            result += doorGroup
            pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
            pm.parentConstraint(loc, grp, mo=True, w=1.0)
            pm.scaleConstraint(loc, grp, mo=True, w=1.0)
    return result


    # Back = "Back" in doorName
    # back = "back" in doorName
    # if any([Back, back]):
    #     doorType = "door2"
    # else:
    #     doorType = "door"
    # cc = Controllers()
    # ctrls = cc.createControllers(**{doorType: doorName})
    # ctrl = ctrls[0]
    # defaultScale = 58
    # doorSize = max(getBoundingBoxSize(objectGroup)) / defaultScale
    # pm.scale(ctrl, [doorSize, doorSize, doorSize])
    # pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
    # pm.matchTransform(ctrl, objectGroup, pos=True, rot=True)
    # doorAGroups = groupOwnPivot(ctrl, null=True)
    # doorBGroups = mirrorCopy(ctrl)
    # locA = createSubLocator(doorAGroups[-1])
    # doorAGroups.append(locA)
    # locB = createSubLocator(doorBGroups[-1])
    # doorBGroups.append(locB)
    # result = doorAGroups + doorBGroups
    # for i in result[2::4]:
    #     pm.transformLimits(i, ry=(-60, 0), ery=(False, True))
    # return result


def createBodyCtrl(objectGroup: str) -> list:
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
    

def createGlobalCtrl(objectGroup: str) -> list:
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
    pm.parentConstraint(ccSub, objectGroup, mo=True, w=1.0)
    pm.scaleConstraint(ccSub, objectGroup, mo=True, w=1.0)
    return result



# wheelCtrlGroup = []
# locators = []
# for cc, obj, chk in zip(ccs, sel, bools):
#     wheelGroups = createWheelCtrl(cc, obj)
#     if chk:
#         tmp = createWheelExpression(wheelGroups)
#         wheelCtrlGroup.append(tmp[0])
#     else:
#         wheelCtrlGroup.append(wheelGroups[0])
#         continue
#     locators.append(wheelGroups[-1])
# try:
#     pm.parent(wheelCtrlGroup, "cc_wheel_grp")
# except:
#     pm.group(wheelCtrlGroup, n="cc_wheel_grp")



# createBodyCtrl(bodyGroup)


# createGlobalCtrl(topGroup)


# createDoorCtrl(doorGroup, doorName)


# createRigGroups("bestaB")


