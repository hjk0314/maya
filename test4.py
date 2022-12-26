from hjk import *


# sel = pm.ls(sl=True)
# num = int(len(sel) / 2)
# for i in range(num):
#     tmp = sel[i].replace('mainGear_L_', 'mainGear_R_')
#     pm.rename(sel[i+num], tmp)


# tmp = selObj()
# fullPath = r"T:\KNP\assets\vhcl\boeing747\mdl\dev\scenes\tmp.json"
# dic = {i.name(): i.getParent().name() for i in tmp}
# with open(fullPath, 'w') as JSON:
#     json.dump(dic, JSON, indent=4)
    

# import pymel.core as pm
# import json


# with open(fullPath) as JSON:
#     data = json.load(JSON)
# for obj, grp in data.items():
#     pm.parent(obj, grp)
    
# selGrp()


# tmp = pm.getReferences()
# for j, k in tmp.items():
#     print(k)
#     print(pm.FileReference(k).refNode)
    



# refName = pm.referenceQuery(resolvedName, rfn=True) # reference name
# refNS = pm.referenceQuery(resolvedName, ns=True) # namespace
# isNodeReferenced = pm.referenceQuery(src, inr=True) # bool


# pm.FileReference(resolvedName).remove()
# pm.FileReference(refName).remove()


# rename('jnt_sideGear_L_mainPistonLink_11_1_1')
# rename('sideGear_L', 'sideGear_R')
# ctrl(sph=True)