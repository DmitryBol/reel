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
        self.reels = []
        for k in range(len(array)):
            tmp = []
            for i in range(len(array[k])):
                for j in range(array[k][i]):
                    tmp.append('empty')
            self.reels.append(tmp)
        #self.len = len(tmp)

        for i in range(len(array)):
            alpha = 1
            bag = copy.deepcopy(array[i])
            available = np.arange(len(array[i]))
            tmp = g(bag, available, len(self.reels[i]), self.reels[i], alpha)
            vse_horosho = tmp[0]
            while(not vse_horosho):
                bag = copy.deepcopy(array[i])
                alpha += h
                available = np.arange(len(array))
                np.delete(available, [names.index(tmp[1][len(tmp[1]) - 1]),names.index(tmp[1][len(tmp[1]) - 2])])
                tmp = g(bag, available, len(self.reels[i]), self.reels[i], alpha)
                vse_horosho = tmp[0]
            self.reels[i] = tmp[1]





#конструктор принимает на вход два массива: 1ый - массив количества элементов, 2ой- их имена. Класс содержит список барабанов
def print_game(test):
    c = []
    for i in range(len(test.reels)):
        c.append(len(test.reels[i]))
    a = max(c)
    for i in range(a):
        for j in range(len(test.reels)):
            if(i < len(test.reels[j])):
                print(test.reels[j][i], end=(9 - len(test.reels[j][i]))*' ')
            else:
                s = 8*' '
                print(s, end=' ')
        print('\n')
#распечатывает сгенерированные барабаны

def is_expand_wild(a):
    if(str(a) == 'Crown'):
        return True
    else:
        return False

def count_killed(reel, game, line, element):
    m = 0
    for i in range(len(game.reels[reel])):
        if(line[reel] == 1):
            if(game.reels[reel][i] == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
                if(is_expand_wild(game.reels[reel][(i + 1) % len(game.reels[reel])]) or is_expand_wild(game.reels[reel][(i + 2) % len(game.reels[reel])])):
                    m += 1
        elif(line[reel] == 2):
            if(game.reels[reel][i] == element):
                if(is_expand_wild(game.reels[reel][(i - 1) % len(game.reels[reel])]) or is_expand_wild(game.reels[reel][(i + 1) % len(game.reels[reel])])):
                    m += 1
    if(line[reel] == 3):
        if(game.reels[reel][i] == element):
            if(is_expand_wild(game.reels[reel][(i - 1) % len(game.reels[reel])]) or is_expand_wild(game.reels[reel][(i - 2) % len(game.reels[reel])])):
                m += 1
    return(m)

def count_combinations(game, line, element, length, names):
    k = []
    w = []
    e = []
    m = []
    n = []
    for i in range(5):
        reel = i
        ind = names.index(element)
        k.append(frequency[i][ind])
        w.append(0)#в shining crown нет обычных wild
        n.append(len(game.reels[i]))
        tmp = 0
        for j in range(len(names)):
            if(is_expand_wild(names[j])):
                tmp += frequency[i][j]
        e.append(tmp)
        m.append(count_killed(reel, game, line, element))
    for i in range(2):
        k.append(0)
        w.append(0)
        e.append(0)
        m.append(0)
        n.append(1)

    tmp = 1
    for i in range(length):
        tmp = tmp*(k[i] + w[i] + 3*e[i] - m[i])
    tmp = tmp*(n[length] - k[length] - w[length] - 3*e[length] + m[length])
    for i in range(length+1, 7):
        tmp = tmp*n[i]
    print(k, w, e, m, n)
    print(line)
    first = tmp
    print(first)
    return(first)




f = open('Shining_Crown.txt', 'r')
text = f.read()
rules = json.loads(text)


frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]
frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2, 2, 1, 0]
frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2, 3, 1, 3]
frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2, 4, 1, 0]
frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]
frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

names = []
for i in range(len(rules['symbol'])):
    names.append(rules['symbol'][i]['name'])


game = reel_generator(frequency, names)



print_game(game)

count_combinations(game, rules['lines'][3], 'Melon', 4, names)




