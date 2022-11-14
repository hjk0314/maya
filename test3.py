import re
import pymel.core as pm


# Select mesh only.
def selObj() -> list:
    sel = pm.ls(sl=True, s=True, dag=True)
    meshList = {i.getParent() for i in sel if pm.objectType(i) == "mesh"}
    result = list(meshList)
    # pm.select(result)
    return result


sel = selObj()
selShp = pm.ls(sel, dag=True, s=True)
referencedList = {i for i in selShp if pm.referenceQuery(i, inr=True)}
referencedList = list(referencedList)
deformedList = []
for i in selShp:
    A = ":" in i.name()
    B = "Deformed" in i.name()
    if not A and B:
        deformedList.append(i)

syncDict = {}
for i in deformedList:
    temp = re.search('(.*)Deformed', i.name())
    obj = temp.group(1)
    for j in referencedList:
        ref = j.rsplit(":", 1)[-1]
        if obj == ref:
            syncDict[j] = i
        else:
            continue
# print(syncDict)
for j, k in syncDict.items():
    attrA = pm.listAttr(j, r=True, sa=True, lf=True)
    attrB = pm.listAttr(k, r=True, sa=True, lf=True)
    attrA_Dict = {}
    for i in attrA:
        try:
            attrA_Dict[i] = pm.getAttr(f'{j}.{i}')
        except:
            continue
    attrB_Dict = {}
    for i in attrB:
        try:
            attrB_Dict[i] = pm.getAttr(f'{k}.{i}')
        except:
            continue
diffList = [i for i in attrA_Dict if attrA_Dict[i] != attrB_Dict[i]]
print(diffList)
for i in diffList:
    pm.setAttr(f"{k}.{i}", attrA_Dict[i])