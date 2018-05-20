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


def freemean(self, game, line, frequency):
    s = 0
    v = 0
    for i in range(len(self.free.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self, frequency) / all_combinations(game)) \
                * self.free.combination_value(i, comb) * self.free_multiplier
    for i in self.free.scatterlist:
        for comb in range(1, self.window[0] + 1):
            v = v + (rg.count_combinations(game, line, i, comb, self, frequency) / all_combinations(game)) * self.free.combination_freespins(i, comb)
    return s * 1.0 / (1 - v)


def RTP(self, game, line, frequency,FreeMean):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self, frequency) / all_combinations(game)) \
                * (self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * FreeMean)
    return s


def volatility(self, game, line, frequency, FreeMean, rtp):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self, frequency) / all_combinations(game)) * (
                    self.base.combination_value(i, comb) + self.base.combination_freespins(i, comb) * FreeMean) ** 2
    return np.sqrt(s - rtp ** 2)


def hitrate(self, game, line, frequency):
    s = 0
    for i in self.base.scatterlist:
        for comb in range(len(self.base.symbol[i].scatter)):
            if self.base.symbol[i].scatter[comb] > 0:
                s = s + rg.count_combinations(game, line, i, comb, self, frequency)
    return s / all_combinations(game)


def baseRTP(self, game, line, frequency):
    s = 0
    for i in range(len(self.base.symbol)):
        for comb in range(1, self.window[0] + 1):
            s = s + (rg.count_combinations(game, line, i, comb, self, frequency) / all_combinations(game)) * self.base.combination_value(i, comb)
    return s


frequency_1 = [20, 18, 17, 11, 12, 12, 13, 9, 16, 13, 22, 4, 3]
frequency_2 = [17, 15, 19, 10, 13, 12, 10, 7, 11, 17, 23, 4, 5]
frequency_3 = [11, 18, 19, 14, 11, 10, 6, 9, 15, 18, 20, 5, 5]
frequency_4 = [17, 16, 18, 11, 10, 9, 13, 6, 15, 23, 18, 4, 4]
frequency_5 = [19, 10, 15, 9, 7, 9, 14, 14, 15, 19, 18, 6, 6]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

gam = rg.reel_generator(frequency, obj)
lin = 3
print('All combinations =', all_combinations(gam))
LAL = freemean(obj, gam, lin, frequency)
print('Freemean =', LAL)
rtp = RTP(obj, gam, lin, frequency, LAL)
print('RTP =', rtp)
print('Volatility =', volatility(obj, gam, lin, frequency, LAL, rtp))
print('Hitrate =', hitrate(obj, gam, lin, frequency))
print('Base RTP =', baseRTP(obj, gam, lin, frequency))

