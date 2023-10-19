import pymel.core as pm


class CreateCurves:
    def __init__(self):
        pass


    def createCurvePassingLocators(self, curveClosed=False):
        """ The closedCurve means that 
        the start and end points of a curve are connected. """
        locators = pm.ls(sl=True)
        positions = [self.getPositionObject(i) for i in locators]
        if curveClosed:
            circle = pm.circle(nr=(0, 1, 0), ch=False, s=len(locators))
            circle = circle[0]
            self.matchDotsToPositions(circle, positions)
        else:
            pm.curve(ep=positions, d=3)


    def createCurveConnectingPoints(self):
        """ If you put straightCurve under Locator and freeze it, 
        the pivot will match. """
        selection = pm.ls(sl=True, fl=True)
        initPoint = selection[0]
        lastPoint = selection[-1]
        positions = self.getPositions([initPoint, lastPoint])
        initPosition, lastPosition = positions
        straightCurve = pm.curve(d=1, p=positions)
        initLocator = pm.spaceLocator()
        lastLocator = pm.spaceLocator()
        pm.move(initLocator, initPosition, r=True)
        pm.move(lastLocator, lastPosition, r=True)
        pm.xform(straightCurve, sp=initPosition, rp=initPosition)
        pm.aimConstraint(lastLocator, initLocator)
        pm.delete(initLocator, cn=True)
        pm.parent(straightCurve, initLocator)
        pm.makeIdentity(straightCurve, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(straightCurve, w=True)
        pm.rebuildCurve(straightCurve, d=1, ch=0, s=3, rpo=1, end=1, kr=0, kt=0)


    def createCurveControllers(self, *args):
        """ Create a controller,
        "cub": cub, 
        "sph": sph, 
        "cyl": cyl, 
        "pip": pip, 
        "con1": con1, 
        "con2" : con2, 
        "car": car, 
        "car2": car2, 
        "car3": car3, 
        "ar1": ar1, 
        "ar2": ar2, 
        "ar3": ar3, 
        "ar4": ar4, 
        "ar5": ar5, 
        "pointer": pointer, 
        "foot": foot, 
        "foot2": foot2, 
        "hoof": hoof, 
        "hoof2": hoof2, 
        "sqr": sqr, 
        "cross": cross, 
        "hat": hat, 
        "head": head, 
        "scapula": scapula, 
        """
        # Cube
        cub = [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), ]
        cub += [(1, 1, -1), (-1, 1, -1), (-1, -1, -1), ]
        cub += [(-1, -1, 1), (1, -1, 1), (1, -1, -1), ]
        cub += [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), ]
        cub += [(1, 1, 1), (1, -1, 1), (1, -1, -1), ]
        cub += [(1, 1, -1), ]
        # Sphere
        sph = [(0, 1, 0), (0, 0.7, 0.7), (0, 0, 1), ]
        sph += [(0, -0.7, 0.7), (0, -1, 0), (0, -0.7, -0.7), ]
        sph += [(0, 0, -1), (0, 0.7, -0.7), (0, 1, 0), ]
        sph += [(-0.7, 0.7, 0), (-1, 0, 0), (-0.7, 0, 0.7), ]
        sph += [(0, 0, 1), (0.7, 0, 0.7), (1, 0, 0), ]
        sph += [(0.7, 0, -0.7), (0, 0, -1), (-0.7, 0, -0.7), ]
        sph += [(-1, 0, 0), (-0.7, -0.7, 0), (0, -1, 0), ]
        sph += [(0.7, -0.7, 0), (1, 0, 0), (0.7, 0.7, 0), ]
        sph += [(0, 1, 0), ]
        # Cylinder
        cyl = [(-1, 1, 0), (-0.7, 1, 0.7), (0, 1, 1), ]
        cyl += [(0.7, 1, 0.7), (1, 1, 0), (0.7, 1, -0.7), ]
        cyl += [(0, 1, -1), (0, 1, 1), (0, -1, 1), ]
        cyl += [(-0.7, -1, 0.7), (-1, -1, 0), (-0.7, -1, -0.7), ]
        cyl += [(0, -1, -1), (0.7, -1, -0.7), (1, -1, 0), ]
        cyl += [(0.7, -1, 0.7), (0, -1, 1), (0, -1, -1), ]
        cyl += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
        cyl += [(1, 1, 0), (1, -1, 0), (-1, -1, 0), ]
        cyl += [(-1, 1, 0), ]
        # Pipe
        pip = [(0, 1, 1), (0, -1, 1), (0.7, -1, 0.7), ]
        pip += [(1, -1, 0), (1, 1, 0), (0.7, 1, -0.7), ]
        pip += [(0, 1, -1), (0, -1, -1), (-0.7, -1, -0.7), ]
        pip += [(-1, -1, 0), (-1, 1, 0), (-0.7, 1, 0.7), ]
        pip += [(0, 1, 1), (0.7, 1, 0.7), (1, 1, 0), ]
        pip += [(1, -1, 0), (0.7, -1, -0.7), (0, -1, -1), ]
        pip += [(0, 1, -1), (-0.7, 1, -0.7), (-1, 1, 0), ]
        pip += [(-1, -1, 0), (-0.7, -1, 0.7), (0, -1, 1), ]
        # Cone1
        con1 = [(0, 2, 0), (-0.87, 0, -0), (0.87, 0, 0), ]
        con1 += [(0, 2, 0), (0, 0, 1), (-0.87, 0, -0), ]
        con1 += [(0.87, 0, 0), (0, 0, 1), ]
        # Cone2
        con2 = [(-1, 0, -0), (-0, 0, 1), (1, 0, 0), ]
        con2 += [(0, 0, -1), (-1, 0, -0), (0, 2, 0), ]
        con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0), ]
        con2 += [(0, 0, -1), (0, 0, -1), (-1, 0, -0), ]
        con2 += [(-0, 0, 1), (1, 0, 0), (0, 2, 0)]
        # car
        car = [(81, 70, 119), (89, 56, 251), (89, -12, 251), ]
        car += [(89, -12, 117), (89, -12, -117), (89, -12, -229), ]
        car += [(81, 70, -229), (81, 70, -159), (69, 111, -105), ]
        car += [(69, 111, 63), (81, 70, 119), (-81, 70, 119), ]
        car += [(-89, 56, 251), (-89, -12, 251), (-89, -12, 117), ]
        car += [(-89, -12, -117), (-89, -12, -229), (-81, 70, -229), ]
        car += [(-81, 70, -159), (-69, 111, -105), (69, 111, -105), ]
        car += [(81, 70, -159), (-81, 70, -159), (-81, 70, -229), ]
        car += [(81, 70, -229), (89, -12, -229), (-89, -12, -229), ]
        car += [(-89, -12, -117), (-89, -12, 117), (-89, -12, 251), ]
        car += [(89, -12, 251), (89, 56, 251), (-89, 56, 251), ]
        car += [(-81, 70, 119), (-69, 111, 63), (-69, 111, -105), ]
        car += [(69, 111, -105), (69, 111, 63), (-69, 111, 63), ]
        # car2
        car2 = [(165, 0, -195), (0, 0, -276), (-165, 0, -195), ]
        car2 += [(-97, 0, -0), (-165, -0, 195), (-0, -0, 276), ]
        car2 += [(165, -0, 195), (97, -0, 0), (165, 0, -195), ]
        # Car3
        car3 = [(212, 0, -212), (0, 0, -300), (-212, 0, -212), ]
        car3 += [(-300, 0, 0), (-212, 0, 212), (0, 0, 300), ]
        car3 += [(212, 0, 212), (300, 0, 0), (212, 0, -212), ]
        # Arrow1
        ar1 = [(0, 0, 2), (2, 0, 1), (1, 0, 1), ]
        ar1 += [(1, 0, -2), (-1, 0, -2), (-1, 0, 1), ]
        ar1 += [(-2, 0, 1), (0, 0, 2), ]
        # Arrow2
        ar2 = [(0, 1, 4), (4, 1, 2), (2, 1, 2), ]
        ar2 += [(2, 1, -4), (-2, 1, -4), (-2, 1, 2), ]
        ar2 += [(-4, 1, 2), (0, 1, 4), (0, -1, 4), ]
        ar2 += [(4, -1, 2), (2, -1, 2), (2, -1, -4), ]
        ar2 += [(-2, -1, -4), (-2, -1, 2), (-4, -1, 2), ]
        ar2 += [(0, -1, 4), (4, -1, 2), (4, 1, 2), ]
        ar2 += [(2, 1, 2), (2, 1, -4), (2, -1, -4), ]
        ar2 += [(-2, -1, -4), (-2, 1, -4), (-2, 1, 2), ]
        ar2 += [(-4, 1, 2), (-4, -1, 2), ]
        # Arrow3
        ar3 = [(7, 0, 0), (5, 0, -5), (0, 0, -7), ]
        ar3 += [(-5, 0, -5), (-7, 0, 0), (-5, 0, 5), ]
        ar3 += [(0, 0, 7), (5, 0, 5), (7, 0, 0), ]
        ar3 += [(5, 0, 2), (7, 0, 3), (7, 0, 0), ]
        # Arrow4
        ar4 = [(0, 0, -11), (-3, 0, -8), (-2.0, 0, -8), ]
        ar4 += [(-2, 0, -6), (-5, 0, -5), (-6, 0, -2), ]
        ar4 += [(-8, 0, -2), (-8, 0, -3), (-11, 0, 0), ]
        ar4 += [(-8, 0, 3), (-8, 0, 2), (-6, 0, 2), ]
        ar4 += [(-5, 0, 5), (-2, 0, 6), (-2, 0, 8), ]
        ar4 += [(-3, 0, 8), (0, 0, 11), (3, 0, 8), ]
        ar4 += [(2, 0, 8), (2, 0, 6), (5, 0, 5), ]
        ar4 += [(6, 0, 2), (8, 0, 2), (8, 0, 3), ]
        ar4 += [(11, 0, 0), (8, 0, -3), (8, 0, -2), ]
        ar4 += [(6, 0, -2), (5, 0, -5), (2, 0, -6), ]
        ar4 += [(2, 0, -8), (3, 0, -8), (0, 0, -11), ]
        # Arrow5
        ar5 = [(-2, 0, -1), (2, 0, -1), (2, 0, -2), ]
        ar5 += [(4, 0, 0), (2, 0, 2), (2, 0, 1), ]
        ar5 += [(-2, 0, 1), (-2, 0, 2), (-4, 0, 0), ]
        ar5 += [(-2, 0, -2), (-2, 0, -1), ]
        # Arrow6
        ar6 = [(-6.3, 6, 0), (-6.5, 4, 0), (-5, 5, 0)]
        ar6 += [(-6.3, 6, 0), (-6, 5, 0), (-5, 3, 0)]
        ar6 += [(-3, 1, 0), (0, 0, 0), (3, 1, 0)]
        ar6 += [(5, 3, 0), (6, 5, 0), (6.3, 6, 0)]
        ar6 += [(5, 5, 0), (6.5, 4, 0), (6.3, 6, 0), ]
        # Pointer
        pointer = [(-1, 0, 0), (-0.7, 0, 0.7), (0, 0, 1), ]
        pointer += [(0.7, 0, 0.7), (1, 0, 0), (0.7, 0, -0.7), ]
        pointer += [(0, 0, -1), (-0.7, 0, -0.7), (-1, 0, 0), ]
        pointer += [(0, 0, 0), (0, 2, 0), ]
        # Foot
        foot = [(-4, 0, -4), (-4, 0, -7), (-3, 0, -11), ]
        foot += [(-1, 0, -12), (0, 0, -12), (1, 0, -12), ]
        foot += [(3, 0, -11), (4, 0, -7), (4, 0, -4), ]
        foot += [(-4, 0, -4), (-5, 0, 1), (-5, 0, 6), ]
        foot += [(-4, 0, 12), (-2, 0, 15), (0, 0, 15.5), ]
        foot += [(2, 0, 15), (4, 0, 12), (5, 0, 6), ]
        foot += [(5, 0, 1), (4, 0, -4), (-4, 0, -4), ]
        foot += [(4, 0, -4), ]
        # foot2
        foot2 = [(-6, 12, -14), (-6, 12, 6), (6, 12, 6), ]
        foot2 += [(6, 12, -14), (-6, 12, -14), (-6, 0, -14), ]
        foot2 += [(-6, 0, 18), (6, 0, 18), (6, 0, -14), ]
        foot2 += [(-6, 0, -14), (-6, 0, 18), (-6, 12, 6), ]
        foot2 += [(6, 12, 6), (6, 0, 18), (6, 0, -14), (6, 12, -14), ]
        # Hoof
        hoof = [(-6, 0, -5), (-6.5, 0, -1), (-6, 0, 3), ]
        hoof += [(-5.2, 0, 5.5), (-3, 0, 7.5), (0, 0, 8.2), ]
        hoof += [(3, 0, 7.5), (5.2, 0, 5.5), (6, 0, 3), ]
        hoof += [(6.5, 0, -1), (6, 0, -5), (4, 0, -5), ]
        hoof += [(4.5, 0, -1), (4, 0, 3), (3.5, 0, 4.5), ]
        hoof += [(2, 0, 6), (0, 0, 6.5), (-2, 0, 6), ]
        hoof += [(-3.5, 0, 4.5), (-4, 0, 3), (-4.5, 0, -1), ]
        hoof += [(-4, 0, -5), (-6, 0, -5), (-5.5, 0, -6.5), ]
        hoof += [(5.5, 0, -6.5), (4.5, 0, -10), (2.2, 0, -12.2), ]
        hoof += [(0, 0, -12.2), (-2.2, 0, -12.2), (-4.5, 0, -10), ]
        hoof += [(-5.5, 0, -6.5), ]
        # Hoof2
        hoof2 = [(6, 6, -12), (0, 8, -12), (-6, 6, -12), ]
        hoof2 += [(-8, 3, -13), (-8, 0, -12), (-7, 0, -10), ]
        hoof2 += [(-8, 0, -6), (-9, 0, -1), (-8, 0, 4), ]
        hoof2 += [(-5, 0, 9), (0, 0, 10), (5, 0, 9), ]
        hoof2 += [(8, 0, 4), (9, 0, -1), (8, 0, -6), ]
        hoof2 += [(7, 0, -10), (8, 0, -12), (8, 3, -13), ]
        hoof2 += [(6, 6, -12), ]
        # Square
        sqr = [(1, 0, 1), (1, 0, -1), (-1, 0, -1), ]
        sqr += [(-1, 0, 1), (1, 0, 1)]
        # Cross
        cross = [(0, 5, 1), (0, 5, -1), (0, 1, -1), ]
        cross += [(0, 1, -5), (0, -1, -5), (0, -1, -1), ]
        cross += [(0, -5, -1), (0, -5, 1), (0, -1, 1), ]
        cross += [(0, -1, 5), (0, 1, 5), (0, 1, 1), ]
        cross += [(0, 5, 1), ]
        # hat
        hat = [(14, 9, 0), (0, 15, 0), (-14, 9, 0), ]
        hat += [(-7, -5, 0), (-29, -7, 0), (0, -7, 0), ]
        hat += [(29, -7, 0), (7, -5, 0), (14, 9, 0), ]
        # head
        head = [(13, 15, -11), (0, 25, -15), (-13, 15, -11), ]
        head += [(-14, 6, 0), (-13, 15, 11), (0, 25, 15), ]
        head += [(13, 15, 11), (14, 6, 0), (13, 15, -11), ]
        # scapula
        scapula = [(2, 10, -11), (0, 0, -11), (-2, 10, -11), ]
        scapula += [(-3, 18, 0), (-2, 10, 11), (0, 0, 11), ]
        scapula += [(2, 10, 11), (3, 18, 0), (2, 10, -11), ]
        # Dictionary
        ctrl = {
            "cub": cub, 
            "sph": sph, 
            "cyl": cyl, 
            "pip": pip, 
            "con1": con1, 
            "con2": con2, 
            "car": car, 
            "car2": car2, 
            "car3": car3, 
            "ar1": ar1, 
            "ar2": ar2, 
            "ar3": ar3, 
            "ar4": ar4, 
            "ar5": ar5, 
            "ar6": ar6, 
            "pointer": pointer, 
            "foot": foot, 
            "foot2": foot2, 
            "hoof": hoof, 
            "hoof2": hoof2, 
            "sqr": sqr, 
            "cross": cross, 
            "hat": hat, 
            "head": head, 
            "scapula": scapula, 
        }
        inputs = {}
        for tmp in args:
            for key, val in tmp.items():
                if isinstance(val, dict):
                    print("Dict in dict.")
                else:
                    inputs[key] = val
        for key, val in kwargs.items():
            inputs[key] = val
        # If there is no inputs...
        if not inputs:
            tmp = input()
            coordinate = []
            try:
                for i in tmp.split(","):
                    key, val = i.strip().split("=")
                    if val == "True":
                        coordinate.append(ctrl[key])
                    else:
                        continue
            except:
                print("Syntax is incorrect.")
        else:
            coordinate = [ctrl[i] for i in inputs if inputs[i]]
        result = [pm.curve(d=1, p=i) for i in coordinate]
        return result


    def getPositions(self, selections: list) -> list:
        positions = []
        for i in selections:
            try:
                position = self.getPositionVertex(i)
            except:
                position = self.getPositionObject(i)
            positions.append(position)
        return positions


    def matchDotsToPositions(self, curveName, positions: list):
        for idx, xyz in enumerate(positions):
            try:
                pm.move("%s.cv[%d]"%(curveName, idx), xyz, ws=True)
            except Exception as e:
                print(e)


class CreateCurvePassingThrough:
    def __init__(self, startFrame, endFrame):
        self.selections = pm.ls(sl=True, fl=True)
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.main()


    def main(self):
        """ The selection should be PyNode. """
        # startFrame, endFrame = duration
        positions = []
        for i in self.selections:
            self.getPositionPerFrame()
            positions.append(xyz)
        return positions
        # duration = (startFrame, endFrame)
        # result = []
        # for i in selections:
        #     positions = self.getPositionPerFrame(i, duration)
        #     curveName = pm.curve(p=positions, d=3)
        #     result.append(curveName)
        # return result

    def doSomethingPerFrame(self, startFrame, endFrame):
        for frame in range(startFrame, endFrame + 1):
            pm.currentTime(frame)
            pass

    def getPositions(self, selection: str) -> list:
        positions = []
        try:
            xyz = pm.pointPosition(selection, w=True)
        except:
            xyz = pm.xform(selection, q=1, ws=1, rp=1)
        positions.append(xyz)
        return positions






    def getPositionPerFrame(self, selection, duration) -> list:


    def isVertex(self, selection: str) -> bool:
        if isinstance(selection, pm.MeshVertex):
            return True
        else:
            return False


    def isObject(self, selection: str) -> bool:
        if isinstance(selection, pm.nodetypes.Transform):
            return True
        else:
            return False


    def getPositionVertex(self, vertex) -> list:
        position = 
        return position


    def getPositionObject(self, object) -> list:
        position = 
        return position

