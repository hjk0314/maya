import maya.cmds as cmds
import hjk3 as hjk



sel = cmds.ls(sl=True, fl=True)
print([i for i in sel])

bones = ['root', 'chest', 'head', 'head_end', 'eye_L', 'eye_L_end', 'eye_R', 'eye_R_end', 'feeler_L_1', 'feeler_L_2', 'feeler_L_3', 'feeler_L_4', 'feeler_L_5', 'feeler_L_6', 'feeler_L_7', 'feeler_L_8', 'feeler_L_9', 'feeler_L_10', 'feeler_L_11', 'feeler_L_12', 'feeler_R_1', 'feeler_R_2', 'feeler_R_3', 'feeler_R_4', 'feeler_R_5', 'feeler_R_6', 'feeler_R_7', 'feeler_R_8', 'feeler_R_9', 'feeler_R_10', 'feeler_R_11', 'feeler_R_12', 'leg_LF_1', 'leg_LF_2', 'leg_LF_3', 'leg_LF_4', 'leg_LF_5', 'leg_RF_1', 'leg_RF_2', 'leg_RF_3', 'leg_RF_4', 'leg_RF_5', 'hip', 'tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_8', 'leg_LB_1', 'leg_LB_2', 'leg_LB_3', 'leg_LB_4', 'leg_LB_5', 'leg_RB_1', 'leg_RB_2', 'leg_RB_3', 'leg_RB_4', 'leg_RB_5', 'leg_LM_1', 'leg_LM_2', 'leg_LM_3', 'leg_LM_4', 'leg_LM_5', 'leg_RM_1', 'leg_RM_2', 'leg_RM_3', 'leg_RM_4', 'leg_RM_5', 'wing_LF_1', 'wing_LF_2', 'wing_LF_3', 'wing_LF_4', 'wing_LF_5', 'wing_LF_6', 'wing_LF_7', 'wing_LB_1', 'wing_LB_2', 'wing_LB_3', 'wing_LB_4', 'wing_LB_5', 'wing_LB_6', 'wing_LB_7', 'wing_RF_1', 'wing_RF_2', 'wing_RF_3', 'wing_RF_4', 'wing_RF_5', 'wing_RF_6', 'wing_RF_7', 'wing_RB_1', 'wing_RB_2', 'wing_RB_3', 'wing_RB_4', 'wing_RB_5', 'wing_RB_6', 'wing_RB_7']


# for i in sel:
#     for j in ["translate", "rotate"]:
#         cmds.disconnectAttr(f"rig_{i}.{j}", f"{i}.{j}")


# hjk.create_curve_ikSpline(*sel)
# hjk.create_ikSplineHandle("cuv_wing_LB", sel, sx=True)


# hjk.group_with_pivot()


dt = hjk.Data()
# cc = dt.ctrl_shapes["sphere"]
# hjk.create_curve_from_points(*cc)


# for i in sel[1:-1]:
#     locs_weights = hjk.get_constraint_weight_by_distance(sel[0], sel[-1], i)
#     weights_A, weights_B = locs_weights
#     cmds.parentConstraint(sel[0], f"{i}_grp", mo=True, w=weights_A)
#     cmds.parentConstraint(sel[-1], f"{i}_grp", mo=True, w=weights_B)


# bt_dict = {"at": "bool"}
# for attr in ["Sub_Ctrl"]:
#     hjk.create_attributes_proxy("cc_feeler_R_1", "cc_feeler_R_6", attr, bt=bt_dict)
#     hjk.create_attributes_proxy("cc_feeler_R_6", "cc_feeler_R_10", attr, bt=bt_dict)


# bt_dict = {"at": "bool"}
# hjk.create_attributes_proxy(sel[0], sel[1], "Tail_Stretch", bt=bt_dict)
# hjk.create_attributes_proxy(sel[1], sel[2], "Tail_Stretch", bt=bt_dict)
# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# hjk.create_attributes_proxy(sel[0], sel[1], "IK0_FK1", ft=ft_dict)
# hjk.create_attributes_proxy(sel[1], sel[2], "IK0_FK1", ft=ft_dict)


# cpu = hjk.ColorPickerUI()
# cpu.show()


# for i in sel:
    # cmds.connectAttr(f"rig_{i}.translate", f"{i}.translate", f=True)
    # cmds.connectAttr(f"rig_{i}.rotate", f"{i}.rotate", f=True)
    # cmds.connectAttr(f"rig_{i}.scale", f"{i}.scale", f=True)

# for i in sel:
#     cmds.disconnectAttr(f"rig_{i}.translate", f"{i}.translate")
#     cmds.disconnectAttr(f"rig_{i}.rotate", f"{i}.rotate")



# A = "Mouth_Open"
# B = "MOopen_full"

# for i in sel:
#     target = i.replace(A, B)
#     i_pos = hjk.get_position(target)[0]
#     cmds.xform(i, translation=i_pos, ws=True, a=True)


