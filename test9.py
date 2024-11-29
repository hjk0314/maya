import pymel.core as pm
import os


class CreateProxyFile:
    def __init__(self):
        pass


    def main(self):
        self.replaceReference()
        fosterNode = pm.ls("*fosterParent*", type="transform")
        for i in fosterNode:
            for j in i.listRelatives(c=True):
                self.reConnect(j)
        self.cleanUp()


    def reConnect(self, originalConstraintNode: str) -> str:
        if not pm.nodeType(originalConstraintNode).endswith("Constraint"):
            return
        nameSlice = originalConstraintNode.rsplit('_', 1)
        originalSource = nameSlice[0]
        constraintType = nameSlice[-1]
        source = self.createSourceName(originalConstraintNode)[0]
        target = self.createTargetName(originalSource)
        if "parent" in constraintType:
            result = pm.parentConstraint(source, target, mo=True, w=1.0)
        elif "scale" in constraintType:
            result = pm.scaleConstraint(source, target, mo=True, w=1.0)
        elif "orient" in constraintType:
            result = pm.orientConstraint(source, target, mo=True, w=1.0)
        elif "point" in constraintType:
            result = pm.pointConstraint(source, target, mo=True, w=1.0)
        else:
            result = ""
        return result


    def createSourceName(self, constraintNode: str) -> tuple:
        """ Returns source and target object 
        connected with the constraint node.

        Examples:
        >>> createSourceName("brisaB_scaleConstraint1")
        >>> ("cc_sub", "vhcl_brisaB_mdl_v9999RN")
        """
        # Reference Namespace -> ex) vhcl_brisaB_mdl_v9999RN
        target = pm.listConnections(\
            f"{constraintNode}.constraintParentInverseMatrix", s=1, d=0)[0]
        # Beginning of a connection -> ex) jnt_body, cc_sub ...
        source = pm.listConnections(\
            f"{constraintNode}.target[0].targetParentMatrix", s=1, d=0)[0]
        return source, target


    def createTargetName(self, sourceName: str) -> str:
        """ Creates a name for a new target to be connected. """
        ref = pm.listReferences()[0]
        refNS = ref.namespace
        addProxy = f"{sourceName}_proxy"
        finalName = f"{refNS}:{addProxy}"
        return finalName


    def replaceReference(self):
        rigFile = pm.Env().sceneName()
        if not rigFile:
            return
        mdlFile = rigFile.replace("rig", "mdl")
        mdlProxyFile = mdlFile.replace("_mdl_v9999", "_mdl_proxy_v9999")
        mdlProxyFileName = os.path.basename(mdlProxyFile)
        ref = pm.listReferences()
        for i in ref:
            if mdlFile == i and os.path.exists(mdlProxyFile):
                i.replaceWith(mdlProxyFile)
                i.namespace = os.path.splitext(mdlProxyFileName)[0]
            else:
                continue
            pm.parent(i.nodes()[0], "MODEL")


    def cleanUp(self):
        rigFile = pm.Env().sceneName()
        if not rigFile:
            return
        # Add the suffix "_proxy" to the group name
        rigFileName = os.path.basename(rigFile)
        objName = rigFileName.split("_")[1]
        if pm.objExists(objName):
            pm.rename(objName, f"{objName}_proxy")
        # Save as
        try:
            saveAsName = rigFile.replace("_rig_v9999", "_rig_proxy_v9999")
            pm.system.saveAs(saveAsName, force=True)
        except:
            pm.warning("The File was not saved.")



cpf = CreateProxyFile()
print(dir(cpf))
# cpf.replaceReference()
