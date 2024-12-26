import re
import pymel.core as pm


def getNumberIndex(name: str) -> dict:
    """ If the name contains a number, 
    it returns a dict with the number and index.

    Examples: 
    >>> getNumberIndex("vhcl_car123_rig_v0123")
    # ['vhcl_car', '123', '_rig_v', '0123']
    >>> {0: 'vhcl_car', 1: '123', 2: '_rig_v', 3: '0123'}
     """
    nameSlices = re.split(r'(\d+)', name)
    nameSlices = [i for i in nameSlices if i]
    result = {i: slice for i, slice in enumerate(nameSlices)}
    return result


def reName(*args):
    numberOfArgs = len(args)
    result = []
    if numberOfArgs == 0:
        return
    elif numberOfArgs == 1:
        newName = args[0]
        nameSlices = re.split(r'(\d+)', newName)
        nameSlices = [i for i in nameSlices if i]
        numberInfo = {j: k for j, k in enumerate(nameSlices) if k.isdigit()}
        if numberInfo:
            sel = pm.selected(fl=True)
            idx = max(numberInfo)
            nDigit = len(numberInfo[idx])
            number = int(numberInfo[idx])
            for i, obj in enumerate(sel):
                increasedNumber = f"%0{nDigit}d" % (number + i)
                nameSlices[idx] = increasedNumber
                finalName = ''.join(nameSlices)
                if pm.objExists(finalName):
                    pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                    continue
                else:
                    pm.rename(obj, finalName)
                    result.append(finalName)
        else:
            sel = pm.selected(fl=True)
            for i, obj in enumerate(sel):
                finalName = ''.join(nameSlices) + str(i)
                if pm.objExists(finalName):
                    pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                    continue
                else:
                    pm.rename(obj, finalName)
                    result.append(finalName)
    elif numberOfArgs == 2:
        originalWord, wordToChange = args
        sel = pm.selected(fl=True)
        for i in sel:
            obj = i.name()
            finalName = obj.replace(originalWord, wordToChange)
            if pm.objExists(finalName):
                pm.warning(f"['{obj}' -> '{finalName}'] aleady exists.")
                continue
            else:
                pm.rename(obj, finalName)
                result.append(finalName)
    else:
        return
    return result

