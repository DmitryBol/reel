import neighborhood as descent
import random

all_games = ['Games\Shining_Crown.txt',
             'Games\Katana.txt',
             'Games\Attila.txt',
             'Games\Garage.txt',
             'Games\Space Odyssey.txt',
             'Games\HappyBrauer.txt'
             ]

hit_rates = [random.gauss(180, 20) for _ in all_games]
all_base_rtp = [0.65 for _ in all_games]
index = all_games.index('Games\Shining_Crown.txt')
hit_rates[index] = -1
all_base_rtp[index] = 0.95
L = len(all_games)

for index in range(L):
    descent.SecondMethod(file_name=all_games[index],
                         hitrate=hit_rates[index],
                         err_hitrate=1,
                         base_rtp=all_base_rtp[index],
                         err_base_rtp=0.001
                         )
    print(all_games[index] + ' done\n\n\n')
