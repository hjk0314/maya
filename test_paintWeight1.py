import pymel.core as pm


def createPaintWeight1(maxInfluence: int, *args):
    sel = args if args else pm.selected()
    joints = []
    objects = []
    for i in sel:
        if not isinstance(i, pm.PyNode):
            i = pm.PyNode(i)
        shp = i.getShape()
        if shp:
            print(i.type())
            objects.append(i)
        else:
            continue
    print(objects)


createPaintWeight1(5)