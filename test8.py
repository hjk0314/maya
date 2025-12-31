import maya.cmds as cmds
import hjk3


def show_and_hide_sub_ctrl():
    sel = cmds.ls(sl=True)

    for i in sel:
        shapes = cmds.ls(i, dag=True, type="nurbsCurve")

        shapes = [shp for shp in shapes]
        last_ctrl = cmds.listRelatives(shapes[-1], parent=True)[0]
        attr_name = "Sub_Ctrl"
        hjk3.create_attributes(last_ctrl, attr_name, bt={"at": "bool"})
        for shp in shapes[:-1]:
            cmds.connectAttr(f"{last_ctrl}.{attr_name}", f"{shp}.visibility", f=True)



def create_show_and_hide_channel_and_connect():
    cc_main = "cc_main"
    cc_type = "M"
    attr_name = "Show_Signature_Eye_%s" % cc_type
    hjk3.create_attributes(tc=cc_main, an=attr_name, bt={"at": "bool"})

    sel = cmds.ls(sl=True)
    for i in sel:
        cmds.connectAttr(f"{cc_main}.{attr_name}", f"{i}.visibility", f=True)



# sel = cmds.ls(sl=True)
# for i in sel:
#     shapes = cmds.ls(i, dag=True, type="nurbsCurve")
#     shapes = [shp for shp in shapes]
#     result = []
#     for shp in shapes:
#         obj = cmds.listRelatives(shp, p=True)[0]
#         result.append(obj)
#     result.reverse()
#     cmds.select(cl=True)
#     cmds.select(result)
    



sel = cmds.ls(sl=True)
# print(sel)
# sel = ['char_peacockA_mdl_v9999:peacockA_crown_01_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_01_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_02_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_02_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_03_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_03_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_04_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_04_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_05_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_05_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_06_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_06_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_07_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_07_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_08_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_08_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_09_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_09_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_10_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_10_feather_geo', 'char_peacockA_mdl_v9999:peacockA_crown_11_rachii_geo', 'char_peacockA_mdl_v9999:peacockA_crown_11_feather_geo']

# rachiis = sel[::2]
# feathers = sel[1::2]
# for r, f in zip(rachiis, feathers):
#     rac = f"{r}.vtx[9]"
#     fea = f"{f}.vtx[10]"
#     pos = hjk3.get_position(rac, fea)
#     cuv = hjk3.create_curve_from_points(*pos)
#     joints = hjk3.create_joint_on_curve_path(c=cuv, n=5)
#     hjk3.parent_in_sequence(*joints)


# ctrls = hjk3.create_FK_ctrls(cs=0.5, ds=0.125)
# hjk3.group_with_pivot(*ctrls, null=True)


# hjk3.replace_name(s="crown_", r="rig_crown_")


# for cc in sel:
#     jnt = cc.replace("cc_", "rig_")
#     cmds.parentConstraint(cc, jnt, mo=True, w=1.0)


# cpu = hjk3.ColorPickerUI()
# cpu.show()