import pymel.core as pm
import math


def getDistance(obj1, obj2):
    result = math.sqrt(sum((a - b)**2 for a, b in zip(obj1, obj2)))
    return result


obj = pm.ls(sl=True)
allVertices = obj.vtx[:]
sourceVertices = {}
for vtx in allVertices:
    pos = vtx.getPosition(space="world")
    if pos[0] <= 0:
        sourceVertices[vtx] = pos
    else:
        continue


