import json
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q
import time
import random
import numpy as np


# noinspection SpellCheckingInspection,PyShadowingNames
def scatter_payment(obj, gametype, matrix):
    cnt = 0
    res = 0
    for scat in gametype.scatterlist:
        for i in range(obj.window[1]):
            for j in range(obj.window[0]):
                if matrix[i, j] == scat:
                    cnt += 1
        res += gametype.symbol[scat].payment[cnt] * len(obj.line)
    return res


file = open('HappyBrauer.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

frequency_1 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_2 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_3 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_4 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_5 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

REPEAT_CNT = 100000000

matrix = np.zeros((obj.window[1], obj.window[0]))

total_payment = 0

WILD = 0

bad = True
counter = 0
while bad and counter < 100000:

    obj.base.reel_generator(frequency, obj.window[0])
    obj.free.reel_generator(frequency, obj.window[0])
    obj.base.fill_frequency(frequency)
    obj.free.fill_frequency(frequency)

    #print(frequency)

    bad = False

    for reel in obj.base.reels:
        for symbol_index in range(len(reel)):
            symbol = reel[symbol_index]
            near = []
            for i in range(-obj.window[1] + 1, 0, 1):
                near.append(reel[(symbol_index + i) % len(reel)].name)
            if symbol.name == 'wild' and 'Scat' in near:
                bad = True
    counter += 1
if counter == 100000:
    exit(0)

for cnt in range(REPEAT_CNT):
    for i in range(obj.window[0]):
        temp = random.randint(0, len(obj.base.reels[i]))
        for j in range(obj.window[1]):
            matrix[obj.window[1] - 1 - j, i] = obj.base.symbol.index(obj.base.reels[i][(temp - j) % len(obj.base.reels[i])])

    for i in range(obj.window[1]):
        for j in range(obj.window[0]):
            if matrix[i, j] == WILD:
                for k in range(obj.window[1]):
                    matrix[k, j] = WILD

    if cnt % int(REPEAT_CNT/100) == 0:
        print(matrix, '\n')

    total_payment += scatter_payment(obj, obj.base, matrix)
    for line in obj.line:
        string = np.array([matrix[line[i] - 1, i] for i in range(obj.window[0])])
        width = obj.window[0]
        line_combination = obj.base.get_combination(string, width)
        for comb in line_combination:
            total_payment += obj.base.symbol[comb[0]].payment[comb[1]]

rtp = total_payment / (len(obj.line) * REPEAT_CNT)
print('rtp_simulate = ', rtp)

obj.base.fill_num_comb(obj.window, obj.line)
obj.free.fill_num_comb(obj.window, obj.line)
print('All combinations =', obj.base.all_combinations())
LAL = obj.freemean()
print('Freemean =', LAL)
print('Base RTP =', obj.count_baseRTP())
rtp = obj.count_RTP(LAL)
print('RTP =', rtp)
print('Volatility =', obj.count_volatility(LAL, rtp))
print('Hitrate =', obj.count_hitrate())
