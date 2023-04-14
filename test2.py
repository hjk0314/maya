import pathlib
import re
import pymel.core as pm


def getMaxVersion(fullPath: list) -> int:
    tmp = re.compile(".*v(\d{4})") # v0001 ~ v9999
    numList = []
    for i in fullPath:
        ver = tmp.match(i.name)
        if not ver:
            continue
        num = ver.group(1)
        num = int(num)
        if num == 9999:
            continue
        numList.append(num)
    try:
        result = max(numList)
    except:
        result = 0
    return result


dev = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes"
dev = pathlib.Path(dev)
pub = "T:/SOB/assets/vhcl/micaA/rig/pub/scenes"
pub = pathlib.Path(pub)
fileList = [i for i in dev.iterdir() if i.is_file()]
folderList = [i for i in pub.iterdir() if i.is_dir()]

fullPath = "T:/SOB/assets/vhcl/micaA/rig/pub/scenes/v0043/vhcl_micaA_rig_v0043.ma"



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
    