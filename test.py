import pymel.core as pm
import re
import os
import hjk


def pubRigFile():
    # tmp = pm.Env().sceneName()
    fullPath = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes/vhcl_micaA_rig_v0043.ma"
    folder = os.path.dirname(fullPath)
    scenes = os.path.basename(fullPath)
    name, ext = os.path.splitext(scenes)
    print(folder)
    print(scenes)
    print(name, ext)
    dirSplit = folder.split("/")
    if "dev" in dirSplit:
        DevPub = "dev"
    elif "pub" in dirSplit:
        DevPub = "pub"
    else:
        DevPub = ""
    print(DevPub)
    tmp = re.compile(".*[_v](\d{4})")
    print(tmp.match(fullPath).group(1))
    


pubRigFile()