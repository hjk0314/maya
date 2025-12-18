import maya.cmds as cmds
import hjk3
import math




# hjk3.group_with_pivot(null=True)


# cpu = hjk3.ColorPickerUI()
# cpu.show()


# sel = ["new_neck_%d" % i for i in range(1, 9)]
# hjk3.create_curve_ikSpline(*sel)



# hjk3.create_ikSplineHandle("curve3", sel, sy=True)


# sel = cmds.ls(sl=True)
# val1, val2 = hjk3.get_constraint_weight_by_distance(sel[0], sel[1], sel[2])
# cmds.parentConstraint(sel[0], sel[2], mo=True, w=val1)
# cmds.parentConstraint(sel[1], sel[2], mo=True, w=val2)


# ft_dict = {"at": "double", "dv": 0, "min": 0, "max": 10}
# hjk3.create_attributes_proxy("new_cc_neck_1_FK", "new_cc_head_FK", "IK0_FK1", ft=ft_dict)



# bt_dict = {"at": "bool"}
# hjk3.create_attributes_proxy("new_cc_neck_1_IK", "new_cc_neck_1_FK", "IK0_FK1", bt=bt_dict)


# sel = cmds.ls(sl=True)
# for i in sel:
#     result = hjk3.get_pointOnCurve_parameter("curve4", i)
#     result = math.floor(result * 1000) / 1000
#     print(result)


# sel = cmds.ls(sl=True)
# hjk3.replace_name(*sel, s="cc_", r="new_cc_")

# sel = cmds.ls(sl=True)
# half_num = len(sel) / 3
# half_num = int(half_num)
# rig = sel[:half_num]
# iks = sel[half_num:half_num*2]
# fks = sel[half_num*2:]
# node_attr = "new_cc_neck_1_IK.IK0_FK1"
# outputs = hjk3.create_setRange_node(node_attr, rx=[0, 10, 0, 1])
# for ik, fk, rg in zip(iks, fks, rig):
#     # outputs = ['setRange1.outValueX', 'setRange1.outValueY', ...]
#     # fk = "rig_arm_L_FK"
#     # ik = "rig_arm_L_IK"
#     blc_nodes = hjk3.create_blendColor_node(outputs[0], fk, ik, t=True, r=True, s=True)
#     # ['blendColors1.output', 'blendColors2.output', ...]
#     for bo, ri in zip(blc_nodes, [f"{rg}.translate", f"{rg}.rotate", f"{rg}.scale"]):
#         cmds.connectAttr(bo, ri, f=True)



