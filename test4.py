from typing import List
import maya.cmds as cmds
import hjk3
import math



bind_bones = []
bind_bones += ['root', ]
bind_bones += ['spine_1', 'spine_2', ]
bind_bones += [f'neck_{i}' for i in range(1, 9)]
bind_bones += ['head_1', ]
bind_bones += ['jaw', ]
bind_bones += ['wing_1_L_FK', 'wing_2_L_FK', 'wing_3_L_FK', ]
bind_bones += ['wing_1_R_FK', 'wing_2_R_FK', 'wing_3_R_FK', ]
bind_bones += ['tail_2', 'tail_3', 'tail_4', ]
bind_bones += ['thigh_L', 'leg_L', 'knee_L', 'ankle_L', ]
bind_bones += ['thumb_1_L', 'thumb_2_L', ]
bind_bones += ['index_1_L', 'index_2_L', 'index_3_L', 'index_4_L', ]
bind_bones += ['middle_1_L', 'middle_2_L', 'middle_3_L', 'middle_4_L', ]
bind_bones += ['pinky_1_L', 'pinky_2_L', 'pinky_3_L', 'pinky_4_L', ]
bind_bones += ['thigh_R', 'leg_R', 'knee_R', 'ankle_R', ]
bind_bones += ['thumb_1_R', 'thumb_2_R', ]
bind_bones += ['index_1_R', 'index_2_R', 'index_3_R', 'index_4_R', ]
bind_bones += ['middle_1_R', 'middle_2_R', 'middle_3_R', 'middle_4_R', ]
bind_bones += ['pinky_1_R', 'pinky_2_R', 'pinky_3_R', 'pinky_4_R']



sel = cmds.ls(sl=True)
dt = hjk3.Data()


def copy_keys_A_to_B(source, target, s_frame, e_frame):
    attributes = [
        'translateX', 'translateY', 'translateZ', 
        'rotateX', 'rotateY', 'rotateZ', 
        'scaleX', 'scaleY', 'scaleZ'
        ]
    for attr in attributes:
        source_attr = f"{source}.{attr}"
        key_times = cmds.keyframe(source_attr, t=(s_frame, e_frame), q=1, tc=1)
        if key_times:
            key_times = sorted(list(set(key_times)))
            for t in key_times:
                values = cmds.keyframe(source_attr, time=(t, t), q=1, vc=1)
                if values:
                    val = values[0]
                    # condition
                    if attr in ["translateX", "rotateY", "rotateZ"]:
                        val = val * -1
                    # condition
                    cmds.setKeyframe(target, attribute=attr, time=t, value=val)



def create_joints_on_curve(selected_curve, number_of_joints):
    pass




# hjk3.group_with_pivot()
# joints = hjk3.create_joint_on_curve_path("curve2", 8)
# hjk3.parent_in_sequence(*joints)
# hjk3.create_curve_ikSpline(*joints)
# hjk3.create_ikSplineHandle("curve2", joints, scaleX=True)



# cpu = hjk3.ColorPickerUI()
# cpu.show()



def temp_cc_for_hlkim():
    for sig_cuv in sel:
        _ = sig_cuv.split(":")[-1]
        _ = _.replace("peacockA_", "cc_")
        ctrl_name = _.replace("_curve", "_1")


        ctrl_pos = dt.ctrl_shapes["pointer_rhombus"]
        cc = hjk3.create_curve_from_points(*ctrl_pos, curve_name=ctrl_name)


        cmds.matchTransform(cc, sig_cuv, pos=True, rot=True)
        hjk3.group_with_pivot(cc, null=True)



        obj_grp = sig_cuv.replace("_curve", "_grp")
        cmds.parentConstraint(cc, obj_grp, mo=True, w=1.0)
        cmds.scaleConstraint(cc, obj_grp, mo=True, w=1.0)
        cmds.parentConstraint(cc, sig_cuv, mo=True, w=1.0)
        cmds.scaleConstraint(cc, sig_cuv, mo=True, w=1.0)
# temp_cc_for_hlkim()



def get_new_name_1(in_name):
    tmp = in_name.split(":")[-1]
    tmp = tmp.replace("peacockA_", "rig_")
    out_name = tmp.replace("_curve", "")
    return out_name
    


def create_joints_on_ref_cuv(ref_cuv, density_of_joints: float):
    cuv_info = cmds.shadingNode("curveInfo", asUtility=True)
    cmds.connectAttr(f"{ref_cuv}.worldSpace[0]", f"{cuv_info}.inputCurve", f=True)
    ref_cuv_len = cmds.getAttr(f"{cuv_info}.arcLength")
    ref_cuv_len = math.floor(ref_cuv_len * 1000) / 1000
    num_jnt = ref_cuv_len // (1.574 * density_of_joints)
    num_jnt = int(num_jnt)
    cmds.delete(cuv_info)
    

    joints = hjk3.create_joint_on_curve_path(c=ref_cuv, n=num_jnt)
    ##### curve_reverse_option #####
    ##### curve_reverse_option #####
    # joints.reverse()


    rig_name = get_new_name_1(ref_cuv)
    rig_joints = []
    for idx, jnt in enumerate(joints):
        cmds.matchTransform(jnt, ref_cuv, rot=True)
        new_name = rig_name + f"_{idx+1}"
        cmds.rename(jnt, new_name)
        rig_joints.append(new_name)
    hjk3.parent_in_sequence(*rig_joints)
    cmds.makeIdentity(rig_joints[0], t=1, r=1, s=1, n=0, pn=1, a=True)


    return rig_joints




def create_ikfk_joints(rig_joints):
    fk_joints, ik_joints = hjk3.create_joint_IKFK(*rig_joints)
    return [fk_joints, ik_joints]




def create_fk_ctrls(fk_joints: list) -> List[list]:
    num_fk = len(fk_joints)

    ctrls = []
    for idx, fk_jnt in enumerate(fk_joints):
        if idx + 1 >= num_fk:
            continue
        else:
            ctrl_name = fk_jnt.replace("rig_", "cc_")
            cc = cmds.circle(nr=(0, 0, 1), n=ctrl_name, ch=False)[0]
            size_up = 1.2
            cmds.scale(size_up, size_up, size_up, cc, r=True)
            cmds.makeIdentity(cc, t=0, r=0, s=1, n=0, pn=1)
            cmds.matchTransform(cc, fk_jnt, pos=True, rot=True)
            ctrls.append(cc)
    hjk3.parent_in_sequence(*ctrls)
    result = hjk3.group_with_pivot(*ctrls, null=True)

    for cc, jnt in zip(ctrls, fk_joints[:-1]):
        cmds.parentConstraint(cc, jnt, mo=True, w=1.0)
    
    return result




def create_spline_curve_and_locators(ik_joints):
    slices =  ik_joints[0].rsplit("_", 2)
    slice = slices[0]
    splcuv = slice.replace("rig_", "splcuv_")

    cuv_and_locators = hjk3.create_curve_ikSpline(*ik_joints, edit_point=False)
    _ = iter(cuv_and_locators.keys())
    ikspline_cuv = next(_)
    if cmds.objExists(splcuv):
        print("Spline Curve name is exists.")
        return
    cmds.rename(ikspline_cuv, splcuv)
    splcuv_grp = cmds.group(splcuv, n=splcuv+"_grp")

    locators = cuv_and_locators[ikspline_cuv]
    loc_forehead = splcuv.replace("splcuv_", "splloc_")
    renamed_loc = []
    for idx, loc in enumerate(locators):
        cmds.matchTransform(loc, ik_joints[0], rot=True)
        new_loc = loc_forehead + f"_{idx+1}"
        cmds.rename(loc, new_loc)
        renamed_loc.append(new_loc)
    splloc_grp_name = renamed_loc[0].rsplit("_", 1)[0] + "_grp"
    splloc_grp = cmds.group(em=True, n=splloc_grp_name)
    for i in renamed_loc:
        cmds.parent(i, splloc_grp)
    
    return splcuv, splcuv_grp, renamed_loc, splloc_grp




def create_ik_ctrls(ik_joints) -> List[list]:
    # first
    first_jnt = ik_joints[0]
    start_ctrl_name = first_jnt.replace("rig_", "cc_")
    ctrl_pos = dt.ctrl_shapes["pointer_rhombus"]
    start_ctrl = hjk3.create_curve_from_points(*ctrl_pos, curve_name=start_ctrl_name)
    cmds.matchTransform(start_ctrl, first_jnt, pos=True, rot=True)
    start_ctrl_list = hjk3.group_with_pivot(start_ctrl, null=True)[0]
    start_ctrl_grp, _, start_ctrl = start_ctrl_list
    hjk3.create_attributes(start_ctrl, "Stretch", bt={"at": "bool"})
    ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
    hjk3.create_attributes(start_ctrl, "IK0_FK1", ft=ft_dict)


    # end
    end_jnt = ik_joints[-1]
    end_ctrl_name = end_jnt.replace("rig_", "cc_")
    ctrl_pos = dt.ctrl_shapes["circle"]
    end_ctrl = hjk3.create_curve_from_points(*ctrl_pos, curve_name=end_ctrl_name)
    cmds.matchTransform(end_ctrl, end_jnt, pos=True, rot=True)
    cmds.scale(0.4, 0.4, 0.4, end_ctrl, r=True)
    cmds.makeIdentity(end_ctrl, t=0, r=0, s=1, jo=0, n=0, pn=1, a=True)
    end_ctrl_list = hjk3.group_with_pivot(end_ctrl, null=True)[0]
    end_ctrl_grp, _, end_ctrl = end_ctrl_list


    # middle
    mid_jnt_num = len(ik_joints) // 2
    mid_jnt = ik_joints[mid_jnt_num]
    mid_ctrl_name = mid_jnt.replace("rig_", "cc_")
    ctrl_pos = dt.ctrl_shapes["sphere"]
    mid_ctrl = hjk3.create_curve_from_points(*ctrl_pos, curve_name=mid_ctrl_name)
    cmds.scale(0.6, 0.6, 0.6, mid_ctrl, r=True)
    cmds.makeIdentity(mid_ctrl, t=0, r=0, s=1, jo=0, n=0, pn=1, a=True)
    mid_ctrl_list = hjk3.group_with_pivot(mid_ctrl, null=True)[0]
    mid_ctrl_grp, _, mid_ctrl = mid_ctrl_list
    cmds.matchTransform(mid_ctrl_grp, mid_jnt, pos=True, rot=True)
    cons = cmds.parentConstraint(start_ctrl, mid_ctrl_grp, mo=False, w=0.5)
    cons = cmds.parentConstraint(end_ctrl, mid_ctrl_grp, mo=False, w=0.5)
    cmds.delete(cons)


    # sm_ctrl
    sm_jnt_num = len(ik_joints[:mid_jnt_num]) // 2
    sm_jnt = ik_joints[sm_jnt_num]
    sm_ctrl_name = sm_jnt.replace("rig_", "cc_")
    ctrl_pos = dt.ctrl_shapes["sphere"]
    sm_ctrl = hjk3.create_curve_from_points(*ctrl_pos, curve_name=sm_ctrl_name)
    cmds.scale(0.4, 0.4, 0.4, sm_ctrl, r=True)
    cmds.makeIdentity(sm_ctrl, t=0, r=0, s=1, jo=0, n=0, pn=1, a=True)
    sm_ctrl_list = hjk3.group_with_pivot(sm_ctrl, null=True)[0]
    sm_ctrl_grp, _, sm_ctrl = sm_ctrl_list
    cmds.matchTransform(sm_ctrl_grp, sm_jnt, pos=True, rot=True)
    cons = cmds.parentConstraint(start_ctrl, sm_ctrl_grp, mo=False, w=0.5)
    cons = cmds.parentConstraint(mid_ctrl, sm_ctrl_grp, mo=False, w=0.5)
    cmds.delete(cons)


    # middle_end
    me_jnt_num = (len(ik_joints[mid_jnt_num:])//2) + mid_jnt_num
    me_jnt = ik_joints[me_jnt_num]
    me_ctrl_name = me_jnt.replace("rig_", "cc_")
    ctrl_pos = dt.ctrl_shapes["sphere"]
    me_ctrl = hjk3.create_curve_from_points(*ctrl_pos, curve_name=me_ctrl_name)
    cmds.scale(0.4, 0.4, 0.4, me_ctrl, r=True)
    cmds.makeIdentity(me_ctrl, t=0, r=0, s=1, jo=0, n=0, pn=1, a=True)
    me_ctrl_list = hjk3.group_with_pivot(me_ctrl, null=True)[0]
    me_ctrl_grp, _, me_ctrl = me_ctrl_list
    cmds.matchTransform(me_ctrl_grp, me_jnt, pos=True, rot=True)
    cons = cmds.parentConstraint(mid_ctrl, me_ctrl_grp, mo=False, w=0.5)
    cons = cmds.parentConstraint(end_ctrl, me_ctrl_grp, mo=False, w=0.5)
    cmds.delete(cons)


    cmds.parent(end_ctrl_grp, me_ctrl)
    cmds.parent(me_ctrl_grp, mid_ctrl)
    cmds.parent(mid_ctrl_grp, sm_ctrl)
    cmds.parent(sm_ctrl_grp, start_ctrl)


    result =  [
        start_ctrl_list, 
        sm_ctrl_list, 
        mid_ctrl_list, 
        me_ctrl_list, 
        end_ctrl_list
        ]
    return result



def constraint_loc_to_ctrl(ik_ctrls, locators):
    cc_s_lst, cc_sm_lst, cc_m_lst, cc_me_lst, cc_e_lst = ik_ctrls
    cc_s = cc_s_lst[2]
    cc_sm = cc_sm_lst[2]
    cc_m = cc_m_lst[2]
    cc_me = cc_me_lst[2]
    cc_e = cc_e_lst[2]

    q, r = divmod(len(locators), 2)
    a_section = locators[:q]
    b_section = locators[q:]
    if r == 0:
        print("로케이터 갯수가 짝수")
        aq = math.floor(len(a_section)/2 * 10) / 10
        aq = int(aq)
        bq = math.floor(len(b_section)/2 * 10) / 10
        bq = int(bq)
        aa_section = a_section[:aq]
        ab_section = a_section[aq:]
        ba_section = b_section[:bq]
        bb_section = b_section[bq:]
    else:
        print("로케이터 갯수가 홀수")
        aq = math.ceil(len(a_section)/2)
        bq = math.ceil(len(b_section)/2)
        aa_section = a_section[:aq]
        ab_section = a_section[aq:]
        ba_section = b_section[:bq-1]
        bb_section = b_section[bq-1:]
    for loc in aa_section:
        val, _ = hjk3.get_constraint_weight_by_distance(cc_s, cc_sm, loc)
        cmds.parentConstraint(cc_s, loc, mo=True, w=val)
    for loc in ab_section:
        val, _ = hjk3.get_constraint_weight_by_distance(cc_sm, cc_m, loc)
        cmds.parentConstraint(cc_sm, loc, mo=True, w=val)
    for loc in ba_section:
        val, _ = hjk3.get_constraint_weight_by_distance(cc_m, cc_me, loc)
        cmds.parentConstraint(cc_m, loc, mo=True, w=val)
    for idx, loc in enumerate(bb_section):
        if idx == len(bb_section) - 1:
            cmds.parentConstraint(cc_e, loc, mo=True, w=1)
        else:
            val, _ = hjk3.get_constraint_weight_by_distance(cc_me, cc_e, loc)
            cmds.parentConstraint(cc_me, loc, mo=True, w=val)


def create_follicle(mesh: str, UVCoordinates: tuple) -> str:
    """ Create ``follicles`` on mesh at the positions of ``UVCoordinates``.

    Notes
    -----
        **No Decoration**

    Args
    ----
        mesh : str
        UVCoordinates : tuple

    Examples
    --------
    >>> create_follicle("tigerA", (0.8, 0.8))
    "follicle1"
    """
    # deformed_shape = get_deformed_shape(mesh)[-1]
    deformed_shape = "peacockA_skin_geoShape"
    follicle_shape = cmds.createNode("follicle")
    follicle_node = cmds.listRelatives(follicle_shape, parent=True)[0]

    cmds.connectAttr(
        f"{follicle_shape}.outTranslate", 
        f"{follicle_node}.translate", 
        f=True
    )
    cmds.connectAttr(
        f"{follicle_shape}.outRotate", 
        f"{follicle_node}.rotate", 
        f=True
    )
    cmds.connectAttr(
        f"{deformed_shape}.outMesh", 
        f"{follicle_shape}.inputMesh", 
        f=True
    )
    cmds.connectAttr(
        f"{mesh}.worldMatrix[0]", 
        f"{follicle_shape}.inputWorldMatrix", 
        f=True
    )
    u, v = UVCoordinates
    cmds.setAttr(f"{follicle_shape}.parameterU", u)
    cmds.setAttr(f"{follicle_shape}.parameterV", v)

    return follicle_node




def create_signature_git(sel_cuv, dens: float):
    # Create Joints
    rig_joints = create_joints_on_ref_cuv(sel_cuv, dens)
    fk_jnt, ik_jnt = create_ikfk_joints(rig_joints)
    grp_name = rig_joints[0].rsplit("_", 1)[0] + "_grp"
    jnt_grp_name = cmds.group(rig_joints[0], fk_jnt[0], ik_jnt[0], n=grp_name)
    # Create FK Ctrls
    cc_fk_lists = create_fk_ctrls(fk_jnt)
    cc_fk_1_grp, cc_fk_1_null, cc_fk_1 = cc_fk_lists[0]
    # Create Curve and Locators
    cscal_nodes = create_spline_curve_and_locators(ik_jnt)
    splcuv, splcuv_grp, splloc, splloc_top_grp = cscal_nodes
    splloc_lists = hjk3.group_with_pivot(*splloc, null=True)
    splloc_grp = []
    for lst in splloc_lists:
        splloc_grp.append(lst[0])
    ikSpline_result = hjk3.create_ikSplineHandle(splcuv, ik_jnt, sz=1)
    cuvinfo, condi, multi, ikHandle = ikSpline_result
    # Create IK Ctrls
    ik_ctrls = create_ik_ctrls(ik_jnt)
    cc_s_lst, cc_sm_lst, cc_m_lst, cc_me_lst, cc_e_lst = ik_ctrls
    cc_s_grp, cc_s_null, cc_s = cc_s_lst
    cc_sm_grp, cc_sm_null, cc_sm = cc_sm_lst
    cc_m_grp, cc_m_null, cc_m = cc_m_lst
    cc_me_grp, cc_me_null, cc_me = cc_me_lst
    cc_e_grp, cc_e_null, cc_e = cc_e_lst
    hjk3.colorize(cc_s, idx=9)
    hjk3.colorize(cc_sm, idx=20)
    hjk3.colorize(cc_m, idx=18)
    hjk3.colorize(cc_me, idx=20)
    hjk3.colorize(cc_e, idx=17)
    # Constraint Locator to Ctrl
    constraint_loc_to_ctrl(ik_ctrls, splloc_grp)
    cmds.connectAttr(f"{cc_s}.Stretch", f"{condi}.firstTerm", f=True)
    # Create BlendColor Node
    node_attr = f"{cc_s}.IK0_FK1"
    setRange_node = hjk3.create_setRange_node(node_attr, rx=[0, 10, 0, 1])
    sn = setRange_node[0]
    for rig, fk, ik in zip(rig_joints, fk_jnt, ik_jnt):
        blc_nodes = hjk3.create_blendColor_node(sn, fk, ik, t=1, r=1, s=1)
        for blc, attr in zip(blc_nodes, ["translate", "rotate", "scale"]):
            cmds.connectAttr(blc, f"{rig}.{attr}", f=True)
    # Connect visibility IK, FK Ctrls
    cmds.connectAttr(sn, f"{cc_fk_lists[0][0]}.visibility", f=True)
    rev_node = cmds.shadingNode("reverse", au=True)
    cmds.connectAttr(sn, f"{rev_node}.inputX", f=True)
    cmds.connectAttr(f"{rev_node}.outputX", f"{cc_s_grp}.visibility", f=True)
    # Setting ikHandle
    cmds.setAttr(f"{ikHandle}.dTwistControlEnable", 1)
    cmds.setAttr(f"{ikHandle}.dWorldUpType", 4)
    cmds.setAttr(f"{ikHandle}.dForwardAxis", 5)
    cmds.connectAttr(f"{cc_s}.worldMatrix[0]", f"{ikHandle}.dWorldUpMatrix", f=True)
    cmds.connectAttr(f"{cc_e}.worldMatrix[0]", f"{ikHandle}.dWorldUpMatrixEnd", f=True)
    # Create follicle
    mesh = "char_peacockA_mdl_v9999:peacockA_skin_geo"
    uv = hjk3.get_uv_coordinates_closet_object(cc_s, mesh)
    follicle_name = create_follicle(mesh, uv)
    fol_name = cc_s.replace("cc_", "fol_")
    fol_name = cmds.rename(follicle_name, fol_name)
    # Skin Weights

    # Final Touch
    cc_group_name = cc_s.rsplit("_", 1)[0] + "_grp"
    cc_group_name = cmds.group(em=True, n=cc_group_name)
    cmds.matchTransform(cc_group_name, cc_s, pos=True, rot=True)
    cmds.parent(cc_s_grp, cc_group_name)
    cmds.parent(cc_fk_1_grp, cc_group_name)
    cmds.parentConstraint(fol_name, cc_group_name, mo=True, w=1.0)
    cmds.scaleConstraint("cc_sub", cc_group_name, mo=True, w=1.0)
    cmds.parent(cc_group_name, "cc_signature_grp")
    cmds.parent(jnt_grp_name, "rig_signature_grp")
    ikH_grp = splcuv_grp.split("_")
    ikH_grp[0] = "ikH"
    ikH_grp_name = "_".join(ikH_grp)
    ikH = cmds.group([splcuv_grp, splloc_top_grp, ikHandle], n=ikH_grp_name)
    if not cmds.objExists("ikH_signature_grp"):
        new_ikH = cmds.group(em=True, n="ikH_signature_grp")
        cmds.parent(new_ikH, "extraNodes")
    cmds.parent(ikH, "ikH_signature_grp")
    if not cmds.objExists("fol_signature_grp"):
        new_fol = cmds.group(em=True, n="fol_signature_grp")
        cmds.parent(new_fol, "extraNodes")
    cmds.parent(fol_name, "fol_signature_grp")
        

    tmp_sel_cuv = sel_cuv.split("_")
    tmp_sel_cuv[-1] = "grp"
    smooth_obj = "_".join(tmp_sel_cuv)
    obj_children = cmds.listRelatives(smooth_obj, children=True, fullPath=True)
    skin_obj = []
    for i in obj_children:
        if cmds.getAttr(f"{i}.visibility"):
            skin_obj.append(i)
    for j in skin_obj:
        if "rachii" in j:
            cmds.skinCluster(rig_joints[0], j, toSelectedBones=False, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=3, foc=True)
        else:
            cmds.skinCluster(rig_joints[-1], j, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=1, foc=True)





v_dens = 9.5
v_curve = []
for i in range(1, 41):
    v = "char_peacockA_mdl_v9999:peacockA_signature_v_%02d_curve" % i
    v_curve.append(v)

for vc in v_curve:
    create_signature_git(vc, v_dens)


eye_curve = [
    'char_peacockA_mdl_v9999:peacockA_signature_eye_a_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_a_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_b_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_c_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_d_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_e_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_f_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_g_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_h_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_i_16_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_16_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_j_17_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_16_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_17_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_k_18_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_16_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_17_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_18_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_l_19_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_01_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_02_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_03_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_04_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_05_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_06_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_07_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_08_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_09_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_10_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_11_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_12_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_13_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_14_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_15_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_16_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_17_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_18_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_19_curve', 'char_peacockA_mdl_v9999:peacockA_signature_eye_m_20_curve']


for i in eye_curve:
    if "_a_" in i:
        dens = 0.7
    elif "_b_" in i:
        dens = 1.5
    elif "_c_" in i:
        dens = 2.2
    elif "_d_" in i:
        dens = 3.5
    elif "_e_" in i:
        dens = 4.8
    elif "_f_" in i:
        dens = 6.0
    elif "_g_" in i:
        dens = 6.5
    elif "_h_" in i:
        dens = 7.0
    elif "_i_" in i:
        dens = 7.5
    elif "_j_" in i:
        dens = 8.0
    elif "_k_" in i:
        dens = 8.5
    elif "_l_" in i:
        dens = 9.0
    elif "_m_" in i:
        dens = 9.5
    else:
        continue
    create_signature_git(i, dens)




p_curve = []
for i in range(1, 27):
    p = "char_peacockA_mdl_v9999:peacockA_signature_p_%02d_curve" % i
    p_curve.append(p)

L_p_curve = p_curve[:13]
R_p_curve = p_curve[13:]
dens_lst = [9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 5.5, 4.5, 3.5, 3.0, 2.2]
for cuv, d in zip(L_p_curve, dens_lst):
    create_signature_git(cuv, d)

dens_lst.reverse()
for cuv, d in zip(R_p_curve, dens_lst):
    create_signature_git(cuv, d)





