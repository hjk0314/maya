import pymel.core as pm
import hjk


def createLoc():
    sel = pm.selected()
    num = [458, 474]
    for i in sel:
        for j in num:
            vtx = i.vtx[j]
            pos = vtx.getPosition(space="world")
            pm.select(cl=True)
            jnt = pm.joint(p=(0, 0, 0))
            # loc = pm.spaceLocator()
            pm.move(jnt, pos)


def temp1():
    for i in pm.selected():
        pm.select(cl=True)
        jnt = pm.joint(p=(0,0,0))
        pm.matchTransform(jnt, i, pos=True)

    
def temp2():
    sel = pm.selected()
    for j, k in enumerate(sel):
        num = (j+1) * 2
        pm.rename(k, f"jnt_{num}")


def temp3():
    sel = pm.selected()
    for j, k in enumerate(sel):
        try:
            one = sel[j]
            two = sel[j+1]
            pm.parent(two, one)
        except:
            continue


def temp4():
    jntList = [f"jnt_{i}" for i in range(3, 298, 2)]
    objList = pm.selected()
    for i in range(len(jntList)):
        pm.parentConstraint(jntList[i], objList[i], w=1.0, mo=True)
    

def temp5():
    for i in range(1, 20):
        pm.parent(f"clt_{i}_grp", f"cc_{i}")
        pm.setAttr(f"clt_{i}_grp.visibility", 0)


def temp6():
    jntList = [f"jnt_{i}" for i in range(3, 298, 2)]
    numList = [i for i in range(1, 149)]
    numList = sorted(numList, reverse=True)
    obj = "prop_bandolier_mdl_v9999:bandolier_magazine"
    objList = [f"{obj}_{i}_grp" for i in numList]
    print(jntList)
    print(numList)
    print(len(jntList), len(numList))
    for i in range(len(jntList)):
        pm.parentConstraint(jntList[i], objList[i], w=1, mo=True)
        pm.scaleConstraint(jntList[i], objList[i], w=1, mo=True)


def createExpression1(obj, num):
    expr = f"float $bX = {obj}.translateX;\n"
    expr += f"float $bY = {obj}.translateY;\n"
    expr += f"float $bZ = {obj}.translateZ;\n"
    expr += "float $cc10X = cc_10.translateX;\n"
    expr += "float $cc10Y = cc_10.translateY;\n"
    expr += "float $cc10Z = cc_10.translateZ;\n"
    expr += "float $dist = `mag<<$bX-$cc10X, $bY-$cc10Y, $bZ-$cc10Z>>`;\n"
    expr += f"if ($dist > {num}) " + "{\n"
    expr += f"    {obj}.visibility = 0;\n"
    expr += "}\n"
    expr += "else {\n"
    expr += f"    {obj}.visibility = 1;\n"
    expr += "}\n"
    pm.expression(s=expr, o='', ae=1, uc='all')


def createExpression2(num):
    name = "prop_bandolier_mdl_v9999:bandolier_magazine"
    expr = f"float $loc = locator{num}.translateX;\n"
    expr += "if ($loc > 0) {\n"
    expr += f"    {name}_{num}_grp.visibility = 0;" + "} \n"
    expr += "else {\n"
    expr += f"    {name}_{num}_grp.visibility = 1;" + "}"
    pm.expression(s=expr, o='', ae=1, uc='all')


def createExpression3(num):
    expr = f"float $loc1 = locator{num}.translateX;\n"
    expr += f"float $loc2 = locator{num+1}.translateX;\n"
    expr += "if ($loc1 >= 0 && $loc2 < 0) {\n"
    expr += f"    cuv_num_{num}_grp.visibility = 1;" + "}\n"
    expr += "else {\n"
    expr += f"    cuv_num_{num}_grp.visibility = 0;" + "}\n"
    pm.expression(s=expr, o='', ae=1, uc='all')


for i in range(1, 149):
    createExpression3(i)


def temp7():
    jntList = [i for i in range(3, 298, 2)]
    jntList.sort(reverse=True)
    jntList = [f"jnt_{i}" for i in jntList]
    for i in jntList:
        loc = pm.spaceLocator()
        pm.pointConstraint(i, loc, mo=False, w=1.0)
        # pm.orientConstraint(i, loc, mo=True, w=1.0)


def temp8():
    sel = pm.selected()
    for j, k in enumerate(sel):
        grp = k.getChildren()
        pm.rename(k, f"cuv_num_{j+1}_grp")
        for l, m in enumerate(grp):
            cuv = m.getChildren()
            pm.rename(m, f"cuv_num_{j+1}_{l+1}_grp")
            for x, y in enumerate(cuv):
                pm.rename(y, f"cuv_num_{j+1}_{l+1}_{x+1}")
    




