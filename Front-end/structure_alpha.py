import numpy as np
import itertools
import re


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
        if sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'multiplier'):
            self.multiplier = sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'multiplier')
        self.expand = sought(sought(sought(sought(interim, 'symbol')[i], type), 'wild'), 'expand')
        self.substitute = []


class Symbol:
    def __init__(self, interim, type, i, w):
        self.name = sought(sought(interim, 'symbol')[i], 'name')
        self.payment = [0]*(w+1)
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
            if str(sought(sought(sought(interim, 'symbol')[i], type), 'scatter')) == "0":
                self.scatter = [0] * (w + 1)
            else:
                if sought(sought(sought(interim, 'symbol')[i], type), 'scatter'):
                    self.scatter = [0] * (w + 1)
                    for j in range(len(sought(sought(sought(interim, 'symbol')[i], type), 'scatter'))):
                        self.scatter[sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][0]] = sought(sought(sought(interim, 'symbol')[i], type), 'scatter')[j][1]
                else:
                    self.scatter = sought(sought(sought(interim, 'symbol')[i], type), 'scatter')

            if sought(sought(sought(interim, 'symbol')[i], type), 'wild'):
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
                if sought(sought(interim, 'symbol')[i], type):
                    self.symbol[i] = Symbol(interim, type, i, w)
                else:
                    self.symbol[i] = Symbol(interim, 'base', i, w)
        else:
            raise Exception('Field "symbol" is not found in json file.')

        self.wildlist = []
        self.ewildlist = []
        self.scatterlist = []

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
                s = s + count_combination(game, line, self.free.symbol[i], comb, names) * self.free.combination_value(i, comb) * self.free_multiplier
        for i in self.free.scatterlist:
            for comb in range(1, self.window[0] + 1):
                v = v + count_combination(game, line, self.base.symbol[i], comb, names) * self.free.combination_freespins(i, comb)
        return s * 1.0 / (1 - v)

    def RTP(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + count_combination(game, line, self.base.symbol[i], comb, names) * (self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * freemean())
        return s

    def volatility(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + count_combination(game, line, self.base.symbol[i], comb, names) * (
                            self.base.combination_value(i, comb) + self.base.combination_freespins(i,
                                                                                                   comb) * freemean())**2
        return np.sqrt(s - self.RTP()**2)

    def baseRTP(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + count_combination(game, line, self.base.symbol[i], comb, names) * self.base.combination_value(i, comb)
        return s
