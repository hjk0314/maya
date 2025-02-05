from collections import Iterable
import re
import math
import numpy as np
import sympy
import pymel.core as pm
import maya.OpenMaya as om


def getPosition(selection: str) -> tuple:
    """ Get the coordinates of an object or point.

    Examples: 
    >>> getPosition("pSphere1")
    >>> getPosition("pSphere1.vtx[317]")
    >>> (0.0, 0.0, 0.0)
     """
    try:
        position = pm.pointPosition(selection)
    except:
        position = pm.xform(selection, q=1, ws=1, rp=1)
    x, y, z = position
    result = (round(x, 5), round(y, 5), round(z, 5))
    return result


def getFlattenList(data, seen=None) -> list:
    """ Flattens a list within a list. 

    Examples: 
    >>> getFlattenList(["ab", ["bc"], ["ef"]], [[["gh", ], "ij"], "jk"], ...)
    >>> ['ab', 'bc', 'ef', 'gh', 'ij', 'jk']
     """
    if seen is None:
        seen = set()
    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in seen:
                seen.add(key)
                result.append(key)
            result.extend(getFlattenList(value, seen))
    elif isinstance(data, list):
        for item in data:
            result.extend(getFlattenList(item, seen))
    else:
        if data not in seen:
            seen.add(data)
            result.append(data)
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


def getDistance(xyz1: tuple, xyz2: tuple) -> float:
    """ Both arguments are coordinates. 
    Returns the distance between the two coordinates.
    
    Args: 
        >>> getDistance((0,0,0), (1,2,3))
        >>> getDistance([0,0,0], [1,2,3])
     """
    result = math.sqrt(sum((a - b)**2 for a, b in zip(xyz1, xyz2)))
    return result


def getReferencedGroupList() -> list:
    """ Returns a list of groups of referenced. 
    
    Examples: 
    >>> getReferencedGroupList()
    >>> [nt.Transform('vhcl_bestaB_mdl_v9999:bestaB'), ...]
     """
    references = pm.listReferences()
    if not references:
        result = []
    else:
        result = [ref.nodes()[0] for ref in references if ref.nodes()]
    return result


def getNumberIndex(name: str) -> dict:
    """ If the name contains a number, 
    it returns a dict with the number and index.

    Examples: 
    >>> getNumberIndex("vhcl_car123_rig_v0123")
    >>> {0: 'vhcl_car', 1: '123', 2: '_rig_v', 3: '0123'}
     """
    nameSlices = re.split(r'(\d+)', name)
    nameSlices = [i for i in nameSlices if i]
    result = {i: slice for i, slice in enumerate(nameSlices)}
    return result


def getVertexNumber() -> dict:
    """ Get vertex numbers only, strip others. """
    sel = pm.ls(sl=True)
    obj = pm.ls(sel, o=True)
    shapes = set(obj)
    result = {}
    for shp in shapes:
        pattern = r'\.vtx\[\d+(?::\d+)?\]'
        vertexNumbers = []
        for i in sel:
            try:
                temp = re.search(pattern, i.name())
                vertexNumbers.append(temp.group())
            except:
                continue
        result[shp.getParent().name()] = vertexNumbers
    return result


def getSubJoint(startJnt: str, endJoint: str) -> list:
    """ Get the sub joints from the start joint to the end joint. 
    The end joint is not included.
     """
    if not isinstance(startJnt, pm.PyNode):
        startJnt = pm.PyNode(startJnt)
    result = [startJnt]
    subJnt = pm.listRelatives(startJnt, c=True, type="joint")
    if subJnt and not (endJoint in subJnt):
        result += getSubJoint(subJnt[0], endJoint)
        # for i in subJnt:
        #     result += getSubJoint(i, endJoint)
    return result


def orientJoints(*args, **kwargs) -> None:
    """ Select joints and don't put anything in the argument, 
    it will be oriented with the Maya default settings.

    args
    ----
    - Args are joints or
    - Selected joints

    kwargs
    ------
    - If there are no Args, Maya default settings are used : 
        1. primary: "xyz"
        2. secondary: "yup"
    - Mixamo Settings is : 
        1. primary: "yzx"
        2. secondary: "zup"
    - Especially, If it's "Left hand" : 
        1. primary: "yxz"
        2. secondary: "zdown"

    Examples
    --------
    >>> orientJoints()
    >>> orientJoints("joint1", "joint4")
    >>> orientJoints("joint1", "joint2", primary="yzx", secondary="zup")
    >>> orientJoints(*["joint1", "joint2"], p="yzx", s="zup")
     """
    sel = [pm.PyNode(i) for i in args] if args else pm.selected(type=["joint"])
    flags = {
        "primary": ["xyz", "yzx", "zxy", "zyx", "yxz", "xzy", "none"], 
        "p": ["xyz", "yzx", "zxy", "zyx", "yxz", "xzy", "none"], 
        "secondary": ["xup", "xdown", "yup", "ydown", "zup", "zdown", "none"], 
        "s": ["xup", "xdown", "yup", "ydown", "zup", "zdown", "none"], 
        }
    primary = "xyz"
    secondary = "yup"
    for k, v in kwargs.items():
        if ("primary"==k or "p"==k) and v in flags[k]:
            primary = v
        elif ("secondary"==k or "s"==k) and v in flags[k]:
            secondary = v
        else:
            continue
    pm.makeIdentity(sel, a=True, jo=True, n=0)
    for jnt in sel:
        pm.joint(jnt, 
                 edit=True, 
                 children=True, 
                 zeroScaleOrient=True, 
                 orientJoint=primary, 
                 secondaryAxisOrient=secondary, 
                 )
        allDescendents = pm.listRelatives(jnt, ad=True, type="joint")
        endJoints = [i for i in allDescendents if not i.getChildren()]
        for i in endJoints:
            pm.joint(i, e=True, oj='none', ch=True, zso=True)


def createPolevectorJoint(*args) -> list:
    """ Select three joints.
    Put the pole vector at 90 degrees to the direction 
    of the first and last joints.

    Examples: 
    >>> createPolevectorJoint("joint1", "joint2", "joint3")
    >>> [polevectorJoint1, polevectorJoint2]
     """
    sel = args if args else pm.selected()
    if len(sel) != 3:
        pm.warning("Three joints needed.")
        return
    jntPosition = [getPosition(i) for i in sel]
    middleJnt, endJnt = sel[1:3]
    result = []
    pm.select(cl=True)
    result = [pm.joint(p=pos) for pos in jntPosition[::2]]
    newJnt = result[0]
    orientJoints(*result, d=True)
    pm.aimConstraint(endJnt, newJnt, o=(0,0,90), wut='object', wuo=middleJnt)
    pm.delete(newJnt, cn=True)
    pm.matchTransform(newJnt, middleJnt, pos=True)
    return result


def setJointsStyle(*args, **kwargs) -> None:
    """ Change the drawing style of a joint. 
    
    Kewords: 
     - 0: Bone
     - 1: Multi-child as Box
     - 2: None

    Examples: 
    >>> setJointsStyle(b=True)
    >>> setJointsStyle("joint1", n=True)
     """
    sel = args if args else pm.selected()
    flags = {
        "bone": 0, "b": 0, 
        "multiChild": 1, "mc": 1, 
        "none": 2, "n": 2
        }
    if kwargs:
        key = next(iter(kwargs))
        if key in flags and kwargs[key]:
            drawStyle = flags[key]
        else:
            drawStyle = 0
    else:
        drawStyle = 0
    for i in sel:
        try:
            pm.setAttr(f"{i}.drawStyle", drawStyle)
        except:
            continue


def createJointOnMotionPath(*args, **kwargs) -> list:
    """ Create a number of joints and apply a motionPath on the curve.

    Examples: 
    >>> createJointOnMotionPath(num=3, cuv="curve1")
    >>> ['joint1', 'joint2', 'joint3']
    >>> createJointOnMotionPath("obj1", "obj2", "obj3", num=3, cuv="curve1")
    >>> ['obj1', 'obj2', 'obj3']
     """
    # Selections or arguments
    sel = args if args else pm.selected()
    # Number of Joints
    if "numberOfJoints" in kwargs and isinstance(kwargs["numberOfJoints"], int):
        numOfJnt = kwargs["numberOfJoints"]
    elif "num" in kwargs and isinstance(kwargs["num"], int):
        numOfJnt = kwargs["num"]
    else:
        pm.warning("NumberOfJoints flag is not an integer or invalid.")
        return
    mod = 1/(numOfJnt-1) if numOfJnt > 1 else 0
    # Curve name
    if "curve" in kwargs and pm.objExists(kwargs["curve"]):
        cuv = kwargs["curve"]
    elif "cuv" in kwargs and pm.objExists(kwargs["curve"]):
        cuv = kwargs["cuv"]
    else:
        pm.warning("Curve flag is not not exists or invalid.")
        return
    # Main
    result = []
    for i in range(numOfJnt):
        if not sel:
            pm.select(cl=True)
            obj = pm.joint(p=(0,0,0))
        elif len(sel) >= numOfJnt:
            obj = sel[i]
        elif len(sel) < numOfJnt:
            pm.warning("The input number and selection do not match.")
            continue
        else:
            continue
        uValue = i * mod
        motionPath = pm.pathAnimation(obj, c=cuv, fractionMode=True, \
                                      follow=True, followAxis='x', \
                                      upAxis='y', worldUpType='vector', \
                                      worldUpVector=(0,1,0))
        pm.cutKey(motionPath, cl=True, at='u')
        pm.setAttr(f"{motionPath}.uValue", uValue)
        result.append(obj)
    return result


def createJointOnCurveSameSpacing(**kwargs) -> list:
    """ Create joints with Same Spacing on the curve.
    Input a Curve or Select one.

    Examples:
    >>> createJointOnCurveSameSpacing(num=3)
    >>> ["joint1", "joint2", "joint3"]
    >>> createJointOnCurveSameSpacing(num=3, cuv="curve1")
    >>> ["joint1", "joint2", "joint3"]
     """
    # Number of Joints
    if "numberOfJoints" in kwargs:
        numOfJnt = kwargs["numberOfJoints"]
    elif "num" in kwargs:
        numOfJnt = kwargs["num"]
    else:
        return
    # Curve name
    if "curve" in kwargs:
        cuv = kwargs["curve"]
    elif "cuv" in kwargs:
        cuv = kwargs["cuv"]
    else:
        sel = pm.selected(dag=True, type=['nurbsCurve'])
        if sel:
            cuv = sel[0].getParent()
        else:
            return
    # Main
    pm.select(cl=True)
    joints = createJointOnMotionPath(num=numOfJnt, curve=cuv)
    if not joints:
        return
    result = []
    for i in joints:
        pm.select(cl=True)
        jnt = pm.joint(p=(0,0,0))
        pm.matchTransform(jnt, i, pos=True, rot=True, scl=True)
        result.append(jnt)
    parentHierarchically(*result)
    pm.makeIdentity(result, t=1, r=1, s=1, n=0, pn=1, jo=1, a=1)
    orientJoints(*result)
    pm.delete(joints)
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


def createSubLocator(ctrl: str) -> str:
    """ Create a locator that goes under the Controller.

    Examples: 
    >>> createWheelLocator("cc_wheelLeftFront_sub")
    >>> loc_wheelLeftFront_sub
    """
    ctrl = ctrl.name() if isinstance(ctrl, pm.PyNode) else ctrl
    if "cc_" in ctrl:
        locName = ctrl.replace("cc_", "loc_")
    else:
        locName = f"loc_{ctrl}"
    if pm.objExists(locName):
        return locName
    else:
        locator = pm.spaceLocator(n=locName)
        pm.matchTransform(locator, ctrl, pos=True)
        pm.parent(locator, ctrl)
        pm.makeIdentity(locator, a=1, t=1, r=1, s=1, n=0, pn=1)
        return locator


def createLocatorSameTargetsRotation(ctrl: str, target: str) -> str:
    """ Create a locator with the same target's rotation. 
    And goes under the controller, not target's under.

    Notes: 
    ------ 
    - Create a locator.
    - pm.matchTransform(locator, target, pos=True, rot=True)
    - pm.parent(locator, ctrl)

    Examples:  
    --------
    >>> createLocatorSameTargetsRotation("cc_neck", "jnt_neck")
    >>> "loc_neck"
     """
    if "cc_" in ctrl:
        locName = ctrl.replace("cc_", "loc_")
    else:
        locName = f"loc_{ctrl}"
    loc = pm.spaceLocator(p=(0, 0, 0), n=locName)
    pm.matchTransform(loc, target, pos=True, rot=True)
    pm.parent(loc, ctrl)
    return loc


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


def selectTopGroup(objectGroup: str, *filter) -> list:
    """ Get the top group containing arguments such as 'body' 
    among the subgroups of the selected group.

    Examples: 
    >>> selectTopGroup("vhcl_bestaB_mdl_v9999:bestaB", "body")
    >>> ["vhcl_bestaB_mdl_v9999:bestaB_body_grp"]
    >>> selectTopGroup("vhcl_bestaB_mdl_v9999:bestaB", "door", "_L", "_Ft"])
    >>> ["vhcl_bestaB_mdl_v9999:bestaB_body_door_Ft_L_grp"]
    >>> selectTopGroup("vhcl_bestaB_mdl_v9999:bestaB", *["wheel", "_L", "_Ft"])
    >>> ["vhcl_bestaB_mdl_v9999:bestaB_wheel_Ft_L_grp"]
    """
    result = []
    if not objectGroup:
        pm.warning("The argument is empty.")
    elif not pm.objExists(objectGroup):
        pm.warning(f"Object's Group <{objectGroup}> doesn't exist.")
    else:
        sel = selectGroupOnly(objectGroup)
        pm.select(cl=True)
        groups = [i for i in sel if all([f in i.name() for f in filter])]
        for grp in groups:
            if not any(j in groups for j in grp.listRelatives(p=True)):
                result.append(grp)
    pm.select(result)
    return result


def selectObjectOnly(*args) -> list:
    """ Selects only the object. 
    It also selects all objects under the selected.
     """
    if args:
        sel = pm.ls(args, dag=True, type=['mesh', 'nurbsSurface'])
    else:
        sel = pm.selected(dag=True, type=['mesh', 'nurbsSurface'])
    obj = {i.getParent() for i in sel}
    result = list(obj)
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


def parentHierarchically(*args) -> list:
    """ Hierarchically parent.
    >>> parentHierarchically(*lst)
    >>> parentHierarchically(parents, child)
     """
    sel = [pm.PyNode(i) for i in args] if args else pm.selected()
    if not sel:
        return
    for idx, parents in enumerate(sel):
        try:
            child = sel[idx + 1]
            pm.parent(child, parents)
        except:
            continue
    return sel


def groupOwnPivot(*args, **kwargs) -> list:
    """ Create a group with the same pivot.

    Examples: 
    >>> groupOwnPivot()
    >>> ["selection_grp", "selection"]
    >>> groupOwnPivot("pCube1", "pCube2")
    >>> ["pCube1_grp", "pCube1", "pCube2_grp", "pCube2"]
    >>> groupOwnPivot(*list)
    >>> ["obj1_grp", "obj1", "obj2_grp", "obj2", ...]
    >>> groupOwnPivot("pCube1", null=True)
    >>> ["pCube1_grp", "pCube1_null", "pCube1"]
    >>> groupOwnPivot("pCube1", null=True, n="newName")
    >>> ["newName_grp", "newName_null", "pCube1"]
     """
    sel = args if args else pm.selected()
    flags = {"null": False, "n": ""}
    for key, value in kwargs.items():
        if key in flags:
            flags[key] = value
        else:
            continue
    result = []
    for i in sel:
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


def softSelection() -> list:
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
    return cluster


def changeLeftToRight(inputs: str) -> str:
    """ If you input the "left", it returns the "right".

    Examples: 
    >>> changeLeftToRight('Left')
    >>> 'Right'
    >>> changeLeftToRight('Right')
    >>> 'Left'
    >>> changeLeftToRight('left')
    >>> 'right'
    >>> changeLeftToRight('right')
    >>> 'left'
    >>> changeLeftToRight('_L')
    >>> '_R'
    >>> changeLeftToRight('_R')
    >>> '_L'
     """
    inputs = inputs.name() if isinstance(inputs, pm.PyNode) else inputs
    if not inputs:
        return
    elif "Left" in inputs:
        sideA = "Left"
        sideB = "Right"
    elif "left" in inputs:
        sideA = "left"
        sideB = "right"
    elif "_L" in inputs:
        sideA = "_L"
        sideB = "_R"
    elif "Right" in inputs:
        sideA = "Right"
        sideB = "Left"
    elif "right" in inputs:
        sideA = "right"
        sideB = "left"
    elif "_R" in inputs:
        sideA = "_R"
        sideB = "_L"
    else:
        return
    result = inputs.replace(sideA, sideB)
    return result


def duplicateObj(obj: str, prefix: str="", suffix: str="") -> str:
    """ Duplictate the joint and rename it to all descendents. 
    
    Args
    ----
    - obj : Source joint
        - "Hips", "Spine", "LeftArm", ...
    - prefix : Add a prefix to the source joint.
        - "rig_Hips", "rig_Spine", "rig_LeftArm", ...
    - suffix : Add a suffix to the source joint.
        - "rig_Hips_FK", "rig_Spine_FK", "rig_LeftArm_FK", ...

    Examples
    --------
    >>> duplicateObj("Hips", "", "")
    >>> duplicateObj("Hips", "rig_", "")
    >>> duplicateObj("Hips", "", "_FK")
    >>> duplicateObj("Hips", "rig_", "_IK")
     """
    duplicated = f"{prefix}{obj}{suffix}"
    duplicated = pm.duplicate(obj, rr=True, n=duplicated)[0]
    for i in pm.listRelatives(duplicated, ad=True):
        end = i.rsplit("|", 1)[-1]
        new = i.replace(end, f"{prefix}{end}{suffix}")
        try:
            pm.rename(i, new)
        except:
            continue
    return duplicated


def stringConcatenation(name: list=[], prefix: list=[], suffix: list=[]):
    """ Naming Convention Modification.

    Args
    ----
    - Prefixing : "rig_" -> "rig_name"
    - Suffixing : "_FK" -> "name_FK"
    - Affixation = prefix + suffix

    Examples
    --------
    >>> stringConcatenation(["Hips"], ["rig_"], ["_FK", "_IK"])
    >>> ['rig_Hips_FK', 'rig_Hips_IK']
    >>> stringConcatenation(["Hips"], ["rig_"], [])
    >>> ['rig_Hips']
    >>> stringConcatenation(["Hips"], [], ["_FK", "_IK"])
    >>> ['Hips_FK', 'Hips_IK']
    >>> stringConcatenation(["Hips"])
    >>> ['Hips']
    >>> stringConcatenation()
    >>> []
     """
    result = []
    if name and prefix and suffix:
        result = [f"{p}{n}{s}" for n in name for p in prefix for s in suffix]
    elif name and prefix and not suffix:
        result = [f"{p}{n}" for n in name for p in prefix]
    elif name and not prefix and suffix:
        result = [f"{n}{s}" for n in name for s in suffix]
    elif not name and prefix and suffix:
        result = [f"{p}{s}" for p in prefix for s in suffix]
    elif not name and prefix and not suffix:
        result = [f"{p}" for p in prefix]
    elif not name and not prefix and suffix:
        result = [f"{s}" for s in suffix]
    else:
        pass
    return result


def connectBlendColor(ctrl: str, joints: list=[], \
                      t=False, r=False, s=False, v=False) -> None:
    """ Create a <blendColorNode>.
    - Connect FK, IK to color1, color2 of the <blendColorNode>.
    - Connect the output of the <blendColorNode> to the joint.
    - Connect the controller to the blender. 
    
    Args
    ----
    - ctrl : str
        - "cc_IKFK.Spine_IK0_FK1", 
        - "cc_IKFK.Left_Arm_IK0_FK1", 
        - "cc_IKFK.Right_Arm_IK0_FK1", 
        - "cc_IKFK.Left_Leg_IK0_FK1", 
        - "cc_IKFK.Right_Leg_IK0_FK1"
    - joints : list
        - sample = [
            'rig_RightUpLeg', 
            'rig_RightLeg', 
            'rig_RightFoot', 
            'rig_RightToeBase', 
            'rig_RightToe_End', 
            'rig_RightUpLeg_FK', 
            'rig_RightLeg_FK', 
            'rig_RightFoot_FK', 
            'rig_RightToeBase_FK', 
            'rig_RightToe_End_FK', 
            'rig_RightUpLeg_IK', 
            'rig_RightLeg_IK', 
            'rig_RightFoot_IK', 
            'rig_RightToeBase_IK', 
            'rig_RightToe_End_IK', 
            ]
    - t : bool (translate)
    - r : bool (rotate)
    - s : bool (scale)
    - v : bool (visibility)

    Examples
    --------
    >>> connectBlendColor("cc_IKFK.Spine_IK0_FK1", t=1, r=1)
    >>> connectBlendColor("cc_IKFK.Left_Arm_IK0_FK1", t=1, r=1)
    >>> connectBlendColor("cc_IKFK.Right_Arm_IK0_FK1", t=1, r=1)
    >>> connectBlendColor("cc_IKFK.Left_Leg_IK0_FK1", joints, t=1, r=1)
    >>> connectBlendColor("cc_IKFK.Right_Leg_IK0_FK1", joints, t=1, r=1)
        """
    sel = joints if joints else pm.selected()
    if len(sel) % 3:
        return
    else:
        mod = len(sel) // 3
        joint = sel[0 : mod*1]
        jntFK = sel[mod : mod*2]
        jntIK = sel[mod*2 : mod*3]
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        for fk, ik, jnt in zip(jntFK, jntIK, joint):
            blColor = pm.shadingNode("blendColors", au=True)
            pm.connectAttr(f"{fk}.{i}", f"{blColor}.color1", f=True)
            pm.connectAttr(f"{ik}.{i}", f"{blColor}.color2", f=True)
            pm.connectAttr(f"{blColor}.output", f"{jnt}.{i}", f=True)
            pm.connectAttr(ctrl, f"{blColor}.blender")


def mirrorCopy(obj: str, mirrorPlane: str="YZ") -> list:
    """ Mirror copy based on 'YZ' or 'XY'. Default mirrorPlane is "YZ".
    This function is shown below.
    - First, Check Selection.
    - Duplicate and Grouping own Pivot.
    - Move Groups to Other Side.
    - Creates a Mirror Shape.
    - Finish and Clean up. 

    Examples: 
    >>> mirrorCopy()
    >>> Error
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
    replaced = changeLeftToRight(obj)
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
    if mirrorPlane == "XY":
        tz *= -1
        rz += (180 if rz < 0 else -180)
    elif mirrorPlane == "YZ":
        tx *= -1
        rx += (180 if rx < 0 else -180)
        ry *= -1
        rz *= -1
    else:
        return
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


def createRigGroups(assetName: str="") -> list:
    """ Create a Group Tree used by Madman Company.

    Return
    ------
    >>> ['assetName', 'rig', 'MODEL', 'controllers', 'skeletons', 
    'geoForBind', 'extraNodes', 'bindBones', 'rigBones']

     """
    grpNames = {
        "assetName": ["rig", "MODEL"], 
        "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
        "skeletons": ["bindBones", "rigBones"]
        }
    if assetName:
        grpNames[assetName] = grpNames.pop("assetName")
        grpNames = {k: grpNames[k] for k in [assetName, "rig", "skeletons"]}
    for parents, children in grpNames.items():
        if not pm.objExists(parents):
            pm.group(em=True, n=parents)
        for child in children:
            if not pm.objExists(child):
                pm.group(em=True, n=child)
            pm.parent(child, parents)
    result = getFlattenList(grpNames)
    return result


def MovePointNearObject(sourceObject: str, *arg) -> None:
    """ The selected point moves to the closest point 
    on the source object. This function only works for points on -X.
    The Selected Points move to the closest points possible, 
    the objects should overlap as much as possible.
    
    Examples:
        >>> moveNearbyPoint("pSphere1", "pSphere2.vtx[:23]")
        >>> moveNearbyPoint("pSphere1")
     """
    sel = arg if arg else pm.selected(fl=True)
    if not isinstance(sourceObject, pm.PyNode):
        src = pm.PyNode(sourceObject)
    sourceVertices = {i.name(): pm.pointPosition(i) for i in src.vtx[:]}
    for i in sel:
        if not isinstance(i, pm.MeshVertex):
            pm.warning("Please, Select a Vertices.")
            continue
        temp = {}
        iPos = pm.pointPosition(i)
        x = iPos[0]
        if x >= 0:
            continue
        else:
            for srcVtx, srcVtxPos in sourceVertices.items():
                distance = math.sqrt(sum((a - b)**2 \
                                         for a, b in zip(iPos, srcVtxPos)))
                temp[srcVtx] = distance
        minimumKey = min(temp, key=temp.get)
        pm.move(i, sourceVertices[minimumKey])


def lineUpCurvePointsToStraightLine(*args) -> list:
    """ Arrange the points in a straight line.
    Use the equation of a straight line in space 
    to make a curved line a straight line.

    Examples: 
    >>> LineUpCurvePointsToStraightLine()
    >>> ["curve2"]
    >>> LineUpCurvePointsToStraightLine("curve1", "curve2")
    >>> ["curve3", "curve4"]
    """
    sel = args if args else pm.selected()
    if not sel:
        pm.warning("Please, Select a Curve.")
        return
    result = []
    for cuv in sel:
        curveVertices = pm.ls(f"{cuv}.cv[*]", fl=True)
        if len(curveVertices) < 2:
            pm.warning("Please, Select Curve Points.")
            continue
        startPoint = curveVertices[0]
        lastPoint = curveVertices[-1]
        x1, y1, z1 = startPoint.getPosition(space="world")
        x2, y2, z2 = lastPoint.getPosition(space="world")
        A, B, C = (x2 - x1), (y2 - y1), (z2 - z1)
        x, y, z = sympy.symbols('x y z')
        expr1 = sympy.Eq(B*x - A*y, B*x1 - A*y1)
        expr2 = sympy.Eq(C*y - B*z, C*y1 - B*z1)
        expr3 = sympy.Eq(A*z - C*x, A*z1 - C*x1)
        biggestGap = max([abs(i) for i in [A, B, C]])
        if abs(A) == biggestGap:
            idx = 0
            biggestGapAxis = x
            variables = [y, z]
            expr = [expr1, expr3]
        elif abs(B) == biggestGap:
            idx = 1
            biggestGapAxis = y
            variables = [x, z]
            expr = [expr1, expr2]
        elif abs(C) == biggestGap:
            idx = 2
            biggestGapAxis = z
            variables = [x, y]
            expr = [expr2, expr3]
        else:
            continue
        originalCurve = pm.ls(curveVertices, o=True)
        copiedCurve = pm.duplicate(originalCurve, rr=True)
        copiedCurve = copiedCurve[0]
        copiedCurveVertices = pm.ls(f"{copiedCurve}.cv[*]", fl=True)
        for i in copiedCurveVertices:
            pointPosition = i.getPosition(space="world")
            idx, biggestGapAxis, variables, expr, [x, y, z]
            value = pointPosition[idx]
            fx = [i.subs(biggestGapAxis, value) for i in expr]
            position = sympy.solve(fx, variables)
            position[biggestGapAxis] = value
            finalPosition = [round(float(position[i]), 4) for i in [x, y, z]]
            pm.move(i, finalPosition)
        result.append(copiedCurve)
    return result


def lineUpObjectsOnOnePlane(*arg) -> list:
    """ The three selected objects create a surface in space.
    And the last points are placed on this surface.
    Select 4 or more objects for this function to be effective.
    - Used to make the finger joints line up in space.
    - Ball and toe joints can be placed in a straight line 
    on the surface formed by the pelvis, knees, and ankles.

    Examples: 
    >>> lineUpObjectsOnOnePlane()
    >>> ["obj4"]
    >>> lineUpObjectsOnOnePlane("obj1", "obj2", "obj3", "obj4", "obj5")
    >>> ["obj4", "obj5"]
     """
    sel = [pm.PyNode(i) for i in arg] if arg else pm.selected()
    if len(sel) < 4:
        pm.warning("Select 4 or more objects.")
        return
    parentsInfo = {i: i.getParent() for i in sel}
    transformNodes = []
    for child, parents in parentsInfo.items():
        try:
            pm.parent(child, w=True)
            transformNode = child.getParent()
            if transformNode:
                transformNodes.append(transformNode)
        except:
            continue
    mainDots = sel[:3]
    lastDots = sel[3:]
    mainDotsPos = [pm.xform(i, q=1, t=1, ws=1) for i in mainDots]
    face = pm.polyCreateFacet(p=mainDotsPos)
    info = pm.polyInfo(face, fn=True)
    stripInfo = info[0].split(":")[-1].strip()
    normalVector = [float(i) for i in stripInfo.split(" ")]
    pm.delete(face)
    planePoint = mainDotsPos[0]
    for i in lastDots:
        pointOfLine = pm.xform(i, q=True, t=True, ws=True)
        planeNormal = np.array(normalVector)
        planePoint = np.array(planePoint)
        lineDirection = np.array(normalVector)
        linePoint = np.array(pointOfLine)
        delta1 = np.dot(planeNormal, (planePoint - linePoint)) 
        delta2 = np.dot(planeNormal, lineDirection)
        lean = delta1 / delta2
        intersectionPoint = pointOfLine + (lean*lineDirection)
        pm.move(i, intersectionPoint)
    for child, parents in parentsInfo.items():
        try:
            pm.parent(child, parents)
        except:
            continue
    pm.delete(transformNodes)
    return lastDots


def reName(*args) -> list:
    """If there
        - is one argument, create a new name, 
        - are two arguments, replace a specific word.

    Examples: 
        >>> reName("obj_001")
        >>> ["obj_001", "obj_002", "obj_003"]

        >>> reName("Apple", "Banana")
        >>> ["Banana"]

        >>> reName("obj_001")
        >>> Warning: ['oldName' -> 'obj_001'] aleady exists.
         """
    numberOfArgs = len(args)
    result = []
    if numberOfArgs == 0:
        return
    elif numberOfArgs == 1:
        newName = args[0]
        nameSlices = re.split(r'(\d+)', newName)
        nameSlices = [i for i in nameSlices if i]
        numberInfo = {j: k for j, k in enumerate(nameSlices) if k.isdigit()}
        if numberInfo:
            sel = pm.selected(fl=True)
            idx = max(numberInfo)
            nDigit = len(numberInfo[idx])
            number = int(numberInfo[idx])
            for i, obj in enumerate(sel):
                increasedNumber = f"%0{nDigit}d" % (number + i)
                nameSlices[idx] = increasedNumber
                finalName = ''.join(nameSlices)
                if pm.objExists(finalName):
                    pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                    continue
                else:
                    pm.rename(obj, finalName)
                    result.append(finalName)
        else:
            sel = pm.selected(fl=True)
            for i, obj in enumerate(sel):
                finalName = ''.join(nameSlices) + str(i)
                if pm.objExists(finalName):
                    pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                    continue
                else:
                    pm.rename(obj, finalName)
                    result.append(finalName)
    elif numberOfArgs == 2:
        originalWord, wordToChange = args
        sel = pm.selected(fl=True)
        for i in sel:
            obj = i.name()
            finalName = obj.replace(originalWord, wordToChange)
            if pm.objExists(finalName):
                pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                continue
            else:
                pm.rename(obj, finalName)
                result.append(finalName)
    else:
        return
    return result


def createPaintWeightToOne(maxInfluence: int, *args) -> None:
    """ Paint Skin Weights to One.
     - Create paintSkinWeights with value 1.
     - Create a dictionary with the vertex weight values in this way.
     - Paint the skin weights with the given max influence.
     - Finally, Create paint skin weights from the dictionary.
     """
    sel = [pm.PyNode(i) for i in args] if args else pm.selected()
    # Create a list of objects and joints.
    joints = []
    objects = []
    for i in sel:
        shp = i.getShape()
        if shp and pm.ls(shp, type=["mesh", "nurbsSurface"]):
            objects.append(i)
        elif i.type() == "joint":
            joints.append(i)
        else:
            continue
    # Get vertex information and paint skin weight with max influence.
    for obj in objects:
        data = {}
        isSkinCluster = pm.listHistory(obj, type="skinCluster")
        if isSkinCluster:
            pm.warning("skinCluster aleady exists.")
            continue
        skinClt = pm.skinCluster(joints, obj, \
                                 toSelectedBones=True, 
                                 bindMethod=0, 
                                 skinMethod=0, 
                                 normalizeWeights=1, wd=0, mi=1
                                 )
        for jnt in joints:
            pm.select(cl=True)
            pm.skinCluster(skinClt, e=True, siv=jnt)
            data[jnt] = getVertexNumber()
        pm.select(cl=True)
        pm.skinCluster(obj, e=True, mi=maxInfluence)
        # Unlock
        lockWeights = []
        for j in data.keys():
            lockWeights.append(pm.getAttr(f"{j}.liw"))
            pm.setAttr(f"{j}.liw", 0)
        for jntName, obj_vtxList in data.items():
            for obj, vtxList in obj_vtxList.items():
                if not pm.objExists(obj):
                    continue
                for vtx in vtxList:
                    objVtx = f"{obj}{vtx}"
                    skinClt = pm.listHistory(objVtx, type="skinCluster")
                    try:
                        # Paint Skin Weights to One.
                        pm.skinPercent(skinClt[0], objVtx, \
                                       transformValue=(jntName, 1))
                        pm.displayInfo(f"{objVtx} was painted successfully.")
                    except:
                        pm.warning(f"{objVtx} failed to be painted.")
                        continue
        # Lock Weights again.
        for j, onOff in zip(data.keys(), lockWeights):
            pm.setAttr(f"{j}.liw", onOff)


def createJointScaleExpression(*args, **kwargs) -> str:
    """ As the length of the curve increases, 
    the length of the joint also increases.
    Select at least 3 or more.

    Usage: 
     - Select the start joint
     - Select the end joint
     - Select the curve

    Example: 
    >>> createJointScaleExpression()
    >>> createJointScaleExpression("startJnt", "endJnt", "curve1", x=True)
    >>> createJointScaleExpression(x=True, y=True)
    >>> createJointScaleExpression(*["startJnt", "endJnt", "curve1"])
     """
    sel = args if args else pm.selected()
    if len(sel) < 3:
        return
    startJnt = sel[0]
    endJnt = sel[-2]
    cuv = pm.ls(sel, dag=True, type=["nurbsCurve"])
    if cuv:
        cuv = cuv[0]
    else:
        pm.warning("There is no Curve.")
        return
    scales = []
    if kwargs:
        for i in kwargs.keys():
            if (i == "x" or i == "X") and kwargs[i]:
                scales.append("X")
            if (i == "y" or i == "Y") and kwargs[i]:
                scales.append("Y")
            if (i == "z" or i == "Z") and kwargs[i]:
                scales.append("Z")
    else:
        scales.append("X")
    cuvInf = pm.shadingNode("curveInfo", au=True)
    pm.connectAttr(f"{cuv}.worldSpace[0]", f"{cuvInf}.inputCurve", f=True)
    cuvLen = pm.getAttr(f"{cuvInf}.arcLength")
    muldvd = pm.shadingNode("multiplyDivide", au=True)
    pm.setAttr(f"{muldvd}.operation", 2)
    pm.setAttr(f"{muldvd}.input2X", cuvLen)
    pm.connectAttr(f"{cuvInf}.arcLength", f"{muldvd}.input1X", f=True)
    joints = getSubJoint(startJnt, endJnt)
    for jnt in joints:
        for scl in scales:
            pm.connectAttr(f"{muldvd}.outputX", f"{jnt}.scale{scl}", f=True)
    return muldvd


def colorize(*args, **kwargs) -> None:
    """ Color an Object.
    
    args
    ----
    - args if args else pm.selected()

    kwargs
    ------
    - "blue": 6, 
    - "blue2": 18, 
    - "pink": 9, 
    - "red": 13, 
    - "red2": 21, 
    - "green": 14, 
    - "green2": 23, 
    - "yellow": 17,
    
    Examples
    --------
    >>> colorize(red=True)
    >>> colorize("pCube1", red=True)
    >>> colorize("pCube1", "pCube2", red=True)
    >>> colorize(*["pCube1", "pCube2"], red=True)
     """
    sel = args if args else pm.selected()
    if not sel or not kwargs:
        return
    colorBar = {
        "blue": 6, 
        "blue2": 18, 
        "pink": 9, 
        "red": 13, 
        "red2": 21, 
        "green": 14, 
        "green2": 23, 
        "yellow": 17
        }
    idx = [colorBar[j] for j, k in kwargs.items() if j in colorBar and k]
    for obj in sel:
        try:
            obj = pm.PyNode(obj)
            shp = obj.getShape()
            pm.setAttr(f"{shp}.overrideEnabled", 1)
            for i in idx:
                pm.setAttr(f"{shp}.overrideColor", i)
        except:
            continue


def deletePlugins() -> None:
    """ Attempt to delete unused plugins. """
    unknownList = pm.ls(type="unknown")
    pm.delete(unknownList)
    pluginList = pm.unknownPlugin(q=True, l=True)
    if not pluginList:
        print("There are no unknown plugins.")
    else:
        for j, k in enumerate(pluginList):
            pm.unknownPlugin(k, r=True)
            print(f"{j} : {k}")


class Controllers:
    def __init__(self):
        """ Create Curve Controllers for rig """
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
                (165, 0, -195), (0, 0, -276), (-165, 0, -195), (-165, 0, -0), 
                (-165, -0, 195), (-0, -0, 276), (165, -0, 195), (165, -0, 0), 
                (165, 0, -195)
                ], 
            "car3": [
                (-92, 0, -300), (-193, 0, -200), (-193, 0, 0), 
                (-193, 0, 200), (-92, 0, 300), (92, 0, 300), 
                (193, 0, 200), (193, 0, 0), (193, 0, -200), 
                (92, 0, -300), (-92, 0, -300)
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

        Args: 
        - "arrow", "arrow2", "arrow3", "arrow4", "arrow5", "arrow6", 
        - "cap", "car", "car2", "circle", "cone", "cone2", 
        - "cross", "cube", "cylinder", 
        - "door", "door2", 
        - "foot", "foot2", 
        - "hat", "head", "hoof", "hoof2", 
        - "IKFK", 
        - "pipe", "pointer", 
        - "scapula", "sphere", "spine", "square", 

        Examples: 
        >>> createCurveControllers()
        >>> ["ctrl1", "ctrl2", "ctrl3", ...]
        >>> createCurveControllers(cube="newCubeName", cone="newConeName")
        >>> ["newCubeName", "newConeName"]
        >>> createCurveControllers(**{"cube": "cubeName", "cone": "coneName"})
        >>> ["cubeName", "coneName"]
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


