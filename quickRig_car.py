from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QFont
from shiboken2 import wrapInstance
from hjk import *
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class QuickRig_Car(QWidget):
    def __init__(self):
        # Root Field
        tempRoot = getReferencedGroupList()
        self.rootGroup = u"%s" % tempRoot[0] if tempRoot else ""
        # Body Field
        tempBody = selectTopGroup(self.rootGroup, "body")
        self.bodyGroup = u"%s" % tempBody[0] if tempBody else ""
        # Door Field
        tempDoorLF = selectTopGroup(self.rootGroup, "door", "_L", "_Ft")
        self.doorLF = u"%s" % tempDoorLF[0] if tempDoorLF else ""
        tempDoorLB = selectTopGroup(self.rootGroup, "door", "_L", "_Bk")
        self.doorLB = u"%s" % tempDoorLB[0] if tempDoorLB else ""
        tempDoorRF = selectTopGroup(self.rootGroup, "door", "_R", "_Ft")
        self.doorRF = u"%s" % tempDoorRF[0] if tempDoorRF else ""
        tempDoorRB = selectTopGroup(self.rootGroup, "door", "_R", "_Bk")
        self.doorRB = u"%s" % tempDoorRB[0] if tempDoorRB else ""
        self.doorGroup = [self.doorLF, self.doorLB, self.doorRF, self.doorRB]
        tempDoorName = ["LeftFront", "LeftBack", "RightFront", "RightBack"]
        self.doorName = ["cc_door%s" % i for i in tempDoorName]
        # Wheel Field
        tempWheelLF = selectTopGroup(self.rootGroup, "wheel", "_L", "_Ft")
        self.wheelLF = u"%s" % tempWheelLF[0] if tempWheelLF else ""
        tempWheelLB = selectTopGroup(self.rootGroup, "wheel", "_L", "_Bk")
        self.wheelLB = u"%s" % tempWheelLB[0] if tempWheelLB else ""
        tempWheelRF = selectTopGroup(self.rootGroup, "wheel", "_R", "_Ft")
        self.wheelRF = u"%s" % tempWheelRF[0] if tempWheelRF else ""
        tempWheelRB = selectTopGroup(self.rootGroup, "wheel", "_R", "_Bk")
        self.wheelRB = u"%s" % tempWheelRB[0] if tempWheelRB else ""
        self.wheelGroup = [self.wheelLF, self.wheelLB, self.wheelRF, self.wheelRB]
        tempWheelName = ["LeftFront", "LeftBack", "RightFront", "RightBack"]
        self.wheelName = ["cc_wheel%s" % i for i in tempWheelName]
        # ColorBar
        self.colorBar = {
            "cc_main": "yellow", 
            "cc_sub": "pink", 
            "cc_body": "yellow", 
            "cc_doorLeftFront": "red", 
            "cc_doorLeftBack": "red", 
            "cc_doorRightFront": "blue", 
            "cc_doorRightBack": "blue", 
            "cc_wheelLeftFront_upDownMain": "yellow", 
            "cc_wheelLeftFront_upDownSub": "pink", 
            "cc_wheelLeftFront_main": "red", 
            "cc_wheelLeftFront_sub": "red2", 
            "cc_wheelLeftBack_upDownMain": "yellow", 
            "cc_wheelLeftBack_upDownSub": "pink", 
            "cc_wheelLeftBack_main": "red", 
            "cc_wheelLeftBack_sub": "red2", 
            "cc_wheelRightFront_upDownMain": "yellow", 
            "cc_wheelRightFront_upDownSub": "pink", 
            "cc_wheelRightFront_main": "blue", 
            "cc_wheelRightFront_sub": "blue2", 
            "cc_wheelRightBack_upDownMain": "yellow", 
            "cc_wheelRightBack_upDownSub": "pink", 
            "cc_wheelRightBack_main": "blue", 
            "cc_wheelRightBack_sub": "blue2", 
            }
        # Group Hierarchy
        self.groupHierarchy = {
            "controllers": [
                "cc_main_grp", 
                "cc_wheelLeftFront_grp", 
                "cc_wheelLeftBack_grp", 
                "cc_wheelRightFront_grp", 
                "cc_wheelRightBack_grp", 
                ], 
            "cc_sub": ["cc_body_grp"], 
            "cc_body": [
                "cc_doorLeftFront_grp", 
                "cc_doorLeftBack_grp", 
                "cc_doorRightFront_grp", 
                "cc_doorRightBack_grp", 
                ], 
            }
        # Delete List
        self.deleteName = [
            "cc_main_grp", 
            "cc_body_grp", 
            "cc_doorLeftFront_grp", 
            "cc_doorLeftBack_grp", 
            "cc_doorRightFront_grp", 
            "cc_doorRightBack_grp", 
            "cc_wheelLeftFront_grp", 
            "cc_wheelLeftFront_upDownMain_grp", 
            "cc_wheelLeftBack_grp", 
            "cc_wheelLeftBack_upDownMain_grp", 
            "cc_wheelRightFront_grp", 
            "cc_wheelRightFront_upDownMain_grp", 
            "cc_wheelRightBack_grp", 
            "cc_wheelRightBack_upDownMain_grp", 
            ]
        # Created Locators
        self.locators = [
            "loc_sub", 
            "loc_body", 
            "loc_doorLeftFront", 
            "loc_doorLeftBack", 
            "loc_doorRightFront", 
            "loc_doorRightBack", 
            "loc_wheelLeftFront_sub", 
            "loc_wheelLeftBack_sub", 
            "loc_wheelRightFront_sub", 
            "loc_wheelRightBack_sub", 
            ]
        # Set up User Interface
        super(QuickRig_Car, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()

    # UI
    def setupUI(self):
        self.setWindowTitle(u"Quick Rig for Car")
        self.move(0, 0)
        self.resize(300, 410)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, -1)
        self.lblRootGrp = QLabel()
        self.lblRootGrp.setObjectName(u"lblRootGrp")
        font = QFont()
        font.setFamily(u"Courier New")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.lblRootGrp.setFont(font)
        self.lblRootGrp.setLayoutDirection(Qt.LeftToRight)
        self.lblRootGrp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblRootGrp, 0, 0, 1, 1)
        self.fldRootGrp = QLineEdit()
        self.fldRootGrp.setObjectName(u"fldRootGrp")
        self.fldRootGrp.setClearButtonEnabled(True)
        self.fldRootGrp.setText(self.rootGroup)
        self.gridLayout.addWidget(self.fldRootGrp, 0, 1, 1, 1)
        self.btnRootGrp = QPushButton()
        self.btnRootGrp.setObjectName(u"btnRootGrp")
        self.btnRootGrp.setFont(font)
        self.gridLayout.addWidget(self.btnRootGrp, 0, 2, 1, 2)
        self.lblBodyGrp = QLabel()
        self.lblBodyGrp.setObjectName(u"lblBodyGrp")
        self.lblBodyGrp.setFont(font)
        self.lblBodyGrp.setLayoutDirection(Qt.LeftToRight)
        self.lblBodyGrp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblBodyGrp, 1, 0, 1, 1)
        self.fldBodyGrp = QLineEdit()
        self.fldBodyGrp.setObjectName(u"fldBodyGrp")
        self.fldBodyGrp.setClearButtonEnabled(True)
        self.fldBodyGrp.setText(self.bodyGroup)
        self.gridLayout.addWidget(self.fldBodyGrp, 1, 1, 1, 1)
        self.btnBodyGrp = QPushButton()
        self.btnBodyGrp.setObjectName(u"btnBodyGrp")
        self.btnBodyGrp.setFont(font)
        self.gridLayout.addWidget(self.btnBodyGrp, 1, 2, 1, 2)
        self.lblDoorLF = QLabel()
        self.lblDoorLF.setObjectName(u"lblDoorLF")
        self.lblDoorLF.setFont(font)
        self.lblDoorLF.setLayoutDirection(Qt.LeftToRight)
        self.lblDoorLF.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblDoorLF, 2, 0, 1, 1)
        self.fldDoorLF = QLineEdit()
        self.fldDoorLF.setObjectName(u"fldDoorLF")
        self.fldDoorLF.setClearButtonEnabled(True)
        self.fldDoorLF.setText(self.doorLF)
        self.gridLayout.addWidget(self.fldDoorLF, 2, 1, 1, 1)
        self.btnDoorLF = QPushButton()
        self.btnDoorLF.setObjectName(u"btnDoorLF")
        self.btnDoorLF.setFont(font)
        self.gridLayout.addWidget(self.btnDoorLF, 2, 2, 1, 2)
        self.lblDoorLB = QLabel()
        self.lblDoorLB.setObjectName(u"lblDoorLB")
        self.lblDoorLB.setFont(font)
        self.lblDoorLB.setLayoutDirection(Qt.LeftToRight)
        self.lblDoorLB.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblDoorLB, 3, 0, 1, 1)
        self.fldDoorLB = QLineEdit()
        self.fldDoorLB.setObjectName(u"fldDoorLB")
        self.fldDoorLB.setClearButtonEnabled(True)
        self.fldDoorLB.setText(self.doorLB)
        self.gridLayout.addWidget(self.fldDoorLB, 3, 1, 1, 1)
        self.btnDoorLB = QPushButton()
        self.btnDoorLB.setObjectName(u"btnDoorLB")
        self.btnDoorLB.setFont(font)
        self.gridLayout.addWidget(self.btnDoorLB, 3, 2, 1, 2)
        self.lblDoorRF = QLabel()
        self.lblDoorRF.setObjectName(u"lblDoorRF")
        self.lblDoorRF.setFont(font)
        self.lblDoorRF.setLayoutDirection(Qt.LeftToRight)
        self.lblDoorRF.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblDoorRF, 4, 0, 1, 1)
        self.fldDoorRF = QLineEdit()
        self.fldDoorRF.setObjectName(u"fldDoorRF")
        self.fldDoorRF.setClearButtonEnabled(True)
        self.fldDoorRF.setText(self.doorRF)
        self.gridLayout.addWidget(self.fldDoorRF, 4, 1, 1, 1)
        self.btnDoorRF = QPushButton()
        self.btnDoorRF.setObjectName(u"btnDoorRF")
        self.btnDoorRF.setFont(font)
        self.gridLayout.addWidget(self.btnDoorRF, 4, 2, 1, 2)
        self.lblDoorRB = QLabel()
        self.lblDoorRB.setObjectName(u"lblDoorRB")
        self.lblDoorRB.setFont(font)
        self.lblDoorRB.setLayoutDirection(Qt.LeftToRight)
        self.lblDoorRB.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblDoorRB, 5, 0, 1, 1)
        self.fldDoorRB = QLineEdit()
        self.fldDoorRB.setObjectName(u"fldDoorRB")
        self.fldDoorRB.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.fldDoorRB, 5, 1, 1, 1)
        self.fldDoorRB.setText(self.doorRB)
        self.btnDoorRB = QPushButton()
        self.btnDoorRB.setObjectName(u"btnDoorRB")
        self.btnDoorRB.setFont(font)
        self.gridLayout.addWidget(self.btnDoorRB, 5, 2, 1, 2)
        self.lblWheelLF = QLabel()
        self.lblWheelLF.setObjectName(u"lblWheelLF")
        self.lblWheelLF.setFont(font)
        self.lblWheelLF.setLayoutDirection(Qt.LeftToRight)
        self.lblWheelLF.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblWheelLF, 6, 0, 1, 1)
        self.fldWheelLF = QLineEdit()
        self.fldWheelLF.setObjectName(u"fldWheelLF")
        self.fldWheelLF.setClearButtonEnabled(True)
        self.fldWheelLF.setText(self.wheelLF)
        self.gridLayout.addWidget(self.fldWheelLF, 6, 1, 1, 1)
        self.chkWheelLF = QCheckBox()
        self.chkWheelLF.setObjectName(u"chkWheelLF")
        self.chkWheelLF.setFont(font)
        self.gridLayout.addWidget(self.chkWheelLF, 6, 2, 1, 1)
        self.btnWheelLF = QPushButton()
        self.btnWheelLF.setObjectName(u"btnWheelLF")
        self.btnWheelLF.setFont(font)
        self.gridLayout.addWidget(self.btnWheelLF, 6, 3, 1, 1)
        self.lblWheelLB = QLabel()
        self.lblWheelLB.setObjectName(u"lblWheelLB")
        self.lblWheelLB.setFont(font)
        self.lblWheelLB.setLayoutDirection(Qt.LeftToRight)
        self.lblWheelLB.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblWheelLB, 7, 0, 1, 1)
        self.fldWheelLB = QLineEdit()
        self.fldWheelLB.setObjectName(u"fldWheelLB")
        self.fldWheelLB.setClearButtonEnabled(True)
        self.fldWheelLB.setText(self.wheelLB)
        self.gridLayout.addWidget(self.fldWheelLB, 7, 1, 1, 1)
        self.chkWheelLB = QCheckBox()
        self.chkWheelLB.setObjectName(u"chkWheelLB")
        self.chkWheelLB.setFont(font)
        self.gridLayout.addWidget(self.chkWheelLB, 7, 2, 1, 1)
        self.btnWheelLB = QPushButton()
        self.btnWheelLB.setObjectName(u"btnWheelLB")
        self.btnWheelLB.setFont(font)
        self.gridLayout.addWidget(self.btnWheelLB, 7, 3, 1, 1)
        self.lblWheelRF = QLabel()
        self.lblWheelRF.setObjectName(u"lblWheelRF")
        self.lblWheelRF.setFont(font)
        self.lblWheelRF.setLayoutDirection(Qt.LeftToRight)
        self.lblWheelRF.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblWheelRF, 8, 0, 1, 1)
        self.fldWheelRF = QLineEdit()
        self.fldWheelRF.setObjectName(u"fldWheelRF")
        self.fldWheelRF.setClearButtonEnabled(True)
        self.fldWheelRF.setText(self.wheelRF)
        self.gridLayout.addWidget(self.fldWheelRF, 8, 1, 1, 1)
        self.chkWheelRF = QCheckBox()
        self.chkWheelRF.setObjectName(u"chkWheelRF")
        self.chkWheelRF.setFont(font)
        self.gridLayout.addWidget(self.chkWheelRF, 8, 2, 1, 1)
        self.btnWheelRF = QPushButton()
        self.btnWheelRF.setObjectName(u"btnWheelRF")
        self.btnWheelRF.setFont(font)
        self.gridLayout.addWidget(self.btnWheelRF, 8, 3, 1, 1)
        self.lblWheelRB = QLabel()
        self.lblWheelRB.setObjectName(u"lblWheelRB")
        self.lblWheelRB.setFont(font)
        self.lblWheelRB.setLayoutDirection(Qt.LeftToRight)
        self.lblWheelRB.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.lblWheelRB, 9, 0, 1, 1)
        self.fldWheelRB = QLineEdit()
        self.fldWheelRB.setObjectName(u"fldWheelRB")
        self.fldWheelRB.setClearButtonEnabled(True)
        self.fldWheelRB.setText(self.wheelRB)
        self.gridLayout.addWidget(self.fldWheelRB, 9, 1, 1, 1)
        self.chkWheelRB = QCheckBox()
        self.chkWheelRB.setObjectName(u"chkWheelRB")
        self.chkWheelRB.setFont(font)
        self.gridLayout.addWidget(self.chkWheelRB, 9, 2, 1, 1)
        self.btnWheelRB = QPushButton()
        self.btnWheelRB.setObjectName(u"btnWheelRB")
        self.btnWheelRB.setFont(font)
        self.gridLayout.addWidget(self.btnWheelRB, 9, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)


        self.hLine1 = QFrame()
        self.hLine1.setObjectName(u"hLine1")
        self.hLine1.setFrameShape(QFrame.HLine)
        self.hLine1.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.hLine1)


        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.btnCreateCtrl = QPushButton()
        self.btnCreateCtrl.setObjectName(u"btnCreateCtrl")
        self.btnCreateCtrl.setFont(font)
        self.buttonLayout.addWidget(self.btnCreateCtrl)
        self.btnDeleteCtrl = QPushButton()
        self.btnDeleteCtrl.setObjectName(u"btnDeleteCtrl")
        self.btnDeleteCtrl.setFont(font)
        self.buttonLayout.addWidget(self.btnDeleteCtrl)
        self.btnClose = QPushButton()
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setFont(font)
        self.buttonLayout.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi()
        self.buttonsLink()

    # UI
    def retranslateUi(self):
        self.lblRootGrp.setText(QCoreApplication.translate("Form", u"Root Grp : ", None))
        self.btnRootGrp.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblBodyGrp.setText(QCoreApplication.translate("Form", u"Body Grp : ", None))
        self.btnBodyGrp.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblDoorLF.setText(QCoreApplication.translate("Form", u"Door L F : ", None))
        self.btnDoorLF.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblDoorLB.setText(QCoreApplication.translate("Form", u"Door L B : ", None))
        self.btnDoorLB.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblDoorRF.setText(QCoreApplication.translate("Form", u"Door R F : ", None))
        self.btnDoorRF.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblDoorRB.setText(QCoreApplication.translate("Form", u"Door R B : ", None))
        self.btnDoorRB.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblWheelLF.setText(QCoreApplication.translate("Form", u"Wheel L F : ", None))
        self.chkWheelLF.setText(QCoreApplication.translate("Form", u"Auto", None))
        self.btnWheelLF.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblWheelLB.setText(QCoreApplication.translate("Form", u"Wheel L B : ", None))
        self.chkWheelLB.setText(QCoreApplication.translate("Form", u"Auto", None))
        self.btnWheelLB.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblWheelRF.setText(QCoreApplication.translate("Form", u"Wheel R F : ", None))
        self.chkWheelRF.setText(QCoreApplication.translate("Form", u"Auto", None))
        self.btnWheelRF.setText(QCoreApplication.translate("Form", u"Select", None))
        self.lblWheelRB.setText(QCoreApplication.translate("Form", u"Wheel R B : ", None))
        self.chkWheelRB.setText(QCoreApplication.translate("Form", u"Auto", None))
        self.btnWheelRB.setText(QCoreApplication.translate("Form", u"Select", None))
        self.btnCreateCtrl.setText(QCoreApplication.translate("Form", u"Create Controllers", None))
        self.btnDeleteCtrl.setText(QCoreApplication.translate("Form", u"Delete Controllers", None))
        self.btnClose.setText(QCoreApplication.translate("Form", u"Close", None))

    # UI
    def buttonsLink(self):
        self.btnRootGrp.clicked.connect(self.buttonSelect)
        self.btnBodyGrp.clicked.connect(self.buttonSelect)
        self.btnDoorLF.clicked.connect(self.buttonSelect)
        self.btnDoorLB.clicked.connect(self.buttonSelect)
        self.btnDoorRF.clicked.connect(self.buttonSelect)
        self.btnDoorRB.clicked.connect(self.buttonSelect)
        self.btnWheelLF.clicked.connect(self.buttonSelect)
        self.btnWheelLB.clicked.connect(self.buttonSelect)
        self.btnWheelRF.clicked.connect(self.buttonSelect)
        self.btnWheelRB.clicked.connect(self.buttonSelect)
        self.btnCreateCtrl.clicked.connect(self.run)
        self.btnDeleteCtrl.clicked.connect(self.deleteCtrl)
        self.btnClose.clicked.connect(self.close)

    # UI
    def buttonSelect(self):
        button = self.sender().objectName()
        replaced = button.replace("btn", "fld")
        temp = self.findChild(QLineEdit, replaced)
        isEmpty = temp.text().strip() == ""
        if not isEmpty:
            try:
                pm.select(temp.text())
            except:
                pass
        else:
            sel = pm.selected()
            if sel:
                temp.setText(sel[0].name())
            else:
                pm.warning(f"{button.strip('btn')} Field is empty.")

    # Main Process
    def run(self):
        asset = self.rootGroup.rsplit(":", 1)[-1] if self.rootGroup else ""
        createRigGroups(asset)
        self.deleteCtrl()
        self.createGlobalCtrl(self.fldRootGrp.text())
        self.createBodyCtrl(self.fldBodyGrp.text())
        self.buildDoorCtrl()
        self.buildWheelCtrl()
        self.finalTouch()

    # Sub Process - Door
    def buildDoorCtrl(self):
        result = []
        doorGroup = [
            self.fldDoorLF.text(), 
            self.fldDoorLB.text(), 
            self.fldDoorRF.text(), 
            self.fldDoorRB.text(), 
            ]
        for grp, dn in zip(doorGroup, self.doorName):
            if not grp or pm.objExists(dn):
                continue
            else:
                doorGroup = self.createDoorCtrl(grp, dn)
                result.append(doorGroup[0])
        return result

    # Sub Process - Wheel
    def buildWheelCtrl(self):
        wheelLF = self.fldWheelLF.text()
        wheelLB = self.fldWheelLB.text()
        wheelRF = self.fldWheelRF.text()
        wheelRB = self.fldWheelRB.text()
        wheelGroup = [wheelLF, wheelLB, wheelRF, wheelRB]
        chkLF = self.chkWheelLF.isChecked()
        chkLB = self.chkWheelLB.isChecked()
        chkRF = self.chkWheelRF.isChecked()
        chkRB = self.chkWheelRB.isChecked()
        checkExpr = [chkLF, chkLB, chkRF, chkRB]
        temp = ["_upDownMain", "_upDownSub", "_main", "_sub"]
        for grp, wn, chk in zip(wheelGroup, self.wheelName, checkExpr):
            if not grp or any([pm.objExists(wn + i) for i in temp]):
                continue
            else:
                createdWheelGrp = self.createWheelCtrl(grp, wn)
                if chk:
                    exprGroup = self.createWheelExpressionGroups(wn)
                    self.createWheelExpression(createdWheelGrp, exprGroup)
                    pm.parent(createdWheelGrp[0], exprGroup[1])
                else:
                    pm.parent(createdWheelGrp[0], "controllers")
        self.connectWheels()

    # Door
    def createDoorCtrl(self, objectGroup: str, doorName: str) -> list:
        """ Create a door controller. 
        - When the doorName contains the word "Right", "right", "_R", 
            - set the group's rotateX to -180 in the YZ plane.
        - When the doorName contains the word "Back", "back", "Bk",
            - the door controller shape changes to door2 type.

        Examples: 
        >>> createDoorCtrl("bestaB_body_door_Ft_L_grp", "cc_door_L_Ft")
        >>> ["cc_door_L_Ft_grp", ..., "cc_door_L_Ft", "loc_door_L_Ft"]
        >>> createDoorCtrl("bestaB_body_door_Ft_L_grp", "cc_door_R_Bk")
        >>> ["cc_door_R_Bk_grp", ..., "cc_door_R_Bk", "loc_door_R_Bk"]
        """
        defaultScale = 58
        Back = "Back" in doorName
        back = "back" in doorName
        Bk = "Bk" in doorName
        Right = "Right" in doorName
        right = "right" in doorName
        _R = "_R" in doorName
        _rt = "_rt" in doorName
        doorType = "door1" if any([Back, back, Bk]) else "door"
        ctrls = Controllers().createControllers(**{doorType: doorName})
        ctrl = ctrls[0]
        doorSize = max(getBoundingBoxSize(objectGroup)) / defaultScale
        pm.scale(ctrl, [doorSize, doorSize, doorSize])
        pm.matchTransform(ctrl, objectGroup, pos=True, rot=True)
        doorGroup = groupOwnPivot(ctrl, null=True)
        if any([Right, right, _R, _rt]):
            pm.setAttr(f"{ctrl}.rotateX", -180)
            pm.setAttr(f"{doorGroup[0]}.rotateX", -180)
        pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
        loc = createSubLocator(doorGroup[-1])
        doorGroup.append(loc)
        pm.transformLimits(doorGroup[2], ry=(-60, 0), ery=(False, True))
        pm.parentConstraint(loc, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(loc, objectGroup, mo=True, w=1.0)
        return doorGroup

    # Wheel
    def createWheelCtrl(self, objectGroup: str, ctrlName: str) -> list:
        """ Create a wheel controller.

        Examples: 
        >>> createWheelCtrl("pCylinder", "cc_wheelLeftFront")
        >>> ['cc_wheelLeftFront_upDownMain_grp', ...]
        """
        ctrls = [
            f"{ctrlName}_upDownMain", 
            f"{ctrlName}_upDownSub", 
            f"{ctrlName}_main", 
            f"{ctrlName}_sub"
        ]
        if any([pm.objExists(i) for i in ctrls]):
            return
        sizeRatio = [14, 18, 9, 11]
        cc = Controllers()
        rad = max(getBoundingBoxSize(objectGroup))
        for ctrlName, sr in zip(ctrls[:2], sizeRatio[:2]):
            cuv = cc.createControllers(square=ctrlName)[0]
            pm.scale(cuv, (rad/(sr*2), rad/sr, rad/sr))
            pm.matchTransform(cuv, objectGroup, pos=True)
            pm.setAttr(f"{cuv}.translateY", 0)
        for ctrlName, sr in zip(ctrls[2:], sizeRatio[2:]):
            cuv = cc.createControllers(circle=ctrlName)[0]
            pm.scale(cuv, (rad/sr, rad/sr, rad/sr))
            pm.rotate(cuv, (0, 0, 90))
            pm.matchTransform(cuv, objectGroup, pos=True)
        ccGrp = groupOwnPivot(*ctrls, null=True)
        parentHierarchically(*ccGrp)
        pm.makeIdentity(ccGrp, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccMain = ctrls[2]
        pm.addAttr(ccMain, ln="Radius", at="double", min=0.0001, dv=1)
        pm.setAttr(f"{ccMain}.Radius", e=True, k=True)
        pm.setAttr(f"{ccMain}.Radius", rad)
        locator = createSubLocator(ctrls[-1])
        ccGrp.append(locator)
        pm.parentConstraint(locator, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(locator, objectGroup, mo=True, w=1.0)
        return ccGrp

    # Wheel2
    def createWheelExpressionGroups(self, ctrlName: str) -> list:
        """ Create groups for the expression. 

        Examples: 
        >>> createWheelExpressionGroups("cc_wheelLeftFront")
        >>> grpNames = [
            "cc_wheelLeftFront_grp", 
            "cc_wheelLeftFront_offset", 
            "cc_wheelLeftFront_offsetNull", 
            "cc_wheelLeftFront_offsetPrevious", 
            "cc_wheelLeftFront_offsetOrient", 
            ]
         """
        grpNames = [
            f"{ctrlName}_grp", 
            f"{ctrlName}_offset", 
            f"{ctrlName}_offsetNull", 
            f"{ctrlName}_offsetPrevious", 
            f"{ctrlName}_offsetOrient"
            ]
        result = [pm.group(n=i, em=True) for i in grpNames]
        grp, offset, offsetNull, offsetPrevious, offsetOrient = result
        pm.parent(offset, grp)
        pm.parent(offsetNull, offset)
        pm.parent(offsetPrevious, grp)
        pm.parent(offsetOrient, offsetPrevious)
        offsetOrient.translate.set([-0.001, -0.001, -0.001])
        pm.aimConstraint(offset, offsetPrevious, mo=False)
        pm.orientConstraint(offsetNull, offsetOrient, mo=False)
        for i in ['X', 'Y', 'Z']:
            pm.addAttr(offset, ln=f'PreviousPosition{i}', at='double', dv=0)
            pm.setAttr(f'{offset}.PreviousPosition{i}', e=True, k=True)
        return result

    # Wheel3
    def createWheelExpression(self, wheelGrp: list, exprGrp: list) -> None:
        """ Rotate the locator by the moving distance of offset_grp.

        Args: 
        -----
        >>> wheelGrp = [
            'cc_wheelLeftFront_upDownMain_grp', 
            'cc_wheelLeftFront_upDownMain_null', 
            'cc_wheelLeftFront_upDownMain', 
            'cc_wheelLeftFront_upDownSub_grp', 
            'cc_wheelLeftFront_upDownSub_null', 
            'cc_wheelLeftFront_upDownSub', 
            'cc_wheelLeftFront_main_grp', 
            'cc_wheelLeftFront_main_null', 
            'cc_wheelLeftFront_main', 
            'cc_wheelLeftFront_sub_grp', 
            'cc_wheelLeftFront_sub_null', 
            'cc_wheelLeftFront_sub', 
            'loc_wheelLeftFront_sub', 
            ]
        >>> exprGrp = [
            "cc_wheelLeftFront_grp", 
            "cc_wheelLeftFront_offset", 
            "cc_wheelLeftFront_offsetNull", 
            "cc_wheelLeftFront_offsetPrevious", 
            "cc_wheelLeftFront_offsetOrient", 
            ]
        
        Return: 
        -------
        >>> exprGrp = [
            "cc_wheelLeftFront_grp", 
            "cc_wheelLeftFront_offset", 
            "cc_wheelLeftFront_offsetNull", 
            "cc_wheelLeftFront_offsetPrevious", 
            "cc_wheelLeftFront_offsetOrient", 
            ]
        """
        firstGroup = wheelGrp[0]
        ctrlMain = wheelGrp[8]
        locator = wheelGrp[-1]
        if not pm.attributeQuery("AutoRoll", node=ctrlMain, ex=True):
            attrAuto = 'AutoRoll'
            pm.addAttr(ctrlMain, ln=attrAuto, at='long', min=0, max=1, dv=1)
            pm.setAttr(f'{ctrlMain}.{attrAuto}', e=True, k=True)
        br = '\n'
        offset = exprGrp[1]
        previous, orient = exprGrp[3:]
        pm.parent(firstGroup, offset)
        # expression1
        expr1 = f'float $rad = {ctrlMain}.Radius;{br}'
        expr1 += f'float $auto = {ctrlMain}.AutoRoll;{br}'
        expr1 += f'float $locator = {locator}.rotateX;{br}'
        expr1 += f'float $circleLength = 2 * 3.141 * $rad;{br}'
        expr1 += f'float $orientRotY = {orient}.rotateY;{br}'
        expr1 += f'float $offsetScale = {offset}.scaleY;{br}'
        expr1 += f'float $pointX1 = {offset}.PreviousPositionX;{br}'
        expr1 += f'float $pointY1 = {offset}.PreviousPositionY;{br}'
        expr1 += f'float $pointZ1 = {offset}.PreviousPositionZ;{br}'
        expr1 += f'{previous}.translateX = $pointX1;{br}'
        expr1 += f'{previous}.translateY = $pointY1;{br}'
        expr1 += f'{previous}.translateZ = $pointZ1;{br}'
        expr1 += f'float $pointX2 = {offset}.translateX;{br}'
        expr1 += f'float $pointY2 = {offset}.translateY;{br}'
        expr1 += f'float $pointZ2 = {offset}.translateZ;{br*2}'
        # expression2
        pointsGap = '$pointX2-$pointX1, $pointY2-$pointY1, $pointZ2-$pointZ1'
        expr2 = f'float $distance = `mag<<{pointsGap}>>`;{br*2}'
        # expression3
        expr3 = f'{locator}.rotateX = $locator'
        expr3 += ' + ($distance/$circleLength) * 360'
        expr3 += ' * $auto'
        expr3 += ' * 1'
        expr3 += ' * sin(deg_to_rad($orientRotY))'
        expr3 += f' / $offsetScale;{br*2}'
        # expression4
        expr4 = f'{offset}.PreviousPositionX = $pointX2;{br}'
        expr4 += f'{offset}.PreviousPositionY = $pointY2;{br}'
        expr4 += f'{offset}.PreviousPositionZ = $pointZ2;{br}'
        # final expression
        expr = expr1 + expr2 + expr3 + expr4
        pm.expression(s=expr, o='', ae=1, uc='all')

    # Wheel4
    def connectWheels(self):
        """ Connect the rotateX of the wheels.

        Descriptions
        ------------
        - When an expression is applied to one wheel,
            - LF -> LB, RF, RB
        - When an expression is applied to two wheels,
            - LF -> RF / LB -> RB
            - LF -> LB / RF -> RB
            - LF -> RF / RB -> LB
            - LB -> LF / RF -> RB
            - LB -> LF / RB -> RF
            - RF -> LF / RB -> LB
        - When an expression is applied to three wheels,
            - RF -> LF
            - RB -> LB
            - LF -> RF
            - LB -> RB
         """
        chkLF = self.chkWheelLF.isChecked()
        chkLB = self.chkWheelLB.isChecked()
        chkRF = self.chkWheelRF.isChecked()
        chkRB = self.chkWheelRB.isChecked()
        checkExpr = [chkLF, chkLB, chkRF, chkRB]
        locLF = "loc_wheelLeftFront_sub"
        locLB = "loc_wheelLeftBack_sub"
        locRF = "loc_wheelRightFront_sub"
        locRB = "loc_wheelRightBack_sub"
        locators = [locLF, locLB, locRF, locRB]
        if checkExpr.count(True) == 0:
            pass
        elif checkExpr.count(True) == 1:
            tmp = [loc for chk, loc in zip(checkExpr, locators) if not chk]
            src = [loc for chk, loc in zip(checkExpr, locators) if chk][0]
            for i in tmp:
                pm.connectAttr(f"{src}.rotateX", f"{i}.rotateX", f=True)
        elif checkExpr.count(True) == 2:
            if chkLF and chkLB:
                src = [locLF, locLB]
                des = [locRF, locRB]
            elif chkLF and chkRF:
                src = [locLF, locRF]
                des = [locLB, locRB]
            elif chkLF and chkRB:
                src = [locLF, locRB]
                des = [locRF, locLB]
            elif chkLB and chkRF:
                src = [locLB, locRF]
                des = [locLF, locRB]
            elif chkLB and chkRB:
                src = [locLB, locRB]
                des = [locLF, locRF]
            else:
                src = [locRF, locRB]
                des = [locLF, locLB]
            for s, d in zip(src, des):
                pm.connectAttr(f"{s}.rotateX", f"{d}.rotateX", f=True)
        elif checkExpr.count(True) == 3:
            if not chkLF:
                src = locRF
                des = locLF
            elif not chkLB:
                src = locRB
                des = locLB
            elif not chkRF:
                src = locLF
                des = locRF
            else:
                src = locLB
                des = locRB
            pm.connectAttr(f"{src}.rotateX", f"{des}.rotateX", f=True)
        else:
            pass


    def deleteCtrl(self):
        """ Try to delete what is in Delete list. 

        Delete List
        -----------
        - "cc_main_grp", 
        - "cc_body_grp", 
        - "cc_doorLeftFront_grp", 
        - "cc_doorLeftBack_grp", 
        - "cc_doorRightFront_grp", 
        - "cc_doorRightBack_grp", 
        - "cc_wheelLeftFront_grp", 
        - "cc_wheelLeftFront_upDownMain_grp", 
        - "cc_wheelLeftBack_grp", 
        - "cc_wheelLeftBack_upDownMain_grp", 
        - "cc_wheelRightFront_grp", 
        - "cc_wheelRightFront_upDownMain_grp", 
        - "cc_wheelRightBack_grp", 
        - "cc_wheelRightBack_upDownMain_grp", 
         """
        try:
            pm.parent(self.fldRootGrp.text(), w=True)
        except:
            pass
        for i in self.deleteName:
            try:
                pm.delete(i)
            except:
                continue


    def createGlobalCtrl(self, objectGroup: str) -> list:
        """ Create a global controller. 
        Take the Arguments that can be used to estimate 
        the overall size of the model.

        Examples: 
        >>> createGlobalCtrl("vhcl_bestaB_mdl_v9999:bestaB_body_grp")
        >>> ["cc_main_grp", "cc_main", "cc_sub_grp", "cc_sub"]
        """
        ccMain = "cc_main"
        ccSub = "cc_sub"
        if pm.objExists(ccMain) or pm.objExists(ccSub):
            return
        a, b, c = getBoundingBoxSize(objectGroup)
        x, y, z = 100, 100, 250
        cc = Controllers()
        ccs = cc.createControllers(car2=ccMain, car1=ccSub)
        for i in ccs:
            pm.scale(i, [a/x, b/y, c/z])
            pm.makeIdentity(i, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccsGroup = groupOwnPivot(*ccs)
        result = parentHierarchically(*ccsGroup)
        locator = createSubLocator(ccs[-1])
        result.append(locator)
        pm.parentConstraint(ccSub, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(ccSub, objectGroup, mo=True, w=1.0)
        return result


    def createBodyCtrl(self, objectGroup: str) -> list:
        """ Create the Body Controller. 
        Take the Arguments that can be used to estimate 
        the overall size of the body.

        Examples: 
        >>> createBodyCtrl("body")
        >>> ['cc_body_grp', 'cc_body_null', 'cc_body', 'loc_body']
        """
        ccBody = "cc_body"
        if pm.objExists(ccBody):
            return
        defaultScale = 240
        bodySize = max(getBoundingBoxSize(objectGroup)) / defaultScale
        cc = Controllers()
        ctrl = cc.createControllers(car=ccBody)
        pm.scale(ctrl, [bodySize, bodySize, bodySize])
        pm.makeIdentity(ctrl, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.matchTransform(ctrl, objectGroup, pos=True, rot=True)
        bodyGroups = groupOwnPivot(ctrl[0], null=True)
        locator = createSubLocator(ctrl[0])
        bodyGroups.append(locator)
        pm.parentConstraint(locator, objectGroup, mo=True, w=1.0)
        pm.scaleConstraint(locator, objectGroup, mo=True, w=1.0)
        return bodyGroups


    def finalTouch(self):
        """ Final Touch. 

        Descriptions
        ------------
        - try to [Parent] what is in self.groupHierarchy list.
            - MODEL <- referenced group
            - controllers <- cc_main_grp
            - controllers <- cc_wheelLeftFront_grp
            - controllers <- cc_wheelLeftBack_grp
            - controllers <- cc_wheelRightFront_grp
            - controllers <- cc_wheelRightBack_grp
            - cc_sub <- cc_body_grp
            - cc_body <- cc_doorLeftFront_grp
            - cc_body <- cc_doorLeftBack_grp
            - cc_body <- cc_doorRightFront_grp
            - cc_body <- cc_doorRightBack_grp
        - try to [Constraint] what is in wheelGroups.
            - cc_sub <- cc_wheelLeftFront_offset 
            - cc_sub <- cc_wheelLeftFront_upDownMain_grp 
            - cc_sub <- cc_wheelLeftBack_offset 
            - cc_sub <- cc_wheelLeftBack_upDownMain_grp 
            - cc_sub <- cc_wheelRightFront_offset 
            - cc_sub <- cc_wheelRightFront_upDownMain_grp 
            - cc_sub <- cc_wheelRightBack_offset 
            - cc_sub <- cc_wheelRightBack_upDownMain_grp 
        - Add Attributes and Connect
            - cc_main -> cc_main.Geo -> MODEL.visibility
        - Hide Locators
            - loc_sub
            - loc_body
            - loc_doorLeftFront
            - loc_doorLeftBack
            - loc_doorRightFront
            - loc_doorRightBack
            - loc_wheelLeftFront_sub
            - loc_wheelLeftBack_sub
            - loc_wheelRightFront_sub
            - loc_wheelRightBack_sub
         """
        ccMain = "cc_main"
        ccSub = "cc_sub"
        wheelGroups = [
            "cc_wheelLeftFront_offset", 
            "cc_wheelLeftFront_upDownMain_grp", 
            "cc_wheelLeftBack_offset", 
            "cc_wheelLeftBack_upDownMain_grp", 
            "cc_wheelRightFront_offset", 
            "cc_wheelRightFront_upDownMain_grp", 
            "cc_wheelRightBack_offset", 
            "cc_wheelRightBack_upDownMain_grp", 
            ]
        # Try to parent
        try:
            pm.parent(self.fldRootGrp.text(), "MODEL")
        except:
            pass
        for parents, children in self.groupHierarchy.items():
            for child in children:
                try:
                    pm.parent(child, parents)
                except:
                    continue
        # Try to constraint
        for i in wheelGroups:
            try:
                pm.parentConstraint(ccSub, i, mo=True, w=1.0)
                pm.scaleConstraint(ccSub, i, mo=True, w=1.0)
            except:
                continue
        self.setColor()
        # Add attributes to main controller.
        geo = "Geo"
        pm.addAttr(ccMain, ln=geo, at="bool", dv=1)
        pm.setAttr(f'{ccMain}.{geo}', e=True, k=True)
        pm.connectAttr(f"{ccMain}.{geo}", "MODEL.visibility", f=True)
        # Hide Locators
        for i in self.locators:
            try:
                pm.setAttr(f"{i}.visibility", 0)
            except:
                continue


    def setColor(self):
        """ Try to colorize what is in self.colorBar. """
        for cc, color in self.colorBar.items():
            try:
                temp = {color: True}
                colorize(cc, **temp)
            except:
                continue


# if __name__ == "__main__":
#     try:
#         qrc.close()
#         qrc.deleteLater()
#     except:
#         pass
#     qrc = QuickRig_Car()
#     qrc.show()

