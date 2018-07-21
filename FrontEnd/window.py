# -*- coding: utf-8 -*-
import sys
import sip
import json
from PyQt5 import QtWidgets, QtGui, QtCore

count = 0


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


class Aesthetic(QtWidgets.QWidget):
    def __init__(self, obj):
        super(Aesthetic, self).__init__()

        fon = QtWidgets.QHBoxLayout()
        fon.addWidget(obj)
        fon.addStretch(40)
        self.setLayout(fon)


class LineEdits(QtWidgets.QWidget):
    def __init__(self, width, size):
        super(LineEdits, self).__init__()

        self.fon = QtWidgets.QHBoxLayout()
        self.lines = []

        self.init_ui(width, size)

    def init_ui(self, width, size):
        for i in range(width):
            line = QtWidgets.QLineEdit('0')
            self.lines.append(line)
            self.lines[i].setMinimumWidth(size)
            self.lines[i].setMaximumWidth(size)
            self.fon.addWidget(self.lines[i])
        self.fon.addStretch(40)

        self.setLayout(self.fon)

    def collect_info(self):
        info = []
        for i in range(len(self.lines)):
            if isint(str(self.lines[i].text())) > 0:
                info.append([i + 1, int(str(self.lines[i].text()))])
        return info


class SwitchButtons(QtWidgets.QWidget):
    def __init__(self, width, size):
        super(SwitchButtons, self).__init__()

        self.fon = QtWidgets.QHBoxLayout()
        self.buttons = []

        self.init_ui(width, size)

    def init_ui(self, width, size):
        for i in range(width):
            button = QtWidgets.QPushButton('✓')
            button.setCheckable(True)
            button.setStyleSheet("background-color: green")
            button.clicked[bool].connect(self.toggle)
            self.buttons.append(button)
            self.buttons[i].setMinimumWidth(size)
            self.buttons[i].setMaximumWidth(size)
            self.fon.addWidget(self.buttons[i])
        self.fon.addStretch(40)

        self.setLayout(self.fon)

    def toggle(self, pressed):
        sender = self.sender()
        if pressed:
            sender.setText('✕')
            sender.setStyleSheet("background-color: red")
        else:
            sender.setText('✓')
            sender.setStyleSheet("background-color: green")

    def collect_info(self):
        info = []
        for i in range(len(self.buttons)):
            if not self.buttons[i].isChecked():
                info.append(i + 1)
        return info


class Wild(QtWidgets.QWidget):
    def __init__(self):
        super(Wild, self).__init__()

        self.fon = QtWidgets.QGridLayout()

        self.label_multiplier = QtWidgets.QLabel('multiplier')
        self.line_multiplier = QtWidgets.QLineEdit()

        self.label_expand = QtWidgets.QLabel('expand')
        self.checkbox_expand = QtWidgets.QCheckBox()

        self.label_substitute = QtWidgets.QLabel('substitute')
        self.line_substitute = QtWidgets.QLineEdit()

        self.init_ui()

    def init_ui(self):
        self.fon.addWidget(self.label_multiplier, 0, 0)
        self.fon.addWidget(self.line_multiplier, 0, 1)

        self.fon.addWidget(self.label_expand, 1, 0)
        self.fon.addWidget(self.checkbox_expand, 1, 1)

        self.fon.addWidget(self.label_substitute, 2, 0)
        self.fon.addWidget(self.line_substitute, 2, 1)

        self.setLayout(self.fon)

    def collect_info(self):
        d = {}
        if isint(str(self.line_multiplier.text())) >= 0:
            d.update({'multiplier': int(str(self.line_multiplier.text()))})
        if self.checkbox_expand.checkState() == QtCore.Qt.Checked:
            d.update({'expand': True})
        return d


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
        self.line_direction.setMinimumWidth(100)
        self.line_direction.setMaximumWidth(100)
        self.line_direction.addItems(['left', 'right', 'both', 'any'])

        self.label_position = QtWidgets.QLabel('position')
        self.buttons_position = SwitchButtons(self.width, 28)

        self.label_scatter = QtWidgets.QLabel('scatter')
        self.checkbox_scatter = QtWidgets.QCheckBox()

        self.label_freespins = QtWidgets.QLabel('freespins')
        self.line_freespins = None

        self.label_wild = QtWidgets.QLabel('wild')
        self.checkbox_wild = QtWidgets.QCheckBox()

        self.wild = None

        self.frame = QtWidgets.QFrame()

        self.init_ui(width)

    def init_ui(self, width):
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
            self.line_freespins = LineEdits(self.width, 28)
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
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(242, 224, 63))
            self.frame.setPalette(p)

        elif self.checkbox_scatter.checkState() == QtCore.Qt.Checked:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(58, 209, 204))
            self.frame.setPalette(p)

        else:
            self.frame.setAutoFillBackground(True)
            p = self.frame.palette()
            p.setColor(self.frame.backgroundRole(), QtGui.QColor(200, 200, 200))
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


class Symbol(QtWidgets.QWidget):
    def __init__(self, count, width):
        super(Symbol, self).__init__()

        self.fon_symbol = QtWidgets.QVBoxLayout()
        self.fon_type = QtWidgets.QGridLayout()
        self.fon_type.setRowStretch(0, 1)
        self.fon_type.setRowStretch(1, 40)
        self.border = QtWidgets.QLabel(' ')
        self.label_base = QtWidgets.QLabel('base')
        self.label_free = QtWidgets.QLabel('free')

        self.fon_name = QtWidgets.QHBoxLayout()
        self.label_name = QtWidgets.QLabel('name     ')
        self.line_name = QtWidgets.QLineEdit('symbol_' + str(count + 1))

        self.fon_payment = QtWidgets.QHBoxLayout()
        self.label_payment = QtWidgets.QLabel('payment')
        self.line_payment = None

        self.width = width
        self.base = Gametype('base', self.width)
        self.free = None

        self.button_free = QtWidgets.QPushButton('Specify \n free game \n properties')
        self.button_state = True

        self.init_ui()

    def init_ui(self):
        self.fon_name.addWidget(self.label_name)
        self.fon_name.addWidget(Aesthetic(self.line_name))

        self.fon_payment.addWidget(self.label_payment)
        self.line_payment = LineEdits(self.width, 40)
        self.fon_payment.addWidget(self.line_payment)

        self.fon_symbol.addLayout(self.fon_name)
        self.fon_symbol.addLayout(self.fon_payment)
        self.fon_symbol.addLayout(self.fon_type)

        self.fon_type.addWidget(self.base, 0, 0, 2, 1)

        self.fon_type.addWidget(self.button_free, 0, 2)
        self.button_free.clicked.connect(self.button_free_clicked)

        self.fon_symbol.addWidget(self.border)

        self.fon_symbol.setSpacing(0)
        self.setLayout(self.fon_symbol)

    def button_free_clicked(self):
        if self.button_state:
            self.free = Gametype('free', self.width)
            self.base.fon.addWidget(self.base.label, 0, 0, 1, 2)
            self.free.fon.addWidget(self.free.label, 0, 0, 1, 2)
            self.fon_type.addWidget(self.free, 0, 1, 2, 1)
            self.button_free.setText('Cancel')
            self.free.fon_cancel.addWidget(self.button_free)
            self.button_state = False

        else:
            self.fon_type.addWidget(self.button_free, 0, 2)

            self.base.fon.removeWidget(self.base.label)
            sip.delete(self.base.label)
            self.base.label = QtWidgets.QLabel('base')

            self.free.fon.removeWidget(self.free.label)
            sip.delete(self.free.label)
            self.free.label = QtWidgets.QLabel('free')

            self.fon_type.removeWidget(self.free)
            sip.delete(self.free)
            self.free = None
            self.button_free.setText('Specify \n free game \n properties')
            self.fon_type.addWidget(self.button_free, 0, 2)
            self.button_state = True

    def collect_info(self):
        d = {}
        d.update({'name': str(self.line_name.text())})
        d.update({'payment': self.line_payment.collect_info()})
        d.update({'base': self.base.collect_info()})
        if self.free is not None:
            d.update({'free': self.free.collect_info()})
        return d


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.fon = QtWidgets.QGridLayout()

        self.frame_symbols = QtWidgets.QFrame()
        self.fon_symbols = QtWidgets.QVBoxLayout()
        self.grid_symbols = QtWidgets.QGridLayout()

        self.add = QtWidgets.QPushButton('Add symbol')

        self.label_window = QtWidgets.QLabel('window')
        self.line_width = QtWidgets.QLineEdit('5')
        self.line_height = QtWidgets.QLineEdit('3')
        self.width = 5
        self.height = 3

        self.label_symbol = QtWidgets.QLabel('symbols')

        self.fon_window = QtWidgets.QHBoxLayout()

        self.symbols = []
        self.deleteButtons = []

        self.label_lines = QtWidgets.QLabel('lines')

        self.label_freemultiplier = QtWidgets.QLabel('free multiplier')
        self.line_freemultiplier = QtWidgets.QLineEdit()

        self.label_distance = QtWidgets.QLabel('distance')
        self.line_distance = QtWidgets.QLineEdit()

        self.label_rtp = QtWidgets.QLabel('RTP')
        self.line_rtp = QtWidgets.QLineEdit()

        self.label_volatility = QtWidgets.QLabel('volatility')
        self.line_volatility = QtWidgets.QLineEdit()

        self.label_hitrate = QtWidgets.QLabel('hitrate')
        self.line_hitrate = QtWidgets.QLineEdit()

        self.label_baseRTP = QtWidgets.QLabel('base RTP')
        self.line_baseRTP = QtWidgets.QLineEdit()

        self.init_ui()

    def init_ui(self):
        self.fon.setRowStretch(0, 1)
        self.fon.setRowStretch(1, 1)
        self.fon.setRowStretch(2, 40)

        self.fon.setColumnStretch(0, 1)
        self.fon.setColumnStretch(1, 1)
        self.fon.setColumnStretch(3, 40)

        self.fon.addWidget(self.label_window, 0, 0)

        self.fon.addWidget(self.line_width, 0, 1)
        self.line_width.setMinimumWidth(40)
        self.line_width.setMaximumWidth(40)
        self.fon.addWidget(self.line_height, 0, 2)
        self.line_height.setMinimumWidth(40)
        self.line_height.setMaximumWidth(40)

        self.grid_symbols.setHorizontalSpacing(0)

        self.fon.addWidget(self.label_symbol, 1, 0)
        self.fon.addWidget(self.frame_symbols, 1, 1, 2, 3)
        self.frame_symbols.setLayout(self.fon_symbols)
        self.frame_symbols.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_symbols.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.fon_symbols.addLayout(self.grid_symbols)
        self.fon_symbols.setStretchFactor(self.grid_symbols, 40)
        self.fon_symbols.addWidget(self.add)

        self.add.clicked.connect(self.add_click)

        self.line_width.textChanged.connect(self.width_changed)
        self.line_height.textChanged.connect(self.height_changed)

        self.fon.addWidget(self.label_lines, 3, 0)

        self.fon.addWidget(self.label_freemultiplier, 4, 0)
        self.fon.addWidget(self.line_freemultiplier, 4, 1)

        self.fon.addWidget(self.label_distance, 5, 0)
        self.fon.addWidget(self.line_distance, 5, 1)

        self.fon.addWidget(self.label_rtp, 6, 0)
        self.fon.addWidget(self.line_rtp, 6, 1)

        self.fon.addWidget(self.label_volatility, 7, 0)
        self.fon.addWidget(self.line_volatility, 7, 1)

        self.fon.addWidget(self.label_hitrate, 8, 0)
        self.fon.addWidget(self.line_hitrate, 8, 1)

        self.fon.addWidget(self.label_baseRTP, 9, 0)
        self.fon.addWidget(self.line_baseRTP, 9, 1)

        self.setLayout(self.fon)

    def add_click(self):
        global count

        symbol = Symbol(count, self.width)
        self.symbols.append(symbol)

        button_delete = QtWidgets.QPushButton('✕')
        button_delete.setMinimumSize(28, 28)
        button_delete.setMaximumSize(28, 28)
        self.deleteButtons.append(button_delete)
        self.deleteButtons[-1].clicked.connect(self.delete_click)

        self.grid_symbols.addWidget(self.symbols[-1], 2 * count, 0, 2, 1)

        self.symbols[-1].setAutoFillBackground(True)
        p = self.symbols[-1].palette()
        p.setColor(self.symbols[-1].backgroundRole(), QtGui.QColor(200, 200, 200))
        self.symbols[-1].setPalette(p)

        self.grid_symbols.addWidget(self.deleteButtons[-1], 2 * count, 1, 1, 1)

        count += 1

    def delete_click(self):
        sender = self.sender()
        num = self.deleteButtons.index(sender)

        self.grid_symbols.removeWidget(self.symbols[num])
        sip.delete(self.symbols[num])
        del self.symbols[num]

        self.grid_symbols.removeWidget(self.deleteButtons[num])
        sip.delete(self.deleteButtons[num])
        del self.deleteButtons[num]

    def width_changed(self):
        if isint(str(self.line_width.text())) > 0:
            self.width = int(str(self.line_width.text()))
            for i in range(len(self.symbols)):
                self.symbols[i].width = self.width

                self.symbols[i].fon_payment.removeWidget(self.symbols[i].line_payment)
                sip.delete(self.symbols[i].line_payment)

                self.symbols[i].line_payment = LineEdits(self.width, 40)
                self.symbols[i].fon_payment.addWidget(self.symbols[i].line_payment)

                self.symbols[i].base.width = self.width

                self.symbols[i].base.fon.removeWidget(self.symbols[i].base.buttons_position)
                sip.delete(self.symbols[i].base.buttons_position)
                self.symbols[i].base.buttons_position = SwitchButtons(self.width, 28)
                self.symbols[i].base.fon.addWidget(self.symbols[i].base.buttons_position, 2, 1)

                if self.symbols[i].base.checkbox_scatter.checkState() == QtCore.Qt.Checked:
                    self.symbols[i].base.fon.removeWidget(self.symbols[i].base.line_freespins)
                    sip.delete(self.symbols[i].base.line_freespins)
                    self.symbols[i].base.line_freespins = LineEdits(self.width, 28)
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
                        self.symbols[i].free.line_freespins = LineEdits(self.width, 28)
                        self.symbols[i].free.fon.addWidget(self.symbols[i].free.line_freespins, 4, 1)

    def height_changed(self):
        if isint(str(self.line_height.text())) > 0:
            self.height = int(str(self.line_height.text()))

    def collect_info(self):
        d = {}
        d.update({'window': [self.width, self.height]})
        symbols = []
        for i in range(len(self.symbols)):
            symbols.append(self.symbols[i].collect_info())
        d.update({'symbol': symbols})
        if isint(str(self.line_freemultiplier.text())) >= 0:
            d.update({'free_multiplier': int(str(self.line_freemultiplier.text()))})

        if isint(str(self.line_distance.text())) >= 0:
            d.update({'distance': int(str(self.line_distance.text()))})

        if isfloat(str(self.line_rtp.text())):
            d.update({'RTP': float(str(self.line_rtp.text()))})

        if isfloat(str(self.line_volatility.text())):
            d.update({'volatility': float(str(self.line_volatility.text()))})

        if isfloat(str(self.line_hitrate.text())):
            d.update({'hitrate': float(str(self.line_hitrate.text()))})

        if isfloat(str(self.line_baseRTP.text())):
            d.update({'baseRTP': float(str(self.line_baseRTP.text()))})
        return d


class Scroll(QtWidgets.QScrollArea):
    def __init__(self):
        super(Scroll, self).__init__()

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.window = Window()

        self.setWidget(self.window)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.setWindowTitle('Azino 777')
        self.setWindowIcon(QtGui.QIcon('icons/yarlyk.png'))
        self.setGeometry(200, 200, 1000, 600)
        self.scroll = Scroll()

        self.tool_file = self.addToolBar('file')
        self.tool_run = self.addToolBar('run')
        self.bar = self.menuBar()

        self.action_new = QtWidgets.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        self.action_new.setShortcut('Ctrl+N')

        self.action_open = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        self.action_open.setShortcut('Ctrl+O')

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

        self.action_run = QtWidgets.QAction(QtGui.QIcon('icons/run.png'), 'Run', self)
        self.action_run.setEnabled(False)

        self.action_submitnrun = QtWidgets.QAction(QtGui.QIcon('icons/submitnrun.png'), 'Submit and run', self)
        self.action_submitnrun.triggered.connect(self.trigger_submit)

        self.info = None

        self.json_path = None

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.scroll)

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

    def trigger_submit(self):
        self.info = self.scroll.window.collect_info()
        print(self.info)
        self.action_saveas.setEnabled(True)
        self.action_run.setEnabled(True)

    def trigger_save(self):
        data = json.dumps(self.info)
        file = open(self.json_path, 'w')
        json.dump(data, file)
        file.close()

    def trigger_saveas(self):
        self.json_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'All Files (*);;Json Files (*.json)')
        if self.json_path:
            data = json.dumps(self.info)
            file = open(self.json_path, 'w')
            json.dump(data, file)
            file.close()
            self.action_save.setEnabled(True)

    def trigger_quit(self):
        QtWidgets.qApp.quit()


app = QtWidgets.QApplication(sys.argv)
a_window = Main()
a_window.show()
sys.exit(app.exec_())
