from Descent.Optimize import Descent_free, Descent_base
import simulate
from rebalance import rebalance

all_games = ['Games\HappyBrauer.txt']

L = len(all_games)


params = {'base_rtp': 0.65,
          'rtp': 0.95,
          'sdnew': 10,
          'hitrate': 160,
          'err_base_rtp': 0.01,
          'err_rtp': 0.01,
          'err_sdnew': 1,
          'err_hitrate': 1}

for index in range(L):
    basePoint, game = Descent_base(file_name=all_games[index],
                                   params=params)
    if params['hitrate'] > 0:
        freePoint, game = Descent_free(game=game,
                                       params=params,
                                       start_point=basePoint)
        print('REBALANCE BASE')
        rebalance(freePoint, game, game.base, params=params)

        print('REBALANCE FREE')
        print(freePoint.freeFrequency)
        rebalance(freePoint, game, game.free, params=params)


    print(all_games[index] + ' done\n\n\n')
    #simulate_result = simulate.make_spins(game, count=1_000_000)
    #print('simulate rtp: ', simulate_result['rtp'], '\tsimulate sd: ', simulate_result['sd'])
