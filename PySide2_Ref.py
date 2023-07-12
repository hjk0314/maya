from PySide2.QtWidgets import QApplication, QWidget, \
QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel


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

