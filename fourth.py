import archive.test_file as tf
import json
import FrontEnd.structure_alpha as Q
import time

tf.func1()

file = open('Games\HappyBrauer.txt', 'r')
j = file.read()

interim = json.loads(j)

obj = Q.Game(interim)

#print(obj.base.count_killed[0][0])

start_time = time.time()

frequency_1 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_2 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_3 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_4 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]
frequency_5 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 16, 4]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

obj.base.reel_generator(frequency, obj.window[0], obj.distance)
obj.free.reel_generator(frequency, obj.window[0], obj.distance)
obj.base.fill_frequency(frequency)
obj.free.fill_frequency(frequency)

print('started')

time1 = time.time()

time_killed = time.time()
obj.base.fill_count_killed(obj.window[0])
print('base count killed: ', round(time.time() - time_killed, 2), ' seconds')
time_simple = time.time()
obj.base.fill_simple_num_comb(obj.window, obj.line)
print('base simple num comb: ', round(time.time() - time_simple, 2), ' seconds')
time_scatter = time.time()
obj.base.fill_scatter_num_comb(obj.window)
print('base scatter num comb: ', round(time.time() - time_scatter, 2), 'seconds')

obj.free.fill_count_killed(obj.window[0])
obj.free.fill_simple_num_comb(obj.window, obj.line)
obj.free.fill_scatter_num_comb(obj.window)

time2 = time.time()

print('All combinations =', obj.base.all_combinations())
base_rtp = obj.count_base_RTP2('base')
print('Base RTP = ', base_rtp)
freemean = obj.freemean2()
print('FreeMean = ', freemean)
rtp = obj.count_RTP2(freemean, base_rtp)
print('RTP = ', rtp)
sd = obj.count_volatility2(freemean, rtp)
print('RTP SD = ', sd)
sdnew = obj.count_volatility2new(freemean, rtp)
print('RTP SD new = ', sdnew)
hitrate = obj.count_hitrate2()
print('Hitrate = ', hitrate)

print('filling: ', round(time2 - time1, 2), ' seconds')
print('functions: ', round(time.time() - time2, 2), ' seconds')
