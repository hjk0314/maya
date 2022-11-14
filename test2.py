import os
import re
import pymel.core as pm


# Select mesh only.
def selObj() -> list:
    sel = pm.ls(sl=True, s=True, dag=True)
    meshList = {i.getParent() for i in sel if pm.objectType(i) == "mesh"}
    result = list(meshList)
    # pm.select(result)
    return result


def getAlembicPath(sel: list) -> list:
    referencedList = {i for i in sel if pm.referenceQuery(i, inr=True)}
    referencedList = list(referencedList)
    referencedPath = {pm.referenceQuery(i, f=True) for i in referencedList}
    referencedPath = list(referencedPath)
    abcPath = []
    for i in referencedPath:
        if 'mdl/pub' in i:
            replacedPath = i.replace('scenes', 'data/alembic')
            dir = os.path.dirname(replacedPath)
            abc = os.listdir(dir)
            for j in abc:
                if j.endswith('abc') and not (j in abcPath):
                    abcPath.append(f'{dir}/{j}')
                else:
                    continue
        else:
            continue
    return abcPath
    

def getReferencedName(abcPath: list) -> list:
    name = os.path.basename(abcPath)
    name, ext = os.path.splitext(name)
    resolvedName = pm.createReference(
        abcPath, # abcPath
        gl=True, # groupLocator
        shd="shadingNetworks", # sharedNodes
        mnc=False, # mergeNamespacesOnClash
        ns=name # namespace: fileName
    )
    referencedName = pm.referenceQuery(resolvedName, rfn=True)
    return referencedName


sel = selObj()
selShp = pm.ls(sel, dag=True, s=True)
referencedList = {i for i in selShp if pm.referenceQuery(i, inr=True)}
referencedList = list(referencedList)
deformedList = []
for i in selShp:
    A = ":" in i
    B = "Deformed" in i
    if A and B:
        deformedList.append(i)

syncDict = {}
for i in deformedList:
    temp = re.search('(.*)Deformed', i)
    obj = temp.group(1)
    for j in referencedList:
        ref = j.rsplit(":", 1)[-1]
        if obj == ref:
            syncDict[j] = i
        else:
            continue



# abc = getAlembicPath(sel)
# RN = [getReferencedName(i) for i in abc]
# abcShp = {}
# for i in RN:
#     nodes = pm.referenceQuery(i, n=True)
#     abcShp[i] = pm.ls(nodes, dag=True, s=True)

#     referencedObj = pm.referenceQuery(referencedName, n=True)
#     referencedObj = pm.ls(referencedObj, dag=True, s=True)
#     # pm.FileReference(resolvedName).remove()
#     # pm.FileReference(referencedName).remove()
# for i in abc:
#     RN, objs = bringAlembicFile(i)
#     for j in objs:
#         obj.append(j)
# pm.FileReference(abc).remove()


# sel = pm.ls(sel, dag=True, s=True)
# deformed = [i for i in sel if 'Deformed' in i.name()]


# sel = pm.ls(sl=True, dag=True, s=True)
# p1, p2 = sel
for i in syncDict:
    A = i
    B = syncDict[i]
    attrA = pm.listAttr(A, r=True, sa=True, lf=True)
    attrB = pm.listAttr(B, r=True, sa=True, lf=True)
    attrADict = {}
    for i in attrA:
        try:
            attrADict[i] = pm.getAttr(f'{A}.{i}')
        except:
            continue
    attrBDict = {}
    for i in attrB:
        try:
            attrBDict[i] = pm.getAttr(f'{B}.{i}')
        except:
            continue
    diffList = [i for i in attrADict if attrADict[i] != attrBDict[i]]
    for i in diffList:
        pm.setAttr(f"{B}.{i}", attrADict[i])
