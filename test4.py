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


sel = pm.selected()

tmp = [i.name() for i in sel]
    # pm.select(cl=True)
    # jnt = pm.joint(p=(0, 0, 0))
    # pm.matchTransform(jnt, i, pos=True)
print(tmp)