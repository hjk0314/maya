from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance
from general import *
import pymel.core as pm
import maya.OpenMayaUI as omui


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Car(QWidget):
    def __init__(self):
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
        self.resize(250, 330)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(5)
        self.fldCarName = QLineEdit("carName")
        self.fldCarName.setClearButtonEnabled(True)
        self.fldCarName.setPlaceholderText("Input your car name")
        self.verticalLayout.addWidget(self.fldCarName)
        self.line0 = QFrame()
        self.line0.setFrameShape(QFrame.HLine)
        self.line0.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line0)
        self.btnTempJnt = QPushButton("Create temp joints")
        self.verticalLayout.addWidget(self.btnTempJnt)
        self.horizontalLayout = QHBoxLayout()
        self.btnLtoR = QPushButton("Left -> Right")
        self.horizontalLayout.addWidget(self.btnLtoR)
        self.btnRtoL = QPushButton("Right -> Left")
        self.horizontalLayout.addWidget(self.btnRtoL)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line1)
        self.btnBuild = QPushButton("Build")
        self.verticalLayout.addWidget(self.btnBuild)
        self.gridLayout = QGridLayout()
        self.btnAutoWheel = QPushButton("Auto Wheel")
        self.gridLayout.addWidget(self.btnAutoWheel, 0, 0, 1, 1)
        self.btnKeyWheel = QPushButton("Key Wheel")
        self.gridLayout.addWidget(self.btnKeyWheel, 0, 1, 1, 1)
        self.btnDoor = QPushButton("Door")
        self.gridLayout.addWidget(self.btnDoor, 1, 0, 1, 1)
        self.btnHandle = QPushButton("Handle")
        self.gridLayout.addWidget(self.btnHandle, 1, 1, 1, 1)
        self.btnTirePressure = QPushButton("Tire Pressure")
        self.gridLayout.addWidget(self.btnTirePressure, 2, 0, 1, 1)
        self.btnEtc = QPushButton("Etc")
        self.gridLayout.addWidget(self.btnEtc, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.btnCleanUp = QPushButton("Clean Up")
        self.verticalLayout.addWidget(self.btnCleanUp)
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line2)
        self.btnConnection = QPushButton("Joint Connection")
        self.verticalLayout.addWidget(self.btnConnection)
        self.btnDisconnection = QPushButton("Disconnection")
        self.verticalLayout.addWidget(self.btnDisconnection)
        self.btnDeleteAll = QPushButton("Delete All")
        self.verticalLayout.addWidget(self.btnDeleteAll)
        self.line3 = QFrame()
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line3)
        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        # Buttons Links
        self.buttonsLink()


    def buttonsLink(self):
        self.btnClose.clicked.connect(self.close)


    def build(self):
        self.updateJointsPosition()
        self.updateSameSide()
        self.cleanUp()
        self.createGroups()
        self.createJoints()
        self.createFbxJoints()
        self.createCtrls()
        # self.setControllers()


    def updateJointsPosition(self):
        for jnt in self.jntNameAndPos.keys():
            pos = getPosition(jnt)
            self.jntNameAndPos[jnt] = pos


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
        carName = "test"
        rg = RigGroups()
        rg.createRigGroups(carName)


    def createJoints(self):
        for jnt, pos in self.jntNameAndPos.items():
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
        cc = [f"{ccName}_upDownMain", f"{ccName}_upDownSub", 
            f"{ccName}_Main", f"{ccName}_Sub"]
        ccGrp = []
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


    def createRotationLocator(self, ctrl):
        locName = ctrl.replace("cc_", "loc_")
        locator = pm.spaceLocator(n=locName)
        pm.matchTransform(locator, ctrl, pos=True)
        pm.parent(locator, ctrl)
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


if __name__ == "__main__":
    try:
        qrCar.close()
        qrCar.deleteLater()
    except:
        pass
    qrCar = Car()
    qrCar.show()


# car = Car()
# obj = "jaguarA_down_tire_Ft_L_tire_rubber_1"
# ctrl = "cc_wheelLeftFront"
# grpNames = car.createWheelGroups(ctrl)
# ccSub = car.createWheelCtrl(obj, ctrl, grpNames[1])
# locator = car.createRotationLocator(ccSub)
# car.createExpression(ccSub, locator, grpNames)

