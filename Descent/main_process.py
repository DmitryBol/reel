import time
import json
import copy

from Descent.Optimize import descent_base, descent_free
from Descent.rebalance import rebalance
from FrontEnd.reelWork.reel_generator_alpha import indexes_to_names
from FrontEnd.structure_alpha import Game
from Descent.Point import Point


def print_res(out, point: Point, game_name, game):
    out.write('Game: ' + str(game_name) + '\n')
    out.write('Base RTP:' + str(point.base_rtp) + ', RTP:' + str(point.rtp) + ', SD:' + str(point.sdnew))
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


def create_plot(plot_name, point: Point, game):
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
        print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')
        print_res(out_log, current_point, game_name, game)
        create_plot(plot_name, current_point, game)
        return True
    return False


def main_process(game_name, out_log, max_rebalance_count, plot_name):
    file = open(game_name, 'r')
    j = file.read()
    interim = json.loads(j)
    game = Game(interim)
    file.close()
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
        return
    if free_mode:
        print('REBALANCE FREE')
        # print(current_point.freeFrequency)
        current_point, game = rebalance(current_point, game, game.free, params=params)
    if is_done(current_point, start_time, game_name, game, out_log, plot_name):
        return

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
            return

        prev_value = current_value
        current_value = current_point.get_value()

        if current_value == prev_value:
            current_point.scaling(base=True)
            current_point.scaling(base=False)

        rebalance_count += 1

    if is_done(current_point, start_time, game_name, game, out_log, plot_name):
        return

    current_point, game = descent_base(params=params, game=game, balance=False, start_point=current_point)

    if free_mode:
        current_point, game = descent_free(game=game, params=params, start_point=current_point, balance=False)

    current_point.collect_params()

    print('Base RTP:', current_point.base_rtp, 'RTP:', current_point.rtp, 'SD:', current_point.sdnew, 'Hitrate: ',
          current_point.hitrate)

    print_res(out_log, current_point, game_name, game)
    create_plot(plot_name, current_point, game)

    spend_time = time.time() - start_time
    hours = int(spend_time / 60 / 60)
    mins = int((spend_time - hours * 3600) / 60)
    sec = int(spend_time - hours * 3600 - mins * 60)

    print(game_name + ' done in ' + str(hours) + 'h ' + str(mins) + 'min ' + str(sec) + 'sec')

    return
