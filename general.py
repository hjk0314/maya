from collections import Iterable, Counter
import numpy as np
import sympy
import pymel.core as pm
import maya.OpenMaya as om


def getPosition(selection: str) -> tuple:
    """ Get the coordinates of an object or point.
    >>> getPosition("pSphere1")
    >>> getPosition("pSphere1.vtx[317]")
    >>> (0.0, 0.0, 0.0)
     """
    try:
        position = pm.pointPosition(selection)
    except:
        position = pm.xform(selection, q=1, ws=1, rp=1)
    result = tuple(position)
    return result


def makeSameAsParentPivot(object, parents) -> None:
    """ If you put object under parents and freeze it, 
    the pivots match together. """
    parentsPivot = pm.xform(parents, q=1, ws=1, rp=1)
    pm.xform(object, sp=parentsPivot, rp=parentsPivot)
    pm.parent(object, parents)
    pm.makeIdentity(object, a=1, t=1, r=1, s=1, n=0, pn=1)
    pm.parent(object, w=True)


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


def getBoundingBoxPosition(vertexOrObject) -> list:
    boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    return [x, y, z]


def getBoundingBoxSize(vertexOrObject) -> list:
    boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMax - xMin) / 2
    y = (yMax - yMin) / 2
    z = (zMax - zMin) / 2
    boundingBoxSize = max(x, y, z)
    boundingBoxSize = round(boundingBoxSize, 3)
    return boundingBoxSize


def orientJoints(joints=[], primaryAxis='yzx', secondaryAxis='zup'):
    """ This settings are Mixamo values.
    - "yzx"
    - "zup"

    The Default settings in MAYA is
    - "xyz"
    - "yup"
     """
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


def createCurvePassingKeyedUp(startFrame, endFrame, objects=[]):
    sel = objects if objects else pm.ls(sl=True)
    curves = []
    for i in sel:
        positions = []
        for frame in range(startFrame, endFrame + 1):
            pm.currentTime(frame)
            pos = getPosition(i)
            positions.append(pos)
        cuv = pm.curve(p=positions, d=3)
        curves.append(cuv)
    return curves


def createCurvePassingThrough(objects=[]) -> str:
    """ Return curveName """
    sel = objects if objects else pm.ls(sl=True, fl=True)
    positions = [getPosition(i) for i in sel]
    curve = pm.curve(ep=positions, d=3)
    return curve


def createClosedCurve(objects=[]) -> str:
    """ The closedCurve means that 
    the start and end points of a curve are connected.
    >>> createCurvePassingLocators()
    >>> createCurvePassingLocators(curveClosed=True)
    >>> return "circleName"
     """
    sel = objects if objects else pm.ls(sl=True, fl=True)
    positions = [getPosition(i) for i in sel]
    circle = pm.circle(nr=(0, 1, 0), ch=False, s=len(sel))
    circle = circle[0]
    for i, pos in enumerate(positions):
        pm.move(f"{circle}.cv[{i}]", pos, ws=True)
    return circle


def createCurveAimingPoint(objects=[]) -> str:
    """ Select two objects or points.
    A straight line is created looking at the last point.
    >>> return "curveName"
     """
    sel = objects if objects else pm.ls(sl=True, fl=True)
    positions = [getPosition(i) for i in [sel[0], sel[-1]]]
    simpleCurve = pm.curve(p=positions, d=1)
    locators = []
    for i in positions:
        locator = pm.spaceLocator()
        pm.move(locator, i)
        locators.append(locator)
    startLocator, endLocator = locators
    pm.aimConstraint(endLocator, startLocator)
    pm.delete(startLocator, cn=True)
    makeSameAsParentPivot(simpleCurve, startLocator)
    pm.rebuildCurve(simpleCurve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
    pm.delete(locators)
    return simpleCurve


def createCurvesNormalDirection(vertex=[]) -> list:
    sel = vertex if vertex else pm.ls(sl=True, fl=True)
    result = []
    for vtx in sel:
        vertexPosition = pm.pointPosition(vtx)
        normalVector = pm.polyNormalPerVertex(vtx, q=True, normalXYZ=True)
        normalVector = normalVector[0:3]
        locators = []
        for pos in [(0, 0, 0), normalVector]:
            locator = pm.spaceLocator()
            locators.append(locator)
            pm.move(locator, pos)
        unitCurve = createCurveAimingPoint(locators)
        pm.move(unitCurve, vertexPosition)
        pm.delete(locators)
        result.append(unitCurve)
    return result


def selectObjectOnly() -> list:
    shapeNodes = pm.ls(sl=True, dag=True, type=['mesh', 'nurbsSurface'])
    objectNodes = {i.getParent() for i in shapeNodes}
    result = list(objectNodes)
    pm.select(result)
    return result


def selectGroupOnly() -> list:
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
    return result


def selectConstraintOnly() -> list:
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
    return result


def selectJointOnly(*args) -> list:
    if args:    sel = pm.ls(args, dag=True, type=['transform'])
    else:       sel = pm.ls(sl=True, dag=True, type=['transform'])
    result = []
    for i in sel:
        iType = pm.objectType(i)
        if iType == 'joint':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectIKHandleOnly() -> list:
    transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
    result = []
    for i in transformNodes:
        iType = pm.objectType(i)
        if iType == 'ikHandle':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectClusterOnly() -> list:
    transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
    result = []
    for i in transformNodes:
        iShape = pm.listRelatives(i, s=True)
        iNodeType = pm.nodeType(iShape)
        if iNodeType == 'clusterHandle':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectLocatorOnly() -> list:
    transformNodes = pm.ls(sl=True, dag=True, type=['transform'])
    result = []
    for i in transformNodes:
        iShape = pm.listRelatives(i, s=True)
        iNodeType = pm.nodeType(iShape)
        if iNodeType == 'locator':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectNurbsCurveOnly() -> list:
    transformNodes = pm.ls(sl=True, dag=True, type=['nurbsCurve'])
    result = [i.getParent() for i in transformNodes]
    pm.select(result)
    return result


def groupingWithOwnPivot(*arg) -> list:
    selections = arg if arg else pm.ls(sl=True)
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
        result.append(emptyGroup)
    return result


def groupOwnPivot(*args, **kwargs) -> list:
    """ Create a group with the same pivot.
    - groupOwnPivot() \\
    >>> ["selection_grp", "selection"]
    - groupOwnPivot("pCube1", "pCube2") \\
    >>> ["pCube1_grp", "pCube1", "pCube2_grp", "pCube2"]
    - groupOwnPivot(*list) \\
    >>> ["element1_grp", "element1", "element2_grp", "element2", ...]
    - groupOwnPivot("pCube1", null=True) \\
    >>> ["pCube1_grp", "pCube1_null", "pCube1"]
    - groupOwnPivot("pCube1", null=True, n="newName") \\
    >>> ["newName_grp", "newName_null", "pCube1"]
     """
    selections = args if args else pm.ls(sl=True)
    flags = {"null": False, "n": ""}
    for key, value in kwargs.items():
        if key in flags:
            flags[key] = value
        else:
            continue
    result = []
    for i in selections:
        objName = flags["n"]
        objName = objName if objName else i
        topGroup = pm.listRelatives(i, p=True)
        temp = []
        if True == flags["null"]:
            grpName = [f"{objName}_grp", f"{objName}_null"]
            for name in grpName:
                grp = pm.group(em=True, n=name)
                pm.matchTransform(grp, i, pos=True, rot=True)
                temp.append(grp)
        else:
            grpName = f"{objName}_grp"
            grp = pm.group(em=True, n=grpName)
            pm.matchTransform(grp, i, pos=True, rot=True)
            temp.append(grp)
        temp.append(i)
        parentHierarchically(*temp)
        try:    pm.parent(temp[0], topGroup)
        except: pass
        result += temp
    return result


def createPolevectorJoint(*args) -> list:
    """ Select three joints.
    Put the pole vector at 90 degrees to the direction 
    of the first and last joints.
    >>> return [polevectorJoint1, polevectorJoint2]
     """
    jnt = args if args else pm.ls(sl=True)
    if len(jnt) != 3:
        pm.warning("Three joints needed.")
        return
    jntPosition = [getPosition(i) for i in jnt]
    middleJnt, endJnt = jnt[1:3]
    result = []
    pm.select(cl=True)
    result = [pm.joint(p=pos) for pos in jntPosition[::2]]
    newJnt = result[0]
    orientJoints(result, 'xyz', 'yup')
    pm.aimConstraint(endJnt, newJnt, o=(0,0,90), wut='object', wuo=middleJnt)
    pm.delete(newJnt, cn=True)
    pm.matchTransform(newJnt, middleJnt, pos=True)
    return result


def setJointsStyle(joints=[], drawStyle=2) -> list:
    """ Change the drawing style of a joint. Default is 2: None. 
    0: Bone
    1: Multi-child as Box
    2: None
     """
    sel = joints if joints else pm.ls(sl=True)
    result = []
    for i in sel:
        try:
            pm.setAttr(f"{i}.drawStyle", drawStyle)
            result.append(i)
        except:
            continue
    return result


def parentHierarchically(*args) -> None:
    """ Hierarchically parent.
    >>> parentHierarchically(*lst)
    >>> parentHierarchically(parents, child)
     """
    sel = [pm.PyNode(i) for i in args] if args else pm.selected()
    for idx, parents in enumerate(sel):
        try:
            child = sel[idx + 1]
            pm.parent(child, parents)
        except:
            continue


def softSelection():
    """ Make the selected soft selection area into a cluster. """
    selection = om.MSelectionList()
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)
    dagPath = om.MDagPath()
    component = om.MObject()
    iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
    elements = []
    while not iter.isDone(): 
        iter.getDagPath(dagPath, component)
        dagPath.pop()
        node = dagPath.fullPathName()
        fnComp = om.MFnSingleIndexedComponent(component)   
        for i in range(fnComp.elementCount()):
            elem = fnComp.element(i)
            infl = fnComp.weight(i).influence()
            elements.append([node, elem, infl])
        iter.next()
    sel = ["%s.vtx[%d]" % (el[0], el[1]) for el in elements] 
    pm.select(sel, r=True)
    cluster = pm.cluster(relative=True)
    for i in range(len(elements)):
        pm.percent(cluster[0], sel[i], v=elements[i][2])
    pm.select(cluster[1], r=True)


def replaceLeftRight(obj: str) -> str:
    """ Confinedly, used.
    >>> replaceLeftRight('Left')
    >>> 'Right'
    >>> replaceLeftRight('Right')
    >>> 'Left'
    >>> replaceLeftRight('_L')
    >>> '_R'
    >>> replaceLeftRight('_R')
    >>> '_L'
     """
    obj = obj.name() if isinstance(obj, pm.PyNode) else obj
    if not obj:
        return
    elif "Left" in obj:
        sideA = "Left"
        sideB = "Right"
    elif "_L" in obj:
        sideA = "_L"
        sideB = "_R"
    elif "Right" in obj:
        sideA = "Right"
        sideB = "Left"
    elif "_R" in obj:
        sideA = "_R"
        sideB = "_L"
    else:
        return
    result = obj.replace(sideA, sideB)
    return result


def getLeftOrRight(*args):
    """ Finds the number of 'left' and 'right' in a word 
    and returns the 'left' or 'right' that contain the most.
     """
    jntSide = []
    for i in args:
        jnt = i.name() if isinstance(i, pm.PyNode) else i
        if "Left" in jnt:
            jntSide.append("Left")
        elif "_L" in jnt:
            jntSide.append("Left")
        elif "Right" in jnt:
            jntSide.append("Right")
        elif "_R" in jnt:
            jntSide.append("Right")
        else:
            jntSide.append("")
    count = Counter(jntSide).most_common(1)[0]
    num = count[1]
    if num == len(args):
        result = count[0]
    else:
        pm.warning("Must have a left or right side.")
        result = ""
    return result


def mirrorCopy(obj: str, mirrorPlane: str="YZ") -> list:
    """ Mirror copy based on 'YZ' or 'XY'. Default mirrorPlane is "YZ".
    This function is shown below.
    - First, Check Selection.
    - Duplicate and Grouping own Pivot.
    - Move Groups to Other Side.
    - Creates a Mirror Shape.
    - Finish and Clean up. 

    >>> mirrorCopy()
    >>> -> Error Message.
    >>> mirrorCopy('pCube1')
    >>> ['pCube1_grp', 'pCube1_null', 'pCube2']
    >>> mirrorCopy('cc_doorLeftFront')
    >>> ['cc_doorRight_grp', 'cc_doorRight_null', 'cc_doorRight']
    >>> mirrorCopy('lever_R', 'XY')
    >>> ['lever_L_grp', 'lever_L_null', 'lever_L']
     """
    # Check Selection
    if not obj:
        pm.warning("Nothing Selected.")
        return
    # Duplicate and Grouping own Pivot
    replaced = replaceLeftRight(obj)
    copied = pm.duplicate(obj, rr=True, n=replaced)[0]
    pm.parent(copied, w=True)
    result = groupOwnPivot(copied, null=True, n=replaced)
    topGrp, nullGrp, copied = result
    pm.parent(copied, w=True)
    # Move Groups to Other Side.
    pos = pm.getAttr(f'{topGrp}.translate')
    rot = pm.getAttr(f'{topGrp}.rotate')
    tx, ty, tz = pos
    rx, ry, rz = rot
    if mirrorPlane == "YZ":
        tx *= -1
        rx += (180 if rx < 0 else -180)
        ry *= -1
        rz *= -1
    else:
        tz *= -1
        rz += (180 if rz < 0 else -180)
    attr = {'tx': tx, 'ty': ty, 'tz': tz, 'rx': rx, 'ry': ry, 'rz': rz}
    for key, value in attr.items():
        pm.setAttr(f'{topGrp}.{key}', value)
    # Creates a Mirror Shape.
    tempGrp = pm.group(em=True)
    pm.parent(copied, tempGrp)
    if mirrorPlane == "XY":
        direction = [1, 1, -1]
    elif mirrorPlane == "YZ":
        direction = [-1, 1, 1]
    else:
        return
    pm.scale(tempGrp, direction, r=True)
    # Finish and Clean up.
    pm.parent(copied, nullGrp)
    pm.makeIdentity(copied, a=True, t=1, r=1, s=1, n=0, pn=1)
    pm.delete(tempGrp)
    return result


def createRigGroups(assetName: str = ""):
    groupNames = {
        "assetName": ["rig", "MODEL"], 
        "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
        "skeletons": ["bindBones", "rigBones"]
        }
    if assetName:
        groupNames[assetName] = groupNames.pop("assetName")
    for parents, children in groupNames.items():
        if not pm.objExists(parents):
            pm.group(em=True, n=parents)
        for child in children:
            if not pm.objExists(child):
                pm.group(em=True, n=child)
            pm.parent(child, parents)
    result = groupNames.keys()
    result = list(result)
    return result


class AlignObjects:
    def __init__(self):
        """ This class arranges some objects in a straight line in space. """
        pass

    
    def lineUp(self, *arg):
        """ The three selected objects create a surface in space.
        And the remaining points are placed on this surface.
        Select 4 or more objects for this function to be effective.
        - Used to make the finger joints line up in space.
        - Ball and toe joints can be placed in a straight line 
        on the surface formed by the pelvis, knees, and ankles.
         """
        # check parameters
        sel = [pm.PyNode(i) for i in arg] if arg else pm.ls(sl=True)
        if len(sel) < 4:
            pm.warning("Select 4 or more objects.")
            return
        # information of parents
        parentsInfo = {i: i.getParent() for i in sel}
        # unParent
        transformNodes = []
        for child, parents in parentsInfo.items():
            try:
                pm.parent(child, w=True)
                transformNode = child.getParent()
                if transformNode:
                    transformNodes.append(transformNode)
            except:
                continue
        # main
        mainDots = sel[:3]
        lastDots = sel[3:]
        mainDotsPos = [pm.xform(i, q=1, t=1, ws=1) for i in mainDots]
        normalVector = self.getFaceNormalVector(mainDotsPos)
        planePoint = mainDotsPos[0]
        for i in lastDots:
            pointOfLine = pm.xform(i, q=True, t=True, ws=True)
            intersectionPoint = self.getIntersectionPoint(normalVector, \
                                planePoint, normalVector, pointOfLine)
            pm.move(i, intersectionPoint)
        # reParent
        for child, parents in parentsInfo.items():
            try:
                pm.parent(child, parents)
            except:
                continue
        pm.delete(transformNodes)


    def getFaceNormalVector(self, threePointsPosition=[]):
        """ Given three points, 
        create a face and return the normal vector of the face.
        """
        face = pm.polyCreateFacet(p=threePointsPosition)
        info = pm.polyInfo(face, fn=True)
        stripInfo = info[0].split(":")[-1].strip()
        normalVector = [float(i) for i in stripInfo.split(" ")]
        pm.delete(face)
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


class AlignCurvePoints:
    def __init__(self):
        pass


    def lineUp(self):
        """ Arrange the points in a straight line.
        Use the equation of a straight line in space 
        to make a curved line a straight line.
        1. Create an equation
        2. Check the condition.
        3. Make a straight line.
        """
        cuvVtx = pm.ls(sl=True, fl=True)
        if len(cuvVtx) < 2:
            pm.warning("2 or more points needed.")
            return
        initPoint = cuvVtx[0]
        lastPoint = cuvVtx[-1]
        solutions = self.createEquation(initPoint, lastPoint)
        copiedCurve = self.copyCurve(cuvVtx)
        copiedCuvVtx = pm.ls(f"{copiedCurve}.cv[*]", fl=True)
        for i in copiedCuvVtx:
            pointPos = i.getPosition(space="world")
            finalPos = self.getFinalPosition(pointPos, solutions)
            pm.move(i, finalPos)


    def copyCurve(self, vertices: list):
        originalCurve = pm.ls(vertices, o=True)
        copiedCurve = pm.duplicate(originalCurve, rr=True)
        copiedCurve = copiedCurve[0]
        return copiedCurve


    def createEquation(self, initPoint, lastPoint):
        """ Create an equation for a straight line 
        passing through two points. Calculate the positions of other points 
        not included in the straight line. 
         """
        # Equation
        x1, y1, z1 = initPoint.getPosition(space="world")
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
            "cap": [
                (0, 0, 12), (-9, 0, 9), (-6.667, 6.667, 6.667), 
                (0, 9, 9), (6.667, 6.667, 6.667), (9, 0, 9), 
                (0, 0, 12), (0, 9, 9), (0, 12, 0), 
                (0, 9, -9), (0, 0, -12), (9, 0, -9), 
                (6.667, 6.667, -6.667), (0, 9, -9), (-6.667, 6.667, -6.667), 
                (-9, 0, -9), (0, 0, -12), (9, 0, -9), 
                (12, 0, 0), (9, 0, 9), (6.667, 6.667, 6.667), 
                (9, 9, 0), (6.667, 6.667, -6.667), (9, 0, -9), 
                (12, 0, 0), (9, 9, 0), (0, 12, 0), 
                (-9, 9, 0), (-6.667, 6.667, -6.667), (-9, 0, -9), 
                (-12, 0, 0), (-9, 9, 0), (-6.667, 6.667, 6.667), 
                (-9, 0, 9), (-12, 0, 0)
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
            "door": [
                (0, 8, 0), (0, 58, -48), (0, 61, -100), (0, 8, -97), 
                (0, -45, -97), (0, -45, 0), (0, -16, 2), (0, 8, 0)
                ], 
            "door2": [
                (0, 8, 0), (0, 58, -5), (0, 61, -73), (0, -4, -82), 
                (0, -45, -46), (0, -45, -2), (0, 8, 0)
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
            "IKFK": [
                (-6.611, 0, 2), (-6.611, 0, -2), (-5.792, 0, -2), 
                (-5.792, 0, 2), (-6.611, 0, 2), (-4.692, 0, 2), 
                (-4.692, 0, -2), (-3.879, 0, -2), (-3.879, 0, -0.368), 
                (-2.391, 0, -2), (-1.342, 0, -2), (-2.928, 0, -0.358), 
                (-1.245, 0, 2), (-2.304, 0, 2), (-3.495, 0, 0.245), 
                (-3.879, 0, 0.65), (-3.879, 0, 2), (-4.692, 0, 2), 
                (-0.376, 0, 2), (-0.376, 0, -2), (2.401, 0, -2), 
                (2.401, 0, -1.294), (0.442, 0, -1.294), (0.442, 0, -0.384), 
                (2.156, 0, -0.384), (2.156, 0, 0.322), (0.442, 0, 0.322), 
                (0.442, 0, 2), (-0.376, 0, 2), (3.164, 0, 2), 
                (3.164, 0, -2), (3.977, 0, -2), (3.977, 0, -0.368), 
                (5.465, 0, -2), (6.513, 0, -2), (4.928, 0, -0.358), 
                (6.611, 0, 2), (5.552, 0, 2), (4.36, 0, 0.245), 
                (3.977, 0, 0.65), (3.977, 0, 2), (3.164, 0, 2), 
                (6.611, 0, 2)
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
                (2.4, 9.5, -15), (0, 0, -18), (-2.4, 9.5, -15), (-4, 17, 0), 
                (-2.4, 9.5, 15), (0, 0, 18), (2.4, 9.5, 15), (4, 17, 0), 
                (2.4, 9.5, -15)
                ], 
            "sphere": [
                (0, 5, 0), (0, 3.5, 3.5), (0, 0, 5), (0, -3.5, 3.5), 
                (0, -5, 0), (0, -3.5, -3.5), (0, 0, -5), (0, 3.5, -3.5), 
                (0, 5, 0), (-3.5, 3.5, 0), (-5, 0, 0), (-3.5, 0, 3.5), 
                (0, 0, 5), (3.5, 0, 3.5), (5, 0, 0), (3.5, 0, -3.5), 
                (0, 0, -5), (-3.5, 0, -3.5), (-5, 0, 0), (-3.5, -3.5, 0), 
                (0, -5, 0), (3.5, -3.5, 0), (5, 0, 0), (3.5, 3.5, 0), 
                (0, 5, 0)
                ], 
            "spine": [
                (-4, 0, 18), (4, 0, 18), (4, 12, 12.7), (4, 17, 0), 
                (4, 12, -12.7), (4, 0, -18), (-4, 0, -18), (-4, 12, -12.7), 
                (-4, 18, 0), (-4, 12, 12.7), (-4, 0, 18)
                ], 
            "square": [
                (25, 0, 25), (25, 0, -25), (-25, 0, -25), 
                (-25, 0, 25), (25, 0, 25)
                ], 
            }


    def createControllers(self, **kwargs):
        """ If there are no **kwargs, all controllers will be created.
        However, it is usually used as follows.
        >>> createCurveControllers()
        >>> return [all controllers]
        >>> createCurveControllers(cube="newCubeName", cone="newConeName")
        >>> return ["newCubeName", "newConeName"]
        >>> createCurveControllers(**{"cube": "cubeName", "cone": "coneName"})
        >>> return ["cubeName", "coneName"]

        - "arrow", "arrow2", "arrow3", "arrow4", "arrow5", "arrow6", 
        - "cap", "car", "car2", "circle", "cone", "cone2", 
        - "cross", "cube", "cylinder", 
        - "door", "door2", 
        - "foot", "foot2", 
        - "hat", "head", "hoof", "hoof2", 
        - "IKFK", 
        - "pipe", "pointer", 
        - "scapula", "sphere", "spine", "square", 
         """
        allShp = self.controllerShapes.keys()
        result = []
        if kwargs.keys():
            cuvToMake = [i for i in kwargs.keys() if i in allShp]
        else:
            cuvToMake = allShp
        for shpName in cuvToMake:
            pos = self.controllerShapes[shpName]
            try:
                cuvName = kwargs[shpName]
            except:
                cuvName = shpName
            cuv = pm.curve(p=pos, d=1, n=cuvName)
            result.append(cuv)
        return result


# channel = ["translate", "rotate", "scale", "visibility"]
# sel = pm.ls(sl=True)
# for rig in sel:
#     jnt = rig.replace("rig_", "jnt_")
#     for i in channel:
#         pm.connectAttr(f"{rig}.{i}", f"{jnt}.{i}", f=True)

# Controllers().createControllers()
# groupOwnPivot(null=True)
# mirrorCopy("loc_noseGear_L")
# createCurveAimingPoint()
# createRigGroups("needleA")

# def constraintBoth(parents, child):
#     pm.parentConstraint(parents, child, mo=True, w=1.0)
#     pm.scaleConstraint(parents, child, mo=True, w=1.0)


# for i in range(1, 11):
#     jnt = f"train_{i}"
#     mainGrp = f"cc_train_{i}_main_grp"
#     sub = f"cc_train_{i}_sub"
#     body = f"cc_train_{i}_body_grp"
#     bodyCtrl = f"cc_train_{i}_body"
#     mdlBody = f"vhcl_mugunghwaTrainA_mdl_v9999:mugunghwaTrainA_{chr(64 + i)}_body_grp"
#     mdlBt = f"vhcl_mugunghwaTrainA_mdl_v9999:mugunghwaTrainA_{chr(64 + i)}_Bt_grp"
#     mdlWheel = f"vhcl_mugunghwaTrainA_mdl_v9999:mugunghwaTrainA_{chr(64 + i)}_wheel_grp"
#     constraintBoth(jnt, mainGrp)
#     constraintBoth(sub, body)
#     constraintBoth(bodyCtrl, mdlBody)
#     constraintBoth(sub, mdlBt)
#     constraintBoth(sub, mdlWheel)
#     pm.connectAttr("txt_connect_c.Connect", f"{mainGrp}_parentConstraint1.{jnt}W0", f=True)
#     pm.connectAttr("txt_connect_c.Connect", f"{mainGrp}_scaleConstraint1.{jnt}W0", f=True)

# src = "vhcl_mugunghwaTrainA_mdl_v9999:mugunghwaTrainA_A_wheel_Ft_L_1_grp"
# sel = pm.ls(sl=True)
# for i in sel:
#     pm.connectAttr(f"{src}.rotateX", f"{i}.rotateX", f=True)


# sel = pm.ls(sl=True)
# for i in sel:
#     jnt = f"jnt_{i}"
#     pm.connectAttr(f"{jnt}.translate", f"{i}.translate", f=True)
#     pm.connectAttr(f"{jnt}.rotate", f"{i}.rotate", f=True)
#     pm.connectAttr(f"{jnt}.scale", f"{i}.scale", f=True)
    # pm.scaleConstraint(jnt, i, mo=True, w=1.0)


# sel = pm.ls(sl=True)
# for i in sel:
#     jnt = i.replace("cc_", "jnt_")
#     pm.parentConstraint(i, jnt, mo=True, w=1.0)
#     pm.scaleConstraint(i, jnt, mo=True, w=1.0)