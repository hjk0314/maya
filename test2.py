import os
import datetime
import pymel.core as pm


# Create reference and their handle.
def createRef():
    src = r"C:\Users\jkhong\Desktop\a.abc"
    fileName = os.path.basename(src)
    name, ext = os.path.splitext(fileName)
    resolvedName = pm.createReference(
        src, # full path
        gl=True, # groupLocator
        shd="shadingNetworks", # sharedNodes
        mnc=False, # mergeNamespacesOnClash
        ns=name # namespace
    )
    refName = pm.referenceQuery(resolvedName, rfn=True) # reference name
    refNS = pm.referenceQuery(resolvedName, ns=True) # namespace
    return refName, refNS


a = datetime.datetime.today()
print(a)
