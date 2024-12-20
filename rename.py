import re
import pymel.core as pm


class Rename:
    def __init__(self):
        """ 
        reName("nameToCreate_001")
        >>> "nameToCreate_001"
        >>> "nameToCreate_002"
        >>> "nameToCreate_003"

        reName("Apple", "Banana")
        >>> "Apple_01" -> "Banana_01"
         """
        pass


    def reName(self, *arg: str):
        """ If there
        - is one argument, create a new name, 
        - are two arguments, replace a specific word.

        reName("nameToCreate_001")
        >>> "nameToCreate_001"
        >>> "nameToCreate_002"
        >>> "nameToCreate_003"

        reName("Apple", "Banana")
        >>> "Apple_01" -> "Banana_01"
         """
        numberOfArguments = len(arg)
        if numberOfArguments == 1:
            nameToCreate = arg[0]
            self.createNewName(nameToCreate)
        elif numberOfArguments == 2:
            originalWord = arg[0]
            wordToChange = arg[1]
            self.changeWords(originalWord, wordToChange)
        else:
            pass


    def createNewName(self, nameToCreate):
        nameSlices = self.splitNumbers(nameToCreate)
        numberDict = self.numbersInfo(nameSlices)
        if numberDict:
            result = self.nameDigitly(nameSlices, numberDict)
        else:
            result = self.nameSimply(nameToCreate)
        self.failureReport(result)


    def changeWords(self, originalWord, wordToChange) -> dict:
        selections = pm.ls(sl=True, fl=True)
        failureDict = {}
        for i in selections:
            selected = i.name()
            nameToChange = selected.replace(originalWord, wordToChange)
            if pm.objExists(nameToChange):
                failureDict[selected] = nameToChange
                continue
            else:
                pm.rename(selected, nameToChange)
        return failureDict


    def splitNumbers(self, fullName: str) -> list:
        """ inputName -> "vhcl_car123_rig_v0123"
        >>> ['vhcl_car', '123', '_rig_v', '0123']
        """
        nameSlices = re.split(r'(\d+)', fullName)
        result = [i for i in nameSlices if i]
        return result


    def numbersInfo(self, nameSlices: list) -> dict:
        """ Create and return the numbers in a name as a dict.
        - inputName -> "vhcl_car123_rig_v0123"
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
        - result -> {1: '123', 3: '0123'}
         """
        result = {}
        for i, slice in enumerate(nameSlices):
            if slice.isdigit():
                # 'slice' must be a string to know the number of digits.
                result[i] = slice
            else:
                continue
        return result


    def nameDigitly(self, nameSlices: list, numbersInfo: dict) -> dict:
        """ Name by increasing number.
        - originalName -> "vhcl_car123_rig_v0123".
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
        - numbersInfo -> {1: '123', 3: '0123'}

        Select 3 objects and name them. Return below.
        >>> "vhcl_car123_rig_v0123"
        >>> "vhcl_car123_rig_v0124"
        >>> "vhcl_car123_rig_v0125"
        """
        selections = pm.ls(sl=True, fl=True)
        idx = max(numbersInfo)
        nDigit = len(numbersInfo[idx])
        number = int(numbersInfo[idx])
        failureDict = {}
        for i, obj in enumerate(selections):
            increasedNumber = f"%0{nDigit}d" % (number + i)
            nameSlices[idx] = increasedNumber
            result = ''.join(nameSlices)
            if pm.objExists(result):
                failureDict[obj] = result
                continue
            else:
                pm.rename(obj, result)
        return failureDict


    def nameSimply(self, nameSlices: list) -> dict:
        """ Name Simply. And returns a Dict of failures.
        - originalName -> "vhcl_car123_rig_v0123"
        - nameSlices -> ['vhcl_car', '123', '_rig_v', '0123']
         """
        selections = pm.ls(sl=True, fl=True)
        failureDict = {}
        for i, obj in enumerate(selections):
            result = ''.join(nameSlices) + str(i)
            if pm.objExists(result):
                failureDict[obj] = result
                continue
            else:
                pm.rename(obj, result)
        return failureDict


    def failureReport(self, failureDict: dict):
        if failureDict:
            warningMessages = "\n"
            for objName, nameToChange in failureDict.items():
                warningMessages += f"{objName} -> {nameToChange} failed. \n"
            pm.warning(warningMessages)
        else:
            warningMessages = "Rename all success."
            print(warningMessages)



rn = Rename()
rn.changeWords("joint", "fbx")