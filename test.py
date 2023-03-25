import pymel.core as pm


def getRadius(*args):
    """ Create the controller 1.2 times the sizeUp of the object.
    If no parameters are given, the selected object is used.
     """
    SIZEUP = 1.2
    sel = args if args else pm.ls(sl=True)
    result = []
    for obj in sel:
        bBox = pm.xform(obj, q=True, bb=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bBox
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        radius = max([x, y, z])
        radius = round(radius*SIZEUP, 3)
        result.append(radius)
    return result



