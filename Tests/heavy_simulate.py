import numpy as np
import json
import FrontEnd.structure_alpha as Q
import time
from simulate import make_spins
from simulate import greedy_simulate
import math


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


for counter in range(5):
    print(reels[counter])

total_cnt = 1
for reel in reels:
    total_cnt *= len(reel)
print('total_cnt: ', total_cnt)


file = open('/home/amvasylev/PycharmProjects/reel/Games/Shining Crown.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

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

print('frequency:')
for cnt in range(len(frequency)):
    print(frequency[cnt])


game.base.frequency = frequency
game.base.reels = reels

game.base.create_simple_num_comb(game.window, game.line)
game.base.fill_scatter_num_comb(game.window)
game.base.fill_count_killed(game.window[0])
game.base.fill_simple_num_comb(game.window, game.line)

b_rtp = game.count_base_RTP2('base', game.line)
freemean = game.freemean2(game.line)
params = game.count_parameters(base=False, sd_flag=True)

sd_alpha = params['sdold']
sd_beta = params['sdnew']

dict = make_spins(game=game, count=100)


print('theoretical: ', sd_alpha, 'first: ', sd_beta, '\treal: ', dict['sd'])
