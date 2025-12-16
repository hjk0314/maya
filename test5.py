import hjk3
import maya.cmds as cmds




a = ['locator40', 'locator41', 'locator42', 'locator43', 'locator44', 'locator45', 'locator46', 'locator47', 'locator48', 'locator49', 'locator50']


b = ['locator29', 'locator30', 'locator31', 'locator32', 'locator33', 'locator34', 'locator35', 'locator36', 'locator37', 'locator38', 'locator39']



for idx, (i, j) in enumerate(zip(a, b)):
    crown_curve = hjk3.create_curve_aim(i, j)
    joints = hjk3.create_joint_on_curve_path(crown_curve, 5)
    new_joints = []
    for ki, k in enumerate(joints):
        new_name = cmds.rename(k, "rig_crown_%d_%d" % (idx+1, ki+1))
        new_joints.append(new_name)
    hjk3.parent_in_sequence(*new_joints)
    cmds.delete(crown_curve)

    cc_list = []
    for jnt in new_joints:
        cc_name = jnt.replace("rig_", "cc_")
        cc = cmds.circle(nr=(1,0,0), n=cc_name, constructionHistory=False)[0]
        cmds.scale(0.5, 0.5, 0.5, cc)
        cmds.makeIdentity(cc, t=0, r=0, s=1, n=0, pn=1, a=True)
        cmds.matchTransform(cc, jnt, pos=True, rot=True)
        cc_list.append(cc)
    hjk3.parent_in_sequence(*cc_list)
    hjk3.group_with_pivot(*cc_list, null=True)
    