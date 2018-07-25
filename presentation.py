import neighborhood as descent
import random

all_games = ['Games\Attila.txt', 'Games\Garage.txt', 'Games\HappyBrauer.txt', 'Games\Shining_Crown.txt',
             'Games\Space Odyssey.txt']
hit_rates = [random.gauss(180, 20) for _ in all_games]
L = len(all_games)

for index in range(L):
    descent.SecondMethod(hit_rates[index], 1, all_games[index])
    print(all_games[index] + ' done\n\n\n')
