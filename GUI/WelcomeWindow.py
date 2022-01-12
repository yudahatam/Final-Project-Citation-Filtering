from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
from ParameterWindow import ParameterWindow
from HelpWindow import HelpWindow


class WelcomeWindow(QDialog):
    # constructor
    def __init__(self, widget):
        super(WelcomeWindow, self).__init__()
        # Load the ui window
        loadUi("Gui/welcomeWindow.ui", self)
        # Queue Frames
        self.widget = widget
        # Start Button
        self.startB = self.findChild(QtWidgets.QPushButton, "startB")
        self.startB.clicked.connect(self.goToParameter)
        # help button
        self.helpB = self.findChild(QtWidgets.QPushButton, "helpB")
        self.helpB.clicked.connect(self.goToHelp)

    def goToParameter(self):
        parameterWind = ParameterWindow(self.widget)
        self.widget.addWidget(parameterWind)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goToHelp(self):
        helpWindow = HelpWindow(self.widget)
        self.widget.addWidget(helpWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
