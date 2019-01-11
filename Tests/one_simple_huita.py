from random import randint
from random import uniform

repeat_cnt = 1000000
map_ = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
rounds = 10

for _ in range(repeat_cnt):
    counters = [0, 0, 0, 0, 0]

    for _ in range(rounds):
        upper_bound = 5
        for item in counters:
            if item == 3:
                upper_bound -= 1
        if upper_bound == 0:
            break
        column = randint(0, upper_bound - 1)
        rnd = uniform(0, 1)
        while counters[column] == 3:
            column += 1
        if rnd < 0.62:
            counters[column] += 1

    three_counter = 0
    for item in counters:
        if item == 3:
            three_counter += 1
    map_[three_counter] += 1

print(map_[0]/repeat_cnt)
print(map_[1]/repeat_cnt)
print(map_[2]/repeat_cnt)
print(map_[3]/repeat_cnt)
print(map_[4]/repeat_cnt)
print(map_[5]/repeat_cnt)
