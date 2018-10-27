import numpy as np
from PyQt5 import QtCore
import FrontEnd.sub_functions as sub

# LineEdits


def collect_line_info(self):
    info = []
    for i in range(len(self.lines)):
        if sub.isint(str(self.lines[i].text())) > 0:
            info.append([i + 1, int(str(self.lines[i].text()))])
    return info


def arrange_line_info(self):
    info = []
    for i in range(len(self.lines)):
        if sub.isint(str(self.lines[i].text())) > 0:
            info.append(int(str(self.lines[i].text())))
        else:
            return None
    return info


def set_line_info(self, interim_info):
    for obj in interim_info:
        self.lines[obj[0] - 1].setText(str(obj[1]))


def fill_line_info(self, interim_info):
    for i in range(len(interim_info)):
        self.lines[i].setText(str(interim_info[i]))

# SwitchButtons


def collect_button_info(self):
    info = []
    for i in range(len(self.buttons)):
        if not self.buttons[i].isChecked():
            info.append(i + 1)
    return info


def set_button_info(self, interim_symbol_type):
    for i in range(len(self.buttons)):
        if i + 1 not in interim_symbol_type['position']:
            self.buttons[i].click()

# Wild


def collect_wild_info(self):
    d = {}
    if sub.isint(str(self.line_multiplier.text())) >= 0:
        d.update({'multiplier': int(str(self.line_multiplier.text()))})
    if self.checkbox_expand.checkState() == QtCore.Qt.Checked:
        d.update({'expand': True})
    words = str(self.line_substitute.text()).split('; ')
    if words is not None and words != ['']:
        d.update({'substitute': words})
    return d


def set_wild_info(self, interim_symbol_type):
    if 'multiplier' in interim_symbol_type['wild']:
        self.line_multiplier.setText(str(interim_symbol_type['wild']['multiplier']))

    if 'expand' in interim_symbol_type['wild'] and interim_symbol_type['wild']['expand'] is True:
        self.checkbox_expand.setChecked(True)

    if 'substitute' in interim_symbol_type['wild']:
        self.line_substitute.setText('; '.join(interim_symbol_type['wild']['substitute']))

# Gametype


def collect_gametype_info(self):
    d = {}
    d.update({'direction': str(self.line_direction.currentText())})
    d.update({'position': self.buttons_position.collect_button_info()})
    if self.box_scatter.isChecked() is True:
        d.update({'scatter': self.line_freespins.collect_line_info()})
    if self.box_wild.isChecked() is True:
        d.update({'wild': self.wild.collect_wild_info()})
    if self.mode is False:
        d.update({'frequency': self.line_frequency.arrange_line_info()})
    return d


def set_gametype_info(self, interim_symbol_type):
    if 'direction' in interim_symbol_type:
        index = self.line_direction.findText(interim_symbol_type['direction'], QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.line_direction.setCurrentIndex(index)

    if 'position' in interim_symbol_type:
        self.buttons_position.set_button_info(interim_symbol_type)

    if 'scatter' in interim_symbol_type:
        self.box_scatter.setChecked(True)
        self.line_freespins.set_line_info(interim_symbol_type['scatter'])

    if 'wild' in interim_symbol_type:
        self.box_wild.setChecked(True)
        self.wild.set_wild_info(interim_symbol_type)

    if 'frequency' in interim_symbol_type:
        self.line_frequency.fill_line_info(interim_symbol_type['frequency'])

# Symbol


def collect_symbol_info(self):
    d = {}
    if str(self.line_name.text()) == '':
        raise Exception('symbol name should not be empty')
    if ';' in str(self.line_name.text()):
        raise Exception('symbol name should not contain ";" in it')
    else:
        d.update({'name': str(self.line_name.text())})
    d.update({'payment': self.line_payment.collect_line_info()})
    d.update({'base': self.base.collect_gametype_info()})
    if self.free is not None:
        d.update({'free': self.free.collect_gametype_info()})
    return d


def set_symbol_info(self, interim_symbol):
    self.line_name.setText(str(interim_symbol['name']))
    self.line_payment.set_line_info(interim_symbol['payment'])
    if 'base' in interim_symbol:
        self.base.set_gametype_info(interim_symbol['base'])
    if 'free' in interim_symbol:
        self.button_free_clicked()
        self.free.set_gametype_info(interim_symbol['free'])

# Window


def collect_info(self):
    d = {}
    d.update({'window': [self.width, self.height]})
    symbols = []
    for i in range(len(self.symbols)):
        symbols.append(self.symbols[i].collect_symbol_info())
    d.update({'symbols': symbols})

    lines = []
    for i in range(len(self.lines)):
        if self.lines[i].arrange_line_info() is not None:
            lines.append(self.lines[i].arrange_line_info())
    d.update({'lines': lines})

    if sub.isint(str(self.line_freemultiplier.text())) >= 0:
        d.update({'free_multiplier': int(str(self.line_freemultiplier.text()))})

    if sub.isint(str(self.line_distance.text())) >= 0:
        d.update({'distance': int(str(self.line_distance.text()))})

    if self.mode is True:
        if sub.isfloat(str(self.line_rtp.text())) and sub.isfloat(str(self.line_rtp_error.text())):
            d.update({'RTP': [float(str(self.line_rtp.text())), float(str(self.line_rtp_error.text()))]})
        else:
            raise Exception('RTP was not set correctly')

        if sub.isfloat(str(self.line_volatility.text())) and sub.isfloat(str(self.line_volatility_error.text())):
            d.update({'volatility': [float(str(self.line_volatility.text())), float(str(self.line_volatility_error.text()))]})
        else:
            raise Exception('volatility was not set correctly')

        if sub.isfloat(str(self.line_hitrate.text())) and sub.isfloat(str(self.line_hitrate_error.text())):
            d.update({'hitrate': [float(str(self.line_hitrate.text())), float(str(self.line_hitrate_error.text()))]})
        else:
            raise Exception('hitrate was not set correctly')

        if sub.isfloat(str(self.line_baseRTP.text())) and sub.isfloat(str(self.line_baseRTP_error.text())):
            d.update({'baseRTP': [float(str(self.line_baseRTP.text())), float(str(self.line_baseRTP_error.text()))]})
        else:
            raise Exception('base RTP was not set correctly')

    return d


def collect_frequency(self):
    base_frequency = []
    free_frequency = []
    for symbol in self.symbols:
        if symbol.base.line_frequency.arrange_line_info() is None:
            i = self.symbols.index(symbol) + 1
            raise Exception('Frequency of symbol ' + str(i) + ' was not set correctly')
        else:
            base_frequency.append(symbol.base.line_frequency.arrange_line_info())

        if symbol.free is None:
            free_frequency.append(symbol.base.line_frequency.arrange_line_info())
        else:
            if symbol.free.line_frequency.arrange_line_info() is None:
                i = self.symbols.index(symbol) + 1
                raise Exception('Frequency of symbol ' + str(i) + ' was not set correctly')
            else:
                free_frequency.append(symbol.free.line_frequency.arrange_line_info())

    return {'base_frequency': np.array(base_frequency).T.tolist(), 'free_frequency': np.array(free_frequency).T.tolist()}


def set_info(self, interim):
    if 'window' in interim:
        self.line_width.setText(str(interim['window'][0]))
        self.width = interim['window'][0]
        self.line_height.setText(str(interim['window'][1]))
        self.height = interim['window'][1]

    for i in range(len(interim['symbols'])):
        self.click_add_symbol(True)
        self.symbols[i].set_symbol_info(interim['symbols'][i])

    for i in range(len(interim['lines'])):
        self.click_add_line()
        self.lines[i].fill_line_info(interim['lines'][i])

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
