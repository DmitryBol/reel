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
                res += make_spin(obj, 'free')
    return res


def make_spin(obj, type):
    matrix = np.zeros((obj.window[1], obj.window[0]))
    res = 0
    if type == 'base':
        for i in range(obj.window[0]):
            temp = random.randint(0, len(obj.base.reels[i]))
            for j1 in range(obj.window[1]):
                matrix[obj.window[1] - 1 - j1, i] = obj.base.reels[i][(temp - j1) % len(obj.base.reels[i])]

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
                matrix[obj.window[1] - 1 - j1, i] = obj.free.reels[i][(temp - j1) % len(obj.free.reels[i])]

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


def make_spins(game, count=100000):
    payments_sum = 0
    payments_square_sum = 0

    for cnt in range(count):
        spin_result = make_spin(game, 'base')
        payments_sum += spin_result / len(game.line)
        payments_square_sum += (spin_result / len(game.line)) ** 2
        if (cnt + 1) % int(count/100) == 0:
            print(str(round((cnt + 1) / count * 100)) + '%')

    _rtp = payments_sum / count
    _sd = (1 / (count - 1) * (payments_square_sum - 1 / count * payments_sum ** 2)) ** 0.5

    return {'rtp': _rtp, 'sd': _sd}


def main_process(FILES):
    frequency_1 = [24, 48, 48, 48, 47, 56, 56, 55, 54, 54, 52, 6]
    frequency_2 = [24, 48, 48, 48, 47, 56, 56, 55, 54, 54, 52, 6]
    frequency_3 = [24, 48, 48, 48, 47, 56, 56, 55, 54, 54, 52, 6]
    frequency_4 = [24, 48, 48, 48, 47, 56, 56, 55, 54, 54, 52, 6]
    frequency_5 = [24, 48, 48, 48, 47, 56, 56, 55, 54, 54, 52, 6]
    # [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]
    frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

    REPEAT_CNT = 100000
    #FILES = ['Games\HappyBrauer.txt']

    for sees in FILES:
        for i in range(1):
            file = open(sees, 'r')
            j = file.read()

            interim = json.loads(j)

            obj = Q.Game(interim)
            obj.deleteline(i)

            obj.base.reel_generator(frequency, obj.window[0], obj.distance)
            obj.free.reel_generator(frequency, obj.window[0], obj.distance)
            obj.base.fill_frequency(frequency)
            obj.free.fill_frequency(frequency)

            simulate_result = make_spins(obj, REPEAT_CNT)
            rtp, sd = simulate_result['rtp'], simulate_result['sd']

            print('FILE: ', sees, 10 - i, 'lines')
            print('simulation rtp = ', rtp)
            print('simulation sd = ', sd)
            file.close()
