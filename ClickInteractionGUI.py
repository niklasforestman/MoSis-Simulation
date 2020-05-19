
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QWidget, QPushButton, QVBoxLayout , QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class myApplication:
    def __init__(self):
        self.windowXPos = 320
        self.windowYPos = 150

        self.appWidth = 400
        self.appHeight = 600

        self.window = QWidget()
        self.window.setWindowTitle('PyQt5 App')
        #self.window.setGeometry(self.windowXPos, self.windowYPos, self.appHeight, self.appWidth)

        self.reInit()

    def reInit(self):
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

    def makeCenterLabel(self,title,layout, type):
        self.helloMsg = QLabel(title, parent=self.window)

        if type == 'bold':
            self.myFont= QFont()
            self.myFont.setBold(True)
        else:
            self.myFont = QFont()

        self.helloMsg.setFont(self.myFont)
        self.helloMsg.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.helloMsg)
        #self.window.show()

    def makeLeftLabel(self,title,layout,type):
        self.helloMsg = QLabel(title, parent=self.window)

        if type == 'bold':
            self.myFont= QFont()
            self.myFont.setBold(True)
        else:
            self.myFont = QFont()

        self.helloMsg.setFont(self.myFont)
        self.helloMsg.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.helloMsg)
        #self.window.show()


    def createBushButton(self, title, action,layout):
        self.button = QPushButton(title, parent=self.window)
        layout.addWidget(self.button)
        self.button.clicked.connect(action)    #verbindet das Signal 'button.clicked' mit einem Slot in den ''
        #self.button.show()

    def createLineEdit(self, data, layout):
        self.lineEdit = QLineEdit(str(data), parent=self.window)
        layout.addWidget(self.lineEdit)
        self.lineEdit.setText(str(data))
        #self.lineEdit.show()

    def createLabeledLineEdit(self,label, data, layout):
        self.labeledLineEdit = QHBoxLayout()
        self.makeLabel(label, self.labeledLineEdit, 'normal')
        self.createLineEdit(data, self.labeledLineEdit)
        layout.addLayout(self.labeledLineEdit)

    def printSomething(self):
        print('I printed something')

