# coding=utf-8
# coding=utf-8
# coding=utf-8
# coding=utf-8
import copy
import numpy as np
import math
import time
support = __import__("support")

h = 0.005


# noinspection SpellCheckingInspection
def reel_generator(self, array, width):
    self.reels = [] * width
    for k in range(width):
        tmp = []
        for i in range(len(array[k])):
            for _ in range(array[k][i]):
                tmp.append('empty')
        self.reels.append(tmp)
    names = self.symbol
    for i in range(len(array)):
        alpha = 1

        scat_and_wild = self.scatterlist + self.ewildlist

        bag = copy.deepcopy(array[i])
        available = np.arange(len(array[i]))
        tmp = support.g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
        vse_horosho = tmp[0]
        while not vse_horosho:
            bag = copy.deepcopy(array[i])
            alpha += h
            available = np.arange(len(array))
            np.delete(available, [names.index(tmp[1][len(tmp[1]) - 1]), names.index(tmp[1][len(tmp[1]) - 2])])
            tmp = support.g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
            vse_horosho = tmp[0]
        self.reels[i] = tmp[1]


# конструктор принимает на вход два массива: 1ый - массив количества элементов, 2ой- их имена. Класс содержит список
# барабанов


def count_killed_2(reel, game, line, element, d):
    m = 0

    for i in range(len(game.reels[reel])):
        if game.reels[reel][i].name == element:
            #здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
            is_upper = False
            is_lower = False
            for j in range(1, d+1):
                if line[reel] == j:
                    for k in range(1, j):
                        if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand == True:
                            is_upper = True
                    for k in range(j+1, d+1):
                        if game.reels[reel][(i + k - j) % len(game.reels[reel])].wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand == True:
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
        lens = [0]*len(self.symbol)
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

    #print(len(combinations))
    for string in combinations:
        comb = get_simple_combination(self, string, window[0])
        #возвращает список элементов (индекс символа, длина комбинации)
        for t_comb in comb:
            for line in lines:
                self.num_comb[t_comb[0], t_comb[1]] += count_num_comb(self, string, line, window)


# noinspection PySimplifyBooleanCheck
def count_num_comb(self, string, line, window):

    string = string.astype(int)

    cnt = 1
    for i in range(len(string)):
        k = self.frequency[i][string[i]]
        m = count_killed_2(i, self, line, self.symbol[string[i]].name, window[1])
        if self.symbol[string[i]].wild != False:
            if self.symbol[string[i]].wild.expand == True:
                k = k * window[1]
        # if self.symbol[string[i]].scatter:
        #   k = k * window[1]
        cnt = cnt * (k - m)
    return cnt


def get_all_flags(max_len):
    total_cnt = int(2**max_len)
    res = np.zeros((total_cnt, max_len))
    add = np.zeros(max_len)
    add[max_len - 1] = 1
    for i in range(1, total_cnt):
        res[i] = support.plus_1(res[i - 1], add, 2)
    return res


def binomial_c(n, k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n - k)


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
