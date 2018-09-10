from Descent.Optimize import Descent_free, Descent_base
import simulate
from rebalance import rebalance


def print_res(out, point, game_name):
    out.write('Game: ' + str(game_name) + '\n')
    out.write('Base RTP:' + str(point.base_rtp) + ', RTP:' + str(point.rtp) + ', SD:' + str(point.sdnew))


all_games = ['Games/HappyBrauer.txt']

L = len(all_games)

params = {'base_rtp': 0.65,
          'rtp': 0.95,
          'sdnew': 25,
          'hitrate': 160,
          'err_base_rtp': 0.01,
          'err_rtp': 0.01,
          'err_sdnew': 3,
          'err_hitrate': 1}

rebalance_count = 0
MAX_REBALANCE_COUNT = 5
out = open('out.txt', 'w')

for index in range(L):
    prev_value = -1
    free_mode = params['hitrate'] > 0

    current_point, game = Descent_base(file_name=all_games[index], params=params)
    if free_mode:
        current_point, game = Descent_free(game=game, params=params, start_point=current_point)

    print('REBALANCE BASE')
    current_point, game = rebalance(current_point, game, game.base, params=params)
    if current_point.getValue() < 1:
        print_res(out, current_point, all_games[index])
        continue
    if free_mode:
        print('REBALANCE FREE')
        # print(current_point.freeFrequency)
        current_point, game = rebalance(current_point, game, game.free, params=params)
    if current_point.getValue() < 1:
        print_res(out, current_point, all_games[index])
        continue

    rebalance_count += 1
    current_value = current_point.getValue()

    while rebalance_count < MAX_REBALANCE_COUNT:
        current_point, game = Descent_base(file_name=all_games[index], params=params, rebalance=False,
                                           start_point=current_point)
        if free_mode:
            current_point, game = Descent_free(game=game, params=params, start_point=current_point, rebalance=False)

        # print('\n\n\n\n\n\nCurrent frequency:\n', current_point.freeFrequency)
        # exit('printed')

        current_point, game = rebalance(current_point, game, game.base, params=params)
        if current_point.getValue() < 1:
            break
        if free_mode:
            current_point, game = rebalance(current_point, game, game.free, params=params)
        if current_point.getValue() < 1:
            break

        prev_value = current_value
        current_value = current_point.getValue()

        if current_value == prev_value:
            current_point.scaling(base=True)
            current_point.scaling(base=False)

        rebalance_count += 1

    if current_point.getValue() < 1:
        print_res(out, current_point, all_games[index])
        continue

    current_point, game = Descent_base(file_name=all_games[index], params=params, rebalance=False,
                                       start_point=current_point)

    if free_mode:
        current_point, game = Descent_free(game=game, params=params, start_point=current_point, rebalance=False)

    current_point.fillPoint(game, params['base_rtp'], params['rtp'], params['sdnew'], params['err_base_rtp'], params['err_rtp'], params['err_sdnew'], base=False, sd_flag=True)

    print('Base RTP:', current_point.base_rtp, 'RTP:', current_point.rtp, 'SD:', current_point.sdnew)

    print_res(out, current_point, all_games[index])

    print(all_games[index] + ' done\n\n\n')
    # simulate_result = simulate.make_spins(game, count=1_000_000)
    # print('simulate rtp: ', simulate_result['rtp'], '\tsimulate sd: ', simulate_result['sd'])


