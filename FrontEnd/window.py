# -*- coding: utf-8 -*-
import sys
import json
import ntpath
from PyQt5 import QtWidgets, QtGui, QtCore, sip

count = 0
count_lines = 0
count_tabs = 1


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
    if str(sender.text()) == '':
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
    def __init__(self, type, width):
        super(Gametype, self).__init__()

        self.width = width

        self.fon_back = QtWidgets.QGridLayout()
        self.fon = QtWidgets.QGridLayout()

        for i in range(7):
            self.fon.setRowStretch(i, 1)

        self.fon.setRowStretch(7, 400)

        self.fon_cancel = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(type)
        self.label_direction = QtWidgets.QLabel('direction')
        self.line_direction = QtWidgets.QComboBox()
        self.line_direction.setFixedWidth(100)
        self.line_direction.addItems(['left', 'right', 'both', 'any'])

        self.label_position = QtWidgets.QLabel('position')
        self.buttons_position = SwitchButtons(self.width, 40)

        self.label_scatter = QtWidgets.QLabel('scatter')
        self.checkbox_scatter = QtWidgets.QCheckBox()

        self.label_freespins = QtWidgets.QLabel('freespins')
        self.line_freespins = None

        self.label_wild = QtWidgets.QLabel('wild')
        self.checkbox_wild = QtWidgets.QCheckBox()

        self.wild = None

        self.frame = QtWidgets.QFrame()

        self.init_ui()

    def init_ui(self):
        self.fon.addWidget(self.label_direction, 1, 0)
        self.fon.addWidget(Aesthetic(self.line_direction), 1, 1)

        self.fon.addWidget(self.label_position, 2, 0)
        self.fon.addWidget(self.buttons_position, 2, 1)

        self.fon.addWidget(self.label_scatter, 3, 0)
        self.fon.addWidget(Aesthetic(self.checkbox_scatter), 3, 1)
        self.checkbox_scatter.stateChanged.connect(self.scatter_check)

        self.fon.addWidget(self.label_wild, 5, 0)
        self.fon.addWidget(Aesthetic(self.checkbox_wild), 5, 1)
        self.checkbox_wild.stateChanged.connect(self.wild_check)

        #self.frame.setLineWidth(2)
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLayout(self.fon)

        self.fon_back.addWidget(self.frame)

        self.fon_cancel.addStretch(400)
        self.fon.addLayout(self.fon_cancel, 8, 1)

        self.checkbox_wild.stateChanged.connect(self.change_colour)
        self.checkbox_scatter.stateChanged.connect(self.change_colour)

        self.setLayout(self.fon_back)

    def scatter_check(self, state):
        if state == QtCore.Qt.Checked:
            self.fon.addWidget(self.label_freespins, 4, 0)
            self.line_freespins = LineEdits(self.width, 40, 0, sys.maxsize, None, None, True)
            self.fon.addWidget(self.line_freespins, 4, 1)
        else:
            self.fon.removeWidget(self.label_freespins)
            sip.delete(self.label_freespins)
            self.label_freespins = QtWidgets.QLabel('freespins')

            self.fon.removeWidget(self.line_freespins)
            sip.delete(self.line_freespins)
            self.line_freespins = None

    def wild_check(self, state):
        if state == QtCore.Qt.Checked:
            self.wild = Wild()
            self.fon.addWidget(self.wild, 6, 0, 1, 2)
        else:
            self.fon.removeWidget(self.wild)
            sip.delete(self.wild)
            self.wild = None

    def change_colour(self):
        if self.checkbox_wild.checkState() == QtCore.Qt.Checked and self.checkbox_scatter.checkState() == QtCore.Qt.Checked:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(221, 172, 225))
            self.frame.setPalette(p)

        elif self.checkbox_wild.checkState() == QtCore.Qt.Checked:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(255, 229, 100))
            self.frame.setPalette(p)

        elif self.checkbox_scatter.checkState() == QtCore.Qt.Checked:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(120, 237, 255))
            self.frame.setPalette(p)

        else:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(220, 220, 220))
            self.frame.setPalette(p)

    def collect_info(self):
        d = {}
        d.update({'direction': str(self.line_direction.currentText())})
        d.update({'position': self.buttons_position.collect_info()})
        if self.checkbox_scatter.checkState() == QtCore.Qt.Checked:
            d.update({'scatter': self.line_freespins.collect_info()})
        if self.checkbox_wild.checkState() == QtCore.Qt.Checked:
            d.update({'wild': self.wild.collect_info()})
        return d

    def set_info(self, interim_symbol_type):
        if 'direction' in interim_symbol_type:
            index = self.line_direction.findText(interim_symbol_type['direction'], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.line_direction.setCurrentIndex(index)

        if 'position' in interim_symbol_type:
            self.buttons_position.set_info(interim_symbol_type)

        if 'scatter' in interim_symbol_type:
            self.checkbox_scatter.setCheckState(QtCore.Qt.Checked)
            self.line_freespins.set_info(interim_symbol_type['scatter'])

        if 'wild' in interim_symbol_type:
            self.checkbox_wild.setCheckState(QtCore.Qt.Checked)
            self.wild.set_info(interim_symbol_type)


class Symbol(QtWidgets.QWidget):
    def __init__(self, count, width):
        super(Symbol, self).__init__()

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
        self.base = Gametype('base game', self.width)
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

        #self.frame_symbol.setLineWidth(2)
        self.frame_symbol.setFrameShape(QtWidgets.QFrame.WinPanel)
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
            self.free = Gametype('free game', self.width)
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
    def __init__(self):
        super(Window, self).__init__()

        self.fon_scroll = QtWidgets.QHBoxLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.widget = QtWidgets.QWidget()
        self.fon = QtWidgets.QGridLayout()

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

        self.label_volatility = QtWidgets.QLabel('volatility')
        self.line_volatility = QtWidgets.QLineEdit()
        self.line_volatility_error = QtWidgets.QLineEdit()

        self.label_hitrate = QtWidgets.QLabel('hitrate')
        self.line_hitrate = QtWidgets.QLineEdit()
        self.line_hitrate_error = QtWidgets.QLineEdit()

        self.label_baseRTP = QtWidgets.QLabel('base RTP')
        self.line_baseRTP = QtWidgets.QLineEdit()
        self.line_baseRTP_error = QtWidgets.QLineEdit()

        self.init_ui()

    def init_ui(self):
        self.fon.setRowStretch(2, 40)
        self.fon.setRowStretch(4, 40)

        self.fon.setColumnStretch(4, 4)
        self.fon.setColumnStretch(5, 4)
        # bylo 400

        self.fon.addWidget(self.label_window, 0, 0)

        self.fon.addWidget(self.line_width, 0, 1)
        self.line_width.setFixedWidth(80)
        self.fon.addWidget(self.line_height, 0, 2)
        self.line_height.setFixedWidth(80)

        self.line_width.textChanged.connect(self.width_changed)
        self.line_width.textChanged.connect(lambda: self.int_validate(1, sys.maxsize))
        self.line_height.textChanged.connect(self.height_changed)
        self.line_height.textChanged.connect(lambda: self.int_validate(1, sys.maxsize))

        # symbols
        self.grid_symbols.setHorizontalSpacing(0)

        self.fon.addWidget(self.label_symbol, 1, 0)
        self.fon.addWidget(self.frame_symbols, 1, 1, 2, 4)
        self.frame_symbols.setLayout(self.fon_symbols)
        self.frame_symbols.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_symbols.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_lines.setVerticalSpacing(0)

        self.fon_symbols.addLayout(self.grid_symbols)
        self.fon_symbols.setStretchFactor(self.grid_symbols, 40)
        self.fon_symbols.addWidget(self.add_symbol)

        self.add_symbol.clicked.connect(self.click_add_symbol)

        # lines
        self.grid_lines.setHorizontalSpacing(0)

        self.fon.addWidget(self.label_lines, 3, 0)
        self.fon.addWidget(self.frame_lines, 3, 1, 2, 3)
        self.frame_lines.setLayout(self.fon_lines)
        self.frame_lines.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lines.setFrameShadow(QtWidgets.QFrame.Plain)

        self.fon_lines.addLayout(self.grid_lines)
        self.fon_lines.setStretchFactor(self.grid_lines, 40)
        self.fon_lines.addWidget(self.add_line)

        self.add_line.clicked.connect(self.click_add_line)

        self.fon.addWidget(self.label_freemultiplier, 5, 0)
        self.fon.addWidget(self.line_freemultiplier, 5, 1, 1, 2)
        self.line_freemultiplier.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon.addWidget(self.label_distance, 6, 0)
        self.fon.addWidget(self.line_distance, 6, 1, 1, 2)
        self.line_distance.textChanged.connect(lambda: self.int_validate(0, len(self.symbols)))

        self.fon.addWidget(self.label_rtp, 7, 0)
        self.fon.addWidget(self.line_rtp, 7, 1)
        self.line_rtp.setFixedWidth(80)
        self.fon.addWidget(self.line_rtp_error, 7, 2)
        self.line_rtp_error.setFixedWidth(80)
        self.line_rtp.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_rtp_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon.addWidget(self.label_volatility, 8, 0)
        self.fon.addWidget(self.line_volatility, 8, 1)
        self.line_volatility.setFixedWidth(80)
        self.fon.addWidget(self.line_volatility_error, 8, 2)
        self.line_volatility_error.setFixedWidth(80)
        self.line_volatility.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_volatility_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon.addWidget(self.label_hitrate, 9, 0)
        self.fon.addWidget(self.line_hitrate, 9, 1)
        self.line_hitrate.setFixedWidth(80)
        self.fon.addWidget(self.line_hitrate_error, 9, 2)
        self.line_hitrate_error.setFixedWidth(80)
        self.line_hitrate.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_hitrate_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.fon.addWidget(self.label_baseRTP, 10, 0)
        self.fon.addWidget(self.line_baseRTP, 10, 1)
        self.line_baseRTP.setFixedWidth(80)
        self.fon.addWidget(self.line_baseRTP_error, 10, 2)
        self.line_baseRTP_error.setFixedWidth(80)
        self.line_baseRTP.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))
        self.line_baseRTP_error.textChanged.connect(lambda: self.float_validate(0, sys.maxsize))

        self.widget.setLayout(self.fon)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.fon_scroll.addWidget(self.scroll)
        self.setLayout(self.fon_scroll)

    def click_add_symbol(self):
        symbol = Symbol(self.count_symbols, self.width)
        self.symbols.append(symbol)

        button_delete = QtWidgets.QPushButton()
        button_delete.setIcon(QtGui.QIcon('icons/close.png'))
        button_delete.setToolTip('Delete symbol')
        button_delete.setFixedSize(28, 28)
        self.deleteButtons.append(button_delete)
        self.deleteButtons[-1].clicked.connect(self.click_delete_symbol)

        self.grid_symbols.addWidget(self.symbols[-1], self.count_symbols, 0)

        self.symbols[-1].fon_name.addWidget(self.deleteButtons[-1])

        self.count_symbols += 1

        self.line_distance.textChanged.emit(self.line_distance.text())

    def click_delete_symbol(self):
        sender = self.sender()
        num = self.deleteButtons.index(sender)

        self.grid_symbols.removeWidget(self.symbols[num])
        sip.delete(self.symbols[num])
        del self.symbols[num]

        del self.deleteButtons[num]

        self.line_distance.textChanged.emit(self.line_distance.text())

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

                if self.symbols[i].base.checkbox_scatter.checkState() == QtCore.Qt.Checked:
                    self.symbols[i].base.fon.removeWidget(self.symbols[i].base.line_freespins)
                    sip.delete(self.symbols[i].base.line_freespins)
                    self.symbols[i].base.line_freespins = LineEdits(self.width, 28, 0, sys.maxsize, None, None, True)
                    self.symbols[i].base.fon.addWidget(self.symbols[i].base.line_freespins, 4, 1)

                if self.symbols[i].free is not None:
                    self.symbols[i].free.width = self.width

                    self.symbols[i].free.fon.removeWidget(self.symbols[i].free.buttons_position)
                    sip.delete(self.symbols[i].free.buttons_position)
                    self.symbols[i].free.buttons_position = SwitchButtons(self.width, 28)
                    self.symbols[i].free.fon.addWidget(self.symbols[i].free.buttons_position, 2, 1)

                    if self.symbols[i].free.checkbox_scatter.checkState() == QtCore.Qt.Checked:
                        self.symbols[i].free.fon.removeWidget(self.symbols[i].free.line_freespins)
                        sip.delete(self.symbols[i].free.line_freespins)
                        self.symbols[i].free.line_freespins = LineEdits(self.width, 28, 0, sys.maxsize, None, None, True)
                        self.symbols[i].free.fon.addWidget(self.symbols[i].free.line_freespins, 4, 1)

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
            self.click_add_symbol()
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


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.setWindowTitle('Azino 777')
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

        self.action_submit = QtWidgets.QAction(QtGui.QIcon('icons/submit.png'), 'Submit', self)
        self.action_submit.triggered.connect(self.trigger_submit)

        self.action_run = QtWidgets.QAction(QtGui.QIcon('icons/run1.png'), 'Run', self)
        self.action_run.setEnabled(False)

        self.action_submitnrun = QtWidgets.QAction(QtGui.QIcon('icons/submitnrun1.png'), 'Submit and run', self)
        self.action_submitnrun.triggered.connect(self.trigger_submit)

        self.info = None

        self.json_path = None

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.tab)

        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.setMovable(True)

        file = self.bar.addMenu('File')
        run = self.bar.addMenu('Run')

        file.addAction(self.action_new)
        file.addAction(self.action_open)
        file.addAction(self.action_save)
        file.addAction(self.action_saveas)
        file.addAction(self.action_settings)
        file.addAction(self.action_quit)

        run.addAction(self.action_submit)
        run.addAction(self.action_run)
        run.addAction(self.action_submitnrun)

        self.tool_file.addAction(self.action_new)
        self.tool_file.addAction(self.action_open)
        self.tool_file.addAction(self.action_save)
        self.tool_file.addAction(self.action_saveas)

        self.tool_run.addAction(self.action_submit)
        self.tool_run.addAction(self.action_run)
        self.tool_run.addAction(self.action_submitnrun)

    def close_tab(self, current_index):
        current_widget = self.tab.widget(current_index)
        current_widget.deleteLater()
        self.tab.removeTab(current_index)
        if self.tab.__len__() == 0:
            self.action_submit.setEnabled(False)

    def trigger_submit(self):
        current = self.tab.currentWidget()
        self.info = current.collect_info()
        print(self.info)
        self.action_saveas.setEnabled(True)
        self.action_run.setEnabled(True)

    def trigger_new(self):
        global count_tabs
        new_tab = Window()
        self.tab.addTab(new_tab, 'untitled' + str(count_tabs))
        self.tab.setCurrentWidget(new_tab)
        count_tabs += 1
        self.action_submit.setEnabled(True)

        #button = QtWidgets.QPushButton('x')

        #tab_bar = self.tab.tabBar()
        #tab_bar.setTabButton(self.tab.currentIndex(), QtWidgets.QTabBar.RightSide, button)

    def trigger_save(self):
        file = open(self.json_path, 'w')
        json.dump(self.info, file)
        file.close()

    def trigger_saveas(self):
        self.json_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'All Files (*);;Json Files (*.json)')
        if self.json_path:
            file = open(self.json_path, 'w')
            json.dump(self.info, file)
            file.close()
            self.action_save.setEnabled(True)
            i = self.tab.currentIndex()
            self.tab.setTabText(i, str(path_leaf(self.json_path)))

    def trigger_open(self):
        self.json_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Json Files (*.json)')
        if self.json_path:
            file = open(self.json_path, 'r')
            j = file.read()
            self.info = json.loads(j)
            file.close()

            new_tab = Window()
            new_tab.set_info(self.info)

            self.tab.addTab(new_tab, str(path_leaf(self.json_path)))
            self.tab.setCurrentWidget(new_tab)

            self.action_save.setEnabled(True)
            self.action_saveas.setEnabled(True)
            self.action_run.setEnabled(True)

    def trigger_quit(self):
        QtWidgets.qApp.quit()


app = QtWidgets.QApplication(sys.argv)
a_window = Main()
a_window.show()
sys.exit(app.exec_())
