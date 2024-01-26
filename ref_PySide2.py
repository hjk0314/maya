from PySide2.QtWidgets import QApplication, QWidget, \
QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
QFormLayout, QSpinBox
from PySide2.QtCore import Qt


# =============================================================================
# First way to create an object. ==============
class Ref1(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.show()
# ref1 = Ref1()


# First way to create an object. ==============
class Ref2(QWidget):
    def __init__(self):
        super(Ref2, self).__init__()
# ref2 = Ref2()
# ref2.show()
# =============================================================================


# =============================================================================
class Ref3(QWidget):
    def __init__(self):
        super(Ref3, self).__init__()
        self.setWindowTitle("Ref3's Test")
        self.vb = QVBoxLayout()
        self.setLayout(self.vb)
        self.hbTop = QHBoxLayout()
        self.hbMid = QHBoxLayout()
        self.hbBot = QHBoxLayout()
        self.vb.addLayout(self.hbTop)
        self.vb.addLayout(self.hbMid)
        self.vb.addLayout(self.hbBot)
        self.vb.addStretch()
        self.lbl = QLabel("Example of Box Layout")
        self.ln = QLineEdit()
        self.btn1 = QPushButton("Print")
        self.btn2 = QPushButton("Delete")
        self.btn3 = QPushButton("Print and Delte")
        self.hbTop.addWidget(self.lbl)
        self.hbMid.addWidget(self.ln)
        self.hbMid.addWidget(self.btn1)
        self.hbBot.addWidget(self.btn2)
        # self.vb.addStretch()
        self.hbBot.addWidget(self.btn3)
        self.btn1.clicked.connect(self.prt_line)
        self.btn2.clicked.connect(self.del_line)
        self.btn3.clicked.connect(self.prt_del)


    def prt_line(self):
        print(self.ln.text())


    def del_line(self):
        self.ln.clear()
    

    def prt_del(self):
        self.prt_line()
        self.del_line()
# ref3 = Ref3()
# ref3.show()
# =============================================================================


# =============================================================================
class Ref4(QWidget):
    def __init__(self):
        super(Ref4, self).__init__()
        # set title
        self.setWindowTitle("Form Layout")
        self.setObjectName('hjk0314')
        # create a Form layout.
        self.form = QFormLayout()
        self.setLayout(self.form)
        # name field
        self.lnName = QLineEdit()
        self.form.addRow("Name: ", self.lnName)
        # id field
        self.lnId = QLineEdit()
        self.btnFindId = QPushButton("Check Same")
        self.vbId = QHBoxLayout()
        self.vbId.addWidget(self.lnId)
        self.vbId.addWidget(self.btnFindId)
        self.form.addRow("ID: ", self.vbId)
        # parent's phone number field
        self.lnPNum2 = QLineEdit()
        self.form.addRow("Parent's Phone: ", self.lnPNum2)
        # Case "addWidget" to use
        self.lblChkId = QLabel("ID Check Please.")
        self.form.addWidget(self.lblChkId)
        # Case "addRow" to use
        self.btnOk = QPushButton("Confirm")
        self.form.addRow(self.btnOk)
        # about QSpinBox
        self.spAge = QSpinBox()
        self.spAge.setValue(19)
        self.lnPNum = QLineEdit()
        self.form.addRow("Age: ", self.spAge)
        self.form.addRow("Phone: ", self.lnPNum)
        # spacing samples
        # self.form.setHorizontalSpacing(100)
        # self.form.setVerticalSpacing(100)
        self.form.setLabelAlignment(Qt.AlignLeft)
        # Actions
        self.spAge.valueChanged.connect(self.chk_age)
        self.btnFindId.clicked.connect(self.chk_id)
        self.btnOk.clicked.connect(self.chk_ok)


    def chk_age(self):
        val = self.spAge.value()
        if val < 20:
            self.lnPNum2.setEnabled(True)
            self.lnPNum2.setStyleSheet("")
        else:
            self.lnPNum2.setEnabled(False)
            self.lnPNum2.setStyleSheet("background-color: grey;")


    def chk_id(self):
        ids = ["python", "tamanke"]
        if len(self.lnId.text()) < 2:
            self.lblChkId.setText("Must be at least 2 characters.")
        else:
            if ids.count(self.lnId.text()) == 1:
                self.lblChkId.setText("Duplicated ID")
            else:
                self.lblChkId.setText("Nice ID.")


    def chk_ok(self):
        checkStr = ""
        if self.lnName.text() == "":
            checkStr += "Name, "
        if self.lblChkId.text() != "Nice ID.":
            checkStr += "ID, "
        if len(self.lnPNum.text()) < 13:
            checkStr += "Phone"
        if checkStr != "":
            self.btnOk.setText(checkStr + "Check this field.")
        else:
            self.btnOk.setText("Everything is fine.")


if __name__ == '__main__':
    ref4 = Ref4()
    ref4.show()
    print(ref4.objectName())
# =============================================================================


