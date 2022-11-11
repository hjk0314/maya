import os
import pathlib
import pymel.core as pm


# Select mesh only.
def selObj() -> list:
    sel = pm.ls(sl=True, s=True, dag=True)
    meshList = {i.getParent() for i in sel if pm.objectType(i) == "mesh"}
    result = list(meshList)
    # pm.select(result)
    return result


# Create reference and their handle.
def createRef(fullPath):
    src = fullPath # r"C:\Users\jkhong\Desktop\a.abc"
    fileName = os.path.basename(src)
    name, ext = os.path.splitext(fileName)
    resolvedName = pm.createReference(
        src, # full path
        gl=True, # groupLocator
        shd="shadingNetworks", # sharedNodes
        mnc=False, # mergeNamespacesOnClash
        ns=name # namespace
    )
    refName = pm.referenceQuery(resolvedName, rfn=True) # reference name
    refNS = pm.referenceQuery(resolvedName, ns=True) # namespace
    return refName, refNS


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
    

def getReferencedObj(abcPath: list) -> list:
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
    referencedObj = pm.referenceQuery(referencedName, n=True)
    return referencedObj


sel = selObj()
abc = getAlembicPath(sel)
obj = []
for i in abc:
    for j in getReferencedObj(i):
        obj.append(j)


sel = pm.ls(sel, dag=True, s=True)
deformed = [i for i in sel if 'Deformed' in i]



