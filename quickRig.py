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
        self.btnLeftRear = QPushButton("Left Rear")
        self.gridLayout_4.addWidget(self.btnLeftRear, 2, 0, 1, 1)
        self.btnRightRear = QPushButton("Right Rear")
        self.gridLayout_4.addWidget(self.btnRightRear, 2, 1, 1, 1)
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
        self.btnLeftDoor2 = QPushButton("Left Rear")
        self.gridLayout_6.addWidget(self.btnLeftDoor2, 2, 0, 1, 1)
        self.btnRightDoor2 = QPushButton("Right Rear")
        self.btnRightDoor2.setEnabled(False)
        self.gridLayout_6.addWidget(self.btnRightDoor2, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
        self.btnCreateDoor = QPushButton("Create Door")
        self.verticalLayout.addWidget(self.btnCreateDoor)
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
        self.btnConnection.setEnabled(False)
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
        self.btnSetExpr.clicked.connect(self.buildExpression)
        self.btnDelExpr.clicked.connect(self.deleteExpression)
        self.btnWheelCleanUp.clicked.connect(self.cleanUpWheel)
        self.btnLeftDoor.clicked.connect(self.setDoorName)
        self.btnRightDoor.clicked.connect(self.setDoorName)
        self.btnLeftDoor2.clicked.connect(self.setDoorName)
        self.btnRightDoor2.clicked.connect(self.setDoorName)
        self.btnCreateDoor.clicked.connect(self.createDoor)
        self.btnDoorCleanUp.clicked.connect(self.cleanUpDoor)
        self.btnConnectAll.clicked.connect(self.connectAll)
        self.btnSetColor.clicked.connect(self.setColor)
        self.btnConnection.clicked.connect(self.jointConnect)
        self.btnDisconnection.clicked.connect(self.jointDisconnect)
        self.btnClose.clicked.connect(self.close)


    def build(self):
        """ Create a global controller and body controller. """
        self.updateJointsPosition()
        self.cleanUp()
        self.createGroups()
        self.createJoints()
        self.createFbxJoints()
        self.createCtrls()


    def buildSymmetry(self):
        """ Make the left and right joints the same. """
        button = self.sender()
        buttonName = button.text()
        buttonName = buttonName.replace(" ", "")
        self.updateJointsPosition()
        self.updateSameSide(buttonName)
        self.cleanUp()
        self.createJoints()


    def buildWheels(self):
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
        self.createRotationLocator(ctrl)


    def buildExpression(self):
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
        locator = self.createRotationLocator(ctrl)
        self.createExpression(ctrl, locator, exprGrps)
        pm.parent(ctrlTopGrp, w=True)
        pm.delete(ctrlTopGrp, cn=True)
        pm.parent(ctrlTopGrp, exprGrps[1])


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


    def cleanUpWheel(self):
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


    def cleanUpDoor(self):
        listDelete = [
            "cc_doorLeftFront_grp", 
            "cc_doorLeftRear_grp", 
            "cc_doorRightFront_grp", 
            "cc_doorRightRear_grp", 
            "jnt_doorLeftFront", 
            "jnt_doorLeftRear", 
            "jnt_doorRightFront", 
            "jnt_doorRightRear", 
            "fbx_doorLeftFront", 
            "fbx_doorLeftRear", 
            "fbx_doorRightFront", 
            "fbx_doorRightRear"
            ]
        for i in listDelete:
            try:
                pm.delete(i)
            except:
                continue


    def createGroups(self):
        """ Create an entire car group. """
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
        """ Create a global and body controller. """
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
        """ Remove spaces from wheel names. """
        button = self.sender()
        buttonName = button.text()
        ctrlName = "cc_wheel%s" % buttonName.replace(" ", "")
        self.fldSelectWheel.setText(ctrlName)
        self.fldSelectWheel.clearFocus()


    def setDoorName(self):
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
        print(ccGrp)
        parentHierarchically(*ccGrp)
        pm.makeIdentity(ccGrp, a=1, t=1, r=1, s=1, n=0, pn=1)
        ccMain = cc[2]
        attrRad = "Radius"
        pm.addAttr(ccMain, ln=attrRad, at='double', min=0.0001, dv=1)
        pm.setAttr(f'{ccMain}.{attrRad}', e=True, k=True)
        pm.setAttr(f"{ccMain}.Radius", rad)


    def createRotationLocator(self, ctrl):
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
        jntNames = self.jntNameAndPos.keys()
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
        jntNames = self.jntNameAndPos.keys()
        for jnt in jntNames:
            fbx = jnt.replace("jnt_", "fbx_")
            try:
                pm.disconnectAttr(f"{fbx}.translate", f"{jnt}.translate")
                pm.disconnectAttr(f"{fbx}.rotate", f"{jnt}.rotate")
                pm.disconnectAttr(f"{fbx}.scale", f"{jnt}.scale")
                pm.disconnectAttr(f"{fbx}.visibility", f"{jnt}.visibility")
            except:
                continue


    def createDoor(self):
        """ Create a door controller to rotate the mirror.
        The door on the right is created automatically. 
        The shapes of the front and back doors are different.
        Select the Pivot Object, First.
         """
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning("Nothing Selected.")
            return
        obj = self.fldSelectDoor.text()
        sel = sel[0]
        _B = "_Bk" in obj
        Ba = "Back" in obj
        ba = "back" in obj
        Re = "Rear" in obj
        re = "rear" in obj
        if any([_B, Ba, ba, Re, re]):
            doorType = "door2"
        else:
            doorType = "door"
        ctrl = Controllers()
        cc = ctrl.createControllers(**{doorType: obj})[0]
        pm.matchTransform(cc, sel, pos=True, rot=True)
        doorSideA = groupOwnPivot(cc, null=True)[2]
        doorSideB = mirrorCopy(cc)[2]
        for i in [doorSideA, doorSideB]:
            pm.transformLimits(i, ry=(-60, 0), ery=(False, True))
        self.createDoorJoint(obj)


    def createDoorJoint(self, ctrlName):
        jntName = ctrlName.replace("cc_", "jnt_")
        jnt = pm.joint(p=(0,0,0), n=jntName)
        pm.matchTransform(jnt, ctrlName, pos=True)
        pm.connectJoint(jnt, "jnt_body", pm=True)
        jntList = pm.mirrorJoint(jnt, myz=True, mb=True, sr=("Left", "Right"))
        jntList.insert(0, jnt)
        if pm.objExists("fbx_body"):
            for i in jntList:
                fbx = i.replace("jnt_", "fbx_")
                copied = pm.duplicate(i, rr=True, n=fbx)
                pm.parent(copied, w=True)
                pm.connectJoint(copied, "fbx_body", pm=True)


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

        Joints and modeling must be connected directly.
        - cc_sub ---> modeling top group
        - jnt_body ---> upper modeling group
        - jnt_wheel ---> wheel group
         """
        # Connect most all
        lrfb = ["LeftFront", "RightFront", "LeftRear", "RightRear"]
        locs = [f"loc_wheel{i}" for i in lrfb]
        fbxWheels = [f"fbx_wheel{i}" for i in lrfb]
        wheelGrps = [
            "cc_wheelLeftFront_offset", 
            "cc_wheelRightFront_upDownMain_grp", 
            "cc_wheelLeftRear_upDownMain_grp", 
            "cc_wheelRightRear_upDownMain_grp"
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
        # Connect joints and fbx_joints
        self.jointConnect()


    def setColor(self):
        colorList = {
            "yellow": [
                "cc_main", 
                "cc_body", 
                "cc_wheelLeftFront_upDownMain", 
                "cc_wheelRightFront_upDownMain", 
                "cc_wheelLeftRear_upDownMain", 
                "cc_wheelRightRear_upDownMain"
                ], 
            "pink": [
                "cc_sub", 
                "cc_wheelLeftFront_upDownSub", 
                "cc_wheelRightFront_upDownSub", 
                "cc_wheelLeftRear_upDownSub", 
                "cc_wheelRightRear_upDownSub"
                ], 
            "red": [
                "cc_wheelLeftFront_main", 
                "cc_wheelLeftRear_main"
                ], 
            "red2": [
                "cc_wheelLeftFront_sub", 
                "cc_wheelLeftRear_sub"
                ], 
            "blue": [
                "cc_wheelRightFront_main", 
                "cc_wheelRightRear_main"
                ], 
            "blue2": [
                "cc_wheelRightFront_sub", 
                "cc_wheelRightRear_sub"
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


if __name__ == "__main__":
    try:
        qrCar.close()
        qrCar.deleteLater()
    except:
        pass
    qrCar = Car()
    qrCar.show()


