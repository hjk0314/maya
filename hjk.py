from collections import Iterable, Counter
import math
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


def getFlattenList(*args) -> list:
    """ Flattens a list within a list. 
    >>> getFlattenList(["ab", ["bc"], ["ef"]], [[["gh", ], "ij"], "jk"], ...)
    >>> ['ab', 'bc', 'ef', 'gh', 'ij', 'jk']
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
    """ Get the coordinates of the center pivot of the boundingBox. """
    boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    return [x, y, z]


def getBoundingBoxSize(vertexOrObject) -> list:
    """ Get the length, width, and height of the bounding box. """
    boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    x = (xMax - xMin) / 2
    y = (yMax - yMin) / 2
    z = (zMax - zMin) / 2
    boundingBoxSize = [x, y, z]
    result = [round(i, 5) for i in boundingBoxSize]
    return result


def orientJoints(*args, **kwargs) -> dict:
    """ Orient Joints

    Args: 
     - The Default Maya Settings is -> (default=True, d=True)
        1. primaryAxis: "xyz"
        2. secondaryAxis: "yup"

     - Mixamo Settings is -> (mixamo=True, m=True)
        1. primaryAxis: "yzx"
        2. secondaryAxis: "zup"

    Examples: 
        >>> orientJoints("joint1")
        >>> {"joint1": ["joint2", "joint3", ...]}
        >>> orientJoints("joint1", "joint4")
        >>> {"joint1": ["joint2", "joint3"], "joint4": ["joint5"]}
        >>> orientJoints("joint1", "joint2", m=True)
        >>> {"joint1": ["joint2", "joint3"], "joint4": ["joint5"]}
        >>> orientJoints()
        >>> {"joint1": ["joint2", "joint3", ...]}
        >>> orientJoints(m=True)
        >>> {"joint1": ["joint2", "joint3"], "joint4": ["joint5"]}
     """
    joints = args if args else pm.selected(type=["joint"])
    if joints:
        joints = [pm.PyNode(i) for i in joints]
    else:
        return
    flags = {
        "default": ["xyz", "yup"], 
        "d": ["xyz", "yup"], 
        "mixamo": ["yzx", "zup"], 
        "m": ["yzx", "zup"]
        }
    if kwargs:
        key = next(iter(kwargs))
        value = kwargs[key]
        if key in flags.keys() and value:
            primaryAxis, secondaryAxis = flags[key]
        elif key in flags.keys() and not value:
            return
        else:
            pm.warning("Unrecognized keywords.")
            return
    else:
        primaryAxis, secondaryAxis = ["xyz", "yup"]
    result = {}
    pm.makeIdentity(joints, a=True, jo=True, n=0)
    for jnt in joints:
        pm.joint(jnt, edit=True, children=True, zeroScaleOrient=True, \
                orientJoint=primaryAxis, secondaryAxisOrient=secondaryAxis)
        allDescendents = pm.listRelatives(jnt, ad=True, type="joint")
        endJoint = [i for i in allDescendents if not i.getChildren()]
        for i in endJoint:
            pm.joint(i, e=True, oj='none', ch=True, zso=True)
        result[jnt] = allDescendents
    return result


def createCurveFollowingObject(startFrame: int, endFrame: int, *args) -> list:
    """ This is a function that creates a curve 
    for moving objects or points.
     """
    sel = args if args else pm.selected(fl=True)
    curves = []
    curveAndCoordinate = {}
    for frame in range(startFrame, endFrame + 1):
        pm.currentTime(frame)
        for i in sel:
            pos = getPosition(i)
            curveAndCoordinate.setdefault(i.name(), []).append(pos)
    for points in curveAndCoordinate.values():
        cuv = pm.curve(p=points, d=3)
        curves.append(cuv)
    return curves


def createCurvePassThroughObject(*args) -> str:
    """ Create a curve that passes through objects. """
    sel = args if args else pm.selected(fl=True)
    positions = [getPosition(i) for i in sel]
    curve = pm.curve(ep=positions, d=3)
    return curve


def createClosedCurve(*args) -> str:
    """ Creates a circle that passes through objects or points.

    Examples: 
        >>> createClosedCurve()
        >>> createClosedCurve("point1", "point2", "point3", ...)
     """
    sel = args if args else pm.selected(fl=True)
    positions = [getPosition(i) for i in sel]
    circle = pm.circle(nr=(0, 1, 0), ch=False, s=len(sel))
    circle = circle[0]
    for i, pos in enumerate(positions):
        pm.move(f"{circle}.cv[{i}]", pos, ws=True)
    return circle


def matchPivot(child: str, parents: str) -> None:
    """ Match Child's pivot to the Parent's pivot. """
    parentsPivot = pm.xform(parents, q=1, ws=1, rp=1)
    pm.xform(child, sp=parentsPivot, rp=parentsPivot)
    pm.parent(child, parents)
    pm.makeIdentity(child, a=1, t=1, r=1, s=1, n=0, pn=1)
    pm.parent(child, w=True)


def createCurveAimingPoint(*args) -> str:
    """ Select two objects or points.
    A straight line is created looking at the last point.
    >>> return "curveName"
     """
    sel = args if args else pm.selected(fl=True)
    positions = [getPosition(i) for i in [sel[0], sel[-1]]]
    linearCurve = pm.curve(p=positions, d=1)
    locators = []
    for i in positions:
        locator = pm.spaceLocator()
        pm.move(locator, i)
        locators.append(locator)
    startLocator, endLocator = locators
    pm.aimConstraint(endLocator, startLocator)
    pm.delete(startLocator, cn=True)
    matchPivot(linearCurve, startLocator)
    pm.rebuildCurve(linearCurve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
    pm.delete(locators)
    return linearCurve


def createCurveNormalDirection(*args) -> list:
    """ Create Curves that is the same as the normal direction 
    of the selected point.
     """
    sel = args if args else pm.selected(fl=True)
    result = []
    for vtx in sel:
        if not isinstance(vtx, pm.MeshVertex):
            pm.warning(f"{vtx} is not MeshVertex.")
            continue
        vertexPosition = pm.pointPosition(vtx)
        normalVector = pm.polyNormalPerVertex(vtx, q=True, normalXYZ=True)
        normalVector = normalVector[0:3]
        locators = []
        for pos in [(0, 0, 0), normalVector]:
            locator = pm.spaceLocator()
            locators.append(locator)
            pm.move(locator, pos)
        unitCurve = createCurveAimingPoint(*locators)
        pm.move(unitCurve, vertexPosition)
        pm.delete(locators)
        result.append(unitCurve)
    return result


def selectGroupOnly(*args) -> list:
    """ If there is no shape and the type is not 
    'joint', 'ikEffector', 'ikHandle' and 'Constraint', 
    it is most likely a group. 
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
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


def selectConstraintOnly(*args) -> list:
    """ If there is no shape and the type is not 
    'joint', 'ikEffector', 'ikHandle', and <not> 'Constraint', 
    it is most likely a Constraints.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
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
    """ If the type is 'joint', it is most likely a joint.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
        iType = pm.objectType(i)
        if iType == 'joint':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectIKHandleOnly(*args) -> list:
    """ If the type is 'ikHandle', it is most likely a ikHandle.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
        iType = pm.objectType(i)
        if iType == 'ikHandle':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectClusterOnly(*args) -> list:
    """ If the type is 'clusterHandle', it is most likely a clusterHandle.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
        iShape = pm.listRelatives(i, s=True)
        iNodeType = pm.nodeType(iShape)
        if iNodeType == 'clusterHandle':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectLocatorOnly(*args) -> list:
    """ If the type is 'locator', it is most likely a locator.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['transform'])
    else:
        sel = pm.selected(dag=True, type=['transform'])
    result = []
    for i in sel:
        iShape = pm.listRelatives(i, s=True)
        iNodeType = pm.nodeType(iShape)
        if iNodeType == 'locator':
            result.append(i)
        else:
            continue
    pm.select(result)
    return result


def selectNurbsCurveOnly(*args) -> list:
    """ If the type is 'nurbsCurve', it is most likely a nurbsCurve.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['nurbsCurve'])
    else:
        sel = pm.selected(dag=True, type=['nurbsCurve'])
    result = [i.getParent() for i in sel]
    pm.select(result)
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

