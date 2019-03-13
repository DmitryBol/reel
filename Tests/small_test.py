x = [
 [7, 9, 8, 2, 7, 8, 11, 7, 4, 10, 6, 8, 5, 9, 6, 7, 9, 8, 7, 11, 8, 4, 6, 10, 9, 11, 8, 6, 5, 10, 9, 11, 7, 3, 11, 9,
  10, 11, 7, 8, 10, 3, 9, 2, 7, 5, 4, 11, 6, 4, 7, 6, 8, 7, 11, 9, 3, 10, 8, 7, 9, 10, 3, 6, 7, 4, 9, 7, 6, 10, 2, 2, 2,
  2, 7, 8, 6, 9, 11, 7, 8, 10, 9, 6, 8, 9, 4, 7, 3, 10, 7, 2, 11, 7, 9, 11, 6, 9, 11, 2, 7, 9, 10, 8, 9, 7, 6, 8, 9, 6,
  11, 8, 7, 10, 11, 5, 8, 3, 11, 6, 4, 9, 10, 6, 11, 8, 6, 11, 9, 8, 4, 11, 7, 8, 11, 9, 10, 11, 8, 7, 6, 4, 11, 10, 3,
  11, 7, 3, 9, 8, 7, 9, 11, 8, 4, 11, 5, 10, 11, 7, 6, 8, 10, 11, 6, 9, 8, 7, 9, 8, 7, 10, 9, 7, 11, 10, 9, 8, 3, 7, 8,
  4, 11, 7, 9, 10, 11, 8, 10, 11, 8, 9, 2, 8, 5, 11, 9, 3, 7, 4, 11, 5, 3, 9, 8, 6, 3, 4, 10, 9, 4, 11, 7, 8, 5, 7, 9,
  6, 10, 8, 11, 10, 9, 8, 7, 10, 11, 7, 9, 3, 10, 2, 11, 5, 8, 11, 10, 4, 6, 8, 10, 9, 5, 7, 10, 9, 11, 5, 3, 7, 11, 10,
  9, 8, 3, 10, 5, 4, 7, 10, 11, 7, 10, 9, 7, 11, 10, 4, 6, 3, 10, 8, 7, 10, 11, 5, 8, 9, 10, 6, 9, 7, 6, 3, 5, 6, 8, 5,
  7, 10, 5, 6, 7, 10, 8, 4, 6, 8, 2, 3, 9, 7, 4, 11, 5, 3, 10, 2, 7, 9, 10, 8, 6, 5, 9, 8, 10, 6, 9, 5, 10, 11, 8, 10,
  11, 4, 10, 6, 7, 8, 5, 7, 11, 9, 4, 5, 7, 8, 11, 10, 5, 8, 9, 5, 10, 8, 9, 10, 4, 8, 11, 9, 10, 7, 11, 9, 6, 10, 11,
  3, 8, 9, 11, 10],
  [9, 10, 6, 8, 5, 11, 9, 10, 11, 6, 3, 11, 8, 9, 4, 8, 11, 6, 5, 9, 6, 8, 11, 6, 4, 5, 8, 10, 7, 11, 8, 6, 11, 7, 10,
    4, 9, 3, 10, 8, 7, 5, 10, 6, 9, 8, 7, 11, 8, 10, 11, 2, 10, 9, 8, 6, 10, 4, 9, 10, 7, 11, 10, 8, 7, 10, 9, 5, 7, 11,
    2, 9, 3, 11, 10, 7, 6, 11, 5, 3, 7, 8, 11, 5, 9, 8, 5, 11, 9, 2, 5, 3, 7, 5, 8, 9, 11, 7, 8, 5, 9, 11, 2, 2, 2, 2,
    11, 5, 10, 4, 9, 8, 11, 3, 6, 7, 10, 4, 8, 2, 4, 9, 6, 8, 7, 11, 9, 6, 11, 7, 3, 10, 7, 8, 11, 9, 10, 7, 11, 8, 9,
    6, 4, 11, 10, 4, 9, 5, 8, 6, 9, 5, 7, 9, 5, 11, 7, 4, 9, 6, 7, 10, 11, 9, 7, 2, 4, 8, 5, 7, 9, 8, 11, 5, 3, 4, 6, 8,
    10, 6, 7, 5, 9, 4, 11, 8, 7, 9, 8, 10, 6, 3, 8, 4, 3, 7, 10, 4, 11, 10, 5, 8, 4, 6, 5, 10, 8, 11, 7, 10, 11, 8, 10,
    7, 6, 9, 7, 11, 3, 7, 10, 6, 5, 3, 6, 9, 8, 11, 9, 6, 8, 10, 4, 6, 9, 2, 6, 3, 7, 10, 9, 6, 8, 7, 4, 5, 10, 11, 8,
    2, 4, 9, 10, 8, 7, 10, 8, 7, 11, 3, 9, 6, 11, 10, 7, 8, 3, 9, 7, 11, 8, 10, 11, 6, 8, 10, 3, 11, 2, 10, 9, 8, 10,
    11, 9, 7, 10, 8, 6, 7, 10, 11, 7, 8, 9, 10, 3, 9, 7, 8, 11, 10, 9, 7, 11, 3, 7, 10, 6, 8, 7, 10, 8, 7, 11, 3, 9, 11,
    10, 8, 6, 9, 7, 11, 9, 4, 8, 10, 9, 4, 11, 9, 8, 5, 7, 10, 11, 8, 9, 11, 7, 10, 9, 7, 10, 3, 7, 9, 8, 4, 10, 6, 11,
    7, 10, 9, 8, 7, 9, 11, 7, 9, 10, 7],
  [4, 8, 7, 9, 10, 11, 2, 7, 11, 3, 5, 7, 8, 3, 2, 11, 9, 10, 2, 8, 5, 9, 3, 10, 8, 9, 7, 10, 8, 11, 9, 5, 7, 6, 9, 10,
    5, 4, 10, 6, 11, 2, 9, 10, 7, 8, 3, 9, 5, 3, 11, 8, 9, 10, 11, 4, 8, 10, 7, 9, 4, 7, 11, 8, 4, 3, 10, 11, 9, 7, 10,
    6, 11, 7, 8, 4, 6, 8, 5, 10, 4, 3, 7, 9, 8, 7, 10, 6, 8, 2, 7, 9, 11, 3, 9, 8, 3, 7, 11, 8, 9, 10, 3, 8, 11, 10, 8,
    11, 5, 10, 7, 4, 3, 9, 8, 10, 6, 11, 8, 10, 11, 8, 7, 4, 11, 10, 8, 7, 9, 8, 6, 7, 11, 9, 3, 4, 8, 10, 7, 6, 10, 9,
    7, 11, 8, 6, 10, 7, 6, 10, 9, 7, 6, 8, 9, 3, 11, 6, 9, 7, 6, 10, 3, 6, 7, 8, 6, 11, 7, 9, 8, 10, 11, 6, 8, 9, 10,
    11, 6, 9, 3, 6, 8, 9, 5, 7, 8, 11, 6, 4, 9, 10, 8, 9, 10, 11, 8, 5, 11, 6, 5, 11, 8, 7, 9, 8, 10, 2, 2, 2, 2, 10, 7,
    8, 11, 7, 9, 6, 11, 2, 6, 7, 11, 4, 6, 9, 5, 11, 8, 7, 5, 8, 9, 6, 10, 8, 6, 4, 5, 10, 4, 9, 5, 10, 11, 9, 6, 7, 8,
    10, 7, 11, 6, 10, 9, 7, 11, 4, 10, 9, 3, 7, 11, 5, 8, 7, 10, 9, 11, 7, 8, 4, 5, 10, 11, 9, 7, 5, 6, 4, 3, 8, 7, 3,
    11, 9, 8, 10, 11, 5, 10, 9, 11, 10, 8, 7, 10, 8, 4, 7, 6, 9, 3, 5, 9, 10, 7, 4, 6, 8, 10, 9, 11, 8, 4, 2, 8, 6, 9,
    10, 11, 9, 7, 5, 9, 8, 3, 10, 6, 7, 11, 9, 10, 8, 11, 7, 4, 11, 7, 9, 4, 11, 10, 9, 5, 7, 8, 11, 7, 10, 9, 7, 11, 9,
    10, 7, 5, 11, 10, 2, 11, 7, 5, 11],
  [11, 9, 5, 11, 10, 5, 6, 9, 8, 11, 6, 7, 11, 6, 9, 5, 4, 6, 9, 10, 3, 2, 9, 3, 4, 9, 10, 11, 5, 10, 9, 6, 7, 8, 11,
    6, 3, 9, 7, 5, 4, 7, 10, 3, 7, 11, 9, 10, 2, 2, 2, 2, 7, 9, 8, 5, 11, 10, 6, 7, 8, 11, 6, 3, 10, 9, 2, 10, 5, 8, 11,
    6, 10, 9, 6, 2, 10, 4, 8, 6, 11, 10, 9, 11, 7, 9, 4, 11, 8, 10, 5, 8, 7, 3, 6, 8, 7, 9, 6, 2, 8, 10, 7, 8, 10, 5,
    11, 9, 3, 6, 8, 10, 11, 8, 7, 11, 5, 6, 2, 2, 2, 2, 9, 11, 4, 5, 7, 3, 4, 5, 8, 11, 10, 8, 5, 10, 9, 7, 10, 11, 8,
    3, 9, 11, 10, 8, 3, 9, 8, 11, 10, 4, 7, 11, 6, 7, 9, 11, 6, 9, 3, 10, 8, 9, 6, 5, 8, 10, 7, 5, 9, 8, 11, 9, 7, 6, 8,
    4, 10, 8, 9, 11, 10, 7, 11, 3, 7, 8, 11, 10, 8, 9, 4, 6, 8, 11, 7, 5, 11, 10, 6, 11, 7, 3, 10, 7, 4, 3, 7, 8, 6, 9,
    3, 10, 8, 11, 7, 9, 11, 8, 4, 6, 7, 11, 5, 7, 11, 4, 9, 11, 3, 6, 11, 8, 9, 10, 11, 9, 8, 10, 7, 6, 11, 7, 8, 9, 11,
    8, 10, 4, 11, 7, 10, 5, 7, 10, 9, 11, 7, 8, 10, 9, 7, 10, 11, 9, 7, 4, 9, 11, 8, 5, 4, 9, 6, 3, 11, 7, 10, 8, 7, 10,
    8, 9, 11, 4, 10, 7, 9, 4, 8, 3, 7, 6, 8, 9, 11, 4, 8, 6, 9, 7, 10, 6, 5, 9, 10, 8, 4, 3, 6, 7, 9, 8, 10, 11, 8, 9,
    7, 3, 10, 7, 8, 5, 10, 11, 5, 7, 10, 9, 11, 7, 9, 11, 4, 7, 9, 8, 10, 5, 8, 7, 10, 9, 8, 6, 11, 8, 7, 9, 10, 7, 4,
    6, 8, 7, 10, 8, 7, 10, 9, 8, 10, 7],
  [9, 11, 5, 6, 7, 9, 11, 7, 4, 10, 9, 7, 2, 11, 8, 10, 9, 7, 10, 3, 11, 9, 3, 6, 8, 11, 7, 10, 2, 7, 11, 10, 9, 11,
    10, 8, 7, 11, 9, 2, 10, 11, 5, 7, 8, 6, 10, 11, 3, 10, 8, 5, 7, 11, 8, 3, 7, 8, 4, 9, 7, 10, 9, 7, 2, 6, 5, 10, 8,
    7, 9, 6, 11, 8, 9, 11, 7, 3, 10, 11, 6, 4, 3, 9, 8, 5, 10, 8, 3, 4, 9, 10, 8, 11, 7, 6, 9, 7, 8, 3, 7, 8, 9, 10, 3,
    11, 4, 9, 8, 10, 7, 5, 11, 9, 7, 11, 9, 7, 11, 9, 8, 6, 10, 8, 7, 10, 6, 8, 10, 5, 9, 8, 4, 9, 8, 3, 4, 11, 10, 8,
    3, 2, 7, 11, 3, 9, 4, 7, 11, 10, 9, 6, 10, 9, 11, 6, 10, 7, 8, 2, 6, 11, 5, 2, 6, 9, 11, 7, 9, 10, 5, 7, 10, 9, 7,
    4, 9, 11, 5, 8, 9, 11, 8, 9, 7, 5, 11, 9, 10, 6, 11, 7, 4, 3, 5, 9, 4, 7, 11, 6, 5, 9, 2, 4, 5, 6, 8, 3, 11, 8, 10,
    2, 5, 7, 9, 10, 3, 9, 7, 8, 10, 5, 8, 10, 7, 5, 11, 7, 3, 6, 9, 11, 7, 4, 8, 11, 9, 10, 8, 9, 3, 2, 6, 4, 10, 7, 11,
    6, 8, 5, 6, 9, 8, 10, 5, 8, 7, 10, 8, 2, 7, 6, 8, 7, 9, 5, 10, 6, 9, 10, 8, 4, 10, 3, 11, 10, 9, 5, 11, 7, 8, 10, 3,
    7, 9, 8, 11, 7, 6, 4, 11, 6, 9, 8, 10, 11, 6, 10, 8, 11, 10, 7, 4, 9, 7, 6, 9, 8, 7, 4, 6, 9, 7, 11, 10, 6, 8, 7, 6,
    10, 11, 6, 8, 7, 10, 8, 9, 11, 10, 5, 7, 11, 10, 8, 11, 4, 9, 3, 2, 11, 10, 5, 8, 4, 11, 10, 8, 7, 11, 8, 4, 6, 8,
    4, 9, 8, 11, 6, 9, 10, 11, 7, 8, 10]
]

frequency = [[0 for _ in range(max(x[4]))] for _ in range(len(x))]

for reel_id in range(5):
    for element in x[reel_id]:
        frequency[reel_id][element - 1] += 1

# frequency = [[4*y for y in x] for x in frequency]
print(frequency)