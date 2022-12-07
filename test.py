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
            jsonFile = dir + "/" + name + ".json"
            chk = os.path.isfile(jsonFile)
            if chk:
                with open(jsonFile) as JSON:
                    data = json.load(JSON)
            else:
                data = {}
            result = original_func(data, *args, **kwargs)
            with open(jsonFile, 'w') as JSON:
                json.dump(data, JSON, indent=4)
            return result
    return wrapper


@rwJSON
def writeJSON(data):
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


writeJSON()
# loadJson()