import pathlib
import re
import pymel.core as pm
import hjk


class PubRig:
    def __init__(self):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("Scene was not saved.")
            return
        self.PATH = pathlib.Path(fullPath)
        


    dev = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes"
    dev = pathlib.Path(dev)
    pub = "T:/SOB/assets/vhcl/micaA/rig/pub/scenes"
    pub = pathlib.Path(pub)
    fileList = [i for i in dev.iterdir() if i.is_file()]
    folderList = [i for i in pub.iterdir() if i.is_dir()]

    # fullPath = "T:/SOB/assets/vhcl/micaA/rig/pub/scenes/v0043/vhcl_micaA_rig_v0043.ma"
    fullPath = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes/vhcl_micaA_rig_v0043.ma"
    # fullPath = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes"


    def makeSceneName(fullPath):
        pattern1 = re.compile(r"/(rig)/")
        pattern2 = re.compile(r"/(dev|pub)/")
        pattern3 = re.compile(r".*v(\d{4})")

        worker = pattern1.search(fullPath)
        folder = pattern2.search(fullPath)
        ver = pattern3.search(fullPath)

        if not (worker and folder):
            pass
        else:
            worker = worker.group(1)
            folder = folder.group(1)
            print(worker, folder)

        # if VER == '9999':
        #     dev = ''
        #     pub = ''
        #     v9999 = curr
        # else:
        #     if DP == "dev":
        #         dev = ''
        #         pub = ''
        #         v9999 = ''
        #     else:
        #         dev = ''
        #         pub = ''
        #         v9999 = ''
        # revDP = "pub" if DP == "dev" else "dev"
        # numUp = int(VER) + 1
        # numUp = "v" + str(numUp)
    

tmp = PubRig()
print(tmp)