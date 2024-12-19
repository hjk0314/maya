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
        self.bodyPosition = []
        self.wheelPosition = []
        self.doorPosition = []
        self.rootJnt = "jnt_root"
        self.rootFbx = "fbx_root"
        # self.bodyJnt = "jnt_body"
        # self.bodyFbx = "fbx_body"
        # self.mainCtrl = "cc_main"
        # self.subCtrl = "cc_sub"
        # self.doorCtrls = []
        # self.doorJoints = []
        self.jntNameAndPos = {
            "jnt_root": (0, 15, 0), 
            "jnt_body": (0, 45, 0), 
            "jnt_bodyEnd": (0, 145, 0), 
            }
        self.hierarchy = {
            "jnt_root": [["jnt_body", "jnt_bodyEnd"], ], 
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
        self.btnSetPressure.setEnabled(False)
        self.gridLayout_expression.addWidget(self.btnSetPressure, 1, 0, 1, 1)
        self.btnDelPressure = QPushButton("Del Pressure")
        self.btnDelPressure.setEnabled(False)
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
        self.btnFrontDoor = QPushButton("Left Front")
        self.gridLayout_doorName.addWidget(self.btnFrontDoor, 0, 0, 1, 1)
        self.btnBackDoor = QPushButton("Left Back")
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

        self.btnLeftFront.clicked.connect(self.setWheelName)
        self.btnLeftBack.clicked.connect(self.setWheelName)
        self.btnRightFront.clicked.connect(self.setWheelName)
        self.btnRightBack.clicked.connect(self.setWheelName)
        self.btnCreateWheel.clicked.connect(self.build_wheels)
        self.btnSetExpr.clicked.connect(self.build_expression)
        self.btnDelExpr.clicked.connect(self.delete_expression)
        self.btnDelWheel.clicked.connect(self.delete_wheel)

        self.btnFrontDoor.clicked.connect(self.setDoorName)
        self.btnBackDoor.clicked.connect(self.setDoorName)
        self.btnCreateDoor.clicked.connect(self.build_doors)
        self.btnDelDoor.clicked.connect(self.delete_door)

        self.btnCreateJnt.clicked.connect(self.build_joints)

        self.btnClose.clicked.connect(self.close)


    def build_joints(self):
        # print(self.topGroup)
        # print(self.objGroup)
        # print(self.bodyPosition)
        print(self.wheelPosition)
        # print(self.doorPosition)

        self.deleteJoints()
        self.setBodyJointPosition()
        self.setWheelJointPosition()
        self.createJoints()

        # self.updateJointsPosition()
        # self.createCarGroup()
        # self.createFbxJoints()
        # self.createMainCtrl()


    def deleteJoints(self):
        """ Clean up the joint groups. """
        listDelete = [
            self.rootJnt, 
            self.rootFbx, 
            ]
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue


    def setBodyJointPosition(self):
        if not self.wheelPosition:
            return
        wheelHeights = [getPosition(i)[1] for i in self.wheelPosition]
        heightsAverage = sum(wheelHeights) / len(wheelHeights)
        halfHeights = heightsAverage / 2.0
        jnt_root = (0, heightsAverage - halfHeights, 0)
        jnt_body = (0, heightsAverage + halfHeights, 0)
        jnt_bodyEnd = (0, heightsAverage + halfHeights + 100, 0)
        self.jntNameAndPos["jnt_root"] = jnt_root
        self.jntNameAndPos["jnt_body"] = jnt_body
        self.jntNameAndPos["jnt_bodyEnd"] = jnt_bodyEnd


    def setWheelJointPosition(self):
        if not self.wheelPosition:
            return
        temp = []
        for i in self.wheelPosition:
            x, y, z = getPosition(i)
            jnt = i.replace("loc_", "jnt_")
            self.jntNameAndPos[jnt] = (x, y, z)
            if "right" in jnt or "Right" in jnt or "_R" in jnt:
                self.jntNameAndPos[f"{jnt}End"] = (x - 15, y, z)
            else:
                self.jntNameAndPos[f"{jnt}End"] = (x + 15, y, z)
            temp.append([jnt, f"{jnt}End"])
        result = self.hierarchy["jnt_root"] + temp
        self.hierarchy["jnt_root"] = result


    def createJoints(self):
        for jnt, pos in self.jntNameAndPos.items():
            if pm.objExists(jnt):
                pm.delete(jnt)
            else:
                pm.select(cl=True)
                pm.joint(p=pos, n=jnt)
        for parents, childList in self.hierarchy.items():
            for children in childList:
                parentHierarchically(*children)
                pm.makeIdentity(children, a=1, t=1, r=1, s=1, jo=1)
                pm.parent(children[0], parents)


    def build_wheels(self):
        """ Create a wheel controller only.
        There is no expression for turning the wheel.
         """
        ctrlName = self.lineWheelName.text()
        obj = selectObjectOnly()
        if not ctrlName:
            pm.warning("Input your Controller's name.")
            return
        if not obj:
            pm.warning("Select the polygon of the wheel.")
            return
        if pm.objExists(f"{ctrlName}_main"):
            pm.warning(f"{ctrlName}_main ctrl aleady exists.")
            return
        self.createWheelCtrl(ctrlName, obj)
        locator = self.createWheelRotationLocator(ctrlName)
        self.insertPositionList(self.wheelPosition, locator)


    def build_expression(self):
        """ Add an expression to the wheel controller.
        Rotate the locator by calculating the moving distance 
        of the offset group.
         """
        ctrl = self.lineWheelName.text()
        if not ctrl:
            pm.warning("Input your Controller's name.")
            return
        grpNames = [
            f"{ctrl}_grp", 
            f"{ctrl}_offset", 
            f"{ctrl}_offsetNull", 
            f"{ctrl}_offsetPrevious", 
            f"{ctrl}_offsetOrient"
            ]
        if True in [pm.objExists(i) for i in grpNames]:
            pm.warning("Expression groups already exist. Clean up first.")
            return
        ctrlTopGrp = f"{ctrl}_upDownMain_grp"
        if not pm.objExists(ctrlTopGrp):
            pm.warning("The upDownMain_grp does not exist.")
            return
        exprGrps = self.createWheelGroups(ctrl)
        locator = self.createWheelRotationLocator(ctrl)
        self.createExpression(ctrl, locator, exprGrps)
        pm.parent(ctrlTopGrp, w=True)
        pm.delete(ctrlTopGrp, cn=True)
        pm.parent(ctrlTopGrp, exprGrps[1])


    def build_doors(self):
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning("Nothing Selected.")
            return
        doorName = self.lineDoorName.text()
        if not doorName:
            pm.warning("Door Name Field is empty.")
            return
        if pm.objExists(doorName):
            pm.warning("%s is aleady exists." % doorName)
            return
        doorCtrlGroup = self.createDoorCtrl(sel[0], doorName)
        for i in doorCtrlGroup:
            self.insertPositionList(self.doorPosition, i)


    def createDoorCtrl(self, selection, doorName) -> list:
        """ Create a door controller to rotate the mirror.
        The door on the right is created automatically. 
        The shapes of the front and back doors are different.
         """
        Back = "Back" in doorName
        back = "back" in doorName
        if any([Back, back]):
            doorType = "door2"
        else:
            doorType = "door"
        ctrl = Controllers()
        cc = ctrl.createControllers(**{doorType: doorName})[0]
        defaultScale = 58
        size = getBoundingBoxSize(selection) / defaultScale
        pm.scale(cc, [size, size, size])
        pm.makeIdentity(cc, a=1, t=1, r=1, s=1, n=0, pn=1)
        pm.matchTransform(cc, selection, pos=True, rot=True)
        doorAGrp, doorA = groupOwnPivot(cc, null=True)[::2]
        doorBGrp, doorB = mirrorCopy(cc)[::2]
        result = [doorAGrp, doorBGrp]
        for i in [doorA, doorB]:
            pm.transformLimits(i, ry=(-60, 0), ery=(False, True))
        return result


    def createWheelGroups(self, ctrl):
        """ Create groups for the expression. """
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


    def createExpression(self, ctrl: str, locator: str, names: list) -> None:
        """ Rotate the locator by the moving distance of offset_grp. """
        ctrlMain = f"{ctrl}_main"
        if not pm.attributeQuery("AutoRoll", node=ctrlMain, ex=True):
            attrAuto = 'AutoRoll'
            pm.addAttr(ctrlMain, ln=attrAuto, at='long', min=0, max=1, dv=1)
            pm.setAttr(f'{ctrlMain}.{attrAuto}', e=True, k=True)
        br = '\n'
        offset = names[1]
        previous, orient = names[3:]
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


    def delete_expression(self):
        """ Deletes the expression applied to the wheel controller. """
        ctrl = self.lineWheelName.text()
        if not ctrl:
            pm.warning("The ctrl's name field is empty.")
            return
        ctrlTopGrp = f"{ctrl}_upDownMain_grp"
        exprTopGrp = f"{ctrl}_grp"
        ctrlMain = f"{ctrl}_main"
        exprList = pm.listConnections(ctrlMain, type="expression", d=True)
        try:
            pm.delete(exprList)
            pm.parent(ctrlTopGrp, w=True)
            pm.delete(exprTopGrp)
        except:
            pass
        if pm.attributeQuery("AutoRoll", node=ctrlMain, ex=True):
            pm.deleteAttr(f"{ctrlMain}.AutoRoll")


    def delete_wheel(self):
        """ Clean up the wheel controllers. """
        ctrl = self.lineWheelName.text()
        if not ctrl:
            pm.warning("The ctrl's name field is empty.")
            return
        ctrlGrp = f"{ctrl}_grp"
        ctrlTopGrp = f"{ctrl}_upDownMain_grp"
        for i in [ctrlGrp, ctrlTopGrp]:
            try:
                pm.delete(i)
            except:
                pass
        if "cc_" in ctrl:
            locName = ctrl.replace("cc_", "loc_")
        else:
            locName = f"{ctrl}_%s" % "exprLocator"
        try:
            self.wheelPosition.remove(locName)
        except:
            pass


    def delete_door(self):
        for i in self.doorPosition:
            try:
                pm.delete(i)
            except:
                continue
        self.doorPosition = []


    def createWheelCtrl(self, ccName, obj) -> str:
        """ Make controllers according to the wheel size. """
        cc = [
            f"{ccName}_upDownMain", 
            f"{ccName}_upDownSub", 
            f"{ccName}_main", 
            f"{ccName}_sub"
        ]
        sizeRatio = [14, 18, 9, 11]
        ctrl = Controllers()
        rad = getBoundingBoxSize(obj)
        rad = max(rad)
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
        ccGrp = groupOwnPivot(*cc, null=True)
        parentHierarchically(*ccGrp)
        pm.makeIdentity(ccGrp, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccMain = cc[2]
        attrRad = "Radius"
        pm.addAttr(ccMain, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ccMain}.{attrRad}', e=True, k=True)
        pm.setAttr(f"{ccMain}.Radius", rad)


    def createWheelRotationLocator(self, ctrl):
        ctrlSub = f"{ctrl}_sub"
        if "cc_" in ctrl:
            locName = ctrl.replace("cc_", "loc_")
        else:
            locName = f"{ctrl}_%s" % "exprLocator"
        if pm.objExists(locName):
            return locName
        else:
            locator = pm.spaceLocator(n=locName)
            pm.matchTransform(locator, ctrlSub, pos=True)
            pm.parent(locator, ctrlSub)
            pm.makeIdentity(locator, a=1, t=1, r=0, s=0, n=0, pn=1)
            return locator


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
        print(self.bodyPosition)
        print(self.wheelPosition)
        print(self.doorPosition)
        sel = selectGroupOnly()
        if sel:
            txt = sel[0].name()
            self.bodyGroup = txt
            self.lineSelBody.setText(txt)
            self.insertPositionList(self.bodyPosition, txt)
            return txt
        else:
            return


    def insertPositionList(self, positionGroup: list, element: str):
        if isinstance(element, pm.PyNode):
            element = element.name()
        if element in positionGroup:
            return
        else:
            positionGroup.append(element)
            return element
    

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
        try:
            pm.parent(self.objGroup, "MODEL")
        except:
            pass
        return grpName


    def setWheelName(self):
        """ Remove spaces from wheel names. """
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_wheel%s" % buttonName.replace(" ", "")
        self.lineWheelName.setText(ctrlName)
        self.lineWheelName.clearFocus()


    def setDoorName(self):
        """ Remove spaces from door names. """
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_door%s" % buttonName.replace(" ", "")
        self.lineDoorName.setText(ctrlName)
        self.lineDoorName.clearFocus()


# if __name__ == "__main__":
#     try:
#         qrCar.close()
#         qrCar.deleteLater()
#     except:
#         pass
#     qrCar = Car()
#     qrCar.show()