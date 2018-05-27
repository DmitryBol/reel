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


def combinations2(width, numbers):
    combs = np.zeros((numbers ** width, width))
    neutral = np.zeros(width)
    neutral[len(neutral) - 1] = 1
    temp = np.zeros(width)
    for i in range(numbers ** width):
        combs[i, ] = temp
        temp = plus_1(temp, neutral, numbers)
    return combs


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
                    for j in range(bag[i]):
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
