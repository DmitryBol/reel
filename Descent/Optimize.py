import simple_functions_for_fit as sm
import copy
from Descent.Point import Point
from Descent.Groups import Group
from FrontEnd.structure_alpha import Game
from Descent.parameters_utils import get_parameters_from_dict

Inf = 0.025
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005

scaleLimit = 5


def double_bubble(a, b):
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                b[i], b[j] = b[j], b[i]
    return


def get_blocked_symbols(window_width, symbols):
    blocked_symbols = []
    for reel_id in range(window_width):
        blocked_symbols.append([])
        for symbol_id in range(len(symbols)):
            if reel_id not in symbols[symbol_id].position:
                blocked_symbols[reel_id].append(symbol_id)
    return blocked_symbols


def create_initial_frequency(game, blocked_symbols, total, numb_of_scatters, used_symbols_cnt, base_frequency,
                             blocked_scatters, initial, free_frequency, main_symbol, type_flag):
    used_symbols_count = used_symbols_cnt - 1
    if main_symbol in blocked_scatters:
        return

    for reel_id in range(game.window[0]):
        if type_flag == 'middle':
            base_frequency[reel_id][main_symbol] = (total - numb_of_scatters[reel_id]) // (
                    used_symbols_count - len(blocked_symbols[reel_id]))
        elif type_flag == 'max':
            base_frequency[reel_id][main_symbol] = int(game.base.max_border * total)
        elif type_flag == 'min':
            base_frequency[reel_id][main_symbol] = int(game.base.infPart(main_symbol) * total) + 1
        else:
            raise Exception('No such type for initial distribution')

        partition_frequency = (total - numb_of_scatters[reel_id] - base_frequency[reel_id][main_symbol]) // (
                used_symbols_count - len(blocked_symbols[reel_id]))
        ost = (total - numb_of_scatters[reel_id] - base_frequency[reel_id][main_symbol]) % (
                used_symbols_count - len(blocked_symbols[reel_id]))
        for symbol_id in range(len(game.base.symbol)):
            if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [main_symbol]:
                base_frequency[reel_id][symbol_id] = partition_frequency
        counter = 0
        symbol_id = 0
        while counter < ost:
            if symbol_id not in blocked_scatters + blocked_symbols[reel_id] + [main_symbol]:
                base_frequency[reel_id][symbol_id] += 1
                counter += 1
            symbol_id += 1

    initial.append(Point(main_frequency=base_frequency, second_frequency=free_frequency, game=game, main_type='base'))


def fresh_free_scatters(free_frequency, scatterlist, free_symbols, window_width, max_len):
    for scatter_id in scatterlist:
        if max(free_symbols[scatter_id].scatter) > 0:
            for reel_id in range(window_width):
                if reel_id in free_symbols[scatter_id].position:
                    free_frequency[reel_id][scatter_id] = max(1, int(scatterInf * max_len))
                else:
                    free_frequency[reel_id][scatter_id] = 0
    return


def initial_base_distributions(game: Game, scatter_frequency_result, params, max_len=100):
    free_frequency = [[max_len // len(game.free.symbol) for _ in range(len(game.free.symbol))] for _ in
                      range(game.window[0])]

    fresh_free_scatters(free_frequency=free_frequency, scatterlist=game.free.scatterlist, free_symbols=game.free.symbol,
                        window_width=game.window[0], max_len=max_len)

    base_frequency = [[0 for _ in range(len(game.base.symbol))] for _ in range(game.window[0])]
    numb_of_scatters = []
    for reel_id in range(game.window[0]):
        numb_of_scatters.append(0)
        for j in range(len(game.base.scatterlist)):
            scatter_id = game.base.scatterlist[j]
            base_frequency[reel_id][scatter_id] = scatter_frequency_result.scatter_index_with_frequency[scatter_id]
            numb_of_scatters[reel_id] += base_frequency[reel_id][scatter_id]

    initial = []
    total = scatter_frequency_result.total_length
    game_symbols_count = len(game.base.symbol)

    blocked_scatters = []
    for scatter_id in game.base.scatterlist:
        if max(game.base.symbol[scatter_id].scatter) > 0:
            blocked_scatters.append(scatter_id)
    used_symbols_count = game_symbols_count - len(blocked_scatters)

    blocked_symbols = get_blocked_symbols(window_width=game.window[0], symbols=game.base.symbol)

    main_symbol = 0
    for symbol_id in range(len(game.base.symbol)):
        if symbol_id not in blocked_scatters and any(
                [symbol_id not in blocked_symbols[reel_id] for reel_id in range(game.window[0])]):
            main_symbol = symbol_id
            break
    create_initial_frequency(game=game, blocked_symbols=blocked_symbols, total=total,
                             numb_of_scatters=numb_of_scatters, used_symbols_cnt=used_symbols_count,
                             base_frequency=base_frequency, blocked_scatters=blocked_scatters, initial=initial,
                             free_frequency=free_frequency, main_symbol=main_symbol, type_flag='middle')

    for symbol_id in range(len(game.base.symbol)):
        create_initial_frequency(game=game, blocked_symbols=blocked_symbols, total=total,
                                 numb_of_scatters=numb_of_scatters, used_symbols_cnt=used_symbols_count,
                                 base_frequency=base_frequency, blocked_scatters=blocked_scatters, initial=initial,
                                 free_frequency=free_frequency, main_symbol=symbol_id, type_flag='max')

        create_initial_frequency(game=game, blocked_symbols=blocked_symbols, total=total,
                                 numb_of_scatters=numb_of_scatters, used_symbols_cnt=used_symbols_count,
                                 base_frequency=base_frequency, blocked_scatters=blocked_scatters, initial=initial,
                                 free_frequency=free_frequency, main_symbol=symbol_id, type_flag='min')

    counter = 1
    # TODO убрать slice
    for point in initial[:1]:
        point.fill_point(game, params)
        print('end point ', counter, point.base.frequency, point.value)
        counter += 1
    return initial[:1]


def initial_free_distributions(game, base_frequency, free_frequency, params, base_reels=None):
    initial = []

    freeFrequencyCopy = sm.notice_positions(free_frequency, game.free)
    baseFrequencyCopy = sm.notice_positions(base_frequency, game.base)
    initial.append(
        Point(second_frequency=baseFrequencyCopy, main_frequency=freeFrequencyCopy, game=game, main_type='free',
              base_reels=base_reels))

    for point in initial:
        point.fill_point(game, params, base=False, sd_flag=False, base_shuffle=False, free_shuffle=True)

    return initial


# параметр balance отвечает за балансировку групп после перекидываний элементов

def descent_base(params, game, balance=True, start_point=None):
    base_rtp, rtp, sdnew, hitrate, err_base_rtp, err_rtp, err_sdnew, err_hitrate = get_parameters_from_dict(params)

    start_game = copy.deepcopy(game)

    out = sm.get_scatter_frequency(game, hitrate, err_hitrate)
    print('Generated scatter frequency')
    if out == -1 and hitrate != -1:
        raise Exception('Game rules not contain freespins, but you try to fit HitRate. Please, set it -1')
    elif out == -1:
        out = sm.OutResult(game.base.scatterlist)
        out.add_symbols(game.base.symbol)

    blocked_scatters = []
    for scatter_id in game.base.scatterlist:
        if max(game.base.symbol[scatter_id].scatter) > 0:
            blocked_scatters.append(scatter_id)

    print('started base descent')
    game.base.create_simple_num_comb(game.window, game.line)
    game.free.create_simple_num_comb(game.window, game.line)
    print('created_num_comb')

    roots = []
    if start_point is None:
        roots = initial_base_distributions(game, out, params)
    else:
        roots.append(start_point)
    finded_min = Point(main_frequency=roots[0].base.frequency, second_frequency=roots[0].free.frequency, game=game,
                       main_type='base')
    print('INITIAL POINTS, THEIR DISTRIBUTIONS, VALUES AND PARAMETERS:')

    value_list = []
    for root in roots:
        # root.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
        print(root.base.frequency, ' value is ', root.value, 'base_rtp, rtp, sdnew, hitrate :',
              root.base_rtp, root.rtp, root.sdnew, root.hitrate)
        value_list = value_list + [root.value]
    index_list = list(range(len(value_list)))
    double_bubble(value_list, index_list)
    print('assuming base rtp, rtp, sd ', base_rtp, rtp, sdnew)
    print('assuming errors for base rtp, rtp,  sd ', err_base_rtp, err_rtp, err_sdnew)

    # print(value_list)
    index_list.remove(0)
    index_list = [0] + index_list

    for index in index_list:
        print('TRYING POINT', roots[index].base.frequency,
              ' value is ', roots[index].value,
              'base_rtp, rtp, sdnew, hitrate :',
              roots[index].base_rtp, roots[index].rtp, roots[index].sdnew, roots[index].hitrate)
        root = roots[index]

        currentScale = 0
        while currentScale < scaleLimit:
            number_of_groups = len(game.base.wildlist) + len(game.base.ewildlist) + \
                               len(game.base.scatterlist) - len(blocked_scatters) + 1
            max_number_of_groups = len(game.base.symbol) - len(blocked_scatters)
            while number_of_groups <= max_number_of_groups:
                temp_group = Group(game, 'base', root, number_of_groups, params, rebalance=balance, sd_flag=False)
                print('groups ', temp_group.split.groups)

                temp_group.print_group()

                finded_min = temp_group.find_best_point()
                if finded_min != -1:
                    if finded_min.value < 1:
                        print('ending with ', finded_min.value)
                        print('base ', finded_min.base_rtp)
                        print('rtp ', finded_min.rtp)
                        print('sdnew ', finded_min.sdnew)
                        print('hitrate ', finded_min.hitrate)
                        root = copy.deepcopy(finded_min)
                        print(root.base.frequency)
                        game.base.reels = copy.deepcopy(finded_min.base.reels)
                        game.free.reels = copy.deepcopy(finded_min.free.reels)
                        finded_min.fill_point_metric(params)
                        return [finded_min, game]
                    else:
                        print('path ', finded_min.value)
                        root = copy.deepcopy(finded_min)
                else:
                    if 0.5 * max_number_of_groups < number_of_groups < max_number_of_groups:
                        number_of_groups = max_number_of_groups
                    else:
                        number_of_groups += 1

            root.scaling()
            currentScale += 1
            print('SCALING ', currentScale)

    print('Base done')

    if finded_min == -1:
        return [start_point, start_game]

    finded_min.fill_point(game, params, base=False, sd_flag=True, base_shuffle=False, free_shuffle=False)

    return [finded_min, game]


def descent_free(params, start_point: Point, game, balance=True):
    base_rtp, rtp, sdnew, hitrate, err_base_rtp, err_rtp, err_sdnew, err_hitrate = get_parameters_from_dict(params)

    print('started free descent')

    # print('start point base reels: ', start_point.base.reels)

    if rtp == -1:
        return [start_point, game]

    roots = initial_free_distributions(game, start_point.base.frequency, start_point.free.frequency, params,
                                       base_reels=start_point.base.reels)
    finded_min = Point(second_frequency=roots[0].base.frequency, main_frequency=roots[0].free.frequency, game=game,
                       main_type='free', base_reels=start_point.base.reels)
    finded_min.base.reels = start_point.base.reels

    value_list = []
    for root in roots:
        print(root.free.frequency, ' value is ', root.value, 'base_rtp, rtp, sdnew, hitrate :',
              root.base_rtp, root.rtp, root.sdnew, root.hitrate)
        value_list = value_list + [root.value]

    index_list = list(range(len(value_list)))
    double_bubble(value_list, index_list)
    print('assuming base rtp, rtp, sd ', base_rtp, rtp, sdnew)
    print('assuming errors for base rtp, rtp,  sd ', err_base_rtp, err_rtp, err_sdnew)

    index_list.remove(0)
    index_list = [0] + index_list

    for index in index_list:
        print('TRYING POINT', roots[index].free.frequency,
              ' value is ', roots[index].value,
              'base_rtp, rtp, sdnew, hitrate :',
              roots[index].base_rtp, roots[index].rtp, roots[index].sdnew, roots[index].hitrate)
        root = roots[index]

        currentScale = 0
        while currentScale < scaleLimit:
            number_of_groups = len(game.free.wildlist) + len(game.free.ewildlist) + \
                               len(game.free.scatterlist) + 1
            max_number_of_groups = len(game.base.symbol)
            while number_of_groups <= max_number_of_groups:
                temp_group = Group(game, 'free', root, number_of_groups, params, rebalance=balance, sd_flag=False,
                                   base_reels=start_point.base.reels)
                print('groups ', temp_group.split.groups)

                temp_group.print_group('free')

                finded_min = temp_group.find_best_point()
                if finded_min != -1:
                    if finded_min.value < 1:
                        print('ending with ', finded_min.value)
                        print('base ', finded_min.base_rtp)
                        print('rtp ', finded_min.rtp)
                        print('sdnew ', finded_min.sdnew)
                        print('hitrate ', finded_min.hitrate)
                        root = copy.deepcopy(finded_min)
                        print(root.free.frequency)
                        finded_min.fill_point_metric(params, base=False, sd_flag=False)
                        finded_min.base.reels = copy.deepcopy(start_point.base.reels)
                        return [finded_min, game]
                    else:
                        print('path ', finded_min.value)
                        root = copy.deepcopy(finded_min)
                else:
                    if 0.5 * max_number_of_groups < number_of_groups < max_number_of_groups:
                        number_of_groups = max_number_of_groups
                    else:
                        number_of_groups += 1
            root.scaling()
            currentScale += 1
            print('SCALING ', currentScale)

    print('Free done')

    finded_min.fill_point(game, params, base=False, sd_flag=True, base_shuffle=False, free_shuffle=False)
    finded_min.base.reels = copy.deepcopy(start_point.base.reels)

    return [finded_min, game]
