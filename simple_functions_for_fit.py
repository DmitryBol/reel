import json
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q
import time
import math


class Out_result:
    def __init__(self, scatterlist):
        self.scatter_index_with_frequency = {scat: 1 for scat in scatterlist}
        self.total_length = 3*len(scatterlist)
        self.total_scats = len(scatterlist)


def simple_iteration(base_game, window, res, temp_HR, HR):
    if temp_HR < HR:
        res.total_length += 1
        index = 0
        while index in base_game.scatterlist:
            index += 1
        for i in range(window[0]):
            base_game.frequency[i][index] += 1
        base_game.fill_scatter_num_comb(window)
    else:
        for scat in base_game.scatterlist:
            res.scatter_index_with_frequency[scat] += 1
        s = 0
        for key in res.scatter_index_with_frequency:
            s += res.scatter_index_with_frequency[key]
        res.total_scats = s
        res.total_length = 5*s
        reel = [0] * len(base_game.symbol)
        for scat in base_game.scatterlist:
            reel[scat] = res.scatter_index_with_frequency[scat]
        index = 0
        while index in base_game.scatterlist:
            index += 1
        reel[index] = res.total_length - res.total_scats
        frequency = [reel for i in range(window[0])]
        base_game.fill_frequency(frequency)
        base_game.fill_scatter_num_comb(window)


def get_scatter_frequency(gameFileName, HR, ERROR):
    file = open(gameFileName, 'r')
    j = file.read()
    interim = json.loads(j)
    game = Q.Game(interim)
    file.close()

    res = Out_result(game.base.scatterlist)

    reel = [0]*len(game.base.symbol)
    for scat in game.base.scatterlist:
        reel[scat] = res.scatter_index_with_frequency[scat]
    index = 0
    while index in game.base.scatterlist:
        index += 1
    reel[index] = res.total_length - res.total_scats
    frequency = [reel for i in range(game.window[0])]
    game.base.fill_frequency(frequency)
    game.base.fill_scatter_num_comb(game.window)

    temp_HR = game.count_hitrate2()

    while math.fabs(temp_HR - HR) > ERROR:
        if temp_HR < HR:
            index = 0
            while index in game.base.scatterlist:
                index += 1
            for i in range(game.window[0]):
                frequency[i][index] += 1
            game.base.fill_frequency(frequency)
            game.base.fill_scatter_num_comb(game.window)
            res.total_length = sum(game.base.frequency[0])
        else:
            for scat in game.base.scatterlist:
                res.scatter_index_with_frequency[scat] += 1
            s = 0
            for key in res.scatter_index_with_frequency:
                s += res.scatter_index_with_frequency[key]
            res.total_scats = s
            res.total_length = 3 * s
            reel = [0] * len(game.base.symbol)
            for scat in game.base.scatterlist:
                reel[scat] = res.scatter_index_with_frequency[scat]
            index = 0
            while index in game.base.scatterlist:
                index += 1
            reel[index] = res.total_length - res.total_scats
            frequency = [reel for i in range(game.window[0])]
            game.base.fill_frequency(frequency)
            game.base.fill_scatter_num_comb(game.window)
        temp_HR = game.count_hitrate2()

    return res


# get_scatter_frequency получает на вход:
# 1) Название файла с конфигурацией игры
# 2) необходимый HitRate
# 3) Максимальную погрешность вычисления HitRate'a
# На выходе отдает структуру с полями:
# total_length - суммарная длина каждой линии
# scatter_index_with_frequency - набор пар (индекс скатера, его количество на ленте)
# получение частот по ключу "индекс скатера"
# Пример кода ниже

out = get_scatter_frequency('HappyBrauer.txt', 160, 0.5)
print(out.total_length)
print(out.scatter_index_with_frequency)
print(out.scatter_index_with_frequency[12]) #количество скатеров с индексом 12 на одной ленте