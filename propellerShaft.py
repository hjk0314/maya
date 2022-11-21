import pymel.core as pm


# Create locators in boundingBox.
# 'jnt=True' option available.
def createLoc(**kwargs):
    sel = pm.ls(sl=True)
    if not sel:
        pass
    else:
        # bb is boundingBox
        bb = pm.xform(sel, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMin + xMax) / 2
        y = (yMin + yMax) / 2
        z = (zMin + zMax) / 2
        loc = pm.spaceLocator()
        pm.move(loc, x, y, z)
        if not kwargs:
            pass
        else:
            for key, value in kwargs.items():
                if key == "jnt" and value:
                    pm.select(cl=True)
                    jnt = pm.joint(p=(0,0,0), rad=10)
                    pm.matchTransform(jnt, loc, pos=True)
                    pm.delete(loc)
                else:
                    pass


# Create an ikHandle and a controller on both joints.
def propellerShaft():
    sel = pm.ls(sl=True)
    joint1, joint2 = sel
    pm.parent(joint2, joint1)
    # Freeze and orient joints
    pm.makeIdentity(joint1, joint2, a=True, jo=True, n=0)
    pm.joint(joint1, e=True, oj='xyz', sao='yup', ch=True, zso=True)
    pm.joint(joint2, e=True, oj='none', ch=True, zso=True)
    # create a "ik single chain handle"
    ikH = pm.ikHandle(sj=joint1, ee=joint2, sol='ikSCsolver')
    ikH = ikH[0]
    # create a controller and place.
    pointList = [(0,1,1), (0,1,-1), (0,-1,-1), (0,-1,1), (0,1,1)]
    cuv = pm.curve(d=1, p=pointList)
    cuvGrp = pm.group(cuv)
    pm.matchTransform(cuvGrp, joint2, pos=True, rot=True)
    pm.parent(ikH, cuv)
    # select controller's curve points.
    cuvShp = pm.ls(cuv, dag=True, s=True)
    cuvShp = cuvShp[0]
    pm.select(f"{cuvShp}.cv[0:]")


createLoc(jnt=True)
# propellerShaft()