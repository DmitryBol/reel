import copy
from Descent.Point import Point
from Descent.Optimize import double_bubble

Inf = 0.015
wildInf = 0.015
ewildInf = 0.01
scatterInf = 0.005


def calc_val(params, point: Point):
    if params['rtp'] == -1:
        return point.sdnew ** 1.5 / point.base_rtp - (params['sdnew']) ** 1.5 / params['base_rtp']
    return point.sdnew ** 1.5 / point.rtp - (params['sdnew']) ** 1.5 / params['rtp']


def calc_val_bad(params, point):
    if abs(point.rtp - params['rtp']) < params['err_rtp']:
        return (point.sdnew - params['sdnew']) / point.rtp
    else:
        if point.rtp < params['rtp']:
            return point.sdnew / point.rtp - params['sdnew'] / (params['rtp'] - params['err_rtp'])
        else:
            return point.sdnew / point.rtp - params['sdnew'] / (params['rtp'] + params['err_rtp'])


def calc_val_old(params, point):
    return - (point.sdnew - params['sdnew']) * (abs(point.rtp - params['rtp']) + params['err_rtp']) ** 0.2


def cant_take(source_frequency, swap_count, source, gametype, total_on_reel):
    statement1 = source_frequency - swap_count < 0
    statement3 = False
    statement4 = False
    statement5 = False
    statement7 = False
    if source in gametype.wildlist:
        statement3 = source_frequency - swap_count < wildInf * total_on_reel
    if source in gametype.ewildlist:
        statement4 = source_frequency - swap_count < ewildInf * total_on_reel
    if source not in gametype.wildlist and source not in gametype.ewildlist and source not in gametype.scatterlist:
        statement5 = source_frequency - swap_count < Inf * total_on_reel
    if source in gametype.scatterlist:
        statement7 = source_frequency - swap_count < scatterInf * total_on_reel
    return statement1 or statement3 or statement4 or statement5 or statement7


def cant_put(destination_frequency, swap_count, reel_id, gametype, destination, total_on_reel):
    statement2 = destination_frequency + swap_count > 0 and reel_id not in gametype.symbol[
        destination].position
    statement6 = destination_frequency + swap_count > gametype.max_border * total_on_reel
    return statement2 or statement6


# делает "шахматный" порядок с символами i, j
def chess(frequency, i, j, game, k=1, base=True):
    new_frequency = copy.deepcopy(frequency)
    if base:
        gametype = game.base
    else:
        gametype = game.free
    totals = [sum(_) for _ in frequency]
    for reelID in range(len(new_frequency)):
        if reelID % 2 == 0:
            source = i
            destination = j
        else:
            source = j
            destination = i
        tmp_k_1 = copy.deepcopy(k)
        tmp_k_2 = copy.deepcopy(k)
        # проверка на то, что символы можно забрать
        while tmp_k_1 > 0:
            if cant_take(source_frequency=new_frequency[reelID][source], swap_count=tmp_k_1, source=source,
                         gametype=gametype, total_on_reel=totals[reelID]):
                tmp_k_1 -= 1
            else:
                break

        # проверка на то, что символы можно положить
        while tmp_k_2 > 0:
            if cant_put(destination_frequency=new_frequency[reelID][destination], swap_count=tmp_k_2, reel_id=reelID,
                        gametype=gametype, destination=destination, total_on_reel=totals[reelID]):
                tmp_k_2 -= 1
            else:
                break

        # если можно, то делаем
        new_frequency[reelID][source] -= min(tmp_k_1, tmp_k_2)
        new_frequency[reelID][destination] += min(tmp_k_1, tmp_k_2)
    if new_frequency == frequency:
        print("CAN'T MAKE CHESS ORDER WITH ", i, " AND ", j)
        return frequency
    return new_frequency


def binary_search(game, gametype, start_point: Point, params, sorted_symbols, i, j, right, left=1):
    if gametype.name == 'base':
        main_frequency = start_point.base.frequency
        second_frequency = start_point.free.frequency
    elif gametype.name == 'free':
        main_frequency = start_point.free.frequency
        second_frequency = start_point.base.frequency
    else:
        raise Exception('No such gametype for binary_search')

    left_frequency = chess(main_frequency, sorted_symbols[i], sorted_symbols[j], game, k=left)
    right_frequency = chess(main_frequency, sorted_symbols[i], sorted_symbols[j], game, k=right)

    left_point = Point(main_frequency=left_frequency, second_frequency=second_frequency, game=game,
                       main_type=gametype.name)
    right_point = Point(main_frequency=right_frequency, second_frequency=second_frequency, game=game,
                        main_type=gametype.name)

    left_point.fill_point(game, params, base=True, sd_flag=False)
    left_point.fill_point(game, params, base=False, sd_flag=True)

    right_point.fill_point(game, params, base=True, sd_flag=False)
    right_point.fill_point(game, params, base=False, sd_flag=True)

    left_val = calc_val(params, left_point)
    right_val = calc_val(params, right_point)
    middle = (right + left) // 2

    while right - left > 2:
        middle_frequency = chess(main_frequency, sorted_symbols[i], sorted_symbols[j], game, k=middle)
        middle_point = Point(main_frequency=middle_frequency, second_frequency=second_frequency, game=game,
                             main_type=gametype.name)

        middle_point.fill_point(game, params, base=True, sd_flag=False)
        middle_point.fill_point(game, params, base=False, sd_flag=True)

        middle_val = calc_val(params, middle_point)

        if middle_val * left_val < 0:
            right = middle
            right_val = middle_val

        elif middle_val * right_val < 0:
            left = middle
            left_val = middle_val
        else:
            return middle

        middle = (left + right) // 2

    return middle


def rebalance(start_point: Point, game, gametype, params):
    print('REBALANCE')

    print('\n\n\n')
    print(params['base_rtp'], params['rtp'], params['sdnew'])
    print(start_point.base_rtp, start_point.rtp, start_point.sdnew)
    print('metric: ', start_point.metric(params, base=False, sd_flag=True))

    if start_point.metric(params, base=False, sd_flag=True) < 1:
        return [start_point, game]

    print('during fitting')
    print('base rtp: ', start_point.base_rtp)
    print('rtp: ', start_point.rtp)
    print('sdnew: ', start_point.sdnew)
    print('value: ', start_point.value)
    print(start_point.base.frequency)

    prev_val = calc_val(params, start_point)

    blocked_scatters = []
    if gametype.name == 'base':
        for scatter_id in gametype.scatterlist:
            if max(gametype.symbol[scatter_id].scatter) > 0:
                blocked_scatters.append(scatter_id)
    sortedSymbols = []
    val = []
    for i in range(len(gametype.symbol)):
        if i not in blocked_scatters and i not in gametype.wildlist and i not in gametype.ewildlist:
            sortedSymbols.append(i)
            val.append(gametype.symbol[i].payment[game.window[0]])
    double_bubble(val, sortedSymbols)
    print('sorted = ', sortedSymbols, '\n')
    SD = [start_point.sdnew, start_point.base_rtp, start_point.rtp]

    out_point = None
    out_game = None

    for i in range(len(sortedSymbols) - 1):
        for j in range(i + 1, len(sortedSymbols)):
            if gametype.name == 'base':
                list_k = [sum(start_point.base.frequency[_]) for _ in range(len(start_point.base.frequency))]
                max_k = max(list_k)
                best_k = binary_search(game, gametype, start_point, params, sortedSymbols, i, j, max_k, 1)
                if best_k == 0:
                    print('\nazaza\n')
                    continue
                new_frequency = chess(start_point.base.frequency, sortedSymbols[i], sortedSymbols[j], game, k=best_k)
            elif gametype.name == 'free':
                list_k = [sum(start_point.free.frequency[_]) for _ in range(len(start_point.free.frequency))]
                max_k = max(list_k)
                best_k = binary_search(game, gametype, start_point, params, sortedSymbols, i, j, max_k, 1)
                if best_k == 0:
                    print('\nazaza\n')
                    continue
                new_frequency = chess(start_point.free.frequency, sortedSymbols[i], sortedSymbols[j], game, k=best_k,
                                      base=False)
            else:
                raise Exception('No such gametype for rebalance')

            if new_frequency is None:
                continue
            else:
                if gametype.name == 'base':
                    result_point = Point(new_frequency, start_point.free.frequency, game)
                elif gametype.name == 'free':
                    result_point = Point(start_point.base.frequency, new_frequency, game)
                else:
                    raise Exception('No such gametype in rebalance')
                result_point.fill_point(game, params, base=True, sd_flag=False)
                result_point.fill_point(game, params, base=False, sd_flag=True)
                print('trying to change in ', sortedSymbols[i], ' and ', sortedSymbols[j], ' positions')
                print('base rtp: ', result_point.base_rtp)
                print('rtp: ', result_point.rtp)
                print('sdnew: ', result_point.sdnew)
                print('hitrate: ', result_point.hitrate)
                print('val: ', result_point.value)
                if gametype.name == 'base':
                    print('total = ', sum(result_point.base.frequency[0]), 'base ', result_point.base.frequency)
                elif gametype.name == 'free':
                    print('total = ', sum(result_point.free.frequency[0]), 'free ', result_point.free.frequency)
                print('\n')
                new_val = calc_val(params, result_point)
                print('prev_val: ', prev_val, 'new_val: ', new_val)
                if abs(new_val) < abs(prev_val):
                    prev_val = new_val
                    SD = [result_point.sdnew, result_point.base_rtp, result_point.rtp]
                    out_point = copy.deepcopy(result_point)
                    out_game = copy.deepcopy(game)
                    if out_point.metric(params, base=False, sd_flag=True) < 1:
                        return [out_point, game]

                    print('\nChanging result\n')

    print('BEST SD IS ', SD[0])
    print('with base_rtp: ', SD[1], 'rtp: ', SD[2])
    if out_game is None:
        out_game = game
    if out_point is None:
        out_point = start_point
    return [out_point, out_game]
