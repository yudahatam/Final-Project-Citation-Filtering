import argparse
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog, QSpinBox, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi


class ResultWindow(QDialog):
    # constructor
    def __init__(self, widget,percent,numOfTraining,orgGraph,coreGraph):
        super(ResultWindow, self).__init__()
        # Load the ui window
        loadUi("Gui/resultWindow.ui", self)
        # Queue Frames
        self.widget = widget
        self.widget.setFixedHeight(750)
        self.widget.setFixedWidth(1300)
        # Exit button
        hen=self.findChild(QLabel,"variables")
        hen.setText("Variables chosen by user:\t\t\tOriginal\tCore\n  percentage of core:\t{}\tNodes:\t{}\t{}\n  "
                    "amount of training:\t{}\tEdges:\t{}\t{}".format(percent,len(orgGraph.nodes),
                                                                     len(coreGraph.nodes),numOfTraining,
                                                                     len(orgGraph.edges),len(coreGraph.edges)))
        self.originalGraph=self.findChild(QtWidgets.QLabel, "orig")
        self.originalGraph.setScaledContents(True)
        self.originalGraph.setStyleSheet("border:1px solid black;")
        im=QPixmap('../images/graphOrg.jpg')
        self.originalGraph.setPixmap(im)
        self.coreGraph=self.findChild(QtWidgets.QLabel, "newim")
        self.coreGraph.setScaledContents(True)
        self.coreGraph.setStyleSheet("border:1px solid black;")
        im2 = QPixmap('../images/newGraph.jpg')
        self.coreGraph.setPixmap(im2)
        self.exitB = self.findChild(QtWidgets.QPushButton, "exitB")
        self.exitB.clicked.connect(self.goToExit)

    def goToExit(self):
        sys.exit()