from hjk import *


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
    return ccGrp


def createWheelLocator(ctrlName: str) -> str:
    """ Create a rotation locator that turns a wheel.

    Examples: 
    >>> createWheelLocator("cc_wheelLeftFront")
    >>> loc_wheelLeftFront
     """
    ctrlSub = f"{ctrlName}_sub"
    if "cc_" in ctrlName:
        locName = ctrlName.replace("cc_", "loc_")
    else:
        locName = f"{ctrlName}_exprLocator"
    if pm.objExists(locName):
        return locName
    else:
        locator = pm.spaceLocator(n=locName)
        pm.matchTransform(locator, ctrlSub, pos=True)
        pm.parent(locator, ctrlSub)
        pm.makeIdentity(locator, a=1, t=1, r=0, s=0, n=0, pn=1)
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


def createWheelExpression(ctrlName: str, locator: str, groupNames: list):
    """ Rotate the locator by the moving distance of offset_grp. """
    ctrlMain = f"{ctrlName}_main"
    if not pm.attributeQuery("AutoRoll", node=ctrlMain, ex=True):
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrlMain, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrlMain}.{attrAuto}', e=True, k=True)
    br = '\n'
    offset = groupNames[1]
    previous, orient = groupNames[3:]
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


def buildWheel():
    ctrlName = "cc_wheelLeftFront"
    sel = pm.selected()[0]
    ctrls = createWheelCtrl(ctrlName, sel)
    locator = createWheelLocator(ctrlName)
    exprGroups = createWheelExpressionGroups(ctrlName)
    createWheelExpression(ctrlName, locator, exprGroups)
    pm.parent(ctrls[0], w=True)
    pm.delete(ctrls[0], cn=True)
    pm.parent(ctrls[0], exprGroups[1])
    pm.parentConstraint(locator, sel, mo=True, w=1.0)


def createDoorCtrl(doorName: str, obj: str) -> list:
    """ Create a door controller to rotate the mirror.
    The door on the right is created automatically. 
    The shapes of the front and back doors are different.
     """
    Back = "Back" in doorName
    back = "back" in doorName
    if any([Back, back]):
        doorType = "door2"
    else:
        doorType = "door"
    cc = Controllers()
    ctrls = cc.createControllers(**{doorType: doorName})
    ctrl = ctrls[0]
    defaultScale = 58
    doorSize = max(getBoundingBoxSize(obj)) / defaultScale
    pm.scale(ctrl, [doorSize, doorSize, doorSize])
    pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
    pm.matchTransform(ctrl, obj, pos=True, rot=True)
    doorAGrp, doorA = groupOwnPivot(ctrl, null=True)[::2]
    doorBGrp, doorB = mirrorCopy(ctrl)[::2]
    result = [doorAGrp, doorA, doorBGrp, doorB]
    for i in result[1::2]:
        pm.transformLimits(i, ry=(-60, 0), ery=(False, True))
    return result


def builddoor():
    doorName = "cc_doorLeftFront"
    sel = pm.selected()[0]
    createDoorCtrl(doorName, sel)
