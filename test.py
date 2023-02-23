import pymel.core as pm


def createLoc():
    sel = pm.ls(sl=True)
    for i in sel:
        loc = pm.spaceLocator()
        pm.matchTransform(loc, i, pos=True)


def connNodes():
    sel = pm.ls(sl=True)
    num = len(sel)
    countSetRange = (num//3) + (1 if num%3 else 0)
    setRangeList = []
    for i in range(countSetRange):
        tmp = pm.shadingNode("setRange", au=True)
        pm.setAttr(f"{tmp}.maxX", 180)
        pm.setAttr(f"{tmp}.maxY", 180)
        pm.setAttr(f"{tmp}.maxZ", 180)
        pm.setAttr(f"{tmp}.oldMinX", 0 + (i * 3))
        pm.setAttr(f"{tmp}.oldMinY", 1 + (i * 3))
        pm.setAttr(f"{tmp}.oldMinZ", 2 + (i * 3))
        pm.setAttr(f"{tmp}.oldMaxX", 1 + (i * 3))
        pm.setAttr(f"{tmp}.oldMaxY", 2 + (i * 3))
        pm.setAttr(f"{tmp}.oldMaxZ", 3 + (i * 3))
        setRangeList.append(tmp)
    for j, k in enumerate(sel):
        prev = sel[j-1]
        curr = k
        next = sel[0] if j+1 >= num else sel[j+1]
        setRangeNode = setRangeList[j//3]
        print(setRangeNode, j//3)
        plusMinusNode = pm.shadingNode("plusMinusAverage", au=True)
        pm.setAttr(f"{plusMinusNode}.operation", 2)
        pm.setAttr(f"{plusMinusNode}.input1D[1]", 180)
        out = ["outValueX", "outValueY", "outValueZ"]
        pm.connectAttr(f"{setRangeNode}.{out[j%3]}", f"{k}.rotateX", f=True)
        pm.connectAttr(f"{k}.rotateX", f"{plusMinusNode}.input1D[0]", f=True)
        pm.connectAttr(f"{plusMinusNode}.output1D", f"{prev}.visibility", f=True)
    

