from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
# from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
from general import *
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
        self.resize(250, 590)
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
        self.fldSelectWheel.setClearButtonEnabled(True)
        self.fldSelectWheel.setEnabled(True)
        self.fldSelectWheel.setPlaceholderText("Click Wheel Name")
        self.fldSelectWheel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.fldSelectWheel)
        self.gridLayout_4 = QGridLayout()
        self.btnLeftFront = QPushButton("Left Front")
        self.gridLayout_4.addWidget(self.btnLeftFront, 0, 0, 1, 1)
        self.btnRightFront = QPushButton("Right Front")
        self.gridLayout_4.addWidget(self.btnRightFront, 0, 1, 1, 1)
        self.btnLeftBack = QPushButton("Left Back")
        self.gridLayout_4.addWidget(self.btnLeftBack, 2, 0, 1, 1)
        self.btnRightBack = QPushButton("Right Back")
        self.gridLayout_4.addWidget(self.btnRightBack, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.btnCreateWheel = QPushButton("Create Wheel")
        self.verticalLayout.addWidget(self.btnCreateWheel)
        self.gridLayout_5 = QGridLayout()
        self.btnSetExpr = QPushButton("Set Expression")
        self.gridLayout_5.addWidget(self.btnSetExpr, 0, 0, 1, 1)
        self.btnDelExpr = QPushButton("Del Expression")
        self.gridLayout_5.addWidget(self.btnDelExpr, 0, 1, 1, 1)
        self.btnSetPressure = QPushButton("Set Pressure")
        self.btnSetPressure.setEnabled(False)
        self.gridLayout_5.addWidget(self.btnSetPressure, 2, 0, 1, 1)
        self.btnDelPressure = QPushButton("Del Pressure")
        self.btnDelPressure.setEnabled(False)
        self.gridLayout_5.addWidget(self.btnDelPressure, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.btnWheelCleanUp = QPushButton("Clean Up")
        self.verticalLayout.addWidget(self.btnWheelCleanUp)
        self.line_3 = QFrame()
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_3)
        self.fldSelectDoor = QLineEdit()
        self.fldSelectDoor.setClearButtonEnabled(True)
        self.fldSelectDoor.setEnabled(True)
        self.fldSelectDoor.setPlaceholderText("Click Door Name")
        self.fldSelectDoor.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.fldSelectDoor)
        self.gridLayout_6 = QGridLayout()
        self.btnLeftDoor = QPushButton("Left Front")
        self.gridLayout_6.addWidget(self.btnLeftDoor, 0, 0, 1, 1)
        self.btnRightDoor = QPushButton("Right Front")
        self.btnRightDoor.setEnabled(False)
        self.gridLayout_6.addWidget(self.btnRightDoor, 0, 1, 1, 1)
        self.btnLeftDoor2 = QPushButton("Left Back")
        self.gridLayout_6.addWidget(self.btnLeftDoor2, 2, 0, 1, 1)
        self.btnRightDoor2 = QPushButton("Right Back")
        self.btnRightDoor2.setEnabled(False)
        self.gridLayout_6.addWidget(self.btnRightDoor2, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        self.btncreateDoorCtrl = QPushButton("Create Door")
        self.verticalLayout.addWidget(self.btncreateDoorCtrl)
        self.btnDoorCleanUp = QPushButton("Clean Up")
        self.verticalLayout.addWidget(self.btnDoorCleanUp)
        self.line_4 = QFrame()
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_4)
        self.btnConnectAll = QPushButton("Connect All")
        self.verticalLayout.addWidget(self.btnConnectAll)
        self.btnSetColor = QPushButton("Set Color")
        self.verticalLayout.addWidget(self.btnSetColor)
        self.btnConnection = QPushButton("Joint Connection")
        # self.btnConnection.setEnabled(False)
        self.verticalLayout.addWidget(self.btnConnection)
        self.btnDisconnection = QPushButton("Disconnection")
        self.verticalLayout.addWidget(self.btnDisconnection)
        self.line_5 = QFrame()
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_5)
        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # Buttons Links
        self.buttonsLink()


    def buttonsLink(self):
        self.fldCarName.returnPressed.connect(self.createCarGroup)
        self.btnCarGrp.clicked.connect(self.createCarGroup)
        self.btnTempJnt.clicked.connect(self.createJoints)
        self.btnLtoR.clicked.connect(self.build_symmetry)
        self.btnRtoL.clicked.connect(self.build_symmetry)
        self.btnBuild.clicked.connect(self.build)
        self.btnCleanUp.clicked.connect(self.cleanUp)
        self.btnLeftFront.clicked.connect(self.setWheelNameField)
        self.btnRightFront.clicked.connect(self.setWheelNameField)
        self.btnLeftBack.clicked.connect(self.setWheelNameField)
        self.btnRightBack.clicked.connect(self.setWheelNameField)
        self.btnCreateWheel.clicked.connect(self.build_wheels)
        self.btnSetExpr.clicked.connect(self.build_expression)
        self.btnDelExpr.clicked.connect(self.deleteExpression)
        self.btnWheelCleanUp.clicked.connect(self.cleanUp_wheel)
        self.btnLeftDoor.clicked.connect(self.setDoorNameField)
        self.btnRightDoor.clicked.connect(self.setDoorNameField)
        self.btnLeftDoor2.clicked.connect(self.setDoorNameField)
        self.btnRightDoor2.clicked.connect(self.setDoorNameField)
        self.btncreateDoorCtrl.clicked.connect(self.build_doors)
        self.btnDoorCleanUp.clicked.connect(self.cleanUp_door)
        self.btnConnectAll.clicked.connect(self.connectAll)
        self.btnSetColor.clicked.connect(self.setColor)
        self.btnConnection.clicked.connect(self.jointConnect)
        self.btnDisconnection.clicked.connect(self.jointDisconnect)
        self.btnClose.clicked.connect(self.close)


    def build(self):
        """ Create a global controller and body controller. """
        self.updateJointsPosition()
        self.cleanUp()
        self.createCarGroup()
        self.createJoints()
        self.createFbxJoints()
        self.createMainCtrl()


    def build_symmetry(self):
        """ Make the left and right joints the same. """
        button = self.sender()
        buttonName = button.text()
        buttonName = buttonName.replace(" ", "")
        self.updateJointsPosition()
        self.updateSameSide(buttonName)
        self.cleanUp()
        self.createJoints()


    def build_wheels(self):
        """ Create a wheel controller only.
        There is no expression for turning the wheel.
         """
        ctrl = self.fldSelectWheel.text()
        obj = selectObjectOnly()
        if not ctrl:
            pm.warning("Input your Controller's name.")
            return
        if not obj:
            pm.warning("Select the polygonal mesh of the wheel.")
            return
        if pm.objExists(f"{ctrl}_main"):
            pm.warning(f"{ctrl}_main ctrl aleady exists.")
            return
        self.createWheelCtrl(ctrl, obj)
        self.createWheelRotationLocator(ctrl)


    def build_expression(self):
        """ Add an expression to the wheel controller.
        Rotate the locator by calculating the moving distance 
        of the offset group.
         """
        ctrl = self.fldSelectWheel.text()
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
        doorName = self.fldSelectDoor.text()
        if not doorName:
            pm.warning("Door Name Field is empty.")
            return
        if pm.objExists(doorName):
            pm.warning("%s is aleady exists." % doorName)
            return
        self.doorCtrls += self.createDoorCtrl(sel[0], doorName)
        self.doorCtrls = list(set(self.doorCtrls))
        self.doorJoints += self.createDoorJoint(doorName)
        self.doorJoints = list(set(self.doorJoints))


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
        """ Clean up the joint groups. """
        listDelete = [
            # self.topGroup, 
            self.rootJnt, 
            self.rootFbx, 
            self.mainCtrl + "_grp", 
            ]
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue


    def cleanUp_wheel(self):
        """ Clean up the wheel controllers. """
        ctrl = self.fldSelectWheel.text()
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


    def cleanUp_door(self):
        listDelete = self.doorCtrls + self.doorJoints
        if not listDelete:
            pm.warning("There is no door to delete.")
            return
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue
        self.doorCtrls = []
        self.doorJoints = []


    def createCarGroup(self):
        """ Create an entire car group. """
        carName = self.fldCarName.text()
        if self.topGroup == carName:
            grpName = carName
        elif self.topGroup != "" and carName == "":
            grpName = self.topGroup
        else:
            grpName = carName
            self.topGroup = carName
        createRigGroups(grpName)
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
        """ Copy jnt_root, jnt_body... to fbx_root, fbx_body... """
        fbx = pm.duplicate(self.rootJnt, rr=True, n=self.rootFbx)
        fbx = fbx[0]
        pm.select(cl=True)
        pm.select(fbx, hi=True)
        for i in pm.ls(sl=True):
            new = i.replace("jnt_", "fbx_")
            pm.rename(i, new)
        self.tryParent(self.rootFbx, "rigBones")


    def createMainCtrl(self):
        """ Create main, sub and body controllers. """
        ctrlNames = {
            "car": "cc_body", 
            "car2": "cc_sub", 
            "circle": "cc_main", 
            }
        cc = Controllers()
        ctrl = cc.createControllers(**ctrlNames)
        name = list(ctrlNames.values())
        if sorted(ctrl) != sorted(name):
            pm.warning("Check if the Ctrl already exists.")
            return
        grps = []
        for i in ctrl:
            if self.mainCtrl == i:
                pm.scale(i, (20, 20, 20))
                pm.makeIdentity(i, a=1, t=0, r=0, s=1, n=0, pn=1)
            grp = groupOwnPivot(i)[0]
            grps.append(grp)
        for child, parents in zip(grps[:2], ctrl[1:]):
            pm.parent(child, parents)
        pm.matchTransform(grps[0], self.bodyJnt, pos=True)
        self.tryParent(grps[-1], "controllers")
        

    def tryParent(self, child: str, parents: str):
        try:
            pm.parent(child, parents)
        except:
            pass


    def setWheelNameField(self):
        """ Remove spaces from wheel names. """
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_wheel%s" % buttonName.replace(" ", "")
        self.fldSelectWheel.setText(ctrlName)
        self.fldSelectWheel.clearFocus()


    def setDoorNameField(self):
        """ Remove spaces from door names. """
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_door%s" % buttonName.replace(" ", "")
        self.fldSelectDoor.setText(ctrlName)
        self.fldSelectDoor.clearFocus()


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


    def deleteExpression(self):
        """ Deletes the expression applied to the wheel controller. """
        ctrl = self.fldSelectWheel.text()
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


    def jointConnect(self):
        """ Connect the bind joints and the rig joints. """
        jntNames = selectJointOnly("bindBones")
        # jntNames = self.jntNameAndPos.keys()
        for jnt in jntNames:
            fbx = jnt.replace("jnt_", "fbx_")
            try:
                pm.connectAttr(f"{fbx}.translate", f"{jnt}.translate", f=True)
                pm.connectAttr(f"{fbx}.rotate", f"{jnt}.rotate", f=True)
                pm.connectAttr(f"{fbx}.scale", f"{jnt}.scale", f=True)
                pm.connectAttr(f"{fbx}.visibility", f"{jnt}.visibility", f=True)
            except:
                continue


    def jointDisconnect(self):
        """ Disconnect the bind joints and rig joints. """
        jntNames = selectJointOnly("bindBones")
        # jntNames = self.jntNameAndPos.keys()
        for jnt in jntNames:
            fbx = jnt.replace("jnt_", "fbx_")
            try:
                pm.disconnectAttr(f"{fbx}.translate", f"{jnt}.translate")
                pm.disconnectAttr(f"{fbx}.rotate", f"{jnt}.rotate")
                pm.disconnectAttr(f"{fbx}.scale", f"{jnt}.scale")
                pm.disconnectAttr(f"{fbx}.visibility", f"{jnt}.visibility")
            except:
                continue


    def createDoorCtrl(self, selection, doorName) -> list:
        """ Create a door controller to rotate the mirror.
        The door on the right is created automatically. 
        The shapes of the front and back doors are different.
         """
        _B = "_Bk" in doorName
        Ba = "Back" in doorName
        ba = "back" in doorName
        if any([_B, Ba, ba]):
            doorType = "door2"
        else:
            doorType = "door"
        ctrl = Controllers()
        cc = ctrl.createControllers(**{doorType: doorName})[0]
        pm.matchTransform(cc, selection, pos=True, rot=True)
        doorAGrp, doorA = groupOwnPivot(cc, null=True)[::2]
        doorBGrp, doorB = mirrorCopy(cc)[::2]
        result = [doorAGrp, doorBGrp]
        for i in [doorA, doorB]:
            pm.transformLimits(i, ry=(-60, 0), ery=(False, True))
        return result


    def createDoorJoint(self, ctrlName) -> list:
        """ Create a door joint, 
        and if there is an fbx joint, copy it to fbx as well.
         """
        if not ctrlName:
            return
        jntName = ctrlName.replace("cc_", "jnt_")
        jnt = pm.joint(p=(0,0,0), n=jntName)
        pm.matchTransform(jnt, ctrlName, pos=True)
        pm.connectJoint(jnt, self.bodyJnt, pm=True)
        pm.makeIdentity(jnt, a=1, t=1, r=1, s=1, jo=1)
        jntList = pm.mirrorJoint(jnt, myz=True, mb=True, sr=("Left", "Right"))
        jntList.insert(0, jnt)
        fbxList = []
        if not pm.objExists(self.bodyFbx):
            pass
        else:
            for i in jntList:
                fbx = i.replace("jnt_", "fbx_")
                copied = pm.duplicate(i, rr=True, n=fbx)[0]
                pm.parent(copied, w=True)
                pm.connectJoint(copied, self.bodyFbx, pm=True)
                fbxList.append(copied)
        return jntList + fbxList


    def connectAll(self):
        """ Most connections for rough cars. 
        Expression is for the left front wheel only.
        Most connections are as bellows

        - Locator1 <---> Locator2, 3, 4
        - Locators ---> fbx Joints
        - cc_sub ---> skeletons
        - cc_sub ---> wheelCtrl
        - cc_sub ---> fbx_root
        - cc_body ---> fbx_body

        You have to connect the joints and modeling manually.
        - cc_sub ---> modeling top group
        - jnt_body ---> upper modeling group
        - jnt_wheel ---> wheel group
         """
        # Connect most all
        lrfb = ["LeftFront", "RightFront", "LeftBack", "RightBack"]
        locs = [f"loc_wheel{i}" for i in lrfb]
        fbxWheels = [f"fbx_wheel{i}" for i in lrfb]
        wheelGrps = [
            "cc_wheelLeftFront_offset", 
            "cc_wheelRightFront_upDownMain_grp", 
            "cc_wheelLeftBack_upDownMain_grp", 
            "cc_wheelRightBack_upDownMain_grp"
            ]
        rotX = "rotateX"
        ccSub = "cc_sub"
        for i in range(1, 4):
            pm.connectAttr(f"{locs[0]}.{rotX}", f"{locs[i]}.{rotX}", f=True)
        for l, w in zip(locs, fbxWheels):
            pm.parentConstraint(l, w, mo=True, w=1.0)
        for i in wheelGrps:
            pm.parentConstraint(ccSub, i, mo=True, w=1.0)
            pm.scaleConstraint(ccSub, i, mo=True, w=1.0)
        pm.scaleConstraint(ccSub, "skeletons", mo=True, w=1.0)
        pm.parentConstraint(ccSub, "fbx_root", mo=True, w=1.0)
        pm.parentConstraint("cc_body", "fbx_body", mo=True, w=1.0)
        # Visibility off
        for i in locs:
            pm.setAttr(f"{i}.visibility", 0)
        pm.setAttr(f"skeletons.visibility", 0)
        pm.setAttr(f"rigBones.visibility", 0)


    def setColor(self):
        colorList = {
            "yellow": [
                "cc_main", 
                "cc_body", 
                "cc_wheelLeftFront_upDownMain", 
                "cc_wheelRightFront_upDownMain", 
                "cc_wheelLeftBack_upDownMain", 
                "cc_wheelRightBack_upDownMain"
                ], 
            "pink": [
                "cc_sub", 
                "cc_wheelLeftFront_upDownSub", 
                "cc_wheelRightFront_upDownSub", 
                "cc_wheelLeftBack_upDownSub", 
                "cc_wheelRightBack_upDownSub"
                ], 
            "red": [
                "cc_wheelLeftFront_main", 
                "cc_wheelLeftBack_main"
                ], 
            "red2": [
                "cc_wheelLeftFront_sub", 
                "cc_wheelLeftBack_sub"
                ], 
            "blue": [
                "cc_wheelRightFront_main", 
                "cc_wheelRightBack_main"
                ], 
            "blue2": [
                "cc_wheelRightFront_sub", 
                "cc_wheelRightBack_sub"
                ]
            }
        colorIndex = {
            "blue": 6, 
            "blue2": 18, 
            "pink": 9, 
            "red": 13, 
            "red2": 21, 
            "green": 14, 
            "green2": 23, 
            "yellow": 17
            }
        for color, objList in colorList.items():
            idx = colorIndex[color]
            for obj in objList:
                try:
                    obj = pm.PyNode(obj)
                    shp = obj.getShape()
                    pm.setAttr(f"{shp}.overrideEnabled", 1)
                    pm.setAttr(f"{shp}.overrideColor", idx)
                except:
                    continue


# if __name__ == "__main__":
#     try:
#         qrCar.close()
#         qrCar.deleteLater()
#     except:
#         pass
#     qrCar = Car()
#     qrCar.show()


class MixamoCharacter(QWidget):
    def __init__(self):
        self.mainCurve = "mainCurve"
        self.spine = [
            "Hips", 
            "Spine", 
            "Spine1", 
            "Spine2", 
            "Neck", 
            "Head", 
            "HeadTop_End"
            ]
        self.leftArms = [
            "LeftShoulder", 
            "LeftArm", 
            "LeftForeArm", 
            "LeftHand"
            ]
        self.leftLegs = [
            "LeftUpLeg", 
            "LeftLeg", 
            "LeftFoot", 
            "LeftToeBase", 
            "LeftToe_End"
            ]
        self.leftThumb = [
            "LeftHandThumb1", 
            "LeftHandThumb2", 
            "LeftHandThumb3", 
            "LeftHandThumb4"
            ]
        self.leftIndex = [
            "LeftHandIndex1", 
            "LeftHandIndex2", 
            "LeftHandIndex3", 
            "LeftHandIndex4"
            ]
        self.leftMiddle = [
            "LeftHandMiddle1", 
            "LeftHandMiddle2", 
            "LeftHandMiddle3", 
            "LeftHandMiddle4"
            ]
        self.leftRing = [
            "LeftHandRing1", 
            "LeftHandRing2", 
            "LeftHandRing3", 
            "LeftHandRing4"
            ]
        self.leftPinky = [
            "LeftHandPinky1", 
            "LeftHandPinky2", 
            "LeftHandPinky3", 
            "LeftHandPinky4"
            ]
        self.rightArms = [
            "RightShoulder", 
            "RightArm", 
            "RightForeArm", 
            "RightHand"
            ]
        self.rightLegs = [
            "RightUpLeg", 
            "RightLeg", 
            "RightFoot", 
            "RightToeBase", 
            "RightToe_End"
            ]
        self.rightThumb = [
            "RightHandThumb1", 
            "RightHandThumb2", 
            "RightHandThumb3", 
            "RightHandThumb4"
            ]
        self.rightIndex = [
            "RightHandIndex1", 
            "RightHandIndex2", 
            "RightHandIndex3", 
            "RightHandIndex4"
            ]
        self.rightMiddle = [
            "RightHandMiddle1", 
            "RightHandMiddle2", 
            "RightHandMiddle3", 
            "RightHandMiddle4"
            ]
        self.rightRing = [
            "RightHandRing1", 
            "RightHandRing2", 
            "RightHandRing3", 
            "RightHandRing4"
            ]
        self.rightPinky = [
            "RightHandPinky1", 
            "RightHandPinky2", 
            "RightHandPinky3", 
            "RightHandPinky4"
            ]
        self.jointPosition = {
            "Hips": (0.0, 98.223, 1.464), 
            "Spine": (0.0, 107.814, 1.588), 
            "Spine1": (0.0, 117.134, 0.203), 
            "Spine2": (0.0, 125.82, -1.089), 
            "Neck": (0.0, 141.589, -3.019), 
            "Head": (0.0, 150.649, -1.431), 
            "HeadTop_End": (0.0, 171.409, 5.635), 
            "LeftShoulder": (4.305, 136.196, -3.124), 
            "LeftArm": (19.934, 135.702, -5.494), 
            "LeftForeArm": (42.774, 135.702, -6.376), 
            "LeftHand": (63.913, 135.702, -6.131), 
            "LeftHandThumb1": (65.761, 135.008, -2.444), 
            "LeftHandThumb2": (68.495, 133.652, -0.242), 
            "LeftHandThumb3": (70.727, 132.545, 1.556), 
            "LeftHandThumb4": (72.412, 131.709, 2.913), 
            "LeftHandIndex1": (71.683, 134.879, -2.495), 
            "LeftHandIndex2": (74.972, 134.879, -2.495), 
            "LeftHandIndex3": (77.576, 134.879, -2.495), 
            "LeftHandIndex4": (80.181, 134.879, -2.495), 
            "LeftHandMiddle1": (71.566, 134.682, -4.906), 
            "LeftHandMiddle2": (75.085, 134.762, -4.906), 
            "LeftHandMiddle3": (78.171, 134.832, -4.906), 
            "LeftHandMiddle4": (81.57, 134.908, -4.906), 
            "LeftHandRing1": (71.293, 134.575, -6.84), 
            "LeftHandRing2": (74.241, 134.742, -6.84), 
            "LeftHandRing3": (77.231, 134.912, -6.84), 
            "LeftHandRing4": (80.134, 135.078, -6.84), 
            "LeftHandPinky1": (70.702, 134.116, -8.847), 
            "LeftHandPinky2": (73.811, 134.283, -8.847), 
            "LeftHandPinky3": (75.625, 134.38, -8.847), 
            "LeftHandPinky4": (77.461, 134.478, -8.847), 
            "RightShoulder": (-4.305, 136.196, -3.124), 
            "RightArm": (-21.859, 135.702, -5.585), 
            "RightForeArm": (-42.316, 135.702, -6.381), 
            "RightHand": (-63.913, 135.702, -6.131), 
            "RightHandThumb1": (-65.761, 135.008, -2.444), 
            "RightHandThumb2": (-68.495, 133.652, -0.242), 
            "RightHandThumb3": (-70.727, 132.545, 1.556), 
            "RightHandThumb4": (-72.412, 131.709, 2.913), 
            "RightHandIndex1": (-71.683, 134.879, -2.495), 
            "RightHandIndex2": (-74.972, 134.879, -2.495), 
            "RightHandIndex3": (-77.576, 134.879, -2.495), 
            "RightHandIndex4": (-80.181, 134.879, -2.495), 
            "RightHandMiddle1": (-71.565, 134.682, -4.906), 
            "RightHandMiddle2": (-75.085, 134.762, -4.906), 
            "RightHandMiddle3": (-78.171, 134.832, -4.906), 
            "RightHandMiddle4": (-81.569, 134.908, -4.906), 
            "RightHandRing1": (-71.293, 134.575, -6.84), 
            "RightHandRing2": (-74.24, 134.742, -6.84), 
            "RightHandRing3": (-77.231, 134.912, -6.84), 
            "RightHandRing4": (-80.134, 135.078, -6.84), 
            "RightHandPinky1": (-70.702, 134.116, -8.847), 
            "RightHandPinky2": (-73.811, 134.283, -8.847), 
            "RightHandPinky3": (-75.625, 134.38, -8.847), 
            "RightHandPinky4": (-77.461, 134.478, -8.847), 
            "LeftUpLeg": (10.797, 91.863, -1.849), 
            "LeftLeg": (10.797, 50.067, -0.255), 
            "LeftFoot": (10.797, 8.223, -4.39), 
            "LeftToeBase": (10.797, 0.001, 5.7), 
            "LeftToe_End": (10.797, 0.0, 14.439), 
            "RightUpLeg": (-10.797, 91.863, -1.849), 
            "RightLeg": (-10.797, 50.066, -0.255), 
            "RightFoot": (-10.797, 8.223, -4.39), 
            "RightToeBase": (-10.797, 0.001, 5.7), 
            "RightToe_End": (-10.797, 0.0, 14.439), 
            }
        self.hierarchy = {
            "Hips": [self.spine[1:], self.leftLegs, self.rightLegs], 
            "Spine2": [self.leftArms, self.rightArms], 
            "LeftHand": [
                self.leftThumb, 
                self.leftIndex, 
                self.leftMiddle, 
                self.leftRing, 
                self.leftPinky
                ], 
            "RightHand": [
                self.rightThumb, 
                self.rightIndex, 
                self.rightMiddle, 
                self.rightRing, 
                self.rightPinky
                ], 
            }
        # self.setupUI()
    

    def setupUI(self):
        # super(Car, self).__init__()
        # self.setParent(mayaMainWindow())
        # self.setWindowFlags(Qt.Window)
        self.buttonsLink()


    def buttonsLink(self):
        pass


    def createBones(self):
        self.cleanUp(self.mainCurve, self.jointPosition.keys())
        self.createJointAndNameIt(self.jointPosition)
        self.buildHierarchy(self.hierarchy)
        self.createMainCurve()


    def alignBonesCenter(self):
        self.updateAllJointPositions()
        self.updatePositionGridCenter(self.spine)
        self.createBones()


    def alignBonesSameSide(self):
        AtoB = "LeftToRight"
        # AtoB = "RightToLeft"
        self.updateAllJointPositions()
        sideA, sideB = self.seperateLeftAndRight(AtoB)
        self.updateBothSideToSame(sideA, sideB)
        self.createBones()


    def createRig_All(self):
        self.updateAllJointPositions()
        jntPos = self.jointPosition
        hiraky = self.hierarchy
        data = self.copyBonesForRig(jntPos, hiraky, "rig_", "")
        rigJntPos, rigHiraky = data
        self.cleanUp(rigJntPos.keys())
        self.createJointAndNameIt(rigJntPos)
        self.buildHierarchy(rigHiraky)


    def createRig_IKFK(self):
        self.createIKFK(self.spine[0], self.spine[1:4])
        self.createIKFK(self.leftArms[0], self.leftArms[1:])
        self.createIKFK(self.rightArms[0], self.rightArms[1:])
        self.createIKFK(self.spine[0], self.leftLegs)
        self.createIKFK(self.spine[0], self.rightLegs)


# ==============================================================================


    def createIKFK(self, parents: str, joints: list):
        self.updateAllJointPositions()
        jntPos = {i: self.jointPosition[i] for i in joints}
        hiraky = {parents: [joints]}
        for i in ["_IK", "_FK"]:
            data = self.copyBonesForRig(jntPos, hiraky, "rig_", i)
            rigJntPos, temp = data
            rigHiraky = {k.rsplit("_", 1)[0]: v for k, v in temp.items()}
            self.cleanUp(rigJntPos.keys())
            self.createJointAndNameIt(rigJntPos)
            self.buildHierarchy(rigHiraky)


    def copyBonesForRig(self, jointPosition, hierarchy, fore="", tail=""):
        """ Returns the data with a new name. 
        - positions = {str: (float, float, float), ...}
        - hierarchy = {str: [[ ],[ ]], ...}
         """
        rigJointPosition = {}
        for jnt, pos in jointPosition.items():
            rigJointPosition[f"{fore}{jnt}{tail}"] = pos 
        rigHierarchy = {}
        for parents, children in hierarchy.items():
            key = f"{fore}{parents}{tail}"
            value = [[f"{fore}{j}{tail}" for j in i] for i in children]
            rigHierarchy[key] = value
        return rigJointPosition, rigHierarchy


    def updateBothSideToSame(self, sideA, sideB):
        for idx, joint in enumerate(sideA):
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[sideB[idx]] = (x*-1, y, z)


    def seperateLeftAndRight(self, twoOptions: str) -> list:
        """ Direction has one of the options: 
        >>> "LeftToRight" or "RightToLeft" 
         """
        allJoints = self.jointPosition.keys()
        A, B = twoOptions.split("To")
        side = []
        otherSide = []
        for jointName in allJoints:
            if A in jointName:
                side.append(jointName)
            elif B in jointName:
                otherSide.append(jointName)
            else:
                continue
        return side, otherSide


    def updateAllJointPositions(self):
        allJoints = self.jointPosition.keys()
        for joint in allJoints:
            position = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = tuple(position)


    def updatePositionGridCenter(self, joints: list):
        for joint in joints:
            x, y, z = pm.xform(joint, q=True, t=True, ws=True)
            self.jointPosition[joint] = (0, y, z)


    def createMainCurve(self):
        rootJnt = self.spine[0]
        if not pm.objExists(rootJnt):
            return
        else:
            bbSize = getBoundingBoxSize(rootJnt)
            pm.circle(nr=(0, 1, 0), n=self.mainCurve, ch=0, r=bbSize)
            pm.parent(rootJnt, self.mainCurve)


    def getPrimaryAndSecondaryAxis(self, jnt=[]):
        isLeft = any(i in jnt[0] for i in self.leftArms)
        isRight = any(i in jnt[0] for i in self.rightArms)
        if isLeft:
            primaryAxis = 'yxz'
            secondaryAxis = 'zdown'
        elif isRight:
            primaryAxis = 'yxz'
            secondaryAxis = 'zup'
        else:
            primaryAxis = 'yzx'
            secondaryAxis = 'zup'
        return primaryAxis, secondaryAxis


    def buildHierarchy(self, hierarchyStructure: dict):
        for parents, bothSideList in hierarchyStructure.items():
            for jointList in bothSideList:
                parentHierarchically(*jointList)
                priAxis, secAxis = self.getPrimaryAndSecondaryAxis(jointList)
                orientJoints(jointList, priAxis, secAxis)
                parentHierarchically(*[parents, jointList[0]])


    def createJointAndNameIt(self, nameAndPosition: dict):
        for jointName, position in nameAndPosition.items():
            pm.select(cl=True)
            pm.joint(p=position, n=jointName)


    def cleanUp(self, *args):
        for element in args:
            isStr = isinstance(element, str)
            isIter = isinstance(element, Iterable)
            if not isStr and isIter:
                for i in element:
                    self.cleanUp(i)
            else:
                try:
                    pm.delete(element)
                except:
                    pass


# mc = MixamoCharacter()
# mc.createBones()
# mc.alignBonesCenter()
# mc.alignBonesSameSide()
# mc.createRig_All()
# mc.createRig_IKFK()


def connectAttributes(source: str, destination: str, \
                    t=False, r=False, s=False, v=False) -> None:
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        try:
            pm.connectAttr(f"{source}.{i}", f"{destination}.{i}", f=True)
        except:
            continue


def disConnectAttributes(source: str, destination: str, \
                    t=False, r=False, s=False, v=False) -> None:
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        try:
            pm.disconnectAttr(f"{source}.{i}", f"{destination}.{i}")
        except:
            continue


def connectBlendColorsNode(blender: str, objects: list=[], \
                            t=False, r=False, s=False, v=False) -> None:
    """ Create a blendColors node and 
    connect FK to colors1 and IK to colors2.
    
    Args: 
        blender: This is Switch.
            "cc_IKFK.Spine_IK0FK1", 
            "cc_IKFK.LArm_IK0FK1", 
            "cc_IKFK.RArm_IK0FK1", 
            "cc_IKFK.LLeg_IK0FK1", 
            "cc_IKFK.RLeg_IK0FK1", 
        objects: The list have destination, FK, and IK elements.
            objects = ["destination", "FK", "IK"]

    Options: 
        -- t: translate, 
        -- r: rotate, 
        -- s: scale, 
        -- v: visibility

    Examples:
        >>> connectBlendColorsNode("cc_IKFK.Spine_IK0FK1", t=1)
        >>> connectBlendColorsNode("cc_IKFK.LArm_IK0FK1", r=1)
        >>> connectBlendColorsNode("cc_IKFK.RArm_IK0FK1", s=1)
        >>> connectBlendColorsNode("cc_IKFK.LLeg_IK0FK1", v=1)
        >>> connectBlendColorsNode("cc_IKFK.RLeg_IK0FK1", t=1, v=1)
     """
    args = objects if objects else pm.ls(sl=True)
    if len(args) % 3:
        return
    else:
        quotient = len(args) // 3
        destination = args[0 : quotient*1]
        source1 = args[quotient : quotient*2]
        source2 = args[quotient*2 : quotient*3]
    attr = []
    if t:   attr.append("translate")
    if r:   attr.append("rotate")
    if s:   attr.append("scale")
    if v:   attr.append("visibility")
    for i in attr:
        for s1, s2, fin in zip(source1, source2, destination):
            blColor = pm.shadingNode("blendColors", au=True)
            pm.connectAttr(f"{s1}.{i}", f"{blColor}.color1", f=True)
            pm.connectAttr(f"{s2}.{i}", f"{blColor}.color2", f=True)
            pm.connectAttr(f"{blColor}.output", f"{fin}.{i}", f=True)
            pm.connectAttr(blender, f"{blColor}.blender")


def createIKHandle(*args, rp=False, sc=False, spl=False, spr=False):
    """ Create a ikHandle and return names.

    Args: 
        startJoint = ["joint1", "joint2", ..., "joint27"][0]
        endJoint = ["joint1", "joint2", ..., "joint27"][-1]

    Options:
        --rp: "ikRPsolver"
        --sc: "ikSCsolver"
        --spl: "ikSplineSolver"
        --spr: "ikSpringSolver"
    
    Return: 
        Created ikHandle name.
    """
    sel = args if args else pm.ls(sl=True)
    if rp:
        solver = "ikRPsolver"
    elif sc:
        solver = "ikSCsolver"
    elif spl:
        solver = "ikSplineSolver"
    elif spr:
        solver = "ikSpringSolver"
    else:
        return
    try:
        start = sel[0]
        end = sel[-1]
    except:
        return
    temp = start.split("_")
    temp[0] = "ikH"
    ikHandleName = "_".join(temp)
    result = pm.ikHandle(sj=start, ee=end, sol=solver, n=ikHandleName)
    return result


def connectLegAttributes(*args: list):
    """ Connect the leg's locators to the controller's attributes.

    Args: 
        The elements of the list are 
        ctrl, locHeel, locToe, locBankIn, locBankOut, locBall, grpBall.
        locators = [
            "cc_LeftFoot_IK", 
            "loc_LeftHeel_IK", 
            "loc_LeftToe_End_IK", 
            "loc_LeftBankIn_IK", 
            "loc_LeftBankOut_IK", 
            "loc_LeftToeBase_IK", 
            "ikH_LeftToeBase_IK_null"
            ]

    Examples:
        >>> connectLegAttributes(*locators)
     """
    sel = args if args else pm.ls(sl=True)
    ctrl, locHeel, locToe, locBankIn, locBankOut, locBall, grpBall = sel
    rx, ry, rz = ["rotateX", "rotateY", "rotateZ"]
    pm.connectAttr(f"{ctrl}.heelUp", f"{locHeel}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.heelTwist", f"{locHeel}.{ry}", f=True)
    pm.connectAttr(f"{ctrl}.toeUp", f"{locToe}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.toeTwist", f"{locToe}.{ry}", f=True)
    pm.connectAttr(f"{ctrl}.ballUp", f"{locBall}.{rx}", f=True)
    pm.connectAttr(f"{ctrl}.ballDown", f"{grpBall}.{rx}", f=True)
    clampNode = pm.shadingNode("clamp", au=True)
    pm.setAttr(f"{clampNode}.minR", -180)
    pm.setAttr(f"{clampNode}.maxG", 180)
    output1 = "outputR" if "Left" in locBankOut else "outputG"
    output2 = "outputG" if "Left" in locBankIn else "outputR"
    pm.connectAttr(f"{clampNode}.{output1}", f"{locBankOut}.{rz}", f=True)
    pm.connectAttr(f"{clampNode}.{output2}", f"{locBankIn}.{rz}", f=True)
    pm.connectAttr(f"{ctrl}.bank", f"{clampNode}.inputR", f=True)
    pm.connectAttr(f"{ctrl}.bank", f"{clampNode}.inputG", f=True)


def connectFKControllers(*args):
    fkJoints = args if args else pm.ls(sl=True)
    for jnt in fkJoints:
        ctrl = jnt.replace("rig_", "cc_")
        if pm.objExists(ctrl) and pm.objExists(jnt):
            pm.parentConstraint(ctrl, jnt, mo=True, w=1.0)
        else:
            continue

# ==============================================================================
# joints = [
#     'rig_RightUpLeg', 
#     'rig_RightLeg', 
#     'rig_RightFoot', 
#     'rig_RightToeBase', 
#     'rig_RightToe_End', 
#     'rig_RightUpLeg_FK', 
#     'rig_RightLeg_FK', 
#     'rig_RightFoot_FK', 
#     'rig_RightToeBase_FK', 
#     'rig_RightToe_End_FK', 
#     'rig_RightUpLeg_IK', 
#     'rig_RightLeg_IK', 
#     'rig_RightFoot_IK', 
#     'rig_RightToeBase_IK', 
#     'rig_RightToe_End_IK'
#     ]
# connectBlendColorsNode("cc_IKFK.RArm_IK0FK1", t=1, r=1)


# ==============================================================================
# createIKHandle(rp=True)


# ==============================================================================
# locators = [
#     "cc_LeftFoot_IK", 
#     "loc_LeftHeel_IK", 
#     "loc_LeftToe_End_IK", 
#     "loc_LeftBankIn_IK", 
#     "loc_LeftBankOut_IK", 
#     "loc_LeftToeBase_IK", 
#     "ikH_LeftToeBase_IK_null"
#     ]
# connectLegAttributes()


# ==============================================================================
# createPolevectorJoint()


# ==============================================================================
# fkJoints = [
#     'rig_LeftUpLeg_FK', 
#     'rig_LeftLeg_FK', 
#     'rig_LeftFoot_FK', 
#     'rig_LeftToeBase_FK', 
#     'rig_LeftToe_End_FK'
#     ]
# connectFKControllers()

# groupOwnPivot()
# sel = pm.ls(sl=True)
# print([i.name() for i in sel])