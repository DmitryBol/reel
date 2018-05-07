import json
import numpy as np
try:
    j = """
    {
    "window": [5, 3],
    "symbol": 
    [
        {
            "name": "7",
            "payment": [[5, 5000], [4, 250], [3, 50], [2, 10]]
        },
        {
            "name": "Melon",
            "payment": [[5, 700], [4, 120], [3, 40]]
        },
        {
            "name": "Cherry",
            "payment": [[5, 150], [4, 30], [3, 10]]
        },
        {
            "name": "Lemon",
            "payment": [[5, 150], [4, 30], [3, 10]]
        },
        {
            "name": "Grape",
            "payment": [[5, 700], [4, 120], [3, 40]]
        },
        {
            "name": "Bell",
            "payment": [[5, 200], [4, 40], [3, 20]]
        },
        {
            "name": "Plum",
            "payment": [[5, 150], [4, 30], [3, 10]]
        },
        {
            "name": "Orange",
            "payment": [[5, 150], [4, 30], [3, 10]]
        },
        {
            "name": "Crown",
            "payment": [[5, 0], [4, 0], [3, 0], [2, 0], [1, 0]],
            "base":
            {
                "position": [2, 3, 4],
                "wild": 
                {
                    "expand": true
                }
            }
        },
        {
            "name": "Dollar",
            "payment": [[5, 100], [4, 20], [3, 5]],
            "base":
            {
                "scatter": 0
            }    
        },
        {
            "name": "Star",
            "payment": [[3, 20]],
            "base":
            {
                "position": [1, 3, 5],
                "scatter": 0
            }
        }
    ],
    "lines":
    [
        [2,2,2,2,2],
        [1,1,1,1,1],
        [3,3,3,3,3],
        [1,2,3,2,1],
        [3,2,1,2,3],
        [1,1,2,3,3],
        [3,3,2,1,1],
        [2,3,3,3,2],
        [2,1,1,1,2],
        [1,2,2,2,1]
    ]
    }"""

    interim = json.loads(j)

    class Mda:
        def __init__(self):
            self = False

    B = Mda()
    print("TYTYTYTYTYTY = ", B)

    class Wild:
        def __init__(self, type, interim, i):
            if ("wild" in interim["symbol"][i]["base"]):
                self.multiplier = interim["symbol"][i][type]["wild"].get("multiplier")
                self.expand = interim["symbol"][i][type]["wild"].get("expand")
                self.substitute = interim["symbol"][i][type]["wild"].get("substitute")
            else:
                self = False

    class Gametype:
        def __init__(self, type, interim, i):
            if (type in interim["symbol"][i]):
                self.direction = interim["symbol"][i][type].get("direction")
                self.position = interim["symbol"][i][type].get("position")
                if (str(interim["symbol"][i][type].get("scatter")) == "0"):
                    self.scatter = [0]*interim["window"][0]
                else:
                    self.scatter = interim["symbol"][i][type].get("scatter")
                self.wild = Wild(type, interim, i)
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
            self.symbol = [None]*len(interim["symbol"])
            for i in range (len(interim["symbol"])):
                self.symbol[i] = Symbol(interim, i)
            self.lines = interim["lines"]
            if ("free_multiplier" in interim):
                self.free_multiplier = interim["free_multiplier"]
            else:
                self.free_multiplier = 1
            if ("distance" in interim):
                self.distance = interim["distance"]
            else:
                self.distance = interim["window"][1]
            self.RTP = interim.get("RTP")
            self.volatility = interim.get("volatility")
            self.hitrate = interim.get("hitrate")
            self.baseRTP = interim.get("baseRTP")
            self.borders = interim.get("borders")
            self.weights = interim.get("weights")

    obj = Game(interim)

    print(obj.window)
    print(obj.symbol[2])
    print(obj.symbol[10].name)
    print(obj.symbol[4].base.scatter)
    print(obj.symbol[10].base.scatter)
    if (obj.symbol[10].base.wild):
        print ("SASASASO")
    print(obj.symbol[10].base.wild)

except json.decoder.JSONDecodeError:
    print("Incorrect json file")

except KeyError:
    print("Json file does not fit the rules")