from simulate import fillMatrix
import FrontEnd.structure_alpha as Q
import json
import numpy as np
import time

CROWN = 8
DOLLAR = 9
STAR = 10


def take_win(game, gametype, matrix):
    res = 0

    for i in range(gametype.window[1]):
        for j1 in range(gametype.window[0]):
            if matrix[i, j1] in gametype.ewildlist:
                for k in range(gametype.window[1]):
                    matrix[k, j1] = matrix[i, j1]

    for line in game.line:
        line_symbols = []
        for index in range(len(line)):
            line_symbols.append(matrix[line[index] - 1, index])
        symbol = line_symbols[0]
        if symbol == DOLLAR or symbol == STAR:
            continue
        cnt = 1
        for reel_id in range(1, len(line)):
            if line_symbols[reel_id] == symbol or line_symbols[reel_id] == CROWN:
                cnt += 1
            else:
                break
        res += gametype.symbol[int(symbol)].payment[cnt]

    cnt_dollar = 0
    cnt_star = 0
    for i in range(3):
        for j in range(5):
            if matrix[i, j] == DOLLAR:
                cnt_dollar += 1
            if matrix[i, j] == STAR:
                cnt_star += 1
    res += gametype.symbol[DOLLAR].payment[cnt_dollar] * len(game.line)
    res += gametype.symbol[STAR].payment[cnt_star] * len(game.line)

    return res


file = open('/home/amvasylev/PycharmProjects/reel/Games/Shining Crown.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
gametype = game.base
file.close()

reels = [[], [], [], [], []]
reels_file = open('/home/amvasylev/PycharmProjects/reel/Games/reels.txt')
for line in reels_file:
    symbols = line.split(',')
    for counter in range(len(symbols)):
        symbol = symbols[counter]
        if 'Seven' in symbol:
            reels[counter].append(0)
        elif 'Melon' in symbol:
            reels[counter].append(1)
        elif 'Cherry' in symbol:
            reels[counter].append(2)
        elif 'Lemon' in symbol:
            reels[counter].append(3)
        elif 'Grape' in symbol:
            reels[counter].append(4)
        elif 'Bell' in symbol:
            reels[counter].append(5)
        elif 'Plum' in symbol:
            reels[counter].append(6)
        elif 'Orange' in symbol:
            reels[counter].append(7)
        elif 'Crown' in symbol:
            reels[counter].append(8)
        elif 'Dollar' in symbol:
            reels[counter].append(9)
        elif 'Star' in symbol:
            reels[counter].append(10)


frequency = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
for reel_id in range(5):
    for symbol in reels[reel_id]:
        frequency[reel_id][symbol] += 1

game.base.frequency = frequency
game.base.reels = reels

game.base.create_simple_num_comb(game.window, game.line)
game.base.fill_scatter_num_comb(game.window)
game.base.fill_count_killed(game.window[0])
game.base.fill_simple_num_comb(game.window, game.line)

b_rtp = game.count_base_RTP2('base')




total_cnt = 1
for reel in reels:
    total_cnt = total_cnt * len(reel)

total_sum = 0
counter = 0
matrix = np.zeros((3, 5))
lens = [len(reels[i]) for i in range(len(reels))]

start_time = time.time()
for index0 in range(lens[0]):
    for index1 in range(lens[1]):
        for index2 in range(lens[2]):
            for index3 in range(lens[3]):
                for index4 in range(lens[4]):
                    indexes = [index0, index1, index2, index3, index4]
                    fillMatrix(gametype, matrix, reels, indexes, 3)
                    win = take_win(game, gametype, matrix)
                    total_sum += win
                    counter += 1
        print('{0}% done, current rtp: {1}%, cuurent time: {2}'.format(str(round(counter / total_cnt * 100, 4)),
                                                                       str(round(total_sum / counter / len(
                                                                           game.line) * 100, 2)),
                                                                       time.time() - start_time))
print('rtp = ', total_sum / counter / len(game.line) * 100, '%')
print('b_rtp = ', str(b_rtp*100) + '%')
