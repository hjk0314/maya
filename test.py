import re
import os
import json
import pymel.core as pm


def rwJSON(original_func):
    def wrapper(*args, **kwargs):
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("File not saved.")
        else:
            dir = os.path.dirname(fullPath)
            name_Ext = os.path.basename(fullPath)
            name, ext = os.path.splitext(name_Ext)
            jsonAll = [i for i in os.listdir(dir) if i.endswith('.json')]
            verDict = {}
            for i in jsonAll:
                tmp = re.search('(.*)[_v]([0-9]{4})[.].*', i)
                num = int(tmp.group(2))
                verDict[num] = tmp.group(1)
            verMax = max(verDict.keys())
            print(verMax)
            if not verMax:
                jsonFile = dir + "/" + name + ".json"
                data = {}
            else:
                jsonFile = f"{dir}/{verDict[verMax]}v%04d.json" % verMax
                with open(jsonFile) as JSON:
                    data = json.load(JSON)
            print(jsonFile)
            result = original_func(data, *args, **kwargs)
            print(data)
            with open(dir + "/" + name + ".json", 'w') as JSON:
                json.dump(data, JSON, indent=4)
            return result
    return wrapper


@rwJSON
def writeJSON(data):
    print(data)
    sel = pm.ls(sl=True)
    if not sel:
        print("Nothing selected.")
    else:
        for j, k in enumerate(sel):
            if j % 2:
                continue
            else:
                obj = sel[j+1].name()
                cc = k.name()
                pm.parentConstraint(cc, obj, mo=True, w=1)
                pm.scaleConstraint(cc, obj, mo=True, w=1)
                data[obj] = cc


@rwJSON
def loadJson(data):
    for obj, cc in data.items():
        pm.parentConstraint(cc, obj, mo=True, w=1)
        pm.scaleConstraint(cc, obj, mo=True, w=1)


# writeJSON()
# loadJson()


