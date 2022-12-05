import pymel.core as pm
import json




def writeJSON():
    with open(r'C:\Users\jkhong\Desktop\cherokeeJeep.json') as JSON:
        data = json.load(JSON)
    # data = {}
    sel = pm.ls(sl=True)
    for j, k in enumerate(sel):
        if j % 2:
            continue
        else:
            data[k.name()] = sel[j+1].name()
    with open(r'C:\Users\jkhong\Desktop\cherokeeJeep.json', 'w') as JSON:
        json.dump(data, JSON, indent=4)
    print(data)


# writeJSON()


def constraintFromJSON():
    with open(r'C:\Users\jkhong\Desktop\cherokeeJeep.json') as JSON:
        data = json.load(JSON)
    for j, k in data.items():
        pm.parentConstraint(j, k, mo=True, w=1)
        pm.scaleConstraint(j, k, mo=True, w=1)


constraintFromJSON()