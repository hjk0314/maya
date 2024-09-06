from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
# from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
from general import *
# import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Car(QWidget):
    def __init__(self):
        """ It was made for rough car rigging.
        - Function to make joints symmetrical.
        - Function to create a wheel controllers.
        - Function to add an expressions that rotates by the distance moved.
        - Tire compression function.
        - Function to create a door controllers.
        - Function to connect bind joint and rig joint.
         """
        self.topGroup = ""
        self.objGroup = ""
        self.bodyGroup = ""
        self.rootJnt = "jnt_root"
        self.rootFbx = "fbx_root"
        self.bodyJnt = "jnt_body"
        self.bodyFbx = "fbx_body"
        self.mainCtrl = "cc_main"
        self.subCtrl = "cc_sub"
        self.doorCtrls = []
        self.doorJoints = []
        self.jntNameAndPos = {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_bodyEnd": (0, 145, 0), 
            "jnt_wheelLeftFront": (70, 30, 140), 
            "jnt_wheelLeftFrontEnd": (85, 30, 140), 
            "jnt_wheelRightFront": (-70, 30, 140), 
            "jnt_wheelRightFrontEnd": (-85, 30, 140), 
            "jnt_wheelLeftBack": (70, 30, -140), 
            "jnt_wheelLeftBackEnd": (85, 30, -140), 
            "jnt_wheelRightBack": (-70, 30, -140), 
            "jnt_wheelRightBackEnd": (-85, 30, -140), 
            }
        self.hierarchy = {
            "jnt_root": [
                [f"jnt_body{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftBack{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightBack{i}" for i in ["", "End"]], 
                ], 
            }
        super(Car, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()
    

    def setupUI(self):
        self.setWindowTitle("quickRig_car")
        self.move(0, 0)
        self.resize(250, 630)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(5)
        self.gridLayout_createGrp = QGridLayout()
        self.lineSelObj = QLineEdit()
        self.lineSelObj.setPlaceholderText("Select")
        self.gridLayout_createGrp.addWidget(self.lineSelObj, 0, 0, 1, 1)
        self.btnSelObj = QPushButton("Object Group")
        self.gridLayout_createGrp.addWidget(self.btnSelObj, 0, 1, 1, 1)
        self.lineCreateGrp = QLineEdit()
        self.lineCreateGrp.setPlaceholderText("Typing Name")
        self.gridLayout_createGrp.addWidget(self.lineCreateGrp, 1, 0, 1, 1)
        self.btnCreateGrp = QPushButton("Create Group")
        self.gridLayout_createGrp.addWidget(self.btnCreateGrp, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_createGrp)
        self.hBar1 = QFrame()
        self.hBar1.setFrameShape(QFrame.HLine)
        self.hBar1.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar1)
        # ======================================================================
        self.gridLayout_selBody = QGridLayout()
        self.lineSelBody = QLineEdit()
        self.lineSelBody.setPlaceholderText("Select")
        self.gridLayout_selBody.addWidget(self.lineSelBody, 0, 0, 1, 1)
        self.btnSelBody = QPushButton("Body")
        self.btnSelBody.setFixedSize(80, 23)
        self.gridLayout_selBody.addWidget(self.btnSelBody, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_selBody)
        self.hBar2 = QFrame()
        self.hBar2.setFrameShape(QFrame.HLine)
        self.hBar2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar2)
        # ======================================================================
        self.verticalLayout_wheel = QVBoxLayout()
        self.lineWheelName = QLineEdit()
        self.lineWheelName.setPlaceholderText("Typing Name")
        self.verticalLayout_wheel.addWidget(self.lineWheelName)
        self.gridLayout_wheelName = QGridLayout()
        self.btnLeftFront = QPushButton("Left Front")
        self.gridLayout_wheelName.addWidget(self.btnLeftFront, 0, 0, 1, 1)
        self.btnRightFront = QPushButton("Right Front")
        self.gridLayout_wheelName.addWidget(self.btnRightFront, 0, 1, 1, 1)
        self.btnLeftBack = QPushButton("Left Back")
        self.gridLayout_wheelName.addWidget(self.btnLeftBack, 1, 0, 1, 1)
        self.btnRightBack = QPushButton("Right Back")
        self.gridLayout_wheelName.addWidget(self.btnRightBack, 1, 1, 1, 1)
        self.verticalLayout_wheel.addLayout(self.gridLayout_wheelName)
        self.btnCreateWheel = QPushButton("Create Wheel")
        self.verticalLayout_wheel.addWidget(self.btnCreateWheel)
        self.gridLayout_expression = QGridLayout()
        self.btnSetExpr = QPushButton("Set Expression")
        self.gridLayout_expression.addWidget(self.btnSetExpr, 0, 0, 1, 1)
        self.btnDelExpr = QPushButton("Del Expression")
        self.gridLayout_expression.addWidget(self.btnDelExpr, 0, 1, 1, 1)
        self.btnSetPressure = QPushButton("Set Pressure")
        self.gridLayout_expression.addWidget(self.btnSetPressure, 1, 0, 1, 1)
        self.btnDelPressure = QPushButton("Del Pressure")
        self.gridLayout_expression.addWidget(self.btnDelPressure, 1, 1, 1, 1)
        self.verticalLayout_wheel.addLayout(self.gridLayout_expression)
        self.btnDelWheel = QPushButton("Delete Wheel")
        self.verticalLayout_wheel.addWidget(self.btnDelWheel)
        self.verticalLayout.addLayout(self.verticalLayout_wheel)
        self.hBar3 = QFrame()
        self.hBar3.setFrameShape(QFrame.HLine)
        self.hBar3.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar3)
        # ======================================================================
        self.verticalLayout_door = QVBoxLayout()
        self.lineDoorName = QLineEdit()
        self.lineDoorName.setPlaceholderText("Typing Name")
        self.verticalLayout_door.addWidget(self.lineDoorName)
        self.gridLayout_doorName = QGridLayout()
        self.btnFrontDoor = QPushButton("Front Door")
        self.gridLayout_doorName.addWidget(self.btnFrontDoor, 0, 0, 1, 1)
        self.btnBackDoor = QPushButton("Back Door")
        self.gridLayout_doorName.addWidget(self.btnBackDoor, 0, 1, 1, 1)
        self.verticalLayout_door.addLayout(self.gridLayout_doorName)
        self.btnCreateDoor = QPushButton("Create Door")
        self.verticalLayout_door.addWidget(self.btnCreateDoor)
        self.btnDelDoor = QPushButton("Delete Door")
        self.verticalLayout_door.addWidget(self.btnDelDoor)
        self.verticalLayout.addLayout(self.verticalLayout_door)
        self.hBar4 = QFrame()
        self.hBar4.setFrameShape(QFrame.HLine)
        self.hBar4.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar4)
        # ======================================================================
        self.verticalLayout_createJnt = QVBoxLayout()
        self.btnCreateJnt = QPushButton("Create Joints")
        self.verticalLayout_createJnt.addWidget(self.btnCreateJnt)
        self.gridLayout_symSide = QGridLayout()
        self.btnLeftRight = QPushButton("Left to Right")
        self.gridLayout_symSide.addWidget(self.btnLeftRight, 0, 0, 1, 1)
        self.btnRightLeft = QPushButton("Right to Left")
        self.gridLayout_symSide.addWidget(self.btnRightLeft, 0, 1, 1, 1)
        self.verticalLayout_createJnt.addLayout(self.gridLayout_symSide)
        self.btnBuild = QPushButton("Build")
        self.verticalLayout_createJnt.addWidget(self.btnBuild)
        self.btnCleanAll = QPushButton("Clean All")
        self.verticalLayout_createJnt.addWidget(self.btnCleanAll)
        self.verticalLayout.addLayout(self.verticalLayout_createJnt)
        self.hBar5 = QFrame()
        self.hBar5.setFrameShape(QFrame.HLine)
        self.hBar5.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar5)
        # ======================================================================
        self.horizontalLayout_connect = QHBoxLayout()
        self.btnConnect = QPushButton("Connect")
        self.horizontalLayout_connect.addWidget(self.btnConnect)
        self.btnDisconnect = QPushButton("Disonnect")
        self.horizontalLayout_connect.addWidget(self.btnDisconnect)
        self.verticalLayout.addLayout(self.horizontalLayout_connect)
        self.hBar6 = QFrame()
        self.hBar6.setFrameShape(QFrame.HLine)
        self.hBar6.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hBar6)
        # ======================================================================
        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # ======================================================================
        self.buttonsLink()


    def buttonsLink(self):
        self.btnSelObj.clicked.connect(self.selectObjectGroup)
        self.btnCreateGrp.clicked.connect(self.createTopGroup)
        self.btnSelBody.clicked.connect(self.selectBodyGroup)
        self.btnClose.clicked.connect(self.close)


    def selectObjectGroup(self):
        sel = selectGroupOnly()
        if sel:
            txt = sel[0].name()
            self.objGroup = txt
            self.lineSelObj.setText(txt)
            return txt
        else:
            return


    def selectBodyGroup(self):
        sel = selectGroupOnly()
        if sel:
            txt = sel[0].name()
            self.bodyGroup = txt
            self.lineSelBody.setText(txt)
            return txt
        else:
            return


    def createTopGroup(self) -> str:
        txt = self.lineCreateGrp.text()
        if self.topGroup == "" and txt == "":
            return
        elif self.topGroup != "" and txt == "":
            grpName = self.topGroup
        elif txt != "":
            grpName = txt
        else:
            return
        createRigGroups(grpName)
        self.topGroup = grpName
        self.lineCreateGrp.setText(grpName)
        self.lineCreateGrp.clearFocus()
        return grpName




if __name__ == "__main__":
    try:
        qrCar.close()
        qrCar.deleteLater()
    except:
        pass
    qrCar = Car()
    qrCar.show()