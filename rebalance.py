import json
import FrontEnd.structure_alpha as Q
import copy
from Descent.Point import Point
from Descent.Split import Split

Inf = 0.025
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005


def double_bouble(a, b):
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                b[i], b[j] = b[j], b[i]


def calc_val(params, point):
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
    return - (point.sdnew - params['sdnew']) * (abs(point.rtp - params['rtp']) + params['err_rtp'])**0.2


# делает "шахматный" порядок с символами i, j
def Chess(frequency, i, j, game, k=1, base=True):
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
            statement1 = new_frequency[reelID][source] - tmp_k_1 < 0
            statement3 = False
            statement4 = False
            statement5 = False
            statement7 = False
            if source in gametype.wildlist:
                statement3 = new_frequency[reelID][source] - tmp_k_1 < wildInf * totals[reelID]
            if source in gametype.ewildlist:
                statement4 = new_frequency[reelID][source] - tmp_k_1 < ewildInf * totals[reelID]
            if source not in gametype.wildlist and source not in gametype.ewildlist and source not in gametype.scatterlist:
                statement5 = new_frequency[reelID][source] - tmp_k_1 < Inf * totals[reelID]
            if source in gametype.scatterlist:
                statement7 = new_frequency[reelID][source] - tmp_k_1 < scatterInf * totals[reelID]
            if statement1 or statement3 or statement4 or statement5 or statement7:
                tmp_k_1 -= 1
                continue
            else:
                break

        # проверка на то, что символы можно положить
        while tmp_k_2 > 0:

            statement2 = new_frequency[reelID][destination] + tmp_k_2 > 0 and reelID not in gametype.symbol[
                destination].position
            statement6 = new_frequency[reelID][destination] + tmp_k_2 > gametype.max_border * totals[reelID]
            if statement2 or statement6:
                tmp_k_2 -= 1
                continue
            else:
                break

        # если можно, то делаем
        new_frequency[reelID][source] -= min(tmp_k_1, tmp_k_2)
        new_frequency[reelID][destination] += min(tmp_k_1, tmp_k_2)
    if new_frequency == frequency:
        print("CAN'T MAKE CHESS ORDER WITH ", i, " AND ", j)
        return frequency
    return new_frequency

def binar_search(game, gamtype, start_point, params, sortedSymbols, i, j, right, left=1):

    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']
    #current_value = calc_val(params, start_point)
    if gamtype.name == 'base':
        left_frequency = Chess(start_point.baseFrequency, sortedSymbols[i], sortedSymbols[j], game, k=left)
        right_frequency = Chess(start_point.baseFrequency, sortedSymbols[i], sortedSymbols[j], game, k=right)

        left_point = Point(left_frequency, start_point.freeFrequency, game)
        right_point = Point(right_frequency, start_point.freeFrequency, game)

        left_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                               sd_flag=False)
        left_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                               sd_flag=True)

        right_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                               sd_flag=False)
        right_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                               sd_flag=True)

        left_val = calc_val(params, left_point)
        right_val = calc_val(params, right_point)
        middle = int((right + left)/2)

        # print('left_val = ', left_val, 'right_val = ', right_val)

        if left_val * right_val >= 0:
            if abs(left_val) < abs(right_val):
                return left
            else:
                return right


        middle_frequency = Chess(start_point.baseFrequency, sortedSymbols[i], sortedSymbols[j], game, k=middle)
        middle_point = Point(middle_frequency, start_point.freeFrequency, game)

        middle_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                             sd_flag=False)
        middle_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                             sd_flag=True)

        middle_val = calc_val(params, middle_point)

        while right - left > 2:
            if middle_val * left_val < 0:
                right = middle
                right_point = middle_point
                right_val = middle_val

            elif middle_val * right_val < 0:
                left = middle
                left_point = right_point
                left_val = middle_val
            else:
                return middle

            middle = (left + right)//2

        return middle

    elif gamtype.name == 'free':

        left_frequency = Chess(start_point.freeFrequency, sortedSymbols[i], sortedSymbols[j], game, k=left, base=False)
        right_frequency = Chess(start_point.freeFrequency, sortedSymbols[i], sortedSymbols[j], game, k=right, base=False)

        left_point = Point(start_point.baseFrequency, left_frequency, game)
        right_point = Point(start_point.baseFrequency, right_frequency, game)

        left_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                             sd_flag=False)
        left_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                             sd_flag=True)

        right_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                              sd_flag=False)
        right_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                              sd_flag=True)

        left_val = calc_val(params, left_point)
        right_val = calc_val(params, right_point)
        middle = int((right + left) / 2)

        if left_val * right_val >= 0:
            if abs(left_val) < abs(right_val):
                return left
            else:
                return right

        while right - left > 2:
            middle_frequency = Chess(start_point.freeFrequency, sortedSymbols[i], sortedSymbols[j], game, k=middle)
            middle_point = Point(start_point.baseFrequency, middle_frequency, game)

            middle_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                                   sd_flag=False)
            middle_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                                   sd_flag=True)

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

    else:
        raise Exception('No such gametype')






def rebalance(start_point, game, gametype, params):
    print('REBALANCE')
    base_rtp = params['base_rtp']
    rtp = params['rtp']
    sdnew = params['sdnew']
    err_base_rtp = params['err_base_rtp']
    err_rtp = params['err_rtp']
    err_sdnew = params['err_sdnew']

    start_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False, sd_flag=True)

    if start_point.F(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False, sd_flag=True) < 1:
        return start_point

    print('during fitting')
    print('base rtp: ', start_point.base_rtp)
    print('rtp: ', start_point.rtp)
    print('sdnew: ', start_point.sdnew)
    print('value: ', start_point.value)
    print(start_point.baseFrequency)

    prev_val = calc_val(params, start_point)
    new_val = copy.deepcopy(prev_val)

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
    double_bouble(val, sortedSymbols)
    print('sorted = ', sortedSymbols, '\n')
    SD = [start_point.sdnew, start_point.base_rtp, start_point.rtp]

    out_point = None
    out_game = None

    for i in range(len(sortedSymbols) - 1):
        for j in range(i + 1, len(sortedSymbols)):
            if gametype.name == 'base':
                list_k = [sum(start_point.baseFrequency[_]) for _ in range(len(start_point.baseFrequency))]
                max_k = max(list_k)
                best_k = binar_search(game, gametype, start_point, params, sortedSymbols, i, j, max_k, 1)
                if best_k == 0:
                    print('\nazaza\n')
                    continue
                new_frequency = Chess(start_point.baseFrequency, sortedSymbols[i], sortedSymbols[j], game, k=best_k)
            else:
                list_k = [sum(start_point.freeFrequency[_]) for _ in range(len(start_point.freeFrequency))]
                max_k = max(list_k)
                best_k = binar_search(game, gametype, start_point, params, sortedSymbols, i, j, max_k, 1)
                if best_k == 0:
                    print('\nazaza\n')
                    continue
                new_frequency = Chess(start_point.freeFrequency, sortedSymbols[i], sortedSymbols[j], game, k=best_k,
                                      base=False)

            if new_frequency == None:
                continue
            else:
                result_point = None
                if gametype.name == 'base':
                    result_point = Point(new_frequency, start_point.freeFrequency, game)
                elif gametype.name == 'free':
                    result_point = Point(start_point.baseFrequency, new_frequency, game)
                else:
                    raise Exception('No such gametype in rebalance')
                result_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True,
                                       sd_flag=False)
                result_point.fillPoint(game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False,
                                       sd_flag=True)
                print('trying to change in ', sortedSymbols[i], ' and ', sortedSymbols[j], ' positions')
                print('base rtp: ', result_point.base_rtp)
                print('rtp: ', result_point.rtp)
                print('sdnew: ', result_point.sdnew)
                print('hitrate: ', result_point.hitrate)
                print('val: ', result_point.value)
                if gametype.name == 'base':
                    print('total = ', sum(result_point.baseFrequency[0]), 'base ', result_point.baseFrequency)
                elif gametype.name == 'free':
                    print('total = ', sum(result_point.freeFrequency[0]), 'free ', result_point.freeFrequency)
                print('\n')
                new_val = calc_val(params, result_point)
                print('prev_val: ', prev_val, 'new_val: ', new_val)
                if abs(new_val) < abs(prev_val):
                    prev_val = new_val
                    SD = [result_point.sdnew, result_point.base_rtp, result_point.rtp]
                    out_point = copy.deepcopy(result_point)
                    out_game = copy.deepcopy(game)
                    print('\nChanging result\n')

    print('BEST SD IS ', SD[0])
    print('with base_rtp: ', SD[1], 'rtp: ', SD[2])
    if out_game is None:
        out_game = game
    if out_point is None:
        out_point = start_point
    return [out_point, out_game]
