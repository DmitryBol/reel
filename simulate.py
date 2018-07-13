# coding=utf-8
import json
import FrontEnd.structure_alpha as Q
import random
import numpy as np


# noinspection SpellCheckingInspection,PyShadowingNames
def scatter_payment(obj, gametype, matrix):
    res = 0
    for scat in gametype.scatterlist:
        cnt = 0
        for i in range(obj.window[1]):
            for j in range(obj.window[0]):
                if matrix[i, j] == scat:
                    cnt += 1
        res += gametype.symbol[scat].payment[cnt] * len(obj.line)

        if gametype.symbol[scat].scatter[cnt] > 0:
            for _ in range(gametype.symbol[scat].scatter[cnt]):
                res += make_spin('free')
    return res


def make_spin(type):
    res = 0
    if type == 'base':
        for i in range(obj.window[0]):
            temp = random.randint(0, len(obj.base.reels[i]))
            for j1 in range(obj.window[1]):
                matrix[obj.window[1] - 1 - j1, i] = obj.base.symbol.index(
                    obj.base.reels[i][(temp - j1) % len(obj.base.reels[i])])

        for i in range(obj.window[1]):
            for j1 in range(obj.window[0]):
                if matrix[i, j1] in obj.base.ewildlist:
                    for k in range(obj.window[1]):
                        matrix[k, j1] = matrix[i, j1]

        res += scatter_payment(obj, obj.base, matrix)
        for line in obj.line:
            string = np.array([matrix[line[i] - 1, i] for i in range(obj.window[0])])
            width = obj.window[0]
            line_combination = obj.base.get_combination(string, width)
            for comb in line_combination:
                res += obj.base.symbol[comb[0]].payment[comb[1]]

    if type == 'free':
        for i in range(obj.window[0]):
            temp = random.randint(0, len(obj.free.reels[i]))
            for j1 in range(obj.window[1]):
                matrix[obj.window[1] - 1 - j1, i] = obj.free.symbol.index(
                    obj.free.reels[i][(temp - j1) % len(obj.free.reels[i])])

        for i in range(obj.window[1]):
            for j1 in range(obj.window[0]):
                if matrix[i, j1] in obj.free.ewildlist:
                    for k in range(obj.window[1]):
                        matrix[k, j1] = matrix[i, j1]

        res += scatter_payment(obj, obj.free, matrix)
        for line in obj.line:
            string = np.array([matrix[line[i] - 1, i] for i in range(obj.window[0])])
            width = obj.window[0]
            line_combination = obj.free.get_combination(string, width)
            for comb in line_combination:
                res += obj.free.symbol[comb[0]].payment[comb[1]] * obj.free_multiplier

    return res


file = open('Games\HappyBrauer.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

frequency_1 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_2 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_3 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_4 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_5 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

REPEAT_CNT = 300000

matrix = np.zeros((obj.window[1], obj.window[0]))

obj.base.reel_generator(frequency, obj.window[0], obj.distance)
obj.free.reel_generator(frequency, obj.window[0], obj.distance)
obj.base.fill_frequency(frequency)
obj.free.fill_frequency(frequency)

#все выплаты в тотал бетах
payments_sum = 0
payments_square_sum = 0
for cnt in range(REPEAT_CNT):
    spin_result = make_spin('base')
    payments_sum += spin_result / len(obj.line)
    payments_square_sum += (spin_result / len(obj.line))**2
    if (cnt + 1) % int(REPEAT_CNT/100) == 0:
        print(str(round((cnt + 1) / REPEAT_CNT * 100)) + '%')

rtp = payments_sum / REPEAT_CNT
sd = (1/(REPEAT_CNT - 1) * (payments_square_sum - 1/REPEAT_CNT * payments_sum**2))**0.5
print('simulation rtp = ', rtp)
print('simulation sd = ', sd)
