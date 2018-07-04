import numpy as np
import random

def isComparable(x, s1, s2):
    return x != s1 and x != s2 and not (isSenior(x) and isSenior(s1)) and not (isSenior(x) and isSenior(s2))

def isSenior(x):
    return (x in [0, 1]) #для случая скаттер и вайлд с индексами 0, 1

def get_index(weights):
    s = sum(weights)
    if s == 0:
        return -1
    temp = random.uniform(0, s)
    index = 0
    temp0 = temp
    while temp > weights[index]:
        temp -= weights[index]
        index += 1
    while weights[index] == 0:
        index += 1
    return index

#senior_coeff - коэффициент увеличения веса "важных" символов, power - показатель степени
def get_element(indexes_with_frequency, senior_coeff, power, s1, s2):
    n = len(indexes_with_frequency)
    weights = [0]*n
    for i in range(n):
        weights[i] = (indexes_with_frequency[i, 1])**power
        if isSenior(i):
            weights[i] *= (senior_coeff)**power
        #print(i, s1, s2, isComparable(i, s1, s2))
        if not isComparable(i, s1, s2):
            weights[i] = 0
    res = get_index(weights)
    if res != -1:
        indexes_with_frequency[res, 1] -= 1
    return res


n = 13 #количество символов
for j in range(10):
    can_continue = True
    frequency = [4, 6, 10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]

    indexes_with_frequency = np.zeros((n, 2))
    for i in range(n):
        indexes_with_frequency[i, 0] = i
        indexes_with_frequency[i, 1] = frequency[i]

    total_symbols = sum(frequency)
    res = []
    s1 = -10
    s2 = -20
    for i in range(total_symbols):    
        new_s = get_element(indexes_with_frequency, 2, 2, s1, s2) 
        if new_s == -1:
            can_continue = False
            break
        res.append(new_s)
        s2 = s1
        s1 = new_s
    if not can_continue:
        #print(len(res), 'of', total_symbols)
        print(res)
        continue
    if isComparable(res[0], res[-1], res[-2]) and isComparable(res[1], res[0], res[-1]):
        print(res)
        break

print('iterations: ', j + 1)
