# coding=utf-8
import copy
import numpy as np
import math
import time
import random
from . import support as support


def isComparable(new_symbol, array, seniors):
    for symbol in array:
        if new_symbol == symbol or (new_symbol in seniors and symbol in seniors):
            return False
    return True


def find_index(weights):
    s = sum(weights)
    temp = random.uniform(0, s)
    index = 0
    while temp >= weights[index]:
        temp -= weights[index]
        index += 1
    while weights[index] == 0:
        index += 1
    return index


def get_element(array, seniors, last_symbols, senior_coef, power):
    len_ = len(array)
    weights = [0] * len_
    for i in range(len_):
        if isComparable(i, last_symbols, seniors):
            weights[i] = (array[i]) ** power
        else:
            weights[i] = 0
        if i in seniors:
            weights[i] *= senior_coef ** power
    if sum(weights) == 0:
        return -1
    return find_index(weights)


def generate_one_reel(symbols, array, distance, seniors):
    s = sum(array)
    res = []
    for j in range(10000):
        array_copy = copy.deepcopy(array)
        last_symbols = [-10] * (distance - 1)
        senior_coef = 2
        power = 1 + 0.01 * j
        good_shuffle = True

        for _ in range(s):
            new_index = get_element(array_copy, seniors, last_symbols, senior_coef, power)
            if new_index == -1:
                good_shuffle = False
                break
            for k in range(distance - 2):
                last_symbols[distance - k - 2] = last_symbols[distance - k - 3]
            last_symbols[0] = new_index
            array_copy[new_index] -= 1
            res.append(new_index)
        if good_shuffle:
            for i in range(distance - 1):
                for_compare = []
                for index in range(distance - 1):
                    for_compare.append(res[i - distance + 1 + index])
                #print(res[i], for_compare, seniors, isComparable(res[i], for_compare, seniors))
                if not isComparable(res[i], for_compare, seniors):
                    good_shuffle = False
        if good_shuffle:
            break
        else:
            res = []
            continue

    #print(res)
    result = []
    for index in res:
        result.append(symbols[index])
    return result


def reel_generator(self, array, width, distance):
    seniors = []
    res = []
    total_symbols = len(self.symbol)
    for i in range(total_symbols):
        if self.symbol[i].scatter:
            seniors.append(i)
        if self.symbol[i].wild:
            if self.symbol[i].wild.expand:
                seniors.append(i)

    for i in range(width):
        res.append(generate_one_reel(self.symbol, array[i], distance, seniors))

    self.reels = res


def count_killed_2(reel, game, line, element, d):
    m = 0

    for i in range(len(game.reels[reel])):
        if game.reels[reel][i].name == element:
            # здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
            is_upper = False
            is_lower = False
            for j in range(1, d + 1):
                if line[reel] == j:
                    for k in range(1, j):
                        if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild:
                            if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand:
                                is_upper = True
                    for k in range(j + 1, d + 1):
                        if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild:
                            if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand:
                                is_lower = True
                    break
            if is_upper == True or is_lower == True:
                m += 1
    return m


def payment_for_combination(element_num, length, obj):
    return obj.base.symbol[element_num].payment[length]


# noinspection PySimplifyBooleanCheck
def get_simple_combination(self, string, width):
    string = string.astype(int)

    res = []

    if self.symbol[string[0]].direction in ['left', 'both']:
        lens = [0] * len(self.symbol)
        for i in range(len(lens)):
            for j in range(0, width):
                if string[j] == i or string[j] in self.symbol[i].substituted_by \
                        or string[j] in self.symbol[i].substituted_by_e:
                    lens[i] += 1
                else:
                    break

        payments = [self.symbol[i].payment[lens[i]] for i in range(len(self.symbol))]
        for i in self.scatterlist:
            payments[i] = 0

        all_wilds = self.wildlist + self.ewildlist

        for i in range(len(self.symbol)):
            payment_wilds = []
            for j in range(lens[i]):
                symbol = string[j]
                if symbol in all_wilds:
                    payment_wilds.append(symbol)
            payment_wilds = list(set(payment_wilds))
            for wild in payment_wilds:
                payments[i] = payments[i] * self.symbol[wild].wild.multiplier

        max_ = max(payments)
        index = payments.index(max_)
        res.append([index, lens[index], 'left'])
    if self.symbol[string[width - 1]].direction in ['right', 'both']:
        lens = [0] * len(self.symbol)
        for i in range(len(lens)):
            for j in range(0, width):
                if string[width - 1 - j] == i or string[width - 1 - j] in self.symbol[i].substituted_by \
                        or string[width - 1 - j] in self.symbol[i].substituted_by_e:
                    lens[i] += 1
                else:
                    break

        payments = [self.symbol[i].payment[lens[i]] for i in range(len(self.symbol))]
        for i in self.scatterlist:
            payments[i] = 0

        all_wilds = self.wildlist + self.ewildlist

        for i in range(len(self.symbol)):
            payment_wilds = []
            for j in range(lens[i]):
                symbol = string[width - 1 - j]
                if symbol in all_wilds:
                    payment_wilds.append(symbol)
            payment_wilds = list(set(payment_wilds))
            for wild in payment_wilds:
                payments[i] = payments[i] * self.symbol[wild].wild.multiplier

        max_ = max(payments)
        index = payments.index(max_)
        res.append([index, lens[index], 'right'])
    return res


def fill_num_comb(self, window, lines):
    self.num_comb = np.zeros((len(self.symbol), window[0] + 1))
    start = time.time()
    combinations = support.combinations2(self, window[0], len(self.symbol))
    print('names ', time.time() - start)
    count_combinations2(self, combinations, window, lines)


def count_combinations2(self, combinations, window, lines):
    for scat in self.scatterlist:
        flags = get_all_flags(window[0])
        for flag in flags:
            res_cnt = 1
            for j in range(window[0]):
                if flag[j] == 1:
                    res_cnt = res_cnt * window[1] * self.frequency[j][scat]
                else:
                    res_cnt = res_cnt * (sum(self.frequency[j]) - window[1] * self.frequency[j][scat])
            self.num_comb[scat, int(sum(flag))] += res_cnt

    # print(len(combinations))
    for string in combinations:
        comb = get_simple_combination(self, string, window[0])
        # возвращает список элементов (индекс символа, длина комбинации)
        for t_comb in comb:
            for line in lines:
                self.num_comb[t_comb[0], t_comb[1]] += count_num_comb(self, string, line, window)


def count_num_comb(self, string, line, window):
    string = string.astype(int)

    cnt = 1
    for i in range(len(string)):
        k = self.frequency[i][string[i]]
        m = self.count_killed[self.lines.index(line)][string[i]][i]
        if self.symbol[string[i]].wild:
            if self.symbol[string[i]].wild.expand:
                k = k * window[1]
        cnt = cnt * (k - m)
    return cnt


def get_all_flags(max_len):
    total_cnt = int(2 ** max_len)
    res = np.zeros((total_cnt, max_len))
    add = np.zeros(max_len)
    add[max_len - 1] = 1
    for i in range(1, total_cnt):
        res[i] = support.plus_1(res[i - 1], add, 2)
    return res


def binomial_c(n, k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n - k)


def fill_count_killed(self, window_width):
    n_lines = len(self.lines)
    for reel_id in range(window_width):
        reel_len = len(self.reels[reel_id])
        for symbol_position in range(reel_len):
            if self.symbol.index(self.reels[reel_id][symbol_position]) in self.ewildlist:
                for line_id in range(n_lines):

                    if self.lines[line_id][reel_id] == 1:
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][(symbol_position + 1) % reel_len])][reel_id] += 1
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][(symbol_position + 2) % reel_len])][reel_id] += 1
                    if self.lines[line_id][reel_id] == 2:
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][symbol_position - 1])][reel_id] += 1
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][(symbol_position + 1) % reel_len])][reel_id] += 1
                    if self.lines[line_id][reel_id] == 3:
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][symbol_position - 2])][reel_id] += 1
                        self.count_killed[line_id][self.symbol.index(self.reels[line_id][symbol_position - 1])][reel_id] += 1


def fill_scatter_num_comb(self, window):
    self.scatter_num_comb = []
    ind = 0
    for scat in self.scatterlist:
        self.scatter_num_comb.append([scat, []])
        for _ in range(window[0] + 1):
            self.scatter_num_comb[ind][1].append(0)
        ind += 1

    ind = 0
    for scat in self.scatterlist:
        flags = get_all_flags(window[0])
        for flag in flags:
            res_cnt = 1
            for j in range(window[0]):
                if flag[j] == 1:
                    res_cnt = res_cnt * window[1] * self.frequency[j][scat]
                else:
                    res_cnt = res_cnt * (sum(self.frequency[j]) - window[1] * self.frequency[j][scat])
            self.scatter_num_comb[ind][1][int(sum(flag))] += res_cnt
        ind += 1


def fill_simple_num_comb(self, window, lines):
    all_strings = support.combinations2(self, window[0], len(self.symbol))
    result = []
    for string in all_strings:
        count = 0
        for line in lines:
            count += count_num_comb(self, string, line, window)
        result.append([string, count])
    self.simple_num_comb = copy.deepcopy(result)


def get_wilds_in_comb(self, string, comb):
    width = len(string)
    all_wilds = self.wildlist + self.ewildlist
    res = []
    if comb[2] == 'left':
        for j in range(comb[1]):
            if string[j] in all_wilds:
                res.append(string[j])
    if comb[2] == 'right':
        for j in range(comb[1]):
            if string[width - 1 - j] in all_wilds:
                res.append(string[width - 1 - j])
    res = list(set(res))
    return res


def get_simple_payment(self, string):
    width = len(string)
    combs = self.get_combination(string, width)

    res = 0
    for comb in combs:
        comb_payment = self.symbol[comb[0]].payment[comb[1]]
        wilds_in_comb = self.get_wilds_in_comb(string, comb)
        for wild in wilds_in_comb:
            comb_payment = comb_payment * self.symbol[int(wild)].wild.multiplier
        res += comb_payment
    return res
