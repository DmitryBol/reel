import json
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q
import time

file = open('HappyBrauer.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

start_time = time.time()

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
print('started')



obj.base.fill_simple_num_comb(obj.window, obj.line)
obj.base.fill_scatter_num_comb(obj.window)
obj.free.fill_simple_num_comb(obj.window, obj.line)
obj.free.fill_scatter_num_comb(obj.window)

print('All combinations =', obj.base.all_combinations())
base_rtp = obj.count_base_RTP2('base')
print('Base RTP = ', base_rtp)
freemean = obj.freemean2()
print('FreeMean = ', freemean)
rtp = obj.count_RTP2(freemean, base_rtp)
print('RTP = ', rtp)
sd = obj.count_volatility2(freemean, rtp)
print('RTP SD = ', sd)
hitrate = obj.count_hitrate2()
print('Hitrate = ', hitrate)

print(time.time() - start_time)
