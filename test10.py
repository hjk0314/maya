import pymel.core as pm


sel = pm.selected()


def test():
    if len(sel) < 3:
        return

    startJnt = sel[0]
    endJnt = sel[-2]
    cuv = pm.ls(sel, dag=True, type=["nurbsCurve"])[0]
    print(startJnt, endJnt, cuv)
    print(sel[0:-2])

    # cuvInf = pm.shadingNode("curveInfo", au=True)
    # pm.connectAttr(f"{cuv}.worldSpace[0]", f"{cuvInf}.inputCurve", f=True)


