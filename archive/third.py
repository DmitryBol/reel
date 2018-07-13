import numpy as np
import json
#rg = __import__("reel generator")
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q
import time


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


file = open('..\Games\HappyBrauer.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)


frequency_1 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_2 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_3 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_4 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_5 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

bad = True
counter = 0
while bad and counter < 100000:

    obj.base.reel_generator(frequency, obj.window[0])
    obj.free.reel_generator(frequency, obj.window[0])
    obj.base.fill_frequency(frequency)
    obj.free.fill_frequency(frequency)

    bad = False

    for reel in obj.base.reels:
        for symbol_index in range(len(reel)):
            symbol = reel[symbol_index]
            near = []
            for i in range(-obj.window[1] + 1, 0, 1):
                near.append(reel[(symbol_index + i) % len(reel)].name)
            if symbol.name == 'wild' and 'Scat' in near or symbol.name == 'Scat' and 'wild' in near:
                bad = True
    counter += 1
if counter == 100000:
    exit('cant shuffle')

#print_game(obj.base)

print('started')


obj.base.fill_simple_num_comb(obj.window, obj.line)
obj.base.fill_scatter_num_comb(obj.window)
obj.free.fill_simple_num_comb(obj.window, obj.line)
obj.free.fill_scatter_num_comb(obj.window)
print('RTP2 = ', obj.count_base_RTP2('base'))
print('freemean2 = ', obj.freemean2())
#exit(0)
#string = np.array([1., 0., 0., 0., 2.])
#res = obj.base.get_combination(string, 5)
#print(res)

#res = obj.base.count_num_comb(string, [2, 2, 2, 2, 2], [5, 3])
#print(res)

#print(obj.base.scatterlist)
start = time.time()
obj.base.fill_num_comb(obj.window, obj.line)
obj.free.fill_num_comb(obj.window, obj.line)

print('filling ', time.time() - start)

#print(obj.base.num_comb[1][5])

print('All combinations =', obj.base.all_combinations())
LAL = obj.freemean()
print('Freemean =', LAL)
print('Base RTP =', obj.count_baseRTP())
rtp = obj.count_RTP(LAL)
print('RTP =', rtp)
print('Volatility =', obj.count_volatility(LAL, rtp))
print('Hitrate =', obj.count_hitrate())

obj.base.fill_scatter_num_comb(obj.window)
obj.base.fill_simple_num_comb(obj.window, obj.line)

