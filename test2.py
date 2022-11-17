import re
import pymel.core as pm


# Match attributes of referenced shape to deformed shape's attributes.
class MatchAttr:
    def __init__(self):
        """ When you apply a deformer to a referenced object, 
        a deformed node is created in this scene. 
        There are some cases 
        below to apply 'anorld catclark attribute' to the deformed node.
        Case 1 : When 'referenced' and 'deformed' are together
        Case 2 : When 'referenced' and not 'deformed'
        Case 3 : when not 'referenced' and 'deformed'
        Case 4 : When it is an object created in this scene.
         """
        self.attrName = {
            'aiSubdivType': 1, 
            'aiSubdivIterations': 1, 
        }
        self.conditions()


    def conditions(self):
        """ 1. Select only objects that object type is mesh, 
        2. Determines the referenced and Deformed created in this scene. 
        3. And compare the names and match, 
        4. For use 'pm.setAttr()', 'pm.rename()' in pymel's commands, 
        5. get attribute infomations from the Referenced shape.
        6. And match the attributes to Deformed. 
        7. Finally, rename it by deleting 'Deformed' from the name.
         """
        objs = self.selObj()
        allShape = pm.ls(objs, dag=True, s=True)
        referenced = pm.ls(allShape, rn=True)
        notReferenced = [i for i in allShape if not i in referenced]
        deformed = [i for i in notReferenced if re.search('.*Deformed', i.name())]
        created = [i for i in notReferenced if not i in deformed]
        if not objs:
            print("Nothing selected.")
        else:
            """ Case 1 """
            if referenced and deformed:
                attrInfo = self.getAttrInfo(referenced)
                result = self.syncAttrDeformed(attrInfo, deformed)
                print('\n'.join(result))
            """ Case 2 """
            if referenced and (not deformed):
                pass
                # attrInfo = self.getAttrInfo(referenced)
                # result = [f"{name}: {attr}" for name, attr in attrInfo.items()]
                # print('\n'.join(result))
            """ Case 3 """
            if (not referenced) and deformed:
                result = self.setCatclark(deformed)
                print('\n'.join(result))
            """ Case 4 """
            if created:
                result = self.setCatclark(created)
                print('\n'.join(result))


    # Select only objects that object type is mesh,
    def selObj(self) -> list:
        sel = pm.ls(sl=True, s=True, dag=True)
        objList = []
        for i in sel:
            if pm.objectType(i) == "mesh":
                obj = i.getParent()
                objList.append(obj)
            else:
                continue
        objSet = set(objList)
        result = list(objSet)
        return result


    # Get attributes infomations from the Referenced shape.
    def getAttrInfo(self, shape: list) -> dict:
        result = {}
        for shapeName in shape:
            attr = {i: pm.getAttr(f"{shapeName}.{i}") for i in self.attrName}
            result[shapeName] = attr
        return result


    # And match the attributes to Deformed.
    def syncAttrDeformed(self, attrInfo: dict, deformed: list) -> list:
        """ First, remove the 'Deformed' letter from the shape. 
        Compares the name of the reference. 
        Get attributes information, applied to deformed shape.
         """
        result = []
        for shapeDeformed in deformed:
            removeDeformed = shapeDeformed.rsplit("Deformed", 1)[0]
            for shapeReferenced, attrs in attrInfo.items():
                chk = re.search(f'.*[:]{removeDeformed}', shapeReferenced.name())
                if chk:
                    for attrName, attrValue in attrs.items():
                        pm.setAttr(f"{shapeDeformed}.{attrName}", attrValue)
                else:
                    continue
                result.append(f"{shapeDeformed} -> {removeDeformed} = {attrs}")
            pm.rename(shapeDeformed, removeDeformed)
        return result


    # Put a value in the attribute.
    def setCatclark(self, shape: list) -> list:
        result = []
        for shapeName in shape:
            for attr, value in self.attrName.items():
                pm.setAttr(f"{shapeName}.{attr}", value)
                result.append(f"{shapeName}.{attr} = {value}")
        return result


MatchAttr()
