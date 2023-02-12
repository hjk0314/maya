from hjk import *


jntDict = {
    'jnt_root': ['cc_root_grp'], 
    'jnt_spine_1': ['cc_spine_1_grp'], 
    'jnt_spine_2': ['cc_spine_2_grp'], 
    'jnt_spine_3': ['cc_spine_3_grp'], 
    'jnt_spine_4': ['cc_spine_4_grp'], 
    'jnt_neck_1': ['cc_neck_1_grp'], 
    'jnt_neck_2': ['cc_neck_2_grp'], 
    'jnt_head_1': ['cc_head_grp'], 
    'jnt_head_end': [], 
    'jnt_scapula_L': ['cc_scapula_L_grp'], 
    'jnt_shoulder_L': ['cc_shoulderIK_L_grp', 'cc_shoulderFK_L_grp'], 
    'jnt_elbow_L': ['cc_elbowIK_L_grp', 'cc_elbowFK_L_grp'], 
    'jnt_wrist_L': ['cc_wristIK_L_grp', 'cc_wristFK_L_grp'], 
    'jnt_parm_L': ['cc_parm_L_grp'], 
    'jnt_thumb_L_1': ['cc_thumb_L_1_grp'], 
    'jnt_thumb_L_2': ['cc_thumb_L_2_grp'], 
    'jnt_thumb_L_3': ['cc_thumb_L_3_grp'], 
    'jnt_thumb_L_4': ['cc_thumb_L_4_grp'], 
    'jnt_index_L_1': ['cc_index_L_1_grp'], 
    'jnt_index_L_2': ['cc_index_L_2_grp'], 
    'jnt_index_L_3': ['cc_index_L_3_grp'], 
    'jnt_index_L_4': ['cc_index_L_4_grp'], 
    'jnt_middle_L_1': ['cc_middle_L_1_grp'], 
    'jnt_middle_L_2': ['cc_middle_L_2_grp'], 
    'jnt_middle_L_3': ['cc_middle_L_3_grp'], 
    'jnt_middle_L_4': ['cc_middle_L_4_grp'], 
    'jnt_ring_L_1': ['cc_ring_L_1_grp'], 
    'jnt_ring_L_2': ['cc_ring_L_2_grp'], 
    'jnt_ring_L_3': ['cc_ring_L_3_grp'], 
    'jnt_ring_L_4': ['cc_ring_L_4_grp'], 
    'jnt_pinky_L_1': ['cc_pinky_L_1_grp'], 
    'jnt_pinky_L_2': ['cc_pinky_L_2_grp'], 
    'jnt_pinky_L_3': ['cc_pinky_L_3_grp'], 
    'jnt_pinky_L_4': ['cc_pinky_L_4_grp'], 
    'jnt_scapula_R': ['cc_scapula_R_grp'], 
    'jnt_shoulder_R': ['cc_shoulderIK_R_grp', 'cc_shoulderFK_R_grp'], 
    'jnt_elbow_R': ['cc_elbowIK_R_grp', 'cc_elbowFK_R_grp'], 
    'jnt_wrist_R': ['cc_wristIK_R_grp', 'cc_wristFK_R_grp'], 
    'jnt_parm_R': ['cc_parm_R_grp'], 
    'jnt_thumb_R_1': ['cc_thumb_R_1_grp'], 
    'jnt_thumb_R_2': ['cc_thumb_R_2_grp'], 
    'jnt_thumb_R_3': ['cc_thumb_R_3_grp'], 
    'jnt_thumb_R_4': ['cc_thumb_R_4_grp'], 
    'jnt_index_R_1': ['cc_index_R_1_grp'], 
    'jnt_index_R_2': ['cc_index_R_2_grp'], 
    'jnt_index_R_3': ['cc_index_R_3_grp'], 
    'jnt_index_R_4': ['cc_index_R_4_grp'], 
    'jnt_middle_R_1': ['cc_middle_R_1_grp'], 
    'jnt_middle_R_2': ['cc_middle_R_2_grp'], 
    'jnt_middle_R_3': ['cc_middle_R_3_grp'], 
    'jnt_middle_R_4': ['cc_middle_R_4_grp'], 
    'jnt_ring_R_1': ['cc_ring_R_1_grp'], 
    'jnt_ring_R_2': ['cc_ring_R_2_grp'], 
    'jnt_ring_R_3': ['cc_ring_R_3_grp'], 
    'jnt_ring_R_4': ['cc_ring_R_4_grp'], 
    'jnt_pinky_R_1': ['cc_pinky_R_1_grp'], 
    'jnt_pinky_R_2': ['cc_pinky_R_2_grp'], 
    'jnt_pinky_R_3': ['cc_pinky_R_3_grp'], 
    'jnt_pinky_R_4': ['cc_pinky_R_4_grp'], 
    'jnt_hip_L': ['cc_hipIK_L_grp', 'cc_hipFK_L_grp'], 
    'jnt_knee_L': ['cc_kneeIK_L_grp', 'cc_kneeFK_L_grp'], 
    'jnt_ankle_L': ['cc_ankleIK_L_grp', 'cc_ankleFK_L_grp'], 
    'jnt_ball_L': ['cc_ballIK_L_grp', 'cc_ballFK_L_grp'], 
    'jnt_toe_L': ['cc_toeIK_L_grp', 'cc_toeFK_L_grp'], 
    'jnt_hip_R': ['cc_hipIK_R_grp', 'cc_hipFK_R_grp'], 
    'jnt_knee_R': ['cc_kneeIK_R_grp', 'cc_kneeFK_R_grp'], 
    'jnt_ankle_R': ['cc_ankleIK_R_grp', 'cc_ankleIK_R_grp'], 
    'jnt_ball_R': ['cc_ballIK_R_grp', 'cc_ballFK_R_grp'], 
    'jnt_toe_R': ['cc_toeIK_R_grp', 'cc_toeFK_R_grp'], 
}


# Create an empty group and match the pivot with the selector.
def grouping(obj: str):
    grp = pm.group(em=True, n = obj + "_grp")
    pm.matchTransform(grp, obj, pos=True, rot=True)
    try:
        # Selector's mom group.
        objParent = "".join(pm.listRelatives(obj, p=True))
        pm.parent(grp, objParent)
    except:
        pass
    pm.parent(obj, grp)
    return grp


def createCC(jnt: str):
    ccName = jnt.replace("jnt_", "cc_")
    cc = pm.circle(nr=(1,0,0), ch=False, n=ccName)
    cc = cc[0]
    grp = grouping(cc)
    pm.matchTransform(grp, jnt, pos=True, rot=True)


def createFingerCC():
    FINGER = ["thumb", "index", "middle", "ring", "pinky"]
    LR = ["L", "R"]
    for j in FINGER:
        for k in LR:
            for num in range(1, 4):
                jntName = f'jnt_{j}_{k}_{num}'
                createCC(jntName)


def createSelCC():
    sel = pm.ls(sl=True)
    for i in sel:
        createCC(i)


# Select groups only.
def isGrp(obj: str) -> list:
    '''If there is no shape and the object type is not 
    'joint', 'ikEffector', 'ikHandle', 'Constraint', ...
    then it is most likely a group.'''
    sel = pm.ls(obj, dag=True, type=['transform'])
    grp = []
    for i in sel:
        typ = pm.objectType(i)
        A = pm.listRelatives(i, s=True)
        B = typ in ['joint', 'ikEffector', 'ikHandle',]
        C = 'Constraint' in typ
        if not (A or B or C):
            grp.append(i)
        else:
            continue
    return grp


def parentSel():
    sel = pm.ls(sl=True)
    for j, k in enumerate(sel):
        if (j + 1) < len(sel):
            if isGrp(k):
                par = k.getChildren()
            else:
                par = k
            pm.parent(sel[j+1], par)
        else:
            continue


def addNameFKIK(FKIK: str):
    sel = pm.ls(sl=True)
    for i in sel:
        wordList = i.split("_")
        word = wordList[1]
        new = f"{word}{FKIK}"
        wordList[1] = new
        pm.rename(i, '_'.join(wordList))


def createChannels():
    sel = pm.ls(sl=True)
    # channelList = [
    #     "Toe", 
    #     "Bank", 
    #     "Twist", 
    #     "Heel", 
    #     "Ball", 
    #     "Down", 
    #     ]
    channelList = [
        "FKIK_Arm_L", 
        "FKIK_Arm_R", 
        "FKIK_Leg_L", 
        "FKIK_Leg_R", 
        ]
    for i in sel:
        for cName in channelList:
            pm.addAttr(i, ln=cName, at='double', dv=0, min=0, max=1)
            pm.setAttr(f'{i}.{cName}', e=True, k=True)


def batchCC():
    sel = pm.ls(sl=True)
    for i in sel:
        tmp = i.split("_")
        tmp.pop(-1)
        tmp = "_".join(tmp)
        jnt = tmp.replace("cc_", "jnt_")
        pm.matchTransform(i, jnt, pos=True, rot=True)


def parentCCtoJnt():
    sel = pm.ls(sl=True)
    for i in sel:
        jnt = i.replace("cc_", "jnt_")
        pm.parentConstraint(i, jnt, mo=True, w=1.0)


def allCCBatch():
    for jnt, ccList in jntDict.items():
        if not ccList:
            continue
        else:
            for cc in ccList:
                if not pm.ls(cc):
                    continue
                else:
                    if 'FK' in cc:
                        pm.matchTransform(cc, jnt, pos=True, rot=True)
                    else:
                        pm.matchTransform(cc, jnt, pos=True)


def legIKSetting():
    sel = pm.ls(sl=True)
    num = len(sel) - 1
    ikHList = []
    grpList = []
    for i in range(num):
        solver = 'ikRPsolver' if i == 0 else 'ikSCsolver'
        startJnt = sel[i]
        endJnt = sel[i+1]
        name = startJnt.replace('jnt_', 'ikH_')
        ikH = pm.ikHandle(sj=startJnt, ee=endJnt, sol=solver, n=name)
        tmp = grpEmpty()
        ikHList.append(ikH[0])
        grpList.append(tmp)
    pm.parent(ikHList[1], grpList[0])
    pm.parent(ikHList[2], grpList[1])
    pm.delete(grpList[2])
    new = f"{ikHList[2]}_grp"
    pm.rename(grpList[1], new)
    pm.select(new)
    tmp = grpEmpty()
    pm.rename(new, new.replace('_grp', '_null'))
    pm.rename(tmp, new)


def armIKSetting():
    sel = pm.ls(sl=True)
    num = len(sel) - 1
    for i in range(num):
        solver = 'ikRPsolver' if i == 0 else 'ikSCsolver'
        startJnt = sel[i]
        endJnt = sel[i+1]
        name = startJnt.replace('jnt_', 'ikH_')
        pm.ikHandle(sj=startJnt, ee=endJnt, sol=solver, n=name)
        grpEmpty()


def footConnect():
    sel = pm.ls(sl=True)
    if not sel:
        print("Nothing selected.")
    else:
        for i in sel:
            LR = i.split("_")[-1]
            clampNode = pm.shadingNode("clamp", au=True)
            pm.setAttr(f"{clampNode}.minR", -180)
            pm.setAttr(f"{clampNode}.maxG", 180)
            connDict = {
                f"loc_heel_{LR}.rotateX": f"cc_foot_{LR}.Heel", 
                f"loc_toe_{LR}.rotateX": f"cc_foot_{LR}.Toe", 
                f"loc_toe_{LR}.rotateY": f"cc_foot_{LR}.Twist", 
                f"loc_ball_{LR}.rotateZ": f"cc_foot_{LR}.Ball", 
                f"ikH_ball_{LR}_null.rotateZ": f"cc_foot_{LR}.Down", 
                f"{clampNode}.inputR": f"cc_foot_{LR}.Bank", 
                f"{clampNode}.inputG": f"cc_foot_{LR}.Bank", 
                f"loc_bankOut_{LR}.rotateZ": f"{clampNode}.outputR", 
                f"loc_bankIn_{LR}.rotateZ": f"{clampNode}.outputG", 
                }
            for key, value in connDict.items():
                pm.connectAttr(value, key, f=True)


def createIKSplineHandle():
    ikH = pm.ikHandle(sol="ikSplineSolver", 
            n="ikH_spine_1", # name
            sj="jnt_spine_1", # startJoint
            ee="jnt_spine_4", # endEffector
            c="cuv_spine_1", # curve
            ccv=False, # createCurve
            scv=False, # simplifyCurve
            cra=True, # createRootAxis
            ns=3,  # numSpans
            pcv=False
        )


def parentCluster():
    sel = pm.ls(sl=True)
    ccList = ["cc_spine_1", "cc_spine_2"]
    ccGrpList = ["cc_spine_1_grp", "cc_spine_2_grp"]
    cltGrpList = []
    for j, k in enumerate(sel):
        rename(k.name(), f"clt_spine_{j}")
        pm.select(k)
        tmp = grpEmpty()
        cltGrpList.append(tmp)
    for i in range(2):
        pm.matchTransform(ccGrpList[i], cltGrpList[i], pos=True)
        pm.select(cl=True)
        pm.parent(cltGrpList[i], ccList[i])
    pm.connectAttr("cc_spine_1.rotateY", "ikH_spine_1.twist", f=True)
    pm.connectAttr("cc_spine_2.rotateY", "ikH_spine_1.roll", f=True)


leg_L_1 = ["cc_hipIK_L", "cc_sub"]
leg_L_2 = ["cc_foot_L_grp", "cc_legPole_L_grp"]
leg_R_1 = ["cc_hipIK_R", "cc_sub"]
leg_R_2 = ["cc_foot_R_grp", "cc_legPole_R_grp"]
arm_L_1 = ["cc_shoulderIK_L", "cc_sub"]
arm_L_2 = ["cc_handIK_L_grp", "cc_armPole_L_grp"]
arm_R_1 = ["cc_shoulderIK_R", "cc_sub"]
arm_R_2 = ["cc_handIK_R_grp", "cc_armPole_R_grp"]


def connectFollow(Parent: list, Child: list):
    ctrl = Child[0].replace('_grp', '')
    conList = []
    rev = pm.shadingNode('reverse', au=True)
    for j in Parent:
        for k in Child:
            par = pm.parentConstraint(j, k, mo=True, w=1.0)
            sca = pm.scaleConstraint(j, k, w=1.0)
            conList.append(par)
            conList.append(sca)
    pm.connectAttr(f"{ctrl}.Follow", f"{rev}.inputX")
    pm.connectAttr(f"{ctrl}.Follow", f"{conList[0]}.{Parent[0]}W0")
    pm.connectAttr(f"{rev}.outputX", f"{conList[0]}.{Parent[1]}W1")
    pm.connectAttr(f"{ctrl}.Follow", f"{conList[2]}.{Parent[0]}W0")
    pm.connectAttr(f"{rev}.outputX", f"{conList[2]}.{Parent[1]}W1")
    pm.connectAttr(f"{ctrl}.Follow", f"{conList[1]}.{Parent[0]}W0")
    pm.connectAttr(f"{rev}.outputX", f"{conList[1]}.{Parent[1]}W1")
    pm.connectAttr(f"{ctrl}.Follow", f"{conList[3]}.{Parent[0]}W0")
    pm.connectAttr(f"{rev}.outputX", f"{conList[3]}.{Parent[1]}W1")


def createPV():
    leg_L = ['jnt_hip_L', 'jnt_knee_L', 'jnt_ankle_L']
    leg_R = ['jnt_hip_R', 'jnt_knee_R', 'jnt_ankle_R']
    arm_L = ['jnt_shoulder_L', 'jnt_elbow_L', 'jnt_wrist_L']
    arm_R = ['jnt_shoulder_R', 'jnt_elbow_R', 'jnt_wrist_R']
    pv = [
        'cc_legPole_L_grp', 
        'cc_legPole_R_grp', 
        'cc_armPole_L_grp', 
        'cc_armPole_R_grp'
    ]
    pm.select(cl=True)
    pm.select(leg_L)
    loc = poleVector()
    pm.matchTransform('cc_legPole_L_grp', loc, pos=True)
    pm.select(cl=True)
    pm.select(leg_R)
    loc = poleVector()
    pm.matchTransform('cc_legPole_R_grp', loc, pos=True)
    pm.select(cl=True)
    pm.select(arm_L)
    loc = poleVector()
    pm.matchTransform('cc_armPole_L_grp', loc, pos=True)
    pm.select(cl=True)
    pm.select(arm_R)
    loc = poleVector()
    pm.matchTransform('cc_armPole_R_grp', loc, pos=True)



# createIKSplineHandle()
# parentCluster()

# parentCCtoJnt()
# createFingerCC()
# createSelCC()
# parentSel()
# addNameFKIK("IK")
# addNameFKIK("FK")
# createChannels()

# ctrl(cub=True)
# orientJnt()
# MirrorCopy('x')
# rename('clt_spine_1')
# grpEmpty()
# rename('jnt_', 'fbx_')
# rename('IK', 'FK')

# batchCC()
# poleVector()

# color(yellow=True)
# color(pink=True)
# color(red=True)
# color(red2=True)
# color(blue=True)
# color(blue2=True)
# color(green2=True)

# armIKSetting()
# footConnect()


# connectFollow(leg_L_1, leg_L_2)
# connectFollow(leg_R_1, leg_R_2)
# connectFollow(arm_L_1, arm_L_2)
# connectFollow(arm_R_1, arm_R_2)