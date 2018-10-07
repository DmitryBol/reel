# coding=utf-8
import json
import FrontEnd.structure_alpha as Q
import math
import copy


class OutResult:
    def __init__(self, scatterlist):
        self.scatter_index_with_frequency = {scat: 1 for scat in scatterlist}
        self.total_length = 3*len(scatterlist)
        self.total_scats = len(scatterlist)

    def add_symbols(self, symbols):
        self.total_length = 7 * len(symbols)


def notice_positions(frequency, gametype):
    if frequency is None:
        return None
    window_width = len(frequency)
    n_symbols = len(gametype.symbol)
    res = copy.deepcopy(frequency)
    for reel_id in range(window_width):
        for symbol_id in range(n_symbols):
            if reel_id in gametype.symbol[symbol_id].position:
                continue
            else:
                res[reel_id][symbol_id] = 0
    return res


def get_scatter_frequency(game, hitrate, hitrate_error):

    exit_flag = True
    for scat in game.base.scatterlist:
        for cnt in range(game.window[0] + 1):
            if game.base.symbol[scat].scatter[cnt] > 0:
                exit_flag = False
    if exit_flag:
        return -1

    res = OutResult(game.base.scatterlist)

    if hitrate == -1:
        for scatter_id in game.base.scatterlist:
            if max(game.base.symbol[scatter_id].scatter) > 0:
                res[scatter_id] = 0
        return res

    reel = [0]*len(game.base.symbol)
    for scat in game.base.scatterlist:
        reel[scat] = res.scatter_index_with_frequency[scat]
    index = 0
    while index in game.base.scatterlist:
        index += 1
    reel[index] = res.total_length - res.total_scats
    frequency = [reel for _ in range(game.window[0])]
    frequency = notice_positions(frequency, game.base)
    game.base.fill_frequency(frequency)
    game.base.fill_scatter_num_comb(game.window)

    temp_HR = game.count_hitrate2()

    while math.fabs(temp_HR - hitrate) > hitrate_error:
        if temp_HR < hitrate:
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
                if max(game.base.symbol[scat].scatter) > 0:
                    res.scatter_index_with_frequency[scat] += 1
            s = 0
            for key in res.scatter_index_with_frequency:
                s += res.scatter_index_with_frequency[key]
            res.total_scats = s
            res.total_length = 3 * s
            reel = [0] * len(game.base.symbol)
            for scat in game.base.scatterlist:
                if max(game.base.symbol[scat].scatter) > 0:
                    reel[scat] = res.scatter_index_with_frequency[scat]
            index = 0
            while index in game.base.scatterlist:
                index += 1
            reel[index] = res.total_length - res.total_scats
            frequency = [reel for _ in range(game.window[0])]
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

#out = get_scatter_frequency('Games\HappyBrauer.txt', 160, 0.5)
#print(out.total_length)
#print(out.scatter_index_with_frequency)
#print(out.scatter_index_with_frequency[11]) #количество скатеров с индексом 11 на одной ленте
