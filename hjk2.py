""" These functions were created to speed up rigging in Maya. """


from typing import Union, Tuple
import pymel.core as pm
import math
import re
import inspect


__version__ = "Python 3.7.9"
__author__ = "HONG JINKI <hjk0314@gmail.com>"
__all__ = []


# Limit all lines to a maximum of 79 characters. ==============================
# Docstrings or Comments, limit the line length to 72 characters. ======


def with_selection(func):
    """ If there is no argument in the wrapper,
    Pass the selected object as an argument to the wrapper.
     """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    has_varargs = any(
        p.kind == inspect.Parameter.VAR_POSITIONAL for p in params
    )
    required_positional = [
        p 
        for p in params 
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]

    def wrapper(*args, **kwargs):
        if args:
            return func(*args, **kwargs)

        sel = pm.ls(sl=True, fl=True)
        if not sel:
            pm.warning("Nothing is selected.")
            return

        if has_varargs:
            return func(*sel, **kwargs)

        elif len(required_positional) == 1:
            result = {}
            for i in sel:
                key = i.name() if isinstance(i, pm.PyNode) else str(i)
                result[key] = func(i, **kwargs)
            return result

        else:
            pm.warning("Unsupported function signature for with_selection.")
            return

    return wrapper


@with_selection
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


@with_selection
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


@with_selection
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


def get_downstream(start: str, end: str) -> list:
    """ Get the downstream ``joints`` or ``objects`` 
    from the start joint to the end joint. The end is included.

    Examples
    --------
    >>> get_downstream('joint2', 'joint10')
    >>> ['joint2', 'joint3', 'joint8', 'joint9', 'joint10']

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


@with_selection
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


@with_selection
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


@with_selection
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


@with_selection
def chain_parenting(*args) -> list:
    """ Parent given nodes hierarchically in sequence.
    If no arguments are provided, use the current selection.
    Each node will become the parent of the next one in order.

    Examples
    --------
    >>> chain_parenting('joint1', 'joint2', 'joint3')
    >>> chain_parenting() # Uses current selection
    >>> ['joint1', 'joint2', 'joint3']
     """
    sel = [pm.PyNode(i) for i in args]

    result = []
    for idx, parents in enumerate(sel):
        result.append(parents.name())
        try:
            child = sel[idx + 1]
            pm.parent(child, parents)
        except:
            continue

    return result


@with_selection
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
        chain_parenting(*temp)
        try:
            pm.parent(temp[0], top_group)
        except:
            pass
        result += temp

    return result


@with_selection
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


@with_selection
def create_curve_from_positions(*args) -> str:
    """ Create a degree-3 curve 
    passing through the positions of the given objects.

    If no arguments are provided, 
    it uses the currently selected objects in Maya.

    Parameters
    ----------
    *args : pm.PyNode, optional
        Maya objects to get positions from. If empty, uses selected objects.

    Returns
    -------
    str : The name of the created curve.
    
    Examples
    --------
    >>> create_curve_from_positions(obj1, obj2, obj3)
    >>> create_curve_from_positions()  # Uses current selection
    """
    sel = [pm.PyNode(i) for i in args]
    positions = [pm.xform(i, q=True, ws=True, rp=True) for i in sel]
    result = pm.curve(ep=positions, d=3)

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


@with_selection
def create_joint_chain_on_curve(*args) -> list:
    """ Create a joint chain based on the positions of the given objects.

    This function creates joints at the world positions of the input objects,
    parents them in a chain, applies freeze, and orients the joints.

    Parameters
    ----------
    *args : pm.PyNode
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

    sel = [pm.PyNode(i) for i in args]
    for i in sel:
        pm.select(cl=True)
        jnt = pm.joint(p=(0, 0, 0))
        pm.matchTransform(jnt, i, pos=True)
        result.append(jnt)

    chain_parenting(*result)
    pm.makeIdentity(result, t=1, r=1, s=1, n=0, pn=1, jo=1, a=1)
    orient_joints(*result)

    return result


# Limit all lines to a maximum of 79 characters. ==============================
# Docstrings or Comments, limit the line length to 72 characters. ======

