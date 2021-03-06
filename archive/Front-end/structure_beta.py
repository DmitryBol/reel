import numpy as np
import itertools
import re
import sys
sys.path.insert(0, '/')
rg = __import__("reel generator")

def sought(dictionary, string):
    K = list(dictionary.keys())[:]
    for i in range(len(K)):
        prob = re.compile(K[i], re.IGNORECASE)
        if prob.search(string):
            return dictionary[K[i]]
    return None


class Wild:
    def __init__(self, interim, type, i):
        self.multiplier = 1
        if "multiplier" in interim["symbol"][i][type]["wild"]:
            self.multiplier = interim["symbol"][i][type]["wild"]["multiplier"]
        self.expand = interim["symbol"][i][type]["wild"].get("expand")
        self.substitute = []


class Symbol:
    def __init__(self, interim, type, i, w):
        self.name = interim["symbol"][i]["name"]
        self.payment = [0]*(w+1)
        for j in range(len(interim["symbol"][i]["payment"])):
            self.payment[interim["symbol"][i]["payment"][j][0]] = interim["symbol"][i]["payment"][j][1]

        self.substituted_by = []
        self.substituted_by_e = []
        if type in interim["symbol"][i]:
            if "direction" in interim["symbol"][i][type]:
                self.direction = interim["symbol"][i][type]["direction"]
            else:
                self.direction = "left"
            if "position" in interim["symbol"][i][type]:
                self.position = interim["symbol"][i][type]["position"][:]
                self.position[:] = [x - 1 for x in self.position]
            else:
                self.position = np.arange(0, w, 1)
            if str(interim["symbol"][i][type].get("scatter")) == "0":
                self.scatter = [0] * (w + 1)
            else:
                if interim["symbol"][i][type].get("scatter"):
                    self.scatter = [0] * (w + 1)
                    for j in range(len(interim["symbol"][i][type]["scatter"])):
                        self.scatter[interim["symbol"][i][type]["scatter"][j][0]] = interim["symbol"][i][type]["scatter"][j][1]
                else:
                    self.scatter = interim["symbol"][i][type].get("scatter")

            if "wild" in interim["symbol"][i][type]:
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
        self.symbol = [None] * len(interim["symbol"])
        for i in range(len(interim["symbol"])):
            if type in interim["symbol"][i]:
                self.symbol[i] = Symbol(interim, type, i, w)
            else:
                self.symbol[i] = Symbol(interim, 'base', i, w)
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
        if "substitute" in interim["symbol"][i][type]["wild"]:
            self.symbol[i].wild.substitute.append(i)
            for j in range(len(interim["symbol"][i][type]["wild"]["substitute"])):
                for k in range(len(interim["symbol"])):
                    if interim["symbol"][i][type]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
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

        if "window" in interim:
            self.window = interim["window"][:]
        else:
            self.window = [5, 3]

        self.base = Gametype(interim, 'base', self.window[0])
        self.free = Gametype(interim, 'free', self.window[0])

        self.line = interim["lines"][:]

        if "free_multiplier" in interim:
            self.free_multiplier = interim["free_multiplier"]
        else:
            self.free_multiplier = 1

        if "distance" in interim:
            self.distance = interim["distance"]
        else:
            self.distance = self.window[1]

        self.RTP = interim.get("RTP")
        self.volatility = interim.get("volatility")
        self.hitrate = interim.get("hitrate")
        self.baseRTP = interim.get("baseRTP")
        self.borders = interim.get("borders")
        self.weights = interim.get("weights")

        self.base.wildlists()
        self.base.scatterlists()

        self.free.wildlists()
        self.free.scatterlists()

        # заполнение массива substitute для каждого вайлда из обычной игры
        for i in itertools.chain(self.base.wildlist, self.base.ewildlist):
            self.base.transsubst(interim, 'base', i)

        # заполнение массива substitute для каждого вайлда из бесплатной игры
        for i in itertools.chain(self.free.wildlist, self.free.ewildlist):
            if "free" in interim["symbol"][i]:
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

    def all_combinations(self, reel):
        c = 1
        for i in range(len(reel)):
            c = c * len(reel[i])
        return c

    def freemean(self):
        s = 0
        v = 0
        for i in range(len(self.free.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, self.free.symbol[i], comb, names) / self.all_combinations(reel)) \
                    * self.free.combination_value(i, comb) * self.free_multiplier
        for i in self.free.scatterlist:
            for comb in range(1, self.window[0] + 1):
                v = v + (rg.count_combination(game, line, self.free.symbol[i], comb, names) / self.all_combinations(reel)) * self.free.combination_freespins(i, comb)
        return s * 1.0 / (1 - v)

    def RTP(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, self.free.symbol[i], comb, names) / self.all_combinations(reel)) \
                    * (self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * freemean())
        return s

    def volatility(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, self.free.symbol[i], comb, names) / self.all_combinations(reel)) * (
                            self.base.combination_value(i, comb) + self.base.combination_freespins(i,
                                                                                                   comb) * freemean())**2
        return np.sqrt(s - self.RTP()**2)

    def hitrate(self):
        s = 0
        for i in self.base.scatterlist:
            for comb in range(len(self.base.symbol[i].scatter)):
                if self.base.symbol[i].scatter[comb] > 0:
                    s = s + rg.count_combination(game, line, self.free.symbol[i], comb, names)
        return s / self.all_combinations(reel)

    def baseRTP(self):
        s = 0
        for i in range(len(self.base.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, self.free.symbol[i], comb, names) / self.all_combinations(reel)) * self.base.combination_value(i, comb)
        return s

