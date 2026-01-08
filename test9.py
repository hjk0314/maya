import maya.cmds as cmds
import hjk3 as hjk

def create_tongue_joints_IKFK(curve=None, num_joints=4, ctrl_size=1.0):
    """
    혀의 조인트를 생성하고 FK 컨트롤러를 만드는 함수
    
    Args:
        curve: 커브 이름 (선택사항, None이면 커브를 찾거나 직접 생성)
        num_joints: 생성할 조인트 개수 (기본값: 4)
        ctrl_size: 컨트롤러 크기 (기본값: 1.0)
    """
    # 선택된 오브젝트 확인
    sel = cmds.ls(sl=True)
    
    # 커브가 선택되어 있으면 사용
    if sel:
        curve = sel[0]
        # 선택된 오브젝트가 커브인지 확인
        shapes = cmds.listRelatives(curve, shapes=True, type="nurbsCurve")
        if shapes:
            # 조인트를 커브에 따라 생성
            joints = hjk.create_joint_on_curve_path(curve, num_joints)
        else:
            # 커브가 아니면 선택된 위치에 직접 조인트 생성
            joints = create_tongue_joints_from_selection(sel, num_joints)
    else:
        # 선택된 오브젝트가 없으면 기본 위치에 조인트 생성
        joints = create_tongue_joints_default(num_joints)
    
    # 조인트 이름 변경 (rig_tongue_1 형식)
    new_joints = []
    for idx, jnt in enumerate(joints):
        jnt_name = f"rig_tongue_{idx+1}"
        renamed_jnt = cmds.rename(jnt, jnt_name)
        new_joints.append(renamed_jnt)
    
    # 조인트 체인 연결
    hjk.parent_in_sequence(*new_joints)
    cmds.makeIdentity(new_joints[0], t=1, r=1, s=1, n=0, pn=1, a=True)
    
    # FK/IK 조인트 생성
    fk_joints, ik_joints = hjk.create_joint_IKFK(*new_joints)
    
    # FK 컨트롤러 생성 (suffix 없이)
    fk_ctrls_temp = hjk.create_FK_ctrls(
        *fk_joints,
        joint_axis=(1, 0, 0),  # X축을 향하는 원형 컨트롤러
        ctrl_size=ctrl_size,
        down_step=0.1,  # 각 컨트롤러가 조금씩 작아지도록
        end_ctrl=False,  # 마지막 조인트에는 컨트롤러 생성하지 않음
        prefix="cc",
        suffix=""  # suffix 제거
    )
    
    # 컨트롤러 이름 변경 (cc_tongue_1 형식)
    fk_ctrls = []
    for idx, ctrl in enumerate(fk_ctrls_temp):
        ctrl_name = f"cc_tongue_{idx+1}"
        renamed_ctrl = cmds.rename(ctrl, ctrl_name)
        fk_ctrls.append(renamed_ctrl)
    
    # 각 FK 컨트롤러를 group_with_pivot(null=True)로 그룹화
    for ctrl in fk_ctrls:
        hjk.group_with_pivot(ctrl, null=True)
    
    # FK 컨트롤러와 FK 조인트 연결
    for ctrl, jnt in zip(fk_ctrls, fk_joints[:-1]):  # 마지막 조인트 제외
        cmds.parentConstraint(ctrl, jnt, mo=True, w=1.0)
    
    # IK Spline 설정 (edit_point=True로 원형에 가깝게 생성)
    ik_curve_info = hjk.create_curve_ikSpline(*ik_joints, edit_point=True)
    ik_curve = list(ik_curve_info.keys())[0]
    ik_curve = cmds.rename(ik_curve, "splcuv_tongue")
    ik_locators = ik_curve_info[list(ik_curve_info.keys())[0]]
    
    # IK 컨트롤러 생성 (첫 번째, 중간, 마지막 조인트에)
    ik_ctrls = []
    # 첫 번째 컨트롤러
    start_ctrl = cmds.circle(nr=(1, 0, 0), ch=False, n="cc_tongue_start")[0]
    cmds.scale(0.6, 0.6, 0.6, start_ctrl, r=True)
    cmds.matchTransform(start_ctrl, ik_joints[0], pos=True, rot=True)
    cmds.makeIdentity(start_ctrl, t=0, r=0, s=1, n=0, pn=1, a=True)
    hjk.group_with_pivot(start_ctrl, null=True)
    ik_ctrls.append(start_ctrl)
    
    # 마지막 컨트롤러
    end_ctrl = cmds.circle(nr=(1, 0, 0), ch=False, n="cc_tongue_end")[0]
    cmds.scale(0.5, 0.5, 0.5, end_ctrl, r=True)
    cmds.matchTransform(end_ctrl, ik_joints[-1], pos=True, rot=True)
    cmds.makeIdentity(end_ctrl, t=0, r=0, s=1, n=0, pn=1, a=True)
    hjk.group_with_pivot(end_ctrl, null=True)
    ik_ctrls.append(end_ctrl)
    
    # 중간 컨트롤러 생성 (커브의 중간 위치에 배치)
    mid_ctrl = cmds.circle(nr=(1, 0, 0), ch=False, n="cc_tongue_mid")[0]
    cmds.scale(0.55, 0.55, 0.55, mid_ctrl, r=True)
    mid_ctrl_list = hjk.group_with_pivot(mid_ctrl, null=True)[0]
    mid_ctrl_grp = mid_ctrl_list[0]
    ik_ctrls.append(mid_ctrl)
    
    # 중간 컨트롤러를 IK 커브의 중간 위치에 배치 (중간 로케이터 위치 사용)
    mid_loc_idx = len(ik_locators) // 2
    mid_locator = ik_locators[mid_loc_idx]
    cmds.matchTransform(mid_ctrl_grp, mid_locator, pos=True, rot=True)
    cmds.makeIdentity(mid_ctrl, t=0, r=0, s=1, n=0, pn=1, a=True)
    
    # 첫 번째 컨트롤러에 IK/FK 스위치 및 Stretch 속성 추가
    hjk.create_attributes(start_ctrl, "IK0_FK1", ft={"at": "double", "dv": 0, "min": 0, "max": 10})
    hjk.create_attributes(start_ctrl, "Stretch", bt={"at": "bool"})
    
    # IK Spline 핸들 생성
    ik_handle_nodes = hjk.create_ikSplineHandle(
        ik_curve, 
        ik_joints, 
        scaleX=True, 
        scaleY=True, 
        scaleZ=True
    )
    # ik_handle_nodes: [curve_info, condition_node, multiplyDivide_node, ikHandle_name]
    curve_info, condition_node, multiplyDivide_node, ikHandle_name = ik_handle_nodes
    
    # Stretch attribute는 채널창에만 생성 (조건 노드 연결은 사용자가 직접 처리)
    
    # IK 로케이터와 컨트롤러 연결 (거리에 따라 weight 값 적용)
    if len(ik_locators) >= 2:
        # 중간 지점 찾기 (로케이터 개수의 절반)
        mid_loc_idx = len(ik_locators) // 2
        
        for idx, loc in enumerate(ik_locators):
            if idx < mid_loc_idx:
                # 첫 번째 컨트롤러와 중간 컨트롤러 사이의 로케이터들
                if idx == 0:
                    # 첫 번째 로케이터는 start_ctrl만
                    cmds.parentConstraint(start_ctrl, loc, mo=True, w=1.0)
                else:
                    # 거리에 따라 weight 계산
                    weights = hjk.get_constraint_weight_by_distance(start_ctrl, mid_ctrl, loc)
                    if weights:
                        weight_start, weight_mid = weights
                        cmds.parentConstraint(start_ctrl, loc, mo=True, w=weight_start)
                        cmds.parentConstraint(mid_ctrl, loc, mo=True, w=weight_mid)
            elif idx > mid_loc_idx:
                # 중간 컨트롤러와 마지막 컨트롤러 사이의 로케이터들
                if idx == len(ik_locators) - 1:
                    # 마지막 로케이터는 end_ctrl만
                    cmds.parentConstraint(end_ctrl, loc, mo=True, w=1.0)
                else:
                    # 거리에 따라 weight 계산
                    weights = hjk.get_constraint_weight_by_distance(mid_ctrl, end_ctrl, loc)
                    if weights:
                        weight_mid, weight_end = weights
                        cmds.parentConstraint(mid_ctrl, loc, mo=True, w=weight_mid)
                        cmds.parentConstraint(end_ctrl, loc, mo=True, w=weight_end)
            else:
                # 중간 로케이터는 mid_ctrl만
                cmds.parentConstraint(mid_ctrl, loc, mo=True, w=1.0)
    
    # IK/FK 블렌드 연결
    switch_attr = f"{start_ctrl}.IK0_FK1"
    setRange_outputs = hjk.create_setRange_node(switch_attr, rangeX=[0, 10, 0, 1])
    
    # 원본 조인트에 FK/IK 블렌드 연결
    for org_jnt, fk_jnt, ik_jnt in zip(new_joints, fk_joints, ik_joints):
        blend_outputs = hjk.create_blendColor_node(
            setRange_outputs[0],
            fk_jnt,
            ik_jnt,
            translate=True,
            rotate=True,
            scale=True
        )
        # blendColor output을 원본 조인트에 연결
        cmds.connectAttr(blend_outputs[0], f"{org_jnt}.translate", force=True)
        cmds.connectAttr(blend_outputs[1], f"{org_jnt}.rotate", force=True)
        cmds.connectAttr(blend_outputs[2], f"{org_jnt}.scale", force=True)
    
    print(f"Created tongue joints: {new_joints}")
    print(f"Created FK joints: {fk_joints}")
    print(f"Created IK joints: {ik_joints}")
    print(f"Created FK controllers: {fk_ctrls}")
    print(f"Created IK controllers: {ik_ctrls}")
    print(f"IK/FK Switch: {switch_attr} (0=IK, 10=FK)")
    print(f"Stretch Control: {start_ctrl}.Stretch (0=Off, 1=On)")
    
    return new_joints, fk_joints, ik_joints, fk_ctrls, ik_ctrls, start_ctrl


def create_tongue_joints_from_selection(sel, num_joints):
    """선택된 오브젝트 위치에 따라 조인트 생성"""
    joints = []
    if len(sel) >= num_joints:
        # 충분한 선택이 있으면 그 위치에 조인트 생성
        for i in range(num_joints):
            cmds.select(cl=True)
            pos = cmds.xform(sel[i], q=True, ws=True, t=True)
            jnt = cmds.joint(p=pos)
            joints.append(jnt)
    else:
        # 선택이 부족하면 기본 위치에 생성
        joints = create_tongue_joints_default(num_joints)
    return joints


def create_tongue_joints_default(num_joints):
    """기본 위치에 혀 조인트 생성 (Y축 방향으로)"""
    joints = []
    cmds.select(cl=True)
    for i in range(num_joints):
        pos = (0, i * 2, 0)  # Y축 방향으로 2단위씩
        if i == 0:
            jnt = cmds.joint(p=pos)
        else:
            jnt = cmds.joint(p=pos)
        joints.append(jnt)
    return joints


# 실행
sel = cmds.ls(sl=True)
if sel:
    tongue_joints, fk_joints, ik_joints, fk_ctrls, ik_ctrls, main_ctrl = create_tongue_joints_IKFK(
        num_joints=6,
        ctrl_size=2.0
    )
    cmds.select(tongue_joints + fk_ctrls + ik_ctrls + [main_ctrl])
    print(f"\nIK/FK 스위치 사용법:")
    print(f"  {main_ctrl}.IK0_FK1 속성을 조절하세요. (0 = IK 모드, 10 = FK 모드)")
    print(f"  {main_ctrl}.Stretch 속성을 조절하세요. (0 = Off, 1 = On)")
else:
    print("커브나 오브젝트를 선택한 후 스크립트를 실행하세요.")
    print("또는 기본 위치에 조인트를 생성하려면 아래 코드의 주석을 해제하세요:")
    print("# tongue_joints, fk_joints, ik_joints, fk_ctrls, ik_ctrls, main_ctrl = create_tongue_joints_IKFK(num_joints=4, ctrl_size=1.0)")
