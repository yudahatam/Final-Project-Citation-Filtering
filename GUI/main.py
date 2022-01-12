import os
import sys
import time

import networkx as nx
from PyQt5.QtWidgets import QApplication, QStackedWidget
from matplotlib import pyplot as plt

from WelcomeWindow import WelcomeWindow
from utils import graph_reader

''''''''''''
''' Main '''
''''''''''''
app = QApplication(sys.argv)
widget = QStackedWidget()
welcome = WelcomeWindow(widget)
widget.addWidget(welcome)
widget.setFixedHeight(500)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")
