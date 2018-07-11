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


# noinspection SpellCheckingInspection,PyChainedComparisons
def g(bag, available, length, reel, alpha, names):
    for k in range(length):
        probabilities = np.empty(available.size)
        vse_horosho = False
        available_in_bag = 0
        for j in available:
            available_in_bag += bag[j]
        if available_in_bag == 0:
            ostatok = []
            for i in range(len(bag)):
                if bag[i] > 0:
                    for _ in range(bag[i]):
                        ostatok.append(names[i])
            reel[k:] = ostatok
            break
        else:

            temp = 0
            for j in range(available.size):
                temp += math.pow(bag[available[j]], alpha)
                probabilities[j] = math.pow(bag[available[j]], alpha)
            probabilities = probabilities / temp
            r = random.random()
            left = 0
            number = ' '
            for i in range(probabilities.size):
                right = left + probabilities[i]
                if r <= right and left <= r:
                    number = i
                    break
                left = right
            bag[available[number]] -= 1
            reel[k] = names[available[number]]
            if k == 0 or k == 1:
                available = np.delete(available, number)
            else:
                available = np.arange(len(bag))
                temp_1 = reel[k]
                temp_2 = reel[k - 1]
                available = np.delete(available, [names.index(temp_1), names.index(temp_2)])
            if reel[0] != reel[length - 1] and reel[0] != reel[length - 2] and reel[1] != reel[length - 1]:
                vse_horosho = True
    result = [vse_horosho, reel]
    return result
