import maya.cmds as cmds
import hjk3






sel = cmds.ls(sl=True)


for i in sel:
    sign_parameter, sign_transform = cmds.nonLinear(i, type="sine", n="abc")
    cmds.rotate(-90, 0, 0, sign_transform, r=True, os=True, fo=True)
    cmds.matchTransform(sign_transform, i, pos=True)
    cmds.setAttr("abc.highBound", 2)
    cmds.setAttr("abc.lowBound", 0)
    cmds.setAttr("abc.dropoff", -1)


