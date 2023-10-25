import pymel.core as pm


class CreateCurves:
    def __init__(self):
        self.controllerShapes = {
            "arrow": [
                (0, 0, 2), (2, 0, 1), (1, 0, 1), (1, 0, -2), (-1, 0, -2), 
                (-1, 0, 1), (-2, 0, 1), (0, 0, 2)
                ], 
            "arrow2": [
                (0, 1, 4), (4, 1, 2), (2, 1, 2), (2, 1, -4), (-2, 1, -4), 
                (-2, 1, 2), (-4, 1, 2), (0, 1, 4), (0, -1, 4), (4, -1, 2), 
                (2, -1, 2), (2, -1, -4), (-2, -1, -4), (-2, -1, 2), 
                (-4, -1, 2), (0, -1, 4), (4, -1, 2), (4, 1, 2), (2, 1, 2), 
                (2, 1, -4), (2, -1, -4), (-2, -1, -4), (-2, 1, -4), 
                (-2, 1, 2), (-4, 1, 2), (-4, -1, 2)
                ], 
            "arrow3": [
                (7, 0, 0), (5, 0, -5), (0, 0, -7), (-5, 0, -5), (-7, 0, 0), 
                (-5, 0, 5), (0, 0, 7), (5, 0, 5), (7, 0, 0), (5, 0, 2), 
                (7, 0, 3), (7, 0, 0)
                ], 
            "arrow4": [
                (0, 0, -11), (-3, 0, -8), (-2.0, 0, -8), (-2, 0, -6), 
                (-5, 0, -5), (-6, 0, -2), (-8, 0, -2), (-8, 0, -3), 
                (-11, 0, 0), (-8, 0, 3), (-8, 0, 2), (-6, 0, 2), (-5, 0, 5), 
                (-2, 0, 6), (-2, 0, 8), (-3, 0, 8), (0, 0, 11), (3, 0, 8), 
                (2, 0, 8), (2, 0, 6), (5, 0, 5), (6, 0, 2), (8, 0, 2), 
                (8, 0, 3), (11, 0, 0), (8, 0, -3), (8, 0, -2), (6, 0, -2), 
                (5, 0, -5), (2, 0, -6), (2, 0, -8), (3, 0, -8), (0, 0, -11)
                ], 
            "arrow5": [
                (-2, 0, -1), (2, 0, -1), (2, 0, -2), (4, 0, 0), (2, 0, 2), 
                (2, 0, 1), (-2, 0, 1), (-2, 0, 2), (-4, 0, 0), (-2, 0, -2), 
                (-2, 0, -1)
                ], 
            "arrow6": [
                (-6.3, 6, 0), (-6.5, 4, 0), (-5, 5, 0), (-6.3, 6, 0), 
                (-6, 5, 0), (-5, 3, 0), (-3, 1, 0), (0, 0, 0), (3, 1, 0), 
                (5, 3, 0), (6, 5, 0), (6.3, 6, 0), (5, 5, 0), (6.5, 4, 0), 
                (6.3, 6, 0)
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
                (0, 0, -3), (-2, 0, -2), (-3, 0, 0), (-2, 0, 2), (0, 0, 3), 
                (2, 0, 2), (3, 0, 0), (2, 0, -2), (0, 0, -3)
                ], 
            "cone": [
                (0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), (0, 2, 0), 
                (0, 0, 1), (-0.87, 0, -0), (0.87, 0, 0), (0, 0, 1)
                ], 
            "cone2": [
                (-1, 0, -0), (-0, 0, 1), (1, 0, 0), (0, 0, -1), (0, 2, 0), 
                (-1, 0, -0), (0, 2, 0), (-0, 0, 1), (1, 0, 0), (0, 0, -1), 
                (0, 0, -1), (-1, 0, -0), (-0, 0, 1), (1, 0, 0), (0, 2, 0)
                ], 
            "cube": [
                (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1), 
                (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1), 
                (-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (1, 1, 1), 
                (1, -1, 1), (1, -1, -1), (1, 1, -1)
                ], 
            "cross": [
                (0, 5, 1), (0, 5, -1), (0, 1, -1), (0, 1, -5), (0, -1, -5), 
                (0, -1, -1), (0, -5, -1), (0, -5, 1), (0, -1, 1), (0, -1, 5), 
                (0, 1, 5), (0, 1, 1), (0, 5, 1)
                ], 
            "cylinder": [
                (-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), (0.7, 1, 0.7), 
                (1, 1, 0), (0.7, 1, -0.7), (0, 1, -1), (0, 1, 1), (0, -1, 1), 
                (-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), (0, -1, -1), 
                (0.7, -1, -0.7), (1, -1, 0), (0.7, -1, 0.7), (0, -1, 1), 
                (0, -1, -1), (0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), 
                (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)
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
                (-29, -7, 0), (0, -7, 0), (29, -7, 0), (7, -5, 0), 
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
                (0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), (1, -1, 0), (1, 1, 0), 
                (0.7, 1, -0.7), (0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), 
                (-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), 
                (0.7, 1, 0.7), (1, 1, 0), (1, -1, 0), (0.7, -1, -0.7), 
                (0, -1, -1), (0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), 
                (-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1)
                ], 
            "pointer": [
                (-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), (0.7, 0, 0.7), 
                (1, 0, 0), (0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), 
                (-1, 0, 0), (0, 0, 0), (0, 2, 0)
                ], 
            "scapula": [
                (2, 10, -11), (0, 0, -11), (-2, 10, -11), (-3, 18, 0), 
                (-2, 10, 11), (0, 0, 11), (2, 10, 11), (3, 18, 0), 
                (2, 10, -11)
                ], 
            "sphere": [
                (0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), (0, -0.7, 0.7), 
                (0, -1, 0), (0, -0.7, -0.7), (0, 0, -1), (0, 0.7, -0.7), 
                (0, 1, 0), (-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), 
                (0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), 
                (0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), (-0.7, -0.7, 0), 
                (0, -1, 0), (0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), 
                (0, 1, 0)
                ], 
            "square": [
                (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1), (1, 0, 1)
                ]
            }


    def createCurvePassingThrough(self, startFrame, endFrame):
        """ Creates curves passing through points or objects. """
        duration = (startFrame, endFrame)
        selections = pm.ls(sl=True)
        curveNames = []
        for i in selections:
            positions = self.getPositionPerFrame(i, duration)
            curve = pm.curve(p=positions, d=3)
            curveNames.append(curve)
        return curveNames


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


    def createCurveConnectingPoints(self):
        """ If you put line under Locator and freeze it, 
        the pivot will match. """
        selections = pm.ls(sl=True)
        startPoint = selections[0]
        lastPoint = selections[-1]
        positions = [self.getPosition(i) for i in [startPoint, lastPoint]]
        startPosition = positions[0]
        lastPosition = positions[-1]
        line = pm.curve(p=positions, d=1)
        startLocator = pm.spaceLocator()
        lastLocator = pm.spaceLocator()
        pm.move(startLocator, startPosition, r=True)
        pm.move(lastLocator, lastPosition, r=True)
        pm.xform(line, sp=startPosition, rp=startPosition)
        pm.aimConstraint(lastLocator, startLocator)
        pm.delete(startLocator, cn=True)
        pm.parent(line, startLocator)
        pm.makeIdentity(line, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(line, w=True)
        pm.rebuildCurve(line, d=1, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)


    def createCurveControllers(self, **kwargs):
        """ 
        createCurveControllers(cube=3, sphere=2 ...)
        >>> Create 3 cubes and 2 spheres to Maya.

        - Below are the keywords for ControllerShape.
        "arrow", "arrow2", "arrow3", "arrow4", "arrow5", "arrow6", 
        "car", "car2", "car3", 
        "circle", 
        "cone", "cone2", 
        "cross", 
        "cube", 
        "cylinder", 
        "foot", "foot2", 
        "hat", 
        "head", 
        "hoof", "hoof2", 
        "pipe", 
        "pointer", 
        "scapula", 
        "sphere", 
        "square", 
         """
        curvesWeHave = self.controllerShapes.keys()
        curvesToMake = kwargs.keys()
        commonElements = set(curvesWeHave) & set(curvesToMake)
        for i in commonElements:
            positions = self.controllerShapes[i]
            number = kwargs[i]
            result = [pm.curve(p=positions, d=1) for i in range(number)]


    def getPositionPerFrame(self, selection, duration) -> list:
        startFrame, endFrame = duration
        positions = []
        for frame in range(startFrame, endFrame + 1):
            pm.currentTime(frame)
            xyz = self.getPosition(selection)
            positions.append(xyz)
        return positions


    def getPosition(self, selection) -> list:
        try:
            position = pm.pointPosition(selection)
        except:
            position = pm.xform(selection, q=1, ws=1, rp=1)
        return position


class Select:
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


    def selectJointOnly(self):
        transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
        result = []
        for i in transformNodes:
            iType = pm.objectType(i)
            if iType == 'joint':
                result.append(i)
            else:
                continue
        pm.select(result)


class Grouping:
    def __init__(self):
        pass


    def groupingWithOwnPivot(self, *args: str):
        selections = [pm.PyNode(i) for i in args] if args else pm.ls(sl=True)
        for i in selections:
            emptyGroup = pm.group(em=True, n=f"{i}_grp")
            pm.matchTransform(emptyGroup, i, pos=True, rot=True)
            try:
                pm.parent(emptyGroup, i.getParent())
            except:
                pass
            pm.parent(i, emptyGroup)



# 79 char line ================================================================
# 72 docstring or comments line ========================================   


# cc = CreateCurves()
# cc.createCurveControllers(circle=1)