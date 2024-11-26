import pymel.core as pm


class CreateProxyWheel:
    def __init__(self):
        """ Replace the detailed wheels with proxy wheels. """
        pass


    def main(self):
        sel = pm.selected()
        for i in sel:
            if "wheel" in i.name():
                self.replaceProxyWheel(i)
            else:
                pm.warning("Did you choose the wheel?")
                continue


    def getBoundingBoxPosition(self, vertexOrObject) -> list:
        boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
        x = (xMin + xMax) / 2
        y = (yMin + yMax) / 2
        z = (zMin + zMax) / 2
        return [x, y, z]


    def getBoundingBoxSize(self, vertexOrObject) -> list:
        boundingBox = pm.xform(vertexOrObject, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        boundingBoxSize = [x, y, z]
        result = [round(i, 5) for i in boundingBoxSize]
        return result


    def replaceProxyWheel(self, obj):
        # Object's Information
        objParents = obj.getParent()
        proxyName = obj.name()
        # Duplicate Object and Unparent
        copied = pm.duplicate(obj, rr=True)[0]
        pm.parent(copied, w=True)
        # Create a proxy wheel and locate position.
        for i in ["X", "Y", "Z"]:
            pm.setAttr(f"{copied}.translate{i}", 0)
            pm.setAttr(f"{copied}.rotate{i}", 0)
            pm.setAttr(f"{copied}.scale{i}", 1)
        objPiv = pm.xform(copied, q=True, ws=True, rp=True)
        bbSize = self.getBoundingBoxSize(copied)
        bbPosition = self.getBoundingBoxPosition(copied)
        x, y, z = bbSize
        temp = [x - y, y - z, z - x]
        idx = min(range(len(temp)), key=lambda i: abs(temp[i]))
        if idx == 0:    wheelAxis = (0, 0, 1)
        if idx == 1:    wheelAxis = (1, 0, 0)
        if idx == 2:    wheelAxis = (0, 1, 0)
        proxyWheel = pm.polyCylinder(sc=1, sx=16, ax=wheelAxis, cuv=3, ch=0)
        pm.scale(proxyWheel, bbSize)
        pm.makeIdentity(proxyWheel, a=1, s=1, n=0, pn=1)
        pm.xform(proxyWheel, ws=True, t=bbPosition)
        pm.xform(proxyWheel, ws=True, piv=objPiv)
        # Position the proxy wheel as an object.
        pm.matchTransform(proxyWheel, obj, pos=True, rot=True, scl=True)
        pm.parent(proxyWheel, objParents)
        pm.makeIdentity(proxyWheel, a=1, t=1, n=0, pn=1)
        pm.delete(copied)
        if not obj.isReferenced():
            pm.delete(obj)
        pm.rename(proxyWheel, proxyName)


cpw = CreateProxyWheel()
cpw.main()

