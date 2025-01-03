import pymel.core as pm
import re



def getVertexNumber() -> dict:
    """ Get vertex numbers only, strip others. """
    sel = pm.ls(sl=True)
    obj = pm.ls(sel, o=True)
    shapes = set(obj)
    result = {}
    for shp in shapes:
        pattern = r'\.vtx\[\d+(?::\d+)?\]'
        vertexNumbers = []
        for i in sel:
            try:
                temp = re.search(pattern, i.name())
                vertexNumbers.append(temp.group())
            except:
                continue
        result[shp.getParent().name()] = vertexNumbers
    return result


def createPaintWeightToOne(maxInfluence: int, *args):
    """ Paint Skin Weights to One.
     - Create paintSkinWeights with value 1.
     - Create a dictionary with the vertex weight values in this way.
     - Paint the skin weights with the given max influence.
     - Finally, Create paint skin weights from the dictionary.
     """
    sel = [pm.PyNode(i) for i in args] if args else pm.selected()
    # Create a list of objects and joints.
    joints = []
    objects = []
    for i in sel:
        shp = i.getShape()
        if shp and pm.ls(shp, type=["mesh", "nurbsSurface"]):
            objects.append(i)
        elif i.type() == "joint":
            joints.append(i)
        else:
            continue
    # Get vertex information and paint skin weight with max influence.
    for obj in objects:
        data = {}
        isSkinCluster = pm.listHistory(obj, type="skinCluster")
        if isSkinCluster:
            pm.warning("skinCluster aleady exists.")
            continue
        skinClt = pm.skinCluster(joints, obj, toSelectedBones=False, bindMethod=0, skinMethod=0, normalizeWeights=1, wd=0, mi=1)
        for jnt in joints:
            pm.select(cl=True)
            pm.skinCluster(skinClt, e=True, siv=jnt)
            data[jnt] = getVertexNumber()
        pm.select(cl=True)
        pm.skinCluster(obj, e=True, mi=maxInfluence)
        # Unlock
        lockWeights = []
        for j in data.keys():
            lockWeights.append(pm.getAttr(f"{j}.liw"))
            pm.setAttr(f"{j}.liw", 0)
        for jntName, obj_vtxList in data.items():
            for obj, vtxList in obj_vtxList.items():
                if not pm.objExists(obj):
                    continue
                for vtx in vtxList:
                    objVtx = f"{obj}{vtx}"
                    skinClt = pm.listHistory(objVtx, type="skinCluster")
                    try:
                        # Paint Skin Weights to One.
                        pm.skinPercent(skinClt[0], objVtx, transformValue=(jntName, 1))
                        pm.displayInfo(f"{objVtx} was painted successfully.")
                    except:
                        pm.warning(f"{objVtx} failed to be painted.")
                        continue
        # Lock Weights again.
        for j, onOff in zip(data.keys(), lockWeights):
            pm.setAttr(f"{j}.liw", onOff)


