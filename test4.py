import maya.cmds as cmds
import hjk3



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



def get_target_name(a):
    pass



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
print(sel)


# hjk3.group_with_pivot()
# joints = hjk3.create_joint_on_curve_path("curve2", 8)
# hjk3.parent_in_sequence(*joints)
# hjk3.create_curve_ikSpline(*joints)
# hjk3.create_ikSplineHandle("curve2", joints, scaleX=True)



# cpu = hjk3.ColorPickerUI()
# cpu.show()


dt = hjk3.Data()
for sig_cuv in sel:
    _ = sig_cuv.split(":")[-1]
    _ = _.replace("peacockA_", "cc_")
    ctrl_name = _.replace("_curve", "_1")


    ctrl_pos = dt.ctrl_shapes["sphere"]
    cc = hjk3.create_curve_from_points(*ctrl_pos, curve_name=ctrl_name)


    cmds.matchTransform(cc, sig_cuv, pos=True, rot=True)
    hjk3.group_with_pivot(cc, null=True)


    obj_grp = sig_cuv.replace("_curve", "_grp")
    cmds.parentConstraint(cc, obj_grp, mo=True, w=1.0)
    cmds.scaleConstraint(cc, obj_grp, mo=True, w=1.0)
    cmds.parentConstraint(cc, sig_cuv, mo=True, w=1.0)
    cmds.scaleConstraint(cc, sig_cuv, mo=True, w=1.0)





['char_peacockA_mdl_v9999:peacockA_signature_v_01_grp', 'char_peacockA_mdl_v9999:peacockA_signature_v_01_curve']


