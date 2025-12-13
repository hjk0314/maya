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




sel = cmds.ls(sl=True)
dt = hjk3.Data()



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
    


def create_joints_on_ref_cuv(ref_cuv):
    cuv_info = cmds.shadingNode("curveInfo", asUtility=True)
    cmds.connectAttr(f"{ref_cuv}.worldSpace[0]", f"{cuv_info}.inputCurve", f=True)
    ref_cuv_len = cmds.getAttr(f"{cuv_info}.arcLength")
    ref_cuv_len = math.floor(ref_cuv_len * 1000) / 1000
    num_jnt = ref_cuv_len // (1.574 * 8)
    num_jnt = int(num_jnt)
    cmds.delete(cuv_info)
    

    joints = hjk3.create_joint_on_curve_path(c=ref_cuv, n=num_jnt)
    ##### curve_reverse_option #####
    ##### curve_reverse_option #####
    joints.reverse()


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
    grp_name = rig_joints[0].rsplit("_", 1)[0] + "_grp"
    cmds.group(rig_joints[0], fk_joints[0], ik_joints[0], n=grp_name)
    return [fk_joints, ik_joints]




def create_fk_ctrls(fk_joints: list):
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
    hjk3.group_with_pivot(*ctrls, null=True)

    for cc, jnt in zip(ctrls, fk_joints[:-1]):
        cmds.parentConstraint(cc, jnt, mo=True, w=1.0)




def create_spline_curve_and_locators(ik_joints):
    slices =  ik_joints[0].rsplit("_", 2)
    slice = slices[0]
    splcuv = slice.replace("rig_", "splcuv_")

    cuv_and_locators = hjk3.create_curve_ikSpline(*ik_joints)
    _ = iter(cuv_and_locators.keys())
    ikspline_cuv = next(_)
    if cmds.objExists(splcuv):
        print("Spline Curve name is exists.")
        return
    cmds.rename(ikspline_cuv, splcuv)
    cmds.group(splcuv, n=splcuv+"_grp")

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
    
    return splcuv, renamed_loc




def create_ik_ctrls(ik_joints):
    splcuv, splloc = create_spline_curve_and_locators(ik_joints)
    hjk3.create_ikSplineHandle(splcuv, ik_joints, sz=True)
    






for sel_cuv in sel:
    rig_joints = create_joints_on_ref_cuv(sel_cuv)
    fk_joints, ik_joints = create_ikfk_joints(rig_joints)
    # create_fk_ctrls(fk_joints)
    create_ik_ctrls(ik_joints)

    
    






