from typing import Tuple
import maya.cmds as cmds
import hjk3



def create_sign_deform(mdl_curve) -> Tuple[str, list, list]:
    """ 모델링에 있는 시그니처 커브를 선택하고, 이 함수를 실행.
    커브를 복사하고, sign deformer를 적용한 후, 
    1. 복사된 커브 이름을 반환
    2. 디포머 목록 반환
    3. 시그니처 깃을 움직이게 하는 스플라인 커브상의 로케이터 목록을 반환

    선택 예 : char_peacockA_mdl_v9999:peacockA_signature_v_01_curve
    결과 값 : curve_name, [sign, signHandle], [loc_null_1, loc_null_2, ...]
    """

    # 모델링 커브의 이름 변형
    slices1 = mdl_curve.split(":")[-1]
    slices1 = slices1.split("_")
    slices1[0] = "signCurve"
    sign_cuv = "_".join(slices1[:-1])

    # 커브를 복사
    sign_cuv = cmds.duplicate(mdl_curve, rr=True, n=sign_cuv)[0]
    cmds.parent(sign_cuv, w=True)

    # 사인 핸들을 만듦
    slices1[0] = "signHandle"
    sign_handle = "_".join(slices1[:-1])
    sign_nodes = cmds.nonLinear(sign_cuv, type="sine", n=sign_handle)
    sign_parameter, sign_transform = sign_nodes

    # 사인 핸들 셋팅
    cmds.rotate(-90, 0, 0, sign_transform, r=True, os=True, fo=True)
    cmds.matchTransform(sign_transform, mdl_curve, pos=True)
    cmds.setAttr(f"{sign_parameter}.highBound", 4.5)
    cmds.setAttr(f"{sign_parameter}.lowBound", 0)
    cmds.setAttr(f"{sign_parameter}.dropoff", -1)

    # 로케이터 목록 : locator_nulls
    slices1[0] = "splloc"
    spline_locator_grp = "_".join(slices1[:-1]) + "_grp"
    locator_grps = cmds.listRelatives(spline_locator_grp, children=True)
    locator_nulls = []
    for locator_grp in locator_grps:
        locator_null = locator_grp.replace("_grp", "_null")
        locator_nulls.append(locator_null)
    
    # 로케이터 목록 반환
    return sign_cuv, sign_nodes, locator_nulls
    



def create_pointOnCurveNode_and_settings(mdl_cuv):
    # 커브, 디포머, 로케이터
    dup_cuv, sign_nodes, locator_nulls = create_sign_deform(mdl_cuv)

    # 그룹 정리
    dup_cuv_slices = dup_cuv.split("_")
    dup_cuv_slices[0] = "signDeform"
    signDeform_grp = "_".join(dup_cuv_slices) + "_grp"
    cmds.group(em=True, n=signDeform_grp)
    cmds.parent(dup_cuv, signDeform_grp)

    sign_parameter, sign_transform = sign_nodes
    cmds.parent(sign_transform, signDeform_grp)

    # pointOnCurve 연결
    for loc_null in locator_nulls:
        # pointOnCurve에 연결될 로케이터 생성과 준비
        loc_null_slices = loc_null.split("_")
        loc_null_slices[0] = "signLoc"
        sign_loc_name = loc_null_slices[:-1]
        sign_loc_name = "_".join(sign_loc_name)
        sign_loc = cmds.spaceLocator(p=(0, 0, 0), n=sign_loc_name)[0]
        sign_loc_nodes = hjk3.group_with_pivot(sign_loc, null=True)[0]
        sign_loc_grp, sign_loc_null, sign_loc = sign_loc_nodes
        cmds.parent(sign_loc_null, w=True)
        cmds.matchTransform(sign_loc_grp, loc_null, pos=True, rot=True)
        cmds.matchTransform(sign_loc_null, loc_null, pos=True, rot=True)

        # pointOnCurveInfo 노드 생성과 연결
        poci = cmds.shadingNode("pointOnCurveInfo", au=True)
        param = hjk3.get_pointOnCurve_parameter(dup_cuv, loc_null)
        cmds.setAttr(f"{poci}.parameter", param)
        _, dup_cuv_shp = hjk3.get_deformed_shape(dup_cuv)
        cmds.connectAttr(f"{dup_cuv_shp}.worldSpace[0]", f"{poci}.inputCurve", f=True)
        cmds.connectAttr(f"{poci}.position", f"{sign_loc_grp}.translate", f=True)
        cmds.parentConstraint(sign_loc_grp, sign_loc, mo=True, w=1.0)
        cmds.connectAttr(f"{sign_loc}.translateX", f"{loc_null}.translateX", f=True)

        # 그룹 정리
        cmds.parent(sign_loc_grp, signDeform_grp)
        cmds.parent(sign_loc_null, signDeform_grp)



# sel = cmds.ls(sl=True)
# for mdl_cuv in sel:
#     create_pointOnCurveNode_and_settings(mdl_cuv)




def create_animCurve_and_set_key(tl=False, ta=False, tu=False, tt=True, keys={}, node_name=""):
    """ in tangent type : ["spline", "linear", "fast", "slow", "flat", "step", "stepnext", "fixed", "clamped", "plateau", "auto", "autoease", "automix", "autocustom"]
    """

    if tl:
        typ = "animCurveTL"
    elif ta:
        typ = "animCurveTA"
    elif tu:
        typ = "animCurveTU"
    elif tt:
        typ = "animCurveTT"
    else:
        typ = ""
    

    if not typ:
        return


    animCurve = cmds.createNode(typ, name=node_name)


    for key, val in keys.items():
        cmds.setKeyframe(animCurve, t=key, v=val)


    cmds.keyTangent(node_name, edit=True, itt='linear', ott='linear')





