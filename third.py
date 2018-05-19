import numpy as np
import json
rg = __import__("reel generator")
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q


file = open('Front-end/Atilla.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)


def all_combinations(game):
    c = 1
    for i in range(len(game.reels)):
        c = c * len(game.reels[i])
    return c


def freemean(self, game, line):
    s = 0
    v = 0
    for i in range(len(self.free.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self) / all_combinations(game)) \
                * self.free.combination_value(i, comb) * self.free_multiplier
    for i in self.free.scatterlist:
        for comb in range(1, self.window[0] + 1):
            v = v + (rg.count_combinations(game, line, i, comb, self) / all_combinations(game)) * self.free.combination_freespins(i, comb)
    return s * 1.0 / (1 - v)


def RTP(self, game, line):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self) / all_combinations(game)) \
                * (self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * freemean(self, game, line))
    return s


def volatility(self, game, line):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self) / all_combinations(game)) * (
                    self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * freemean(self, game, line)) ** 2
    return np.sqrt(s - RTP(self, game, line) ** 2)


def hitrate(self, game, line):
    s = 0
    for i in self.base.scatterlist:
        for comb in range(len(self.base.symbol[i].scatter)):
            if self.base.symbol[i].scatter[comb] > 0:
                s = s + rg.count_combinations(game, line, i, comb, self)
    return s / all_combinations(game)


def baseRTP(self, game, line):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self) / all_combinations(game)) * self.base.combination_value(i, comb)
    return s


frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

gam = rg.reel_generator(frequency, obj)
lin = 3
print('All combinations =', all_combinations(gam))
print('Freemean =', freemean(obj, gam, lin))
print('RTP =', RTP(obj, gam, lin))
print('Volatility =', volatility(obj, gam, lin))
print('Hitrate =', hitrate(obj, gam, lin))
print('Base RTP =', baseRTP(obj, gam, lin))

