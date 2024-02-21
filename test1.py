
from PySide2.QtWidgets import QApplication, QWidget, QDialog, \
QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
QFormLayout, QSpinBox, QSpacerItem, QSizePolicy, QRadioButton, \
QFrame, QGridLayout, QMainWindow, QListWidget
from PySide2.QtCore import Qt, QSize, QDir
from shiboken2 import wrapInstance
import pymel.core as pm
import maya.OpenMayaUI as omui
import json
import os
import re


class TestDialog(QMainWindow):
    def mayaMainWindow():
        mainWindow_pointer = omui.MQtUtil.mainWindow()
        return wrapInstance(int(mainWindow_pointer), QMainWindow)


    # def __init__(self):
    def __init__(self, parent=mayaMainWindow()):
        super(TestDialog, self).__init__(parent)
        mainWidget = QWidget(self)
        self.setupUI(mainWidget)
        # self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # self.setWindowFlags(self.windowFlags()^Qt.WindowContextHelpButtonHint)


    def setupUI(self, mainWindow):
        self.setWindowTitle("Test_Dialog")
        self.move(0, 0)
        self.setMinimumSize(QSize(220, 220))
        self.setMinimumWidth(200)
        self.setCentralWidget(mainWindow)
        self.verticalLayout = QVBoxLayout(mainWindow)
        self.horizontalLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnCreate = QPushButton("Create")
        self.horizontalLayout.addWidget(self.btnCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.lineEdit_2 = QLineEdit()
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.btnDelete = QPushButton("Delete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalSpacer_3 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.rdBtnAdd = QRadioButton("Add")
        self.rdBtnAdd.setChecked(True)
        self.horizontalLayout_3.addWidget(self.rdBtnAdd)
        self.horizontalSpacer_4 = QSpacerItem(31, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)
        self.rdBtnToggle = QRadioButton("Toggle")
        self.horizontalLayout_3.addWidget(self.rdBtnToggle)
        self.horizontalSpacer_2 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        # Create Buttons from json file.
        self.gridLayout = QGridLayout()
        self.buttons = self.buttonsRefresh()
        self.verticalLayout.addLayout(self.gridLayout)
        # End - Create Buttons from json file.
        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)
        self.btnRefresh = QPushButton("Refresh")
        self.horizontalLayout_4.addWidget(self.btnRefresh)
        self.btnClose = QPushButton("Close")
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # Button Clicked
        self.btnCreate.clicked.connect(self.createJsonFile)
        self.lineEdit.returnPressed.connect(self.createJsonFile)
        self.btnDelete.clicked.connect(self.deleteButtons)
        self.btnRefresh.clicked.connect(self.buttonsRefresh)
        self.btnClose.clicked.connect(self.close)


    def buttonClicked(self):
        jsonPath = self.getJsonFilePath()
        button = self.sender()
        buttonsName = button.text()
        self.lineEdit_2.setText(buttonsName)
        data = self.loadJsonFile(jsonPath)
        objectVertex = data[buttonsName]
        vertices = []
        for obj, vtxList in objectVertex.items():
            for vtx in vtxList:
                vertices.append(f"{obj}{vtx}")
        boolAdd = self.rdBtnAdd.isChecked()
        boolToggle = self.rdBtnToggle.isChecked()
        pm.select(vertices, af=boolAdd, tgl=boolToggle)
        

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
        """ If the json file doesn't exist, create a new one, but overwrite. """
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
        with open(jsonPath, 'w') as txt:
            json.dump(data, txt, indent=4)
        self.buttonsRefresh()


    def deleteButtons(self):
        jsonPath = self.getJsonFilePath()
        data = self.loadJsonFile(jsonPath)
        key = self.lineEdit_2.text()
        data.pop(key, None)
        with open(jsonPath, 'w') as txt:
            json.dump(data, txt, indent=4)
        self.buttonsRefresh()


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


    def buttonsRefresh(self):
        jsonPath = self.getJsonFilePath()
        if not os.path.isfile(jsonPath):
            data = {}
        else:
            data = self.getJsonData(jsonPath)
        self.deleteGridLayoutItems()
        buttons = self.createButtons(data)
        self.buttonsConnection(buttons)
        # self.lineEdit.clear()
        self.lineEdit_2.clear()


    def buttonsConnection(self, buttons):
        for btn in buttons:
            btn.clicked.connect(self.buttonClicked)


    def getJsonData(self, fullPath):
        with open(fullPath, 'r') as txt:
            data = json.load(txt)
        return data


    def deleteGridLayoutItems(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


    def createButtons(self, data: dict) -> list:
        buttons = []
        for idx, buttonName in enumerate(data.keys()):
            row, column = divmod(idx, 2)
            button = QPushButton(buttonName, self)
            buttons.append(button)
            self.gridLayout.addWidget(button, row, column, 1, 1)
        self.gridLayout.setSpacing(2)
        return buttons


if __name__ == "__main__":
    try:
        test.close()
        test.deleteLater()
    except:
        pass
    test = TestDialog()
    test.show()


