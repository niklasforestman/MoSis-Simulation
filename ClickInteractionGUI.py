

#GUI - Bibliotheken
from PyQt5 import QtWidgets

import sys #Wird zum Schließen des Programms benötigt

import person

#Das hier ist Eine Klasse, in der die GUI mittels einer App gestartet wird
#Als Input wird immer die angeklickte Person durchgereicht
#Wozu genau was da ist weiß ich nicht - aber es funktioniert so :)
class guiErstellen():
    def __init__(self, Proband):
        app = QtWidgets.QApplication([])
        interactionGUI = myApplication(Proband)

        interactionGUI.show()
        ret = app.exec_()


#In dieser Klasse wird die GUI erstellt
#Die Klasse erbt von QtWisgets
class myApplication(QtWidgets.QWidget):
    def __init__(self, person):
        #mit super().__init__() wird die init von QtWidget aufgerufen und auch die von allen anderen Klassen von denen geerbt wird
        super().__init__()
        #hier wird einmal eine Person für diese Klasse festgelegt, damit wir die verschiedenen Variablen der ausgewählten Person ändern können
        self.derAuserwaelhte = person

        self.guiInteractionSetup()


        '''
        def reInit(self):

        self.layout = QtWidgets.QVBoxLayout()
        self.window.setLayout(self.layout)
        '''

#hier wird abhängig von den eingaben ain der GUI der jeweilige Wert der Parameter der Person geändert
    def werteEintragen(self):

        #kurze Statusausgabe
        print(self.derAuserwaelhte.immune)
        print(self.derAuserwaelhte.isolated)

        #mit currentText() kann der Text einer Combobox ausgelesen werden
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

        #statusausgabe
        print(self.derAuserwaelhte.immune )
        print(self.derAuserwaelhte.isolated)



    def guiInteractionSetup(self):
        #es wird ein layout vom Typ QVBoxlayout erstellt
        self.layout = QtWidgets.QVBoxLayout()
        #dem Layout unserer GUI wird das erstellte Layout zugewiesen
        self.setLayout(self.layout)


        #es werden die einzelnen Elemente der GUI erstellt

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





        #es werden die einzelnen Elemente dem Layout hinzugefügt
        #dabei legt die Reihenfolge des Hinzufügens auch die Reihenfolge in der GUI fest

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

        #dem layout wird erneut das selbst erstellte layout zugewiesen
        self.setLayout(self.layout)







if __name__ == '__main__': #diese Zeile bedeutet, dass der folgende Code nur ausgeführt wird, wenn auch dieses Programm ausgeführt wird. Wird dieses Programm in einem anderen aufgerufen, wird der folgende Code nicht ausgeführt


    #Code zum Testen der GUI -> für das eigentliche Programm nicht wichtig
    Proband = person.Person(False, False, False, False, False, False )

    app = QtWidgets.QApplication([])
    interactionGUI = myApplication(Proband)

    interactionGUI.show()
    ret = app.exec_()
    sys.exit(ret)


