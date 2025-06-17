import hjk
import pymel.core as pm
import math


def aim_Y_axis(obj1, obj2):
    obj1 = pm.PyNode(obj1)
    obj2 = pm.PyNode(obj2)
    # obj1_pos = pm.xform(obj1, q=True, ws=True, t=True)
    obj1_pos = hjk.getPosition(obj1)
    # obj2_pos = pm.xform(obj2, q=True, ws=True, t=True)
    obj2_pos = hjk.getPosition(obj2)
    dx = obj2_pos[0] - obj1_pos[0]
    dz = obj2_pos[2] - obj1_pos[2]
    angle_rad = math.atan2(dx, dz)
    angle_deg = math.degrees(angle_rad)
    obj1.setRotation([0, angle_deg, 0], space="object")


sel = pm.selected()
for obj in sel:
    startPoint = f"{obj}.vtx[0]"
    endPoint = f"{obj}.vtx[2]"
    # pm.select(cl=True)
    # pm.select(startPoint, endPoint)
    # aimCuv = hjk.createCurveAimingPoint()
    aimCuv = pm.curve(d=3, p=[(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)])
    pm.matchTransform(aimCuv, obj, pos=True)
    aim_Y_axis(aimCuv, endPoint)
    # objPivot = pm.xform(obj, q=True, ws=True, rp=True)
    # pm.xform(aimCuv, ws=True, piv=objPivot)
    obj_grp = f"{obj}_grp"
    obj_grp = pm.PyNode(obj_grp)
    obj_grp_upstreamNode = obj_grp.getParent()
    pm.parent(obj_grp, aimCuv)
    pm.makeIdentity(obj_grp, t=0, r=1, s=0, n=0, pn=1, a=True)
    pm.parent(obj_grp, obj_grp_upstreamNode)





