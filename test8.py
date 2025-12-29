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



sel = cmds.ls(sl=True)
for i in sel:
    shapes = cmds.ls(i, dag=True, type="nurbsCurve")
    shapes = [shp for shp in shapes]
    result = []
    for shp in shapes:
        obj = cmds.listRelatives(shp, p=True)[0]
        result.append(obj)
    result.reverse()
    cmds.select(cl=True)
    cmds.select(result)
    
