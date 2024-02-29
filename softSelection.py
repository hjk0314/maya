import pymel.core as pm
import maya.OpenMaya as om


class SoftSelection:
    def __init__(self):
        """ Applies cluster to the soft selection area. """
        pass
    

    def createCluster(self):
        softElementData = self.softSelectionsArea()
        selection = ["%s.vtx[%d]" % (el[0], el[1]) for el in softElementData] 
        pm.select(selection, r=True)
        cluster = pm.cluster(relative=True)
        for i in range(len(softElementData)):
            pm.percent(cluster[0], selection[i], v=softElementData[i][2])
        pm.select(cluster[1], r=True)

    
    def softSelectionsArea(self):
        selection = om.MSelectionList()
        softSelection = om.MRichSelection()
        om.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)
        dagPath = om.MDagPath()
        component = om.MObject()
        iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        elements = []
        while not iter.isDone(): 
            iter.getDagPath(dagPath, component)
            dagPath.pop()
            node = dagPath.fullPathName()
            fnComp = om.MFnSingleIndexedComponent(component)   
            for i in range(fnComp.elementCount()):
                elem = fnComp.element(i)
                infl = fnComp.weight(i).influence()
                elements.append([node, elem, infl])
            iter.next()
        return elements

