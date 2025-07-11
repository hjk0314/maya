""" These functions were created to speed up rigging in Maya. """


from typing import Iterable, Optional, Union, List, Tuple
import functools
import math
import re
import inspect
import maya.cmds as cmds
import pymel.core as pm
import maya.api.OpenMaya as om2


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = []


def use_selection(func):
    """ Decorator to pass selected objects as item to the wrapped function.

    This decorator modifies the behavior of a function 
    such that if no arguments are explicitly provided when 
    calling the wrapped function, it attempts to pass the currently 
    selected objects (from `cmds.ls(fl=True, os=True)`) as arguments.

    The behavior depends on the decorated function's signature:
    - If the function accepts variable positional arguments (`*args`), 
      all selected objects will be passed as individual positional arguments.
    - If the function accepts exactly one positional argument, 
      it will be called for each selected object, 
      and the results will be returned in a dictionary where 
      keys are the selected objects and values are the func's return values.
    - Otherwise, if the function accepts a fixed number of positional args,
      the decorator will pass the first `n` selected objects, where
      `n` is the number of positional arguments the function expects.

    If no objects are selected and no arguments are provided, 
    a warning will be issued.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: The wrapped function with selection handling capabilities.

    Raises:
        RuntimeWarning: If nothing is selected and no arguments are passed.

    Examples:
        >>> @use_selection
        >>> func(*args)
        ...
        >>> @use_selection
        >>> func(obj)
        ...
        >>> @use_selection
        >>> func(item1, item2)
        ...
        >>> @use_selection
        >>> func(arg1, arg2="default")
     """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    has_varargs = any(
        p.kind == inspect.Parameter.VAR_POSITIONAL for p in params
    )
    positional_arg = [
        p 
        for p in params 
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    num_positional_arg = len(positional_arg)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            return func(*args, **kwargs)

        sel = cmds.ls(fl=True, os=True)

        if not sel:
            pm.warning("Nothing is selected.")
            return

        if has_varargs:
            return func(*sel, **kwargs)
        elif num_positional_arg == 1:
            result = {}
            for i in sel:
                result[i] = func(i, **kwargs)
            return result
        else:
            return func(*sel[:num_positional_arg], **kwargs)

    return wrapper


def alias(**alias_map):
    """ Decorator to allow aliasing of keyword args when calling a function.

    This decorator enables alternate (shortened or customized) 
    keyword arguments to be mapped to the actual parameter names 
    defined in the function signature.

    Args
    ----
    alias_map : dict
        A dictionary mapping alias names (str) to actual parameter names. 
        For example: {'a': 'x', 'b': 'y'}

    Returns
    -------
    function : 
        A wrapped version of the original function that resolves
        aliases before calling it.

    Example
    -------
    >>> @alias(rx='rangeX', ry='rangeY', rz='rangeZ')
    >>> func(rx=[0, 0, 0, 0], ry=[0, 0, 0, 0])
    ...
    >>> @alias(t="translate", r="rotate", s="sclae", v="visibility")
    >>> func(t=True, r=True, s=True, v=True)
     """
    # def decorator(func):
    #     sig = inspect.signature(func)
    #     valid_params = set(sig.parameters.keys())

    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         resolved_kwargs = {}
    #         for key, value in kwargs.items():
    #             full_key = alias_map.get(key, key)
    #             if full_key in valid_params:
    #                 resolved_kwargs[full_key] = value
    #         return func(*args, **resolved_kwargs)
    #     return wrapper
    # return decorator
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resolved_kwargs = {
                alias_map.get(k, k): v for k, v in kwargs.items()
            }
            return func(*args, **resolved_kwargs)
        return wrapper
    return decorator


@use_selection
def get_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of an object or point.

    Examples
    --------
    >>> get_position("pSphere1")
    >>> get_position("pSphere1.vtx[317]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    try:
        position = pm.pointPosition(obj_or_vtx)
    except:
        position = pm.xform(obj_or_vtx, q=1, ws=1, rp=1)
    result = [round(i, 5) for i in position]

    return tuple(result)


@use_selection
def get_bounding_box_position(obj_or_vtx: str) -> tuple:
    """ Get the coordinates of the center pivot of the boundingBox.

    Args
    ----
    1. Objects
    2. Vertices

    Examples
    --------
    >>> get_bounding_box_position("objectName")
    >>> get_bounding_box_position("objectName.vtx[0:7]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    bounding_box = pm.xform(obj_or_vtx, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = bounding_box
    x = (xMin + xMax) / 2
    y = (yMin + yMax) / 2
    z = (zMin + zMax) / 2
    result = [round(i, 5) for i in [x, y, z]]

    return tuple(result)


@use_selection
def get_bounding_box_size(obj_or_vtx: str) -> tuple:
    """ Get the length, width, and height of the bounding box.

    Args
    ----
    1. Objects
    2. Vertices

    Examples
    --------
    >>> get_bounding_box_size("objectName")
    >>> get_bounding_box_size("objectName.vtx[0:7]")
    >>> (64.60261, 67.08806, -62.83971)
     """
    bounding_box = pm.xform(obj_or_vtx, q=True, bb=True, ws=True)
    xMin, yMin, zMin, xMax, yMax, zMax = bounding_box
    x = (xMax - xMin) / 2
    y = (yMax - yMin) / 2
    z = (zMax - zMin) / 2
    result = [round(i, 5) for i in [x, y, z]]

    return tuple(result)


def get_flatten_list(data: Union[dict, list], seen=None) -> list:
    """ Flattens a list within a list. 

    Examples
    --------
    >>> get_flatten_list({'a': {'b': {'c': 1}, 'd': 2}})
    >>> ['a', 'b', 'c', 1, 'd', 2]
    >>> get_flatten_list(["a", ["b"], ["c"]], [[["d"], "e"], "f"], ...)
    >>> ['a', 'b', 'c', 'd', 'e', 'f']
     """
    if seen is None:
        seen = set()

    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key not in seen:
                seen.add(key)
                result.append(key)
            result.extend(get_flatten_list(value, seen))
    elif isinstance(data, list):
        for item in data:
            result.extend(get_flatten_list(item, seen))
    else:
        if data not in seen:
            seen.add(data)
            result.append(data)

    return result


def get_distance(
        point1: Union[tuple, list], 
        point2: Union[tuple, list]
    ) -> float:
    """ Both arguments are coordinates. 
    Returns the distance between the two coordinates.
    
    Examples
    --------
    >>> get_distance((0,0,0), (1,2,3))
    >>> get_distance([0,0,0], [1,2,3])
     """
    result = math.sqrt(sum((a - b)**2 for a, b in zip(point1, point2)))
    result = round(result, 5)

    return result


def get_referenced_list() -> list:
    """ Returns a list of groups of referenced. 
    
    Examples
    --------
    >>> get_referencedList()
    >>> [nt.Transform('vhcl_bestaB_mdl_v9999:bestaB'), ...]
     """
    references = pm.listReferences()

    if not references:
        result = []
    else:
        result = [ref.nodes()[0] for ref in references if ref.nodes()]

    return result


@use_selection
def get_downstream_path(start: str, end: str) -> list:
    """ Get the downstream ``joints`` or ``objects`` 
    from the start joint to the end joint. The end is included.

    Structure
    ---------
    joint1
        joint2
            joint3
                joint4
                    joint5
            joint8
                joint9
                    joint10
                        joint11

    Examples
    --------
    >>> get_downstream_path('joint2', 'joint10')
    >>> ['joint2', 'joint3', 'joint8', 'joint9', 'joint10']
     """
    end = pm.PyNode(end)
    result = [end.name()]

    while True:
        end = end.getParent()
        if not pm.objExists(end):
            raise ValueError(f"{end} does not exist.")
        elif end is None:
            raise ValueError(f"{end} has no parent.")
        elif "|" in end:
            raise ValueError(f"There are '|' in the name.")
        else:
            result.append(end.name())
        if end == start:
            break

    result.reverse()

    return result


@use_selection
def split_by_number(name: str) -> dict:
    """ If the name contains a number, 
    it returns a dict with the number and index.

    Examples
    --------
    >>> split_by_number("vhcl_car123_rig_v0123")
    >>> {0: 'vhcl_car', 1: '123', 2: '_rig_v', 3: '0123'}
     """
    name_slices = re.split(r'(\d+)', name)
    name_slices = [i for i in name_slices if i]
    result = {i: slice for i, slice in enumerate(name_slices)}

    return result


@use_selection
def orient_joints(*joints, **kwargs) -> None:
    """ Select joints and don't put anything in the argument, 
    it will be oriented with the Maya default settings.

    Parameters
    ----------
    - joints : str
        joint1, joint2, joint3 ...

    - kwargs: 
        - Maya default: xyz, yup
        - Mixamo: yzx, zup
        - Left hand: yxz, zdown

    Examples
    --------
    >>> orient_joints()
    >>> orient_joints("joint1", "joint4")
    >>> orient_joints("joint1", "joint2", p="yzx", s="zup")
    >>> orient_joints(*["joint1", "joint2"], p="yzx", s="zup")
     """
    sel = [pm.PyNode(i) for i in joints]

    valid_primary = {"xyz", "yzx", "zxy", "zyx", "yxz", "xzy", "none"}
    valid_secondary = {"xup", "xdown", "yup", "ydown", "zup", "zdown", "none"}

    primary = "xyz"
    secondary = "yup"

    for k, v in kwargs.items():
        if k in ("primary", "p") and v in valid_primary:
            primary = v
        elif k in ("secondary", "s") and v in valid_secondary:
            secondary = v
        else:
            pm.warning(f"Ignored invalid flag: {k}={v}")

    pm.makeIdentity(sel, a=True, jo=True, n=0)

    for jnt in sel:
        pm.joint(
            jnt,
            edit=True,
            children=False,
            zeroScaleOrient=True,
            orientJoint=primary,
            secondaryAxisOrient=secondary
        )
        all_joints = pm.listRelatives(jnt, ad=True, type="joint")
        end_joints = [j for j in all_joints if not j.getChildren()]
        for j in end_joints:
            pm.joint(j, e=True, oj='none', ch=True, zso=True)


@use_selection
def create_pole_vector_joints(*joints) -> list:
    """ Put the pole vector joint at 90 degrees to the direction 
    of the first and last joints.

    Examples
    --------
    >>> create_pole_vector_joints()
    >>> create_pole_vector_joints("joint1", "joint2", "joint3")
    >>> create_pole_vector_joints(*["joint1", "joint2", "joint3"])
    >>> ["joint1", "joint2"]
     """
    if len(joints) < 3:
        pm.warning("At least 3 joints are required.")
        return
    
    jnt_position = [pm.xform(i, q=True, ws=True, rp=True) for i in joints]
    # start_jnt = joints[0]
    middle_jnt = joints[int(len(joints)/2)]
    end_jnt = joints[-1]
    pm.select(cl=True)
    result = [pm.joint(p=pos) for pos in jnt_position[::2]]
    orient_joints(*result)
    pm.aimConstraint(
        end_jnt, 
        result[0], 
        o=(0, 0, 90), 
        wut='object', 
        wuo=middle_jnt
    )
    pm.delete(result[0], cn=True)
    pm.matchTransform(result[0], middle_jnt, pos=True)

    return result


@use_selection
def parent_in_sequence(*objs) -> list:
    """ Parent given nodes hierarchically in sequence.
    If no arguments are provided, use the current selection.
    Each node will become the parent of the next one in order.

    Examples
    --------
    >>> parent_in_sequence('joint1', 'joint2', 'joint3')
    >>> chain_parenting() # Uses current selection
    >>> ['joint1', 'joint2', 'joint3']
     """
    sel = [pm.PyNode(i) for i in objs]

    result = []
    for idx, obj in enumerate(sel):
        result.append(obj.name())
        try:
            child = sel[idx + 1]
            pm.parent(child, obj)
        except:
            continue

    return result


@use_selection
def group_with_pivot(*args, **kwargs) -> list:
    """ Create a group at the same pivot point as the object(s).
    If no arguments are given, the selected objects in Maya 
    will be grouped. Each object is grouped with its own pivot preserved.
    Optionally, a 'null' group can be inserted between the object 
    and the outer group. 
    A custom base name can also be assigned using the 'n' keyword.

    Parameters
    ----------
    - *args : Variable list of PyNodes or names of objects to group.
    - null (bool, optional): adds an extra null group inside the main group.
    - n (str, optional): Custom base name for the group and null.

    Returns
    -------
    List of newly created groups and original objects in hierarchical order.

    Examples
    --------
    >>> group_with_pivot()
    ['selection_grp', 'selection']
    >>> group_with_pivot('pCube1', 'pCube2')
    ['pCube1_grp', 'pCube1', 'pCube2_grp', 'pCube2']
    >>> group_with_pivot('pCube1', null=True)
    ['pCube1_grp', 'pCube1_null', 'pCube1']
     """
    sel = [pm.PyNode(i) for i in args]
    null_flag = kwargs.get("null", False)

    result = []
    for i in sel:
        top_group = pm.listRelatives(i, p=True)

        temp = []
        if null_flag:
            grp_names = [f"{i}_grp", f"{i}_null"]
            for name in grp_names:
                grp = pm.group(em=True, n=name)
                pm.matchTransform(grp, i, pos=True, rot=True)
                temp.append(grp.name())
        else:
            grp_name = f"{i}_grp"
            grp = pm.group(em=True, n=grp_name)
            pm.matchTransform(grp, i, pos=True, rot=True)
            temp.append(grp.name())
        temp.append(i.name())
        parent_in_sequence(*temp)
        try:
            pm.parent(temp[0], top_group)
        except:
            pass
        result += temp

    return result


@use_selection
def set_joint_style(*joints, style: str="bone") -> None:
    """
    Set the drawing style of the specified joints in Maya.

    Parameters
    ----------
    - joints : str
        Names of the joints to apply the style to. 
        If empty, uses selected joints.
    - style : str, optional
        Drawing style to apply. Options:
        - "bone": Default bone style (0)
        - "multiChild" or "box": Multi-child as box (1)
        - "none": No visual style (2)

    Examples
    --------
    >>> set_joint_style("joint1", style="bone")
    >>> set_joint_style(style="none") # applies to selection
    """
    style_map = {
        "bone": 0,
        "b": 0,
        "box": 1,
        "multiChild": 1,
        "mc": 1,
        "none": 2,
        "n": 2
        }

    draw_style = style_map.get(style, 0)
    sel = [pm.PyNode(i) for i in joints]

    for jnt in sel:
        try:
            pm.setAttr(f"{jnt}.drawStyle", draw_style)
        except Exception:
            continue


@use_selection
def create_curve_from_points(*obj_or_vtx) -> str:
    """ Create a degree-3 curve 
    passing through the points of the given objects.

    If no arguments are provided, 
    it uses the currently selected objects in Maya.

    Parameters
    ----------
    *obj_or_vtx : pm.PyNode, optional
        Maya objects to get points from. If empty, uses selected objects.

    Returns
    -------
    str : The name of the created curve.
    
    Examples
    --------
    >>> create_curve_from_points(obj1, obj2, obj3)
    >>> create_curve_from_points()  # Uses current selection
    """
    points = []
    for i in obj_or_vtx:
        i_name = i.name() if isinstance(i, pm.PyNode) else str(i)
        pos = get_position(i_name)
        points.append(pos)

    result = pm.curve(ep=points, d=3)

    return result


def create_motion_path_joints(num: int, curve: str) -> list:
    """ Create joints and distribute them evenly along a curve 
    using Maya's motion path.

    Parameters
    ----------
    - num : int
        The number of joints to create and distribute.
    - curve : str
        The name of the curve to follow with motion path.

    Returns
    -------
    list
        List of joints that were created and attached to the motion path.

    Raises
    ------
    Warning
        - If num < 1, the function will warn and return an empty list.
        - If curve doesn't exist, the func will warn and return an empty list.

    Examples
    --------
    >>> create_motion_path_joints(5, "curve1")
    >>> ["joint1", "joint2", "joint3", "joint4", "joint5"]
     """
    if not isinstance(num, int) or num < 1:
        pm.warning("Parameter 'num' must be a positive integer.")
        return []

    if not pm.objExists(curve):
        pm.warning(f"Curve '{curve}' does not exist.")
        return []

    step = 1.0 / (num - 1) if num > 1 else 0.0
    result = []

    for i in range(num):
        pm.select(cl=True)
        jnt = pm.joint(p=(0, 0, 0))
        u_value = i * step

        motion_path = pm.pathAnimation(
            jnt,
            c=curve,
            fractionMode=True,
            follow=True,
            followAxis='x',
            upAxis='y',
            worldUpType='vector',
            worldUpVector=(0, 1, 0)
        )
        pm.cutKey(motion_path, cl=True, at='u')
        pm.setAttr(f"{motion_path}.uValue", u_value)

        result.append(jnt.name())

    return result


@use_selection
def create_chain_joint(*obj_or_vtx) -> list:
    """ Create a joint chain based on the positions of the given objects.

    This function creates joints at the world positions of the input objects,
    parents them in a chain, applies freeze, and orients the joints.

    Parameters
    ----------
    *obj_or_vtx : pm.PyNode
        Objects (e.g., locators or curve points) to use as joint positions.

    Returns
    -------
    list
        List of created joint nodes.

    Examples
    --------
    >>> create_joint_chain_on_curve(obj1, obj2, obj3, ...)
    >>> ["joint1", "joint2", "joint3", ...]
     """
    result = []
    for i in obj_or_vtx:
        pm.select(cl=True)
        jnt = pm.joint(p=(0, 0, 0))
        i_name = i.name() if isinstance(i, pm.PyNode) else str(i)
        i_position = get_position(i_name)
        pm.xform(jnt, ws=True, t=i_position)
        result.append(jnt.name())

    parent_in_sequence(*result)
    pm.makeIdentity(result, t=1, r=1, s=1, n=0, pn=1, jo=1, a=1)
    orient_joints(*result)

    return result


@alias(sf="start_frame", ef="end_frame")
@use_selection
def create_animation_curves(*obj_or_vtx, **kwargs) -> list:
    """ Create animation curves 
    from object or vertex positions over a frame range.

    This function iterates through a specified frame range, retrieves the
    position of each provided object or vertex at each frame, and then
    creates a 3-degree NURBS curve using these recorded positions.

    obj_or_vtx:
        *obj_or_vtx (pm.PyNode or str): Positional arguments
            representing the objects or vertices for which to record positions.
            Can be PyNode objects or their string names.
        **kwargs: Keyword arguments for specifying the frame range.
            - start_frame (int): The starting frame of the animation range.
                Aliases: 'sf'.
            - end_frame (int): The ending frame of the animation range.
                Aliases: 'ef'.

    Returns:
        list: A list of `pymel.core.general.Curve` objects,
            each representing an animation curve created from the
            recorded positions.

    Raises:
        pm.maya.warning: If 'start_frame' or 'end_frame' (or their aliases)
            are not provided or are not integers.

    Examples:
        >>> create_animation_curves(start_frame=1, end_frame=27)
        >>> create_animation_curves(obj, sf=1, ef=27)
     """
    start_frame = kwargs.get("start_frame")
    end_frame = kwargs.get("end_frame")

    if not isinstance(start_frame, int) or not isinstance(end_frame, int):
        pm.warning("Both start_frame and end_frame must be provided as int.")
        return []

    recorded_positions = {}
    for frame in range(start_frame, end_frame + 1):
        pm.currentTime(frame)
        for i in obj_or_vtx:
            i_name = i.name() if isinstance(i, pm.PyNode) else str(i)
            pos = get_position(i_name)
            recorded_positions.setdefault(i_name, []).append(pos)

    result_curves = []
    for positions in recorded_positions.values():
        if len(positions) >= 2:
            curve = pm.curve(p=positions, d=3)
            result_curves.append(curve.name())
        else:
            pm.warning(f"Not enough points to create a curve for an item.")

    return result_curves


@alias(sf="start_frame", ef="end_frame", rot="rotation")
@use_selection
def set_key_on_range(
    object: str, 
    start_frame: int, 
    end_frame: int, 
    rotation: bool = False
) -> None:
    """ Sets keyframes for an object's translation and optional rotation 
    over a specified frame range.

    This function takes an object's name, a start frame, and an end frame. 
    It then iterates through each frame in the given range (inclusive) 
    and sets keyframes for the object's current world-space translation. 
    If the 'rotation' parameter is set to True, it also sets keyframes 
    for the object's current world-space rotation.

    Args:
        object (str): 
            The name of the object to set keyframes on. This should be a valid
            PyNode-compatible string (e.g., 'pCube1').
        start_frame (int): 
            The first frame in the range to set keyframes.
        end_frame (int): 
            The last frame in the range to set keyframes (inclusive).
        rotation (bool, optional): 
            If True, keyframes will also be set for the object's
            X, Y, and Z rotation channels. Defaults to False.

    Raises:
        pm.MayaNodeError: 
            If the provided 'object' string does not correspond to a valid
            Maya object.

    Examples:
        >>> set_key_on_range(start_frame=12, end_frame=20) # @use_selection
        >>> # @alias
        >>> set_key_on_range("pSphere1", sf=12, ef=20, rot=True) # @alias
        >>> set_key_on_range(sf=12, ef=20) # @alias, # @use_selection

     """
    obj = pm.PyNode(object)
    position = obj.getTranslation(space='world')
    if rotation:
        rotation_value = obj.getRotation(space='world')

    for frame in range(start_frame, end_frame + 1):
        pm.currentTime(frame)
        obj.translateX.setKey(value=position.x, time=frame)
        obj.translateY.setKey(value=position.y, time=frame)
        obj.translateZ.setKey(value=position.z, time=frame)
        if rotation:
            obj.rotateX.setKey(value=rotation_value.x, time=frame)
            obj.rotateY.setKey(value=rotation_value.y, time=frame)
            obj.rotateZ.setKey(value=rotation_value.z, time=frame)


@use_selection
def create_closed_curve(*obj_or_vtx) -> str:
    """ Creates a circle that passes through objects or points.

    This function takes any number of objects or vertices names as args.
    It then creates a NURBS circle and positions its control vertices (CVs)
    to pass through the specified objects or points.

    Args:
        *obj_or_vtx: Variable length argument list of objects or vertices.
                     Each argument should be a string representing the name of
                     a valid object or vertex in the scene.

    Returns:
        str: The name of the created NURBS circle object.

    Examples:
        >>> create_closed_curve("sphere1", "cube2", "pCylinder3")
        >>> create_closed_curve("obj1.vtx[0]", "obj2.vtx[1]", "obj3.vtx[2]")
     """
    positions = [get_position(i) for i in obj_or_vtx]
    circles = pm.circle(nr=(0, 1, 0), ch=False, s=len(obj_or_vtx))
    circle = circles[0]

    for idx, pos in enumerate(positions):
        pm.move(f"{circle}.cv[{idx}]", pos, ws=True)

    return circle


@use_selection
def create_aimed_curve(
        start_obj_or_vtx: str, 
        end_obj_or_vtx: str, 
        world_up_object: str=""
    ) -> str:
    """ Create a straight curve between two points and aim it at the end point.

    The curve is initially created along the X-axis at the origin and then
    translated to the 'start_obj_or_vtx' position. It is then aimed at the
    'end_obj_or_vtx'. An optional 'world_up_object' can be provided to control
    the world up vector for the aiming constraint. The resulting curve 
    is rebuilt for smoother interpolation and history is deleted.

    Args:
        start_obj_or_vtx: 
            The name of the starting object or vertex 
            (e.g., 'pSphere1', 'pCube1.vtx[0]').
        end_obj_or_vtx: 
            The name of the ending object or vertex.
        world_up_object: 
            An optional object to define the world up direction 
            for the aim constraint. If not provided, 
            a default world up will be used.

    Returns:
        str: The name of the newly created and aimed curve.

    Examples:
    >>> create_aimed_curve(obj1, obj2)
    >>> create_aimed_curve(obj1, obj2, obj3)
    >>> create_aimed_curve(obj1.vtx[23], obj2.vtx[99])
    >>> create_aimed_curve(obj1.vtx[23], obj2.vtx[99], obj3.vtx[36])
     """
    positions = [get_position(i) for i in [start_obj_or_vtx, end_obj_or_vtx]]
    start_point, end_point = positions
    length_of_curve = get_distance(start_point, end_point)

    result_curve = pm.curve(p=[(0, 0, 0), (length_of_curve, 0, 0)], d=1)
    pm.xform(result_curve, ws=True, t=start_point)

    end_point_locator = pm.spaceLocator()
    pm.move(end_point_locator, end_point)

    if not world_up_object:
        pm.aimConstraint(end_point_locator, result_curve)
    else:
        world_up_object_position = get_position(world_up_object)
        world_up_object_locator = pm.spaceLocator()
        pm.move(world_up_object_locator, world_up_object_position)
        pm.aimConstraint(
            end_point_locator, 
            result_curve, 
            worldUpType="object", 
            worldUpObject=world_up_object_locator
        )
        pm.delete(world_up_object_locator)

    pm.rebuildCurve(result_curve, d=3, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)
    pm.delete(result_curve, cn=True)
    pm.delete(end_point_locator)

    return result_curve


@use_selection
def get_deformed_shape(obj: str) -> str:
    """ Returns the original shape (including namespace) 
    and the shape resulting from the deformer 
    (without namespace or intermediate) from the transform node.

    Parameters
    ----------
    obj : str
        "char_tigerA_mdl_v9999:tigerA_body"
     """
    try:
        transform = pm.PyNode(obj)
    except pm.MayaNodeError:
        pm.warning(f"Node {obj} does not exist.")
        return None, None

    shapes = transform.getShapes(noIntermediate=False)
    original_shape = None
    deformed_shape = None

    for shp in shapes:
        if shp.intermediateObject.get():
            original_shape = shp
        else:
            deformed_shape = shp

    return original_shape, deformed_shape


@use_selection
def get_uv_coordinates(vtx_edge_face: str) -> tuple:
    """ Get the average UV coordinates for a given mesh component.

    This function calculates the average UV coordinates for a mesh vertex,
    edge, or face. For edges and faces, it averages the UVs of their
    connected vertices.

    Args
    ----
    vtx_edge_face : str
        A string representing the name of a mesh vertex, edge,
        or face (e.g., "pCube1.vtx[0]", "pCube1.e[0]",
        "pCube1.f[0]"), or a PyNode object representing one of these components.

    Returns
    -------
    tuple : 
        A tuple containing the rounded average U,V coordinates (float, float).
        Returns an empty tuple if an invalid component type is provided.

    Raises
    ------
        (No explicit raises, but pymel.PyNode may raise if name is invalid)
     """
    if isinstance(vtx_edge_face, pm.PyNode):
        item = vtx_edge_face 
    else:
        item = pm.PyNode(vtx_edge_face)

    uvs = []
    if isinstance(item, pm.MeshVertex):
        uv = item.getUV()
        uvs.append(uv)
    elif isinstance(item, pm.MeshEdge):
        points = item.connectedVertices()
        uvs += [i.getUV() for i in points]
    elif isinstance(item, pm.MeshFace):
        points = item.getVertices()
        uvs += [i.getUV() for i in points]
    else:
        pm.warning("No valid arguments supplied for uv coodinates.")
        return ()

    average_u = sum(u for u, v in uvs) / len(uvs)
    average_v = sum(v for u, v in uvs) / len(uvs)
    result_u = round(average_u, 5)
    result_v = round(average_v, 5)
    return result_u, result_v


def get_uv_coordinates_closet_object(
    obj_closet_mesh: str, mesh: str, uv_set: str = "map1"
) -> Tuple[float, float]:
    """ Get UV coordinates from the closest point on a mesh to an object.

    This function finds the closest point on the specified mesh to the
    given object's world position and then returns the UV coordinates
    at that point.

    Args
    ----
    - obj_closet_mesh : str
        The object to get the world position from.
        Can be a PyNode or a string convertible to PyNode.
    - mesh : str
        The target mesh to find the closest point on.
        Can be a PyNode or a string convertible to PyNode.
    - uv_set : str, optional
        The name of the UV set to query. Defaults to "map1".

    Returns
    -------
    tuple : 
        A tuple containing the U and V coordinates (float, float).

    Raises
    ------
    RuntimeError : 
        If the mesh has no shape node.
     """
    obj = (
        obj_closet_mesh 
        if isinstance(obj_closet_mesh, pm.PyNode) 
        else pm.PyNode(obj_closet_mesh)
    )

    obj_position = pm.xform(obj, q=True, ws=True, t=True)
    world_position = om2.MPoint(*obj_position)

    mesh_shapes = get_deformed_shape(mesh)
    mesh_shp = pm.PyNode(mesh_shapes[-1])
    if not mesh_shp:
        raise RuntimeError(f"Mesh '{mesh}' has no Shape node.")

    selection = om2.MSelectionList()
    selection.add(mesh_shp.name())
    dag_path = selection.getDagPath(0)
    mfn_mesh = om2.MFnMesh(dag_path)

    closet_point, _ = mfn_mesh.getClosestPoint(
        world_position, om2.MSpace.kWorld
    )
    u, v, _= mfn_mesh.getUVAtPoint(closet_point, om2.MSpace.kWorld, uv_set)

    return u, v


def create_follicle(obj: str, UVCoordinates: tuple, uv_set="map1") -> str:
    """ Create ``follicles`` on mesh at the positions of ``UVCoordinates``.

    Parameters
    ----------
    - mesh : str or pm.PyNode
        Mesh used to host the follicles.
    - UVCoordinates : tuple
        UVCoordinates whose positions should be converted to UV coordinates.
    - uv_set : str, optional
        UV set to query. ``map1`` by default.

    Returns
    -------
    - str : The created follicle transform nodes.

    Examples
    --------
    >>> create_follicle("tigerA", (0.8, 0.8), )
     """
    mesh = pm.PyNode(obj)
    deformed_shape = get_deformed_shape(obj)[-1]
    follicle_shape = pm.createNode("follicle")
    follicle_node = follicle_shape.getParent()

    pm.connectAttr(
        f"{follicle_shape}.outTranslate", 
        f"{follicle_node}.translate", 
        f=True
    )
    pm.connectAttr(
        f"{follicle_shape}.outRotate", 
        f"{follicle_node}.rotate", 
        f=True
    )
    pm.connectAttr(
        f"{deformed_shape}.outMesh", 
        f"{follicle_shape}.inputMesh", 
        f=True
    )
    pm.connectAttr(
        f"{mesh}.worldMatrix[0]", 
        f"{follicle_shape}.inputWorldMatrix", 
        f=True
    )
    u, v = UVCoordinates
    pm.setAttr(f"{follicle_shape}.parameterU", u)
    pm.setAttr(f"{follicle_shape}.parameterV", v)

    return follicle_node


@alias(rx="rangeX", ry="rangeY", rz="rangeZ")
def create_setRange_node(
        ctrl: str, 
        ctrl_attr: str, 
        rangeX: list=[0, 0, 0, 0], 
        rangeY: list=[0, 0, 0, 0], 
        rangeZ: list=[0, 0, 0, 0], 
    ) -> list:
    """ Create and configure a setRange node 
    connected to a controller's attribute.

    This function connects a specified controller's attribute 
    to the value inputs(valueX, valueY, valueZ) of a new setRange node. 
    It then sets the oldMin, oldMax, min, and max attributes 
    for the X, Y, and Z ranges on the setRange node.

    Args
    ----
    ctrl : str
        The name of the controller (e.g., 'pCube1').
    ctrl_attr : str
        The name of the attribute on the controller to connect.
    rangeX : list, optional 
        A list of four floats representing [oldMinX, oldMaxX, minX, maxX] for the X-axis range. Defaults to [0, 0, 0, 0].
    rangeY : list, optional 
        A list of four floats representing [oldMinY, oldMaxY, minY, maxY] for the Y-axis range. Defaults to [0, 0, 0, 0].
    rangeZ : list, optional 
        A list of four floats representing [oldMinZ, oldMaxZ, minZ, maxZ] for the Z-axis range. Defaults to [0, 0, 0, 0].

    Returns
    -------
    list : 
        A list of strings representing the full paths to the output attributes
        of the setRange node.

    Examples
    --------
    >>> create_setRange_node("ctrl", "IK0_FK1", [0, 10, 0, 1])
    # ['setRange1', 'outValueX', 'outValueY', 'outValueZ']
     """
    inputs = ['valueX', 'valueY', 'valueZ']
    outputs = ['outValueX', 'outValueY', 'outValueZ']
    range_attrs = {
        'X': ["oldMinX", "oldMaxX", "minX", "maxX"],
        'Y': ["oldMinY", "oldMaxY", "minY", "maxY"],
        'Z': ["oldMinZ", "oldMaxZ", "minZ", "maxZ"]
    }
    ranges = {
        'X': rangeX,
        'Y': rangeY,
        'Z': rangeZ
    }

    setRange_node = pm.shadingNode("setRange", au=True)

    for inp in inputs:
        pm.connectAttr(f"{ctrl}.{ctrl_attr}", f"{setRange_node}.{inp}", f=True)
    for axis, attrs in range_attrs.items():
        for attr, num in zip(attrs, ranges[axis]):
            pm.setAttr(f"{setRange_node}.{attr}", num)

    result_attr = [setRange_node.name()]
    result_attr += outputs

    return result_attr


@alias(t="translate", r="rotate", s="sclae", v="visibility")
def create_blendColor_node(
    ctrl: str, 
    ctrl_attr: str, 
    fk_joint: str, 
    ik_joint: str,
    translate: bool=False, 
    rotate: bool=False, 
    scale: bool=False, 
    visibility: bool=False
) -> list:
    """ Create blendColors nodes to blend attributes between two joints.

    This function generates blendColors nodes to seamlessly blend specified
    attributes (translate, rotate, scale, visibility) between a 'fk' (forward
    kinematics) joint and an 'ik' (inverse kinematics) joint. The blending is
    controlled by a given attribute on a control object.

    Args:
        ctrl (str): The name of the control object that drives the blend.
        ctrl_attr (str): The specific attribute on the control object used
                         as the 'blender' input for the blendColors node.
        fk_joint (str): The name of the FK joint, whose attributes will be
                        connected to 'color1' of the blendColors node.
        ik_joint (str): The name of the IK joint, whose attributes will be
                        connected to 'color2' of the blendColors node.
        translate (bool, optional): If True, blend translate attributes (tx, ty, tz).
                                    Defaults to False.
        rotate (bool, optional): If True, blend rotate attributes (rx, ry, rz).
                                 Defaults to False.
        scale (bool, optional): If True, blend scale attributes (sx, sy, sz).
                                Defaults to False.
        visibility (bool, optional): If True, blend the visibility attribute.
                                     Defaults to False.

    Returns:
        list: A list of tuples, where each tuple contains the name of the
              created blendColors node and the string "output", representing
              the output attribute of the blendColors node
              (e.g., [('blendColors1', 'output')]).

    Raises:
        RuntimeError: If any of the specified nodes or attributes do not exist
                      or connections cannot be made.
     """
    attrs = {
        "translate": translate,
        "rotate": rotate,
        "scale": scale,
        "visibility": visibility
    }
    blend_attrs = [key for key, value in attrs.items() if value]

    result = []
    for attr in blend_attrs:
        blend_node = pm.shadingNode("blendColors", au=True)
        pm.connectAttr(
            f"{ctrl}.{ctrl_attr}", f"{blend_node}.blender", force=True)
        pm.connectAttr(
            f"{fk_joint}.{attr}", f"{blend_node}.color1", force=True)
        pm.connectAttr(
            f"{ik_joint}.{attr}", f"{blend_node}.color2", force=True)
        result.append(blend_node.name())
    
    result.append("output")

    return result


@alias(ft="float_type", bt="bool_type", et="enum_type", it="integer_type", 
       p="source_ctrl_for_proxy")
def create_attributes(
    ctrl_name: str,
    attr_name: str,
    source_ctrl_for_proxy: str = "",
    keyable: bool = True,
    float_type: dict = None,
    bool_type: dict = None,
    enum_type: dict = None,
    integer_type: dict = None,
) -> None:
    """ Creates attributes on a given controller.

    Args
    ----
    ctrl_name : str
        The name of the controller to add attributes to.
    attr_name : str
        The name of the attribute to create.
    keyable : bool, optional 
        Whether the attribute is keyable. Defaults to True.
    source_ctrl_for_proxy : str, optional
        The name of the source controller for a proxy attribute. 
        Defaults to an empty string.
    float_type : dict, optional
        Additional properties for a float type attribute
        (e.g., {"at": "double", "dv": 0, "min": 0, "max": 10})
    bool_type : dict, optional
        Additional properties for a boolean type attribute
        (e.g., {"at": "bool"})
    enum_type : dict, optional
        Additional properties for an enum type attribute
        (e.g., {"at": "enum", "enumName": "World:Hips:Chest"})
    integer_type : dict, optional
        Additional properties for an integer type attribute
        (e.g., {"at": "long", "dv": 0, "min": 0, "max": 10})

    Examples
    --------
    >>> ctrl_1 = "nurbsCircle1"
    >>> ctrl_2 = "nurbsCircle2"
    >>> attr = "FK1_IK0"
    ...
    >>> ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
    >>> bt_dict = {"at": "bool"}
    >>> et_dict = {"at": "enum", "enumName": "World:Hips:Chest"}
    >>> it_dict = {"at": "long", "dv": 0}
    ...
    >>> create_attributes(ctrl_1, attr, ft=ft_dict)
    >>> create_attributes(ctrl_2, attr, ft=ft_dict, p=ctrl_1)
    ...
    >>> create_attributes(ctrl_2, attr, ft=ft_dict, p=ctrl_1)
    >>> create_attributes(ctrl_2, attr, bt=bt_dict)
    >>> create_attributes(ctrl_2, attr, et=et_dict)
    >>> create_attributes(ctrl_2, attr, it=it_dict)

    Returns
    -------
    tuple: 
        A tuple containing the controller name and the created attribute name.
     """
    kwargs = {
        "ln": attr_name,
        "k": keyable,
    }

    if float_type:
        kwargs.update(float_type)
    elif bool_type:
        kwargs.update(bool_type)
    elif enum_type:
        kwargs.update(enum_type)
    elif integer_type:
        kwargs.update(integer_type)

    if source_ctrl_for_proxy:
        kwargs["proxy"] = f"{source_ctrl_for_proxy}.{attr_name}"

    if pm.attributeQuery(attr_name, node=ctrl_name, exists=True):
        pm.deleteAttr(f"{ctrl_name}.{attr_name}")

    pm.addAttr(ctrl_name, **kwargs)

    return ctrl_name, attr_name


def create_rig_groups(group_name: str) -> list:
    """" Create a hierarchical set of rig groups in the scene.

    This function generates a predefined structure of empty Maya groups,
    parenting them according to a standard rig hierarchy. It checks for
    the existence of groups before creating them and ensures proper
    parenting.

    Args:
        group_name (str): 
            The name for the topmost group in the hierarchy.
            This will typically be the main group for the rig
            (e.g., "characterName_rig_GRP").

    Returns:
        A list of strings containing the names of all created or existing
        groups in the rig hierarchy. This list provides a flat representation
        of all groups involved.
     """
    if not group_name:
        return []
    
    names_of_all_groups = {
        group_name: ["rig", "MODEL"], 
        "rig": ["controllers", "skeletons", "geoForBind", "extraNodes"], 
        "skeletons": ["bindBones", "rigBones"]
    }
    result = [
        group_name, 
        "rig", 
        "MODEL", 
        "controllers", 
        "skeletons", 
        "geoForBind", 
        "extraNodes", 
        "bindBones", 
        "rigBones"
    ]

    for parents, children in names_of_all_groups.items():
        if not pm.objExists(parents):
            pm.group(em=True, n=parents)
        for child in children:
            if not pm.objExists(child):
                pm.group(em=True, n=child)
            pm.parent(child, parents)

    return result


@use_selection
def create_annotation(knee_jnt: str, polevector_ctrl: str) -> str:
    """ Create a temporary annotation from the knee joint to 
    the pole vector control.

    This function places an annotation at the position of the specified 
    knee joint and points it toward the pole vector control object. 
    The annotation transform's display type is set to 'template' 
    to make it non-selectable and visually distinct.

    Parameters
    ----------
    knee_jnt : str
        The name of the knee joint to serve as the base position for the annotation.
    polevector_ctrl : str
        The name of the pole vector control to which the annotation will point.

    Returns
    -------
    str
        The name of the annotation transform node created in the scene.

    Examples
    --------
    >>> create_annotation() # @use_selection
    >>> create_annotation("knee_jnt_L", "cc_poleVector_L")
    # 'annotation1'
     """
    knee_jnt_position = get_position(knee_jnt)
    annotation_shape = pm.annotate(polevector_ctrl, tx="", p=knee_jnt_position)
    annotation_transform = annotation_shape.getParent()
    pm.setAttr(f"{annotation_transform}.overrideEnabled", 1)
    pm.setAttr(f"{annotation_transform}.overrideDisplayType", 1)

    return annotation_transform


@alias(obj="object", grp="group", con="constraint", loc="locator", 
       jnt="joint", clt="cluster", cuv="nurbsCurve", ikh="ikhandle")
@use_selection
def select_only(*args, **kwargs) -> list:
    """ Select objects that match one or more specified filter types.

    Parameters
    ----------
    *args: str 
        Object names to filter. If empty, uses current selection.

    **kwargs : dict
        Supported filters (all bool, default False):
        - joint
        - ikhandle
        - constraint
        - group
        - object (mesh/nurbsSurface)
        - cluster
        - locator
        - nurbsCurve

    Returns
    -------
    List[pm.nt.Transform]
        List of filtered transform nodes.

    Examples
    --------
    >>> select_only(joint=True) # @use_selection
    >>> select_only(jnt=True, loc=True) # @use_selection, @alias
    >>> select_only('obj1', 'obj2', group=True, constraint=True)
     """
    filters = {
        "joint": kwargs.get("joint", False),
        "ikhandle": kwargs.get("ikhandle", False),
        "constraint": kwargs.get("constraint", False),
        "group": kwargs.get("group", False),
        "object": kwargs.get("object", False),
        "cluster": kwargs.get("cluster", False),
        "locator": kwargs.get("locator", False),
        "nurbsCurve": kwargs.get("nurbsCurve", False),
    }

    if not any(filters.values()):
        raise ValueError("At least one filter must be set to True.")

    result = set()

    if filters["object"]:
        shapes = pm.ls(args, dag=True, type=['mesh', 'nurbsSurface'])
        result.update(i.getParent() for i in shapes)

    if filters["nurbsCurve"]:
        curves = pm.ls(args, dag=True, type=['nurbsCurve'])
        result.update(i.getParent() for i in curves)

    if args: 
        sel = pm.ls(args, dag=True, type=["transform"]) 
    else:
        sel = pm.selected(dag=True, type=["transform"])

    for obj in sel:
        obj_type = pm.objectType(obj)
        shapes = pm.listRelatives(obj, s=True)
        node_type = pm.nodeType(shapes[0]) if shapes else None
    
        if filters["joint"] and obj_type == "joint":
            result.add(obj)

        if filters["ikhandle"] and obj_type == "ikHandle":
            result.add(obj)

        if filters["constraint"] and "Constraint" in obj_type and not shapes:
            result.add(obj)

        if filters["group"]:
            is_constraint = "Constraint" in obj_type
            is_special = obj_type in ['joint', 'ikEffector', 'ikHandle']
            if not (shapes or is_constraint or is_special):
                result.add(obj)

        if filters["cluster"] and node_type == "clusterHandle":
            result.add(obj)

        if filters["locator"] and node_type == "locator":
            result.add(obj)
    
    pm.select(result)

    return list(result)


@alias(p="prefix", s="suffix")
@use_selection
def add_affixes(*args, prefix: str = "", suffix: str = "") -> list:
    """ Add a prefix and/or suffix to each input string.

    Given one or more strings, returns a list of strings with the specified
    prefix and/or suffix added to each string. If neither prefix nor suffix 
    is provided, the string is omitted from the result.

    Args:
        *args: One or more strings to modify.
        prefix (str, optional): 
            String to prepend to each input. Defaults to "".
        suffix (str, optional): 
            String to append to each input. Defaults to "".

    Returns:
        list: A list of strings with the prefix and/or suffix applied.

    Examples:
        >>> add_affixes("item", "node", prefix="pre_")
        # ['pre_item', 'pre_node']
        >>> add_affixes("item", "node", suffix="_ctrl")
        # ['item_ctrl', 'node_ctrl']
        >>> add_affixes("item", prefix="pre_", suffix="_ctrl")
        # ['pre_item_ctrl']
     """
    result = []
    for input_string in args:
        if prefix and suffix:
            result_string = f"{prefix}{input_string}{suffix}"
        elif prefix and not suffix:
            result_string = f"{prefix}{input_string}"
        elif not prefix and suffix:
            result_string = f"{input_string}{suffix}"
        else:
            continue
        result.append(result_string)

    return result


def duplicate_with_rename(downstream_path: list, new_names: list) -> list:
    """ Duplicates the top-level object of a specified hierarchy and 
    renames specific nodes within the duplicated hierarchy.

    This function maps the original node names listed in `downstream_path` 
    to the new names in `new_names`, then renames the corresponding nodes 
    in the duplicated hierarchy. Any other nodes within the duplicated 
    hierarchy that are not included in `downstream_path` will be deleted.

    Args:
        downstream_path (list): 
            A list of original node names (short names) within the hierarchy 
            to be renamed. The first element should be the name of the 
            top-level object to be duplicated.
        new_names (list): 
            A list of new names that correspond one-to-one with the nodes 
            in `downstream_path`.

    Returns:
        list: 
            A list of the full path names of the newly created or renamed
            objects. The top-level duplicated object will be the last
            element in the list.

    Raises:
        Warning: 
            A warning is issued and the function exits if any of the names 
            in `new_names` already exist in the scene. In this case, no 
            duplication or renaming will occur.
        Exception: 
            If an unexpected error occurs during the name mapping process 
            or during Maya command execution, the error will be printed 
            to the console and the function will exit.
    
    Examples:
        >>> list_of_joints = get_downstream_path("joint1", "joint9")
        >>> renamed_joints = add_affixes(*list_of_joints, p="rig_", s="_FK")
        >>> duplicate_with_rename(list_of_joints, renamed_joints)
        # List with child nodes removed
     """
    if any([pm.objExists(i) for i in new_names]):
        pm.warning("There are duplicate names in new_names.")
        return

    try:
        name_info = {d: n for d, n in zip(downstream_path, new_names)}
    except Exception as e:
        print(e)
        return

    copied = pm.duplicate(downstream_path[0], rr=True, n=new_names[0])
    copied = copied[0]

    result = []
    for i in pm.listRelatives(copied, ad=True):
        old_name = i.rsplit("|", 1)[-1]
        if old_name in downstream_path:
            new_name = i.replace(old_name, name_info[old_name])
            result_name = pm.rename(i, new_name)
            result.append(result_name.name())
        else:
            pm.delete(i)

    result.append(copied.name())
    result.reverse()

    return result


# Limit all lines to a maximum of 79 characters. ==============================
# Docstrings or Comments, limit the line length to 72 characters. ======


