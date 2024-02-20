from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QMainWindow)


class Ui_MainWindow(QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)


    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(220, 220)
        MainWindow.setMinimumSize(QSize(220, 220))
        self.verticalLayout = QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(MainWindow)
        self.lineEdit.setObjectName(u"lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnCreate = QPushButton(MainWindow)
        self.btnCreate.setObjectName(u"btnCreate")
        self.horizontalLayout.addWidget(self.btnCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_2 = QLineEdit(MainWindow)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.btnDelete = QPushButton(MainWindow)
        self.btnDelete.setObjectName(u"btnDelete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)
        self.rdBtnAdd = QRadioButton(MainWindow)
        self.rdBtnAdd.setObjectName(u"rdBtnAdd")
        self.rdBtnAdd.setChecked(True)
        self.horizontalLayout_3.addWidget(self.rdBtnAdd)
        self.horizontalSpacer_4 = QSpacerItem(31, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)
        self.rdBtnToggle = QRadioButton(MainWindow)
        self.rdBtnToggle.setObjectName(u"rdBtnToggle")
        self.horizontalLayout_3.addWidget(self.rdBtnToggle)
        self.horizontalSpacer_2 = QSpacerItem(30, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QFrame(MainWindow)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnSample3 = QPushButton(MainWindow)
        self.btnSample3.setObjectName(u"btnSample3")
        self.gridLayout.addWidget(self.btnSample3, 1, 0, 1, 1)
        self.btnSample1 = QPushButton(MainWindow)
        self.btnSample1.setObjectName(u"btnSample1")
        self.gridLayout.addWidget(self.btnSample1, 0, 0, 1, 1)
        self.btnSample2 = QPushButton(MainWindow)
        self.btnSample2.setObjectName(u"btnSample2")
        self.gridLayout.addWidget(self.btnSample2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QFrame(MainWindow)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)
        self.btnDeleteJsonData = QPushButton(MainWindow)
        self.btnDeleteJsonData.setObjectName(u"btnDeleteJsonData")
        self.horizontalLayout_4.addWidget(self.btnDeleteJsonData)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Vertex Selector", None))
        self.btnCreate.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.btnDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.rdBtnAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.rdBtnToggle.setText(QCoreApplication.translate("MainWindow", u"Toggle", None))
        self.btnSample3.setText(QCoreApplication.translate("MainWindow", u"btn3", None))
        self.btnSample1.setText(QCoreApplication.translate("MainWindow", u"btn1", None))
        self.btnSample2.setText(QCoreApplication.translate("MainWindow", u"btn2", None))
        self.btnDeleteJsonData.setText(QCoreApplication.translate("MainWindow", u"Delete Json Data", None))


if __name__ == "__main__":
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = Ui_MainWindow()
    ui.show()



