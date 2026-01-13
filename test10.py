import maya.cmds as cmds


sel = cmds.ls(sl=True)
# print(sel)


for i in sel:
    grp = i.replace("_curve", "_grp")
    print(grp)
    temp = i.split(":")[-1]
    temp = temp.replace("peacockA_", "rig_")
    jnt = temp.replace("_curve", "")

    joints = []
    num = 1
    while cmds.objExists(jnt + "_" + str(num)):
        joints.append(jnt + "_" + str(num))
        num += 1

    objs = cmds.listRelatives(grp, children=True)
    for obj in objs:
        if "_rachii" in obj and "_yetiDummy" in obj:
            cmds.skinCluster(joints[0], obj, toSelectedBones=False, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=3, foc=True)
        elif "_feather" in obj and "_yetiDummy" in obj:
            cmds.skinCluster(joints[-1], obj, toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=1, foc=True)
        else:
            continue
    
    

