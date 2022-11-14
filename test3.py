import re
import pymel.core as pm


# Select mesh only.
def selObj() -> list:
    sel = pm.ls(sl=True, s=True, dag=True)
    meshList = []
    for i in sel:
        if pm.objectType(i) == "mesh":
            obj = i.getParent()
            meshList.append(obj)
        else:
            continue
    meshSet = set(meshList)
    result = list(meshSet)
    return result


def getReferenced(shape: list) -> list:
    result = {i for i in shape if pm.referenceQuery(i, inr=True)}
    result = list(result)
    return result


def getDeformed(shape: list) -> list:
    result = []
    for i in shape:
        A = ":" in i.name()
        B = "Deformed" in i.name()
        if not A and B:
            result.append(i)
    return result


def getCompared(ref: list, rig: list) -> dict:
    result = {}
    for i in rig:
        temp = re.search('(.*)Deformed', i.name())
        obj = temp.group(1)
        for j in ref:
            ref = j.rsplit(":", 1)[-1]
            if obj == ref:
                result[j] = i
            else:
                continue
    return result


def makeTheSame(compare: dict) -> str:
    for ref, rig in compare.items():
        A = pm.listAttr(ref, r=True, sa=True, lf=True)
        B = pm.listAttr(rig, r=True, sa=True, lf=True)
        attrA = {}
        for i in A:
            try:
                attrA[i] = pm.getAttr(f'{ref}.{i}')
            except:
                continue
        attrB = {}
        for i in B:
            try:
                attrB[i] = pm.getAttr(f'{rig}.{i}')
            except:
                continue
        diff = [i for i in attrA if attrA[i] != attrB[i]]
        diff.remove('intermediateObject')
        if not diff:
            msg = 'Nothing to do.'
        else:
            msg = 'Matched the shape.'
            for i in diff:
                pm.setAttr(f"{rig}.{i}", attrA[i])
        return msg

def main():
    sel = selObj()
    if not sel:
        print("Nothing selected.")
    else:
        shp = pm.ls(sel, dag=True, s=True)
        ref = getReferenced(shp)
        rig = getDeformed(shp)
        cmp = getCompared(ref, rig)
        msg = makeTheSame(cmp)
        if msg == None:
            print("There is no Deformed shape.")
        else:
            print(msg)


main()