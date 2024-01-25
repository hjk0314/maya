
import sys
import re
import pymel.core as pm
import maya.OpenMaya as om
import os
import json


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


class QuickRig:
    def upParentHierarchically(self, selections: list=[]):
        if not selections:
            selections = pm.selected()
        for object in selections:
            if not pm.listRelatives(object, p=True):
                continue
            else:
                pm.parent(object, w=True)


    def attachLocatorsToHumanSpines(self, spinesGroup: list) -> list:
        """ Return created locators.
        >>> spinesGroup = ['Hips', 'Spine', 'Spine1', ]
        >>> result = ['loc_Hips', 'loc_Spine', 'loc_Spine1', ]
         """
        result = []
        for boneName in spinesGroup:
            locatorName = f"loc_{boneName}"
            locator = pm.spaceLocator(n=locatorName)
            pm.matchTransform(locator, boneName, pos=True)
            result.append(locator)
        return result


    def attachHumanSpinesToLocators(self, spinesGroup):
        for boneName in spinesGroup:
            try:
                pm.matchTransform(boneName, f"loc_{boneName}", pos=True)
            except:
                continue


    def isSpinesGroupCentered(self, spinesGroup) -> bool:
        for bone in spinesGroup:
            x, y, z = pm.xform(bone, q=True, t=True, ws=True)
            x = round(x, 3)
            if x != 0:
                return False
            else:
                continue
        return True


    def seperateRootJointFromMainCurve(self):
        rootJoint = self.humanSpines[0]
        pm.makeIdentity(self.humanMainCurve, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.parent(rootJoint, w=True)


    def combineRootJointToMainCurve(self):
        rootJoint = self.humanSpines[0]
        pm.parent(rootJoint, w=True)


    def seperateHumanArmsAndLegs(self):
        arms = self.humanArms[0]
        legs = self.humanLegs[0]
        for i in ["Left", "Right"]:
            pm.parent(i + arms, self.humanMainCurve)
            pm.parent(i + legs, self.humanMainCurve)


    def combineHumanArmsAndLegs(self):
        for parents, child in self.humanJointStructure2.items():
            try:
                pm.parent(child, parents)
            except:
                continue


    def centerTheLocators(self, locators: list):
        for i in locators:
            x, y, z = pm.xform(i, q=True, t=True, ws=True)
            position = [0-x, y, z]
            pm.xform(i, t=position, r=True, ws=True)


class VertexSeletor:
    def __init__(self):
        self.jsonPath = self.getJsonPath()
        if not self.jsonPath:
            return
        else:
            self.setupUI()
    

    def getJsonPath(self):
        """ Create the path of the json file based on this scene. """
        fullPath = pm.Env().sceneName()
        if not fullPath:
            print("File not saved.")
            return
        else:
            dir = os.path.dirname(fullPath)
            # name_ext = os.path.basename(fullPath)
            # name, ext = os.path.splitext(name_ext)
            result = f"{dir}/vertexSeletor.json"
            return result


    # UI
    def setupUI(self):
        winName = 'vertexButton'
        if pm.window(winName, exists=True):
            pm.deleteUI(winName)
        win = pm.window(winName, t='Vertex Selector', s=True, rtf=True)
        pm.columnLayout(cat=('both', 4), rs=2, cw=178)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=3, cw=[(1, 80), (2, 5), (3, 80)])
        self.field = pm.textField(ed=True)
        pm.text('')
        pm.button(l="Create", c=lambda x: self.writeJson())
        pm.setParent("..", u=True)
        pm.separator(h=10)
        pm.rowColumnLayout(nc=3, cw=[(1, 80), (2, 5), (3, 80)])
        pm.radioCollection()
        self.radioAdd = pm.radioButton(l='add', sl=True)
        pm.text('')
        self.radioTgl = pm.radioButton(l='tgl')
        pm.setParent("..", u=True)
        spacing = [(1, 80), (2, 3), (3, 80), (4, 3)]
        pm.rowColumnLayout(nc=4, rs=(1, 3), cw=spacing)
        chk = os.path.isfile(self.jsonPath)
        if chk:
            data = self.loadJson()
            for key in data:
                self.button(key)
        else:
            pass
        pm.setParent("..", u=True)
        pm.separator(h=10)
        pm.button(l="Clear", c=lambda x: pm.select(cl=True))
        pm.button(l="Delete Data", c=lambda x: self.deleteJson())
        pm.button(l="Close", c=lambda x: pm.deleteUI(winName))
        pm.separator(h=10)
        pm.showWindow(win)


    def button(self, *args):
        """ Create the looping button. """
        for i in args:
            pm.button(l=i, c=lambda x: self.selectVtx(i))
            pm.text(' ')


    def writeJson(self) -> None:
        """ If the json file does not exist, create a new one.
        Otherwise, Save the dictionary as a json file
         """
        chk = os.path.isfile(self.jsonPath)
        if not chk:
            data = {}
        else:
            data = self.loadJson()
        name = self.field.getText()
        info = self.vertexNum()
        data[name] = info
        with open(self.jsonPath, 'w') as JSON:
            json.dump(data, JSON, indent=4)
        VertexSeletor()


    def loadJson(self) -> dict:
        """ Load information from json file and select vertex. """
        with open(self.jsonPath, 'r') as JSON:
            data = json.load(JSON)
        return data


    def deleteJson(self):
        """ It doesn't delete the data, it destroys the file itself. """
        chk = os.path.isfile(self.jsonPath)
        if not chk:
            return
        else:
            os.remove(self.jsonPath)


    def vertexNum(self) -> dict:
        """ Make a list of vertex numbers only. """
        sel = pm.ls(sl=True)
        obj = pm.ls(sel, o=True)
        shapes = set(obj)
        result = {}
        for shp in shapes:
            com = re.compile(f'(?<={shp}).+[0-9]+:*[0-9]*.+')
            vtxNum = []
            for j in sel:
                try:
                    tmp = com.search(j.name())
                    vtxNum.append(tmp.group(0))
                except:
                    continue
            result[shp.getParent().name()] = vtxNum
        return result


    def selectVtx(self, key: str):
        """ Click the button, selects the vortex. """
        data = self.loadJson()
        temp = data[key]
        result = []
        for j, k in temp.items():
            for i in k:
                result.append(j + i)
        ADD = self.radioAdd.getSelect()
        TGL = self.radioTgl.getSelect()
        pm.select(result, af=ADD, tgl=TGL)


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(QWidget):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setWindowTitle("Ref3's Test")
        self.resize(220, 220)
        self.setMinimumSize(QSize(220, 220))
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(u"lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnCreate = QPushButton()
        self.btnCreate.setObjectName(u"btnCreate")
        self.horizontalLayout.addWidget(self.btnCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.btnDelete = QPushButton()
        self.btnDelete.setObjectName(u"btnDelete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.rdBtnAdd = QRadioButton()
        self.rdBtnAdd.setObjectName(u"rdBtnAdd")
        self.rdBtnAdd.setChecked(True)
        self.horizontalLayout_3.addWidget(self.rdBtnAdd)
        self.horizontalSpacer_4 = QSpacerItem(31, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)
        self.rdBtnToggle = QRadioButton()
        self.rdBtnToggle.setObjectName(u"rdBtnToggle")
        self.horizontalLayout_3.addWidget(self.rdBtnToggle)
        self.horizontalSpacer_2 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QFrame()
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnSample3 = QPushButton()
        self.btnSample3.setObjectName(u"btnSample3")
        self.gridLayout.addWidget(self.btnSample3, 1, 0, 1, 1)
        self.btnSample1 = QPushButton()
        self.btnSample1.setObjectName(u"btnSample1")
        self.gridLayout.addWidget(self.btnSample1, 0, 0, 1, 1)
        self.btnSample2 = QPushButton()
        self.btnSample2.setObjectName(u"btnSample2")
        self.gridLayout.addWidget(self.btnSample2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QFrame()
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)
        self.btnDeleteJsonData = QPushButton()
        self.btnDeleteJsonData.setObjectName(u"btnDeleteJsonData")
        self.horizontalLayout_4.addWidget(self.btnDeleteJsonData)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self):
        # MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Vertex Selector", None))
        self.btnCreate.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.btnDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.rdBtnAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.rdBtnToggle.setText(QCoreApplication.translate("MainWindow", u"Toggle", None))
        self.btnSample3.setText(QCoreApplication.translate("MainWindow", u"btn3", None))
        self.btnSample1.setText(QCoreApplication.translate("MainWindow", u"btn1", None))
        self.btnSample2.setText(QCoreApplication.translate("MainWindow", u"btn2", None))
        self.btnDeleteJsonData.setText(QCoreApplication.translate("MainWindow", u"Delete Json Data", None))
    # retranslateUi


ui = Ui_MainWindow()
ui.show()


