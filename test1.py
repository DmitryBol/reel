import numpy as np
import json
import FrontEnd.structure_alpha as Q
import time
from simulate import make_spins
from simulate import greedy_simulate
import math

file = open('Games/PrinceOfPersia.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

frequency = [
    [0, 3, 4, 6, 6, 8, 8, 12, 14, 15, 16, 16],
    [0, 3, 4, 6, 6, 8, 8, 12, 14, 15, 16, 16],
    [0, 3, 4, 6, 6, 8, 8, 12, 14, 15, 16, 16],
    [0, 3, 4, 6, 6, 8, 8, 12, 14, 15, 16, 16],
    [0, 3, 4, 6, 6, 8, 8, 12, 14, 15, 16, 16]
]

game.base.fill_frequency(frequency)
game.free.fill_frequency(frequency)

game.base.reel_generator(game.base.frequency, game.window[0], game.distance, validate=True)
game.free.reel_generator(game.free.frequency, game.window[0], game.distance, validate=True)

print('{')
for reel in game.base.reels:
    s = '{'
    for symbol in reel:
        s += str(symbol) + ', '
    s = s[:-2] + '},'
    print(s)
print('},')

game.base.create_simple_num_comb(game.window, game.line)
game.free.create_simple_num_comb(game.window, game.line)

game.base.create_simple_num_comb(game.window, game.line)
game.base.fill_scatter_num_comb(game.window)
game.base.fill_count_killed(game.window[0])
game.base.fill_simple_num_comb(game.window, game.line)

game.free.create_simple_num_comb(game.window, game.line)
game.free.fill_scatter_num_comb(game.window)
game.free.fill_count_killed(game.window[0])
game.free.fill_simple_num_comb(game.window, game.line)

print(game.base.scatter_num_comb[0])

print(game.freemean2(game.line))
print('base rtp: ', game.count_base_RTP2('base', game.line))
print(game.count_RTP2(game.freemean2(game.line), game.count_base_RTP2('base', game.line)))
print(game.count_hitrate2())

# print(make_spins(game))
