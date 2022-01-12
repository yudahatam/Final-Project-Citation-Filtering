import argparse
import sys
import time

from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog, QSpinBox, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

import embeddingTraining
import embeddingTraining as alg
import param_parser as param
from GUI.ResultWindow import ResultWindow
from GUI.HelpWindow import HelpWindow
from utils import graph_reader


class ParameterWindow(QDialog):
    # constructor

    def __init__(self, widget):
        super(ParameterWindow, self).__init__()
        # Load the ui window
        loadUi("Gui/parameterWindow.ui", self)
        # Queue Frames
        self.widget = widget
        # back button
        self.backB = self.findChild(QtWidgets.QPushButton, "backB")
        self.backB.clicked.connect(self.goToBack)
        # home button
        self.homeB = self.findChild(QtWidgets.QPushButton, "homeB")
        self.homeB.clicked.connect(self.goToBack)
        # help button
        self.helpB = self.findChild(QtWidgets.QPushButton, "helpB")
        self.helpB.clicked.connect(self.goToHelp)
        # Go button
        self.goB = self.findChild(QtWidgets.QPushButton, "goB")
        self.goB.setEnabled(False)
        self.goB.clicked.connect(self.startTraining)
        # BrowseFile button
        self.browseFile = self.findChild(QtWidgets.QPushButton, "browseFile")
        self.browseFile.clicked.connect(self.UploadFile)
        # browserText
        self.browserText = self.findChild(QtWidgets.QTextEdit, "browserText")
        self.browserText2 = self.findChild(QtWidgets.QTextEdit, "browserText_2")
        # PercentageGraphCore
        self.percentageGraphCore = self.findChild(QSpinBox, "precentageGraphCore")
        # Number of training
        self.numOfTraining = self.findChild(QSpinBox, 'numoftraining')
        # Nodes and edges label
        self.amountLabel = self.findChild(QLabel, 'amountlabel')
        self.amountLabel.hide()

    def startTraining(self, args=None):
        percent = self.percentageGraphCore.text()
        numOfTraining = self.numOfTraining.text()
        args = param.parameter_parser()
        path = self.browserText.toPlainText()
        args.edge_path = path
        stringArr = path.split('/')
        fileNAme = stringArr[len(stringArr) - 1]
        fileNAme = fileNAme.split('.')[0]
        args.embedding_output_path = '../output/{}.csv'.format(fileNAme)
        args.percent = int(percent)
        args.training = int(numOfTraining)
        embeddingTraining.embeddingTraining(args)
        # go to result window
        orgGraph = graph_reader(path)
        coreGraph = graph_reader('../output/' + fileNAme + "_Core.edgelist")
        resultWindow = ResultWindow(self.widget, percent, numOfTraining, orgGraph, coreGraph)
        self.widget.addWidget(resultWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goToBack(self):
        self.deleteLater()

    def goToHelp(self):
        helpWindow = HelpWindow(self.widget)
        self.widget.addWidget(helpWindow)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def UploadFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        fname = QFileDialog.getOpenFileName()
        sp = fname[0].split('/')
        sp1 = sp[len(sp) - 1].split('.')
        fileType = sp1[len(sp1) - 1]
        if fileType != "edgelist":
            self.browserText.setTextColor(QColor(255, 0, 0))
            self.browserText.setPlainText("please choose valid edgelist file!!!")
            self.goB.setEnabled(False)
        else:
            tempGraph = graph_reader(fname[0])
            self.amountLabel.setText(
                "Number of nodes = {}\nNumber of edges = {}".format(len(tempGraph.nodes), len(tempGraph.edges)))
            self.amountLabel.show()
            self.browserText.setTextColor(QColor(0, 0, 255))
            self.browserText.setPlainText(fname[0])
            self.goB.setEnabled(True)
