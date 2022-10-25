import pymel.core as pm


sel = pm.ls(sl=True, dag=True)
channel = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]
jnt = [i for i in sel if pm.objectType(i, i='joint')]
for i in jnt:
    pm.delete(i, cn=True)
    for j in channel:
        pm.disconnectAttr(i + j)