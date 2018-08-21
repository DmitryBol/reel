# -*- coding: utf-8 -*-
import sys
import time
import ntpath
from PyQt5 import QtWidgets, QtGui, QtCore, sip


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.fon = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton('joske')
        self.frame = QtWidgets.QFrame()
        self.fon_scroll = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QWidget()
        self.scroll = QtWidgets.QScrollArea()

        self.init_ui()

    def init_ui(self):
        self.fon.addWidget(self.button)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.fon.addWidget(self.frame)
        for i in range(40):
            label = QtWidgets.QLabel(str(i))
            self.fon.addWidget(label)
        self.button.clicked.connect(self.click)

        self.widget.setLayout(self.fon)
        self.scroll.setWidget(self.widget)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.fon_scroll.addWidget(self.scroll)
        self.setLayout(self.fon_scroll)

    def click(self):
        self.anime_frame = QtCore.QPropertyAnimation(self.frame, b'geometry')
        self.anime_frame.setDuration(1600)
        self.anime_frame.setStartValue(self.frame.geometry())
        self.anime_frame.setEndValue(
            QtCore.QRect(self.frame.pos().x(), self.frame.pos().y(), self.frame.width(), self.frame.height() + 200))
        self.anime_frame.start()

        scroll = self.scroll.verticalScrollBar()
        scroll.setSingleStep(1)
        for i in range(40):
            QtCore.QTimer.singleShot(10*i, lambda: scroll.triggerAction(QtWidgets.QAbstractSlider.SliderSingleStepAdd))
            print(scroll.value())
        QtCore.QTimer.singleShot(1000, self.func)

    def func(self):
        self.frame.setStyleSheet('QFrame {color: red; background-color: #EB6C6C;}')


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.show()
sys.exit(app.exec_())
