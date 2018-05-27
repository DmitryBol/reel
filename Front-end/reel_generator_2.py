import copy
import numpy as np
import math
import support

h = 0.005


# noinspection SpellCheckingInspection
def reel_generator(self, array, width):
    for k in range(width):
        tmp = []
        for i in range(len(array[k])):
            for j in range(array[k][i]):
                tmp.append('empty')
        self.reels.append(tmp)
    names = self.symbol
    for i in range(len(array)):
        alpha = 1
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

    if self.symbol[0].direction == 'left':
        lens = [0]*len(self.symbol)
        for i in range(len(lens)):
            for j in range(0, width):
                if string[j] == i or string[j] in self.symbol[i].substituted_by:
                    lens[i] += 1
                else:
                    break

        payments = [self.symbol[i].payment[lens[i]] for i in range(len(self.symbol)) if i not in self.scatterlist]
        max_ = max(payments)
        index = payments.index(max_)
        return [[index, lens[index]]]
    elif self.direction == 'right':
        begin = string[len(string) - 1]
        subst = [begin]
        if self.symbol[begin].wild != False:
            subst = subst + self.symbol[begin].wild.substitute
        subst_l = [1]*len(subst)
        for i in range(len(subst)):
            flag = True
            for j in range(width - 2, -1, -1):
                if flag:
                    if string[j] == begin or string[j] == subst[i]:
                        subst_l[i] += 1
                    else:
                        flag = False
                else:
                    break
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst)) if i not in self.scatterlist]
        max_ = max(payments)
        index = payments.index(max_)
        return [[subst[index], subst_l[index]]]

    elif self.direction == 'both':
        begin = string[0]
        subst = [begin]
        if self.symbol[begin].wild != False:
            subst = subst + self.symbol[begin].wild.substitute
        subst_l = [1]*len(subst)
        for i in range(len(subst)):
            flag = True
            for j in range(1, width):
                if flag:
                    if string[j] == begin or string[j] == subst[i]:
                        subst_l[i] += 1
                    else:
                        flag = False
                else:
                    break
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst)) if i not in self.scatterlist]
        max_ = max(payments)
        index = payments.index(max_)
        res_left = [subst[index], subst_l[index]]

        begin = string[len(string) - 1]
        subst = [begin]
        if self.symbol[begin].wild != False:
            subst = subst + self.symbol[begin].wild.substitute
        subst_l = [1]*len(subst)
        for i in range(len(subst)):
            flag = True
            for j in range(width - 2, -1, -1):
                if flag:
                    if string[j] == begin or string[j] == subst[i]:
                        subst_l[i] += 1
                    else:
                        flag = False
                else:
                    break
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst)) if i not in self.scatterlist]
        max_ = max(payments)
        index = payments.index(max_)
        res_right = [subst[index], subst_l[index]]

        if res_right[1] != width:
            return [res_left, res_right]
        else:
            return [res_right]


def fill_num_comb(self, window, lines):
    self.num_comb = np.zeros((len(self.symbol), window[0] + 1))
    combinations = support.combinations2(window[0], len(self.symbol))
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
    temp = -1

    for string in combinations:
        if string[0] != temp:
            print(string)
            temp += 1
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
        if self.symbol[string[i]].scatter:
            k = k * window[1]
        cnt = cnt * (k - m)
    return cnt


def get_all_flags(max_len):
    total_cnt = int(2**max_len)
    res = np.zeros((total_cnt, max_len))
    add = np.zeros(max_len)
    add[max_len - 1] = 1
    for i in range(1, total_cnt):
        res[i] = support.plus_1(res[i - 1], add, max_len, 2)
    return res


def binomial_c(n, k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n - k)
