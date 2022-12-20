import re
import pymel.core as pm
from hjk import *


def cc_addAttr():
    sel = pm.ls(sl=True, l=True)
    for controller in sel:
        # pm.addAttr(controller, ln='Ball', at='double', dv=0)
        # pm.setAttr(f'{controller}.Ball', e=True, k=True)
        # pm.addAttr(controller, ln='RotY', at='double', dv=0)
        # pm.setAttr(f'{controller}.RotY', e=True, k=True)
        # pm.addAttr(controller, ln='RotZ', at='double', dv=0)
        # pm.setAttr(f'{controller}.RotZ', e=True, k=True)
        pm.addAttr(controller, ln='Foot_Follow', at='double', min=0, max= 1, dv=0)
        pm.setAttr(f'{controller}.Foot_Follow', e=True, k=True)


# cc_addAttr()


def renameIKH():
    sel = pm.ls(sl=True)
    typ = ['spring', 'rp', 'sc1', 'sc2']
    end = '_R_mid'
    renameList = [pm.rename(k, f"ikH_{typ[j]}{end}") for j, k in enumerate(sel)]
    pm.parent(renameList[1], renameList[0])
    pm.select(renameList[0], renameList[2], renameList[3])
    grpEmpty()
    

# renameIKH()
    

def poleFollow():
    sel = pm.ls(sl=True)
    sub = 'cc_sub'
    foot = 'cc_foot'
    pole = 'cc_poleVector'
    for i in sel:
        tmp = re.search('cc_poleVector(.*)', i.name())
        end = tmp.group(1)
        pm.parentConstraint(sub, f"{pole}{end}_null", mo=True, w=0)
        pm.parentConstraint(f"{foot}{end}", f"{pole}{end}_null", mo=True, w=1)


# poleFollow()


def legFollow():
    sel = pm.ls(sl=True)
    sub = 'cc_sub'
    foot = 'cc_foot'
    leg = 'cc_leg'
    for i in sel:
        tmp = re.search('cc_foot(.*)', i.name())
        end = tmp.group(1)
        pm.scaleConstraint(sub, f"{foot}{end}_null", mo=True, w=0)
        pm.scaleConstraint(f"{leg}{end}", f"{foot}{end}_null", mo=True, w=1)


# legFollow()


def createAntennaCC():
    for i in range(1, 17):
        par = 'cc_antenna_R_%d' % i
        chi = 'jnt_antenna_R_%d' % i
        pm.parentConstraint(par, chi, mo=True, w=1)


# sel = pm.ls(sl=True)
# for i in sel:
#     pm.addAttr(i, ln='Leg_Follow', at='double', min=0, max=1, dv=0)
#     pm.setAttr(f'{i}.Leg_Follow', e=True, k=True)



# sel = pm.ls(sl=True)
# for i in sel:
#     fbx = i.name()
#     rig = i.name()
#     rig = rig.replace('joint', 'jnt')
#     print(fbx, rig)
#     pm.select(cl=True)
#     pm.select([rig, fbx])
#     writeJSON()


# createLoc(jnt=True)
# rename('leg_', 'legSpring_')
# rename('_mid', '_Bk')
# rename('jnt_leg_L_Bk_1')
# ctrl(sph=True)
# color(red=True)


def connA():
    sel = pm.ls(sl=True)
    org = "jnt_Ft_wheel_mid_L_3"
    for i in sel:
        pm.connectAttr(f"{org}.rotateX", f"{i}.rotateX", f=True)


def selSomething(typ):
    sel = pm.ls(sl=True, dag=True)
    lst = [i for i in sel if pm.objectType(i) == typ]
    return lst


# pm.delete(selSomething('scaleConstraint'))


def temp():
    jointList = selSomething('joint')
    # pm.select(jointList)
    # jointList = pm.ls(sl=True)
    for i in jointList:
        # pm.scaleConstraint('cc_head_grp', i, mo=True, w=1)
        pm.connectAttr('cc_antenna_grp.scale', f'{i}.scale', f=True)


# sel = pm.ls(sl=True)
# for fbx in sel:
#     rig = fbx.replace('joint_', 'jnt_')
#     pm.parentConstraint(rig, fbx, mo=True, w=1)


color(pink=True)
