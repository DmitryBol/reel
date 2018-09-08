from FrontEnd.reelWork.reel_generator_alpha import reel_generator
import FrontEnd.structure_alpha as Q
import json

frequency = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
]

file = open('/home/amvasylev/PycharmProjects/reel/Games/Shining Crown.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

game.base.reel_generator(array=frequency, width=5, distance=3)

print(game.base.reels)