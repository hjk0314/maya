from collections.abc import Iterable 
import sympy
import numpy as np
import pymel.core as pm


def getPosition(selection: str) -> list:
    """ Get the coordinates of an object or point.
    >>> getPosition("pSphere1")
    >>> getPosition("pSphere1.vtx[317]")
    >>> [0.0, 0.0, 0.0]
     """
    try:
        position = pm.pointPosition(selection)
    except:
        position = pm.xform(selection, q=1, ws=1, rp=1)
    return position


def getNameAndPosition(selections: list) -> dict:
    """ Returns the dictionary of names and positions. """
    nameAndPosition = {}
    for i in selections:
        position = pm.xform(i, q=True, ws=True, rp=True)
        nameAndPosition[i] = position
    return nameAndPosition


def getBoundingBoxPosition(vertexOrObject) -> list:
    boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    return [x, y, z]


def getFlattenList(*args):
    """ Flattens a list within a list. 
    >>> args = (["ab", ["bc"], ["ef"]], [[["gh", ], "ij"], "jk"],)
    >>> return ['ab', 'bc', 'ef', 'gh', 'ij', 'jk']
     """
    result = []
    for arg in args:
        if not isinstance(arg, str) and isinstance(arg, Iterable):
            for i in arg:
                result.extend(getFlattenList(i))
        else:
            result.append(arg)
    return result


def createLocators(positions: list=[]) -> list:
    """ The positions are like [(0,0,0), (1,1,1), (1,2,3), ...] """
    result = []
    if not positions:
        positions = [getPosition(i) for i in pm.selected(fl=True)]
    for i in positions:
        locator = pm.spaceLocator()
        pm.move(locator, i)
        result.append(locator)
    return result


def createJoints(jointsInfo) -> list:
    """ Create joints or Create joints and name it.
    >>> createJoints([[0,0,0], [1,2,3], ...])
    >>> createJoints({"firstJoint": [0,0,0], "secondJoint": [1,2,3], ...})
    >>> return [created joints]
     """
    pm.select(cl=True)
    if isinstance(jointsInfo, list):
        result = [pm.joint(p=position) for position in jointsInfo]
    elif isinstance(jointsInfo, dict):
        result = []
        for jointName, position in jointsInfo.items():
            jnt = pm.joint(p=position, n=jointName) 
            result.append(jnt)
    else:
        result = []
    return result


def orientJoints(joints=[], primaryAxis='yzx', secondaryAxis='zup'):
    """ The default value of primaryAxis and secondaryAxis are 
    the same as Mixamo spine. """
    if joints:
        allJoints = [pm.PyNode(i) for i in joints]
    else:
        allJoints = pm.ls(sl=True)
    endJoints = [i for i in allJoints if not i.getChildren()]
    initJoint = allJoints[0]
    pm.makeIdentity(allJoints, a=True, jo=True, n=0)
    pm.joint(initJoint, 
            e=True, # edit
            oj=primaryAxis, # orientJoint
            sao=secondaryAxis, # secondaryAxisOrient
            ch=True, # children
            zso=True, # zeroScaleOrient
        )
    for i in endJoints:
        pm.joint(i, e=True, oj='none', ch=True, zso=True)


def makeSameAsParentPivot(object, parents) -> None:
    """ If you put object under parents and freeze it, 
    the pivots match together. """
    parentsPivot = pm.xform(parents, q=1, ws=1, rp=1)
    pm.xform(object, sp=parentsPivot, rp=parentsPivot)
    pm.parent(object, parents)
    pm.makeIdentity(object, a=1, t=1, r=1, s=1, n=0, pn=1)
    pm.parent(object, w=True)


def setPoleDirection(object, aimJoint, upVectorJoint):
    """ This Function mainly used 
    when determining poleVector's direction """
    pm.aimConstraint(aimJoint, object, o=(0,0,90), wut='object', 
                     wuo=upVectorJoint)
    pm.delete(object, cn=True)


def removeDeformed():
    """ Remove Deformed from all objects including the text Deformed. """
    removeStr = "Deformed"
    nullStr = ""
    nodes = pm.ls("*{}*".format(removeStr), r=True)
    for node in nodes:
        new_name = node.name().replace(removeStr, nullStr)
        node.rename(new_name)


class Curves:
    def __init__(self):
        pass


    def createCurvePassingKeyedUp(self, startFrame, endFrame, objects=[]):
        selections = objects if objects else pm.ls(sl=True)
        curves = []
        for i in selections:
            positions = []
            for frame in range(startFrame, endFrame + 1):
                pm.currentTime(frame)
                xyz = getPosition(i)
                positions.append(xyz)
            cuv = pm.curve(p=positions, d=3)
            curves.append(cuv)
        return curves


    def createCurvePassingPoints(self, objects=[]):
        selections = objects if objects else pm.ls(sl=True, fl=True)
        positions = [getPosition(i) for i in selections]
        curve = pm.curve(ep=positions, d=3)
        return curve


    def createCurvePassingLocators(self, curveClosed=False) -> str:
        """ The closedCurve means that 
        the start and end points of a curve are connected.
        >>> createCurvePassingLocators()
        >>> createCurvePassingLocators(curveClosed=True)
        >>> return curveName
         """
        locators = pm.ls(sl=True, fl=True)
        positions = [getPosition(i) for i in locators]
        result = ""
        if not curveClosed:
            result = pm.curve(ep=positions, d=3)
        else:
            circle = pm.circle(nr=(0, 1, 0), ch=False, s=len(locators))
            result = circle[0]
            for i, xyz in enumerate(positions):
                pm.move(f"{result}.cv[{i}]", xyz, ws=True)
        return result


    def createCurveAimingPoint(self):
        """ Select two objects or points.
        A straight line is created looking at the first point.
         """
        sel = pm.ls(sl=True)
        first = sel[0]
        last = sel[-1]
        positions = [getPosition(i) for i in [first, last]]
        simpleCurve = self.createCurveOnlyTwoPoints(positions)
        startLocator, endLocator = createLocators(positions)
        pm.aimConstraint(endLocator, startLocator)
        pm.delete(startLocator, cn=True)
        makeSameAsParentPivot(simpleCurve, startLocator)
        pm.rebuildCurve(simpleCurve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)


    def createCurvesNormalDirection(self) -> list:
        selections = pm.ls(sl=True, fl=True)
        result = []
        for i in selections:
            vertexPosition = pm.pointPosition(i)
            normalPosition = pm.polyNormalPerVertex(i, q=True, normalXYZ=True)[0:3]
            twoPositions = [(0,0,0), normalPosition]
            curve = self.createCurveOnlyTwoPoints(twoPositions)
            startLocator, endLocator = createLocators(twoPositions)
            pm.aimConstraint(endLocator, startLocator)
            pm.delete(startLocator, constraints=True)
            makeSameAsParentPivot(curve, startLocator)
            pm.rebuildCurve(curve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
            pm.move(curve, vertexPosition)
            pm.delete([startLocator, endLocator])
            result.append(curve)
        return result


    def createCurveOnlyTwoPoints(self, positions: list=[]) -> str:
        """ The positions are like [(0,0,0), (1,1,1), (1,2,3), ...] """
        if not positions:
            positions = [getPosition(i) for i in pm.ls(sl=True, fl=True)]
        try:
            startPoint = positions[0]
            endPoint = positions[-1]
            simpleLine = pm.curve(p=[startPoint, endPoint], d=1)
            return simpleLine
        except:
            return


class Controllers:
    def __init__(self):
        self.controllerShapes = {
            "arrow": [
                (0, 0, 8), (8, 0, 4), (4, 0, 4), (4, 0, -8), 
                (-4, 0, -8), (-4, 0, 4), (-8, 0, 4), (0, 0, 8)
                ], 
            "arrow2": [
                (0, 3, 12), (12, 3, 6), (6, 3, 6), (6, 3, -12), 
                (-6, 3, -12), (-6, 3, 6), (-12, 3, 6), (0, 3, 12), 
                (0, -3, 12), (12, -3, 6), (6, -3, 6), (6, -3, -12), 
                (-6, -3, -12), (-6, -3, 6), (-12, -3, 6), (0, -3, 12), 
                (12, -3, 6), (12, 3, 6), (6, 3, 6), (6, 3, -12), 
                (6, -3, -12), (-6, -3, -12), (-6, 3, -12), (-6, 3, 6), 
                (-12, 3, 6), (-12, -3, 6)
                ], 
            "arrow3": [
                (14, 0, 0), (10, 0, -10), (0, 0, -14), (-10, 0, -10), 
                (-14, 0, 0), (-10, 0, 10), (0, 0, 14), (10, 0, 10), 
                (14, 0, 0), (10, 0, 4), (14, 0, 6), (14, 0, 0)
                ], 
            "arrow4": [
                (0, 0, -23.1), (-6.3, 0, -16.8), (-4.2, 0, -16.8), 
                (-4.2, 0, -12.6), (-10.5, 0, -10.5), (-12.6, 0, -4.2), 
                (-16.8, 0, -4.2), (-16.8, 0, -6.3), (-23.1, 0, 0), 
                (-16.8, 0, 6.3), (-16.8, 0, 4.2), (-12.6, 0, 4.2), 
                (-10.5, 0, 10.5), (-4.2, 0, 12.6), (-4.2, 0, 16.8), 
                (-6.3, 0, 16.8), (0, 0, 23.1), (6.3, 0, 16.8), 
                (4.2, 0, 16.8), (4.2, 0, 12.6), (10.5, 0, 10.5), 
                (12.6, 0, 4.2), (16.8, 0, 4.2), (16.8, 0, 6.3), 
                (23.1, 0, 0), (16.8, 0, -6.3), (16.8, 0, -4.2), 
                (12.6, 0, -4.2), (10.5, 0, -10.5), (4.2, 0, -12.6), 
                (4.2, 0, -16.8), (6.3, 0, -16.8), (0, 0, -23.1)
                ], 
            "arrow5": [
                (-8, 0, -4), (8, 0, -4), (8, 0, -8), (16, 0, 0), 
                (8, 0, 8), (8, 0, 4), (-8, 0, 4), (-8, 0, 8), 
                (-16, 0, 0), (-8, 0, -8), (-8, 0, -4)
                ], 
            "arrow6": [
                (-0, 0, -12.6), (-0, 4, -13), (-0, 2, -10), 
                (-0, 0, -12.6), (-0, 2, -12), (-0, 6, -10), 
                (-0, 10, -6), (0, 12, 0), (0, 10, 6), (0, 6, 10), 
                (0, 2, 12), (0, 0, 12.6), (0, 2, 10), (0, 4, 13), 
                (0, 0, 12.6)
                ], 
            "car": [
                (81, 70, 119), (89, 56, 251), (89, -12, 251), 
                (89, -12, 117), (89, -12, -117), (89, -12, -229), 
                (81, 70, -229), (81, 70, -159), (69, 111, -105), 
                (69, 111, 63), (81, 70, 119), (-81, 70, 119), 
                (-89, 56, 251), (-89, -12, 251), (-89, -12, 117), 
                (-89, -12, -117), (-89, -12, -229), (-81, 70, -229), 
                (-81, 70, -159), (-69, 111, -105), (69, 111, -105), 
                (81, 70, -159), (-81, 70, -159), (-81, 70, -229), 
                (81, 70, -229), (89, -12, -229), (-89, -12, -229), 
                (-89, -12, -117), (-89, -12, 117), (-89, -12, 251), 
                (89, -12, 251), (89, 56, 251), (-89, 56, 251), 
                (-81, 70, 119), (-69, 111, 63), (-69, 111, -105), 
                (69, 111, -105), (69, 111, 63), (-69, 111, 63)
                ], 
            "car2": [
                (165, 0, -195), (0, 0, -276), (-165, 0, -195), (-97, 0, -0), 
                (-165, -0, 195), (-0, -0, 276), (165, -0, 195), (97, -0, 0), 
                (165, 0, -195)
                ], 
            "car3": [
                (212, 0, -212), (0, 0, -300), (-212, 0, -212), (-300, 0, 0), 
                (-212, 0, 212), (0, 0, 300), (212, 0, 212), (300, 0, 0), 
                (212, 0, -212)
                ], 
            "circle": [
                (0, 0, -15), (-10, 0, -10), (-15, 0, 0), 
                (-10, 0, 10), (0, 0, 15), (10, 0, 10), 
                (15, 0, 0), (10, 0, -10), (0, 0, -15)
                ], 
            "cone": [
                (0, 10, 0), (-4.35, 0, 0), (4.35, 0, 0), (0, 10, 0), 
                (0, 0, 5), (-4.35, 0, 0), (4.35, 0, 0), (0, 0, 5)
                ], 
            "cone2": [
                (-5, 0, 0), (0, 0, 5), (5, 0, 0), (0, 0, -5), 
                (0, 10, 0), (-5, 0, 0), (0, 10, 0), (0, 0, 5), 
                (5, 0, 0), (0, 0, -5), (0, 0, -5), (-5, 0, 0), 
                (0, 0, 5), (5, 0, 0), (0, 10, 0)
                ], 
            "cube": [
                (-5, 5, -5), (-5, 5, 5), (5, 5, 5), (5, 5, -5), 
                (-5, 5, -5), (-5, -5, -5), (-5, -5, 5), (5, -5, 5), 
                (5, -5, -5), (-5, -5, -5), (-5, -5, 5), (-5, 5, 5), 
                (5, 5, 5), (5, -5, 5), (5, -5, -5), (5, 5, -5)
                ], 
            "cross": [
                (-1, 5, 0), (1, 5, 0), (1, 1, 0), (5, 1, 0), 
                (5, -1, 0), (1, -1, 0), (1, -5, 0), (-1, -5, 0), 
                (-1, -1, 0), (-5, -1, 0), (-5, 1, 0), (-1, 1, 0), 
                (-1, 5, 0)
                ], 
            "cylinder": [
                (-7, 7, 0), (-5, 7, 5), (0, 7, 7), (5, 7, 5), (7, 7, 0), 
                (5, 7, -5), (0, 7, -7), (0, 7, 7), (0, -7, 7), (-5, -7, 5), 
                (-7, -7, 0), (-5, -7, -5), (0, -7, -7), (5, -7, -5), 
                (7, -7, 0), (5, -7, 5), (0, -7, 7), (0, -7, -7), 
                (0, 7, -7), (-5, 7, -5), (-7, 7, 0), (7, 7, 0), 
                (7, -7, 0), (-7, -7, 0), (-7, 7, 0)
                ], 
            "foot": [
                (-4, 0, -4), (-4, 0, -7), (-3, 0, -11), (-1, 0, -12), 
                (0, 0, -12), (1, 0, -12), (3, 0, -11), (4, 0, -7), 
                (4, 0, -4), (-4, 0, -4), (-5, 0, 1), (-5, 0, 6), 
                (-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), (2, 0, 15), 
                (4, 0, 12), (5, 0, 6), (5, 0, 1), (4, 0, -4), (-4, 0, -4), 
                (4, 0, -4)
                ], 
            "foot2": [
                (-6, 12, -14), (-6, 12, 6), (6, 12, 6), (6, 12, -14), 
                (-6, 12, -14), (-6, 0, -14), (-6, 0, 18), (6, 0, 18), 
                (6, 0, -14), (-6, 0, -14), (-6, 0, 18), (-6, 12, 6), 
                (6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14)
                ], 
            "hat": [
                (14, 9, 0), (0, 15, 0), (-14, 9, 0), (-7, -5, 0), 
                (-16, -7, 0), (0, -7, 0), (16, -7, 0), (7, -5, 0), 
                (14, 9, 0)
                ], 
            "head": [
                (13, 15, -11), (0, 25, -15), (-13, 15, -11), (-14, 6, 0), 
                (-13, 15, 11), (0, 25, 15), (13, 15, 11), (14, 6, 0), 
                (13, 15, -11)
                ], 
            "hoof": [
                (-6, 0, -5), (-6.5, 0, -1), (-6, 0, 3), (-5.2, 0, 5.5), 
                (-3, 0, 7.5), (0, 0, 8.2), (3, 0, 7.5), (5.2, 0, 5.5), 
                (6, 0, 3), (6.5, 0, -1), (6, 0, -5), (4, 0, -5), 
                (4.5, 0, -1), (4, 0, 3), (3.5, 0, 4.5), (2, 0, 6), 
                (0, 0, 6.5), (-2, 0, 6), (-3.5, 0, 4.5), (-4, 0, 3), 
                (-4.5, 0, -1), (-4, 0, -5), (-6, 0, -5), (-5.5, 0, -6.5), 
                (5.5, 0, -6.5), (4.5, 0, -10), (2.2, 0, -12.2), 
                (0, 0, -12.2), (-2.2, 0, -12.2), (-4.5, 0, -10), 
                (-5.5, 0, -6.5)
                ], 
            "hoof2": [
                (6, 6, -12), (0, 8, -12), (-6, 6, -12), (-8, 3, -13), 
                (-8, 0, -12), (-7, 0, -10), (-8, 0, -6), (-9, 0, -1), 
                (-8, 0, 4), (-5, 0, 9), (0, 0, 10), (5, 0, 9), (8, 0, 4), 
                (9, 0, -1), (8, 0, -6), (7, 0, -10), (8, 0, -12), 
                (8, 3, -13), (6, 6, -12)
                ], 
            "pipe": [
                (0, 7, 7), (0, -7, 7), (4.9, -7, 4.9), (7, -7, 0), 
                (7, 7, 0), (4.9, 7, -4.9), (0, 7, -7), (0, -7, -7), 
                (-4.9, -7, -4.9), (-7, -7, 0), (-7, 7, 0), (-4.9, 7, 4.9), 
                (0, 7, 7), (4.9, 7, 4.9), (7, 7, 0), (7, -7, 0), 
                (4.9, -7, -4.9), (0, -7, -7), (0, 7, -7), (-4.9, 7, -4.9), 
                (-7, 7, 0), (-7, -7, 0), (-4.9, -7, 4.9), (0, -7, 7)
                ], 
            "pointer": [
                (0, 8, 4), (-2.8, 8, 2.8), (-4, 8, 0), (-2.8, 8, -2.8), 
                (0, 8, -4), (2.8, 8, -2.8), (4, 8, -0), (2.8, 8, 2.8), 
                (0, 8, 4), (0, 8, -0), (0, 0, -0)
                ], 
            "scapula": [
                (2, 10, -11), (0, 0, -11), (-2, 10, -11), (-3, 18, 0), 
                (-2, 10, 11), (0, 0, 11), (2, 10, 11), (3, 18, 0), 
                (2, 10, -11)
                ], 
            "sphere": [
                (0, 5, 0), (0, 3.5, 3.5), (0, 0, 5), (0, -3.5, 3.5), 
                (0, -5, 0), (0, -3.5, -3.5), (0, 0, -5), (0, 3.5, -3.5), 
                (0, 5, 0), (-3.5, 3.5, 0), (-5, 0, 0), (-3.5, 0, 3.5), 
                (0, 0, 5), (3.5, 0, 3.5), (5, 0, 0), (3.5, 0, -3.5), 
                (0, 0, -5), (-3.5, 0, -3.5), (-5, 0, 0), (-3.5, -3.5, 0), 
                (0, -5, 0), (3.5, -3.5, 0), (5, 0, 0), (3.5, 3.5, 0), (0, 5, 0)
                ], 
            "square": [
                (25, 0, 25), (25, 0, -25), (-25, 0, -25), (-25, 0, 25), (25, 0, 25)
                ], 
            }


    def createControllers(self, *args):
        """ If there are no arguments, all controllers will be created.
        However, it is usually used as follows.
        >>> createCurveControllers(cube, sphere ...)
        >>> return ["created curve name", ...]

        - "arrow", "arrow2", "arrow3", "arrow4", "arrow5", "arrow6", 
        - "car", "car2", "car3", "circle", "cone", "cone2", "cross", "cube", "cylinder", 
        - "foot", "foot2", 
        - "hat", "head", "hoof", "hoof2", 
        - "pipe", "pointer", 
        - "scapula", "sphere", "square", 
        """
        allShapes = self.controllerShapes.keys()
        curvesToMake = [i for i in args if i in allShapes]
        result = []
        for shapeName in curvesToMake:
            position = self.controllerShapes[shapeName]
            curve = pm.curve(p=position, d=1, n=shapeName)
            result.append(curve)
        return result


class Selections:
    def __init__(self):
        pass


    def selectObjectOnly(self):
        shapeNodes = pm.ls(sl=True, dag=True, type=['mesh', 'nurbsSurface'])
        objectNodes = {i.getParent() for i in shapeNodes}
        result = list(objectNodes)
        pm.select(result)


    def selectGroupOnly(self):
        """ If there is no shape and the type is not 
        'joint', 'ikEffector', 'ikHandle' and 'Constraint', 
        it is most likely a group. 
        """
        transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
        result = []
        for i in transformNodes:
            iType = pm.objectType(i)
            isShape = pm.listRelatives(i, s=True)
            isAnotherType = iType in ['joint', 'ikEffector', 'ikHandle',]
            isConstraint = 'Constraint' in iType
            if not (isShape or isAnotherType or isConstraint):
                result.append(i)
            else:
                continue
        pm.select(result)


    def selectConstraintOnly(self):
        """ If there is no shape and the type is not 
        'joint', 'ikEffector', 'ikHandle', and <not> 'Constraint', 
        it is most likely a Constraints.
        """
        transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
        result = []
        for i in transformNodes:
            iType = pm.objectType(i)
            isShape = pm.listRelatives(i, s=True)
            isAnotherType = iType in ['joint', 'ikEffector', 'ikHandle',]
            isConstraint = 'Constraint' in iType
            if not (isShape or isAnotherType or not isConstraint):
                result.append(i)
            else:
                continue
        pm.select(result)


    def selectJointOnly(self) -> list:
        transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
        result = []
        for i in transformNodes:
            iType = pm.objectType(i)
            if iType == 'joint':
                result.append(i)
            else:
                continue
        pm.select(result)
        return result


class Grouping:
    def __init__(self):
        pass


    def groupingWithOwnPivot(self, *arg) -> None:
        selections = getFlattenList(arg) if arg else pm.ls(sl=True)
        result = []
        for i in selections:
            groupName = f"{i}_grp"
            emptyGroup = pm.group(em=True, n=groupName)
            pm.matchTransform(emptyGroup, i, pos=True, rot=True)
            try:
                pm.parent(emptyGroup, pm.listRelatives(i, p=True))
            except:
                pass
            pm.parent(i, emptyGroup)
            result.append(groupName)
        return result


class Joints:
    def __init__(self):
        pass


    def createPolevectorJoint(self, *arg):
        """ Select three joints.
        Put the pole vector at 90 degrees to the direction 
        of the first and last joints.
        >>> return [startJointOfPolevector, endJointOfPolevector]
         """
        joints = getFlattenList(arg)
        selections = joints if joints else pm.ls(sl=True)
        if len(selections) != 3:
            pm.warning("Three joints needed.")
            return
        jointsNameAndPosition = getNameAndPosition(selections)
        jointNames = jointsNameAndPosition.keys()
        jointPoint = jointsNameAndPosition.values()
        firstJoint, middleJoint, endJoint = jointNames
        firstPoint, middlePoint, endPoint = jointPoint
        result = createJoints([firstPoint, endPoint])
        newJoint, newEndJoint = result
        orientJoints([newJoint], 'xyz', 'yup')
        setPoleDirection(newJoint, endJoint, middleJoint)
        pm.matchTransform(newJoint, middleJoint, pos=True)
        return result


    def setJointsStyleNone(self, *arg):
        """ Change the drawing style of a joint to None. """
        sel = getFlattenList(arg) if arg else pm.ls(sl=True)
        joints = [i for i in sel if pm.objectType(i) == 'joint']
        for i in joints:
            pm.setAttr(f"{i}.drawStyle", 2)


class Align:
    def __init__(self):
        pass


    def objectLineUp(self, threePoints=[]):
        """ The three selected objects create a surface in space.
        And the remaining objects are placed on this surface.
        Select 4 or more objects for this function to be effective.
        - Used to make the finger joints line up in space.
        - Ball and toe joints can be placed in a straight line 
        on the surface formed by the pelvis, knees, and ankles.
         """
        selections = self.isThreePoints(threePoints)
        if not selections:
            pm.warning("3 Points needed.")
            return
        parentsInfo = {i: i.getParent() for i in selections}
        self.unParent(parentsInfo)
        self.moveOjbectsToPoint(selections)
        self.reParent(parentsInfo)


    def curveStraightUp(self):
        """ Arrange the points in a straight line.
        Use the equation of a straight line in space 
        to make a curved line a straight line.
        1. Create an equation
        2. Check the condition.
        3. Make a straight line.
        """
        originalCurveVertex = pm.ls(sl=True, fl=True)
        if len(originalCurveVertex) < 2:
            pm.warning("2 or more points needed.")
            return
        firstPoint = originalCurveVertex[0]
        lastPoint = originalCurveVertex[-1]
        solutions = self.calculateEquation(firstPoint, lastPoint)
        copiedCurve = self.copyCurve(originalCurveVertex)
        copiedCurveVertex = pm.ls(f"{copiedCurve}.cv[*]", fl=True)
        for i in copiedCurveVertex:
            pointPosition = i.getPosition(space="world")
            finalPosition = self.getFinalPosition(pointPosition, solutions)
            pm.move(i, finalPosition)


    def isThreePoints(self, threePoints=[]):
        point3 = pm.ls(threePoints) if threePoints else pm.ls(sl=True)
        if len(point3) < 3:
            return
        else:
            return point3


    def unParent(self, parentsInfo: dict) -> None:
        for child, parents in parentsInfo.items():
            if not parents:
                continue
            else:
                pm.parent(child, w=True)


    def reParent(self, parentsInfo: dict) -> None:
        for child, parents in parentsInfo.items():
            if not parents:
                continue
            else:
                pm.parent(child, parents)


    def moveOjbectsToPoint(self, selection: list):
        point3 = selection[:3]
        dotsLeftBehind = selection[3:]
        point3Position = [pm.xform(i, q=1, t=1, ws=1) for i in point3]
        normalVector = self.getFaceNormalVector(point3Position)
        planePoint = point3Position[0]
        for i in dotsLeftBehind:
            pointOfLine = pm.xform(i, q=True, t=True, ws=True)
            intersectionPoint = self.getIntersectionPoint(normalVector, \
                                planePoint, normalVector, pointOfLine)
            pm.move(i, intersectionPoint)


    def getFaceNormalVector(self, threePointsPosition=[]):
        """ Given three points, 
        create a face and return the normal vector of the face.
        """
        face = pm.polyCreateFacet(p=threePointsPosition)
        info = pm.polyInfo(face, fn=True)
        stripInfo = info[0].split(":")[-1].strip()
        normalVector = [float(i) for i in stripInfo.split(" ")]
        return normalVector


    def getIntersectionPoint(self, normalOfPlane: list, pointOnPlane: list, \
            directionOfLine: list, pointOnLine: list) -> list:
        """ Get intersection of plane and line.
        - Equation of surface: dot(normalOfPlane, X - pointOfPlane) = 0
        - Equation of line: pointOfLine + lean*directionOfLine
        """
        planeNormal = np.array(normalOfPlane)
        planePoint = np.array(pointOnPlane)
        lineDirection = np.array(directionOfLine)
        linePoint = np.array(pointOnLine)
        delta1 = np.dot(planeNormal, (planePoint - linePoint)) 
        delta2 = np.dot(planeNormal, lineDirection)
        lean = delta1 / delta2
        intersectionPoint = pointOnLine + (lean*lineDirection)
        return intersectionPoint.tolist()


    def copyCurve(self, vertices: list):
        originalCurve = pm.ls(vertices, o=True)
        copiedCurve = pm.duplicate(originalCurve, rr=True)
        copiedCurve = copiedCurve[0]
        return copiedCurve


    def calculateEquation(self, firstPoint, lastPoint):
        """ Create an equation for a straight line 
        passing through two points. Calculate the positions of other points 
        not included in the straight line. 
         """
        # Equation
        x1, y1, z1 = firstPoint.getPosition(space="world")
        x2, y2, z2 = lastPoint.getPosition(space="world")
        A, B, C = (x2 - x1), (y2 - y1), (z2 - z1)
        x, y, z = sympy.symbols('x y z')
        expr1 = sympy.Eq(B*x - A*y, B*x1 - A*y1)
        expr2 = sympy.Eq(C*y - B*z, C*y1 - B*z1)
        expr3 = sympy.Eq(A*z - C*x, A*z1 - C*x1)
        # Determine direction.
        MAX = max([abs(i) for i in [A, B, C]])
        if abs(A) == MAX:
            idx = 0
            highestGap = x
            variables = [y, z]
            expr = [expr1, expr3]
        elif abs(B) == MAX:
            idx = 1
            highestGap = y
            variables = [x, z]
            expr = [expr1, expr2]
        elif abs(C) == MAX:
            idx = 2
            highestGap = z
            variables = [x, y]
            expr = [expr2, expr3]
        else:
            return
        return idx, highestGap, variables, expr, [x, y, z]


    def getFinalPosition(self, pointPosition, solutions):
        idx, highestGap, variables, expr, equation = solutions
        value = pointPosition[idx]
        fx = [i.subs(highestGap, value) for i in expr]
        position = sympy.solve(fx, variables)
        position[highestGap] = value
        finalPosition = [round(float(position[i]), 4) for i in equation]
        return finalPosition


