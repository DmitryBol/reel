import numpy as np
from simulate import take_win
import FrontEnd.structure_alpha as Q
import json
from simulate import scatter_payment
from simulate import make_spins

def reformate(matrix):
    res = [[], [], []]
    dict = {'Seven': 0,
            'Melon': 1,
            'Cherry': 2,
            'Lemon': 3,
            'Grape': 4,
            'Bell': 5,
            'Plum': 6,
            'Orange': 7,
            'Crown': 8,
            'Dollar': 9,
            'Star': 10
            }
    for index in range(3):
        for symbol in matrix[index]:
            res[index].append(dict[symbol])
    return res


file = open('/home/amvasylev/PycharmProjects/reel/Games/Shining Crown.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

#for symbol in game.base.symbol:
#    print(symbol.payment)


matrix = np.zeros((3, 5))

matrix = np.array(
    reformate(
        [
            ['Melon', 'Lemon', 'Seven', 'Orange', 'Orange'],
            ['Cherry', 'Seven', 'Bell', 'Seven', 'Cherry'],
            ['Seven', 'Cherry', 'Cherry', 'Cherry', 'Seven']
        ]
    )
)

print(matrix)

#print(game.base.scatterlist)

#print(scatter_payment(obj=game, gametype=game.base, matrix=matrix))
print(take_win(game=game, gametype=game.base, matrix=matrix))
