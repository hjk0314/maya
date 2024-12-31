import pymel.core as pm
import re



def getVertexNumberOnly() -> dict:
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
    sel = [pm.PyNode(i) for i in args] if args else pm.selected()
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
    print(f"joints : {joints}")
    print(f"objects : {objects}")


