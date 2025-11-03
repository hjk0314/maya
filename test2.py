import maya.cmds as cmds
import hjk3 as hjk



sel = cmds.ls(sl=True)
print([i for i in sel])

bones = ['root', 'chest', 'head', 'head_end', 'eye_L', 'eye_L_end', 'eye_R', 'eye_R_end', 'feeler_L_1', 'feeler_L_2', 'feeler_L_3', 'feeler_L_4', 'feeler_L_5', 'feeler_L_6', 'feeler_L_7', 'feeler_L_8', 'feeler_L_9', 'feeler_L_10', 'feeler_L_11', 'feeler_L_12', 'feeler_R_1', 'feeler_R_2', 'feeler_R_3', 'feeler_R_4', 'feeler_R_5', 'feeler_R_6', 'feeler_R_7', 'feeler_R_8', 'feeler_R_9', 'feeler_R_10', 'feeler_R_11', 'feeler_R_12', 'leg_LF_1', 'leg_LF_2', 'leg_LF_3', 'leg_LF_4', 'leg_LF_5', 'leg_RF_1', 'leg_RF_2', 'leg_RF_3', 'leg_RF_4', 'leg_RF_5', 'hip', 'tail_1', 'tail_2', 'tail_3', 'tail_4', 'tail_5', 'tail_6', 'tail_7', 'tail_8', 'leg_LB_1', 'leg_LB_2', 'leg_LB_3', 'leg_LB_4', 'leg_LB_5', 'leg_RB_1', 'leg_RB_2', 'leg_RB_3', 'leg_RB_4', 'leg_RB_5', 'leg_LM_1', 'leg_LM_2', 'leg_LM_3', 'leg_LM_4', 'leg_LM_5', 'leg_RM_1', 'leg_RM_2', 'leg_RM_3', 'leg_RM_4', 'leg_RM_5', 'wing_LF_1', 'wing_LF_2', 'wing_LF_3', 'wing_LF_4', 'wing_LF_5', 'wing_LF_6', 'wing_LF_7', 'wing_LB_1', 'wing_LB_2', 'wing_LB_3', 'wing_LB_4', 'wing_LB_5', 'wing_LB_6', 'wing_LB_7', 'wing_RF_1', 'wing_RF_2', 'wing_RF_3', 'wing_RF_4', 'wing_RF_5', 'wing_RF_6', 'wing_RF_7', 'wing_RB_1', 'wing_RB_2', 'wing_RB_3', 'wing_RB_4', 'wing_RB_5', 'wing_RB_6', 'wing_RB_7']


# for i in sel:
#     for j in ["translate", "rotate"]:
#         cmds.disconnectAttr(f"rig_{i}.{j}", f"{i}.{j}")


# hjk.create_curve_ikSpline(*sel)
joints = ['rig_tail_1', 'rig_tail_2', 'rig_tail_3', 'rig_tail_4', 'rig_tail_5', 'rig_tail_6', 'rig_tail_7', 'rig_tail_8']
# hjk.create_ikSplineHandle("cuv_tail", joints, sx=True)


# hjk.group_with_pivot()


# for loc in ['locator12', 'locator13', 'locator14', 'locator15']:
#     locs = hjk.get_constraint_weight_by_distance("cc_tail_1", "cc_tail_3", loc)
#     A_loc, B_loc = locs
#     cmds.parentConstraint("cc_tail_1", f"{loc}_grp", mo=True, w=A_loc)
#     cmds.parentConstraint("cc_tail_3", f"{loc}_grp", mo=True, w=B_loc)



# for loc in ['locator16', 'locator17', 'locator18']:
#     locs = hjk.get_constraint_weight_by_distance("cc_tail_3", "cc_tail_5", loc)
#     A_loc, B_loc = locs
#     cmds.parentConstraint("cc_tail_3", f"{loc}_grp", mo=True, w=A_loc)
#     cmds.parentConstraint("cc_tail_5", f"{loc}_grp", mo=True, w=B_loc)


# locs = hjk.get_constraint_weight_by_distance("cc_tail_1", "cc_tail_5", "cc_tail_3")
# A_loc, B_loc = locs
# cmds.parentConstraint("cc_tail_1", "cc_tail_3_grp", mo=True, w=A_loc)
# cmds.parentConstraint("cc_tail_5", "cc_tail_3_grp", mo=True, w=B_loc)
