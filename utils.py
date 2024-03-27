import math
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Speed(QWidget):
    def __init__(self):
        super(Speed, self).__init__()
        self.Min = pm.playbackOptions(q=True, min=True)    # min -> time slider Min value
        self.Max = pm.playbackOptions(q=True, max=True)    # max -> time slider Max value
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Speed Measurement")
        self.move(0, 0)
        self.resize(267, 151)
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.label = QLabel("Duration")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QLineEdit()
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.pushButton = QPushButton("Load")
        self.horizontalLayout.addWidget(self.pushButton)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QLabel("Create Curve")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.checkBox = QCheckBox()
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkBox)
        self.label_3 = QLabel("Speed1")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QLineEdit()
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_3)
        self.label_4 = QLabel("Speed2")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QLineEdit()
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_4)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButton_2 = QPushButton("Speed")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)


    # Functions for the Animation team.
    def speedAni(self):
        sel = pm.ls(sl=True, fl=True)
        if len(sel) == 0:
            pm.warning('Select at least One object.')
        else:
            obj = pm.ls(sl=True, fl=True)[-1]
            # Duration.
            startFrame = pm.intFieldGrp(self.duration, q=True, v1=True)
            endFrame = pm.intFieldGrp(self.duration, q=True, v2=True)
            duration = endFrame - startFrame + 1
            # Start and End Position.
            pm.currentTime(startFrame)
            sPoint = pm.xform(obj, q=True, ws=True, rp=True)
            pm.currentTime(endFrame)
            ePoint = pm.xform(obj, q=True, ws=True, rp=True)
            # Straight or Curved distance.
            chkBox = pm.checkBoxGrp(self.curvedChk, q=True, v1=True)
            if not chkBox:    # True is Curved Trail
                distance = self.calLinearDistance(sPoint, ePoint)
            else:
                distance = self.calCurvedDistance(obj, startFrame, endFrame)
            # Result
            result = self.calUnitVelocity(distance, duration)
            # Send the result to textField.
            self.speed1.setText('%0.3f km/h' % result[0])
            self.speed2.setText('%0.3f m/s' % result[1])
    
    
    # Calculate Velocity. Maya units
    def calUnitVelocity(self, distance, duration):
        # Units in this scene.
        currUnitLen = pm.currentUnit(q=True, l=True)    # l -> lengthUnit
        currUnitTim = pm.currentUnit(q=True, t=True)    # t -> timeUnit
        # Units determined by Maya.
        unitTimDic = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        unitLenDic = {'mm': 0.1, 'cm': 1, 'm': 100, 'km': 100000, 'in': 2.54, 'ft': 30.48, 'yd': 91.44, 'mi': 160934}
        # Convert Units to Centimeters.
        cm = distance * unitLenDic[currUnitLen]
        # Custom Time Units.(fps - > second)
        if 'fps' in currUnitTim:
            sec = duration / float(currUnitTim.split('fps')[0])
        else:
            sec = duration / unitTimDic[currUnitTim]
        # result -> km/h, m/s
        vel_H = round((cm / unitLenDic['km']) / (sec / 60 / 60), 3)
        vel_S = round((cm / unitLenDic['m']) / sec, 3)
        return vel_H, vel_S
        
    
    # Linear Distance between Start point and End point.
    # input List or Tuple.
    def calLinearDistance(self, startPoint, endPoint):
        lenSP = len(startPoint) if isinstance(startPoint, list) or isinstance(startPoint, tuple) else True
        lenEP = len(endPoint) if isinstance(endPoint, list) or isinstance(endPoint, tuple) else False
        if lenSP == lenEP:
            if lenSP == 3:
                distance = math.sqrt(
                math.pow(endPoint[0] - startPoint[0], 2) + 
                math.pow(endPoint[1] - startPoint[1], 2) + 
                math.pow(endPoint[2] - startPoint[2], 2)
                )            
            elif lenSP == 2:
                distance = math.sqrt(
                math.pow(endPoint[0] - startPoint[0], 2) + 
                math.pow(endPoint[1] - startPoint[1], 2)
                )
            elif lenSP == 1:
                distance = abs(endPoint[0] - startPoint[0])
            else:
                distance = False
            return distance
        else:
            return False


    # Create Curves or measure lengths.
    def calCurvedDistance(self, obj, startFrame, endFrame):
        objType = pm.ls(obj, dag=True, type=['nurbsCurve'])
        if objType:
            curveName = objType[-1].getParent().name()
        else:
            pList = []
            for i in range(startFrame, endFrame + 1):
                pm.currentTime(i)
                try:
                    pList.append(pm.pointPosition(obj))
                except:
                    pList.append(pm.xform(obj, q=True, ws=True, rp=True))
            curveName = pm.curve(p=pList)
        curveNameLength = pm.arclen(curveName)
        return curveNameLength


if __name__ == "__main__":
    try:
        spd.close()
        spd.deleteLater()
    except:
        pass
    spd = Speed()
    spd.show()