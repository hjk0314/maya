import os
import re
import json
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


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


class VertexSelector(QWidget):
    def __init__(self):
        """ This is a UI that gives a name to the selected vertex group 
        and turns it into a button.
        >>> import vertexSelector as vtxSel
        >>> 
        >>> 
        >>> if __name__ == "__main__":
        >>>     try:
        >>>         vtx.close()
        >>>         vtx.deleteLater()
        >>>     except:
        >>>         pass
        >>>     vtx = vtxSel.VertexSelector()
        >>>     vtx.show()
         """
        super(VertexSelector, self).__init__()
        self.sortCount = 0
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()
    # def __init__(self, parent=mayaMainWindow()):
    #     super(VertexSelector, self).__init__(parent)
    #     self.sortCount = 0
    #     self.setWindowFlags(Qt.Window)
    #     self.setupUI()


    def setupUI(self):
        self.setWindowTitle("Vertex Selector")
        self.move(0, 0)
        self.setMinimumWidth(200)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        # Create button.
        self.lineEdit = QLineEdit()
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnCreate = QPushButton("Create")
        self.btnCreate.setFixedSize(60, 23)
        self.horizontalLayout.addWidget(self.btnCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        # Delete button.
        self.horizontalLayout_2 = QHBoxLayout()
        self.lineEdit_2 = QLineEdit()
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.setFixedSize(60, 23)
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        # Rename button.
        self.horizontalLayout_3 = QHBoxLayout()
        self.lineEdit_3 = QLineEdit()
        self.lineEdit_3.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.lineEdit_2.textChanged.connect(self.enableRenameButton)
        self.lineEdit_3.textChanged.connect(self.enableRenameButton)
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.btnRename = QPushButton("Rename")
        self.btnRename.setEnabled(False)
        self.btnRename.setFixedSize(60, 23)
        self.horizontalLayout_3.addWidget(self.btnRename)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        # Radio button.
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalSpacer_3 = QSpacerItem(23, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.rdBtnAdd = QRadioButton("Add")
        self.horizontalLayout_3.addWidget(self.rdBtnAdd)
        self.horizontalSpacer_4 = QSpacerItem(23, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)
        self.rdBtnToggle = QRadioButton("Toggle")
        self.horizontalLayout_3.addWidget(self.rdBtnToggle)
        self.horizontalSpacer_5 = QSpacerItem(22, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)
        self.rdBtnSingle = QRadioButton("Single")
        self.rdBtnSingle.setChecked(True)
        self.horizontalLayout_3.addWidget(self.rdBtnSingle)
        self.horizontalSpacer_2 = QSpacerItem(23, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        # HLine Bar.
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        # Vertex Buttons.
        self.gridLayout = QGridLayout()
        self.verticalLayout.addLayout(self.gridLayout)
        # HLine Bar.
        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QHBoxLayout()
        # Sort
        self.btnSort = QPushButton("Sort")
        self.horizontalLayout_4.addWidget(self.btnSort)
        # Clear
        self.btnClear = QPushButton("Clear")
        self.horizontalLayout_4.addWidget(self.btnClear)
        # Close
        self.btnClose = QPushButton("Close")
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        # Select All
        self.horizontalLayout_5 = QHBoxLayout()
        self.btnSelectAll = QPushButton("Select All")
        self.horizontalLayout_5.addWidget(self.btnSelectAll)
        # Paint weights to One
        self.btnPaintWeights = QPushButton("Paint weights to 1.0")
        self.horizontalLayout_5.addWidget(self.btnPaintWeights)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # Buttons reload and links.
        self.refresh()
        self.buttonsLink()


    def refresh(self):
        """ Reload buttons. """
        jsonPath = self.getJsonFilePath()
        if not os.path.isfile(jsonPath):
            data = {}
        else:
            data = self.loadJsonFile(jsonPath)
        self.deleteGridLayoutItems()
        buttons = self.createButtons(data)
        self.buttonsConnection(buttons)
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.adjustSize()


    def buttonsLink(self):
        self.btnCreate.clicked.connect(self.createJsonFile)
        self.lineEdit.returnPressed.connect(self.createJsonFile)
        self.btnDelete.clicked.connect(self.deleteButtons)
        self.btnDelete.clicked.connect(self.deleteButtons)
        self.btnRename.clicked.connect(self.renameJsonFile)
        self.lineEdit_3.returnPressed.connect(self.renameJsonFile)
        self.btnSort.clicked.connect(self.sortButtons)
        self.btnClear.clicked.connect(self.clearSelection)
        self.btnClose.clicked.connect(self.close)
        self.btnSelectAll.clicked.connect(self.selectAllVertices)
        self.btnPaintWeights.clicked.connect(self.paintAllWeightsOne)
    

    def createButtons(self, data: dict) -> list:
        if self.sortCount % 2 == 1:
            sortedKeys = sorted(data.keys()) 
        else:
            sortedKeys = data.keys()
        buttons = []
        for idx, buttonName in enumerate(sortedKeys):
            row, column = divmod(idx, 2)
            button = QPushButton(buttonName, self)
            buttons.append(button)
            self.gridLayout.addWidget(button, row, column, 1, 1)
        self.gridLayout.setSpacing(2)
        return buttons


    def buttonsConnection(self, buttons):
        for btn in buttons:
            btn.clicked.connect(self.buttonClicked)


    def buttonClicked(self):
        jsonPath = self.getJsonFilePath()
        button = self.sender()
        buttonsName = button.text()
        self.lineEdit.setText(buttonsName)
        self.lineEdit_2.setText(buttonsName)
        data = self.loadJsonFile(jsonPath)
        objectVertex = data[buttonsName]
        vertices = []
        for obj, vtxList in objectVertex.items():
            if not pm.objExists(obj):
                # pm.warning('There is no "%s" mesh.' % obj)
                return
            for vtx in vtxList:
                vertices.append(f"{obj}{vtx}")
        boolAdd = self.rdBtnAdd.isChecked()
        boolToggle = self.rdBtnToggle.isChecked()
        # boolSingle = self.rdBtnSingle.isChecked()
        pm.select(vertices, af=boolAdd, tgl=boolToggle,)
        

    def deleteButtons(self):
        jsonPath = self.getJsonFilePath()
        data = self.loadJsonFile(jsonPath)
        key = self.lineEdit_2.text()
        data.pop(key, None)
        self.writeJsonFile(jsonPath, data)
        self.refresh()


    def sortButtons(self):
        self.sortCount += 1
        self.refresh()


    def clearSelection(self):
        # self.lineEdit.clear()
        self.lineEdit.clearFocus()
        self.lineEdit_2.clear()
        self.lineEdit_2.clearFocus()
        self.lineEdit_3.clear()
        self.lineEdit_3.clearFocus()
        pm.select(cl=True)


    def selectAllVertices(self):
        jsonPath = self.getJsonFilePath()
        if not jsonPath:
            return
        data = self.loadJsonFile(jsonPath)
        vertices = []
        for obj_vtxList in data.values():
            for obj, vtxList in obj_vtxList.items():
                if not pm.objExists(obj):
                    continue
                for vtx in vtxList:
                    vertices.append(f"{obj}{vtx}")
        pm.select(vertices)


    def lockWeightsOnOff(originalFunction):
        def wrapper(self):
            # Load json data
            jsonPath = self.getJsonFilePath()
            if not jsonPath:
                return
            data = self.loadJsonFile(jsonPath)
            # Joint's Lock Weights Status
            lockWeights = []
            for jnt in data.keys():
                lockWeights.append(pm.getAttr(f"{jnt}.liw"))
                pm.setAttr(f"{jnt}.liw", 0)
            # Main Function
            result = originalFunction(self, data)
            # Restore Lock Weights Status
            for jnt, onOff in zip(data.keys(), lockWeights):
                pm.setAttr(f"{jnt}.liw", onOff)
            # Result
            if result:  pm.warning("List of failures: ", result)
            else:       pm.displayInfo("Successfully Done.")
            return result
        return wrapper


    @lockWeightsOnOff
    def paintAllWeightsOne(self, data: dict):
        failed = set()
        for jnt, obj_vtxList in data.items():
            for obj, vtxList in obj_vtxList.items():
                if not pm.objExists(obj):
                    continue
                for vtx in vtxList:
                    objVtx = f"{obj}{vtx}"
                    skinClt = pm.listHistory(objVtx, type="skinCluster")
                    try:
                        pm.skinPercent(skinClt[0], objVtx, tv=(jnt, 1))
                    except:
                        failed.add(jnt)
                        continue
        return failed


    def adjustSize(self):
        optimalSize = self.verticalLayout.sizeHint()
        self.resize(optimalSize)
        # self.setMinimumSize(QSize(optimalSize))


    def deleteGridLayoutItems(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


    def enableRenameButton(self):
        if self.lineEdit_2.text() and self.lineEdit_3.text():
            self.btnRename.setEnabled(True)
        else:
            self.btnRename.setEnabled(False)


    def getJsonFilePath(self) -> str:
        scenePath = pm.Env().sceneName()
        if not scenePath:
            pm.warning("This scene was not saved.")
            result = ""
        else:
            jsonFileName = "vertexForSkinWeight.json"
            dir = os.path.dirname(scenePath)
            result = "%s/%s" % (dir, jsonFileName)
        return result


    def createJsonFile(self):
        """ If the json file doesn't exist, create a new one, 
        but overwrite. 
         """
        vertexName = self.lineEdit.text()
        vertexNumber = self.getListsOfVertexNumber()
        if not vertexName:
            pm.warning("Vertex name field is empty.")
            return
        if not vertexNumber:
            pm.warning("Nothing selected.")
            return
        jsonPath = self.getJsonFilePath()
        isJsonFile = os.path.isfile(jsonPath)
        data = self.loadJsonFile(jsonPath) if isJsonFile else {}
        data[vertexName] = vertexNumber
        self.writeJsonFile(jsonPath, data)
        self.refresh()


    def renameJsonFile(self):
        old = self.lineEdit_2.text()
        new = self.lineEdit_3.text()
        if not old or not new:
            return
        jsonPath = self.getJsonFilePath()
        data = self.loadJsonFile(jsonPath)
        data[new] = data.pop(old, None)
        self.writeJsonFile(jsonPath, data)
        self.refresh()


    def writeJsonFile(self, fullPath, data):
        with open(fullPath, 'w') as txt:
            json.dump(data, txt, indent=4)


    def loadJsonFile(self, fullPath) -> dict:
        with open(fullPath, 'r') as txt:
            data = json.load(txt)
        return data


    def getListsOfVertexNumber(self) -> dict:
        """ Get vertex numbers only, strip others. """
        sel = pm.ls(sl=True)
        obj = pm.ls(sel, o=True)
        shapes = set(obj)
        result = {}
        for shp in shapes:
            compiled = re.compile(f'(?<={shp}).+[0-9]+:*[0-9]*.+')
            vertexNumbers = []
            for i in sel:
                try:
                    temp = compiled.search(i.name())
                    vertexNumbers.append(temp.group(0))
                except:
                    continue
            result[shp.getParent().name()] = vertexNumbers
        return result


class SpeedMeasurement(QWidget):
    def __init__(self):
        self.unitTimeIndex = {
            'game': 15, 
            'film': 24, 
            'pal': 25, 
            'ntsc': 30, 
            'show': 48, 
            'palf': 50, 
            'ntscf': 60
            }
        self.unitLengthIndex = {
            'mm': 0.1, 
            'cm': 1, 
            'm': 100, 
            'km': 100000, 
            'in': 2.54, 
            'ft': 30.48, 
            'yd': 91.44, 
            'mi': 160934
            }
        super(SpeedMeasurement, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Speed Measurement")
        self.move(0, 0)
        self.resize(250, 150)
        # Layout
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.label = QLabel("Duration")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        # Duration
        self.horizontalLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setValidator(QIntValidator())
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setValidator(QIntValidator())
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)
        # Curved path
        self.label_2 = QLabel("Curved Path")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.checkBox = QCheckBox()
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkBox)
        # Speed1
        self.label_3 = QLabel("Speed1")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.speed1 = QLineEdit()
        self.speed1.setReadOnly(True)
        self.speed1.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.speed1)
        # Speed2
        self.label_4 = QLabel("Speed2")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)
        self.speed2 = QLineEdit()
        self.speed2.setReadOnly(True)
        self.speed2.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.speed2)
        self.verticalLayout.addLayout(self.formLayout)
        # Buttons
        self.btnSpeed = QPushButton("Speed")
        self.verticalLayout.addWidget(self.btnSpeed)
        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        # Spacer
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # functions
        self.fillDuration()
        self.buttonsLink()


    def fillDuration(self):
        minTime = pm.playbackOptions(q=True, min=True)
        maxTime = pm.playbackOptions(q=True, max=True)
        minTime = int(minTime)
        maxTime = int(maxTime)
        self.lineEdit.setText(f"{minTime}")
        self.lineEdit_2.setText(f"{maxTime}")


    def buttonsLink(self):
        self.btnSpeed.clicked.connect(self.getSpeed)
        self.btnClose.clicked.connect(self.close)


    def getSpeed(self):
        # selection
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning('Nothing Selected.')
            return
        # time
        startFrame = self.lineEdit.text()
        startFrame = int(startFrame)
        endFrame = self.lineEdit_2.text()
        endFrame = int(endFrame)
        duration = endFrame - startFrame + 1
        # distance
        curveCheckBox = self.checkBox.isChecked()
        if curveCheckBox:
            distance = self.getCurveLength(sel[0], startFrame, endFrame)
        else:
            distance = self.getDistance(sel[0], startFrame, endFrame)
        # Result
        print(distance)
        print(duration)
        speed = self.getVelocity(distance, duration)
        kmPerHour, meterPerSec = speed
        self.speed1.setText('%0.3f km/h' % kmPerHour)
        self.speed2.setText('%0.3f m/s' % meterPerSec)
    

    def getDistance(self, geo: str, startFrame: int, endFrame: int) -> float:
        # positions
        pm.currentTime(startFrame)
        startPos = pm.xform(geo, q=True, ws=True, rp=True)
        pm.currentTime(endFrame)
        endPos = pm.xform(geo, q=True, ws=True, rp=True)
        # result
        startVector = pm.datatypes.Vector(startPos)
        endVector = pm.datatypes.Vector(endPos)
        distance = startVector.distanceTo(endVector)
        return distance

    
    def getCurveLength(self, geo: str, startFrame: int, endFrame: int) -> str:
        # positions every frame
        positions = []
        for i in range(startFrame, endFrame + 1):
            pm.currentTime(i)
            try:
                positions.append(pm.pointPosition(geo))
            except:
                positions.append(pm.xform(geo, q=True, ws=True, rp=True))
        cuv = pm.curve(p=positions)
        # result
        cuvLength = pm.arclen(cuv)
        return cuvLength

    
    def getVelocity(self, distance, duration):
        # Convert Units to Centimeters.
        currUnitTime = pm.currentUnit(q=True, t=True)
        currUnitLength = pm.currentUnit(q=True, l=True)
        convertCentimeter = distance * self.unitLengthIndex[currUnitLength]
        # fps -> second
        if 'fps' in currUnitTime:
            sec = duration / float(currUnitTime.split('fps')[0])
        else:
            sec = duration / self.unitTimeIndex[currUnitTime]
        # result
        kmPerHour = (convertCentimeter/self.unitLengthIndex['km'])/(sec/60/60)
        kmPerHour = round(kmPerHour, 3)
        meterPerSec = (convertCentimeter/self.unitLengthIndex['m'])/sec
        meterPerSec = round(meterPerSec, 3)
        return kmPerHour, meterPerSec


class MoveToCameraKeysAndSequence(QWidget):
    def __init__(self):
        super(MoveToCameraKeysAndSequence, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Offset Camera's Keys And ImageSequences")
        self.move(0, 0)
        self.resize(210, 75)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblKeyframe = QLabel("Keyframes")
        self.lblKeyframe.setObjectName(u"lblKeyframe")
        self.horizontalLayout.addWidget(self.lblKeyframe)
        self.txtKeyStep = QLineEdit()
        self.txtKeyStep.setObjectName(u"txtKeyStep")
        self.txtKeyStep.setValidator(QIntValidator())
        self.txtKeyStep.setText("0")
        self.horizontalLayout.addWidget(self.txtKeyStep)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnOffset = QPushButton("Move Keyframes and imgPlane")
        self.btnOffset.setObjectName(u"btnOffset")
        self.verticalLayout.addWidget(self.btnOffset)
        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.buttonsLink()


    def buttonsLink(self):
        self.btnOffset.clicked.connect(self.moveToKeyframe)


    def moveToKeyframe(self):
        keyStep = self.txtKeyStep.text()
        try:
            keyStep = int(keyStep)
        except:
            pm.warning("Nothing inputs")
            return
        sel = pm.ls(sl=True, dag=True, type=['camera'])
        cam = pm.listRelatives(sel, p=True)
        try:
            currentKey = min(pm.keyframe(cam, q=True))
            value = keyStep - currentKey
        except:
            value = 0
            pm.warning("Camera must have at least one keyframes.")
        img = pm.listRelatives(sel, c=True)
        imgShape = pm.listRelatives(img, c=True)
        if img:
            pm.keyframe(cam, e=True, r=True, tc=value)
            frameOffset = pm.getAttr(imgShape[0] + ".frameOffset")
            pm.setAttr(imgShape[0] + ".frameOffset", frameOffset - value)
        else:
            pm.warning("Please Select a camera.")


# if __name__ == "__main__":
#     try:
#         vtxSel.close()
#         vtxSel.deleteLater()
#     except:
#         pass
#     vtxSel = VertexSelector()
#     vtxSel.show()


# if __name__ == "__main__":
#     try:
#         spd.close()
#         spd.deleteLater()
#     except:
#         pass
#     spd = SpeedMeasurement()
#     spd.show()


# if __name__ == "__main__":
#     try:
#         offsetCam.close()
#         offsetCam.deleteLater()
#     except:
#         pass
#     offsetCam = MoveToCameraKeysAndSequence()
#     offsetCam.show()
