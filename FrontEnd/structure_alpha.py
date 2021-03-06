# coding=utf-8
import time

import numpy as np
import itertools
import re
import copy
import matplotlib.pyplot as plt
from Descent.main_process import descent_base
from Descent.main_process import descent_free
from Descent.main_process import rebalance
from Descent.main_process import is_done
from Descent.main_process import print_res
from Descent.main_process import create_plot

from FrontEnd import moments
# import moments
import FrontEnd.reelWork.reel_generator_alpha as rg

Inf = 0.025
wildInf = 0.025
ewildInf = 0.015


def sought(dictionary, string):
    K = list(dictionary.keys())[:]
    for i in range(len(K)):
        prob = re.compile(K[i], re.IGNORECASE)
        if prob.match(string) or prob.match(string + 's'):
            return dictionary[K[i]]
    return None


class Wild:
    def __init__(self, interim, type, i):
        self.multiplier = 1
        if sought(sought(sought(interim, 'symbol')[i], type), 'wild'):
            if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'multiplier'):
                self.multiplier = sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'multiplier')
            self.expand = sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'expand')
        else:
            self.expand = False
        self.substitute = []


class Symbol:
    def __init__(self, interim, type, i, w):
        self.group_by = [1]
        self.name = sought(sought(interim, 'symbol')[i], 'name')
        self.payment = [0] * (w + 1)
        for j in range(len(sought(sought(interim, 'symbol')[i], 'payment'))):
            self.payment[sought(sought(interim, 'symbol')[i], 'payment')[j][0]] = \
                sought(sought(interim, 'symbol')[i], 'payment')[j][1]

        self.substituted_by = []
        self.substituted_by_e = []
        if sought(sought(interim, 'symbol')[i], type):
            if sought(sought(sought(interim, 'symbol')[i], type), 'direction'):
                self.direction = sought(sought(sought(interim, 'symbol')[i], type), 'direction')
            else:
                self.direction = "left"
            if sought(sought(sought(interim, 'symbol')[i], type), 'position') is not None:
                self.position = sought(sought(sought(interim, 'symbol')[i], type), 'position')[:]
                self.position[:] = [x - 1 for x in self.position]
            else:
                self.position = np.arange(0, w, 1)
            if str(sought(sought(sought(interim, 'symbol')[i], type), 'scatter')) == "0" or str(
                    sought(sought(sought(interim, 'symbol')[i], type), 'scatter')) == '[]':
                self.scatter = [0] * (w + 1)
            else:
                if sought(sought(sought(interim, 'symbol')[i], type), 'scatter'):
                    self.scatter = [0] * (w + 1)
                    for j in range(len(sought(sought(sought(interim, 'symbol')[i], type), 'scatter'))):
                        self.scatter[sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][0]] = \
                            sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][1]
                else:
                    self.scatter = sought(sought(sought(interim, 'symbol')[i], type), 'scatter')

            if str(sought(sought(sought(interim, 'symbol')[i], type), 'wild')) != 'None':
                self.wild = Wild(interim, type, i)
            else:
                self.wild = False
            if sought(sought(sought(interim, 'symbol')[i], type), 'group_by'):
                self.group_by = sought(sought(sought(interim, 'symbol')[i], type), 'group_by')
            else:
                self.group_by = [1]
        else:
            self.direction = "left"
            self.position = np.arange(0, w, 1)
            self.scatter = False
            self.wild = False
            if sought(sought(interim, 'symbol')[i], 'group_by'):
                # print(self.name, self.group_by)
                self.group_by = sought(sought(interim, 'symbol')[i], 'group_by')
                # print(self.name, self.group_by)


class Gametype:
    def __init__(self, interim, type, w, lines, height, distance):
        self.name = type
        self.distance = distance
        if sought(interim, 'symbol'):
            self.symbol = [None] * len(sought(interim, 'symbol'))
            for i in range(len(sought(interim, 'symbol'))):
                if str(sought(sought(interim, 'symbol')[i], type)) != 'None':
                    self.symbol[i] = Symbol(interim, type, i, w)
                else:
                    self.symbol[i] = Symbol(interim, 'base', i, w)
        else:
            raise Exception('Field "symbol" is not found in json file.')

        self.multiplier = 1
        if type == 'free' and sought(interim, 'free_multiplier'):
            self.multiplier = sought(interim, 'free_multiplier')

        self.wildlist = []
        self.ewildlist = []
        self.scatterlist = []
        self.num_comb = np.zeros((len(self.symbol), w + 1))
        self.reels = [] * w
        self.frequency = [] * w

        self.scatter_num_comb = []
        self.simple_num_comb = []
        self.simple_num_comb_first = []

        self.lines = lines
        # (line_id, symbol_id, count_killed for every reel from 0 to window_width)
        self.count_killed = {line_id: {symbol_id: [0 for _ in range(w)] for symbol_id in range(len(self.symbol))} for
                             line_id in range(len(self.lines))}

        self.window = [w, height]
        self.max_border = 0.9 * (1 / height)

    def wildlists(self):
        for i in range(len(self.symbol)):
            if self.symbol[i].wild:
                if self.symbol[i].wild.expand:
                    self.ewildlist.append(i)
                else:
                    self.wildlist.append(i)

    def scatterlists(self):
        for i in range(len(self.symbol)):
            if self.symbol[i].scatter is not False and self.symbol[i].scatter is not None:
                self.scatterlist.append(i)

    def transsubst(self, interim, type, i):
        if sought(sought(sought(interim, 'symbol')[i], type), 'wild') is not None:
            if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute'):
                self.symbol[i].wild.substitute.append(i)
                for j in range(len(sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute'))):
                    for k in range(len(sought(interim, 'symbol'))):
                        if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute')[
                            j] == sought(sought(interim, 'symbol')[k], 'name'):
                            self.symbol[i].wild.substitute.append(k)
            else:
                for j in range(len(self.symbol)):
                    if not self.symbol[j].scatter:
                        self.symbol[i].wild.substitute.append(j)

    def substituted_by(self):
        for i in range(len(self.symbol)):
            for j in self.wildlist:
                if i in self.symbol[j].wild.substitute and i != j:
                    self.symbol[i].substituted_by.append(j)

    def substituted_by_e(self):
        for i in range(len(self.symbol)):
            for j in self.ewildlist:
                if i in self.symbol[j].wild.substitute and i != j:
                    self.symbol[i].substituted_by_e.append(j)

    def combination_value(self, i, comb):
        return self.symbol[i].payment[comb]

    def combination_freespins(self, i, comb):
        if self.symbol[i].scatter:
            return self.symbol[i].scatter[comb]
        else:
            return 0

    def fill_frequency(self, frequency):
        self.frequency = frequency

    def reel_generator(self, frequency_array, window_width, reel_distance, validate=False):
        self.reels = rg.reel_generator(gametype=self, frequency_array=frequency_array, window_width=window_width,
                                       reel_distance=reel_distance, validate=validate)

    def fill_reels(self, input_reels):
        self.reels = copy.deepcopy(input_reels)

    def fill_frequency_from_reels(self, reels):
        print("reels on fill_frequency_from_reels start: ", reels)
        frequency = []
        max_symbol_id = -1
        for reel in reels:
            for symbol_id in reel:
                if symbol_id > max_symbol_id:
                    max_symbol_id = symbol_id
        for reel_id in range(len(reels)):
            frequency.append([0 for _ in range(max_symbol_id + 1)])
            for symbol_id in reels[reel_id]:
                frequency[reel_id][symbol_id] += 1
        self.frequency = frequency

    get_combination = rg.get_simple_combination
    count_combinations2 = rg.count_combinations2
    count_num_comb = rg.count_num_comb
    fill_num_comb = rg.fill_num_comb

    fill_count_killed = rg.fill_count_killed
    fill_scatter_num_comb = rg.fill_scatter_num_comb
    fill_simple_num_comb = rg.fill_simple_num_comb
    create_simple_num_comb = rg.create_simple_num_comb
    get_simple_payment = rg.get_simple_payment
    get_wilds_in_comb = rg.get_wilds_in_comb

    Exi2 = moments.Exi2
    Exieta = moments.Exieta
    Eeta = moments.Eeta
    Eeta2 = moments.Eeta2

    def all_combinations(self):
        c = 1
        for i in range(len(self.reels)):
            c = c * len(self.reels[i])
        return c

    def all_combinations2(self):
        c = 1
        for reel in self.frequency:
            c = c * sum(reel)
        return c

    def fill_reels(self, in_reels):
        self.reels = copy.deepcopy(in_reels)

    def count_base_RTP_gametype(self, window, lines, simple_num_comb):
        s = 0
        for str_with_count in simple_num_comb:
            string = str_with_count[0]
            payment = str_with_count[2]
            s += str_with_count[1] / self.all_combinations2() * payment

        for scatter_comb in self.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(window[0] + 1):
                s += self.symbol[scat].payment[cnt] * len(lines) * counts[
                    cnt] / self.all_combinations2()
        return s / len(lines)

    def check(self, frequency):
        n_reels = len(frequency)
        if n_reels <= 0:
            # print('failed caused by n_reels')
            return False
        n_symbols = len(frequency[0])
        reels_lens = []
        for reel_id in range(n_reels):
            for symbol_id in range(n_symbols):
                if frequency[reel_id][symbol_id] < 0:
                    # print('failed cause frequency < 0')
                    return False
                elif frequency[reel_id][symbol_id] > 0 and reel_id not in self.symbol[symbol_id].position:
                    # print('failed cause frequency > 0 on banned reel')
                    return False
            reels_lens.append(sum(frequency[reel_id]))
        # if max(reels_lens) != min(reels_lens):
        #     return False
        return True

    def infPart(self, symbol_id):
        if symbol_id in self.ewildlist:
            return ewildInf
        elif symbol_id in self.wildlist:
            return wildInf
        else:
            return Inf


# noinspection PyArgumentList
class Game:
    def __init__(self, interim):

        if sought(interim, 'window'):
            self.window = sought(interim, 'window')[:]
        else:
            self.window = [5, 3]

        if sought(interim, 'line'):
            self.line = sought(interim, 'line')[:]
        else:
            raise Exception('Field "line" is not found in json file.')

        if sought(interim, 'distance'):
            self.distance = sought(interim, 'distance')
        else:
            self.distance = self.window[1]

        self.base = Gametype(interim, 'base', self.window[0], self.line, self.window[1], self.distance)
        self.free = Gametype(interim, 'free', self.window[0], self.line, self.window[1], self.distance)

        if sought(interim, 'free_multiplier'):
            self.free_multiplier = sought(interim, 'free_multiplier')
        else:
            self.free_multiplier = 1

        self.RTP = sought(interim, 'RTP')
        self.volatility = sought(interim, 'volatility')
        self.hitrate = sought(interim, 'hitrate')
        self.baseRTP = sought(interim, 'baseRTP')
        self.borders = sought(interim, 'border')
        self.weights = sought(interim, 'weight')

        self.parameters = {'base_rtp': -1, 'freemean': -1, 'rtp': -1, 'sdnew': -1, 'hitrate': -1}

        self.base.wildlists()
        self.base.scatterlists()

        self.free.wildlists()
        self.free.scatterlists()

        # заполнение массива substitute для каждого вайлда из обычной игры
        for i in itertools.chain(self.base.wildlist, self.base.ewildlist):
            self.base.transsubst(interim, 'base', i)

        # заполнение массива substitute для каждого вайлда из бесплатной игры
        for i in itertools.chain(self.free.wildlist, self.free.ewildlist):
            if sought(sought(interim, 'symbol')[i], 'free'):
                self.free.transsubst(interim, 'free', i)
            else:
                self.free.symbol[i].wild.substitute = self.base.symbol[i].wild.substitute

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        self.base.substituted_by()

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        self.base.substituted_by_e()

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        self.free.substituted_by()

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        self.free.substituted_by_e()

    def delete_line(self, number):
        for i in range(number):
            self.line.pop()

    # noinspection PyPep8Naming,SpellCheckingInspection
    def count_base_RTP2(self, game, lines):
        simple_num_comb = [self.base.simple_num_comb, self.free.simple_num_comb]
        if len(lines) == 1:
            simple_num_comb = [self.base.simple_num_comb_first, self.free.simple_num_comb_first]

        if game == 'base':
            return self.base.count_base_RTP_gametype(self.window, lines, simple_num_comb[0])
        elif game == 'free':
            return self.free.count_base_RTP_gametype(self.window, lines, simple_num_comb[1])

    # noinspection SpellCheckingInspection
    def freemean2(self, lines):
        s = self.count_base_RTP2('free', lines)
        v = 0
        for scatter_comb in self.free.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                v += self.free.symbol[scat].scatter[cnt] * counts[cnt] / self.free.all_combinations2()

        return self.free_multiplier * s * 1.0 / (1 - v)

    # noinspection PyPep8Naming
    def count_RTP2(self, FreeMean, base_rtp):
        s = 0
        s += base_rtp
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                s += FreeMean * self.base.symbol[scat].scatter[cnt] * counts[cnt] / self.base.all_combinations2()
        return s

    def count_volatility2new(self, FreeMean, RTP):
        # xi - random variable, equals payment for combination (base_rtp = Exi)
        # eta - random variable, equals the number of freespins given for combination
        # zeta - random variable, equals payment for freespin (FreeMean = Ezeta)
        Exi2 = self.base.Exi2(self.window[0], self.line)
        Exieta = self.base.Exieta(self.window[0], self.line)
        Eeta = self.base.Eeta(self.window[0])
        Eeta2 = self.base.Eeta2(self.window[0])

        Efree_xi2 = self.free.Exi2(self.window[0], self.line)
        Efree_xieta = self.free.Exieta(self.window[0], self.line)
        Efree_eta2 = self.free.Eeta2(self.window[0])

        Ezeta = FreeMean
        Ezeta2 = (Efree_xi2 + 2 * Ezeta * Efree_xieta) / (1 - Efree_eta2)
        l = len(self.line)
        epta = (Exi2 + 2 * Ezeta * Exieta + Eeta * (Ezeta2 - Ezeta ** 2) + Eeta2 * (Ezeta ** 2)) / l
        s = np.sqrt((epta - (RTP ** 2)) * (l + 1) / (2 * l))
        return s

    # noinspection PyPep8Naming
    def count_volatility2(self, FreeMean, rtp):
        s = 0
        for str_with_count in self.base.simple_num_comb:
            string = str_with_count[0]
            # payment = self.base.get_simple_payment(string)
            payment = str_with_count[2]
            s += str_with_count[1] / self.base.all_combinations2() * payment ** 2

        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                s += (self.base.symbol[scat].payment[cnt] * len(self.line) + self.base.symbol[scat].scatter[
                    cnt] * FreeMean) ** 2 * counts[cnt] / self.base.all_combinations2()
        return np.sqrt(s - rtp ** 2) / len(self.line)

    def count_hitrate2(self):
        hits = 0
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                if self.base.symbol[scat].scatter[cnt] > 0:
                    hits += counts[cnt]
        if hits > 0:
            return self.base.all_combinations2() / hits
        else:
            return 0

    # payment = base_payment + xi + eta * zeta
    # zeta = bonus_payment + xi_free + eta_free * zeta
    def count_volatility_alpha(self, FreeMean, lines, simple_num_comb):
        res = 0
        s2 = 0
        s = 0
        base_simple_num_comb = simple_num_comb[0]
        free_simple_num_comb = simple_num_comb[1]
        for str_with_count in base_simple_num_comb:
            payment = str_with_count[2]
            s2 += str_with_count[1] / self.base.all_combinations2() * payment ** 2
            s += str_with_count[1] / self.base.all_combinations2() * payment
        res += s2 - s ** 2

        xi = 0
        xi2 = 0
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                payment = self.base.symbol[scat].payment[cnt] * len(lines)
                xi += payment / self.base.all_combinations2() * counts[cnt]
                xi2 += payment ** 2 / self.base.all_combinations2() * counts[cnt]
        res += xi2 - xi ** 2

        xi_eta = 0
        eta = 0
        eta2 = 0
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                eta += self.base.symbol[scat].scatter[cnt] * counts[cnt] / self.base.all_combinations2()
                eta2 += self.base.symbol[scat].scatter[cnt] ** 2 * counts[cnt] / self.base.all_combinations2()
                xi_eta += self.base.symbol[scat].payment[cnt] * len(lines) * self.base.symbol[scat].scatter[cnt] \
                          * counts[cnt] / self.base.all_combinations2()
        res += 2 * FreeMean * (xi_eta - xi * eta)

        res -= eta ** 2 * FreeMean ** 2

        eta_free2 = 0
        xi_free2 = 0
        xi_free = 0
        eta_free = 0
        for scatter_comb in self.free.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                payment = self.free.symbol[scat].payment[cnt] * len(lines)
                eta_free2 += self.free.symbol[scat].scatter[cnt] ** 2 * counts[cnt] / self.free.all_combinations2()
                xi_free2 += payment ** 2 / self.free.all_combinations2() * counts[cnt]
                xi_free += payment / self.free.all_combinations2() * counts[cnt]
                eta_free += self.free.symbol[scat].scatter[cnt] * counts[cnt] / self.free.all_combinations2()
        s_free = 0
        s_free2 = 0
        for str_with_count in free_simple_num_comb:
            payment = str_with_count[2]
            s_free2 += str_with_count[1] / self.free.all_combinations2() * payment ** 2
            s_free += str_with_count[1] / self.free.all_combinations2() * payment
        if eta_free >= 1:
            print('More than 1 retrigger free spin per free spin in average')
            return 0
        zeta2 = 1 / (1 - 2 * eta_free + eta_free2) * (s_free2 + 2 * s_free * xi_free + xi_free2)

        res += eta2 * zeta2
        return res ** 0.5 / len(lines)

    def count_parameters(self, base=True, sd_flag=False):
        if base:
            base_rtp = self.count_base_RTP2('base', self.line)
            hitrate = self.count_hitrate2()
            self.parameters = {'base_rtp': base_rtp, 'freemean': -1, 'rtp': -1, 'sdnew': -1, 'hitrate': hitrate}

        elif not sd_flag:
            base_rtp = self.count_base_RTP2('base', self.line)
            freemean = self.freemean2(self.line)
            rtp = self.count_RTP2(freemean, base_rtp)
            hitrate = self.count_hitrate2()
            self.parameters = {'base_rtp': base_rtp, 'freemean': freemean, 'rtp': rtp, 'sdnew': -1, 'hitrate': hitrate}

        else:
            base_rtp = self.count_base_RTP2('base', self.line)
            freemean = self.freemean2(self.line)
            rtp = self.count_RTP2(freemean, base_rtp)
            sdalpha = self.count_volatility_alpha(freemean, self.line,
                                                  [self.base.simple_num_comb, self.free.simple_num_comb])
            hitrate = self.count_hitrate2()

            freemean_first = self.freemean2(self.line[0:1])
            sdalpha_first = self.count_volatility_alpha(freemean_first, self.line[0:1],
                                                        [self.base.simple_num_comb_first,
                                                         self.free.simple_num_comb_first])

            self.parameters = {'base_rtp': base_rtp, 'freemean': freemean, 'rtp': rtp, 'sdold': sdalpha,
                               'hitrate': hitrate, 'sdnew': sdalpha_first}

        return self.parameters

        # return {'base_rtp': base_rtp, 'freemean': freemean, 'rtp': rtp, 'sd': sd, 'sdnew': sdnew, 'sdalpha': sdalpha, 'hitrate': hitrate}

    def standalone_count_parameters(self, shuffle=True):
        self.base.create_simple_num_comb(self.window, self.line)
        self.free.create_simple_num_comb(self.window, self.line)

        if shuffle:
            self.base.reel_generator(self.base.frequency, self.window[0], self.distance, validate=True)
            self.free.reel_generator(self.free.frequency, self.window[0], self.distance, validate=True)
        else:
            self.base.fill_frequency_from_reels(self.base.reels)
            self.free.fill_frequency_from_reels(self.free.reels)

        self.base.create_simple_num_comb(self.window, self.line)
        self.base.fill_scatter_num_comb(self.window)
        self.base.fill_count_killed(self.window[0])
        self.base.fill_simple_num_comb(self.window, self.line)

        self.free.create_simple_num_comb(self.window, self.line)
        self.free.fill_scatter_num_comb(self.window)
        self.free.fill_count_killed(self.window[0])
        self.free.fill_simple_num_comb(self.window, self.line)

        return self.count_parameters(base=False, sd_flag=True)

    def fill_borders(self, out_plot):
        if self.borders is None:
            print('No payment borders for plot')
            return
        if 0 not in self.borders:
            self.borders = [0] + self.borders
        self.base.create_simple_num_comb(self.window, self.line)
        self.base.fill_scatter_num_comb(self.window)
        self.base.fill_count_killed(self.window[0])
        self.base.fill_simple_num_comb(self.window, self.line)

        self.free.create_simple_num_comb(self.window, self.line)
        self.free.fill_scatter_num_comb(self.window)
        self.free.fill_count_killed(self.window[0])
        self.free.fill_simple_num_comb(self.window, self.line)

        freemean = self.freemean2(self.line)
        keys_to_bars = {}
        for border in self.borders:
            keys_to_bars['<' + str(border)] = 0

        total_bet = len(self.line)
        for comb in self.base.simple_num_comb:
            index = 0
            while index < len(self.borders) and comb[2] / total_bet >= self.borders[index]:
                index += 1
            keys_to_bars['<' + str(self.borders[index])] += comb[1]
        for scatter_comb in self.base.scatter_num_comb:
            for scatter_count in range(self.window[0] + 1):
                if self.base.symbol[scatter_comb[0]].scatter[scatter_count] > 0:
                    payment = self.base.symbol[scatter_comb[0]].payment[scatter_count]
                    payment += freemean * self.base.symbol[scatter_comb[0]].scatter[scatter_count]
                    index = 0
                    while index < len(self.borders) and payment >= self.borders[index]:
                        index += 1
                        keys_to_bars['<' + str(self.borders[index])] += scatter_comb[1][scatter_count]
                elif self.base.symbol[scatter_comb[0]].payment[scatter_count] > 0:
                    index = 0
                    payment = self.base.symbol[scatter_comb[0]].payment[scatter_count]
                    while index < len(self.borders) and payment >= self.borders[index]:
                        index += 1
                        keys_to_bars['<' + str(self.borders[index])] += scatter_comb[1][scatter_count]
        all_combinations_cnt = self.base.all_combinations2()
        for key in self.borders:
            keys_to_bars['<' + str(key)] = keys_to_bars['<' + str(key)] / all_combinations_cnt
        if '<0' in keys_to_bars:
            del keys_to_bars['<0']
        plt.bar(range(len(keys_to_bars)), list(keys_to_bars.values()), align='center')
        plt.xticks(range(len(keys_to_bars)), list(keys_to_bars.keys()))
        plt.title('Line wins distribution')
        plt.savefig(out_plot)
        plt.clf()
        return

    def main_process(self, out_log, max_rebalance_count=5, plot_name=None, game_name=None):
        params = {'rtp': self.RTP[0], 'err_rtp': self.RTP[1], 'base_rtp': self.baseRTP[0],
                  'err_base_rtp': self.baseRTP[1],
                  'sdnew': self.volatility[0], 'err_sdnew': self.volatility[1], 'hitrate': self.hitrate[0],
                  'err_hitrate': self.hitrate[1]}

        rebalance_count = 0
        start_time = time.time()
        free_mode = params['hitrate'] > 0

        current_point, self = descent_base(params, self, balance=True)
        if free_mode:
            current_point, self = descent_free(game=self, params=params, start_point=current_point)

        current_point.collect_params(self)
        default_SD = current_point.sdnew
        print('default_SD: ', default_SD)
        min_SD = default_SD * 0.95
        if free_mode:
            max_SD = default_SD * 1.25
        else:
            max_SD = default_SD * 1.90
        if params['sdnew'] < min_SD or params['sdnew'] > max_SD:
            exception_str = 'This SD is not compatible with current RTP, base RTP. Please, select SD between ' + str(
                round(min_SD, 2)) + ' and ' + str(round(max_SD, 2))
            raise Exception(exception_str)

        print('REBALANCE BASE')
        current_point, self = rebalance(current_point, self, self.base, params=params)
        if is_done(current_point, start_time, game_name, self, out_log, plot_name):
            return self
        if free_mode:
            print('REBALANCE FREE')
            # print(current_point.freeFrequency)
            current_point, self = rebalance(current_point, self, self.free, params=params)
        if is_done(current_point, start_time, game_name, self, out_log, plot_name):
            return self

        rebalance_count += 1
        current_value = current_point.get_value()

        while rebalance_count < max_rebalance_count:
            current_point, self = descent_base(params=params, game=self, balance=False, start_point=current_point)
            if free_mode:
                current_point, self = descent_free(game=self, params=params, start_point=current_point, balance=False)

            current_point, self = rebalance(start_point=current_point, game=self, gametype=self.base, params=params)
            if free_mode:
                current_point, self = rebalance(current_point, self, self.free, params=params)
            if is_done(current_point, start_time, game_name, self, out_log, plot_name):
                return self

            prev_value = current_value
            current_value = current_point.get_value()

            if current_value == prev_value:
                current_point.scaling(base=True)
                current_point.scaling(base=False)

            rebalance_count += 1

        if is_done(current_point, start_time, game_name, self, out_log, plot_name):
            return self

        current_point, self = descent_base(params=params, game=self, balance=False, start_point=current_point)

        if free_mode:
            current_point, self = descent_free(game=self, params=params, start_point=current_point, balance=False)

        current_point.collect_params()

        print('Base RTP:', current_point.base_rtp, 'RTP:', current_point.rtp, 'SD:', current_point.sdnew, 'Hitrate: ',
              current_point.hitrate)

        print_res(out_log, current_point, game_name, self)
        create_plot(plot_name, current_point, self)

        spend_time = time.time() - start_time
        hours = int(spend_time / 60 / 60)
        mins = int((spend_time - hours * 3600) / 60)
        sec = int(spend_time - hours * 3600 - mins * 60)

        print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')

        return self
