import maya.OpenMaya as om
import pymel.core as pm


# Find a name that breaks the rules.
class badName():
    def __init__(self):
        self.allowedUpper = ['L', 'R', 'T', 'GRP', 'PROXY', 'MODEL']
        self.allowedTitle = ['Bt', 'Ft', 'Bk', 'Top']
        self.notGoodLower = ['l', 'r', 't', 'lt', 'lf', 'rt', 'bt', 'ft', 'bk', 'ct', 'top']
        self.nameMain()


    # Checking and append to bad name list.
    def nameMain(self):
        all = pm.ls(tr=True)
        cam = [i.getParent().name() for i in pm.ls(dag=True, type=['camera'])]
        sel = [i for i in all if not i in cam]
        badName = []
        for i in sel:
            if not self.nameCheck(i):
                badName.append(i)
                continue
            else:
                nameList = i.split("_")
                for word in nameList:
                    if not self.wordCheck(word):
                        badName.append(i)
                        continue
                    else:
                        pass
        if badName:
            pm.select(badName)
            om.MGlobal.displayError("Rule breaker selected in outliner.")
        else:
            om.MGlobal.displayInfo("No bad names.")


    # Checking 4 types : 'abc', 'ABC', 'Abc', 'aBc'
    def wordCheck(self, word):
        if word.islower():
            result = not word in self.notGoodLower
        elif word.isupper():
            result = word in self.allowedUpper
        elif word.istitle():
            result = word in self.allowedTitle
        else:
            result = not word[0].isupper()
        return result


    # Check First, namespace and verticalBar and double underScore.
    def nameCheck(self, name):
        # namespace
        if ":" in name:
            colonList = [i for i in name.split(":") if not self.nameCheck(i)]
            result = False if colonList else name
        # vertical bar
        elif "|" in name:
            result = False
        # double under score
        elif "" in name.split("_"):
            result = False
        else:
            result = name
        return result


# Select objects with duplicate names.
def sameName():
    sel = pm.ls(tr=True)
    dup = [i for i in sel if "|" in i]
    if dup:
        pm.select(dup)
        om.MGlobal.displayError("Same name selected in outliner.")
    else:
        om.MGlobal.displayInfo("No same names.")

