import time
import json
import copy

from Descent.Optimize import descent_base, descent_free
from Descent.rebalance import rebalance
from FrontEnd.reelWork.reel_generator_alpha import indexes_to_names
from Descent.Point import Point


def print_res(out, point: Point, game_name, game):
    out.write('Game: ' + str(game_name) + '\n')
    out.write('Base RTP: ' + str(point.base_rtp) + '\nRTP: ' + str(point.rtp) + '\nSD: ' + str(
        point.sdnew) + '\nBonus Hitrate: ' + str(point.hitrate))
    out.write('\n\nReels\n')
    out.write('base:\n')
    reels_cnt = len(point.base.reels)

    names = indexes_to_names(game.base.symbol, point.base.reels)
    for reel_id in range(reels_cnt):
        out.write('\t{')
        reel_len = len(names[reel_id])
        for index in range(reel_len - 1):
            out.write(names[reel_id][index] + ', ')
        out.write(names[reel_id][reel_len - 1] + '}\n')
    out.write('free:\n')
    reels_cnt = len(point.free.reels)

    names = indexes_to_names(game.free.symbol, point.free.reels)
    for reel_id in range(reels_cnt):
        out.write('\t{')
        reel_len = len(names[reel_id])
        for index in range(reel_len - 1):
            out.write(names[reel_id][index] + ', ')
        out.write(names[reel_id][reel_len - 1] + '}\n')

    out.write('\n\nJava Reels\n')
    out.write('base:\n')
    out.write('{//base\n')
    for reel_id in range(reels_cnt):
        out.write('\t{')
        reel_len = len(point.base.reels[reel_id])
        for index in range(reel_len - 1):
            out.write(str(point.base.reels[reel_id][index] + 1) + ', ')
        out.write(str(point.base.reels[reel_id][reel_len - 1] + 1) + '},\n')
    out.write('}\n')
    out.write('free:\n')
    out.write('{//free\n')
    for reel_id in range(reels_cnt):
        out.write('\t{')
        reel_len = len(point.free.reels[reel_id])
        for index in range(reel_len - 1):
            out.write(str(point.free.reels[reel_id][index] + 1) + ', ')
        out.write(str(point.free.reels[reel_id][reel_len - 1] + 1) + '},\n')
    out.write('}\n')


def create_plot(plot_name, point: Point, game):
    if plot_name is None:
        return
    temp_game = copy.deepcopy(game)
    temp_game.base.frequency = copy.deepcopy(point.base.frequency)
    temp_game.free.frequency = copy.deepcopy(point.free.frequency)
    temp_game.base.reels = copy.deepcopy(point.base.reels)
    temp_game.free.reels = copy.deepcopy(point.free.reels)

    temp_game.fill_borders(plot_name)
    return


def is_done(current_point, start_time, game_name, game, out_log, plot_name):
    if current_point.get_value() < 1:
        spend_time = time.time() - start_time
        hours = int(spend_time / 60 / 60)
        mins = int((spend_time - hours * 3600) / 60)
        sec = int(spend_time - hours * 3600 - mins * 60)
        print(str(game_name) + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
        print_res(out_log, current_point, game_name, game)
        create_plot(plot_name, current_point, game)

        # simulate_result = simulate.make_spins(game, count=1_000_000)
        # print('\n\nsimulate base rtp: ', simulate_result['base_rtp'], '\nsimulate rtp: ', simulate_result['rtp'],
        #       '\nsimulate sd: ', simulate_result['sd'])
        return True
    return False


def main_process(out_log, max_rebalance_count=5, plot_name=None, game_structure=None, game_name=None):
    if game_name is not None:
        file = open(game_name, 'r')
        j = file.read()
        interim = json.loads(j)
        # game = Game(interim)
        file.close()
    elif game_structure is not None:
        game = copy.deepcopy(game_structure)
    else:
        raise Exception('There is no structure Game or rules file for main process')
    params = {'rtp': game.RTP[0], 'err_rtp': game.RTP[1], 'base_rtp': game.baseRTP[0], 'err_base_rtp': game.baseRTP[1],
              'sdnew': game.volatility[0], 'err_sdnew': game.volatility[1], 'hitrate': game.hitrate[0],
              'err_hitrate': game.hitrate[1]}

    rebalance_count = 0
    start_time = time.time()
    free_mode = params['hitrate'] > 0

    current_point, game = descent_base(params, game, balance=True)
    if free_mode:
        current_point, game = descent_free(game=game, params=params, start_point=current_point)

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
    if is_done(current_point, start_time, game_name, game, out_log, plot_name):
        return game
    if free_mode:
        print('REBALANCE FREE')
        # print(current_point.freeFrequency)
        current_point, game = rebalance(current_point, game, game.free, params=params)
    if is_done(current_point, start_time, game_name, game, out_log, plot_name):
        return game

    rebalance_count += 1
    current_value = current_point.get_value()

    while rebalance_count < max_rebalance_count:
        current_point, game = descent_base(params=params, game=game, balance=False, start_point=current_point)
        if free_mode:
            current_point, game = descent_free(game=game, params=params, start_point=current_point, balance=False)

        current_point, game = rebalance(start_point=current_point, game=game, gametype=game.base, params=params)
        if free_mode:
            current_point, game = rebalance(current_point, game, game.free, params=params)
        if is_done(current_point, start_time, game_name, game, out_log, plot_name):
            return game

        prev_value = current_value
        current_value = current_point.get_value()

        if current_value == prev_value:
            current_point.scaling(base=True)
            current_point.scaling(base=False)

        rebalance_count += 1

    if is_done(current_point, start_time, game_name, game, out_log, plot_name):
        return game

    current_point, game = descent_base(params=params, game=game, balance=False, start_point=current_point)

    if free_mode:
        current_point, game = descent_free(game=game, params=params, start_point=current_point, balance=False)

    current_point.collect_params()

    print('Base RTP:', current_point.base_rtp, 'RTP:', current_point.rtp, 'SD:', current_point.sdnew, 'Hitrate: ',
          current_point.hitrate)

    if game_structure is not None:
        game_structure.base.reels = copy.deepcopy(game.base.reels)
        game_structure.free.reels = copy.deepcopy(game.free.reels)
    print_res(out_log, current_point, game_name, game)
    create_plot(plot_name, current_point, game)

    spend_time = time.time() - start_time
    hours = int(spend_time / 60 / 60)
    mins = int((spend_time - hours * 3600) / 60)
    sec = int(spend_time - hours * 3600 - mins * 60)

    print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')

    return game
