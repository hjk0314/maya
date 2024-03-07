import os
import re
import json
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


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
        # Sort, Clear, Close buttons.
        self.horizontalLayout_4 = QHBoxLayout()
        self.btnSort = QPushButton("Sort")
        self.horizontalLayout_4.addWidget(self.btnSort)
        self.btnClear = QPushButton("Clear")
        self.horizontalLayout_4.addWidget(self.btnClear)
        self.btnClose = QPushButton("Close")
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
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
        boolSingle = self.rdBtnSingle.isChecked()
        if boolSingle:
            pm.select(cl=True)
            boolToggle = True
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


if __name__ == "__main__":
    try:
        vtxSel.close()
        vtxSel.deleteLater()
    except:
        pass
    vtxSel = VertexSelector()
    vtxSel.show()


