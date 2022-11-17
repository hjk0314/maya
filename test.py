import re
import os
import subprocess
import maya.OpenMaya as om
import pymel.core as pm


# 79 char line ================================================================
# 72 docstring or comments line ========================================


def cPoint():
    sel = pm.ls(sl=True, fl=True)
    for j in [pm.pointPosition(i) for i in sel]:
        print(j)


def createCircle():
    sel = pm.ls(sl=True)
    for i in sel:
        cc = pm.circle(c=(0,0,0), nr=(1,0,0), ch=False, sw=180)
        pm.matchTransform(cc, i, pos=True, rot=True)


def matchLoc():
    sel = pm.ls(sl=True)
    for i in sel:
        loc = pm.spaceLocator()
        pm.matchTransform(loc, i, pos=True)


# Seperate with Material Name.
def seperateMat():
    sel = pm.ls(sl=True)
    for j in sel:
        sepList = pm.polySeparate(j, ch=False)
        for k in sepList:
            shd = k.shadingGroups()[0] # shading engine
            all = pm.listConnections(shd) # All connecting list
            mat = pm.ls(all, mat=True)[0] # Only Material name
            pm.rename(k, f"{k}_{mat}")


# Match attributes of referenced shape to deformed shape's attributes.
class MatchAttr:
    ''' 1. Select only objects that object type is mesh,
    2. find out the source, 
    Determines the referenced shape and the shape created in this scene.
    3. If you compare the two names and match, 
    Get a string to use 'pm.setAttr()'.
    4. And match the attributes of Deformed and Referenced
    Rename it by deleting 'Deformed' from the name.
    '''
    def __init__(self):
        self.main()


    # main process
    def main(self):
        sel = self.selObj() # 1
        if not sel:
            print("Nothing selected.")
        else:
            shp = pm.ls(sel, dag=True, s=True)
            ref = self.getReferenced(shp)
            rig = self.getDeformed(shp)
            cmp = self.getCompared(ref, rig)
            print(rig)
            # attrStr = self.getAttrStr(cmp)
            # if not attrStr:
            #     print("Nothing to do.")
            # else:
            #     print("# Matched the attributes. #")
            #     self.makeTheSame(attrStr)


    # 1. Select only objects that object type is mesh,
    def selObj(self) -> list:
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


    # 2. find out the source, 
    # Determines the referenced shape and the shape created in this scene.
    def getReferenced(self, shape: list) -> list:
        result = {i for i in shape if pm.referenceQuery(i, inr=True)}
        result = list(result)
        return result


    # 2. find out the source, 
    # Determines the referenced shape and the shape created in this scene.
    def getDeformed(self, shape: list) -> list:
        result = []
        for i in shape:
            A = ":" in i.name()
            B = "Deformed" in i.name()
            if not A and B:
                result.append(i)
        return result


    # 3. If you compare the two names and match, 
    def getCompared(self, ref: list, rig: list) -> dict:
        result = {}
        for i in rig:
            tmp = re.search('(.*)Deformed', i.name()) # (abcd_efg)Defromed
            obj = tmp.group(1) # abcd_efg
            for j in ref:
                ref = j.rsplit(":", 1)[-1] # namespace:abcd_efg
                if obj == ref:
                    result[j] = i # {"referencedAttr": "DeformedAttr"}
                    print(result)
                else:
                    continue
        return result


    # 4. Get a string to use 'pm.setAttr()'.
    def getAttrStr(self, compare: dict) -> dict:
        attrName = [
            'aiSubdivType', 
            'aiSubdivIterations', 
        ]
        diff = {}
        for ref, rig in compare.items():
            for i in attrName:
                refAttr = pm.getAttr(f"{ref}.{i}")
                rigAttr = pm.getAttr(f"{rig}.{i}")
                if refAttr == rigAttr:
                    continue
                else:
                    diff[f"{rig}.{i}"] = refAttr
        return diff


    # 5. And match the attributes of Deformed and Referenced
    # Rename it by deleting 'Deformed' from the name.
    def makeTheSame(self, attrStr: dict) -> None:
        renameDict = {}
        for attr, value in attrStr.items():
            pm.setAttr(attr, value)
            # pCylinderShape1Deformed.aiSubdivType
            tmp = re.search('((.*)Deformed)(.*)', attr)
            org = tmp.group(1) # -> pCylinderShape1Deformed
            new = tmp.group(2) # -> pCylinderShape1
            mod = tmp.group(3) # -> .aiSubdivType
            renameDict[org] = new
            print(f"{attr} -> {new}{mod} = {value}")
        for org, new in renameDict.items():
            # pm.rename('pCylinderShape1Deformed', 'pCylinderShape1')
            pm.rename(org, new)

