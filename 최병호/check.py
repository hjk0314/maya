import maya.OpenMaya as om
import pymel.core as pm


# Select objects with duplicate names.
def sameName():
    sel = pm.ls(tr=True)
    dup = [i for i in sel if "|" in i]
    if dup:
        pm.select(dup)
        om.MGlobal.displayError("아웃라이너에 중복된 이름을 선택했습니다.")
    else:
        om.MGlobal.displayInfo("중복된 이름 없음")

