import maya.cmds as cmds
import hjk3



def ren():
    sel = cmds.ls(sl=True)
    for idx, i in enumerate(sel):
        cc = i.replace("peacockA", "cc")
        ctrl = cc.replace("_curve", "")
        # ctrl = i + "_1"
        cmds.rename(i, ctrl)
        hjk3.group_with_pivot(ctrl, null=True)

# ren()

def copy_keys_exact_locations(source, target, start_frame, end_frame):
    attributes = ['translateX', 'translateY', 'translateZ', 
                  'rotateX', 'rotateY', 'rotateZ', 
                  'scaleX', 'scaleY', 'scaleZ']
    for attr in attributes:
        source_attr = f"{source}.{attr}"
        key_times = cmds.keyframe(source_attr, time=(start_frame, end_frame), query=True, timeChange=True)

        if key_times:
            key_times = sorted(list(set(key_times)))
            for t in key_times:
                values = cmds.keyframe(source_attr, time=(t, t), query=True, valueChange=True)
                if values:
                    val = values[0]
                    # reverse point
                    if attr in ["translateX", "rotateY", "rotateZ"]:
                        val = val * -1
                    # reverse point
                    cmds.setKeyframe(target, attribute=attr, time=t, value=val)



def get_new_ctrl_name(old_name):
    b_ctrl = old_name.replace("_L_", "_R_")
    b_ctrl = b_ctrl + "_null"

    # null = cmds.listRelatives(old_name, p=True)[0]
    # temp = null.split(":")[-1]
    # temp = temp.replace("peacockA", "cc")
    # # temp = temp.replace("_L_", "_R_")
    # b_ctrl = temp.replace("_curve", "_1")
    

    return b_ctrl
    


# sel = cmds.ls(sl=True)
# for i in sel:
#     null = cmds.listRelatives(i, p=True)[0]
#     new_ctrl = get_new_ctrl_name(i)
#     copy_keys_exact_locations(null, new_ctrl, 0, 10)



def create_curve_joints():
    sel = cmds.ls(sl=True)
    for i in sel:
        joints = hjk3.create_joint_on_curve_path(i, 4)
        joints.reverse()
        new_joints = []
        for idx, j in enumerate(joints):
            cmds.matchTransform(j, i, rot=True)
            temp = i.split(":")[-1]
            jnts = temp.replace("peacockA", "rig")
            jnt = jnts.replace("_curve", "_%s" % str(idx+1))
            cmds.rename(j, jnt)
            new_joints.append(jnt)
        hjk3.parent_in_sequence(*new_joints)
        cmds.makeIdentity(new_joints[0], t=1, r=1, s=1, n=0, pn=1, a=True)

        ctrls = []
        for k in new_joints[1:3]:
            cc_name = k.replace("rig_", "cc_")
            cc = cmds.circle(nr=(0,0,1), n=cc_name)[0]
            cmds.matchTransform(cc, k, pos=True, rot=True)
            cmds.xform(cc, scale=(0.8, 0.8, 0.8), ws=True)
            cmds.makeIdentity(cc, t=0, r=0, s=1, n=0, pn=1, a=True)
            cmds.delete(cc, constructionHistory=True)
            ctrls.append(cc)
        
        hjk3.parent_in_sequence(*ctrls)
        child = hjk3.group_with_pivot(*ctrls, null=True)[0][0]
        child_slices = child.split("_")
        _1st_ctrl = child_slices[:-2] + ["1"]
        _1st_ctrl = "_".join(_1st_ctrl)
        cmds.parent(child, _1st_ctrl)
        cmds.parentConstraint(_1st_ctrl, new_joints[0])
        cmds.parentConstraint(ctrls[0], new_joints[1])
        cmds.parentConstraint(ctrls[1], new_joints[2])


        cc_name = ctrls[0]
        cc_name = cc_name.replace("cc_", "_")
        cc_name = "char_peacockA_mdl_v9999:peacockA" + cc_name
        obj_name = cc_name.split("_")
        obj_name[-1] = "grp"
        obj_name_grp = "_".join(obj_name)

        for obj in cmds.listRelatives(obj_name_grp, children=True):
            cmds.skinCluster(new_joints[0], obj, toSelectedBones=False, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=4, foc=True)
# create_curve_joints()


# sel = cmds.ls(sl=True)
# for i in sel:
#     slices = i.split("_")
#     end = slices[-1]
#     if end == "grp":
#         slices[-1] = "1_grp"
#     elif end == "null":
#         slices[-1] = "1_null"
#     else:
#         slices[-1] = slices[-1] + "_1"
#     new_name = "_".join(slices)
#     cmds.rename(i, new_name)


# sel = cmds.ls(sl=True)
# for i in sel:
#     temp = i.split(":")[-1]
#     temp = temp.replace("peacockA_", "cc_")
#     cc_name = temp.replace("_curve", "_1")
#     cc = cmds.duplicate('temp_ctrl', rr=True, n=cc_name)[0]
#     cmds.matchTransform(cc, i, pos=True, rot=True)
#     hjk3.group_with_pivot(cc, null=True)


# sel = cmds.ls(sl=True)
# R_list = []
# for i in sel:
#     ops = i.replace("_L_", "_R_")
#     R_list.append(ops)
# cmds.select(R_list)


bind_bones = ['root', 'spine_1', 'spine_2', 'neck_1', 'neck_2', 'neck_3', 'neck_4', 'neck_5', 'neck_6', 'neck_7', 'neck_8', 'head_1', 'jaw', 'wing_1_L_FK', 'wing_2_L_FK', 'wing_3_L_FK', 'wing_1_R_FK', 'wing_2_R_FK', 'wing_3_R_FK', 'tail_2', 'tail_3', 'tail_4', 'thigh_L', 'leg_L', 'knee_L', 'ankle_L', 'thumb_1_L', 'thumb_2_L', 'index_1_L', 'index_2_L', 'index_3_L', 'index_4_L', 'middle_1_L', 'middle_2_L', 'middle_3_L', 'middle_4_L', 'pinky_1_L', 'pinky_2_L', 'pinky_3_L', 'pinky_4_L', 'thigh_R', 'leg_R', 'knee_R', 'ankle_R', 'thumb_1_R', 'thumb_2_R', 'index_1_R', 'index_2_R', 'index_3_R', 'index_4_R', 'middle_1_R', 'middle_2_R', 'middle_3_R', 'middle_4_R', 'pinky_1_R', 'pinky_2_R', 'pinky_3_R', 'pinky_4_R']


sel = cmds.ls(sl=True)
for i in sel:
    # cmds.connectAttr("cc_wing_1_R_FK.Fold", f"{i}.input", f=True)
    cmds.connectAttr("cc_wing_3_R_FK.Show_Geo_1", f"{i}.visibility", f=True)


