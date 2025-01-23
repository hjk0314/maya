import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindow_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindow_pointer), QWidget)



class MoveToCameraKeysAndSequence(QWidget):
    def __init__(self):
        super(MoveToCameraKeysAndSequence, self).__init__()
        self.setParent(mayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("Offset Camera's Keys And ImageSequences")
        self.move(0, 0)
        self.resize(210, 75)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblKeyframe = QLabel("Keyframes")
        self.lblKeyframe.setObjectName(u"lblKeyframe")
        self.horizontalLayout.addWidget(self.lblKeyframe)
        self.txtKey = QLineEdit()
        self.txtKey.setObjectName(u"txtKeyStep")
        self.txtKey.setValidator(QIntValidator())
        self.txtKey.setText("0")
        self.horizontalLayout.addWidget(self.txtKey)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnOffset = QPushButton("Move Keyframes and imgPlane")
        self.btnOffset.setObjectName(u"btnOffset")
        self.verticalLayout.addWidget(self.btnOffset)
        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.buttonsLink()


    def buttonsLink(self):
        self.btnOffset.clicked.connect(self.moveToKeyframe)


    def moveToKeyframe(self):
        key = self.txtKey.text()
        try:
            key = int(key)
        except:
            pm.warning("Nothing inputs")
            return
        sel = pm.ls(sl=True, dag=True, type=['camera'])
        cam = pm.listRelatives(sel, p=True)
        img = pm.listRelatives(sel, c=True)
        imgShape = pm.listRelatives(img, c=True)
        if not sel:
            pm.warning("Select a Camera")
            return
        if not img:
            pm.warning("There is no imagePlane.")
            return
        else:
            try:
                currentKey = min(pm.keyframe(cam, q=True))
                value = key - currentKey
            except:
                pm.setKeyframe(cam, s=False, t=1)
                value = key - 1
            pm.keyframe(cam, e=True, r=True, tc=value)
            frameOffset = pm.getAttr(imgShape[0] + ".frameOffset")
            pm.setAttr(imgShape[0] + ".frameOffset", frameOffset - value)


# if __name__ == "__main__":
#     try:
#         offsetCam.close()
#         offsetCam.deleteLater()
#     except:
#         pass
#     offsetCam = MoveToCameraKeysAndSequence()
#     offsetCam.show()

