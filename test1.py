import pymel.core as pm


sel = pm.ls(sl=True)


for i in sel:
    print(i)
    skinClt = pm.listHistory(i, type="skinCluster")
    influences = pm.skinCluster(skinClt, q=True, inf=True)
    print(influences)
    # jointIndex = influences.index("Spine")
    # currentWeights = pm.skinPercent(skinClt[0], i, q=True, v=True)
    # print(currentWeights)
    # currentWeights[jointIndex] = 0.9
    # currentWeights[0] = 0.1
    # print(currentWeights)
    # final = pm.skinPercent(skinClt[0], i, transformValue=("Spine", 1))



