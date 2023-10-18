import pymel.core as pm


class CreateCurves:
    def __init__(self):
        pass


    def createCurvePassingThrough(self, startFrame: int, endFrame: int):
        """ The selection should be PyNode. """
        selections = pm.ls(sl=True, fl=True)
        duration = (startFrame, endFrame)
        result = []
        for i in selections:
            positions = self.getPositionPerFrame(i, duration)
            curveName = pm.curve(p=positions, d=3)
            result.append(curveName)
        return result


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


    def getPositionPerFrame(self, selection, duration: tuple):
        startFrame, endFrame = duration
        positions = []
        for i in range(startFrame, endFrame + 1):
            pm.currentTime(i)
            if self.isVertex(selection):
                points = self.getPositionVertex(selection)
            elif self.isObject(selection):
                points = self.getPositionObject(selection)
            else:
                break
            positions.append(points)
        return positions


    def matchDotsToPositions(self, curveName: str, positions: list):
        for idx, xyz in enumerate(positions):
            try:
                pm.move("%s.cv[%d]" % (curveName, idx), xyz, ws=True)
            except:
                return


    def isVertex(self, selection: str):
        if isinstance(selection, pm.MeshVertex):
            return True
        else:
            return False


    def isObject(self, selection: str):
        if isinstance(selection, pm.nodetypes.Transform):
            return True
        else:
            return False


    def getPositionVertex(self, vertex):
        position = pm.pointPosition(vertex)
        return position


    def getPositionObject(self, object):
        position = pm.xform(object, q=1, ws=1, rp=1)
        return position


