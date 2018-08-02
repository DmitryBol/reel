import numpy as np
import math
import random


# noinspection SpellCheckingInspection
def plus_1(a, b, alls):
    temp = a + b
    result = np.zeros(len(a))
    add = 0
    sup = alls
    for i in range(len(a) - 1, -1, -1):
        result[i] = (temp[i] + add) % sup
        add = (temp[i] + add) // sup
    return result


def super_plus(array, possible_symbols):
    width = len(possible_symbols)
    add = np.zeros((1, width))
    add[0, width - 1] = 1
    temp = array + add
    res = np.zeros((1, width))
    ost = 0
    for i in range(width - 1, -1, -1):
        res[0, i] = (temp[0, i] + ost) % len(possible_symbols[i])
        ost = (temp[0, i] + ost) // len(possible_symbols[i])
    return res


# noinspection SpellCheckingInspection,PyUnusedLocal
def combinations2(gametype, width, numbers):

    combs = np.zeros((1, width))
    for symbol_index in range(len(gametype.symbol)):
        for index in range(len(gametype.symbol[symbol_index].payment)):
            if gametype.symbol[symbol_index].payment[index] > 0:
                possible_symbols = [[] for i in range(width)]
                for j in range(index):
                    possible_symbols[j].append(symbol_index)
                    for subs in gametype.symbol[symbol_index].substituted_by:
                        possible_symbols[j].append(subs)
                    for e_subs in gametype.symbol[symbol_index].substituted_by_e:
                        possible_symbols[j].append(e_subs)
                for j in range(index, width):
                    for s1 in range(len(gametype.symbol)):
                        possible_symbols[j].append(s1)
                for j in range(width):
                    possible_symbols[j].sort()
                big_len = 1
                for j in range(width):
                    big_len = big_len * len(possible_symbols[j])
                possible_combs = np.zeros((big_len, width))
                for j in range(1, big_len):
                    possible_combs[j] = super_plus(possible_combs[j - 1], possible_symbols)
                for i in range(big_len):
                    for j in range(width):
                        possible_combs[i, j] = possible_symbols[j][int(possible_combs[i, j])]
                combs = np.concatenate((combs, possible_combs), axis=0)
    data_set = set(tuple(row) for row in combs)
    return np.array(list(data_set))

def print_game(test):
    c = []
    for i in range(len(test.reels)):
        c.append(len(test.reels[i]))
    a = max(c)
    for i in range(a):
        for j in range(len(test.reels)):
            if(i < len(test.reels[j])):
                print(test.reels[j][i].name, end=(25 - len(test.reels[j][i].name))*' ')
            else:
                s = 24*' '
                print(s, end=' ')
        print('\n')
