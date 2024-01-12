from collections.abc import Iterable
import re
import pymel.core as pm


class Common:
    def __init__(self):
        pass


    def getPosition(self, selection) -> list:
        try:
            position = pm.pointPosition(selection)
        except:
            position = pm.xform(selection, q=1, ws=1, rp=1)
        return position


    def getBoundingBoxPosition(self, vertexOrObject) -> list:
        boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
        x = (xMin + xMax) / 2
        y = (yMin + yMax) / 2
        z = (zMin + zMax) / 2
        return [x, y, z]


    def makeSameAsParentPivot(self, object, parents) -> None:
        """ If you put object under parents and freeze it, 
        the pivots match together. """
        parentsPivot = self.getPosition(parents)
        pm.xform(object, sp=parentsPivot, rp=parentsPivot)
        pm.parent(object, parents)
        pm.makeIdentity(object, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(object, w=True)


    def createLocator(self, position=0) -> str:
        locator = pm.spaceLocator()
        pm.move(locator, position)
        return locator


    def getNameAndPosition(self, selections: list) -> dict:
        nameAndPosition = {}
        for i in selections:
            point = pm.xform(i, q=True, ws=True, rp=True)
            nameAndPosition[i] = point
        return nameAndPosition


    def createJoints(self, jointInfo) -> list:
        pm.select(cl=True)
        if isinstance(jointInfo, list):
            result = [pm.joint(p=position) for position in jointInfo]
        elif isinstance(jointInfo, dict):
            result = []
            for jointName, position in jointInfo.items():
                jnt = pm.joint(p=position, n=jointName) 
                result.append(jnt)
        else:
            result = []


    def setPoleDirection(self, object, aimJoint, upVectorJoint):
        pm.aimConstraint(
            aimJoint, object, o=(0,0,90), wut='object', wuo=upVectorJoint
            )
        pm.delete(object, cn=True)


class Curves:
    def __init__(self):
        super().__init__()


    def createCurvePassingKeyedUp(self, startFrame, endFrame):
        selections = pm.ls(sl=True)
        for i in selections:
            positions = []
            for frame in range(startFrame, endFrame + 1):
                pm.currentTime(frame)
                xyz = self.getPosition(i)
                positions.append(xyz)
            pm.curve(p=positions, d=3)


    def createCurvePassingPoints(self):
        selections = pm.ls(sl=True, fl=True)
        positions = [self.getPosition(i) for i in selections]
        result = pm.curve(ep=positions, d=3)


    def createCurvePassingLocators(self, curveClosed=False):
        """ The closedCurve means that 
        the start and end points of a curve are connected. """
        locators = pm.ls(sl=True, fl=True)
        positions = [self.getPosition(i) for i in locators]
        if not curveClosed:
            pm.curve(ep=positions, d=3)
        else:
            circle = pm.circle(nr=(0, 1, 0), ch=False, s=len(locators))
            circle = circle[0]
            for i, xyz in enumerate(positions):
                pm.move(f"{circle}.cv[{i}]", xyz, ws=True)


    def createCurveAimingPoint(self):
        selections = pm.ls(sl=True)
        init = selections[0]
        last = selections[-1]
        positions = [self.getPosition(i) for i in [init, last]]
        simpleCurve = self.createCurveOnlyTwoPoints(positions)
        startLocator, endLocator = self.createLocators(positions)
        pm.aimConstraint(endLocator, startLocator)
        pm.delete(startLocator, cn=True)
        self.makeSameAsParentPivot(simpleCurve, startLocator)
        pm.rebuildCurve(simpleCurve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)


    def createCurvesNormalDirection(self) -> list:
        selections = pm.ls(sl=True, fl=True)
        result = []
        for i in selections:
            vertexPosition = pm.pointPosition(i)
            normalPosition = pm.polyNormalPerVertex(i, q=True, normalXYZ=True)[0:3]
            twoPositions = [(0,0,0), normalPosition]
            curve = self.createCurveOnlyTwoPoints(twoPositions)
            startLocator, endLocator = self.createLocators(twoPositions)
            pm.aimConstraint(endLocator, startLocator)
            pm.delete(startLocator, constraints=True)
            self.makeSameAsParentPivot(curve, startLocator)
            pm.rebuildCurve(curve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
            pm.move(curve, vertexPosition)
            pm.delete([startLocator, endLocator])
            result.append(curve)
        return result


    def createCurveOnlyTwoPoints(self, positions: list=[]) -> str:
        """ The parameter positions are tuples in a list, 
        like this -> [(0,0,0), (1,1,1), (1,2,3), ...]
        """
        if not positions:
            positions = [self.getPosition(i) for i in pm.ls(sl=True, fl=True)]
        try:
            startPoint = positions[0]
            endPoint = positions[-1]
            simpleLine = pm.curve(p=[startPoint, endPoint], d=1)
            return simpleLine
        except:
            return


    def getPosition(self, selection) -> list:
        try:
            position = pm.pointPosition(selection)
        except:
            position = pm.xform(selection, q=1, ws=1, rp=1)
        return position


    def makeSameAsParentPivot(self, object, parents) -> None:
        """ If you put object under parents and freeze it, 
        the pivots match together. """
        parentsPivot = self.getPosition(parents)
        pm.xform(object, sp=parentsPivot, rp=parentsPivot)
        pm.parent(object, parents)
        pm.makeIdentity(object, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(object, w=True)


    def createLocators(self, positions: list=0) -> list:
        result = []
        if not positions:
            positions = [self.getPosition(i) for i in pm.selected(fl=True)]
        for i in positions:
            locator = pm.spaceLocator()
            pm.move(locator, i)
            result.append(locator)
        return result


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


    def createControllers(self, **kwargs):
        """ If there are no arguments, all controllers will be created.
        However, it is usually used as follows.
        >>> createCurveControllers(cube=3, sphere=2 ...)
        >>> Create 3 cubes and 2 spheres to Maya.

        - "arrow", "arrow2", "arrow3", "arrow4", "arrow5", "arrow6", 
        - "car", "car2", "car3", "circle", "cone", "cone2", "cross", "cube", "cylinder", 
        - "foot", "foot2", 
        - "hat", "head", "hoof", "hoof2", 
        - "pipe", "pointer", 
        - "scapula", "sphere", "square", 
        """
        allShapes = self.controllerShapes.keys()
        inputs = kwargs.keys()
        curvesToMake = set(inputs) & set(allShapes) if inputs else allShapes
        result = {}
        for shapeName in curvesToMake:
            try:
                loopingNumbers = kwargs[shapeName]
            except:
                loopingNumbers = 1
            curves = self.createCurveToShape(shapeName, loopingNumbers)
            result[shapeName] = curves
        return result


    def createCurveToShape(self, shapeName, loopingNumbers):
        result = []
        for i in range(loopingNumbers):
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


    def groupingWithOwnPivot(self, tailName: str=None) -> None:
        selections = pm.ls(sl=True)
        for i in selections:
            groupName = f"{i}_{tailName}_grp" if tailName else f"{i}_grp"
            emptyGroup = pm.group(em=True, n=groupName)
            pm.matchTransform(emptyGroup, i, pos=True, rot=True)
            try:
                pm.parent(emptyGroup, i.getParent())
            except:
                pass
            pm.parent(i, emptyGroup)


class Joints:
    def __init__(self):
        super().__init__()


    def orientJoints(self, primaryAxis='yzx', secondaryAxis='zup', selections=[]):
        """ The default value of primaryAxis and secondaryAxis are 
        the same as Mixamo spine. """
        allJoints = selections if selections else self.selectJointOnly()
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


    def createPolevectorJoint(self):
        """ Select three joints.
        Put the pole vector at 90 degrees to the direction 
        of the first and last joints.
         """
        selections = pm.ls(sl=True)
        if len(selections) != 3:
            return
        jointsNameAndPosition = self.getNameAndPosition(selections)
        jointNames = jointsNameAndPosition.keys()
        jointPoint = jointsNameAndPosition.values()
        firstJoint, middleJoint, endJoint = jointNames
        firstPoint, middlePoint, endPoint = jointPoint
        newJoint, newEndJoint = self.createJoints([firstPoint, endPoint])
        pm.select(cl=True)
        pm.select(newJoint)
        self.orientJoints('xyz', 'yup')
        self.setPoleDirection(newJoint, endJoint, middleJoint)
        pm.matchTransform(newJoint, middleJoint, pos=True)


    def setJointsStyleNone(self):
        """ Change the drawing style of a joint to None. """
        selections = pm.ls(sl=True)
        joints = [i for i in selections if pm.objectType(i)=='joint']
        for i in joints:
            pm.setAttr(f"{i}.drawStyle", 2)


    def getNameAndPosition(self, selections: list) -> dict:
        nameAndPosition = {}
        for i in selections:
            point = pm.xform(i, q=True, ws=True, rp=True)
            nameAndPosition[i] = point
        return nameAndPosition


    def createJoints(self, positions: list) -> list:
        """ Tuples in the list.
        >>> [(1,0,1), (-1,0,1), (1,0,-1), (-1,0,-1)]
         """
        pm.select(cl=True)
        jointNames = [pm.joint(p=i) for i in positions]
        return jointNames


    def setPoleDirection(self, object, aimJoint, upVectorJoint):
        pm.aimConstraint(
            aimJoint, object, o=(0,0,90), wut='object', wuo=upVectorJoint
            )
        pm.delete(object, cn=True)


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


class Rename:
    def __init__(self):
        """ 
        reName("nameToCreate_001")
        >>> "nameToCreate_001"
        >>> "nameToCreate_002"
        >>> "nameToCreate_003"

        reName("Apple", "Banana")
        >>> "Apple_01" -> "Banana_01"
         """
        pass


    def reName(self, *arg: str):
        """ If there
        - is one argument, create a new name, 
        - are two arguments, replace a specific word.

        reName("nameToCreate_001")
        >>> "nameToCreate_001"
        >>> "nameToCreate_002"
        >>> "nameToCreate_003"

        reName("Apple", "Banana")
        >>> "Apple_01" -> "Banana_01"
         """
        numberOfArguments = len(arg)
        if numberOfArguments == 1:
            nameToCreate = arg[0]
            self.createNewName(nameToCreate)
        elif numberOfArguments == 2:
            originalWord = arg[0]
            wordToChange = arg[1]
            self.changeWords(originalWord, wordToChange)
        else:
            pass


    def createNewName(self, nameToCreate):
        nameSlices = self.splitNumbers(nameToCreate)
        numberDict = self.numbersInfo(nameSlices)
        if numberDict:
            result = self.nameDigitly(nameSlices, numberDict)
        else:
            result = self.nameSimply(nameToCreate)
        self.failureReport(result)


    def changeWords(self, originalWord, wordToChange) -> dict:
        selections = pm.ls(sl=True, fl=True)
        failureDict = {}
        for i in selections:
            selected = i.name()
            nameToChange = selected.replace(originalWord, wordToChange)
            if pm.objExists(nameToChange):
                failureDict[selected] = nameToChange
                continue
            else:
                pm.rename(selected, nameToChange)
        return failureDict


    def splitNumbers(self, fullName: str) -> list:
        """ inputName -> "vhcl_car123_rig_v0123"
        >>> ['vhcl_car', '123', '_rig_v', '0123']
        """
        nameSlices = re.split(r'(\d+)', fullName)
        result = [i for i in nameSlices if i]
        print(result)
        return result


    def numbersInfo(self, nameSlices: list) -> dict:
        """ Create and return the numbers in a name as a dict.
        - inputName -> "vhcl_car123_rig_v0123"
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
        - result -> {1: '123', 3: '0123'}
         """
        result = {}
        for i, slice in enumerate(nameSlices):
            if slice.isdigit():
                # 'slice' must be a string to know the number of digits.
                result[i] = slice
            else:
                continue
        return result


    def nameDigitly(self, nameSlices: list, numbersInfo: dict) -> dict:
        """ Name by increasing number.
        - originalName -> "vhcl_car123_rig_v0123".
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
        - numbersInfo -> {1: '123', 3: '0123'}

        Select 3 objects and name them. Return below.
        >>> "vhcl_car123_rig_v0123"
        >>> "vhcl_car123_rig_v0124"
        >>> "vhcl_car123_rig_v0125"
        """
        selections = pm.ls(sl=True, fl=True)
        idx = max(numbersInfo)
        nDigit = len(numbersInfo[idx])
        number = int(numbersInfo[idx])
        failureDict = {}
        for i, obj in enumerate(selections):
            increasedNumber = f"%0{nDigit}d" % (number + i)
            nameSlices[idx] = increasedNumber
            result = ''.join(nameSlices)
            if pm.objExists(result):
                failureDict[obj] = result
                continue
            else:
                pm.rename(obj, result)
        return failureDict


    def nameSimply(self, nameSlices: list) -> dict:
        """ Name Simply. And returns a Dict of failures.
        - originalName -> "vhcl_car123_rig_v0123"
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
         """
        selections = pm.ls(sl=True, fl=True)
        failureDict = {}
        for i, obj in enumerate(selections):
            result = ''.join(nameSlices) + str(i)
            if pm.objExists(result):
                failureDict[obj] = result
                continue
            else:
                pm.rename(obj, result)
        return failureDict


    def failureReport(self, failureDict: dict):
        if failureDict:
            warningMessages = "\n"
            for objName, nameToChange in failureDict.items():
                warningMessages += f"{objName} -> {nameToChange} failed. \n"
            pm.warning(warningMessages)
        else:
            warningMessages = "Rename all success."
            print(warningMessages)


class QuickRig_Mixamo:
    def __init__(self):
        self.side = ["Left", "Right"]
        self.arms = ["Shoulder", "Arm", "ForeArm", "Hand"]
        self.legs = ["UpLeg", "Leg", "Foot", "ToeBase", "Toe_End"]
        finger = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        self.finger = [f"Hand{i}" for i in finger]
        self.spines = ["Spine", "Spine1", "Spine2"]
        self.spines += ["Neck", "Head", "HeadTop_End"]
        self.mainCurve = "mainCurve"
        self.rootJoint = "Hips"
        self.jointPosition = {
            "Hips": (0.0, 98.223, 1.464), 
            "Spine": (0.0, 107.814, 1.588), 
            "Spine1": (0.0, 117.134, 0.203), 
            "Spine2": (0.0, 125.82, -1.089), 
            "Neck": (0.0, 141.589, -3.019), 
            "Head": (0.0, 150.649, -1.431), 
            "HeadTop_End": (0.0, 171.409, 5.635), 
            "LeftShoulder": (4.305, 136.196, -3.124), 
            "LeftArm": (19.934, 135.702, -5.494), 
            "LeftForeArm": (42.774, 135.702, -6.376), 
            "LeftHand": (63.913, 135.702, -6.131), 
            "LeftHandThumb1": (65.761, 135.008, -2.444), 
            "LeftHandThumb2": (68.495, 133.652, -0.242), 
            "LeftHandThumb3": (70.727, 132.545, 1.556), 
            "LeftHandThumb4": (72.412, 131.709, 2.913), 
            "LeftHandIndex1": (71.683, 134.879, -2.495), 
            "LeftHandIndex2": (74.972, 134.879, -2.495), 
            "LeftHandIndex3": (77.576, 134.879, -2.495), 
            "LeftHandIndex4": (80.181, 134.879, -2.495), 
            "LeftHandMiddle1": (71.566, 134.682, -4.906), 
            "LeftHandMiddle2": (75.085, 134.762, -4.906), 
            "LeftHandMiddle3": (78.171, 134.832, -4.906), 
            "LeftHandMiddle4": (81.57, 134.908, -4.906), 
            "LeftHandRing1": (71.293, 134.575, -6.84), 
            "LeftHandRing2": (74.241, 134.742, -6.84), 
            "LeftHandRing3": (77.231, 134.912, -6.84), 
            "LeftHandRing4": (80.134, 135.078, -6.84), 
            "LeftHandPinky1": (70.702, 134.116, -8.847), 
            "LeftHandPinky2": (73.811, 134.283, -8.847), 
            "LeftHandPinky3": (75.625, 134.38, -8.847), 
            "LeftHandPinky4": (77.461, 134.478, -8.847), 
            "RightShoulder": (-4.305, 136.196, -3.124), 
            "RightArm": (-21.859, 135.702, -5.585), 
            "RightForeArm": (-42.316, 135.702, -6.381), 
            "RightHand": (-63.913, 135.702, -6.131), 
            "RightHandThumb1": (-65.761, 135.008, -2.444), 
            "RightHandThumb2": (-68.495, 133.652, -0.242), 
            "RightHandThumb3": (-70.727, 132.545, 1.556), 
            "RightHandThumb4": (-72.412, 131.709, 2.913), 
            "RightHandIndex1": (-71.683, 134.879, -2.495), 
            "RightHandIndex2": (-74.972, 134.879, -2.495), 
            "RightHandIndex3": (-77.576, 134.879, -2.495), 
            "RightHandIndex4": (-80.181, 134.879, -2.495), 
            "RightHandMiddle1": (-71.565, 134.682, -4.906), 
            "RightHandMiddle2": (-75.085, 134.762, -4.906), 
            "RightHandMiddle3": (-78.171, 134.832, -4.906), 
            "RightHandMiddle4": (-81.569, 134.908, -4.906), 
            "RightHandRing1": (-71.293, 134.575, -6.84), 
            "RightHandRing2": (-74.24, 134.742, -6.84), 
            "RightHandRing3": (-77.231, 134.912, -6.84), 
            "RightHandRing4": (-80.134, 135.078, -6.84), 
            "RightHandPinky1": (-70.702, 134.116, -8.847), 
            "RightHandPinky2": (-73.811, 134.283, -8.847), 
            "RightHandPinky3": (-75.625, 134.38, -8.847), 
            "RightHandPinky4": (-77.461, 134.478, -8.847), 
            "LeftUpLeg": (10.797, 91.863, -1.849), 
            "LeftLeg": (10.797, 50.067, -0.255), 
            "LeftFoot": (10.797, 8.223, -4.39), 
            "LeftToeBase": (10.797, 0.001, 5.7), 
            "LeftToe_End": (10.797, 0.0, 14.439), 
            "RightUpLeg": (-10.797, 91.863, -1.849), 
            "RightLeg": (-10.797, 50.066, -0.255), 
            "RightFoot": (-10.797, 8.223, -4.39), 
            "RightToeBase": (-10.797, 0.001, 5.7), 
            "RightToe_End": (-10.797, 0.0, 14.439), 
            }
        self.hierarchy = {
            "Hips": 
                [self.spines] + [[i+g for g in self.legs] for i in self.side], 
            "Spine2": 
                [[i+j for j in self.arms] for i in self.side],  
            "LeftHand": 
                [[f"Left{i}{n}" for n in range(1, 5)] for i in self.finger], 
            "RightHand": 
                [[f"Right{i}{n}" for n in range(1, 5)] for i in self.finger], 
        }


    def createMixamoBones(self):
        self.cleanObjects(self.mainCurve, self.jointPosition.keys())
        self.createJointWithName(self.jointPosition)
        self.buildJointsHumanStructure(self.hierarchy)
        self.matchMainCurveToJointSize(self.rootJoint, self.mainCurve)
        pm.parent(self.rootJoint, self.mainCurve)


    def alignSpinesCenter(self):
        spineJoints = [self.rootJoint] + self.spines
        self.updateAllJointPositions()
        self.moveJointsGridZero(spineJoints)
        self.createMixamoBones()


    def sameBothSide(self, direction: str="LeftToRight"):
        self.updateAllJointPositions()
        sideA, sideB = self.getJointNameBothSide(direction)
        self.updateBothSideToSame(sideA, sideB)
        self.createMixamoBones()


    def createAllRigJoints(self):
        self.updateAllJointPositions()
        positions = self.jointPosition
        hierarchy = self.hierarchy
        data = self.getDataWithNewName(positions, hierarchy, "rig_")
        rigPositions, rigHierarchy = data
        self.cleanObjects(rigPositions)
        self.createJointWithName(rigPositions)
        self.buildJointsHumanStructure(rigHierarchy)


    def createIKFKSpines(self, *IKFK):
        self.updateAllJointPositions()
        spinesPositions, spinesHierarchy = self.getDataIKFKSpines(IKFK)
        self.cleanObjects(spinesHierarchy.values())
        self.createJointWithName(spinesPositions)
        self.buildJointsHumanStructure(spinesHierarchy)


    def createIKFKArms(self, *IKFK):
        self.updateAllJointPositions()
        armsPositions, armsHierarchy = self.getDataIKFKArms(IKFK)
        self.cleanObjects(armsHierarchy.values())
        self.createJointWithName(armsPositions)
        self.buildJointsHumanStructure(armsHierarchy)


    def createIKFKLegs(self, *IKFK):
        self.updateAllJointPositions()
        legsPositions, legsHierarchy = self.getDataIKFKLegs(IKFK)
        self.cleanObjects(legsHierarchy.values())
        self.createJointWithName(legsPositions)
        self.buildJointsHumanStructure(legsHierarchy)


# 79 char line ================================================================
# 72 docstring or comments line ======================================== 


    def cleanObjects(self, *args):
        for element in args:
            isStr = isinstance(element, str)
            isIter = isinstance(element, Iterable)
            if not isStr and isIter:
                for i in element:
                    self.cleanObjects(i)
            else:
                try:
                    pm.delete(element)
                except:
                    pass


    def updateAllJointPositions(self):
        allJoints = self.jointPosition.keys()
        for joint in allJoints:
            position = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = tuple(position)


    def updateBothSideToSame(self, sideA, sideB):
        for idx, joint in enumerate(sideA):
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[sideB[idx]] = (x*-1, y, z)


    def createJointWithName(self, nameAndPosition: dict):
        for jointName, position in nameAndPosition.items():
            pm.select(cl=True)
            pm.joint(p=position, n=jointName)


    def buildJointsHumanStructure(self, hierarchyStructure: dict):
        for parents, bothSideList in hierarchyStructure.items():
            for jointList in bothSideList:
                self.parentHierarchically(jointList)
                self.orientJointsMixamoType(jointList)
                self.parentHierarchically([parents, jointList[0]])


    def matchMainCurveToJointSize(self, object: str, curveName: str):
        objectBoundingBox = pm.xform(object, q=True, bb=True, ws=True)
        x1, y1, z1, x2, y2, z2 = objectBoundingBox
        x = (x2 - x1) / 2
        y = (y2 - y1) / 2
        z = (z2 - z1) / 2
        objectSize = max(x, z)
        objectSize = round(objectSize, 3)
        pm.circle(nr=(0, 1, 0), n=curveName, ch=0, r=objectSize)


    def moveJointsGridZero(self, joints: list):
        for joint in joints:
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = (0, y, z)


    def getJointNameBothSide(self, twoOptions: str) -> list:
        """ Direction has one of the options: 
        >>> "LeftToRight" or "RightToLeft" 
         """
        allJoints = self.jointPosition.keys()
        A, B = twoOptions.split("To")
        side = []
        otherSide = []
        for jointName in allJoints:
            if A in jointName:
                side.append(jointName)
            elif B in jointName:
                otherSide.append(jointName)
            else:
                continue
        return side, otherSide


    def parentHierarchically(self, selections: list=[]):
        if not selections:
            selections = pm.selected()
        for idx, upper in enumerate(selections):
            try:
                lower = selections[idx + 1]
                pm.parent(lower, upper)
            except:
                continue


    def orientJointsMixamoType(self, jointList=[]):
        firstJoint = jointList[0]
        ls = "LeftShoulder"
        la = "LeftArm"
        lh = "LeftHand"
        rs = "RightShoulder"
        ra = "RightArm"
        rh = "RightHand"
        if ls in firstJoint or la in firstJoint or lh in firstJoint:
            primaryAxis = 'yxz'
            secondaryAxis = 'zdown'
        elif rs in firstJoint or ra in firstJoint or rh in firstJoint:
            primaryAxis = 'yxz'
            secondaryAxis = 'zup'
        else:
            primaryAxis = 'yzx'
            secondaryAxis = 'zup'
        self.orientJoints(primaryAxis, secondaryAxis, jointList)


    def orientJoints(self, primaryAxis='yzx', secondaryAxis='zup', joints=[]):
        """ The default value of primaryAxis and secondaryAxis are 
        the same as Mixamo spine. """
        allJoints = joints if joints else self.selectJointOnly()
        endJoints = [i for i in allJoints if not pm.listRelatives(i, c=True)]
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


    def getPosition(self, selection) -> list:
        try:
            position = pm.pointPosition(selection)
        except:
            position = pm.xform(selection, q=1, ws=1, rp=1)
        return position


    def getDataWithNewName(self, positions: dict, hierarchy: dict, \
        foreword="", tailword=""):
        """ Returns the data with a new name. 
        - positions = {str: (float, float, float), ...}
        - hierarchy = {str: [[ ],[ ]], ...}
         """
        result1 = {}
        for jnt, pos in positions.items():
            result1[f"{foreword}{jnt}{tailword}"] = pos 
        result2 = {}
        for parents, hierarchy in hierarchy.items():
            key = f"{foreword}{parents}{tailword}"
            val = [[f"{foreword}{j}{tailword}" for j in i] for i in hierarchy]
            result2[key] = val
        return result1, result2


    def getDataIKFKSpines(self, *IKFK):
        IKFK = self.getFlattenList(IKFK)
        sourceSpines = self.spines[:3]
        sourceHierarchy = {"Hips": [sourceSpines]}
        spinesPositions = {}
        for i in sourceSpines:
            for k in IKFK:
                spinesPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        spinesHierarchy = {}
        for parents, c in sourceHierarchy.items():
            key = f"rig_{parents}"
            value = [[f"rig_{i}_{k}" for i in h] for h in c for k in IKFK]
            spinesHierarchy[key] = value
        return spinesPositions, spinesHierarchy


    def getDataIKFKArms(self, *IKFK):
        IKFK = self.getFlattenList(IKFK)
        sourceArms = [i + m for m in self.arms[1:] for i in self.side]
        sourceHierarchy = {i[0]: [i[1:]] for i in self.hierarchy["Spine2"]}
        armsPositions = {}
        for i in sourceArms:
            for k in IKFK:
                armsPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        armsHierarchy = {}
        for parents, hierarchy in sourceHierarchy.items():
            for h in hierarchy:
                key = f"rig_{parents}"
                value = [[f"rig_{i}_{k}" for i in h] for k in IKFK]
                armsHierarchy[key] = value
        return armsPositions, armsHierarchy


    def getDataIKFKLegs(self, *IKFK):
        IKFK = self.getFlattenList(IKFK)
        sourceLegs = [i + g for g in self.legs for i in self.side]
        sourceHierarchy = {"Hips": self.hierarchy["Hips"][1:]}
        legsPositions = {}
        for i in sourceLegs:
            for k in IKFK:
                legsPositions[f"rig_{i}_{k}"] = self.jointPosition[i]
        legsHierarchy = {}
        for parents, c in sourceHierarchy.items():
            key = f"rig_{parents}"
            value = [[f"rig_{i}_{k}" for i in h] for h in c for k in IKFK]
            legsHierarchy[key] = value
        return legsPositions, legsHierarchy


    def getFlattenList(self, iterable):
        result = []
        for item in iterable:
            isIter = isinstance(item, Iterable)
            isStr = isinstance(item, str)
            if not isStr and isIter:
                result.extend(self.getFlattenList(item))
            else :
                result.append(item)
        result = list(set(result))
        return result


# 79 char line ================================================================
# 72 docstring or comments line ========================================   


qm = QuickRig_Mixamo()
# qm.createMixamoBones()
# qm.alignSpinesCenter()
qm.sameBothSide()
qm.createAllRigJoints()
qm.createIKFKSpines("IK", "FK")
qm.createIKFKArms("IK", "FK")
qm.createIKFKLegs("IK", "FK")
# sel = Selections()
# sel.selectJointOnly()

# grp = Grouping()
# grp.groupingWithOwnPivot()
    
# jnt = Joints()
# jnt.createPolevectorJoint()

# ren = Rename()
# ren.changeWords("_Left", "_Right")


topGroupName = ""
groupNameHierarchy = {
    topGroupName: ["rig", "MODEL"], 
    "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
    "skeletons": ["bindBones", "rigBones"]
    }
