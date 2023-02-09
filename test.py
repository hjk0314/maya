import pymel.core as pm
import maya.mel as mel
import re
import os
from math import *


folder = "U:/DOJ/Rnd/Horse/Output/ABC/horseGroomV0006_sim_v0102"
searchList = ['hair', 'add', ]
extension = '.abc'
fileList = os.listdir(folder)
for i in fileList:
    name, ext = os.path.splitext(i)
    for j in searchList:
        if ext != extension:
            continue
        elif re.match(f'.*{j}.*', i):
            print(f"{folder}/{i}")
            pm.importFile(f"{folder}/{i}")
        else:
            print(f"There are no files matching the {j}")

    #     tmp.group(1)

    # print(checkList)
    # for k in checkList:
    #     if ext == extension:
    #     else:
    #         continue


# for i in sel:
#     tmp = re.match(f'(.*){search}(.*)', i)

# print(tmp)


def createChannels():
    sel = pm.ls(sl=True)
    channelList = [
        "Toe", 
        "Bank", 
        "Twist", 
        "Heel", 
        "Ball", 
        "Down", 
        ]
    # channelList = [
    #     "FKIK_L_F", 
    #     "FKIK_R_F", 
    #     "FKIK_L_B", 
    #     "FKIK_R_B", 
    #     ]
    for i in sel:
        for cName in channelList:
            pm.addAttr(i, ln=cName, at='double', dv=0)
            pm.setAttr(f'{i}.{cName}', e=True, k=True)


def connectBlendColors():
    sel = pm.ls(sl=True)
    tmp = int(len(sel) / 3)
    IK = [sel[i] for i in range(tmp)]
    FK = [sel[i] for i in range(tmp, (tmp*2))]
    FBX = [sel[i] for i in range((tmp*2), (tmp*3))]
    SWITCH = "cc_global.FKIK_Tail"
    setR = pm.shadingNode("setRange", au=True)
    pm.connectAttr(SWITCH, f"{setR}.valueX", f=True)
    for i in range(tmp):
        createBlendColors(SWITCH, setR, IK[i], FK[i], FBX[i])


def createBlendColors(SWITCH, setR, IK, FK, FBX):
    bls = pm.shadingNode("blendColors", au=True)
    pm.connectAttr(f"{FK}.rotate", f"{bls}.color1", f=True)
    pm.connectAttr(f"{IK}.rotate", f"{bls}.color2", f=True)
    pm.connectAttr(f"{bls}.output", f"{FBX}.rotate", f=True)
    pm.setAttr(f"{setR}.oldMaxX", 10)
    pm.setAttr(f"{setR}.maxX", 1)
    pm.connectAttr(f"{setR}.outValueX", f"{bls}.blender", f=True)



# createChannels()
# ctrl(pointer=True)
# rename("cc_tailIK_3")
# rename("cc_spineIn_1")
# sel = pm.ls(sl=True)
# new = sel[0]
# old = sel[1]
# pm.matchTransform(new, old, pos=True)
# pm.rename(new, old)
# connectBlendColors()
# sel = pm.ls(sl=True)
# for i in sel:
#     pm.connectAttr("multiplyDivide6.output", f"{i}.scale", f=True)



def getDistance(sp: list, ep: list):
    x1, y1, z1 = sp
    x2, y2, z2 = ep
    result = sqrt(pow(x1-x2, 2) + pow(y1-y2, 2) + pow(z1-z2, 2))
    result = round(result, 3)
    return result


def getSum(numList):
    sum = 0
    for num in numList:
        sum += num
    return sum


def aald():
    sel = pm.ls(sl=True, fl=True)
    jntList = ['joint3', 'joint4', 'joint6']
    disDict = {}
    for point in sel:
        tmp = {}
        for jnt in jntList:
            posJoint = pm.xform(jnt, q=True, ws=True, rp=True)
            posPoint = point.getPosition()
            distance = getDistance(posPoint, posJoint)
            tmp[jnt] = distance
        sum = getSum(tmp.values())
        for key, value in tmp.items():
            tmp[key] = sum / value
        sum = getSum(tmp.values())
        for key, value in tmp.items():
            tmp[key] = round(value/sum, 3)
        disDict[point.name()] = tmp
    return disDict


# skin = 'skinCluster1'
# data = aald()
# print(data)
# for point, jntValue in data.items():
#     tvList = [(jnt, value) for jnt, value in jntValue.items()]
#     print(pm.skinPercent(skin, point, v=True, ib=0.041, q=True))


