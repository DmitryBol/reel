import random
import json
free = [10,1,1,1,1,1,1,1,1,1,1]#массивы частот
base = [1,1,1,1,1,1,1,1,1,1,1]

class reel_generator(object):
    def __init__(self, array, names):
        tmp = []
        for i in range(len(array)):
            for j in range(array[i]):
                tmp.append(names[i]['name'])
        self.ReelStrip = tmp
        reel_1 = tmp.copy()
        reel_2 = tmp.copy()
        reel_3 = tmp.copy()
        reel_4 = tmp.copy()
        reel_5 = tmp.copy()
        self.len = len(tmp)
        random.shuffle(reel_1)
        random.shuffle(reel_2)
        random.shuffle(reel_3)
        random.shuffle(reel_4)
        random.shuffle(reel_5)
        self.reels = [reel_1, reel_2, reel_3, reel_4, reel_5]
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
def counting_combinations(symbol_name, line_number, length_of_sequence, rules):
    line = rules['lines'][line_number]
    name = symbol_name
    unique = list(set(line))
    counter = 0
    length = length_of_sequence
    if(len(unique) == 1):
        for j in range(game.len):
            if(game.reels[0][j] == name):
                print('on raw number our combination ', j)
                tmp = 1
                for k in range(1,length):
                    if(game.reels[k][j] == name):
                        tmp += 1
                if(tmp == length):
                    counter += 1
                print(tmp, length)
    if(len(unique) == 2):
        if(line[0] == min(line)):
            for j in range(game.len - 1):
                if(game.reels[0][j] == name):
                    tmp = 1
                    for k in range(1,length):
                        if(game.reels[k][j + line[k] - line[0]] == name):
                            tmp += 1
                    if(tmp == length):
                        print('on raw number our combination', j)
                        counter += 1
        elif(line[0] == max(line)):
            for j in range(1, game.len):
                if(game.reels[0][j] == name):
                    tmp = 1
                    for k in range(1,length):
                        if(game.reels[k][j + line[k] - line[0]] == name):
                            tmp += 1
                    if(tmp == length):
                        print('on raw number our combination ', j)
                        counter += 1
    if(len(unique) == 3):
        if(line[0] == min(line)):
            for j in range(game.len - 2):
                if(game.reels[0][j] == name):
                    tmp = 1
                    for k in range(1,length):
                        if(game.reels[k][j + line[k] - line[0]] == name):
                            tmp += 1
                    if(tmp == length):
                        print('on raw number our combination', j)
                        counter += 1
        elif(line[0] == max(line)):
            for j in range(2, game.len):
                if(game.reels[0][j] == name):
                    tmp = 1
                    for k in range(1,length):
                        if(game.reels[k][j + line[k] - line[0]] == name):
                            tmp += 1
                    if(tmp == length):
                        print('on raw number our combination ', j)
                        counter += 1
        else:
            for j in range(1, game.len - 1):
                if(game.reels[0][j] == name):
                    tmp = 1
                    for k in range(1,length):
                        if(game.reels[k][j + line[k] - line[0]] == name):
                            tmp += 1
                    if(tmp == length):
                        print('on raw number our combination ', j)
                        counter += 1
    print(line)
    #print(unique)
    return(counter)
#первая переменная - строка, имя символа, вторая - номер линии, 3 - длина куска линии, 4 - структура полученная с помощью json


f = open('Shining_Crown.txt', 'r')
text = f.read()
rules = json.loads(text)

game = reel_generator(free, rules['symbol'])



print_game(game)

counter = counting_combinations(rules['symbol'][0]['name'], 7, 3, rules)

print('counter is ', counter)