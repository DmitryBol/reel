# coding=utf-8
import json
import FrontEnd.structure_alpha as Q
import random
import numpy as np
import copy


# noinspection SpellCheckingInspection,PyShadowingNames
def scatter_payment(obj, gametype, matrix):
    res = 0
    base_res = 0
    for scat in gametype.scatterlist:
        cnt = 0
        for i in range(obj.window[1]):
            for j in range(obj.window[0]):
                if matrix[i, j] == scat:
                    cnt += 1
        res += gametype.symbol[scat].payment[cnt] * len(obj.line)
        base_res += gametype.symbol[scat].payment[cnt] * len(obj.line)

        if gametype.symbol[scat].scatter[cnt] > 0:
            for _ in range(gametype.symbol[scat].scatter[cnt]):
                res += make_spin(obj, 'free')[0]
    return [res, base_res]


def take_win(game, gametype, matrix):
    scat_payment = scatter_payment(game, gametype, matrix)
    res = scat_payment[0]
    base_res = scat_payment[1]
    bonus_count = 0
    if res > base_res and gametype.name == 'base':
        bonus_count += 1

    for i in range(gametype.window[1]):
        for j1 in range(gametype.window[0]):
            if matrix[i, j1] in gametype.ewildlist:
                for k in range(gametype.window[1]):
                    matrix[k, j1] = matrix[i, j1]

    for line in game.line:
        string = np.array([matrix[line[i] - 1, i] for i in range(game.window[0])])
        width = game.window[0]
        line_combination = gametype.get_combination(string, width)
        for comb in line_combination:
            wilds = []
            mult = 1
            for index in range(comb[1]):
                if comb[2] == 'left':
                    if string[index] in gametype.wildlist or string[index] in gametype.ewildlist:
                        wilds.append(string[index])
                if comb[2] == 'right':
                    if string[gametype.window[0] - index - 1] in gametype.wildlist or string[gametype.window[0] - index - 1] in gametype.ewildlist:
                        wilds.append(string[gametype.window[0] - index - 1])
            for wild_id in set(wilds):
                wild_id = int(wild_id)
                mult *= gametype.symbol[wild_id].wild.multiplier
            res += gametype.symbol[comb[0]].payment[comb[1]] * mult
            if gametype.name == 'base':
                base_res += gametype.symbol[comb[0]].payment[comb[1]] * mult
    return [res, base_res, bonus_count]


def make_spin(obj, type):
    matrix = np.zeros((obj.window[1], obj.window[0]))
    res = 0
    base_res = 0
    bonus_count = 0
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

        win = take_win(game=obj, gametype=obj.base, matrix=matrix)
        res += win[0]
        base_res += win[1]
        bonus_count += win[2]

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

        res += take_win(game=obj, gametype=obj.free, matrix=matrix)[0]

    return [res, base_res, bonus_count]


def make_spins(game, count=100000):
    payments_sum = 0
    payments_square_sum = 0
    count_with_win = 0
    base_payments_sum = 0
    bonus_count = 0

    for cnt in range(count):
        spin_result = make_spin(game, 'base')
        if spin_result[0] > 0:
            count_with_win += 1
        payments_sum += spin_result[0] / len(game.line)
        base_payments_sum += spin_result[1] / len(game.line)
        payments_square_sum += (spin_result[0] / len(game.line)) ** 2
        bonus_count += spin_result[2]
        if (cnt + 1) % int(count/100) == 0:
            print(str(round((cnt + 1) / count * 100)) + '%')

    _rtp = payments_sum / count
    _sd = (1 / (count - 1) * (payments_square_sum - 1 / count * payments_sum ** 2)) ** 0.5
    _base_rtp = base_payments_sum / count
    _hitrate = -1
    if bonus_count > 0:
        _hitrate = count / bonus_count

    return {'rtp': _rtp, 'sd': _sd, 'wins': count_with_win / count, 'base_rtp': _base_rtp, 'hitrate': _hitrate}


def make_spins_ui(ui, game, count=100000):
    payments_sum = 0
    payments_square_sum = 0
    count_with_win = 0

    for cnt in range(count):
        spin_result = make_spin(game, 'base')
        if spin_result > 0:
            count_with_win += 1
        payments_sum += spin_result / len(game.line)
        payments_square_sum += (spin_result / len(game.line)) ** 2
        if (cnt + 1) % int(count/100) == 0:
            ui.progressbar.setValue(round((cnt + 1) / count * 100))

    _rtp = payments_sum / count
    _sd = (1 / (count - 1) * (payments_square_sum - 1 / count * payments_sum ** 2)) ** 0.5

    return {'rtp': _rtp, 'sd': _sd, 'wins': count_with_win / count}


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


def fillMatrix(gametype, matrix, reels, indexes, height):
    if len(indexes) != len(reels):
        raise Exception('reels have wrong dimension')
    for row_id in range(height):
        for reel_id in range(len(reels)):
            matrix[row_id, reel_id] = reels[reel_id][(indexes[reel_id] + row_id) % len(reels[reel_id])]


def greedy_simulate(game, gametype, reels):
    print('\n\nstarted greedy simulation')
    for reel in reels:
        if len(reel) > 70:
            raise Exception('Too much symbols for greedy simulation')

    if gametype.window[0] != len(reels):
        raise Exception('reels have wrong dimension')

    total_cnt = 1
    for reel in reels:
        total_cnt = total_cnt * len(reel)

    total_sum = 0
    counter = 0
    matrix = np.zeros((3, 5))
    lens = [len(reels[i]) for i in range(len(reels))]
    for index0 in range(lens[0]):
        for index1 in range(lens[1]):
            for index2 in range(lens[2]):
                for index3 in range(lens[3]):
                    for index4 in range(lens[4]):
                        indexes = [index0, index1, index2, index3, index4]
                        fillMatrix(gametype, matrix, reels, indexes, 3)
                        win = take_win(game, gametype, matrix)
                        total_sum += win
                        counter += 1
                print('{0}% done, current rtp: {1}%'.format(str(round(counter / total_cnt * 100, 4)),
                                                            str(round(total_sum / counter / len(game.line) * 100, 2))))

    return {'rtp': total_sum / counter / len(game.line), 'cnt': counter}
