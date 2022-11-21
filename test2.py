import pymel.core as pm



min = pm.playbackOptions(q=True, min=True)
max = pm.playbackOptions(q=True, max=True)
motionPath = pm.pathAnimation(fm=True, f=True, fa='x', ua='y', wut='vector', wu=(0,1,0), iu=False, inverseFront=False, b=False, stu=min, etu=max)



pm.cutKey(motionPath, cl=True)

