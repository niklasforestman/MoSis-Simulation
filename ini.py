import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from params import Params
parameter = Params()

class Dialog(QDialog):
    """Dialog."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Parameter')
        self.setAttribute(Qt.WA_DeleteOnClose)
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()

        #create lines
        self.line1 = QLineEdit()
        self.line1.setText(str(parameter.isolation)) #set start text
        self.line1.setAlignment(Qt.AlignRight)  #text is on the right site
        self.line2 = QLineEdit()
        self.line2.setText(str(parameter.infected))
        self.line2.setAlignment(Qt.AlignRight)
        self.line3 = QLineEdit()
        self.line3.setText(str(parameter.infection_chance))
        self.line3.setAlignment(Qt.AlignRight)
        self.line4 = QLineEdit()
        self.line4.setText(str(parameter.recovery))
        self.line4.setAlignment(Qt.AlignRight)
        self.line5 = QLineEdit()
        self.line5.setText(str(parameter.heavy_case))
        self.line5.setAlignment(Qt.AlignRight)
        self.line6 = QLineEdit()
        self.line6.setText(str(parameter.incubation_time))
        self.line6.setAlignment(Qt.AlignRight)
        self.line7 = QLineEdit()
        self.line7.setText(str(parameter.superspreader))
        self.line7.setAlignment(Qt.AlignRight)
        self.line8 = QLineEdit()
        self.line8.setText(str(parameter.testrate))
        self.line8.setAlignment(Qt.AlignRight)


        #add lines and text to the Layout
        formLayout.addRow('constant of isolation:', self.line1)
        formLayout.addRow('infection at the beginning:', self.line2)
        formLayout.addRow('probability of infection:', self.line3)
        formLayout.addRow('probaility of cure:', self.line4)
        formLayout.addRow('heavy cases:', self.line5)
        formLayout.addRow('time of incubation:', self.line6)
        formLayout.addRow('superspreader:', self.line7)
        formLayout.addRow('testrate:', self.line8)

        dlgLayout.addLayout(formLayout)
        #create buttons
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dlgLayout.addWidget(btns)
        self.setLayout(dlgLayout)
        #connect buttons to the functions
        btns.accepted.connect(self.set_values)
        btns.rejected.connect(self.closeIt)





    def set_values(self):
        parameter.isolation = int(self.line1.text())
        parameter.infected = int(self.line2.text())
        parameter.infection_chance = int(self.line3.text())
        parameter.recovery = int(self.line4.text())
        parameter.heavy_case = int(self.line5.text())
        parameter.incubation_time = int(self.line6.text())
        parameter.superspreader = int(self.line7.text())
        parameter.testrate = int(self.line8.text())
        self.close() #closes dialogue

    def closeIt(self):
        self.close()

#function for returning values
def new_parameter():
    return parameter




# main function for dialogue
def ini_start():
    app2 = QApplication(sys.argv)  #create window
    #show dialogue
    dlg = Dialog()
    dlg.show()
    app2.exec_()  #run dialogue

