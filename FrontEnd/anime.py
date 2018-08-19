# -*- coding: utf-8 -*-
import sys
import json
import ntpath
from PyQt5 import QtWidgets, QtGui, QtCore, sip


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.grid = QtWidgets.QGridLayout()
        self.fon = QtWidgets.QVBoxLayout()
        self.count = 0

        self.label1 = QtWidgets.QLabel('1')
        self.label2 = QtWidgets.QLabel('2')
        self.label3 = QtWidgets.QLabel('3')
        self.label4 = QtWidgets.QLabel('4')
        self.labels = []
        self.button = QtWidgets.QPushButton('jojo')
        self.seizure = QtWidgets.QPushButton('4ek')

        self.init_ui()

    def init_ui(self):
        self.fon.addLayout(self.grid)

        self.fon.addWidget(self.button)
        self.fon.addWidget(self.seizure)

        self.button.clicked.connect(self.click1)
        self.seizure.clicked.connect(self.pecha)

        self.setLayout(self.fon)

    def click(self):
        label = QtWidgets.QLabel(str(self.count))
        #self.labels.append(label)
        self.grid.addWidget(label, self.count, 0)
        self.count += 1
        QtWidgets.QApplication.processEvents()
        print(label.pos())

    def pecha(self):
        for label in self.labels:
            print(label.pos())

    def click1(self):
        label = QtWidgets.QLabel('ABABABABABA')
        self.grid.addWidget(label, self.count, 0)
        self.count += 1
        QtWidgets.QApplication.processEvents()
        pos = label.pos()
        print(pos.x(), pos.y())
        height = label.height()

        self.hideAnimation = QtCore.QPropertyAnimation(label, b"geometry")
        self.hideAnimation.setDuration(40)
        startGeometry = QtCore.QRect(pos.x(), pos.y(), label.width(), 0)
        endGeometry = QtCore.QRect(pos.x(), pos.y(), label.width(), height)
        self.hideAnimation.setStartValue(startGeometry)
        self.hideAnimation.setEndValue(endGeometry)
        self.hideAnimation.start()


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.show()
sys.exit(app.exec_())
