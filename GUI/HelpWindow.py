from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget


class HelpWindow(QDialog):
    # constructor
    def __init__(self, widget):
        super(HelpWindow, self).__init__()
        # Load the ui window
        loadUi("Gui/helpWindow.ui", self)
        # Queue Frames
        self.widget = widget
        # Home Button
        self.homeB = self.findChild(QtWidgets.QPushButton, "backB")
        self.homeB.clicked.connect(self.goToBack)

    def goToBack(self):
        self.deleteLater()