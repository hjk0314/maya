from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
# from functools import partial
from general import *
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Car(QWidget):
    def __init__(self):
        self.topGroup = ""
        self.rootJnt = "jnt_root"
        self.rootFbx = "fbx_root"
        self.mainCtrl = "cc_main"
        self.ctrlNames = {
            "car": "cc_body", 
            "car2": "cc_sub", 
            "circle": "cc_main", 
            }
        self.jntNameAndPos = {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_bodyEnd": (0, 145, 0), 
            "jnt_wheelLeftFront": (70, 30, 140), 
            "jnt_wheelLeftFrontEnd": (85, 30, 140), 
            "jnt_wheelRightFront": (-70, 30, 140), 
            "jnt_wheelRightFrontEnd": (-85, 30, 140), 
            "jnt_wheelLeftRear": (70, 30, -140), 
            "jnt_wheelLeftRearEnd": (85, 30, -140), 
            "jnt_wheelRightRear": (-70, 30, -140), 
            "jnt_wheelRightRearEnd": (-85, 30, -140), 
            }
        self.hierarchy = {
            "jnt_root": [
                [f"jnt_body{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightFront{i}" for i in ["", "End"]], 
                [f"jnt_wheelLeftRear{i}" for i in ["", "End"]], 
                [f"jnt_wheelRightRear{i}" for i in ["", "End"]], 
                ], 
            }
        super(Car, self).__init__()
        self.sortCount = 0
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUI()
    

    def setupUI(self):
        self.setWindowTitle("quickRig_car")
        self.move(0, 0)
        self.resize(250, 500)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fldCarName = QLineEdit()
        self.fldCarName.setClearButtonEnabled(True)
        self.fldCarName.setPlaceholderText("Input your car name")
        self.verticalLayout.addWidget(self.fldCarName)
        self.btnCarGrp = QPushButton("Car group")
        self.verticalLayout.addWidget(self.btnCarGrp)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.btnTempJnt = QPushButton("Create temp joints")
        self.verticalLayout.addWidget(self.btnTempJnt)
        self.horizontalLayout = QHBoxLayout()
        self.btnLtoR = QPushButton("Left To Right")
        self.horizontalLayout.addWidget(self.btnLtoR)
        self.btnRtoL = QPushButton("Right To Left")
        self.horizontalLayout.addWidget(self.btnRtoL)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.btnBuild = QPushButton("Build")
        self.verticalLayout.addWidget(self.btnBuild)
        self.btnCleanUp = QPushButton("Clean Up")
        self.verticalLayout.addWidget(self.btnCleanUp)
        self.line_5 = QFrame()
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_5)
        self.fldSelectWheel = QLineEdit()
        self.fldSelectWheel.setEnabled(True)
        self.fldSelectWheel.setPlaceholderText("Input Ctrl's Name or Click below")
        self.fldSelectWheel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.fldSelectWheel)

        self.gridLayout_4 = QGridLayout()
        self.btnLeftFront = QPushButton("Left Front")
        self.gridLayout_4.addWidget(self.btnLeftFront, 0, 0, 1, 1)
        self.btnRightFront = QPushButton("Right Front")
        self.gridLayout_4.addWidget(self.btnRightFront, 0, 1, 1, 1)
        self.btnLeftRear = QPushButton("Left Rear")
        self.gridLayout_4.addWidget(self.btnLeftRear, 2, 0, 1, 1)
        self.btnRightRear = QPushButton("Right Rear")
        self.gridLayout_4.addWidget(self.btnRightRear, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)

        self.btnCreateWheel = QPushButton("Create Wheel")
        self.verticalLayout.addWidget(self.btnCreateWheel)
        self.btnWheelCleanUp = QPushButton("Clean Up")
        self.verticalLayout.addWidget(self.btnWheelCleanUp)

        self.gridLayout_5 = QGridLayout()
        self.btnSetExpr = QPushButton("Set Expression")
        self.gridLayout_5.addWidget(self.btnSetExpr, 0, 0, 1, 1)
        self.btnDelExpr = QPushButton("Del Expression")
        self.gridLayout_5.addWidget(self.btnDelExpr, 0, 1, 1, 1)
        self.btnSetPressure = QPushButton("Set Pressure")
        self.gridLayout_5.addWidget(self.btnSetPressure, 2, 0, 1, 1)
        self.btnDelPressure = QPushButton("Del Pressure")
        self.gridLayout_5.addWidget(self.btnDelPressure, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)


        self.line_3 = QFrame()
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_3)

        self.btnConnection = QPushButton("Joint Connection")
        self.verticalLayout.addWidget(self.btnConnection)
        self.btnDisconnection = QPushButton("Disconnection")
        self.verticalLayout.addWidget(self.btnDisconnection)

        self.line_4 = QFrame()
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_4)

        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # Buttons Links
        self.buttonsLink()


    def buttonsLink(self):
        self.fldCarName.returnPressed.connect(self.createGroups)
        self.btnCarGrp.clicked.connect(self.createGroups)
        self.btnTempJnt.clicked.connect(self.createJoints)
        self.btnLtoR.clicked.connect(self.buildSymmetry)
        self.btnRtoL.clicked.connect(self.buildSymmetry)
        self.btnBuild.clicked.connect(self.build)
        self.btnCleanUp.clicked.connect(self.cleanUp)
        self.btnLeftFront.clicked.connect(self.setWheelName)
        self.btnRightFront.clicked.connect(self.setWheelName)
        self.btnLeftRear.clicked.connect(self.setWheelName)
        self.btnRightRear.clicked.connect(self.setWheelName)
        self.btnCreateWheel.clicked.connect(self.buildWheels)

        self.btnClose.clicked.connect(self.close)


    def build(self):
        self.updateJointsPosition()
        self.cleanUp()
        self.createGroups()
        self.createJoints()
        self.createFbxJoints()
        self.createCtrls()


    def buildSymmetry(self):
        button = self.sender()
        buttonName = button.text()
        buttonName = buttonName.replace(" ", "")
        self.updateJointsPosition()
        self.updateSameSide(buttonName)
        self.cleanUp()
        self.createJoints()


    def buildWheels(self):
        ctrl = self.fldSelectWheel.text()
        obj = selectObjectOnly()[0]
        if not ctrl:
            pm.warning("Input your Controller's name.")
            return
        if not obj:
            pm.warning("Select the polygonal mesh of the wheel.")
            return
        self.createWheelGroups(ctrl)
        loc = self.createRotationLocator(ctrl, obj)
        self.createWheelCtrl(loc, ctrl, obj)


    def updateJointsPosition(self):
        for jnt in self.jntNameAndPos.keys():
            try:
                pos = getPosition(jnt)
                self.jntNameAndPos[jnt] = pos
            except:
                continue


    def updateSameSide(self, side: str="LeftToRight"):
        """ The default change is from left to right. 
        But the opposite is also possible.
        >>> updateSameSide()
        >>> updateSameSide("RightToLeft")
         """
        A, B = side.split("To")
        aSide = []
        bSide = []
        for jntName in self.jntNameAndPos.keys():
            if A in jntName:
                aSide.append(jntName)
            elif B in jntName:
                bSide.append(jntName)
            else:
                continue
        for idx, aJoint in enumerate(aSide):
            x, y, z = pm.xform(aJoint, q=True, t=True, ws=True)
            bJoint = bSide[idx]
            self.jntNameAndPos[bJoint] = (-1*x, y, z)


    def cleanUp(self):
        listDelete = [
            self.topGroup, 
            self.rootJnt, 
            self.rootFbx, 
            self.mainCtrl + "_grp", 
            ]
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue


    def createGroups(self):
        carName = self.fldCarName.text()
        if self.topGroup == carName:
            grpName = carName
        elif self.topGroup != "" and carName == "":
            grpName = self.topGroup
        else:
            grpName = carName
            self.topGroup = carName
        rg = RigGroups()
        rg.createRigGroups(grpName)
        self.fldCarName.setText(grpName)
        self.fldCarName.clearFocus()


    def createJoints(self):
        for jnt, pos in self.jntNameAndPos.items():
            if pm.objExists(jnt):
                continue
            else:
                pm.select(cl=True)
                pm.joint(p=pos, n=jnt)
        for parents, childList in self.hierarchy.items():
            for children in childList:
                parentHierarchically(*children)
                pm.makeIdentity(children, a=1, t=1, r=1, s=1, jo=1)
                pm.parent(children[0], parents)
        self.tryParent(self.rootJnt, "bindBones")


    def createFbxJoints(self):
        fbx = pm.duplicate(self.rootJnt, rr=True, n=self.rootFbx)
        fbx = fbx[0]
        pm.select(cl=True)
        pm.select(fbx, hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("jnt_", "fbx_")
            pm.rename(i, new)
        self.tryParent(self.rootFbx, "rigBones")


    def createCtrls(self):
        cc = Controllers()
        cc.createControllers(**self.ctrlNames)
        ctrl = list(self.ctrlNames.values())
        grps = []
        for i in ctrl:
            if self.mainCtrl == i:
                pm.scale(i, (20, 20, 20))
                pm.makeIdentity(i, a=1, t=0, r=0, s=1, n=0, pn=1)
            grp = groupingWithOwnPivot(i)[0]
            grps.append(grp)
        for child, parents in zip(grps[:2], ctrl[1:]):
            pm.parent(child, parents)
        pm.matchTransform(grps[0], "jnt_body", pos=True)
        self.tryParent(self.mainCtrl + "_grp", "controllers")
        

    def tryParent(self, child: str, parents: str):
        try:
            pm.parent(child, parents)
        except:
            pass


    def setWheelName(self):
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_wheel%s" % buttonName.replace(" ", "")
        self.fldSelectWheel.setText(ctrlName)
        self.fldSelectWheel.clearFocus()


    def createWheelGroups(self, ctrl):
        grpNames = [
            f"{ctrl}_grp", 
            f"{ctrl}_offset", 
            f"{ctrl}_offsetNull", 
            f"{ctrl}_offsetPrevious", 
            f"{ctrl}_offsetOrient"
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


    def createWheelCtrl(self, obj, ccName, parentsGroup="") -> str:
        cc = [
            f"{ccName}_upDownMain", 
            f"{ccName}_upDownSub", 
            f"{ccName}_Main", 
            f"{ccName}_Sub"
        ]
        ccType = ["square", "square", "circle", "circle"]
        temp = {key: value for key, value in zip(ccType, cc)}
        ctrl = Controllers()
        ctrlName = ctrl.createControllers(temp)
        ccGrp = []
        sizeRatio = [14, 18, 9, 11]
        rad = getBoundingBoxSize(obj)
        for ccName, sr in zip(cc[:2], sizeRatio[:2]):
            cuv = ctrl.createControllers(square=ccName)[0]
            pm.scale(cuv, (rad/(sr*2), rad/sr, rad/sr))
            pm.matchTransform(cuv, obj, pos=True)
            pm.setAttr(f"{cuv}.translateY", 0)
        for ccName, sr in zip(cc[2:], sizeRatio[2:]):
            cuv = ctrl.createControllers(circle=ccName)[0]
            pm.scale(cuv, (rad/sr, rad/sr, rad/sr))
            pm.rotate(cuv, (0, 0, 90))
            pm.matchTransform(cuv, obj, pos=True)
        for i in cc:
            pm.makeIdentity(i, a=1, t=0, r=1, s=1, n=0, pn=1)
            cuvGrp = groupingWithOwnPivot(i)[0]
            ccGrp.append(cuvGrp)
        for parents, child in zip(cc[:3], ccGrp[1:]):
            parentHierarchically(parents, child)
        ccSub = cc[-1]
        ccUpDownMainGrp = ccGrp[0]
        if pm.objExists(parentsGroup):
            parentHierarchically(parentsGroup, ccUpDownMainGrp)
        # Create wheel controllers channel.
        attrRad = "Radius"
        pm.addAttr(ccSub, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ccSub}.{attrRad}', e=True, k=True)
        attrAuto = 'AutoRoll'
        pm.addAttr(ccSub, ln=attrAuto, at='long', min=0, max=1, dv=1)
        pm.setAttr(f'{ccSub}.{attrAuto}', e=True, k=True)
        pm.setAttr(f"{ccSub}.Radius", rad)
        return ccSub


    def createRotationLocator(self, ctrl, obj):
        if "cc_" in ctrl:
            locName = ctrl.replace("cc_", "loc_")
        else:
            locName = f"{ctrl}_%s" % "exprLocator"
        locator = pm.spaceLocator(n=locName)
        pm.matchTransform(locator, obj, pos=True)
        return locator


    def createExpression(self, ctrl: str, locator: str, names: list) -> None:
        br = '\n'
        offset = names[1]
        previous, orient = names[3:]
        # expression1
        expr1 = f'float $rad = {ctrl}.Radius;{br}'
        expr1 += f'float $auto = {ctrl}.AutoRoll;{br}'
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


# if __name__ == "__main__":
#     try:
#         qrCar.close()
#         qrCar.deleteLater()
#     except:
#         pass
#     qrCar = Car()
#     qrCar.show()


# car = Car()
# obj = "jaguarA_down_tire_Ft_L_tire_rubber_1"
# ctrl = "cc_wheelLeftFront"
# grpNames = car.createWheelGroups(ctrl)
# ccSub = car.createWheelCtrl(obj, ctrl, grpNames[1])
# locator = car.createRotationLocator(ccSub)
# car.createExpression(ccSub, locator, grpNames)


