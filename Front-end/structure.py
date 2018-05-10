import numpy as np
import itertools

def transsubst (i, arr, type, interim, vav):
    if "substitute" in interim["symbol"][i][type]["wild"]:
        for j in range(len(interim["symbol"][i][type]["wild"]["substitute"])):
            for k in range(len(interim["symbol"])):
                if interim["symbol"][i][type]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
                    arr.append(k)
    else:
        for j in range(len(vav)):
            if not vav[j].base.scatter:
                arr.append(j)


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
            if "derection" in interim["symbol"][i][type]:
                self.direction = interim["symbol"][i][type]["direction"]
            else:
                self.direction = "left"
            if "position" in interim["symbol"][i][type]:
                self.position = interim["symbol"][i][type]["position"]
            else:
                self.position = np.arange(1, w + 1, 1)
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
            self.position = np.arange(1, w + 1, 1)
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
        self.lines = []
        for i in range(len(interim["lines"])):
            self.lines.append(interim["lines"][i])
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

        # массив индексов неэкспандящихся вайлдов в базовой игре
        self.set_of_base_wilds = []
        # массив индексов экспандящихся вайлдов в базовой игре
        self.set_of_base_ewilds = []
        # заполнение этих массивов
        for i in range(len(self.symbol)):
            if self.symbol[i].base.wild:
                if self.symbol[i].base.wild.expand:
                    self.set_of_base_ewilds.append(i)
                else:
                    self.set_of_base_wilds.append(i)

        # заполнение массива substitute для каждого вайлда из базовой игры
        for i in itertools.chain(self.set_of_base_wilds, self.set_of_base_ewilds):
            transsubst(i, self.symbol[i].base.wild.substitute, "base", interim, self.symbol)

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].base.substituted_by = []
            for j in self.set_of_base_wilds:
                if i in self.symbol[j].base.wild.substitute:
                    self.symbol[i].base.substituted_by.append(j)

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].base.substituted_by_e = []
            for j in self.set_of_base_ewilds:
                if i in self.symbol[j].base.wild.substitute:
                    self.symbol[i].base.substituted_by_e.append(j)

        # массив индексов неэкспандящихся вайлдов в бесплатной игре
        self.set_of_free_wilds = []
        # массив индексов экспандящихся вайлдов в бесплатной игре
        self.set_of_free_ewilds = []
        # заполнение этих массивов
        for i in range(len(self.symbol)):
            if self.symbol[i].free.wild:
                if self.symbol[i].free.wild.expand:
                    self.set_of_free_ewilds.append(i)
                else:
                    self.set_of_free_wilds.append(i)

        # заполнение массива substitute для каждого вайлда из бесплатной игры
        for i in itertools.chain(self.set_of_free_wilds, self.set_of_free_ewilds):
            if "free" in interim["symbol"][i]:
                transsubst(i, self.symbol[i].free.wild.substitute, "free", interim, self.symbol)
            else:
                self.symbol[i].free.wild.substitute = self.symbol[i].base.wild.substitute

        # для каждого символа создание и заполнение массива индексов неэкспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].free.substituted_by = []
            for j in self.set_of_free_wilds:
                if i in self.symbol[j].free.wild.substitute:
                    self.symbol[i].free.substituted_by.append(j)

        # для каждого символа создание и заполнение массива индексов экспандящихся вайлдов, заменяющих данный символ
        for i in range(len(self.symbol)):
            # self.symbol[i].free.substituted_by_e = []
            for j in self.set_of_free_ewilds:
                if i in self.symbol[j].free.wild.substitute:
                    self.symbol[i].free.substituted_by_e.append(j)
