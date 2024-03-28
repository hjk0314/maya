import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)


class Speed(QWidget):
    def __init__(self):
        self.unitTimeIndex = {
            'game': 15, 
            'film': 24, 
            'pal': 25, 
            'ntsc': 30, 
            'show': 48, 
            'palf': 50, 
            'ntscf': 60
            }
        self.unitLengthIndex = {
            'mm': 0.1, 
            'cm': 1, 
            'm': 100, 
            'km': 100000, 
            'in': 2.54, 
            'ft': 30.48, 
            'yd': 91.44, 
            'mi': 160934
            }
        super(Speed, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Speed Measurement")
        self.move(0, 0)
        self.resize(250, 150)
        # Layout
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.label = QLabel("Duration")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        # Duration
        self.horizontalLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setValidator(QIntValidator())
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setValidator(QIntValidator())
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)
        # Curved path
        self.label_2 = QLabel("Curved Path")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.checkBox = QCheckBox()
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.checkBox)
        # Speed1
        self.label_3 = QLabel("Speed1")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.speed1 = QLineEdit()
        self.speed1.setReadOnly(True)
        self.speed1.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.speed1)
        # Speed2
        self.label_4 = QLabel("Speed2")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)
        self.speed2 = QLineEdit()
        self.speed2.setReadOnly(True)
        self.speed2.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.speed2)
        self.verticalLayout.addLayout(self.formLayout)
        # Buttons
        self.btnSpeed = QPushButton("Speed")
        self.verticalLayout.addWidget(self.btnSpeed)
        self.btnClose = QPushButton("Close")
        self.verticalLayout.addWidget(self.btnClose)
        # Spacer
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        # functions
        self.fillDuration()
        self.buttonsLink()


    def fillDuration(self):
        minTime = pm.playbackOptions(q=True, min=True)
        maxTime = pm.playbackOptions(q=True, max=True)
        minTime = int(minTime)
        maxTime = int(maxTime)
        self.lineEdit.setText(f"{minTime}")
        self.lineEdit_2.setText(f"{maxTime}")


    def buttonsLink(self):
        self.btnSpeed.clicked.connect(self.getSpeed)
        self.btnClose.clicked.connect(self.close)


    def getSpeed(self):
        # selection
        sel = pm.ls(sl=True)
        if not sel:
            pm.warning('Nothing Selected.')
            return
        # time
        startFrame = self.lineEdit.text()
        startFrame = int(startFrame)
        endFrame = self.lineEdit_2.text()
        endFrame = int(endFrame)
        duration = endFrame - startFrame + 1
        # distance
        curveCheckBox = self.checkBox.isChecked()
        if curveCheckBox:
            distance = self.getCurveLength(sel[0], startFrame, endFrame)
        else:
            distance = self.getDistance(sel[0], startFrame, endFrame)
        # Result
        print(distance)
        print(duration)
        speed = self.getVelocity(distance, duration)
        kmPerHour, meterPerSec = speed
        self.speed1.setText('%0.3f km/h' % kmPerHour)
        self.speed2.setText('%0.3f m/s' % meterPerSec)
    

    def getDistance(self, geo: str, startFrame: int, endFrame: int) -> float:
        # positions
        pm.currentTime(startFrame)
        startPos = pm.xform(geo, q=True, ws=True, rp=True)
        pm.currentTime(endFrame)
        endPos = pm.xform(geo, q=True, ws=True, rp=True)
        # result
        startVector = pm.datatypes.Vector(startPos)
        endVector = pm.datatypes.Vector(endPos)
        distance = startVector.distanceTo(endVector)
        return distance

    
    def getCurveLength(self, geo: str, startFrame: int, endFrame: int) -> str:
        # positions every frame
        positions = []
        for i in range(startFrame, endFrame + 1):
            pm.currentTime(i)
            try:
                positions.append(pm.pointPosition(geo))
            except:
                positions.append(pm.xform(geo, q=True, ws=True, rp=True))
        cuv = pm.curve(p=positions)
        # result
        cuvLength = pm.arclen(cuv)
        return cuvLength

    
    def getVelocity(self, distance, duration):
        # Convert Units to Centimeters.
        currUnitTime = pm.currentUnit(q=True, t=True)
        currUnitLength = pm.currentUnit(q=True, l=True)
        convertCentimeter = distance * self.unitLengthIndex[currUnitLength]
        # fps -> second
        if 'fps' in currUnitTime:
            sec = duration / float(currUnitTime.split('fps')[0])
        else:
            sec = duration / self.unitTimeIndex[currUnitTime]
        # result
        kmPerHour = (convertCentimeter/self.unitLengthIndex['km'])/(sec/60/60)
        kmPerHour = round(kmPerHour, 3)
        meterPerSec = (convertCentimeter/self.unitLengthIndex['m'])/sec
        meterPerSec = round(meterPerSec, 3)
        return kmPerHour, meterPerSec
    

if __name__ == "__main__":
    try:
        spd.close()
        spd.deleteLater()
    except:
        pass
    spd = Speed()
    spd.show()