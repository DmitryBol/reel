import random
import json
import copy
import numpy as np
import math

h = 0.005
def g(bag, available, length, reel, alpha):
    for k in range(length):
        probabilities = np.empty(available.size)
        vse_horosho = False
        available_in_bag = 0
        for j in available:
            available_in_bag += bag[j]
        if(available_in_bag == 0):
            ostatok = []
            for i in range(len(bag)):
                if(bag[i] > 0):
                    for j in range(bag[i]):
                        ostatok.append(names[i])
            reel[k:] = ostatok
            break
        else:

            temp = 0
            for j in range(available.size):
                temp += math.pow(bag[available[j]], alpha)
                probabilities[j] = math.pow(bag[available[j]], alpha)
            probabilities = probabilities/temp
            r = random.random()
            left = 0
            number = ' '
            for i in range(probabilities.size):
                right = left + probabilities[i]
                if(r <= right and r >= left):
                    number = i
                    break
                left = right
            bag[available[number]] -= 1
            reel[k] = names[available[number]]
            if(k == 0 or k == 1):
                available = np.delete(available,number)
            else:
                available = np.arange(len(bag))
                temp_1 = reel[k]
                temp_2 = reel[k-1]
                available = np.delete(available, [names.index(temp_1), names.index(temp_2)])
            if(reel[0] != reel[length - 1] and reel[0] != reel[length - 2] and reel[1] != reel[length - 1]):
                vse_horosho = True
    result = [vse_horosho, reel]
    return result


class reel_generator(object):
    def __init__(self, array, names):
        tmp = []
        for i in range(len(array)):
            for j in range(array[i]):
                tmp.append('empty')
        reel_1 = copy.deepcopy(tmp)
        reel_2 = tmp.copy()
        reel_3 = tmp.copy()
        reel_4 = tmp.copy()
        reel_5 = tmp.copy()
        self.len = len(tmp)
        self.reels = [reel_1, reel_2, reel_3, reel_4, reel_5]
        for i in range(5):
            alpha = 1
            bag = copy.deepcopy(frequency)
            available = np.arange(len(array))
            tmp = g(bag, available, self.len, self.reels[i], alpha)
            vse_horosho = tmp[0]
            while(not vse_horosho):
                bag = copy.deepcopy(frequency)
                alpha += h
                available = np.arange(len(array))
                np.delete(available, [names.index(tmp[1][len(tmp[1]) - 1]),names.index(tmp[1][len(tmp[1]) - 2])])
                tmp = g(bag, available, self.len, self.reels[i], alpha)
                vse_horosho = tmp[0]
            self.reels[i] = tmp[1]


#конструктор принимает на вход два массива: 1ый - массив количества элементов, 2ой- их имена. Класс содержит список барабанов
def print_game(test):
    for i in range(len(test.reels[0])):
        print(test.reels[0][i], end=(9 - len(test.reels[0][i]))*' ')
        print(test.reels[1][i], end=(9 - len(test.reels[1][i]))*' ')
        print(test.reels[2][i], end=(9 - len(test.reels[2][i]))*' ')
        print(test.reels[3][i], end=(9 - len(test.reels[3][i]))*' ')
        print(test.reels[4][i], end=(9 - len(test.reels[4][i]))*' ')
        print('\n')
#распечатывает сгенерированные барабаны

def is_wild(a):
    if(str(a) == 'Crown'):
        return True
    else:
        return False



f = open('Shining_Crown.txt', 'r')
text = f.read()
rules = json.loads(text)


frequency = [3, 7, 3, 3, 2, 3, 4, 15, 3, 6, 3]


names = []
for i in range(len(rules['symbol'])):
    names.append(rules['symbol'][i]['name'])


game = reel_generator(frequency, names)

print_game(game)






#print_game(game)

#counter = counting_combinations(rules['symbol'][0]['name'], 7, 3, rules)

#print('counter is ', counter)