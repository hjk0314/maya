import pymel.core as pm
import pathlib
import datetime
import re
import os
import hjk


class PubRigFiles:
    def __init__(self):
        # fullPath = pm.Env().sceneName()
        self.fullPath = "T:/SOB/assets/vhcl/micaA/rig/dev/scenes/vhcl_micaA_rig_v0043.ma"
        # "T:/SOB/assets/vhcl/micaA/rig/pub/scenes/v0043/vhcl_micaA_rig_v0043.ma"
        self.data = [] # The function of main() is to create this data.
        if not self.fullPath:
            print("File was not saved.")
        else:
            self.main()


    def main(self):
        self.data = self.parsing(self.fullPath)
        self.makeSceneName()
    

    def makeSceneName(self):
        curr = self.fullPath
        DP, VER = self.data[3:5]
        if VER == '9999':
            dev = ''
            pub = ''
            v9999 = curr
        else:
            if DP == "dev":
                dev = ''
                pub = ''
                v9999 = ''
            else:
                dev = ''
                pub = ''
                v9999 = ''
        revDP = "pub" if DP == "dev" else "dev"
        numUp = int(VER) + 1
        numUp = "v" + str(numUp)
        curr.replace(f"{DP}/scenes", f"{revDP}/scenes/{numUp}")


    def getMaxVersion(self, directory):
        pass


    def makeFolder(self):
        pass


    def parsing(self, fullPath):
        """ Split into 7 strings and make a list.
        Sample fullPath is shown below.
            "T:/SOB/assets/vhcl/micaA/rig/dev/scenes/vhcl_micaA_rig_v0043.ma"
        This is parsed as below.
            ['SOB', 'assets', 'rig', 'dev', '0043', '.ma', '2023-04-05 15:40:30']
         """
        # 7 Elements
        PROJ = ["KNP", "MAG", "SRT", "SOB", "HRB"]
        AS = ["assets", "seq"]
        TEAM = ["mdl", "ldv", "rig", "ani", "lgt", "fx"]
        DP = ["dev", "pub"]
        VER = []
        EXT = []
        TIME = []
        # Make variables.
        folder = os.path.dirname(fullPath)
        scenes = os.path.basename(fullPath)
        name, ext = os.path.splitext(scenes)
        dir = folder.split("/")
        ver = re.compile(".*[_v](\d{4})")
        ver = ver.match(name).group(1)
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        # Make a list.
        VER.append(ver)
        EXT.append(ext)
        TIME.append(now)
        # Result
        result = list(set(PROJ) & set(dir))
        result += list(set(AS) & set(dir))
        result += list(set(TEAM) & set(dir))
        result += list(set(DP) & set(dir))
        result += VER
        result += EXT
        result += TIME
        # Check if the number is 7.
        if len(result) != 7:
            print("The number of elements must be 7.")
            return []
        else:
            return result


PubRigFiles()