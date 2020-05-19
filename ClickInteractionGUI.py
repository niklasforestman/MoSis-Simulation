
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

import person

class guiErstellen():
    def __init__(self, Proband):
        app = QtWidgets.QApplication([])
        interactionGUI = myApplication(Proband)

        interactionGUI.show()
        ret = app.exec_()
        sys.exit(ret)


class myApplication(QtWidgets.QWidget):
    def __init__(self, person):
        super().__init__()
        self.derAuserwaelhte = person

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

    def werteEintragen(self):
        print(self.derAuserwaelhte.immune)
        if self.AuswahlLeben.currentText() == 'Leben':
            self.derAuserwaelhte.alive = True
            self.derAuserwaelhte.dead = False
        else:
            self.derAuserwaelhte.alive = False
            self.derAuserwaelhte.dead = True

        if self.AuswahlImmune.currentText() == 'immun':
            self.derAuserwaelhte.immune = True
        else:
            self.derAuserwaelhte.immune = False

        if self.AuswahlIsolated.currentText() == 'isoliert':
            self.derAuserwaelhte.isolated = True
        else:
            self.derAuserwaelhte.isolated = False

        if self.AuswahlInfected.currentText() == 'infiziert':
            self.derAuserwaelhte.infected = True
        else:
            self.derAuserwaelhte.infected = False

        if self.AuswahlSick.currentText() == 'krank':
            self.derAuserwaelhte.sick = True
        else:
            self.derAuserwaelhte.sick = False

        if self.AuswahlHeavy.currentText() == 'schwer':
            self.derAuserwaelhte.heavy = True
        else:
            self.derAuserwaelhte.heavy = False

        if self.AuswahlSuperspread.currentText() == 'Superspread':
            self.derAuserwaelhte.superspread = True
        else:
            self.derAuserwaelhte.superspread = False


        print(self.derAuserwaelhte.immune )


    def guiInteractionSetup(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.schroedingersLabel = QtWidgets.QLabel(self)
        self.schroedingersLabel.setText('Zustand 1')
        self.AuswahlLeben = QtWidgets.QComboBox()
        self.AuswahlLeben.addItems(['Leben', 'Sterben'])

        self.labelImmune = QtWidgets.QLabel(self)
        self.labelImmune.setText('Zustand 2')
        self.AuswahlImmune = QtWidgets.QComboBox()
        self.AuswahlImmune.addItems(['immun', 'nicht immun'])

        self.labelIsolated = QtWidgets.QLabel(self)
        self.labelIsolated.setText('Zustand 3')
        self.AuswahlIsolated = QtWidgets.QComboBox()
        self.AuswahlIsolated.addItems(['isoliert', 'nicht isoliert'])

        self.labelInfected = QtWidgets.QLabel(self)
        self.labelInfected.setText('Zustand 4')
        self.AuswahlInfected = QtWidgets.QComboBox()
        self.AuswahlInfected.addItems(['infiziert', 'nicht infiziert'])

        self.labelSick = QtWidgets.QLabel(self)
        self.labelSick.setText('Zustand 5')
        self.AuswahlSick = QtWidgets.QComboBox()
        self.AuswahlSick.addItems(['krank', 'nicht krank'])

        self.labelHeavy = QtWidgets.QLabel(self)
        self.labelHeavy.setText('Zustand 6')
        self.AuswahlHeavy = QtWidgets.QComboBox()
        self.AuswahlHeavy.addItems(['schwer', 'nicht schwer'])

        self.labelSuperspread = QtWidgets.QLabel(self)
        self.labelSuperspread.setText('Zustand 7')
        self.AuswahlSuperspread = QtWidgets.QComboBox()
        self.AuswahlSuperspread.addItems(['Superspread', 'kein Superspread'])

        self.button1 = QtWidgets.QPushButton('Auswahl Bestätigen')
        self.button1.clicked.connect(self.werteEintragen)







        self.layout.addWidget(self.schroedingersLabel)
        self.layout.addWidget(self.AuswahlLeben)

        self.layout.addWidget(self.labelImmune)
        self.layout.addWidget(self.AuswahlImmune)

        self.layout.addWidget(self.labelIsolated)
        self.layout.addWidget(self.AuswahlIsolated)

        self.layout.addWidget(self.labelInfected)
        self.layout.addWidget(self.AuswahlInfected)

        self.layout.addWidget(self.labelSick)
        self.layout.addWidget(self.AuswahlSick)

        self.layout.addWidget(self.labelHeavy)
        self.layout.addWidget(self.AuswahlHeavy)

        self.layout.addWidget(self.labelSuperspread)
        self.layout.addWidget(self.AuswahlSuperspread)

        self.layout.addWidget(self.button1)

        self.setLayout(self.layout)







if __name__ == '__main__':

    Proband = person.Person(False, False, False, False, False, False )

    app = QtWidgets.QApplication([])
    interactionGUI = myApplication(Proband)

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
