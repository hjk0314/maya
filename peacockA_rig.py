import maya.cmds as cmds
import hjk3


hjk3.create_group_for_rig("peacockA")


pos = hjk3.get_bounding_box_position()
loc = cmds.spaceLocator()[0]
cmds.xform(loc, translation=pos, ws=True)


hjk3.align_object_to_plane()


hjk3.orient_joint(p="yxz", s="zdown")


hjk3.re_name(n="guide_locator_1")
