import pymel.core as pm



sel = pm.ls(sl=True)

outLoc, inLoc = sel
midLoc = pm.spaceLocator()
for i in sel:
    pm.pointConstraint(i, midLoc, mo=False, w=0.5)
locList = [outLoc, midLoc, inLoc]

jntList= []
for i in range(3):
    pm.select(cl=True)
    tmp = pm.joint(p=(0,0,0))
    jntList.append(tmp)
outJnt, midJnt, inJnt = jntList
grpList = [pm.group(i, n=f"{i}_grp") for i in jntList]

# loc_Jnt = {locList[i]: jntList[i] for i in range(3)}
for i in range(3):
    pm.parentConstraint(locList[i], grpList[i], mo=False)


