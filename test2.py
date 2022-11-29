import os
import pymel.core as pm


# Get a human dummy to determine size.
class Human:
    def __init__(self):
        '''When to start modeling in Maya, 
        Load a human character into the scene 
        to compare the size of the modeling to be made.
        1. human()
        2. human().remove()
        '''
        # src is the path for human modeling.
        src = "T:/AssetTeam/Share/WorkSource/human/human176.obj"
        assert os.path.isfile(src)
        self.src = src
        self.main()


    # Maya default settings when fetching references.
    def createReference(self) -> None:
        fileName = os.path.basename(self.src)
        name, ext = os.path.splitext(fileName)
        pm.createReference(
            self.src, # full path
            gl=True, # groupLocator
            shd="shadingNetworks", # sharedNodes
            mnc=False, # mergeNamespacesOnClash
            ns=name # namespace
        )


    # Remove human character
    def remove(self) -> None:
        pm.FileReference(self.src).remove()


    # Check the reference with the same path as "src" in the scene.
    def main(self) -> None:
        ref = pm.ls(rn = True, type=["transform"])
        tmp = [i for i in ref if self.src == pm.referenceQuery(i, f=True)]
        # If the same file does not exist, the human character is loaded.
        if not tmp:
            self.createReference()


