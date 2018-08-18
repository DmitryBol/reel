import Descent.Optimize as descent
import random

all_games = ['Games\Shining_Crown.txt']


L = len(all_games)

if None:
    print('Diman prav')

params = {'base_rtp': 0.95,
          'rtp': 0.95,
          'sdnew': 4,
          'hitrate': -1,
          'err_base_rtp': 0.01,
          'err_rtp': 0.01,
          'err_sdnew': 0.5,
          'err_hitrate': 1}

for index in range(L):
    basePoint, game = descent.Descent_base(file_name=all_games[index],
                                     params=params)
    if params['hitrate'] > 0:
        freePoint = descent.Descent_free(game=game,
                                     params=params,
                                     start_point=basePoint)
    print(all_games[index] + ' done\n\n\n')
