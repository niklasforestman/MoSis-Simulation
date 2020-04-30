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


class GUI(QMainWindow):
    def __init__(self,queue):
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Events Isolation')
        self.setFixedSize(250, 150)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createButtons(queue)


    def _createButtons(self,queue):

        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'-': (0, 0),
                   'activate': (0, 1),
                   '+': (0, 2),
                   }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():

            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 60)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            # Add buttonsLayout to the general layout
            self.generalLayout.addLayout(buttonsLayout)

        self.buttons['-'].clicked.connect(partial(isolation_down, queue))
        self.buttons['activate'].clicked.connect(partial(isolation_activate, queue))
        self.buttons['+'].clicked.connect(partial(isolation_up, queue))

def gui(queue):
    """Main function."""
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Show  GUI
    view = GUI(queue)
    view.show()
    # Execute main loop
    sys.exit(app.exec_())


def isolation_down(queue):
    queue.put('isolation_down')


def isolation_up(queue):
    queue.put('isolation_up')


def isolation_activate(queue):
    queue.put('isolation_activate')