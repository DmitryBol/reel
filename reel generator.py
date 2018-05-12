import sys
import random
import json
import copy
import numpy as np
import math

sys.path.insert(0, 'Front-end/')
import structure

h = 0.005
def g(bag, available, length, reel, alpha, names):
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
    def __init__(self, array, obj):
        self.reels = []
        for k in range(obj.window[0]):
            tmp = []
            for i in range(len(array[k])):
                for j in range(array[k][i]):
                    tmp.append('empty')
            self.reels.append(tmp)
        #self.len = len(tmp)
        names = obj.symbol
  #      names = []
        #for i in obj.symbol:
        #    names.append(i.name)
        for i in range(len(array)):
            alpha = 1
            bag = copy.deepcopy(array[i])
            available = np.arange(len(array[i]))
            tmp = g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
            vse_horosho = tmp[0]
            while(not vse_horosho):
                bag = copy.deepcopy(array[i])
                alpha += h
                available = np.arange(len(array))
                np.delete(available, [names.index(tmp[1][len(tmp[1]) - 1]),names.index(tmp[1][len(tmp[1]) - 2])])
                tmp = g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
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
                print(test.reels[j][i].name, end=(25 - len(test.reels[j][i].name))*' ')
            else:
                s = 24*' '
                print(s, end=' ')
        print('\n')
#распечатывает сгенерированные барабаны

def is_expand_wild(a):
    if(str(a) == 'Crown'):
        return True
    else:
        return False


def count_killed(reel, game, line, element, d):#старая версия функции ниже
    m = 0
    for i in range(len(game.reels[reel])):
        if(line[reel] == 1):
            if(game.reels[reel][i].name == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
                if(game.reels[reel][(i + 1) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i + 1) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
                elif(game.reels[reel][(i + 2) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i + 2) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
        elif(line[reel] == 2):
            if(game.reels[reel][i].name == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
                if(game.reels[reel][(i + 1) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i + 1) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
                elif(game.reels[reel][(i - 1) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i - 1) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
        elif(line[reel] == 3):
            if(game.reels[reel][i].name == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
                if(game.reels[reel][(i - 1) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i - 1) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
                elif(game.reels[reel][(i - 2) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i - 2) % len(game.reels[reel])].base.wild.expand == True):
                    m += 1
    return(m)


def count_killed_2(reel, game, line, element, d):
    m = 0
    for i in range(len(game.reels[reel])):
        if(game.reels[reel][i].name == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
            is_upper = False
            is_lower = False
            for j in range(1, d+1):
                if(line[reel] == j):
                    for k in range(1, j):
                        if(game.reels[reel][(i + k - j) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].base.wild.expand == True):
                            is_upper = True
                    for k in range(j+1, d+1):
                        if(game.reels[reel][(i + k - j) % len(game.reels[reel])].base.wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].base.wild.expand == True):
                            is_lower = True
                    break
            if(is_upper == True or is_lower == True):
                m += 1
    return(m)

def payment_for_combination(element_num, length, obj):
    return(obj.symbol[element_num].payment[length])

def more_expensive_combination(payment, wild_num, length, object):#возращает True если из length wild_num можно составить комбинацию длины <= length с большей выплатой чем length подрядя element_num, иначе - False
    possible_elements = object.symbol[wild_num].base.wild.substitute
    l = []
    for i in possible_elements:
        for j in range(1, min(length + 1, object.window[0])):
            l.append(object.symbol[i].payment[j])
    result = max(l)
    if(result > payment):
        return True
    else:
        return False





def count_combinations(game, line_num, element_num, length, obj):
    k = []
    w = []#число wilds заменяющих element
    e = []#число expand wilds заменяющих element
    m = []
    n = []
    names = []
    wilds = obj.symbol[element_num].base.substituted_by
    expands = obj.symbol[element_num].base.substituted_by_e
    wild_alpha = []
    e_wild_alpha = []
    for i in obj.symbol:
        names.append(i.name)
    for v in wilds:
        temp = []
        for i in range(object.window[0]):
            tmp = 0
            for j in range(len(obj.symbol)):
                if(obj.symbol[j].base.wild != False):
                    if(obj.symbol[j].base.wild.expand != True):
                        if(v == j):
                            tmp += frequency[i][j]
            temp.append(tmp)
        wild_alpha.append(temp)
    for v in expands:
        temp = []
        for i in range(object.window[0]):
            tmp = 0
            for j in range(len(obj.symbol)):
                if(obj.symbol[j].base.wild != False):
                    if(obj.symbol[j].base.wild.expand == True):
                        if(v == j):
                            tmp += frequency[i][j]
            temp.append(tmp)
        e_wild_alpha.append(temp)

    line = obj.lines[line_num]
    element = obj.symbol[element_num].name
    for i in range(obj.window[0]):
        reel = i
        ind = names.index(element)
        k.append(frequency[i][ind])
        tmp = 0
        for j in range(len(obj.symbol)):
            if(obj.symbol[j].base.wild != False):
                if(obj.symbol[j].base.wild.expand != True):
                    if(element_num in obj.symbol[j].base.wild.substitute):
                        tmp += frequency[i][j]
        w.append(tmp)#в shining crown нет обычных wild
        n.append(len(game.reels[i]))
        tmp = 0
        for j in range(len(obj.symbol)):
            if(obj.symbol[j].base.wild != False):
                if(obj.symbol[j].base.wild.expand == True):
                    if(element_num in obj.symbol[j].base.wild.substitute):
                        tmp += frequency[i][j]
        e.append(tmp)
        m.append(count_killed_2(reel, game, line, element, 3))
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
    for i in range(length+1, obj.window[1]):
        tmp = tmp*n[i]

    print(k, w, e, m,  n)
    print(line)
    payment = payment_for_combination(element_num, length, obj)
    print('payment for combination',payment)


    first = tmp
    second = 0
    print('printing wild alpha', wild_alpha)
    print('printing expand wild alpha', e_wild_alpha)
    for l in range(len(wild_alpha)):
        if(more_expensive_combination(payment, wilds[l], length, object)):
            tmp1 = 1
            for j in range(length):
                for i in range(j):
                    tmp1 = tmp1*wild_alpha[l][i]
                #tmp1 = tmp1*(k[j+1] + w[j+1] - wild_alpha[l][j+1] + 3*e[j+1] - m[j+1])
                print('number = ', k[j+1] + w[j+1] - wild_alpha[l][j+1] + 3*e[j+1] - m[j+1])
                '''for i in range(j+2, length):
                    tmp1 = tmp1*(k[i] + w[i] + 3*e[i] - m[i])
                tmp1 = tmp1*(n[length + 1] - k[length + 1] - w[length + 1] - 3*e[length + 1] + m[length +1])
                for i in range(length + 2, object.window[0]):
                    tmp1 = tmp1*n[i]'''
            second += tmp1
    return(first, second)


f = open('Front-end/input2.txt', 'r')
text = f.read()
rules = json.loads(text)
object = structure.Game(rules)

#frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]
#frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2, 2, 1, 0]
#frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2, 3, 1, 3]
#frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2, 4, 1, 0]
#frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]



frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2]
frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

game = reel_generator(frequency, object)

print_game(game)

element_number = 2
length = 4

print('element = ', object.symbol[element_number].name)

print(count_combinations(game, 3, element_number, length, object))

print(object.symbol[2].base.substituted_by_e)
print(object.set_of_base_ewilds)


payment = payment_for_combination(element_number, length, object)
print('is there more expensive combination ', more_expensive_combination(payment, 6, length, object))
print(object.symbol[6].payment[length])



