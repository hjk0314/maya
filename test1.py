
from PySide2.QtWidgets import QApplication, QWidget, QDialog, \
QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
QFormLayout, QSpinBox, QSpacerItem, QSizePolicy, QRadioButton, \
QFrame, QGridLayout
from PySide2.QtCore import Qt, QSize
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QDialog)


class TestDialog(QDialog):
    # def __init__(self, parent=None):
    def __init__(self, parent=mayaMainWindow()):
        super(TestDialog, self).__init__(parent)
        self.setupUI()
        # self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # self.setWindowFlags(self.windowFlags()^Qt.WindowContextHelpButtonHint)


    def setupUI(self):
        self.setWindowTitle("Test_Dialog")
        self.resize(220, 220)
        self.setMinimumSize(QSize(220, 220))
        self.setMinimumWidth(200)
        self.verticalLayout = QVBoxLayout(self)
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
        # Start Buttons Looping ===============================
        self.gridLayout = QGridLayout()
        self.btnSample1 = QPushButton("Sample1")
        self.gridLayout.addWidget(self.btnSample1, 0, 0, 1, 1)
        self.btnSample2 = QPushButton("Sample2")
        self.gridLayout.addWidget(self.btnSample2, 0, 1, 1, 1)
        self.btnSample3 = QPushButton("Sample3")
        self.gridLayout.addWidget(self.btnSample3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        # End Buttons Looping ===============================
        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)
        self.btnClose = QPushButton("Close")
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.btnClose.clicked.connect(self.close)


if __name__ == "__main__":
    try:
        test.close()
        test.deleteLater()
    except:
        pass
    test = TestDialog()
    test.show()


