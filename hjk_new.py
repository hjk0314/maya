import pymel.core as pm


# def createCurvePassingThrough(startFrame: int, endFrame: int) -> None:
#     for frame in range(startFrame, endFrame + 1):
#         pm.currentTime(frame)
#         pm.curve(p=positions, d=3)


# def createCurve():
#     selections = pm.ls(sl=True, fl=True)
#     for i in selections:
#         getPositions(i)



# def getPosition(object: str):
#     try:
#         xyz = pm.pointPosition(object) # MeshVertex
#     except:
#         xyz = pm.xform(object, q=1, ws=1, rp=1) # Transform
#     return xyz
