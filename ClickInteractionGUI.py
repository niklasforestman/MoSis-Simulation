
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QWidget, QPushButton, QVBoxLayout , QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#GUI - Bibliotheken
from PyQt5 import QtWidgets, QtCore #QLineEdit #QLineEdit
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
import sys #Wird zum Schließen des Programms benötigt

class myApplication(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        '''
        self.windowXPos = 320
        self.windowYPos = 150

        self.appWidth = 400
        self.appHeight = 600

        self.window = QWidget()
        self.window.setWindowTitle('PyQt5 App')
        #self.window.setGeometry(self.windowXPos, self.windowYPos, self.appHeight, self.appWidth)


        self.window.setLayout(self.layout)
        '''
        self.guiInteractionSetup()

        #self.reInit()

    def reInit(self):

        self.layout = QtWidgets.QVBoxLayout()
        self.window.setLayout(self.layout)



    def guiInteractionSetup(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.schroedingersLabel = QtWidgets.QLabel(self)
        self.schroedingersLabel.setText('Zustand 1')
        self.AuswahlLeben = QtWidgets.QComboBox()
        self.AuswahlLeben.addItems(['Leben', 'Sterben'])

        self.labelImmun = QtWidgets.QLabel(self)
        self.labelImmun.setText('Zustand 2')
        self.AuswahlLeben = QtWidgets.QComboBox()
        self.AuswahlLeben.addItems(['immun', 'nicht immun'])

        self.labelIsolated = QtWidgets.QLabel(self)
        self.labelIsolated.setText('Zustand 3')
        self.AuswahlIsolated = QtWidgets.QComboBox()
        self.AuswahlIsolated.addItems(['isoliert', 'nicht isoliert'])

        self.labelInfected = QtWidgets.QLabel(self)
        self.labelInfected.setText('Zustand 4')
        self.AuswahlInfected = QtWidgets.QComboBox()
        self.AuswahlInfected.addItems(['ifiziert', 'nicht infiziert'])

        self.labelSick = QtWidgets.QLabel(self)
        self.labelSick.setText('Zustand 5')
        self.AuswahlInfected = QtWidgets.QComboBox()
        self.AuswahlInfected.addItems(['ifiziert', 'nicht infiziert'])







        self.layout.addWidget(self.schroedingersLabel)
        self.layout.addWidget(self.AuswahlLeben)

        self.setLayout(self.layout)







if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    interactionGUI = myApplication()
    # auswertung.plot()
    interactionGUI.show()
    ret = app.exec_()
    sys.exit(ret)
'''
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
'''
