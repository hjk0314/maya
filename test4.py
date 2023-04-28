import pymel.core as pm


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

