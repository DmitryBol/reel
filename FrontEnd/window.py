# -*- coding: utf-8 -*-
import sys
import os
import json
import ntpath
import numpy as np
import FrontEnd.structure_alpha as Q
import simulate
from PyQt5 import QtWidgets, QtGui, QtCore, sip

# counts
count_tabs = 1

# colors
default_color = QtGui.QColor(220, 220, 220)
wild_color = QtGui.QColor(255, 247, 165)
scatter_color = QtGui.QColor(192, 236, 249)
wildnscatter_color = QtGui.QColor(221, 172, 225)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def isint(value):
    try:
        int(value)
        return int(value)
    except ValueError:
        return -1


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def float_validate(self, bot, top):
    sender = self.sender()
    if str(sender.text()) != '':
        try:
            if not bot <= float(sender.text()) <= top:
                raise ValueError
            sender.setStyleSheet('')
        except ValueError:
            sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')


def int_validate(self, bot, top):
    sender = self.sender()
    if str(sender.text()) != '':
        try:
            if not bot <= int(sender.text()) <= top:
                raise ValueError
            sender.setStyleSheet('')
        except ValueError:
            sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')


def string_validate(self):
    sender = self.sender()
    if str(sender.text()) == '' or ';' in str(sender.text()):
        sender.setStyleSheet('QLineEdit {background-color: #f6989d;}')
    else:
        sender.setStyleSheet('')


class Aesthetic(QtWidgets.QWidget):
    def __init__(self, obj):
        super(Aesthetic, self).__init__()

        fon = QtWidgets.QHBoxLayout()
        fon.addWidget(obj)
        fon.addStretch(40)
        self.setLayout(fon)


class MyFrame(QtWidgets.QFrame):
    def __init__(self):
        super(MyFrame, self).__init__()

        self.setLineWidth(2)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setAutoFillBackground(True)

    def _set_color(self, col):
        p = self.palette()
        p.setColor(self.backgroundRole(), col)
        self.setPalette(p)

    color = QtCore.pyqtProperty(QtGui.QColor, fset=_set_color)


class LabeledLine(QtWidgets.QWidget):
    def __init__(self, name, color):
        super(LabeledLine, self).__init__()

        self.fon = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(str(name))
        self.line = QtWidgets.QLineEdit()

        self.init_ui(color)

    def init_ui(self, color):
        self.fon.setSpacing(0)
        self.fon.addWidget(self.label)
        self.fon.addWidget(self.line)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.label.setStyleSheet('QLabel {border-left: 1px solid black; border-top: 1px solid black; border-right: none; border-bottom: 1px solid black}')
        self.label.setAutoFillBackground(True)
        p = self.label.palette()
        p.setColor(self.label.backgroundRole(), color)
        self.label.setPalette(p)

        self.setLayout(self.fon)


class LineEdits(QtWidgets.QWidget):
    def __init__(self, length, width, bot, top, height=None, space=None, double=None):
        super(LineEdits, self).__init__()

        self.fon = QtWidgets.QHBoxLayout()
        self.lines = []

        self.init_ui(length, width, bot, top, height, space, double)

    def init_ui(self, length, width, bot, top, height, space, double):
        for i in range(length):
            line = QtWidgets.QLineEdit()
            if double is None:
                line.textChanged.connect(lambda: self.int_validate(bot, top))
            else:
                line.textChanged.connect(lambda: self.float_validate(bot, top))
            self.lines.append(line)
            self.lines[i].setFixedWidth(width)
            if height is not None:
                self.lines[i].setFixedHeight(height)
            self.fon.addWidget(self.lines[i])
            if space is not None:
                self.fon.setSpacing(space)
        self.fon.addStretch(40)

        self.setLayout(self.fon)

    int_validate = int_validate
    float_validate = float_validate

    def collect_info(self):
        info = []
        for i in range(len(self.lines)):
            if isint(str(self.lines[i].text())) > 0:
                info.append([i + 1, int(str(self.lines[i].text()))])
        return info

    def arrange_info(self):
        info = []
        for i in range(len(self.lines)):
            if isint(str(self.lines[i].text())) > 0:
                info.append(int(str(self.lines[i].text())))
            else:
                return None
        return info

    def set_info(self, interim_info):
        for obj in interim_info:
            self.lines[obj[0] - 1].setText(str(obj[1]))

    def fill_info(self, interim_info):
        for i in range(len(interim_info)):
            self.lines[i].setText(str(interim_info[i]))


class SwitchButtons(QtWidgets.QWidget):
    def __init__(self, width, size):
        super(SwitchButtons, self).__init__()

        self.fon = QtWidgets.QHBoxLayout()
        self.buttons = []

        self.init_ui(width, size)

    def init_ui(self, width, size):
        for i in range(width):
            button = QtWidgets.QPushButton()
            button.setCheckable(True)

            button.setStyleSheet("QPushButton {background-color: #4CCD59; border: none;}"
                                 "QPushButton:pressed { background-color: #00A505 }"
                                 "QPushButton:focus { background-color: #4CCD59 }"
                                 "QPushButton:focus:pressed { background-color: #00A505 }"
                                 "QPushButton:hover { background-color: #27E83A }")
            button.setIcon(QtGui.QIcon('icons/allowed.png'))
            button.clicked[bool].connect(self.toggle)
            self.buttons.append(button)
            self.buttons[i].setFixedWidth(size)
            self.buttons[i].setFixedHeight(24)
            self.fon.addWidget(self.buttons[i])
        self.fon.addStretch(40)

        self.setLayout(self.fon)

    def toggle(self, pressed):
        sender = self.sender()
        if pressed:
            sender.setStyleSheet("QPushButton {background-color: #EB6C6C; border: none;}"
                                 "QPushButton:pressed { background-color: #EB4848 }"
                                 "QPushButton:focus { background-color: #EB6C6C }"
                                 "QPushButton:focus:pressed { background-color: #EB4848 }"
                                 "QPushButton:hover { background-color: #F97373 }")
            sender.setIcon(QtGui.QIcon('icons/prohibited.png'))
        else:
            sender.setAutoFillBackground(True)
            sender.setStyleSheet("QPushButton {background-color: #4CCD59; border: none;}"
                                 "QPushButton:pressed { background-color: #00A505 }"
                                 "QPushButton:focus { background-color: #4CCD59 }"
                                 "QPushButton:focus:pressed { background-color: #00A505 }"
                                 "QPushButton:hover { background-color: #27E83A }")
            sender.setIcon(QtGui.QIcon('icons/allowed.png'))

    def collect_info(self):
        info = []
        for i in range(len(self.buttons)):
            if not self.buttons[i].isChecked():
                info.append(i + 1)
        return info

    def set_info(self, interim_symbol_type):
        for i in range(len(self.buttons)):
            if i + 1 not in interim_symbol_type['position']:
                self.buttons[i].click()


class Output(QtWidgets.QFrame):
    def __init__(self, path):
        super(Output, self).__init__()

        self.fon = QtWidgets.QVBoxLayout()

        self.widget_reels = QtWidgets.QWidget()
        self.fon_reels = QtWidgets.QGridLayout()
        self.label_reels = QtWidgets.QLabel('Choose file where reels will be saved:')
        self.line_path = QtWidgets.QLineEdit()
        self.button_open = QtWidgets.QPushButton('open')

        self.table_param = QtWidgets.QTableWidget()

        self.table_simparam = QtWidgets.QTableWidget()

        self.path_reels = None

        if path is not None:
            self.set_path(path)

        self.init_ui()
        self.init_widget()
        self.init_table()

    def init_ui(self):
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fon.addWidget(self.table_param)
        self.fon.addWidget(self.widget_reels)
        self.fon.addWidget(self.table_simparam)
        self.fon.addStretch(4)
        self.fon.setContentsMargins(0, 0, 0, 0)

        self.table_simparam.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table_simparam.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_simparam.setColumnCount(2)
        self.table_simparam.setRowCount(5)
        hheader = self.table_simparam.horizontalHeader()
        hheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.table_param.hide()
        self.table_simparam.hide()

        self.setLayout(self.fon)

    def init_widget(self):
        self.fon_reels.setColumnStretch(0, 4)
        self.widget_reels.setLayout(self.fon_reels)
        self.button_open.clicked.connect(self.file_open)

        self.fon_reels.addWidget(self.label_reels, 0, 0, 1, 2)
        self.fon_reels.addWidget(self.line_path, 1, 0)
        self.fon_reels.addWidget(self.button_open, 1, 1)

    def init_table(self):
        self.table_param.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table_param.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_param.setColumnCount(2)
        self.table_param.setRowCount(4)
        hheader = self.table_param.horizontalHeader()
        hheader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def set_path(self, path):
        directory = os.path.dirname(path)
        leaf = str(path_leaf(path))
        name = leaf.split('.')[0]
        reels_path = directory + '/' + name + '_reels.txt'
        self.line_path.setText(reels_path)

    def switch_mode(self, mode):
        if mode is True:
            self.table_param.hide()
            self.widget_reels.show()
        else:
            self.table_param.show()
            self.widget_reels.hide()

    def set_simparam(self, simparam):
        self.table_simparam.setItem(0, 0, QtWidgets.QTableWidgetItem('RTP'))
        self.table_simparam.setItem(0, 1, QtWidgets.QTableWidgetItem(str(simparam['rtp'])))

        self.table_simparam.setItem(1, 0, QtWidgets.QTableWidgetItem('volatility'))
        self.table_simparam.setItem(1, 1, QtWidgets.QTableWidgetItem(str(simparam['sd'])))

        self.table_simparam.setItem(2, 0, QtWidgets.QTableWidgetItem('hitrate'))
        #self.table_simparam.setItem(2, 1, QtWidgets.QTableWidgetItem(str(simparam['hitrate'])))

        self.table_simparam.setItem(3, 0, QtWidgets.QTableWidgetItem('base RTP'))
        #self.table_simparam.setItem(3, 1, QtWidgets.QTableWidgetItem(str(simparam['base_rtp'])))

        self.table_simparam.setItem(4, 0, QtWidgets.QTableWidgetItem('wins'))
        self.table_simparam.setItem(4, 1, QtWidgets.QTableWidgetItem(str(simparam['wins'])))

        self.table_simparam.show()

    def set_param(self, parameters):
        self.table_param.setItem(0, 0, QtWidgets.QTableWidgetItem('RTP'))
        self.table_param.setItem(0, 1, QtWidgets.QTableWidgetItem(str(parameters['rtp'])))

        self.table_param.setItem(1, 0, QtWidgets.QTableWidgetItem('volatility'))
        self.table_param.setItem(1, 1, QtWidgets.QTableWidgetItem(str(parameters['sdnew'])))

        self.table_param.setItem(2, 0, QtWidgets.QTableWidgetItem('hitrate'))
        self.table_param.setItem(2, 1, QtWidgets.QTableWidgetItem(str(parameters['hitrate'])))

        self.table_param.setItem(3, 0, QtWidgets.QTableWidgetItem('base RTP'))
        self.table_param.setItem(3, 1, QtWidgets.QTableWidgetItem(str(parameters['base_rtp'])))

        self.table_simparam.hide()

    def file_open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*.txt *.json);;Txt Files (*.txt);;Json Files (*.json)')
        if path:
            self.line_path.setText(path)
            self.path_reels = path


class Wild(QtWidgets.QWidget):
    def __init__(self):
        super(Wild, self).__init__()

        self.fon = QtWidgets.QGridLayout()

        self.label_multiplier = QtWidgets.QLabel('multiplier')
        self.line_multiplier = QtWidgets.QLineEdit()

        self.label_substitute = QtWidgets.QLabel('substitute')
        self.line_substitute = QtWidgets.QLineEdit()

        self.label_expand = QtWidgets.QLabel('expand')
        self.checkbox_expand = QtWidgets.QCheckBox()

        self.init_ui()

    def init_ui(self):
        self.fon.setColumnStretch(2, 40)

        self.fon.addWidget(self.label_multiplier, 0, 0)
        self.fon.addWidget(self.line_multiplier, 0, 1)
        self.line_multiplier.setFixedWidth(40)
        self.line_multiplier.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon.addWidget(self.label_substitute, 1, 0)
        self.fon.addWidget(self.line_substitute, 1, 1)
        self.line_substitute.setFixedWidth(40)
        self.line_substitute.textChanged.connect(self.adjust)

        self.fon.addWidget(self.label_expand, 2, 0)
        self.fon.addWidget(self.checkbox_expand, 2, 1)
        self.setLayout(self.fon)

    def adjust(self):
        text = self.line_substitute.text()
        fm = self.line_substitute.fontMetrics()
        w = fm.boundingRect(text).width()
        self.line_substitute.setFixedWidth(max(w + 12, 40))

    float_validate = float_validate

    def collect_info(self):
        d = {}
        if isint(str(self.line_multiplier.text())) >= 0:
            d.update({'multiplier': int(str(self.line_multiplier.text()))})
        if self.checkbox_expand.checkState() == QtCore.Qt.Checked:
            d.update({'expand': True})
        words = str(self.line_substitute.text()).split('; ')
        if words is not None and words != ['']:
            d.update({'substitute': words})
        return d

    def set_info(self, interim_symbol_type):
        if 'multiplier' in interim_symbol_type['wild']:
            self.line_multiplier.setText(str(interim_symbol_type['wild']['multiplier']))

        if 'expand' in interim_symbol_type['wild'] and interim_symbol_type['wild']['expand'] is True:
            self.checkbox_expand.setChecked(True)

        if 'substitute' in interim_symbol_type['wild']:
            self.line_substitute.setText('; '.join(interim_symbol_type['wild']['substitute']))


class Gametype(QtWidgets.QWidget):
    def __init__(self, type, width, mode):
        super(Gametype, self).__init__()

        self.mode = mode

        self.width = width

        self.fon_back = QtWidgets.QGridLayout()
        self.fon = QtWidgets.QGridLayout()

        self.box_scatter = QtWidgets.QGroupBox('scatter')
        self.box_scatter.setCheckable(True)
        self.box_scatter.setChecked(False)
        self.fon_scatter = QtWidgets.QHBoxLayout()

        self.box_wild = QtWidgets.QGroupBox('wild')
        self.box_wild.setCheckable(True)
        self.box_wild.setChecked(False)
        self.fon_wild = QtWidgets.QGridLayout()

        self.fon.setRowStretch(7, 400)

        self.fon_cancel = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(type)
        self.label_direction = QtWidgets.QLabel('direction   ')
        self.line_direction = QtWidgets.QComboBox()
        self.line_direction.setFixedWidth(100)
        self.line_direction.addItems(['left', 'right', 'both', 'any'])

        self.label_position = QtWidgets.QLabel('position')
        self.buttons_position = SwitchButtons(self.width, 40)

        self.label_freespins = QtWidgets.QLabel('freespins')
        self.line_freespins = None

        self.wild = None

        self.frame_frequency = QtWidgets.QFrame()
        self.label_frequency = QtWidgets.QLabel('frequency')
        self.line_frequency = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)

        self.frame = MyFrame()

        self.init_ui(self.mode)

    def init_ui(self, mode):

        self.fon.addWidget(self.label_direction, 1, 0)
        self.fon.addWidget(Aesthetic(self.line_direction), 1, 1)

        self.fon.addWidget(self.label_position, 2, 0)
        self.fon.addWidget(self.buttons_position, 2, 1)

        self.fon.addWidget(self.box_scatter, 3, 0, 1, 2)
        self.box_scatter.toggled.connect(self.scatter_check)
        self.box_scatter.setLayout(self.fon_scatter)

        self.fon.addWidget(self.box_wild, 4, 0, 1, 2)
        self.box_wild.toggled.connect(self.wild_check)
        self.box_wild.setLayout(self.fon_wild)

        self.frame_frequency.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame_frequency.setFrameShadow(QtWidgets.QFrame.Plain)
        self.fon.addWidget(self.frame_frequency, 5, 0, 1, 2)
        self.fon.addWidget(self.label_frequency, 6, 0)
        self.fon.addWidget(self.line_frequency, 6, 1)

        if mode is True:
            self.frame_frequency.hide()
            self.label_frequency.hide()
            self.line_frequency.hide()

        self.frame.setLayout(self.fon)

        self.fon_back.addWidget(self.frame)

        self.fon_cancel.addStretch(400)
        self.fon.addLayout(self.fon_cancel, 8, 1)

        self.box_wild.toggled.connect(self.change_colour)
        self.box_scatter.toggled.connect(self.change_colour)

        self.setLayout(self.fon_back)

    def scatter_check(self, checked):
        if checked is True:
            self.fon_scatter.addWidget(self.label_freespins)
            self.line_freespins = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
            self.fon_scatter.addWidget(self.line_freespins)

            self.line_direction.setCurrentIndex(3)
        else:
            self.fon_scatter.removeWidget(self.label_freespins)
            sip.delete(self.label_freespins)
            self.label_freespins = QtWidgets.QLabel('freespins')

            self.fon_scatter.removeWidget(self.line_freespins)
            sip.delete(self.line_freespins)
            self.line_freespins = None

            self.line_direction.setCurrentIndex(0)

    def wild_check(self, checked):
        if checked is True:
            self.wild = Wild()
            self.fon_wild.addWidget(self.wild, 0, 0)
        else:
            self.fon_wild.removeWidget(self.wild)
            sip.delete(self.wild)
            self.wild = None

    def change_colour(self):
        global default_color, wild_color, scatter_color, wildnscatter_color
        self.anim = QtCore.QPropertyAnimation(self.frame, b'color')
        self.anim.setDuration(160)
        self.anim.setStartValue(QtGui.QColor(self.frame.palette().color(QtGui.QPalette.Background).name()))
        if self.box_wild.isChecked() is True and self.box_scatter.isChecked() is True:
            color = wildnscatter_color
        elif self.box_wild.isChecked() is True:
            color = wild_color
        elif self.box_scatter.isChecked() is True:
            color = scatter_color
        else:
            color = default_color
        self.anim.setEndValue(color)
        self.anim.start()

    def switch_mode(self):
        if self.mode is True:
            self.mode = False
            self.frame_frequency.show()
            self.label_frequency.show()
            self.line_frequency.show()

        else:
            self.mode = True
            self.frame_frequency.hide()
            self.label_frequency.hide()
            self.line_frequency.hide()

    def collect_info(self):
        d = {}
        d.update({'direction': str(self.line_direction.currentText())})
        d.update({'position': self.buttons_position.collect_info()})
        if self.box_scatter.isChecked() is True:
            d.update({'scatter': self.line_freespins.collect_info()})
        if self.box_wild.isChecked() is True:
            d.update({'wild': self.wild.collect_info()})
        if self.mode is False:
            d.update({'frequency': self.line_frequency.arrange_info()})
        return d

    def set_info(self, interim_symbol_type):
        if 'direction' in interim_symbol_type:
            index = self.line_direction.findText(interim_symbol_type['direction'], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.line_direction.setCurrentIndex(index)

        if 'position' in interim_symbol_type:
            self.buttons_position.set_info(interim_symbol_type)

        if 'scatter' in interim_symbol_type:
            self.box_scatter.setChecked(True)
            self.line_freespins.set_info(interim_symbol_type['scatter'])

        if 'wild' in interim_symbol_type:
            self.box_wild.setChecked(True)
            self.wild.set_info(interim_symbol_type)

        if 'frequency' in interim_symbol_type:
            self.line_frequency.fill_info(interim_symbol_type['frequency'])


class Symbol(QtWidgets.QWidget):
    def __init__(self, count, width, mode):
        super(Symbol, self).__init__()

        self.mode = mode

        self.frame_symbol = QtWidgets.QFrame()
        self.fon_back = QtWidgets.QVBoxLayout()
        self.fon_symbol = QtWidgets.QVBoxLayout()
        self.fon_type = QtWidgets.QGridLayout()
        self.border = QtWidgets.QLabel(' ')
        self.label_base = QtWidgets.QLabel('base game')
        self.label_free = QtWidgets.QLabel('free game')

        self.fon_name = QtWidgets.QHBoxLayout()
        self.label_name = QtWidgets.QLabel('name     ')
        self.line_name = QtWidgets.QLineEdit('symbol_' + str(count + 1))

        self.fon_payment = QtWidgets.QHBoxLayout()
        self.label_payment = QtWidgets.QLabel('payment')
        self.line_payment = None

        self.width = width
        self.base = Gametype('base game', self.width, self.mode)
        self.free = None

        self.fon_button = QtWidgets.QVBoxLayout()
        self.frame_button = QtWidgets.QFrame()
        self.button_free = QtWidgets.QPushButton()
        self.button_free.setIcon(QtGui.QIcon('icons/edit.png'))
        self.button_state = True

        self.init_ui()

    def init_ui(self):
        self.fon_name.addWidget(self.label_name)
        self.line_name.setFixedWidth(225)
        self.fon_name.addWidget(Aesthetic(self.line_name))
        self.line_name.textChanged.connect(self.string_validate)

        self.fon_payment.addWidget(self.label_payment)
        self.line_payment = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
        self.fon_payment.addWidget(self.line_payment)

        self.fon_symbol.addLayout(self.fon_name)
        self.fon_symbol.addLayout(self.fon_payment)
        self.fon_symbol.addLayout(self.fon_type)

        self.fon_type.addWidget(self.base, 0, 0, 1, 1)

        self.fon_type.addWidget(self.frame_button, 0, 2)
        self.frame_button.setLayout(self.fon_button)
        self.frame_button.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_button.setContentsMargins(0, 0, 0, 0)
        self.fon_button.addWidget(self.button_free)
        self.button_free.clicked.connect(self.button_free_clicked)
        self.button_free.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.button_free.setToolTip('Edit free game properties')

        self.fon_type.setColumnStretch(0, 40)

        self.fon_type.setHorizontalSpacing(0)

        self.fon_symbol.addWidget(self.border)

        self.frame_symbol.setLineWidth(2)
        self.frame_symbol.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_symbol.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_symbol.setAutoFillBackground(True)
        p = self.frame_symbol.palette()
        p.setColor(self.frame_symbol.backgroundRole(), QtGui.QColor(220, 220, 220))
        self.frame_symbol.setPalette(p)

        self.frame_symbol.setLayout(self.fon_symbol)
        self.fon_back.addWidget(self.frame_symbol)
        self.setLayout(self.fon_back)

    def button_free_clicked(self):
        if self.button_state:
            self.fon_type.setColumnStretch(1, 40)
            self.free = Gametype('free game', self.width, self.mode)
            self.base.fon.addWidget(self.base.label, 0, 0, 1, 2)
            self.base.label.setAlignment(QtCore.Qt.AlignCenter)
            self.free.fon.addWidget(self.free.label, 0, 0, 1, 2)
            self.free.label.setAlignment(QtCore.Qt.AlignCenter)
            self.fon_type.addWidget(self.free, 0, 1, 1, 1)
            self.button_free.setIcon(QtGui.QIcon('icons/noedit.png'))
            self.button_free.setToolTip('Cancel editing')
            self.free.fon_cancel.addWidget(self.button_free)
            self.button_state = False

        else:
            self.fon_type.setColumnStretch(1, 1)
            self.fon_button.addWidget(self.button_free)

            self.base.fon.removeWidget(self.base.label)
            sip.delete(self.base.label)
            self.base.label = QtWidgets.QLabel('base game')

            self.free.fon.removeWidget(self.free.label)
            sip.delete(self.free.label)
            self.free.label = QtWidgets.QLabel('free game')

            self.fon_type.removeWidget(self.free)
            sip.delete(self.free)
            self.free = None
            self.button_free.setIcon(QtGui.QIcon('icons/edit.png'))
            self.button_free.setToolTip('Edit free game properties')
            self.button_state = True

    string_validate = string_validate

    def collect_info(self):
        d = {}
        if str(self.line_name.text()) == '':
            raise Exception('symbol name should not be empty')
        if ';' in str(self.line_name.text()):
            raise Exception('symbol name should not contain ";" in it')
        else:
            d.update({'name': str(self.line_name.text())})
        d.update({'payment': self.line_payment.collect_info()})
        d.update({'base': self.base.collect_info()})
        if self.free is not None:
            d.update({'free': self.free.collect_info()})
        return d

    def set_info(self, interim_symbol):
        self.line_name.setText(str(interim_symbol['name']))
        self.line_payment.set_info(interim_symbol['payment'])
        if 'base' in interim_symbol:
            self.base.set_info(interim_symbol['base'])
        if 'free' in interim_symbol:
            self.button_free_clicked()
            self.free.set_info(interim_symbol['free'])


class Window(QtWidgets.QWidget):
    def __init__(self, path=None):
        super(Window, self).__init__()

        # mode
        self.mode = True

        self.path = path

        self.game = None

        self.fon_scroll = QtWidgets.QGridLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.fon = QtWidgets.QGridLayout()

        self.fon_mode = QtWidgets.QHBoxLayout()
        self.label_mode1 = QtWidgets.QLabel('REEL GENERATOR MODE')
        self.label_mode2 = QtWidgets.QLabel('COUNTING PARAMETERS MODE')

        self.box_rules = QtWidgets.QGroupBox('Rules')
        self.fon_rules = QtWidgets.QGridLayout()

        self.box_param = QtWidgets.QGroupBox('Parameters')
        self.fon_param = QtWidgets.QGridLayout()

        self.label_window = QtWidgets.QLabel('window')
        self.line_width = QtWidgets.QLineEdit('5')
        self.line_height = QtWidgets.QLineEdit('3')
        self.width = 5
        self.height = 3

        self.fon_window = QtWidgets.QHBoxLayout()

        self.label_symbol = QtWidgets.QLabel('symbols')
        self.frame_symbols = QtWidgets.QFrame()
        self.fon_symbols = QtWidgets.QVBoxLayout()
        self.grid_symbols = QtWidgets.QGridLayout()
        self.count_symbols = 0

        self.add_symbol = QtWidgets.QPushButton('Add symbol')

        self.symbols = []
        self.deleteButtons = []

        self.label_lines = QtWidgets.QLabel('lines')
        self.frame_lines = QtWidgets.QFrame()
        self.fon_lines = QtWidgets.QVBoxLayout()
        self.grid_lines = QtWidgets.QGridLayout()
        self.count_lines = 0

        self.add_line = QtWidgets.QPushButton('Add line')

        self.lines = []
        self.deleteLines = []

        self.label_freemultiplier = QtWidgets.QLabel('free multiplier')
        self.line_freemultiplier = QtWidgets.QLineEdit()

        self.label_distance = QtWidgets.QLabel('distance')
        self.line_distance = QtWidgets.QLineEdit()

        self.label_rtp = QtWidgets.QLabel('RTP')
        self.line_rtp = QtWidgets.QLineEdit()
        self.line_rtp_error = QtWidgets.QLineEdit()

        self.label_volatility = QtWidgets.QLabel('volatility        ')
        self.line_volatility = QtWidgets.QLineEdit()
        self.line_volatility_error = QtWidgets.QLineEdit()

        self.label_hitrate = QtWidgets.QLabel('hitrate')
        self.line_hitrate = QtWidgets.QLineEdit()
        self.line_hitrate_error = QtWidgets.QLineEdit()

        self.label_baseRTP = QtWidgets.QLabel('base RTP')
        self.line_baseRTP = QtWidgets.QLineEdit()
        self.line_baseRTP_error = QtWidgets.QLineEdit()

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.widget_output = Output(path)
        self.fon_output = QtWidgets.QVBoxLayout()

        self.fon_log = QtWidgets.QHBoxLayout()
        self.label_log = QtWidgets.QLabel('Log: ')
        self.line_log = QtWidgets.QLineEdit()
        self.progressbar = QtWidgets.QProgressBar()

        self.init_ui()

    def init_ui(self):
        self.fon.setRowStretch(0, 4)

        self.fon_rules.setRowStretch(2, 40)
        self.fon_rules.setRowStretch(4, 40)

        self.fon_rules.setColumnStretch(4, 4)
        self.fon_rules.setColumnStretch(5, 4)

        self.fon_param.setColumnStretch(3, 4)

        self.fon_rules.addWidget(self.label_window, 0, 0)

        self.fon_rules.addWidget(self.line_width, 0, 1)
        self.line_width.setFixedWidth(80)
        self.fon_rules.addWidget(self.line_height, 0, 2)
        self.line_height.setFixedWidth(80)

        self.line_width.textChanged.connect(self.width_changed)
        self.line_width.textChanged.connect(lambda: self.int_validate(1, sys.maxsize))
        self.line_height.textChanged.connect(self.height_changed)
        self.line_height.textChanged.connect(lambda: self.int_validate(1, sys.maxsize))

        # symbols
        self.grid_symbols.setHorizontalSpacing(0)

        self.fon_rules.addWidget(self.label_symbol, 1, 0)
        self.fon_rules.addWidget(self.frame_symbols, 1, 1, 2, 4)
        self.frame_symbols.setLayout(self.fon_symbols)
        self.frame_symbols.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_symbols.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_lines.setVerticalSpacing(0)

        self.fon_symbols.addLayout(self.grid_symbols)
        self.fon_symbols.setStretchFactor(self.grid_symbols, 40)
        self.fon_symbols.addWidget(self.add_symbol)

        self.add_symbol.clicked.connect(lambda: self.click_add_symbol())

        # lines
        self.grid_lines.setHorizontalSpacing(0)

        self.fon_rules.addWidget(self.label_lines, 3, 0)
        self.fon_rules.addWidget(self.frame_lines, 3, 1, 2, 3)
        self.frame_lines.setLayout(self.fon_lines)
        self.frame_lines.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lines.setFrameShadow(QtWidgets.QFrame.Plain)

        self.fon_lines.addLayout(self.grid_lines)
        self.fon_lines.setStretchFactor(self.grid_lines, 40)
        self.fon_lines.addWidget(self.add_line)

        self.add_line.clicked.connect(self.click_add_line)

        self.fon_rules.addWidget(self.label_freemultiplier, 5, 0)
        self.fon_rules.addWidget(self.line_freemultiplier, 5, 1, 1, 2)
        self.line_freemultiplier.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon_rules.addWidget(self.label_distance, 6, 0)
        self.fon_rules.addWidget(self.line_distance, 6, 1, 1, 2)
        self.line_distance.textChanged.connect(lambda: self.int_validate(0, len(self.symbols)))

        self.fon_param.addWidget(self.label_rtp, 7, 0)
        self.fon_param.addWidget(self.line_rtp, 7, 1)
        self.line_rtp.setFixedWidth(80)
        self.fon_param.addWidget(self.line_rtp_error, 7, 2)
        self.line_rtp_error.setFixedWidth(80)
        self.line_rtp.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_rtp_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon_param.addWidget(self.label_volatility, 8, 0)
        self.fon_param.addWidget(self.line_volatility, 8, 1)
        self.line_volatility.setFixedWidth(80)
        self.fon_param.addWidget(self.line_volatility_error, 8, 2)
        self.line_volatility_error.setFixedWidth(80)
        self.line_volatility.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_volatility_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon_param.addWidget(self.label_hitrate, 9, 0)
        self.fon_param.addWidget(self.line_hitrate, 9, 1)
        self.line_hitrate.setFixedWidth(80)
        self.fon_param.addWidget(self.line_hitrate_error, 9, 2)
        self.line_hitrate_error.setFixedWidth(80)
        self.line_hitrate.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_hitrate_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon_param.addWidget(self.label_baseRTP, 10, 0)
        self.fon_param.addWidget(self.line_baseRTP, 10, 1)
        self.line_baseRTP.setFixedWidth(80)
        self.fon_param.addWidget(self.line_baseRTP_error, 10, 2)
        self.line_baseRTP_error.setFixedWidth(80)
        self.line_baseRTP.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_baseRTP_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.box_rules.setLayout(self.fon_rules)
        self.box_param.setLayout(self.fon_param)

        self.fon.addWidget(self.box_rules, 0, 0)
        self.fon.addWidget(self.box_param, 1, 0)

        self.label_mode1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode1.setFixedHeight(20)
        self.label_mode1.setFont(QtGui.QFont("Courier New", 10, QtGui.QFont.Bold))
        self.label_mode2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode2.setFixedHeight(20)
        self.label_mode2.setFont(QtGui.QFont("Courier New", 10, QtGui.QFont.Bold))
        self.fon_mode.setSpacing(0)
        self.fon_mode.addWidget(self.label_mode1)

        self.line_log.setReadOnly(True)
        self.line_log.setStyleSheet('QLineEdit {border: none}')

        self.fon_log.addWidget(self.label_log)
        self.fon_log.addWidget(self.line_log)
        self.fon_log.addWidget(self.progressbar)

        self.fon_scroll.setHorizontalSpacing(0)

        self.widget.setLayout(self.fon)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.fon_scroll.addLayout(self.fon_mode, 0, 0)
        self.splitter.addWidget(self.widget_output)
        self.splitter.addWidget(self.scroll)
        self.splitter.setStretchFactor(self.splitter.indexOf(self.scroll), 4)
        self.fon_scroll.addWidget(self.splitter, 1, 0)
        self.fon_scroll.addLayout(self.fon_log, 2, 0)
        self.setLayout(self.fon_scroll)

    def click_add_symbol(self, opened=None):
        global default_color
        symbol = Symbol(self.count_symbols, self.width, self.mode)
        self.symbols.append(symbol)

        button_delete = QtWidgets.QPushButton()
        button_delete.setIcon(QtGui.QIcon('icons/close.png'))
        button_delete.setToolTip('Delete symbol')
        button_delete.setFixedSize(28, 28)
        self.deleteButtons.append(button_delete)
        self.deleteButtons[-1].clicked.connect(self.click_delete_symbol)
        self.symbols[-1].fon_name.addWidget(self.deleteButtons[-1])
        self.grid_symbols.addWidget(self.symbols[-1], self.count_symbols, 0)

        self.count_symbols += 1

        self.line_distance.textChanged.emit(self.line_distance.text())

        if opened is None:
            QtWidgets.QApplication.processEvents()
            QtCore.QTimer.singleShot(0, self.sup_add_symbol)

    def sup_add_symbol(self):
        x = self.symbols[-1].x()
        y = self.symbols[-1].y()
        width = self.symbols[-1].geometry().width()
        height = self.symbols[-1].geometry().height()

        self.add_symbol_anim = QtCore.QPropertyAnimation(self.symbols[-1], b"geometry")
        self.add_symbol_button_anim = QtCore.QPropertyAnimation(self.add_symbol, b"geometry")
        self.add_symbol_anim.setDuration(320)
        self.add_symbol_button_anim.setDuration(320)
        self.add_symbol_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.add_symbol_button_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.add_symbol_anim.setStartValue(QtCore.QRect(x, y, width, 0))
        self.add_symbol_button_anim.setStartValue(QtCore.QRect(self.add_symbol.x(), self.add_symbol.y() - height, self.add_symbol.width(), self.add_symbol.height()))
        self.add_symbol_anim.setEndValue(QtCore.QRect(x, y, width, height))
        self.add_symbol_button_anim.setEndValue(QtCore.QRect(self.add_symbol.x(), y + height, self.add_symbol.width(), self.add_symbol.height()))
        self.add_symbol_anim.start()
        self.add_symbol_button_anim.start()

        dist = 200 - self.geometry().height() + (y + height) + self.widget.pos().y()
        if dist > 0:
            scroll = self.scroll.verticalScrollBar()
            scroll.setSingleStep(10)
            for i in range(int(dist/10)):
                QtCore.QTimer.singleShot(10 * i, lambda: scroll.triggerAction(QtWidgets.QAbstractSlider.SliderSingleStepAdd))

    def click_delete_symbol(self):
        sender = self.sender()
        num = self.deleteButtons.index(sender)

        height = self.symbols[num].geometry().height()
        self.del_symbol_anim = QtCore.QPropertyAnimation(self.symbols[num], b'minimumHeight')
        self.del_symbol_anim.setDuration(160)
        self.del_symbol_anim.setStartValue(height)
        self.del_symbol_anim.setEndValue(0)
        self.del_symbol_anim.start()

        self.del_symbol_anim.finished.connect(lambda: self.sub_del_symbol(num))

        self.line_distance.textChanged.emit(self.line_distance.text())

    def sub_del_symbol(self, num):
        self.grid_symbols.removeWidget(self.symbols[num])
        sip.delete(self.symbols[num])
        del self.symbols[num]
        del self.deleteButtons[num]

    def click_add_line(self):
        line = LineEdits(self.width, 28, 1, self.height, 24, 0)
        self.lines.append(line)

        button_delete = QtWidgets.QPushButton()
        button_delete.setIcon(QtGui.QIcon('icons/close.png'))
        button_delete.setFixedSize(26, 26)
        self.deleteLines.append(button_delete)
        self.deleteLines[-1].clicked.connect(self.click_delete_line)

        self.grid_lines.addWidget(self.lines[-1], self.count_lines, 0)

        self.grid_lines.addWidget(self.deleteLines[-1], self.count_lines, 1)

        self.count_lines += 1

    def click_delete_line(self):
        sender = self.sender()
        num = self.deleteLines.index(sender)

        self.grid_lines.removeWidget(self.lines[num])
        sip.delete(self.lines[num])
        del self.lines[num]

        self.grid_lines.removeWidget(self.deleteLines[num])
        sip.delete(self.deleteLines[num])
        del self.deleteLines[num]

    def width_changed(self):
        if isint(str(self.line_width.text())) > 0:
            self.width = int(str(self.line_width.text()))
            for i in range(len(self.symbols)):
                self.symbols[i].width = self.width

                self.symbols[i].fon_payment.removeWidget(self.symbols[i].line_payment)
                sip.delete(self.symbols[i].line_payment)

                self.symbols[i].line_payment = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
                self.symbols[i].fon_payment.addWidget(self.symbols[i].line_payment)

                self.symbols[i].base.width = self.width

                self.symbols[i].base.fon.removeWidget(self.symbols[i].base.buttons_position)
                sip.delete(self.symbols[i].base.buttons_position)
                self.symbols[i].base.buttons_position = SwitchButtons(self.width, 40)
                self.symbols[i].base.fon.addWidget(self.symbols[i].base.buttons_position, 2, 1)

                if self.symbols[i].base.box_scatter.isChecked() is True:
                    self.symbols[i].base.fon_scatter.removeWidget(self.symbols[i].base.line_freespins)
                    sip.delete(self.symbols[i].base.line_freespins)
                    self.symbols[i].base.line_freespins = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
                    self.symbols[i].base.fon_scatter.addWidget(self.symbols[i].base.line_freespins)

                if self.symbols[i].free is not None:
                    self.symbols[i].free.width = self.width

                    self.symbols[i].free.fon.removeWidget(self.symbols[i].free.buttons_position)
                    sip.delete(self.symbols[i].free.buttons_position)
                    self.symbols[i].free.buttons_position = SwitchButtons(self.width, 40)
                    self.symbols[i].free.fon.addWidget(self.symbols[i].free.buttons_position, 2, 1)

                    if self.symbols[i].free.box_scatter.isChecked() is True:
                        self.symbols[i].free.fon_scatter.removeWidget(self.symbols[i].free.line_freespins)
                        sip.delete(self.symbols[i].free.line_freespins)
                        self.symbols[i].free.line_freespins = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
                        self.symbols[i].free.fon_scatter.addWidget(self.symbols[i].free.line_freespins)

                if self.mode is False:
                    self.symbols[i].base.fon.removeWidget(self.symbols[i].base.line_frequency)
                    sip.delete(self.symbols[i].base.line_frequency)
                    self.symbols[i].base.line_frequency = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
                    self.symbols[i].base.fon.addWidget(self.symbols[i].base.line_frequency, 6, 1)

                    if self.symbols[i].free is not None:
                        self.symbols[i].free.fon.removeWidget(self.symbols[i].free.line_frequency)
                        sip.delete(self.symbols[i].free.line_frequency)
                        self.symbols[i].free.line_frequency = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
                        self.symbols[i].free.fon.addWidget(self.symbols[i].free.line_frequency, 6, 1)

            for i in range(len(self.lines)):
                pos = self.grid_lines.getItemPosition(self.grid_lines.indexOf(self.lines[i]))
                self.grid_lines.removeWidget(self.lines[i])
                sip.delete(self.lines[i])

                self.lines[i] = LineEdits(self.width, 28, 1, self.height, 24, 0)
                self.grid_lines.addWidget(self.lines[i], pos[0], pos[1])

    def height_changed(self):
        if isint(str(self.line_height.text())) > 0:
            self.height = int(str(self.line_height.text()))
            for line in self.lines:
                for atom in line.lines:
                    try:
                        atom.disconnect()
                    except:
                        pass

                    atom.textChanged.connect(lambda: self.int_validate(1, self.height))
                    atom.textChanged.emit(atom.text())

    int_validate = int_validate
    float_validate = float_validate

    def switch_mode(self):
        if self.mode is True:
            size = self.label_mode1.width()
            self.fon_mode.addWidget(self.label_mode2)
            self.label1_anim = QtCore.QPropertyAnimation(self.label_mode1, b'maximumWidth')
            self.label2_anim = QtCore.QPropertyAnimation(self.label_mode2, b'maximumWidth')
            self.label1_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.label2_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.label1_anim.setDuration(320)
            self.label2_anim.setDuration(320)
            self.label1_anim.setStartValue(size)
            self.label2_anim.setStartValue(0)
            self.label1_anim.setEndValue(0)
            self.label2_anim.setEndValue(size)
            self.label1_anim.start()
            self.label2_anim.start()
            self.mode = False

        else:
            size = self.label_mode2.width()
            self.label1_anim = QtCore.QPropertyAnimation(self.label_mode1, b'maximumWidth')
            self.label2_anim = QtCore.QPropertyAnimation(self.label_mode2, b'maximumWidth')
            self.label1_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.label2_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.label1_anim.setDuration(320)
            self.label2_anim.setDuration(320)
            self.label1_anim.setStartValue(0)
            self.label2_anim.setStartValue(size)
            self.label1_anim.setEndValue(size)
            self.label2_anim.setEndValue(0)
            self.label1_anim.start()
            self.label2_anim.start()
            self.mode = True

            self.label1_anim.finished.connect(self.finished_anim)

        self.box_param.setEnabled(self.mode)
        self.widget_output.switch_mode(self.mode)
        for symbol in self.symbols:
            symbol.mode = not symbol.mode
            symbol.base.switch_mode()
            if symbol.free is not None:
                symbol.free.switch_mode()

    def finished_anim(self):
        self.label_mode1.setMaximumWidth(4000)
        self.label_mode2.setMaximumWidth(4000)

    def answer(self):
        parameters = self.run()
        self.widget_output.setItem(0, 0, QtWidgets.QTableWidgetItem('RTP'))
        self.widget_output.setItem(0, 1, QtWidgets.QTableWidgetItem(str(parameters['rtp'])))

        self.widget_output.setItem(1, 0, QtWidgets.QTableWidgetItem('volatility'))
        self.widget_output.setItem(1, 1, QtWidgets.QTableWidgetItem(str(parameters['sdnew'])))

        self.widget_output.setItem(2, 0, QtWidgets.QTableWidgetItem('hitrate'))
        self.widget_output.setItem(2, 1, QtWidgets.QTableWidgetItem(str(parameters['hitrate'])))

        self.widget_output.setItem(3, 0, QtWidgets.QTableWidgetItem('base RTP'))
        self.widget_output.setItem(3, 1, QtWidgets.QTableWidgetItem(str(parameters['base_rtp'])))

    def collect_info(self):
        d = {}
        d.update({'window': [self.width, self.height]})
        symbols = []
        for i in range(len(self.symbols)):
            symbols.append(self.symbols[i].collect_info())
        d.update({'symbols': symbols})

        lines = []
        for i in range(len(self.lines)):
            if self.lines[i].arrange_info() is not None:
                lines.append(self.lines[i].arrange_info())
        d.update({'lines': lines})

        if isint(str(self.line_freemultiplier.text())) >= 0:
            d.update({'free_multiplier': int(str(self.line_freemultiplier.text()))})

        if isint(str(self.line_distance.text())) >= 0:
            d.update({'distance': int(str(self.line_distance.text()))})

        if self.mode is True:
            if isfloat(str(self.line_rtp.text())) and isfloat(str(self.line_rtp_error.text())):
                d.update({'RTP': [float(str(self.line_rtp.text())), float(str(self.line_rtp_error.text()))]})

            if isfloat(str(self.line_volatility.text())) and isfloat(str(self.line_volatility_error.text())):
                d.update({'volatility': [float(str(self.line_volatility.text())), float(str(self.line_volatility_error.text()))]})

            if isfloat(str(self.line_hitrate.text())) and isfloat(str(self.line_hitrate_error.text())):
                d.update({'hitrate': [float(str(self.line_hitrate.text())), float(str(self.line_hitrate_error.text()))]})

            if isfloat(str(self.line_baseRTP.text())) and isfloat(str(self.line_baseRTP_error.text())):
                d.update({'baseRTP': [float(str(self.line_baseRTP.text())), float(str(self.line_baseRTP_error.text()))]})
        return d

    def set_info(self, interim):
        if 'window' in interim:
            self.line_width.setText(str(interim['window'][0]))
            self.width = interim['window'][0]
            self.line_height.setText(str(interim['window'][1]))
            self.height = interim['window'][1]

        for i in range(len(interim['symbols'])):
            self.click_add_symbol(True)
            self.symbols[i].set_info(interim['symbols'][i])

        for i in range(len(interim['lines'])):
            self.click_add_line()
            self.lines[i].fill_info(interim['lines'][i])

        if 'free_multiplier' in interim:
            self.line_freemultiplier.setText(str(interim['free_multiplier']))

        if 'distance' in interim:
            self.line_distance.setText(str(interim['distance']))

        if 'RTP' in interim:
            self.line_rtp.setText(str(interim['RTP'][0]))
            self.line_rtp_error.setText(str(interim['RTP'][1]))

        if 'volatility' in interim:
            self.line_volatility.setText(str(interim['volatility'][0]))
            self.line_volatility_error.setText(str(interim['volatility'][1]))

        if 'hitrate' in interim:
            self.line_hitrate.setText(str(interim['hitrate'][0]))
            self.line_hitrate_error.setText(str(interim['hitrate'][1]))

        if 'baseRTP' in interim:
            self.line_baseRTP.setText(str(interim['baseRTP'][0]))
            self.line_baseRTP_error.setText(str(interim['baseRTP'][1]))

    def run(self):
        info = self.collect_info()
        self.game = Q.Game(info)

        if self.mode is True:
            pass

        if self.mode is False:
            base_frequency = []
            free_frequency = []
            for symbol in self.symbols:
                if symbol.base.line_frequency.arrange_info() is None:
                    i = self.symbols.index(symbol) + 1
                    raise Exception('Frequency of symbol ' + str(i) + ' was not set correctly')
                else:
                    base_frequency.append(symbol.base.line_frequency.arrange_info())

                if symbol.free is None:
                    free_frequency.append(symbol.base.line_frequency.arrange_info())
                else:
                    if symbol.free.line_frequency.arrange_info() is None:
                        i = self.symbols.index(symbol) + 1
                        raise Exception('Frequency of symbol ' + str(i) + ' was not set correctly')
                    else:
                        free_frequency.append(symbol.free.line_frequency.arrange_info())

            self.game.base.fill_frequency(np.array(base_frequency).T.tolist())
            self.game.free.fill_frequency(np.array(free_frequency).T.tolist())

            parameters = self.game.standalone_count_parameters()

            self.widget_output.set_param(parameters)

    def simulation(self):
        simparam = simulate.make_spins_ui(self, self.game)
        self.widget_output.set_simparam(simparam)



class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.setWindowTitle('Slot Machine Creator')
        self.setWindowIcon(QtGui.QIcon('icons/yarlyk.png'))
        self.setGeometry(200, 200, 1000, 600)

        self.tab = QtWidgets.QTabWidget()

        self.tool_file = self.addToolBar('file')
        self.tool_run = self.addToolBar('run')
        self.bar = self.menuBar()

        self.action_new = QtWidgets.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        self.action_new.setShortcut('Ctrl+N')
        self.action_new.triggered.connect(self.trigger_new)

        self.action_open = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        self.action_open.setShortcut('Ctrl+O')
        self.action_open.triggered.connect(self.trigger_open)

        self.action_save = QtWidgets.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        self.action_save.setShortcut('Ctrl+S')
        self.action_save.triggered.connect(self.trigger_save)
        self.action_save.setEnabled(False)

        self.action_saveas = QtWidgets.QAction(QtGui.QIcon('icons/saveas.png'), 'Save as', self)
        self.action_saveas.setShortcut('Ctrl+Alt+S')
        self.action_saveas.triggered.connect(self.trigger_saveas)
        self.action_saveas.setEnabled(False)

        self.action_settings = QtWidgets.QAction(QtGui.QIcon('icons/settings.png'), 'Settings', self)

        self.action_quit = QtWidgets.QAction(QtGui.QIcon('icons/quit.png'), 'Quit', self)
        self.action_quit.setShortcut('Ctrl+Q')
        self.action_quit.triggered.connect(self.trigger_quit)

        self.action_run = QtWidgets.QAction(QtGui.QIcon('icons/run2.png'), 'Run', self)
        self.action_run.setShortcut('Ctrl+R')
        self.action_run.triggered.connect(self.trigger_run)
        self.action_run.setEnabled(False)

        self.action_simulation = QtWidgets.QAction(QtGui.QIcon('icons/simulation.png'), 'Run simulation', self)
        self.action_simulation.triggered.connect(self.trigger_simulation)
        self.action_simulation.setEnabled(False)

        self.action_switch = QtWidgets.QAction(QtGui.QIcon('icons/switch2.png'), 'Switch mode', self)
        self.action_switch.triggered.connect(self.trigger_switch)
        self.action_switch.setEnabled(False)

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.tab)

        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.currentChanged.connect(self.change_tab)
        self.tab.setMovable(True)

        file = self.bar.addMenu('File')
        run = self.bar.addMenu('Run')

        file.addAction(self.action_new)
        file.addAction(self.action_open)
        file.addAction(self.action_save)
        file.addAction(self.action_saveas)
        file.addAction(self.action_settings)
        file.addAction(self.action_quit)

        run.addAction(self.action_run)
        run.addAction(self.action_simulation)
        run.addAction(self.action_switch)

        self.tool_file.addAction(self.action_new)
        self.tool_file.addAction(self.action_open)
        self.tool_file.addAction(self.action_save)
        self.tool_file.addAction(self.action_saveas)

        self.tool_run.addAction(self.action_run)
        self.tool_run.addAction(self.action_simulation)
        self.tool_run.addAction(self.action_switch)

    def close_tab(self, current_index):
        current_widget = self.tab.widget(current_index)
        current_widget.deleteLater()
        self.tab.removeTab(current_index)

    def change_tab(self, index):
        if index == -1:
            self.action_run.setEnabled(False)
            self.action_simulation.setEnabled(False)
            self.action_switch.setEnabled(False)
            self.action_saveas.setEnabled(False)
            self.action_save.setEnabled(False)
        else:
            self.action_run.setEnabled(True)
            self.action_switch.setEnabled(True)
            self.action_saveas.setEnabled(True)

            current = self.tab.currentWidget()
            if current.path is None:
                self.action_save.setEnabled(False)
            else:
                self.action_save.setEnabled(True)

            if current.game is None:
                self.action_simulation.setEnabled(False)
            else:
                self.action_simulation.setEnabled(True)

    def trigger_run(self):
        self.action_run.setIcon(QtGui.QIcon('icons/stop.png'))
        self.tab.setDisabled(True)
        current = self.tab.currentWidget()
        current.line_log.setStyleSheet('QLineEdit {border: none}')
        if current.mode is True:
            current.line_log.setText('Generating reels...')
        else:
            current.line_log.setText('Counting parameters...')
        QtWidgets.QApplication.processEvents()
        try:
            current.run()

        except Exception as error:
            current.line_log.setStyleSheet('QLineEdit {color: red; border: none}')
            current.line_log.setText("%s" % error)

        else:
            current.line_log.setStyleSheet('QLineEdit {color: green; border: none}')
            current.line_log.setText("process finished")

        self.tab.setEnabled(True)
        self.action_run.setIcon(QtGui.QIcon('icons/run2.png'))

        self.action_simulation.setEnabled(True)

    def trigger_simulation(self):
        self.action_simulation.setIcon(QtGui.QIcon('icons/stop.png'))
        self.tab.setDisabled(True)
        current = self.tab.currentWidget()
        current.line_log.setStyleSheet('QLineEdit {border: none}')
        current.line_log.setText('Running simulation...')
        QtWidgets.QApplication.processEvents()
        try:
            current.simulation()

        except Exception as error:
            current.line_log.setStyleSheet('QLineEdit {color: red; border: none}')
            current.line_log.setText("%s" % error)

        else:
            current.line_log.setStyleSheet('QLineEdit {color: green; border: none}')
            current.line_log.setText("process finished")

        self.tab.setEnabled(True)
        self.action_simulation.setIcon(QtGui.QIcon('icons/simulation.png'))

    def trigger_switch(self):
        current = self.tab.currentWidget()
        current.switch_mode()

    def trigger_new(self):
        global count_tabs
        new_tab = Window()
        self.tab.addTab(new_tab, 'untitled' + str(count_tabs))
        self.tab.setCurrentWidget(new_tab)
        count_tabs += 1

        #button = QtWidgets.QPushButton('x')

        #tab_bar = self.tab.tabBar()
        #tab_bar.setTabButton(self.tab.currentIndex(), QtWidgets.QTabBar.RightSide, button)

    def trigger_save(self):
        current = self.tab.currentWidget()
        info = current.collect_info()
        file = open(current.path, 'w')
        json.dump(info, file)
        file.close()

    def trigger_saveas(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'All Files (*.txt *.json);;Txt Files (*.txt);;Json Files (*.json)')
        if path:
            file = open(path, 'w')
            current = self.tab.currentWidget()
            current.path = path
            current.widget_output.set_path(path)
            info = current.collect_info()
            json.dump(info, file)
            file.close()
            self.action_save.setEnabled(True)
            i = self.tab.currentIndex()
            self.tab.setTabText(i, str(path_leaf(path)))

    def trigger_open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*.txt *.json);;Txt Files (*.txt);;Json Files (*.json)')
        if path:
            file = open(path, 'r')
            j = file.read()
            info = json.loads(j)
            file.close()

            new_tab = Window(path)
            new_tab.set_info(info)

            self.tab.addTab(new_tab, str(path_leaf(path)))
            self.tab.setCurrentWidget(new_tab)

    def trigger_quit(self):
        QtWidgets.qApp.quit()


app = QtWidgets.QApplication(sys.argv)
a_window = Main()
a_window.showMaximized()
sys.exit(app.exec_())
