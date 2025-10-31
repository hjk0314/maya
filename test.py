import maya.cmds as cmds
import hjk3 as hjk



sel = cmds.ls(sl=True)
print(sel)



def create_locator_from_box_position():
    bbpos = hjk.get_bounding_box_position()
    loc = cmds.spaceLocator()
    cmds.xform(loc, translation=bbpos, worldSpace=True)
    return loc


def create_controller(ctrl_shape: str):
    dt = hjk.Data()
    cuv_shape = dt.ctrl_shapes[ctrl_shape]
    cuv = hjk.create_curve_from_points(*cuv_shape, d=1)
    return cuv


def create_FK_ctrl(ctrl: list, jnt: list, parent=False) -> str:
    if len(ctrl) != len(jnt):
        print("The number of controllers and joints must be the same.")
        return []

    new_ctrl = []
    for c, j in zip(ctrl, jnt):
        cmds.matchTransform(c, j, pos=True, rot=True)
        cmds.makeIdentity(c, a=True, t=0, r=0, s=1, n=0, pn=1)
        cmds.delete(c, ch=True)
        cc_name = j.replace("rig_", "cc_")
        cc_new = cmds.rename(c, cc_name)
        if parent:
            cmds.parentConstraint(cc_new, j, mo=True, w=1.0)
        new_ctrl.append(cc_new)

    new_ctrl = hjk.parent_in_sequence(*new_ctrl)
    for idx, cc in enumerate(new_ctrl):
        if idx == 0:
            print(hjk.group_with_pivot(cc, null=True))
        else:
            hjk.group_with_pivot(cc)
    
    return new_ctrl


def blend_node_create(ctrl, attr, FKs, IKs, Org):
    ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}

    hjk.create_attributes(ctrl, attr_name=attr, ft=ft_dict)
    setRange_out = hjk.create_setRange_node(f"{ctrl}.{attr}", rx=[0, 10, 0, 1])
    for f, i, o in zip(FKs, IKs, Org):
        blColor_out = hjk.create_blendColor_node(setRange_out[0], f, i, t=True)
        cmds.connectAttr(blColor_out[0], f"{o}.translate", f=True)
        blColor_out = hjk.create_blendColor_node(setRange_out[0], f, i, r=True)
        cmds.connectAttr(blColor_out[0], f"{o}.rotate", f=True)
        blColor_out = hjk.create_blendColor_node(setRange_out[0], f, i, s=True)
        cmds.connectAttr(blColor_out[0], f"{o}.scale", f=True)


def create_ikSpline_curve_and_ikSpline_handle(joints):
    curve_info = hjk.create_curve_ikSpline(*joints)
    cuv = next(iter(curve_info))
    hjk.create_ikSplineHandle(cuv, joints, scaleX=True)


def constraintParent_by_distance(ctrl_A, ctrl_B, locators):
    for loc in locators:
        locs = hjk.get_constraint_weight_by_distance(ctrl_A, ctrl_B, loc)
        A_loc, B_loc = locs
        cmds.parentConstraint(ctrl_A, f"{loc}_grp", mo=True, w=A_loc)
        cmds.parentConstraint(ctrl_B, f"{loc}_grp", mo=True, w=B_loc)


def duplicate_ctrl(ctrl: str, new_ctrl: str="") -> str:
    """ This function creates a new ctrl and matches it to the pivot position.

    Notes
    -----
        **No Decoration**

    Args
    ----
        - ctrl : str
        - new_ctrl : str

    Examples
    --------
    >>> duplicate_ctrl("cc_ankle_L_IK")
    >>> duplicate_ctrl("cc_ankle_L_IK", "cc_ankle_R_IK")
    cc_ankle_R_IK
    """
    num_of_cvs = hjk.get_curve_cv_count(ctrl)
    cvs = [f"{ctrl}.cv[{i}]" for i in range(num_of_cvs)]
    cvs_pos = hjk.get_position(*cvs)
    result = hjk.create_curve_from_points(*cvs_pos, cn=new_ctrl)
    ctrl_piv = cmds.xform(ctrl, q=True, ws=True, rp=True)
    cmds.xform(result, piv=ctrl_piv, os=True)
    cmds.parent(result, ctrl)
    cmds.makeIdentity(result, a=True, t=True, r=True, n=0, pn=1)
    cmds.parent(result, w=True)

    return result



dt = hjk.Data()
# pt = dt.ctrl_shapes["sphere"]
pt = dt.ctrl_shapes["cube"]

joint = "rig_wing_3_L_FK"

# for cuv in sel:
#     cc = hjk.create_curve_from_points(*pt, cn=f"cc_{cuv}")
#     cmds.xform(cc, scale=[0.165, 0.165, 0.165], relative=True)
#     cmds.makeIdentity(cc, scale=True, a=True, n=False, pn=True)
#     cmds.matchTransform(cc, cuv, pos=True, rot=True)
#     cc_grp = hjk.group_with_pivot(cc, null=True)
#     cc_grp = cc_grp[0][0]
#     cmds.parentConstraint(joint, cc_grp, mo=True, w=1.0)
#     mdl_grp = cuv.replace("_curve", "_grp")
#     cmds.parentConstraint(cc, mdl_grp, mo=True, w=1.0)


# for org_cuv in sel:
#     shd_cuv = org_cuv.split(":")[-1]
#     cc = hjk.create_curve_from_points(*pt, cn=f"cc_{shd_cuv}")
#     cmds.xform(cc, scale=[0.1, 0.1, 0.1], relative=True)
#     cmds.makeIdentity(cc, scale=True, a=True, n=False, pn=True)
#     cmds.matchTransform(cc, org_cuv, pos=True, rot=True)
#     cc_grp = hjk.group_with_pivot(cc, null=True)
#     cc_grp = cc_grp[0][0]
#     cmds.parentConstraint(joint, cc_grp, mo=True, w=1.0)
#     cmds.parentConstraint(cc, org_cuv, mo=True, w=1.0)