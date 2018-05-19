import numpy as np
import itertools


def plus_(a, b, window, bad, alls, wilds, length):
    temp = a + b
    result = np.zeros(window)
    add = 0
    sup = alls
    for i in range(window-1, length, -1):
        result[i] = (temp[i] + add)%sup
        add = (temp[i] + add)//sup
    if(length < window):
        result[length] = ((temp[length] + add)%len(bad))
        add = (temp[length] + add)//len(bad)
    sup = len(wilds)
    for i in range(length - 1, -1, -1):
        result[i] = (temp[i] + add)%sup
        add = (temp[i] + add)//sup
    return(result)
def combinations2(window, bad, alls, wilds, length):
    neutral = np.zeros(window)
    neutral[len(neutral) - 1] = 1
    null = np.zeros(window)
    temp = null
    if(length < window):
        t = int(window - 1 - length)
        tao = len(bad)
    else:
        t = 0
        tao = 1
    combinations = np.zeros(((len(wilds)**(length))*tao*alls**t, window))
    for i in range((len(wilds)**(length))*tao*alls**t):
        combinations[i] = temp
        temp = plus_(temp, neutral, window, bad, alls, wilds, length)
    for i in range(len(combinations)):
        for j in range(length):
            combinations[i,j] = wilds[int(combinations[i,j])]
        if(length < window):
            combinations[i,length] = bad[int(combinations[i,length])]

    return(combinations)