from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from multiprocessing import Process, Queue
from functools import partial
import sys
from params import Params


params = Params()   #needed for inital values of event parameters

class GUI(QMainWindow):
    def __init__(self,queue):   #queue ist the communication channel between main and GUI process
        super().__init__()
        self.setWindowTitle('population control')
        self.setGeometry(1200,500, 150,150)   # setGeometry( x, y, width, height)
        #Layout and QWidget creation
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        #initialise parameters
        self.event_isolation_population = params.event_isolation_population
        self.event_isolation_active = params.event_isolation_active
        self.event_cure_rate = params.event_cure_rate
        self.event_vaccination_rate = params.event_vaccination_rate

        self._createButtons(queue)



    def _createButtons(self,queue):


        buttonsLayout = QGridLayout()

        #row isolation
        self.label1 = QLabel('call for isolation:')
        buttonsLayout.addWidget(self.label1, 0 ,0)  # add label1 to layout; 0, 0 is position

        self.button_isolation_down = QPushButton('<')
        self.button_isolation_down.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_isolation_down, 0, 1)

        self.label2 = QLabel(str(self.event_isolation_population) + ' %')
        buttonsLayout.addWidget(self.label2, 0, 2)

        self.button_isolation_up = QPushButton('>')
        self.button_isolation_up.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_isolation_up, 0, 3)

        self.button_isolation_activate = QPushButton('activate')
        self.button_isolation_activate.setFixedSize(120, 60)
        buttonsLayout.addWidget(self.button_isolation_activate, 0, 4)


        #row vaccination rate
        self.label_vaccination_text = QLabel('vaccination rate:')
        buttonsLayout.addWidget(self.label_vaccination_text, 1 ,0)

        self.button_vaccination_down = QPushButton('<')
        self.button_vaccination_down.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_vaccination_down, 1, 1)

        self.label_vaccination_rate = QLabel(str(self.event_vaccination_rate) + ' %')
        buttonsLayout.addWidget(self.label_vaccination_rate, 1, 2)

        self.button_vaccination_up = QPushButton('>')
        self.button_vaccination_up.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_vaccination_up, 1, 3)

        self.button_vaccination_activate = QPushButton('vaccinate')
        self.button_vaccination_activate.setFixedSize(120, 60)
        buttonsLayout.addWidget(self.button_vaccination_activate, 1, 4)

        #row cure rate
        self.label_cure_text = QLabel('cure rate:')
        buttonsLayout.addWidget(self.label_cure_text, 2, 0)

        self.button_cure_rate_down = QPushButton('<')
        self.button_cure_rate_down.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_cure_rate_down, 2, 1)

        self.label_cure_rate = QLabel(str(self.event_cure_rate) + ' %')
        buttonsLayout.addWidget(self.label_cure_rate, 2, 2)

        self.button_cure_rate_up = QPushButton('>')
        self.button_cure_rate_up.setFixedSize(60, 60)
        buttonsLayout.addWidget(self.button_cure_rate_up, 2, 3)

        self.button_cure_activate = QPushButton('cure')
        self.button_cure_activate.setFixedSize(120, 60)
        buttonsLayout.addWidget(self.button_cure_activate, 2, 4)


        self.generalLayout.addLayout(buttonsLayout)    # add buttonlayout to the main window layout

        # connect buttons with functions
        self.button_isolation_down.clicked.connect(partial(self.isolation_down, queue))  #partial is used because the function needs an argument
        self.button_isolation_activate.clicked.connect(partial(self.isolation_activate, queue))
        self.button_isolation_up.clicked.connect(partial(self.isolation_up, queue))
        self.button_vaccination_down.clicked.connect(partial(self.vaccination_down, queue))
        self.button_vaccination_activate.clicked.connect(partial(self.vaccination_activate, queue))
        self.button_vaccination_up.clicked.connect(partial(self.vaccination_up, queue))
        self.button_cure_rate_down.clicked.connect(partial(self.cure_rate_down, queue))
        self.button_cure_activate.clicked.connect(partial(self.cure_activate, queue))
        self.button_cure_rate_up.clicked.connect(partial(self.cure_rate_up, queue))

    def isolation_up(self,queue):
        queue.put('isolation_up') # the string 'isolation_up' is transferred to the communication channel
        self.event_isolation_population += 5
        self.label2.setText(str(self.event_isolation_population) + ' %')   #updates value in the GUI

    def isolation_down(self,queue):
        queue.put('isolation_down')
        self.event_isolation_population -= 5
        self.label2.setText(str(self.event_isolation_population) + ' %')

    def isolation_activate(self,queue):
        queue.put('isolation_activate')
        if self.event_isolation_active:
            self.event_isolation_active = False
            self.button_isolation_activate.setText('activate')
        else:
            self.event_isolation_active = True
            self.button_isolation_activate.setText('deactivate')


    def vaccination_up(self,queue):
        queue.put('vaccination_up')
        self.event_vaccination_rate += 5
        self.label_vaccination_rate.setText(str(self.event_vaccination_rate) + ' %')

    def vaccination_down(self,queue):
        queue.put('vaccination_down')
        self.event_vaccination_rate -= 5
        self.label_vaccination_rate.setText(str(self.event_vaccination_rate) + ' %')

    def vaccination_activate(self,queue):
        queue.put('vaccination_activate')

    def cure_rate_up(self,queue):
        queue.put('cure_rate_up')
        self.event_cure_rate += 5
        self.label_cure_rate.setText(str(self.event_cure_rate) + ' %')

    def cure_rate_down(self,queue):
        queue.put('cure_rate_down')
        self.event_cure_rate -= 5
        self.label_cure_rate.setText(str(self.event_cure_rate) + ' %')

    def cure_activate(self,queue):
        queue.put('cure_activate')

# main function for the gui
def gui(queue):
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Show  GUI
    view = GUI(queue)
    view.show()
    # Execute main loop
    sys.exit(app.exec_())

