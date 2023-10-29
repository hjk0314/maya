import pymel.core as pm


class HJK:
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


class Curves(HJK):
    def __init__(self):
        super().__init__()


    def createCurvePassingThrough(self, startFrame, endFrame):
        selections = pm.ls(sl=True)
        for i in selections:
            positions = []
            for frame in range(startFrame, endFrame + 1):
                pm.currentTime(frame)
                xyz = self.getPosition(i)
                positions.append(xyz)
            pm.curve(p=positions, d=3)


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
        startLocator, endLocator = [self.createLocator(i) for i in positions]
        pm.aimConstraint(endLocator, startLocator)
        pm.delete(startLocator, cn=True)
        self.makeSameAsParentPivot(simpleCurve, startLocator)
        pm.rebuildCurve(simpleCurve, d=1, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)


    def createCurveOnlyTwoPoints(self, positions: list=[]):
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


class Controllers:
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


    def createControllers(self, **kwargs):
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
        pass


    def orientJoints(self):
        """ Mixamo's spine is like this. """
        # select All Joints
        selectJoint = pm.ls(sl=True)
        allChildren = pm.listRelatives(selectJoint, ad=True, )
        allHierarchy = selectJoint + allChildren
        firstJoint = selectJoint[0]
        endJoints = [i for i in allHierarchy if not i.getChildren()]
        # orient Joints
        primaryAxis = 'yzx'
        secondaryAxisOrient = 'zup'
        pm.makeIdentity(allHierarchy, a=True, jo=True, n=0)
        pm.joint(firstJoint, e=True, oj=primaryAxis, 
            sao=secondaryAxisOrient, ch=True, zso=True, 
            )
        for i in endJoints:
            pm.joint(i, e=True, oj='none', ch=True, zso=True)



    def createPolevectorJoint(self):
        """ Select three joints.
        Put the pole vector at 90 degrees to the direction 
        of the first and last joints.
         """
        # is Select Three Joints
        selectJoints = pm.ls(sl=True)
        if len(selectJoints) != 3:
            print("Select three joints.")
            return
        # get Positions Of Joints 
        firstJoint, middleJoint, endJoint = selectJoints
        jointPositions = []
        for i in selectJoints:
            point = pm.xform(i, q=True, ws=True, rp=True)
            jointPositions.append(point)
        firstJointPoint, middleJointPoint, endJointPoint = jointPositions
        # create Temporary Joints
        pm.select(cl=True)
        newJoint = pm.joint(p=firstJointPoint)
        newJointEnd = pm.joint(p=endJointPoint)
        # set Direction Of Temporary Joint
        pm.joint(newJoint, e=True, oj='xyz', sao='yup', ch=True, zso=True)
        pm.joint(newJointEnd, e=True, oj='none', ch=True, zso=True)
        pm.aimConstraint(
            endJoint, newJoint, o=(0,0,90), wut='object', wuo=middleJoint
            )
        pm.delete(newJoint, cn=True)
        # put Temporary Joint In The Middle.
        pm.matchTransform(newJoint, middleJoint, pos=True)


    def jntNone(*arg: int) -> None:
        '''Change the drawing style of a joint.
        0: Bone
        1: Multi Child as Box
        2: None
        '''
        num = 2 if not arg else arg[0]
        sel = pm.ls(sl=True)
        if num < 0 or num > 2:
            msg = "Allowed numbers are "
            msg += "[0: Bone, 1: Multi Child as Box, 2: None]"
            print(msg)
        elif not sel:
            print("Nothing selected.")
        else:
            jnt = [i for i in sel if pm.objectType(i)=='joint']
            for i in jnt:
                pm.setAttr(f"{i}.drawStyle", num)


# 79 char line ================================================================
# 72 docstring or comments line ========================================   


jnt = Joints()
# jnt.orientJoints()
jnt.createPolevectorJoint()