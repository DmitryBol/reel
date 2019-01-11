import FrontEnd.structure_alpha as Q
import json

frequency = [
    [0, 1, 30, 42, 51, 54, 69, 78, 84, 96],
    [0, 1, 30, 42, 51, 54, 69, 78, 84, 96],
    [0, 1, 30, 42, 51, 54, 69, 78, 84, 96],
    [0, 1, 30, 42, 51, 54, 69, 78, 84, 96],
    [0, 1, 30, 42, 51, 54, 69, 78, 84, 96]
]

# frequency = [
#     [0, 6, 6, 9, 12, 18, 18, 27, 27, 27],
#     [0, 6, 6, 9, 12, 18, 18, 27, 27, 27],
#     [0, 6, 6, 9, 12, 18, 18, 27, 27, 27],
#     [0, 6, 6, 9, 12, 18, 18, 27, 27, 27],
#     [0, 6, 6, 9, 12, 18, 18, 27, 27, 27]
# ]

# frequency = [
#     [9, 9, 9, 15, 15, 18, 18, 18, 24, 24],
#     [9, 9, 9, 15, 15, 18, 18, 18, 24, 24],
#     [9, 9, 9, 15, 15, 18, 18, 18, 24, 24],
#     [9, 9, 9, 15, 15, 18, 18, 18, 24, 24],
#     [9, 9, 9, 15, 15, 18, 18, 18, 24, 24]
# ]

new_frequency = []
reel_id = 0

for reel in frequency:
    new_frequency.append([])
    index = 0
    for element in reel:
        new_frequency[reel_id].append(element)
        index += 1
    reel_id += 1

file = open('/home/amvasylev/PycharmProjects/reel/Games/GoldGold.json', 'r')
j = file.read()
interim = json.loads(j)
game = Q.Game(interim)
file.close()

game.base.reel_generator(frequency_array=new_frequency, window_width=5, reel_distance=3, validate=False)

# game.free.reel_generator(frequency_array=new_frequency, window_width=5, reel_distance=3, validate=False)

print('{')
for reel in game.base.reels:
    # for reel in game.free.reels:
    out_str = '    {'
    for symbol in reel:
        out_str += str(symbol + 1) + ', '
    out_str = out_str[:-2] + '},'
    print(out_str)
print('}')

for reel in game.base.reels:
    # for reel in game.free.reels:
    s = '- ['
    for element in reel:
        s += str(element + 1) + ', '
    s = s[:-2] + ']'
    print(s)
