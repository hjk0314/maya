
import re
import pymel.core as pm
import maya.OpenMaya as om


class AutoRig_Wheel:
    def __init__(self, arg=None):
        """ Automatically creates rigging 
        to turn your selection into wheels. Or, 
        insert the controller's list as a parameter.
        Constraint the wheel to the locator, 
        The movement of the wheel is connected to the offset group.
         """
        self.sel = self.checkParam(arg)
        self.main()


    def main(self):
        """ 1. First, create a controller.
        2. Create a parent group for the controller.
        3. Create a locator under the controller.
        4. Name several groups.
        5. Create the Radius and AutoRoll channels of the controller.
        6. Setting relationships with groups.
        7. Finally, create an expression.
         """
        for obj in self.sel:
            ctrl = self.createWheelCtrl(obj)
            off = self.createOffsetGrp(ctrl)
            loc = self.createCtrlLocator(ctrl)
            null, prev, orient = self.createGroupNames(off)
            self.createCtrlChannel(ctrl)
            self.createOffsetChannel(off)
            self.createCtrlGroup(off, null, prev, orient)
            self.createExpression(ctrl, off, loc, orient, prev)


    def checkParam(self, obj):
        """ Checks if there is an argument 
        and creates the argument as PyNode.
         """
        if obj and isinstance(obj, list):
            for j, k in enumerate(obj):
                if isinstance(k, pm.PyNode):
                    continue
                else:
                    obj[j] = pm.PyNode(k)
            result = obj
        else:
            result = pm.ls(sl=True)
        return result


    def createWheelCtrl(self, obj, sizeUp=1.2):
        """ Create a controller 1.2 times larger than 
        the boundingBox size of the selected object.
         """
        bb = pm.xform(obj, q=True, bb=True, ws=True)
        xMin, yMin, zMin, xMax, yMax, zMax = bb
        x = (xMax - xMin) / 2
        y = (yMax - yMin) / 2
        z = (zMax - zMin) / 2
        rad = max(x, y, z)
        rad = round(rad, 3) * sizeUp
        cuv = pm.circle(nr=(1, 0, 0), r=rad, n=f"cc_{obj}", ch=False)
        cuv = cuv[0]
        pm.matchTransform(cuv, obj, pos=True)
        return cuv


    def createOffsetGrp(self, obj):
        """ Create a parent group for the controller. """
        result = pm.group(obj, n=f"{obj}_offset")
        pm.xform(result, os=True, piv=(0,0,0))
        return result


    def createCtrlLocator(self, ctrl):
        """ Place the locator under the controller. """
        loc = pm.spaceLocator(n='loc_' + ctrl)
        pm.matchTransform(loc, ctrl, pos=True)
        pm.parent(loc, ctrl)
        return loc


    def createGroupNames(self, offset):
        """ Create another group name. """
        null = offset + '_null_grp'
        prev = offset + '_prev_grp'
        orient = offset + '_orient_grp'
        return null, prev, orient


    def createCtrlChannel(self, ctrl):
        """ Creates a Radius channel and AutoRoll channel. """
        attrRad = "Radius"
        pm.addAttr(ctrl, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ctrl}.{attrRad}', e=True, k=True)
        attrAuto = 'AutoRoll'
        pm.addAttr(ctrl, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ctrl}.{attrAuto}', e=True, k=True)


    def createOffsetChannel(self, offset):
        """ Create a PrePos channel in the offset group. """
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PrevPos{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PrevPos{i}', e=True, k=True)


    def createCtrlGroup(self, offset, null, prev, orient):
        """ Determine group relationships. """
        if offset.getParent():
            pm.parent(offset, offset.getParent())
        else:
            tempGrp = pm.group(em=True)
            pm.parent(offset, tempGrp)
        pm.group(n=null, em=True, p=offset)
        pm.group(n=prev, em=True, p=offset.getParent())
        ort = pm.group(n=orient, em=True, p=prev)
        pos = [-0.001, -0.001, -0.001]
        ort.translate.set(pos)
        pm.aimConstraint(offset, prev, mo=False)
        pm.orientConstraint(null, orient, mo=False)


    def createExpression(self, ctrl, offset, loc, orient, prev):
        """ Create an expression. """
        br = '\n'
        # expression1
        expr1 = f'float $R = {ctrl}.Radius;{br}'
        expr1 += f'float $A = {ctrl}.AutoRoll;{br}'
        expr1 += f'float $J = {loc}.rotateX;{br}'
        expr1 += f'float $C = 2 * 3.141 * $R;{br}'
        expr1 += f'float $O = {orient}.rotateY;{br}'
        expr1 += f'float $S = {offset}.scaleY;{br}'
        expr1 += f'float $pX = {offset}.PrevPosX;{br}'
        expr1 += f'float $pY = {offset}.PrevPosY;{br}'
        expr1 += f'float $pZ = {offset}.PrevPosZ;{br}'
        expr1 += f'{prev}.translateX = $pX;{br}'
        expr1 += f'{prev}.translateY = $pY;{br}'
        expr1 += f'{prev}.translateZ = $pZ;{br}'
        expr1 += f'float $nX = {offset}.translateX;{br}'
        expr1 += f'float $nY = {offset}.translateY;{br}'
        expr1 += f'float $nZ = {offset}.translateZ;{br*2}'
        # expression2
        expr2 = f'float $D = `mag<<$nX-$pX, $nY-$pY, $nZ-$pZ>>`;{br*2}'
        # expression3
        expr3 = f'{loc}.rotateX = $J'
        expr3 += ' + ($D/$C) * 360'
        expr3 += ' * $A'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($O))'
        expr3 += f' / $S;{br*2}'
        # expression4
        expr4 = f'{offset}.PrevPosX = $nX;{br}'
        expr4 += f'{offset}.PrevPosY = $nY;{br}'
        expr4 += f'{offset}.PrevPosZ = $nZ;{br}'
        # final
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')


def isVertex(selection: str) -> bool:
    if isinstance(selection, pm.MeshVertex):
        return True
    else:
        return False


def isObject(selection: str) -> bool:
    if isinstance(selection, pm.nodetypes.Transform):
        return True
    else:
        return False


def getPositionVertex(vertex) -> list:
    position = pm.pointPosition(vertex)
    return position


def getPositionObject(object) -> list:
    position = pm.xform(object, q=1, ws=1, rp=1)
    return position


class A:
    def __init__(self):
        self.integerList = [1, 2, 3]


    def sum(self, a: int, b: int) -> int:
        result = a + b
        return result
    

    class B:
        def __init__(self):
            self.stringList = ['a', 'b', 'c']


        def sum(self, a: str, b: str) -> str:
            result = a + b
            return result


        def report(self):
            a = A()
            print(a.integerList)
            print(a.sum(1, 2))
            print(self.sum('a', 'b'))
            print(self.stringList)


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
        nameSlices = self.seperateNumbersInName(nameToCreate)
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


    def seperateNumbersInName(self, fullName: str) -> list:
        """ inputName -> "vhcl_car123_rig_v0123"
        >>> ['vhcl_car', '123', '_rig_v', '0123']
        """
        nameSlices = re.split(r'([^0-9]+)([0-9]*)', fullName)
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


    def nameDigitly(self, nameSlices: list, numbersInfo: dict):
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


    def nameSimply(self, nameSlices: list):
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
            om.MGlobal.displayWarning(warningMessages)
        else:
            warningMessages = "Rename all success."
            om.MGlobal.displayInfo(warningMessages)


