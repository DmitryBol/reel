import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np
from Descent.Point import Point
from Descent.Split import Split
from Descent.Groups import Group
from simple_functions_for_fit import notice_positions
from Descent.rebalance import rebalance
from FrontEnd.reelWork.reel_generator_alpha import name_by_index
from FrontEnd.reelWork.reel_generator_alpha import indexes_to_names

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005

scaleLimit = 5


class Reels:
    def __init__(self, game, base_frequency, free_frequency, base_reels=None, free_reels=None):
        self.base = copy.deepcopy(base_reels)
        self.free = copy.deepcopy(free_reels)
        temp_game = copy.deepcopy(game)
        if base_reels is None:
            temp_game.base.reel_genertor(base_frequency, temp_game.window[0], temp_game.window[1])
            self.base = copy.deepcopy(temp_game.base.reels)
        if free_reels is None:
            temp_game.free.reel_genertor(free_frequency, temp_game.window[0], temp_game.window[1])
            self.free = copy.deepcopy(temp_game.free.reels)


def double_bubble(a, b):
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                b[i], b[j] = b[j], b[i]


def initialDistributions(obj, out, params):
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']

    freeFrequency = [[int(300 / len(obj.free.symbol)) for _ in range(len(obj.free.symbol))] for _ in
                     range(obj.window[0])]

    for scatter_id in obj.free.scatterlist:
        if max(obj.free.symbol[scatter_id].scatter) > 0:
            for reel_id in range(obj.window[0]):
                freeFrequency[reel_id][scatter_id] = max(1, int(scatterInf * 300))

    baseFrequency = [[0 for _ in range(len(obj.base.symbol))] for _ in range(obj.window[0])]
    numb_of_scatters = []
    for reel_id in range(obj.window[0]):
        numb_of_scatters.append(0)
        for j in range(len(obj.base.scatterlist)):
            scatter_id = obj.base.scatterlist[j]
            baseFrequency[reel_id][scatter_id] = out.scatter_index_with_frequency[scatter_id]
            numb_of_scatters[reel_id] += baseFrequency[reel_id][scatter_id]

    initial = []
    total = out.total_length
    n_symbols = len(obj.base.symbol)

    blocked_scatters = []
    for scatter_id in obj.base.scatterlist:
        if max(obj.base.symbol[scatter_id].scatter) > 0:
            blocked_scatters.append(scatter_id)
    n_symbols -= len(blocked_scatters)

    blocked_symbols = []
    for reel_id in range(obj.window[0]):
        blocked_symbols.append([])
        for symbol_id in range(len(obj.base.symbol)):
            if reel_id not in obj.base.symbol[symbol_id].position:
                blocked_symbols[reel_id].append(symbol_id)
        k = (total - numb_of_scatters[reel_id]) // (n_symbols - len(blocked_symbols[reel_id]))
        ost = (total - numb_of_scatters[reel_id]) % (n_symbols - len(blocked_symbols[reel_id]))
        for symbol_id in range(len(obj.base.symbol)):
            if symbol_id not in blocked_symbols[reel_id] and symbol_id not in blocked_scatters:
                baseFrequency[reel_id][symbol_id] = k
        counter = 0
        symbol_id = 0
        while counter < ost:
            if symbol_id not in blocked_symbols[reel_id] and symbol_id not in blocked_scatters:
                baseFrequency[reel_id][symbol_id] += 1
                counter += 1
            symbol_id += 1

    initial.append(Point(baseFrequency, freeFrequency, obj))

    n_symbols -= 1
    for i in range(len(obj.base.symbol)):
        if i in blocked_scatters:
            continue
        for reel_id in range(obj.window[0]):
            baseFrequency[reel_id][i] = int(obj.base.max_border * total)
            k = (total - numb_of_scatters[reel_id] - baseFrequency[reel_id][i]) // (
                    n_symbols - len(blocked_symbols[reel_id]))
            ost = (total - numb_of_scatters[reel_id] - baseFrequency[reel_id][i]) % (
                    n_symbols - len(blocked_symbols[reel_id]))
            for symbol_id in range(len(obj.base.symbol)):
                if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [i]:
                    baseFrequency[reel_id][symbol_id] = k
            counter = 0
            symbol_id = 0
            while counter < ost:
                if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [i]:
                    baseFrequency[reel_id][symbol_id] += 1
                    counter += 1
                symbol_id += 1
        initial.append(Point(baseFrequency, freeFrequency, obj))

        for reel_id in range(obj.window[0]):
            baseFrequency[reel_id][i] = int(obj.base.infPart(i) * total) + 1
            k = (total - numb_of_scatters[reel_id] - baseFrequency[reel_id][i]) // (
                    n_symbols - len(blocked_symbols[reel_id]))
            ost = (total - numb_of_scatters[reel_id] - baseFrequency[reel_id][i]) % (
                    n_symbols - len(blocked_symbols[reel_id]))
            for symbol_id in range(len(obj.base.symbol)):
                if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [i]:
                    baseFrequency[reel_id][symbol_id] = k
            counter = 0
            symbol_id = 0
            while counter < ost:
                if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [i]:
                    baseFrequency[reel_id][symbol_id] += 1
                    counter += 1
                symbol_id += 1
        initial.append(Point(baseFrequency, baseFrequency, obj))

    counter = 1
    # TODO убрать slice
    for point in initial[:1]:
        point.fillPoint(obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
        print('end point ', counter, point.baseFrequency, point.value)
        counter += 1
    return initial[:1]


def initialFreeDistributions(obj, baseFrequency, freeFrequency, params):
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']

    initial = []

    freeFrequencyCopy = sm.notice_positions(freeFrequency, obj.free)
    baseFrequencyCopy = sm.notice_positions(baseFrequency, obj.base)
    initial.append(Point(baseFrequencyCopy, freeFrequencyCopy, obj))
    for p in initial:
        p.fillPoint(obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False, sd_flag=False)

    return initial


# параметр rebalance отвечает за сбаланировку групп псоле перекидываний элементов

def Descent_base(params, file_name, rebalance=True, start_point=None):
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']
    hitrate = params['hitrate']
    err_hitrate = params['err_hitrate']

    file = open(file_name, 'r')
    j = file.read()
    interim = json.loads(j)
    game = Q.Game(interim)
    file.close()

    out = sm.get_scatter_frequency(file_name, hitrate, err_hitrate)
    if out == -1 and hitrate != -1:
        raise Exception('Game rules not contain freespins, but you try to fit HitRate. Please, set it -1')
    elif out == -1:

        out = sm.OutResult(game.base.scatterlist)
        out.add_symbols(game.base.symbol)
    blocked_scatters = []
    for scatter_id in game.base.scatterlist:
        if max(game.base.symbol[scatter_id].scatter) > 0:
            blocked_scatters.append(scatter_id)

    print('started')
    game.base.create_simple_num_comb(game.window, game.line)
    game.free.create_simple_num_comb(game.window, game.line)
    print('created_num_comb')

    roots = []
    if start_point == None:
        roots = initialDistributions(game, out, params)
    else:
        roots.append(start_point)
    findedMin = Point(frequency_base=roots[0].baseFrequency, frequency_free=roots[0].freeFrequency, game=game)
    print('INITIAL POINTS, THEIR DISTRIBUTIONS, VALUES AND PARAMETRES:')

    value_list = []
    for root in roots:
        # root.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
        print(root.baseFrequency, ' value is ', root.value, 'base_rtp, rtp, sdnew, hitrate :',
              root.base_rtp, root.rtp, root.sdnew, root.hitrate)
        value_list = value_list + [root.value]
    index_list = list(range(len(value_list)))
    double_bubble(value_list, index_list)
    print('assuming base rtp, rtp, sd ', base_rtp, rtp, sdnew)
    print('assuming errors for base rtp, rtp,  sd ', err_base_rtp, err_rtp, err_sdnew)

    # print(value_list)
    index_list = [0] + index_list

    for index in index_list:
        print('TRYING POINT', roots[index].baseFrequency,
              ' value is ', roots[index].value,
              'base_rtp, rtp, sdnew, hitrate :',
              roots[index].base_rtp, roots[index].rtp, roots[index].sdnew, roots[index].hitrate)
        root = roots[index]

        min_is_found = False
        currentScale = 0
        while not min_is_found and currentScale < scaleLimit:
            number_of_groups = len(game.base.wildlist) + len(game.base.ewildlist) + \
                               len(game.base.scatterlist) - len(blocked_scatters) + 1
            max_number_of_groups = len(game.base.symbol) - len(blocked_scatters)
            while number_of_groups <= max_number_of_groups:
                temp_group = Group(game, 'base', root, number_of_groups, params, rebalance=rebalance)
                print('groups ', temp_group.split.groups)

                temp_group.printGroup()

                findedMin = temp_group.findMin()
                if findedMin != -1:
                    if findedMin.value < 1:
                        min_is_found = True
                        print('ending with ', findedMin.value)
                        print('base ', findedMin.base_rtp)
                        print('rtp ', findedMin.rtp)
                        print('sdnew ', findedMin.sdnew)
                        print('hitrate ', findedMin.hitrate)
                        root = copy.deepcopy(findedMin)
                        print(root.baseFrequency)
                        game.base.reels = copy.deepcopy(findedMin.baseReel)
                        game.free.reels = copy.deepcopy(findedMin.freeReel)
                        findedMin.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
                        return [findedMin, game]
                    else:
                        print('path ', findedMin.value)
                        root = copy.deepcopy(findedMin)
                else:

                    if number_of_groups > 0.5 * max_number_of_groups and number_of_groups < max_number_of_groups:
                        number_of_groups = max_number_of_groups
                    else:
                        number_of_groups += 1

            if not min_is_found:
                root.scaling()
                currentScale += 1
                print('SCALING ', currentScale)
            else:
                break
        if min_is_found:
            break

    print('Base done')

    findedMin.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)

    return [findedMin, game]


def Descent_free(params, start_point, game, rebalance=True):
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']
    hitrate = params['hitrate']
    err_hitrate = params['err_hitrate']

    print('started_free')

    roots = initialFreeDistributions(game, start_point.baseFrequency, start_point.freeFrequency, params)
    findedMin = Point(frequency_base=roots[0].baseFrequency, frequency_free=roots[0].freeFrequency, game=game)

    value_list = []
    for root in roots:
        print(root.freeFrequency, ' value is ', root.value, 'base_rtp, rtp, sdnew, hitrate :',
              root.base_rtp, root.rtp, root.sdnew, root.hitrate)
        value_list = value_list + [root.value]

    index_list = list(range(len(value_list)))
    double_bubble(value_list, index_list)
    print('assuming base rtp, rtp, sd ', base_rtp, rtp, sdnew)
    print('assuming errors for base rtp, rtp,  sd ', err_base_rtp, err_rtp, err_sdnew)

    index_list = [0] + index_list

    for index in index_list:
        print('TRYING POINT', roots[index].freeFrequency,
              ' value is ', roots[index].value,
              'base_rtp, rtp, sdnew, hitrate :',
              roots[index].base_rtp, roots[index].rtp, roots[index].sdnew, roots[index].hitrate)
        root = roots[index]

        min_is_found = False
        currentScale = 0
        while not min_is_found and currentScale < scaleLimit:
            number_of_groups = len(game.free.wildlist) + len(game.free.ewildlist) + \
                               len(game.free.scatterlist) + 1
            max_number_of_groups = len(game.base.symbol)
            while number_of_groups <= max_number_of_groups:
                temp_group = Group(game, 'free', root, number_of_groups, params, rebalance=rebalance)
                print('groups ', temp_group.split.groups)

                temp_group.printGroup('free')

                findedMin = temp_group.findMin()
                if findedMin != -1:
                    if findedMin.value < 1:
                        min_is_found = True
                        print('ending with ', findedMin.value)
                        print('base ', findedMin.base_rtp)
                        print('rtp ', findedMin.rtp)
                        print('sdnew ', findedMin.sdnew)
                        print('hitrate ', findedMin.hitrate)
                        root = copy.deepcopy(findedMin)
                        print(root.freeFrequency)
                        findedMin.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False)
                        return [findedMin, game]
                    else:
                        print('path ', findedMin.value)
                        root = copy.deepcopy(findedMin)
                else:
                    if number_of_groups > 0.5 * max_number_of_groups and number_of_groups < max_number_of_groups:
                        number_of_groups = max_number_of_groups
                    else:
                        number_of_groups += 1
            if not min_is_found:
                root.scaling()
                currentScale += 1
                print('SCALING ', currentScale)
            else:
                break
        if min_is_found:
            break

    print('Free done')

    findedMin.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False)

    return [findedMin, game]


def print_res(out, point, game_name, game):
    out.write('Game: ' + str(game_name) + '\n')
    out.write('Base RTP:' + str(point.base_rtp) + ', RTP:' + str(point.rtp) + ', SD:' + str(point.sdnew))
    out.write('\n\nReels\n')
    out.write('base:\n')
    reels_cnt = len(point.baseReel)

    names = indexes_to_names(game.base.symbol, point.baseReel)
    for reel_id in range(reels_cnt):
        out.write('\t{')
        reel_len = len(names[reel_id])
        for index in range(reel_len - 1):
            out.write(names[reel_id][index] + ', ')
        out.write(names[reel_id][reel_len - 1] + '}\n')


def create_plot(plot_name, point, game):
    temp_game = copy.deepcopy(game)
    temp_game.base.frequency = copy.deepcopy(point.baseFrequency)
    temp_game.free.frequency = copy.deepcopy(point.freeFrequency)
    temp_game.base.reels = copy.deepcopy(point.baseReel)
    temp_game.free.reels = copy.deepcopy(point.freeReel)

    temp_game.fill_borders(plot_name)
    return


def main_process(game_name, out_log, max_rebalance_count, plot_name):

    file = open(game_name, 'r')
    j = file.read()
    interim = json.loads(j)
    game = Q.Game(interim)
    file.close()
    params = {'rtp': game.RTP[0], 'err_rtp': game.RTP[1], 'base_rtp': game.baseRTP[0], 'err_base_rtp': game.baseRTP[1],
              'sdnew': game.volatility[0], 'err_sdnew': game.volatility[1], 'hitrate': game.hitrate[0],
              'err_hitrate': game.hitrate[1]}

    rebalance_count = 0
    start_time = time.time()
    prev_value = -1
    free_mode = params['hitrate'] > 0

    current_point, game = Descent_base(file_name=game_name, params=params)
    if free_mode:
        current_point, game = Descent_free(game=game, params=params, start_point=current_point)

    current_point.collect_params(game)
    default_SD = current_point.sdnew
    print('default_SD: ', default_SD)
    min_SD = default_SD * 0.95
    if free_mode:
        max_SD = default_SD * 1.25
    else:
        max_SD = default_SD * 1.90
    if params['sdnew'] < min_SD or params['sdnew'] > max_SD:
        exception_str = 'This SD is not compatible with current RTP, base RTP. Please, select SD between ' + str(
            round(min_SD, 2)) + ' and ' + str(round(max_SD, 2))
        raise Exception(exception_str)

    print('REBALANCE BASE')
    current_point, game = rebalance(current_point, game, game.base, params=params)
    if current_point.getValue() < 1:
        spend_time = time.time() - start_time
        hours = int(spend_time / 60 / 60)
        mins = int((spend_time - hours * 3600) / 60)
        sec = int(spend_time - hours * 3600 - mins * 60)
        print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
        print_res(out_log, current_point, game_name, game)
        create_plot(plot_name, current_point, game)
        return
    if free_mode:
        print('REBALANCE FREE')
        # print(current_point.freeFrequency)
        current_point, game = rebalance(current_point, game, game.free, params=params)
    if current_point.getValue() < 1:
        spend_time = time.time() - start_time
        hours = int(spend_time / 60 / 60)
        mins = int((spend_time - hours * 3600) / 60)
        sec = int(spend_time - hours * 3600 - mins * 60)
        print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
        print_res(out_log, current_point, game_name, game)
        create_plot(plot_name, current_point, game)
        return

    rebalance_count += 1
    current_value = current_point.getValue()

    while rebalance_count < max_rebalance_count:
        current_point, game = Descent_base(file_name=game_name, params=params, rebalance=False,
                                           start_point=current_point)
        if free_mode:
            current_point, game = Descent_free(game=game, params=params, start_point=current_point, rebalance=False)

        # print('\n\n\n\n\n\nCurrent frequency:\n', current_point.freeFrequency)
        # exit('printed')

        current_point, game = rebalance(current_point, game, game.base, params=params)
        if current_point.getValue() < 1:
            spend_time = time.time() - start_time
            hours = int(spend_time / 60 / 60)
            mins = int((spend_time - hours * 3600) / 60)
            sec = int(spend_time - hours * 3600 - mins * 60)
            print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
            break
        if free_mode:
            current_point, game = rebalance(current_point, game, game.free, params=params)
        if current_point.getValue() < 1:
            spend_time = time.time() - start_time
            hours = int(spend_time / 60 / 60)
            mins = int((spend_time - hours * 3600) / 60)
            sec = int(spend_time - hours * 3600 - mins * 60)
            print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
            break

        prev_value = current_value
        current_value = current_point.getValue()

        if current_value == prev_value:
            current_point.scaling(base=True)
            current_point.scaling(base=False)

        rebalance_count += 1

    if current_point.getValue() < 1:
        spend_time = time.time() - start_time
        hours = int(spend_time / 60 / 60)
        mins = int((spend_time - hours * 3600) / 60)
        sec = int(spend_time - hours * 3600 - mins * 60)
        print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
        print_res(out_log, current_point, game_name, game)
        create_plot(plot_name, current_point, game)
        return

    current_point, game = Descent_base(file_name=game_name, params=params, rebalance=False,
                                       start_point=current_point)

    if free_mode:
        current_point, game = Descent_free(game=game, params=params, start_point=current_point, rebalance=False)

    # current_point.fillPoint(game, params['base_rtp'], params['rtp'], params['sdnew'], params['err_base_rtp'], params['err_rtp'], params['err_sdnew'], base=False, sd_flag=True)

    current_point.collect_params()

    print('Base RTP:', current_point.base_rtp, 'RTP:', current_point.rtp, 'SD:', current_point.sdnew)

    print_res(out_log, current_point, game_name, game)
    create_plot(plot_name, current_point, game)

    spend_time = time.time() - start_time
    hours = int(spend_time / 60 / 60)
    mins = int((spend_time - hours * 3600) / 60)
    sec = int(spend_time - hours * 3600 - mins * 60)

    print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')

    return
