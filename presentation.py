import Descent.Optimize as descent
import random

all_games = [
             'Games\HappyBrauer.txt'
             ]


L = len(all_games)

params = {'base_rtp': 0.65,
          'rtp': 0.95,
          'sdnew': 4,
          'hitrate': 160,
          'err_base_rtp': 0.01,
          'err_rtp': 0.01,
          'err_sdnew': 0.5,
          'err_hitrate': 1}

for index in range(L):
    descent.Descent(file_name=all_games[index],
                    params=params
                         )
    print(all_games[index] + ' done\n\n\n')
