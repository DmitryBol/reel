import numpy as np
import itertools


def transsubst (i, substitute, type, interim, everyone):
    if "substitute" in interim["symbol"][i][type]["wild"]:
        substitute.append(i)
        for j in range(len(interim["symbol"][i][type]["wild"]["substitute"])):
            for k in range(len(interim["symbol"])):
                if interim["symbol"][i][type]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
                    substitute.append(k)
    else:
        if type == "base":
            for j in range(len(everyone)):
                if not everyone[j].base.scatter:
                    substitute.append(j)
        if type == "free":
            for j in range(len(everyone)):
                if not everyone[j].free.scatter:
                    substitute.append(j)


class Wild:
    def __init__(self, type, interim, i):
        self.multiplier = 1
        if "multiplier" in interim["symbol"][i][type]["wild"]:
            self.multiplier = interim["symbol"][i][type]["wild"]["multiplier"]
        self.expand = interim["symbol"][i][type]["wild"].get("expand")
        self.substitute = []


class Gametype:
    def __init__(self, type, interim, i, w):
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
                self.wild = Wild(type, interim, i)
            else:
                self.wild = False
        else:
            self.direction = "left"
            self.position = np.arange(0, w, 1)
            self.scatter = False
            self.wild = False


class Symbol:
    def __init__(self, interim, i, w):
        self.name = interim["symbol"][i]["name"]
        self.payment = [0]*(w+1)
        for j in range(len(interim["symbol"][i]["payment"])):
            self.payment[interim["symbol"][i]["payment"][j][0]] = interim["symbol"][i]["payment"][j][1]
        self.base = Gametype("base", interim, i, w)
        if "free" in interim["symbol"][i]:
            self.free = Gametype("free", interim, i, w)
        else:
            self.free = Gametype("base", interim, i, w)


class Game:
    def __init__(self, interim):
        if "window" in interim:
            self.window = interim["window"]
        else:
            self.window = [5, 3]
        self.symbol = [None] * len(interim["symbol"])
        for i in range(len(interim["symbol"])):
            self.symbol[i] = Symbol(interim, i, self.window[0])
        self.line = []
        for i in range(len(interim["lines"])):
            self.line.append(interim["lines"][i])
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

        # массив индексов скаттеров в базовой игре
        self.base_scatterlist = []
        # заполнение этого массива
        for i in range(len(self.symbol)):
            if self.symbol[i].base.scatter:
                self.base_scatterlist.append(i)

        # массив индексов скаттеров в бесплатной игре
        self.free_scatterlist = []
        # заполнение этого массива
        for i in range(len(self.symbol)):
            if self.symbol[i].free.scatter:
                self.free_scatterlist.append(i)

        # массив индексов неэкспандящихся вайлдов в базовой игре
        self.base_wildlist = []
        # массив индексов экспандящихся вайлдов в базовой игре
        self.base_ewildlist = []
        # заполнение этих массивов
        for i in range(len(self.symbol)):
            if self.symbol[i].base.wild:
                if self.symbol[i].base.wild.expand:
                    self.base_ewildlist.append(i)
                else:
                    self.base_wildlist.append(i)

        # заполнение массива substitute для каждого вайлда из базовой игры
        for i in itertools.chain(self.base_wildlist, self.base_ewildlist):
            transsubst(i, self.symbol[i].base.wild.substitute, "base", interim, self.symbol)

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            for j in self.base_wildlist:
                if i in self.symbol[j].base.wild.substitute and i != j:
                    self.symbol[i].base.substituted_by.append(j)

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            for j in self.base_ewildlist:
                if i in self.symbol[j].base.wild.substitute and i != j:
                    self.symbol[i].base.substituted_by_e.append(j)

        # массив индексов неэкспандящихся вайлдов в бесплатной игре
        self.free_wildlist = []
        # массив индексов экспандящихся вайлдов в бесплатной игре
        self.free_ewildlist = []
        # заполнение этих массивов
        for i in range(len(self.symbol)):
            if self.symbol[i].free.wild:
                if self.symbol[i].free.wild.expand:
                    self.free_ewildlist.append(i)
                else:
                    self.free_wildlist.append(i)

        # заполнение массива substitute для каждого вайлда из бесплатной игры
        for i in itertools.chain(self.free_wildlist, self.free_ewildlist):
            if "free" in interim["symbol"][i]:
                transsubst(i, self.symbol[i].free.wild.substitute, "free", interim, self.symbol)
            else:
                self.symbol[i].free.wild.substitute = self.symbol[i].base.wild.substitute

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].free.substituted_by = []
            for j in self.free_wildlist:
                if i in self.symbol[j].free.wild.substitute and i != j:
                    self.symbol[i].free.substituted_by.append(j)

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].free.substituted_by_e = []
            for j in self.free_ewildlist:
                if i in self.symbol[j].free.wild.substitute and i != j:
                    self.symbol[i].free.substituted_by_e.append(j)

        self.base_scatterlist = []
        self.free_scatterlist = []

        for i in range(len(self.symbol)):
            if self.symbol[i].base.scatter:
                self.base_scatterlist.append(i)

        for i in range(len(self.symbol)):
            if self.symbol[i].free.scatter:
                self.free_scatterlist.append(i)

    def all_combinations(self, game):
        c = 1
        for i in range(len(game.reels)):
            c = c * len(game.reels[i])
        return c

    def freemean(self, game, line):
        s = 0
        v = 0
        for i in range(len(self.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, i, comb, self) / self.all_combinations(game)) \
                    * self.symbol[i].payment[comb] * self.free_multiplier
        for i in self.free_scatterlist:
            for comb in range(1, self.window[0] + 1):
                v = v + (rg.count_combination(game, line, i, comb, self) / self.all_combinations(game)) * self.symbol[i].free.scatter[comb]
        return s * 1.0 / (1 - v)

    def RTP(self, game, line):
        s = 0
        for i in range(len(self.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, i, comb, self) / self.all_combinations(game)) \
                    * (self.symbol[i].payment[comb] + self.symbol[i].base.scatter[comb] * self.freemean(game, line))
        return s

    def volatility(self, game, line):
        s = 0
        for i in range(len(self.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, i, comb, self) / self.all_combinations(game)) * (
                        self.symbol[i].payment[comb] + self.symbol[i].base.scatter[comb] * self.freemean(game, line))**2
        return np.sqrt(s - self.RTP()**2)

    def hitrate(self, game, line):
        s = 0
        for i in self.base_scatterlist:
            for comb in range(len(self.symbol[i].base.scatter)):
                if self.symbol[i].base.scatter[comb] > 0:
                    s = s + rg.count_combination(game, line, i, comb, self)
        return s / self.all_combinations(game)

    def baseRTP(self, game, line):
        s = 0
        for i in range(len(self.symbol)):
            for comb in range(1, self.window[0] + 1):
                s = s + (rg.count_combination(game, line, i, comb, self) / self.all_combinations(game)) * self.symbol[i].payment[comb]
        return s
