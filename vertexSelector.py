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


class VertexSelector(QWidget):
    def __init__(self):
        """ This is a UI that gives a name to the selected vertex group 
        and turns it into a button.
         """
        # The end joint was removed from the entire joint.
        self.jointName = [
            "Hips", 
            "Spine", "Spine1", "Spine2", 
            "Neck", "Head", 
            "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", 
            "LeftHandThumb1", "LeftHandThumb2", "LeftHandThumb3", 
            "LeftHandIndex1", "LeftHandIndex2", "LeftHandIndex3", 
            "LeftHandMiddle1", "LeftHandMiddle2", "LeftHandMiddle3", 
            "LeftHandRing1", "LeftHandRing2", "LeftHandRing3", 
            "LeftHandPinky1", "LeftHandPinky2", "LeftHandPinky3", 
            "RightShoulder", "RightArm", "RightForeArm", "RightHand", 
            "RightHandThumb1", "RightHandThumb2", "RightHandThumb3", 
            "RightHandIndex1", "RightHandIndex2", "RightHandIndex3", 
            "RightHandMiddle1", "RightHandMiddle2", "RightHandMiddle3", 
            "RightHandRing1", "RightHandRing2", "RightHandRing3", 
            "RightHandPinky1", "RightHandPinky2", "RightHandPinky3", 
            "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", 
            "RightUpLeg", "RightLeg", "RightFoot", "RightToeBase", 
            # "LeftFlipper", "LeftFlipper1", "LeftFlipper2", 
            # "RightFlipper", "RightFlipper1", "RightFlipper2", 
            ]
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
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setContentsMargins(10, 10, 10, 5)
        # Create button.
        self.horizontalLayout = QHBoxLayout()
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
        self.rdBtnAdd = QRadioButton("add")
        self.horizontalLayout_3.addWidget(self.rdBtnAdd)
        self.horizontalSpacer_4 = QSpacerItem(23, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)
        self.rdBtnToggle = QRadioButton("tgl")
        self.horizontalLayout_3.addWidget(self.rdBtnToggle)
        self.horizontalSpacer_5 = QSpacerItem(22, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)
        self.rdBtnSingle = QRadioButton("single")
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
        # Select Object
        self.horizontalLayout_selObj = QHBoxLayout()
        self.lineEdit_selObj = QLineEdit()
        self.horizontalLayout_selObj.addWidget(self.lineEdit_selObj)
        self.btnSelObj = QPushButton("Select")
        self.btnSelObj.setFixedSize(60, 23)
        self.horizontalLayout_selObj.addWidget(self.btnSelObj)
        self.verticalLayout.addLayout(self.horizontalLayout_selObj)
        # Auto Creation
        self.horizontalLayout_auto = QHBoxLayout()
        self.btnAutoPaint = QPushButton("Auto Creation")
        self.horizontalLayout_auto.addWidget(self.btnAutoPaint)
        self.verticalLayout.addLayout(self.horizontalLayout_auto)
        # Paint weights to One
        self.horizontalLayout_paintWeight = QHBoxLayout()
        self.btnPaintWeights = QPushButton("Paint Weights to 1.0")
        self.horizontalLayout_paintWeight.addWidget(self.btnPaintWeights)
        self.verticalLayout.addLayout(self.horizontalLayout_paintWeight)
        # Select All
        self.horizontalLayout_4 = QHBoxLayout()
        self.btnSelectAll = QPushButton("Select all Vertices")
        self.horizontalLayout_4.addWidget(self.btnSelectAll)
        # Clear
        self.btnClear = QPushButton("Clear Selections")
        self.horizontalLayout_4.addWidget(self.btnClear)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        # Sort
        self.horizontalLayout_sort = QHBoxLayout()
        self.btnSort = QPushButton("Sort Buttons")
        self.horizontalLayout_sort.addWidget(self.btnSort)
        self.verticalLayout.addLayout(self.horizontalLayout_sort)
        # Close
        self.horizontalLayout_5 = QHBoxLayout()
        self.btnClose = QPushButton("Close")
        self.horizontalLayout_5.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        # Spacer
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
        self.btnSelObj.clicked.connect(self.selectObject)
        self.btnAutoPaint.clicked.connect(self.autoPaint)
    

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
        self.gridLayout.setSpacing(3)
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


    def selectObject(self):
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning("Select an object to make skinCluster")
            return
        if not sel[-1].getShape():
            pm.warning("Select an object that has a shape.")
            return
        self.lineEdit_selObj.setText(sel[-1].name())


    def autoPaint(self):
        topLevelJoint = self.jointName[0]
        selObj = self.lineEdit_selObj.text()
        isSkinCluster = pm.listHistory(selObj, type="skinCluster")
        if isSkinCluster:
            pm.warning("skinCluster aleady exists.")
            return
        else:
            skinClt = pm.skinCluster(topLevelJoint, selObj, \
                                     tsb=False, bm=0, sm=0, nw=1, wd=0, mi=1)
            for i in self.jointName:
                if not pm.objExists(i):
                    continue
                pm.select(cl=True)
                pm.skinCluster(skinClt, e=True, siv=i)
                self.createJsonFile(i)
            pm.select(cl=True)
            pm.skinCluster(selObj, e=True, mi=5)


    # def paintAllWeightsOne(self):
    #     # Load json data
    #     jsonPath = self.getJsonFilePath()
    #     if not jsonPath:
    #         return
    #     data = self.loadJsonFile(jsonPath)
    #     # Joint's Lock Weights Status
    #     lockWeights = []
    #     for jnt in data.keys():
    #         lockWeights.append(pm.getAttr(f"{jnt}.liw"))
    #         pm.setAttr(f"{jnt}.liw", 0)
    #     failed = set()
    #     for jnt, obj_vtxList in data.items():
    #         for obj, vtxList in obj_vtxList.items():
    #             if not pm.objExists(obj):
    #                 continue
    #             for vtx in vtxList:
    #                 objVtx = f"{obj}{vtx}"
    #                 skinClt = pm.listHistory(objVtx, type="skinCluster")
    #                 try:
    #                     pm.skinPercent(skinClt[0], objVtx, tv=(jnt, 1))
    #                 except:
    #                     failed.add(jnt)
    #                     continue
    #     # Restore Lock Weights Status
    #     for jnt, onOff in zip(data.keys(), lockWeights):
    #         pm.setAttr(f"{jnt}.liw", onOff)
    #     # Result
    #     if failed:  pm.warning("List of failures: ", failed)
    #     else:       pm.displayInfo("Successfully Done.")


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


    def createJsonFile(self, arg: str=""):
        """ If the json file doesn't exist, create a new one, 
        but overwrite. 
         """
        vertexName = arg if arg else self.lineEdit.text()
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
            pattern = r'\.vtx\[\d+(?::\d+)?\]'
            vertexNumbers = []
            for i in sel:
                try:
                    temp = re.search(pattern, i.name())
                    vertexNumbers.append(temp.group())
                except:
                    continue
            result[shp.getParent().name()] = vertexNumbers
        return result


# if __name__ == "__main__":
#     try:
#         vtxSel.close()
#         vtxSel.deleteLater()
#     except:
#         pass
#     vtxSel = VertexSelector()
#     vtxSel.show()

