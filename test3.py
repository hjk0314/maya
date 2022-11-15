import re
import pymel.core as pm


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
            attrStr = self.getAttrStr(cmp)
            if not attrStr:
                print("Nothing to do.")
            else:
                print("# Matched the attributes. #")
                self.makeTheSame(attrStr)


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
            temp = re.search('(.*)Deformed', i.name())
            obj = temp.group(1)
            for j in ref:
                ref = j.rsplit(":", 1)[-1]
                if obj == ref:
                    result[j] = i
                else:
                    continue
        return result


    # 4. Get a string to use 'pm.setAttr()'.
    def getAttrStr(self, compare: dict) -> dict:
        result = {}
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
            # The 'intermediateObject' must be different, 
            # so remove it in diff list.
            diff.remove('intermediateObject')
            if not diff:
                result = False
            else:
                for i in diff:
                    result[f"{rig}.{i}"] = attrA[i]
            return result


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


MatchAttr()