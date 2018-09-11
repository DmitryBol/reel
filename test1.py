import FrontEnd.structure_alpha as Q
import json
from Descent.Point import Point

file = open('/home/amvasylev/PycharmProjects/reel/Games/HappyBrauer.txt', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

frequency = [
    [10 for _ in range(11)] + [3] for _ in range(5)
]

game.base.fill_frequency(frequency)
game.free.fill_frequency(frequency)

game.base.create_simple_num_comb(game.window, game.line)
game.free.create_simple_num_comb(game.window, game.line)

point = Point(frequency, frequency, game)
point.fillPoint(game, 1, 1, 1, 1, 1, 1)
point.fillPoint(game, 1, 1, 1, 1, 1, 1, base=False, sd_flag=True)

print(game.count_parameters(base=False, sd_flag=True))
