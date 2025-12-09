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
                    cmds.setKeyframe(target, attribute=attr, time=t, value=val)



def get_new_ctrl_name(old_name):
    null = cmds.listRelatives(old_name, p=True)[0]
    temp = null.split(":")[-1]
    temp = temp.replace("peacockA", "cc")
    b_ctrl = temp.replace("_curve", "")
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
        for k in new_joints[1:3]:
            cc_name = k.replace("rig_", "cc_")
            cc = cmds.circle(nr=(0,0,1), n=cc_name)[0]
            cmds.matchTransform(cc, k, pos=True, rot=True)
            cmds.xform(cc, scale=(0.8, 0.8, 0.8), ws=True)
            cmds.makeIdentity(cc, t=0, r=0, s=1, n=0, pn=1, a=True)
            cmds.delete(cc, constructionHistory=True)
            hjk3.group_with_pivot(cc, null=True)

# create_curve_joints()



