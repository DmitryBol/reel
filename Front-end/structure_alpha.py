import numpy as np
import itertools
import re
import copy
rg = __import__("reel_generator_alpha")


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
        self.name = sought(sought(interim, 'symbol')[i], 'name')
        self.payment = [0] * (w + 1)
        for j in range(len(sought(sought(interim, 'symbol')[i], 'payment'))):
            self.payment[sought(sought(interim, 'symbol')[i], 'payment')[j][0]] = sought(sought(interim, 'symbol')[i], 'payment')[j][1]

        self.substituted_by = []
        self.substituted_by_e = []
        if sought(sought(interim, 'symbol')[i], type):
            if sought(sought(sought(interim, 'symbol')[i], type), 'direction'):
                self.direction = sought(sought(sought(interim, 'symbol')[i], type), 'direction')
            else:
                self.direction = "left"
            if sought(sought(sought(interim, 'symbol')[i], type), 'position'):
                self.position = sought(sought(sought(interim, 'symbol')[i], type), 'position')[:]
                self.position[:] = [x - 1 for x in self.position]
            else:
                self.position = np.arange(0, w, 1)
            if str(sought(sought(sought(interim, 'symbol')[i], type), 'scatter')) == "0" or str(sought(sought(sought(interim, 'symbol')[i], type), 'scatter')) == '[]':
                self.scatter = [0] * (w + 1)
            else:
                if sought(sought(sought(interim, 'symbol')[i], type), 'scatter'):
                    self.scatter = [0] * (w + 1)
                    for j in range(len(sought(sought(sought(interim, 'symbol')[i], type), 'scatter'))):
                        self.scatter[sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][0]] = sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][1]
                else:
                    self.scatter = sought(sought(sought(interim, 'symbol')[i], type), 'scatter')

            if str(sought(sought(sought(interim, 'symbol')[i], type), 'wild')) != 'None':
                self.wild = Wild(interim, type, i)
            else:
                self.wild = False
        else:
            self.direction = "left"
            self.position = np.arange(0, w, 1)
            self.scatter = False
            self.wild = False


class Gametype:
    def __init__(self, interim, type, w):
        if sought(interim, 'symbol'):
            self.symbol = [None] * len(sought(interim, 'symbol'))
            for i in range(len(sought(interim, 'symbol'))):
                if str(sought(sought(interim, 'symbol')[i], type)) != 'None':
                    self.symbol[i] = Symbol(interim, type, i, w)
                else:
                    self.symbol[i] = Symbol(interim, 'base', i, w)
        else:
            raise Exception('Field "symbol" is not found in json file.')

        self.wildlist = []
        self.ewildlist = []
        self.scatterlist = []
        self.num_comb = np.zeros((len(self.symbol), w + 1))
        self.reels = [] * w
        self.frequency = [] * w

        self.scatter_num_comb = []
        self.simple_num_comb = []

    def wildlists(self):
        for i in range(len(self.symbol)):
            if self.symbol[i].wild:
                if self.symbol[i].wild.expand:
                    self.ewildlist.append(i)
                else:
                    self.wildlist.append(i)

    def scatterlists(self):
        for i in range(len(self.symbol)):
            if self.symbol[i].scatter:
                self.scatterlist.append(i)

    def transsubst(self, interim, type, i):
        if str(sought(sought(sought(interim, 'symbol')[i], type), 'wild')) != None:
            if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute'):
                self.symbol[i].wild.substitute.append(i)
                for j in range(len(sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute'))):
                    for k in range(len(sought(interim, 'symbol'))):
                        if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'substitute')[j] == sought(sought(interim, 'symbol')[k], 'name'):
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

    reel_generator = rg.reel_generator
    get_combination = rg.get_simple_combination
    count_combinations2 = rg.count_combinations2
    count_num_comb = rg.count_num_comb
    fill_num_comb = rg.fill_num_comb

    fill_scatter_num_comb = rg.fill_scatter_num_comb
    fill_simple_num_comb = rg.fill_simple_num_comb
    get_simple_payment = rg.get_simple_payment
    get_wilds_in_comb = rg.get_wilds_in_comb

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


class Game:
    def __init__(self, interim):

        if sought(interim, 'window'):
            self.window = sought(interim, 'window')[:]
        else:
            self.window = [5, 3]

        self.base = Gametype(interim, 'base', self.window[0])
        self.free = Gametype(interim, 'free', self.window[0])

        if sought(interim, 'line'):
            self.line = sought(interim, 'line')[:]
        else:
            raise Exception('Field "line" is not found in json file.')

        if sought(interim, 'free_multiplier'):
            self.free_multiplier = sought(interim, 'free_multiplier')
        else:
            self.free_multiplier = 1

        if sought(interim, 'distance'):
            self.distance = sought(interim, 'distance')
        else:
            self.distance = self.window[1]

        self.RTP = sought(interim, 'RTP')
        self.volatility = sought(interim, 'volatility')
        self.hitrate = sought(interim, 'hitrate')
        self.baseRTP = sought(interim, 'baseRTP')
        self.borders = sought(interim, 'border')
        self.weights = sought(interim, 'weight')

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

    def freemean(self):
        s = 0
        v = 0
        for i in range(len(self.free.symbol)):
            for comb in range(1, self.window[0] + 1):
                s += (self.free.num_comb[i, comb]/self.free.all_combinations()) * self.free.combination_value(i, comb) * self.free_multiplier

        for i in self.free.scatterlist:
            for comb in range(1, self.window[0] + 1):
                v += (self.free.num_comb[i, comb]/self.free.all_combinations()) * self.free.combination_freespins(i, comb)
        return s * 1.0 / (1 - v)

    def count_RTP(self, FreeMean):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                if self.base.num_comb[i, comb] > 0 and self.base.symbol[i].payment[comb] > 0:
                    print('printing freq of', i, 'symbol on ',comb, 'combination:', self.base.all_combinations() / self.base.num_comb[i, comb])
                if i not in self.base.scatterlist:
                    s += (self.base.num_comb[i, comb]/self.base.all_combinations()) \
                        * (self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * FreeMean)
                else:
                    s += (self.base.num_comb[i, comb] / self.base.all_combinations()) \
                         * (self.base.combination_value(i, comb) * len(self.line) + self.base.combination_freespins(i, comb) * FreeMean)
        return s

    def count_volatility(self, FreeMean, rtp):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (self.base.num_comb[i, comb]/self.base.all_combinations()) * (
                        self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * FreeMean) ** 2
        return np.sqrt(s - rtp ** 2)

    def count_hitrate(self):
        s = 0
        for i in self.base.scatterlist:
            for comb in range(len(self.base.symbol[i].scatter)):
                if self.base.symbol[i].scatter[comb] > 0:
                    s = s + self.base.num_comb[i, comb]
        return s / self.base.all_combinations()

    def count_baseRTP(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (self.base.num_comb[i, comb] / self.base.all_combinations()) * self.base.combination_value(i, comb)
        return s

    # noinspection PyPep8Naming,SpellCheckingInspection
    def count_base_RTP2(self, game):
        if game == 'base':
            s = 0
            for str_with_count in self.base.simple_num_comb:
                string = str_with_count[0]
                payment = self.base.get_simple_payment(string)
                s += str_with_count[1] / self.base.all_combinations() * payment

            for scatter_comb in self.base.scatter_num_comb:
                scat = scatter_comb[0]
                counts = scatter_comb[1]
                for cnt in range(self.window[0] + 1):
                    s += self.base.symbol[scat].payment[cnt] * len(self.line) * counts[cnt] / self.base.all_combinations()
            return s
        elif game == 'free':
            s = 0
            for str_with_count in self.free.simple_num_comb:
                string = str_with_count[0]
                payment = self.free.get_simple_payment(string)
                s += str_with_count[1] / self.free.all_combinations() * payment

            for scatter_comb in self.free.scatter_num_comb:
                scat = scatter_comb[0]
                counts = scatter_comb[1]
                for cnt in range(self.window[0] + 1):
                    s += self.free.symbol[scat].payment[cnt] * len(self.line) * counts[
                        cnt] / self.free.all_combinations()
            return s

    # noinspection SpellCheckingInspection
    def freemean2(self):
        s = self.count_base_RTP2('free')
        v = 0
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                v += self.free.symbol[scat].scatter[cnt] * counts[cnt] / self.free.all_combinations()

        return self.free_multiplier * s * 1.0 / (1 - v)

    # noinspection PyPep8Naming
    def count_RTP2(self, FreeMean, base_rtp):
        s = 0
        s += base_rtp
        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                s += FreeMean * self.base.symbol[scat].scatter[cnt] * counts[cnt] / self.base.all_combinations()
        return s

    # noinspection PyPep8Naming
    def count_volatility2(self, FreeMean, rtp):
        s = 0
        for str_with_count in self.base.simple_num_comb:
            string = str_with_count[0]
            payment = self.base.get_simple_payment(string)
            s += str_with_count[1] / self.base.all_combinations() * payment**2

        for scatter_comb in self.base.scatter_num_comb:
            scat = scatter_comb[0]
            counts = scatter_comb[1]
            for cnt in range(self.window[0] + 1):
                s += (self.base.symbol[scat].payment[cnt]*len(self.line)+self.base.symbol[scat].scatter[cnt]*FreeMean)**2 \
                     * counts[cnt] / self.base.all_combinations()
        return np.sqrt(s - rtp ** 2)

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
