import numpy as np


class Wild:
    def __init__(self, type, interim, i):
        if "multiplier" in interim["symbol"][i][type]["wild"]:
            self.multiplier = interim["symbol"][i][type]["wild"]["multiplier"]
        else:
            self.multiplier = 1
        self.expand = interim["symbol"][i][type]["wild"].get("expand")



class Gametype:
    def __init__(self, type, interim, i):
        if type in interim["symbol"][i]:
            self.direction = interim["symbol"][i][type].get("direction")
            self.position = interim["symbol"][i][type].get("position")
            if str(interim["symbol"][i][type].get("scatter")) == "0":
                self.scatter = [0] * interim["window"][0]
            else:
                self.scatter = interim["symbol"][i][type].get("scatter")
            if "wild" in interim["symbol"][i][type]:
                self.wild = Wild(type, interim, i)
            else:
                self.wild = False
        else:
            self.direction = "left"
            self.position = np.arange(1, interim["window"][0], 1)
            self.scatter = False
            self.wild = False


class Symbol:
    def __init__(self, interim, i):
        self.name = interim["symbol"][i]["name"]
        self.payment = interim["symbol"][i]["payment"]
        self.base = Gametype("base", interim, i)
        self.free = Gametype("free", interim, i)


class Game:
    def __init__(self, interim):
        self.window = interim["window"]
        self.symbol = [None] * len(interim["symbol"])
        for i in range(len(interim["symbol"])):
            self.symbol[i] = Symbol(interim, i)
        self.lines = interim["lines"]
        if "free_multiplier" in interim:
            self.free_multiplier = interim["free_multiplier"]
        else:
            self.free_multiplier = 1
        if "distance" in interim:
            self.distance = interim["distance"]
        else:
            self.distance = interim["window"][1]
        self.RTP = interim.get("RTP")
        self.volatility = interim.get("volatility")
        self.hitrate = interim.get("hitrate")
        self.baseRTP = interim.get("baseRTP")
        self.borders = interim.get("borders")
        self.weights = interim.get("weights")

        self.set_of_base_wilds = []
        for i in range(len(self.symbol)):
            if self.symbol[i].base.wild:
                self.set_of_base_wilds.append(i)

        for i in self.set_of_base_wilds:
            self.symbol[i].base.wild.substitute = []
            if "substitute" in interim["symbol"][i]["base"]["wild"]:
                for j in range(len(interim["symbol"][i]["base"]["wild"]["substitute"])):
                    for k in range(len(interim["symbol"])):
                        if interim["symbol"][i]["base"]["wild"]["substitute"][j] == interim["symbol"][k]["name"]:
                            self.symbol[i].base.wild.substitute.append(k)
            else:
                for j in range(len(self.symbol)):
                    if not self.symbol[j].base.scatter:
                        self.symbol[i].base.wild.substitute.append(j)

        for i in range(len(self.symbol)):
            self.symbol[i].base.substituted_by = []
            for j in self.set_of_base_wilds:
                if i in self.symbol[j].base.wild.substitute:
                    self.symbol[i].base.substituted_by.append(j)
