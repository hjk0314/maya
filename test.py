import re
import pymel.core as pm


# 79 char line ================================================================
# 72 docstring or comments line ========================================


# def getPos():
#     sel = pm.ls(sl=True)
#     pos = {j: pm.xform(k, q=True, t=True, ws=True) for j, k in enumerate(sel)}
#     return pos



sel = pm.ls(sl=True)

new = 'new_46_grp'
for j, k in enumerate(sel):
    slice = re.search(r"(.*)([0-9]+)(.*)", new)
    grp1, grp2, grp3 = [slice.group(i) for i in range(1, 4)]
    num = int(grp2) + j
    num = str(num)
    result = grp1 + num + grp3
    pm.rename(k, result)