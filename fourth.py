#import archive.test_file as tf
import json
import FrontEnd.structure_alpha as Q
import time

start_time = time.time()

frequency_1 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]
frequency_2 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]
frequency_3 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]
frequency_4 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]
frequency_5 = [5, 6, 6, 6, 6, 6, 14, 16, 16, 16, 16, 4]

frequency = [frequency_1, frequency_2, frequency_3, frequency_4, frequency_5]

FILES = ['Games\Garage.txt', 'Games\HappyBrauer.txt', 'Games\Katana.txt', 'Games\Attila.txt']

for sees in FILES:
    for i in range(10):
        start_time = time.time()
        file = open(sees, 'r')
        j = file.read()

        interim = json.loads(j)

        obj = Q.Game(interim)
        obj.deleteline(i)

        obj.base.reel_generator(frequency, obj.window[0], obj.distance)
        obj.free.reel_generator(frequency, obj.window[0], obj.distance)
        obj.base.fill_frequency(frequency)
        obj.free.fill_frequency(frequency)

        obj.base.fill_count_killed(obj.window[0])
        obj.base.create_simple_num_comb(obj.window, obj.line)
        obj.base.fill_simple_num_comb(obj.window, obj.line)
        obj.base.fill_scatter_num_comb(obj.window)

        obj.free.fill_count_killed(obj.window[0])
        obj.free.create_simple_num_comb(obj.window, obj.line)
        obj.free.fill_simple_num_comb(obj.window, obj.line)
        obj.free.fill_scatter_num_comb(obj.window)

        param = obj.count_parameters()
        print('FILE: ', sees, 10 - i, 'lines')
        print(round(param['rtp'], 4), ' / ', round(param['sd'], 4), ' / ', round(param['sdnew'], 4), ' / ', round(param['sdalpha'], 4))
        print('time: ', round(time.time() - start_time, 4))
        print('')
        file.close()
