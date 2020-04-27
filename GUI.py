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


class GUI_Test(QMainWindow):
    def __init__(self,queue):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('GUI Test')
        self.setFixedSize(500, 500)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtons(queue)

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)



    def _createButtons(self,queue):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'-': (0, 0),
                   'o': (0, 1),
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
        self.buttons['o'].clicked.connect(partial(isolation_activate, queue))
        self.buttons['+'].clicked.connect(partial(isolation_up, queue))

def gui(queue):
    """Main function."""
    # Create an instance of QApplication
    test = QApplication(sys.argv)
    # Show the calculator's GUI
    view = GUI_Test(queue)
    view.show()
    view.display.setText("Test")
    # Execute the calculator's main loop
    sys.exit(test.exec_())


def isolation_down(queue):
    queue.put('isolation_down')


def isolation_up(queue):
    queue.put('isolation_up')


def isolation_activate(queue):
    queue.put('isolation_activate')