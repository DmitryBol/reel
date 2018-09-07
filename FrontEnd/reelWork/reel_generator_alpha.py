# coding=utf-8
import copy
import numpy as np
import time
import random
from . import support as support
import numpy.random as np_rnd


def index_by_name(symbols, name):
    index = 0
    for symbol in symbols:
        if symbol.name == name:
            return index
        else:
            index += 1
    raise Exception('No such symbol in rules')


def names_to_indexes(symbols, reels):
    res = []
    reel_id = 0
    for reel in reels:
        res.append([])
        for symbol_name in reel:
            res[reel_id].append(index_by_name(symbols, symbol_name))
        reel_id += 1
    return res


def remove_groups(gametype, reels):
    res = []
    reel_id = 0
    for reel in reels:
        res.append([])
        prev_id = reel[len(reel) - 1]
        group_len = 1
        start_index = 0
        while reel[start_index] == prev_id:
            start_index += 1
        for symbol_id in reel[start_index:]:
            if symbol_id == prev_id:
                group_len += 1
            else:
                if group_len not in gametype.symbol[symbol_id].group_by:
                    raise Exception('Reels have group of symbol ' + gametype.symbol[symbol_id].name + "which length "
                                                                                                      "not in rules")
                else:
                    res[reel_id].append(prev_id)
                    group_len = 1
            prev_id = symbol_id
        group_len += start_index
        symbol_id = reel[len(reel) - 1]
        if group_len not in gametype.symbol[symbol_id].group_by:
            raise Exception('Reels have group of symbol ' + gametype.symbol[symbol_id].name + " which length not in "
                                                                                              "rules")
        reel_id += 1
    return res


# Для лент из имен символов
def validate_reels(distance, gametype, reels):
    if len(reels) != gametype.window[0]:
        raise Exception('Reels have wrong dimension')
    reels_copy = names_to_indexes(gametype.symbol, reels)
    if simple_validate_reels(distance, gametype, reels_copy) == 0:
        return 0
    else:
        raise Exception("Can't validate reels")


# Для лент из индексов
def simple_validate_reels(distance, gametype, reels):
    reels_copy = remove_groups(gametype, reels)

    seniors = []
    total_symbols = len(gametype.symbol)
    for i in range(total_symbols):
        if gametype.symbol[i].scatter:
            seniors.append(i)
        if gametype.symbol[i].wild:
            if gametype.symbol[i].wild.expand:
                seniors.append(i)

    reel_id = 0
    for reel in reels_copy:
        L = len(reel)
        for index in range(L):
            if reel_id not in gametype.symbol[reel[index]].position:
                raise Exception('Reels have symbol ' + gametype.symbol[reel[index]].name + ' on ' + str(reel_id + 1) + ' reel')
            array = []
            for i in range(distance - 1):
                array.append(reel[(index + i + 1) % L])
            if not is_comparable(reel[index], array, seniors):
                raise Exception('Not valid reels')
        reel_id += 1
    return 0


def is_comparable(new_symbol, array, seniors):
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
        if is_comparable(i, last_symbols, seniors):
            weights[i] = (array[i]) ** power
        else:
            weights[i] = 0
        if i in seniors:
            weights[i] *= senior_coef ** power
    if sum(weights) == 0:
        return -1
    return find_index(weights)


def generate_one_reel(symbols, array, distance, seniors):
    s = int(sum(array))
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
            else:
                list_of_candidates = [x for x in symbols[new_index].group_by if x <= array_copy[new_index]]
                if len(list_of_candidates) < 1:
                    raise Exception('Reel frequency for symbol ' + symbols[new_index].name + "can't be divided by "
                                                                                             "minimal group length")

                probability_distribution = [1 / x for x in list_of_candidates]
                prob_s = sum(probability_distribution)
                for i in range(len(probability_distribution)):
                    probability_distribution[i] = probability_distribution[i] / prob_s
                cnt = np_rnd.choice(list_of_candidates, 1, p=probability_distribution)[0]

            for k in range(distance - 1 - cnt):
                last_symbols[distance - k - 2] = last_symbols[distance - k - 3]
            for k in range(cnt):
                last_symbols[k] = new_index
            array_copy[new_index] -= cnt
            for _ in range(cnt):
                res.append(new_index)
        if good_shuffle:
            for i in range(distance - 1):
                for_compare = []
                for index in range(distance - 1):
                    for_compare.append(res[i - distance + 1 + index])
                # print(res[i], for_compare, seniors, isComparable(res[i], for_compare, seniors))
                if not is_comparable(res[i], for_compare, seniors):
                    good_shuffle = False
        if good_shuffle:
            break
        else:
            res = []
            continue

    # print(res)
    result = []
    for index in res:
        result.append(symbols[index])
    return res


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

    if simple_validate_reels(distance, self, res) == 0:
        return
    else:
        raise Exception("Can't validate reels")


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


def fill_count_killed(self, window_width):
    n_lines = len(self.lines)
    n_symbols = len(self.symbol)

    for line_id in range(n_lines):
        for symbol_id in range(n_symbols):
            for reel_id in range(window_width):
                self.count_killed[line_id][symbol_id][reel_id] = 0

    for reel_id in range(window_width):
        reel_len = len(self.reels[reel_id])
        for symbol_position in range(reel_len):

            if self.reels[reel_id][symbol_position] in self.ewildlist:
                for line_id in range(n_lines):

                    if self.lines[line_id][reel_id] == 1:
                        # print(line_id, reel_id)
                        # print(self.count_killed[line_id])
                        # print((symbol_position + 1) % reel_len)
                        # print(self.reels[reel_id][(symbol_position + 1) % reel_len])
                        self.count_killed[line_id][self.reels[reel_id][(symbol_position + 1) % reel_len]][reel_id] += 1
                        self.count_killed[line_id][self.reels[reel_id][(symbol_position + 2) % reel_len]][reel_id] += 1

                    if self.lines[line_id][reel_id] == 2:
                        self.count_killed[line_id][self.reels[reel_id][symbol_position - 1]][reel_id] += 1
                        self.count_killed[line_id][self.reels[reel_id][(symbol_position + 1) % reel_len]][reel_id] += 1
                    if self.lines[line_id][reel_id] == 3:
                        self.count_killed[line_id][self.reels[reel_id][symbol_position - 2]][reel_id] += 1
                        self.count_killed[line_id][self.reels[reel_id][symbol_position - 1]][reel_id] += 1
    # print(self.count_killed)
    # support.print_game(self)


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
    len_ = len(all_strings)
    for i in range(len_):
        string = all_strings[i]
        count = 0
        for line in lines:
            count += count_num_comb(self, string, line, window)
        self.simple_num_comb_first[i][1] = count_num_comb(self, string, lines[0], window)
        self.simple_num_comb[i][1] = count


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


def create_simple_num_comb(self, window, lines):
    all_strings = support.combinations2(self, window[0], len(self.symbol))
    result = []
    for string in all_strings:
        result.append([string, 0, self.get_simple_payment(string)])
    self.simple_num_comb = copy.deepcopy(result)
    self.simple_num_comb_first = copy.deepcopy(result)
