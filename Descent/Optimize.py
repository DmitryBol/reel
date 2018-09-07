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

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005

scaleLimit = 5


def double_bouble(a, b):
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

#параметр rebalance отвечает за сбаланировку групп псоле перекидываний элементов

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
    double_bouble(value_list, index_list)
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
                        # findedMin.printBaseReel(file_name)
                        break
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
    double_bouble(value_list, index_list)
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
                        break
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
