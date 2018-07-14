import json
import sys
sys.path.insert(0, 'Front-end/')
import structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np


rg = __import__("reel generator")

def freq(obj, out):#генерируем начальную ленту. 1 аргумент - структура игры, 2 аргумент - структура с нужными параметрами hit rate
    average = out.total_length
    for i in obj.base.scatterlist:
        average -= out.scatter_index_with_frequency[i]
    average = average //  (len(obj.base.symbol) - len(obj.base.scatterlist))
    tmp = [out.scatter_index_with_frequency[i] if i in obj.base.scatterlist else average for i in range(len(obj.base.symbol))]
    j = 0
    while sum(tmp) < out.total_length:
        if j not in obj.base.scatterlist:
            tmp[j] += 1
        j += 1
    frequency = []

    for i in range(obj.window[0]):
        frequency.append(copy.deepcopy(tmp))

    if sum(tmp) != out.total_length:
        print('ERROR')
        return -1

    return frequency

class point(object):
    def __init__(self, frequency):
        self.frequency = frequency
        self.baseReel = '-1'
        self.freeReel = '-1'
        self.base_rtp = '-1'
        self.rtp = '-1'
        self.freemean = '-1'
        self.sdnew = '-1'
        self.hitrate = '-1'
        self.value = '-1'
    def fillVal(self, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew):
        self.value = F(base_rtp, freemean, sdnew, self.base_rtp, self.freemean, self.sdnew, err_base_rtp, err_freemean, err_sdnew)
    def scaling(self, scale=2):
        for i in range(len(self.frequency)):
            for j in range(len(self.frequency[i])):
                self.frequency[i][j] = scale*self.frequency[i][j]
        return self


#Класс окрестность. Аргументы: root - центр окрестности, obj - Юрина структура, base_rtp - параметр введенный пользователем, нужен для того, что бы
#не обсчитывать всю окрестность, previous - окрестность на предыдущем шаге итерации, по дефолту предполагается фиктивной (для начальной точки).
#Аргумент previous нужне для того, что бы на новой итерации не учитывать точки, отброшенные на предыдущей.


class neighbourhood(object):
    def __init__(self, root, obj, base_rtp, previous = 0):
        prev = []
        if previous != 0:
            prev = [previous.neighbour[i].frequency for i in range(len(previous.neighbour))]
        self.neighbour = []
        self.root = root
        if base_rtp > root.base_rtp:
            for i in range(len(obj.base.symbol) - 1):
                for j in range(i + 1, len(obj.base.symbol)):
                    if obj.base.symbol[i].scatter == False and obj.base.symbol[j].scatter == False:
                        if obj.base.symbol[i].payment[obj.window[0]] > obj.base.symbol[j].payment[obj.window[0]]:
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[i] += 1
                            tmp[j] -= 1
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                        elif obj.base.symbol[i].payment[obj.window[0]] < obj.base.symbol[j].payment[obj.window[0]]:
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[j] += 1
                            tmp[i] -= 1
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
        elif base_rtp < root.base_rtp:
            for i in range(len(obj.base.symbol) - 1):
                for j in range(i + 1, len(obj.base.symbol)):
                    if obj.base.symbol[i].scatter == False and obj.base.symbol[j].scatter == False:
                        if obj.base.symbol[i].payment[obj.window[0]] < obj.base.symbol[j].payment[obj.window[0]]:
                            #print('C')
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[i] += 1
                            tmp[j] -= 1
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                            #print('1st +1, sec -1', tmp, i, j)

                        elif obj.base.symbol[i].payment[obj.window[0]] > obj.base.symbol[j].payment[obj.window[0]]:
                            #print('D')
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[j] += 1
                            tmp[i] -= 1
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                            #print('1st -1, sec +1', tmp, i, j)

    def fillParametrs(self, obj, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew):
        for i in range(len(self.neighbour)):
            obj.base.reel_generator(self.neighbour[i].frequency, obj.window[0], obj.window[1])
            obj.free.reel_generator(self.neighbour[i].frequency, obj.window[0], obj.window[1])
            obj.base.fill_frequency(self.neighbour[i].frequency)
            obj.free.fill_frequency(self.neighbour[i].frequency)
            obj.base.fill_simple_num_comb(obj.window, obj.line)
            obj.base.fill_scatter_num_comb(obj.window)
            obj.free.fill_simple_num_comb(obj.window, obj.line)
            obj.free.fill_scatter_num_comb(obj.window)

            self.neighbour[i].baseReel = obj.base.reels
            self.neighbour[i].freeReel = obj.free.reels

            r_base_rtp = obj.count_base_RTP2('base')
            r_freemean = obj.freemean2()
            r_rtp = obj.count_RTP2(r_freemean, r_base_rtp)
            r_sdnew = obj.count_volatility2new(r_freemean, r_rtp)
            r_hitrate = obj.count_hitrate2()

            self.neighbour[i].base_rtp, self.neighbour[i].freemean,self.neighbour[i].rtp, self.neighbour[i].sdnew, self.neighbour[i].hitrate = r_base_rtp, r_freemean, r_rtp, r_sdnew, r_hitrate

            self.neighbour[i].fillVal(base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
    def neighbourVal(self):
        for i in range(len(self.neighbour)):
            print(self.neighbour[i].value, self.neighbour[i].frequency[0])
    def findMin(self):
        tmp_val = 100000
        tmp_ind = -1
        for i in range(len(self.neighbour)):
            if self.neighbour[i].value < tmp_val:
                tmp_val = self.neighbour[i].value
                tmp_ind = i
        print(tmp_val)
        return tmp_ind





def parametrs(file_name, out):
    file = open(file_name, 'r')
    j = file.read()

    interim = json.loads(j)

    obj = Q.Game(interim)

    distr = freq(obj, out)


    print(out.total_length)
    print(out.scatter_index_with_frequency)
    print(out.scatter_index_with_frequency[12]/out.total_length) #количество скатеров с индексом 12 на одной ленте


    start_time = time.time()


    obj.base.reel_generator(distr, obj.window[0], obj.window[1])
    obj.free.reel_generator(distr, obj.window[0], obj.window[1])
    obj.base.fill_frequency(distr)
    obj.free.fill_frequency(distr)


    obj.base.fill_simple_num_comb(obj.window, obj.line)
    obj.base.fill_scatter_num_comb(obj.window)
    obj.free.fill_simple_num_comb(obj.window, obj.line)
    obj.free.fill_scatter_num_comb(obj.window)


    root = point(distr)
    root.baseReel = obj.base.reels
    root.freeReel = obj.free.reels


    print('All combinations =', obj.base.all_combinations())
    base_rtp = obj.count_base_RTP2('base')
    print('Base RTP = ', base_rtp)
    freemean = obj.freemean2()
    print('FreeMean = ', freemean)
    rtp = obj.count_RTP2(freemean, base_rtp)
    print('RTP = ', rtp)
    sd = obj.count_volatility2(freemean, rtp)
    print('RTP SD = ', sd)
    sdnew = obj.count_volatility2new(freemean, rtp)
    print('RTP SD new = ', sdnew)
    hitrate = obj.count_hitrate2()
    print('Hitrate = ', hitrate)

    root.base_rtp, root.freemean, root.rtp, root.sdnew, root.hitrate = base_rtp, freemean, rtp, sdnew, hitrate

    print(time.time() - start_time)

    return distr, base_rtp, freemean, sdnew, hitrate, obj, root


def F(base_rtp, freemean, sdnew, r_base_rtp, r_freemean, r_sdnew, err_base_rtp, err_freemean, err_sdnew):
    t1 = np.fabs(base_rtp - r_base_rtp)/err_base_rtp
    t2 = np.fabs(freemean - r_freemean)/err_freemean
    t3 = np.fabs(sdnew - r_sdnew)/err_sdnew
    return max([t1, t2, t3])




file_name = 'HappyBrauer.txt'
hitrate = 100



out = sm.get_scatter_frequency(file_name, hitrate, 5)

t_distr, r_base_rtp, r_freemean, r_sdnew, r_hitrate, obj, root = parametrs(file_name, out)

print(root.frequency)

print('assuming base rtp, freemean, sd ', 1.4, 1.5, 6)

#s = input()

#s = s.split(', ')

base_rtp, freemean, sdnew = 1.4, 1.5, 6#float(s[0]), float(s[1]), float(s[2])

print('assuming errors for base rtp, freemean, sd ', 0.1, 0.1, 0.1)

#s = input()

#s = s.split(', ')


#1.4, 1.5, 6
#0.1, 0.1, 0.1
err_base_rtp, err_freemean, err_sdnew = 0.1, 0.1, 0.1#float(s[0]), float(s[1]), float(s[2])

root.fillVal(base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
print('root value ', root.value)

print(base_rtp, freemean, sdnew)

print(err_base_rtp, err_freemean, err_sdnew)

print(F(base_rtp, freemean, sdnew, r_base_rtp, r_freemean, r_sdnew, err_base_rtp, err_freemean, err_sdnew))

#print(t_distr)



neighbours = neighbourhood(root, obj, base_rtp)

print('neigh', neighbours.neighbour[0].frequency)
print(len(neighbours.neighbour))
print(root.frequency)



neighbours.fillParametrs(obj, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
neighbours.neighbourVal()

counter = 0

'''root = root.scaling()
print('after scaling ', root.frequency)
root.fillVal(base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
print('root value ', root.value)'''


'''
tmp_min = neighbours.neighbour[neighbours.findMin()]
print('END ', tmp_min.frequency, tmp_min.value)
new = neighbourhood(tmp_min, obj, base_rtp, previous=neighbours)
new.fillParametrs(obj, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
new.neighbourVal()

new_root = tmp_min.scaling()
print('scaling ')
print(new_root.frequency)
new_root.fillVal(base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
print('new root value (must be the same) = ', new_root.value)'''


counter2 = 0

while 1:
    print('AAA')
    tmp_neighbours = neighbours
    if tmp_neighbours.root.value < 1:
        print('000')
        print('minimum ', tmp_neighbours.root.value, tmp_neighbours.root.frequency[0])
        break
    tmp_min = neighbours.neighbour[neighbours.findMin()]

    while tmp_min.value > tmp_neighbours.root.value:
        print('Уперлись')
        tmp_root = tmp_neighbours.root.scaling()
        print('ы')
        tmp_neighbours = neighbourhood(tmp_root, obj, base_rtp)
        print('ыы')
        tmp_neighbours.fillParametrs(obj, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
        print('ыыы')
        tmp_min = tmp_neighbours.neighbour[neighbours.findMin()]
        print('scaling №  ', counter2 , ' value ', tmp_min.value)
        counter2 += 1



    print('CHECKING ', tmp_min.frequency[0], tmp_min.value)
    if tmp_min.value < 1:
        print('111')
        print('minimum ', tmp_min.value, tmp_min.frequency[0])
        break
    neighbours = neighbourhood(tmp_min, obj, base_rtp, previous=tmp_neighbours)
    neighbours.fillParametrs(obj, base_rtp, freemean, sdnew, err_base_rtp, err_freemean, err_sdnew)
    neighbours.neighbourVal()
    print('iteration ', counter, ' value ', tmp_min.value, ' distribution ', tmp_min.frequency[0])
    if counter > 5:
        print('222')
        break

    counter += 1



#rg.print_game(obj.base)


#print('AAA', len(obj.base.reels[0]))

#print(distr[0])
