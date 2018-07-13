import random
import json
import copy
import numpy as np
import math
#import structure_alpha
import support


def plus(a, b, l, sup):
    temp = a + b
    result = np.zeros(l)
    add = 0
    for i in range(l-1, -1, -1):
        result[i] = (temp[i] + add)%sup
        add = (temp[i] + add)//sup
    return(result)

h = 0.005

'''
просто добавлено в файл support

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
'''

def reel_generator(self, array, width):
    for k in range(width):
        tmp = []
        for i in range(len(array[k])):
            for j in range(array[k][i]):
                tmp.append('empty')
        self.reels.append(tmp)
    #self.len = len(tmp)
    names = self.symbol
    #      names = []
    #for i in obj.symbol:
    #    names.append(i.name)
    for i in range(len(array)):
        alpha = 1
        bag = copy.deepcopy(array[i])
        available = np.arange(len(array[i]))
        tmp = support.g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
        vse_horosho = tmp[0]
        while(not vse_horosho):
            bag = copy.deepcopy(array[i])
            alpha += h
            available = np.arange(len(array))
            np.delete(available, [names.index(tmp[1][len(tmp[1]) - 1]),names.index(tmp[1][len(tmp[1]) - 2])])
            tmp = support.g(bag, available, len(self.reels[i]), self.reels[i], alpha, names)
            vse_horosho = tmp[0]
        self.reels[i] = tmp[1]


'''
переписано выше, теперь это метод подкласса Gametype

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
        names = obj.base.symbol
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
'''
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

def count_killed_2(reel, game, line, element, d):
    m = 0

    for i in range(len(game.reels[reel])):
        if(game.reels[reel][i].name == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
            is_upper = False
            is_lower = False
            for j in range(1, d+1):
                if(line[reel] == j):
                    for k in range(1, j):
                        if(game.reels[reel][(i + k - j) % len(game.reels[reel])].wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand == True):
                            is_upper = True
                    for k in range(j+1, d+1):
                        if(game.reels[reel][(i + k - j) % len(game.reels[reel])].wild != False and game.reels[reel][(i + k - j) % len(game.reels[reel])].wild.expand == True):
                            is_lower = True
                    break
            if(is_upper == True or is_lower == True):
                m += 1
    return(m)


def count_killed_3(reel, game, line, element, d, self):
    m = 0

    for i in range(len(game[reel])):
        if(game[reel][i] == element):#здесь еще нужна проверка на wild - or is_wild(game.reels[reel][i])
            is_upper = False
            is_lower = False
            for j in range(1, d+1):
                if(line[reel] == j):
                    for k in range(1, j):
                        if(game[reel][(i + k - j) % len(game[reel])] in self.base.wildlist  and game[reel][(i + k - j) % len(game[reel])] in self.base.ewildlist):
                            is_upper = True
                    for k in range(j+1, d+1):
                        if(game[reel][(i + k - j) % len(game[reel])] in self.base.wildlist  and game[reel][(i + k - j) % len(game[reel])] in self.base.ewildlist):
                            is_lower = True
                    break
            if(is_upper == True or is_lower == True):
                m += 1
    return(m)






def payment_for_combination(element_num, length, obj):
    return(obj.base.symbol[element_num].payment[length])


def get_combination(self, string, width):

    string = string.astype(int)

    scat_res = []
    for scat in self.scatterlist:
        cnt = 0
        for element in string:
            if element == scat:
                cnt += 1
        if self.symbol[scat].payment[cnt] > 0 or self.symbol[scat].scatter[cnt] > 0:
            scat_res.append([scat, cnt])

    if self.symbol[0].direction == 'left':
        lens = [0]*len(self.symbol)
        for i in range(len(lens)):
            for j in range(0, width):
                if string[j] == i or string[j] in self.symbol[i].substituted_by:
                    lens[i] += 1
                else:
                    break

        payments = [self.symbol[i].payment[lens[i]] for i in range(len(self.symbol))]
        max_ = max(payments)
        index = payments.index(max_)
        return scat_res + [[index, lens[index]]]
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
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst))]
        max_ = max(payments)
        index = payments.index(max_)
        return scat_res + [[subst[index], subst_l[index]]]

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
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst))]
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
        payments = [self.symbol[subst[i]].payment[subst_l[i]] for i in range(len(subst))]
        max_ = max(payments)
        index = payments.index(max_)
        res_right = [subst[index], subst_l[index]]

        if res_right[1] != width:
            return scat_res + [res_left, res_right]
        else:
            return scat_res + [res_right]


def fill_num_comb(self, window, lines):
    self.num_comb = np.zeros((len(self.symbol), window[0] + 1))
    for line_num in range(len(lines)):
        count_combinations2(self, lines[line_num], window)
    for scat in self.scatterlist:
        self.num_comb[scat] = self.num_comb[scat]//len(lines)


def count_combinations2(self, line, window):
    numbers = len(self.symbol)
    combinations = support.combinations2(window[0], window[1], numbers)
    temp = -1
    for string in combinations:
        if string[0] != temp:
            print(string)
            temp += 1
        comb = get_combination(self, string, window[0])#возвращает индекс символа и длину
        for t_comb in comb:
            self.num_comb[t_comb[0], t_comb[1]] += count_num_comb(self, string, line, window)


def count_num_comb(self, string, line_num, window):

    string = string.astype(int)

    cnt = 1
    for i in range(len(string)):
        k = self.frequency[i][string[i]]
        m = count_killed_2(i, self, line_num, self.symbol[string[i]].name, window[1])
        if self.symbol[string[i]].wild != False:
            if self.symbol[string[i]].wild.expand == True:
                k = k * window[1]
        if self.symbol[string[i]].scatter:
            k = k * window[1]
        cnt = cnt * (k - m)
    return cnt




def count_combinations(game, line_num, element_num, length, obj, frequency):
    k = []
    w = []#число wilds заменяющих element
    e = []#число expand wilds заменяющих element
    m = []
    n = []
    names = []
    wilds = obj.base.symbol[element_num].substituted_by
    expands = obj.base.symbol[element_num].substituted_by_e
    #print('Expands ', expands)
    wild_alpha = []
    e_wild_alpha = []
    for i in obj.base.symbol:
        names.append(i.name)
    for v in wilds:
        temp = []
        for i in range(obj.window[0]):#!
            tmp = 0
            for j in range(len(obj.base.symbol)):
                if(obj.base.symbol[j].wild != False):
                    if(obj.base.symbol[j].wild.expand != True):
                        if(v == j):
                            tmp += frequency[i][j]
            temp.append(tmp)
        for i in range(obj.window[0], obj.window[0] + 2):
            tmp = 0
            temp.append(tmp)
        wild_alpha.append(temp)
    for v in expands:
        temp = []
        for i in range(obj.window[0]):
            tmp = 0
            for j in range(len(obj.base.symbol)):
                if(obj.base.symbol[j].wild != False):
                    if(obj.base.symbol[j].wild.expand == True):
                        if(v == j):
                            tmp += frequency[i][j]
            temp.append(tmp)
        e_wild_alpha.append(temp)
    bad = []
    for i in range(len(obj.base.symbol)):
        if( i != element_num):
            if(obj.base.symbol[i].wild == False):
                bad.append(i)
            elif(element_num not in obj.base.symbol[i].wild.substitute):
                bad.append(i)
    bad_m = []





    line = obj.line[line_num]

    for j in range(len(bad)):
        temp = []
        badElem = obj.base.symbol[bad[j]].name
        for i in range(obj.window[0]):
            reel = i
            temp.append(count_killed_3(reel, game, line, badElem, obj.window[1], obj))
        bad_m.append(temp)


    element = obj.base.symbol[element_num].name
    for i in range(obj.window[0]):
        reel = i
        ind = names.index(element)
        k.append(frequency[i][ind])
        tmp = 0
        for j in range(len(obj.base.symbol)):
            if(obj.base.symbol[j].wild != False):
                if(obj.base.symbol[j].wild.expand != True):
                    if(element_num in obj.base.symbol[j].wild.substitute):
                        tmp += frequency[i][j]
        w.append(tmp)
        n.append(len(game[i]))
        tmp = 0
        for j in range(len(obj.base.symbol)):
            if(obj.base.symbol[j].wild != False):
                if(obj.base.symbol[j].wild.expand == True):
                    if(element_num in obj.base.symbol[j].wild.substitute):
                        tmp += frequency[i][j]
        e.append(tmp)
        m.append(count_killed_3(reel, game, line, element, obj.window[1]), obj)
    for i in range(2):
        k.append(0)
        w.append(0)
        e.append(0)
        m.append(0)
        n.append(1)
    tmp = 1
    for i in range(length):
        tmp2 = 0
        for v in range(len(wilds)):
            tmp2 += wild_alpha[v][i]
        tmp = tmp*(k[i] + tmp2 + 3*e[i] - m[i])
    tmp2 = 0
    for v in range(len(wilds)):
        tmp2 += wild_alpha[v][length]
    tmp = tmp*(n[length] - k[length] - tmp2 - 3*e[length] + m[length])
    for i in range(length+1, obj.window[0]):
        tmp = tmp*n[i]

    #print(k, w, e, m,  n)
    #print(line)
    payment = payment_for_combination(element_num, length, obj)
    #print('payment for combination',payment)
    first = tmp

    #print('printing wild alpha', wild_alpha)#список частот wilds
    #print('printing expand wild alpha', e_wild_alpha)# список частот expand wild




    alls = len(obj.base.symbol)
    combinations = support.combinations2(obj.window[0], bad, alls, wilds, length)
    #print('combinations \n', combinations)
    sec = 0
    for i in range(len(combinations)):
        subst = obj.base.symbol[int(combinations[i,0])].wild.substitute
        subst_l = []
        for j in range(len(subst)):
            tmp = 1
            for p in range(1, length):
                if(obj.base.symbol[int(combinations[i,p])].wild != False):
                    if(subst[j] in obj.base.symbol[int(combinations[i,p])].wild.substitute):
                        tmp += 1
                else:
                    if(subst[j] == int(combinations[i,p])):
                        tmp += 1
            subst_l.append(tmp)
        #print('combinations', combinations[i, ])
        #print('subst', subst)
        #print('subst length', subst_l)
        payments = []
        for j in range(len(subst)):
           # if(obj.symbol[subst[j]].payment[subst_l[j]] > payment):
            payments.append(obj.base.symbol[subst[j]].payment[subst_l[j]])
        if(max(payments) > payment):
            tmp = 1
            j = payments.index(max(payments))
            for p in range(length):
                tmp = tmp*wild_alpha[wilds.index(int(combinations[i,p]))][p]
            tmp2 = 1
            if(length < obj.window[0]):
                tmp2 = (frequency[length][int(combinations[i,length])] - bad_m[bad.index(int(combinations[i,length]))][length])
            tmp = tmp2*tmp
            tmp2 = 1
            for p in range(length + 1, obj.window[0]):
                tmp2 = tmp2*frequency[p][int(combinations[i,p])]
            tmp = tmp*tmp2
            #print(tmp)
            sec += tmp
            #print(subst[j],subst_l[j], obj.symbol[subst[j]].payment[subst_l[j]])
        #print('tmp', tmp)
        #print('sec', sec)

    #print(combinations[0:64, ])
    combinations = support.combinations2(obj.window[0], bad, alls, expands, length)
    #print('combinations \n', combinations)
    third = 0
    for i in range(len(combinations)):
        subst = obj.base.symbol[int(combinations[i,0])].wild.substitute
        subst_l = []
        for j in range(len(subst)):
            tmp = 1
            for p in range(1, length):
                if(obj.base.symbol[int(combinations[i,p])].wild != False):
                    if(subst[j] in obj.base.symbol[int(combinations[i,p])].wild.substitute):
                        tmp += 1
                else:
                    if(subst[j] == int(combinations[i,p])):
                        tmp += 1
            subst_l.append(tmp)
        payments = []
        for j in range(len(subst)):
            # if(obj.symbol[subst[j]].payment[subst_l[j]] > payment):
            payments.append(obj.base.symbol[subst[j]].payment[subst_l[j]])
        if(obj.base.symbol[element_num].wild == False):
            if(max(payments) > payment):
                tmp = 1
                for p in range(length):
                    tmp = 3*tmp*e_wild_alpha[expands.index(int(combinations[i,p]))][p]
                tmp2 = 1
                if(length < obj.window[0]):
                    tmp2 = (frequency[length][int(combinations[i,length])] - bad_m[bad.index(int(combinations[i,length]))][length])
                tmp = tmp2*tmp
                tmp2 = 1
                for p in range(length + 1, object.window[0]):
                    tmp2 = tmp2*frequency[p][int(combinations[i,p])]
                tmp = tmp*tmp2
                #print('tmp is ', tmp)
                third += tmp
        else:
            if(max(payments) >= payment):
                tmp = 1
                for p in range(length):
                    tmp = 3*tmp*e_wild_alpha[expands.index(int(combinations[i,p]))][p]
                tmp2 = 1
                if(length < obj.window[0]):
                    tmp2 = (frequency[length][int(combinations[i,length])] - bad_m[bad.index(int(combinations[i,length]))][length])
                tmp = tmp2*tmp
                tmp2 = 1
                for p in range(length + 1, object.window[0]):
                    tmp2 = tmp2*frequency[p][int(combinations[i,p])]
                tmp = tmp*tmp2
                #print('tmp is ', tmp)
                third += tmp





    #print('bad ', bad)
    #print('bad m ', bad_m)
    #print('expands ', expands)
    print('second = ', sec)
    return(first - sec - third)


#f = open('Front-end/Atilla.txt', 'r')
#f = open(Front-end +"/Atilla.txt", "r")
#text = f.read()
#rules = json.loads(text)
#object = structure_alpha.Game(rules)

#frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]
#frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2, 2, 1, 0]
#frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2, 3, 1, 3]
#frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2, 4, 1, 0]
#frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2, 0, 1, 3]



#frequency_1 = [3, 5, 3, 3, 2, 3, 4, 2, 1, 1, 1, 1, 1]
#frequency_2 = [3, 5, 3, 3, 2, 3, 4, 2, 1, 1, 1, 1, 1]
#frequency_3 = [3, 5, 3, 3, 2, 3, 4, 2, 1, 1, 1, 1, 1]
#frequency_4 = [3, 5, 3, 3, 2, 3, 4, 2, 1, 1, 1, 1, 1]
#frequency_5 = [3, 5, 3, 3, 2, 3, 4, 2, 1, 1, 1, 1, 1]

#frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

#game = reel_generator(frequency, object)

#print_game(game)

#element_number = 3
#length = 5
#line = 3


#print('element = ', object.symbol[element_number].name)

#print(count_combinations(game, line, element_number, length, object))

#print(object.symbol[element_number].base.substituted_by_e)
#print(object.set_of_base_ewilds)


#payment = payment_for_combination(element_number, length, object)

#print(object.symbol[8].payment[length])



