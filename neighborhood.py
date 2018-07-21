import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np


#rg = __import__("reel generator")

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
    def fillVal(self, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew):
        self.value = F(base_rtp, freemean, rtp, sdnew, self.base_rtp, self.freemean, self.rtp, self.sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
    def scaling(self, scale=2):
        for i in range(len(self.frequency)):
            for j in range(len(self.frequency[i])):
                self.frequency[i][j] = scale*self.frequency[i][j]
        return self
    def fillPoint(self, obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew):
        obj.base.reel_generator(self.frequency, obj.window[0], obj.window[1])
        obj.free.reel_generator(self.frequency, obj.window[0], obj.window[1])
        obj.base.fill_frequency(self.frequency)
        obj.free.fill_frequency(self.frequency)

        obj.base.fill_count_killed(obj.window[0])
        #obj.base.create_simple_num_comb(obj.window, obj.line)
        obj.base.fill_simple_num_comb(obj.window, obj.line)
        obj.base.fill_scatter_num_comb(obj.window)

        obj.free.fill_count_killed(obj.window[0])
        #obj.free.create_simple_num_comb(obj.window, obj.line)
        obj.free.fill_simple_num_comb(obj.window, obj.line)
        obj.free.fill_scatter_num_comb(obj.window)

        self.baseReel = obj.base.reels
        self.freeReel = obj.free.reels


        params = obj.count_parameters()

        self.base_rtp, self.freemean, self.rtp, self.sdnew, self.hitrate = params['base_rtp'], params['freemean'], params['rtp'], params['sdnew'], params['hitrate']

        self.fillVal(base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)



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
                    if not obj.base.symbol[i].scatter and not obj.base.symbol[j].scatter:
                        if obj.base.symbol[i].payment[obj.window[0]] > obj.base.symbol[j].payment[obj.window[0]]:
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[i] += 1
                            tmp[j] -= 1
                            if tmp[i] > (1/obj.window[1])*sum(tmp) or tmp[j] < 0.05*sum(tmp):
                                print('ABSOLUTELY DEGENERATE')
                                break
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                        elif obj.base.symbol[i].payment[obj.window[0]] < obj.base.symbol[j].payment[obj.window[0]]:
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[j] += 1
                            tmp[i] -= 1
                            if tmp[j] > (1/obj.window[1])*sum(tmp) or tmp[i] < 0.05*sum(tmp):
                                print('ABSOLUTELY DEGENERATE')
                                break
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
        elif base_rtp < root.base_rtp:
            for i in range(len(obj.base.symbol) - 1):
                for j in range(i + 1, len(obj.base.symbol)):
                    if not obj.base.symbol[i].scatter and not obj.base.symbol[j].scatter:
                        if obj.base.symbol[i].payment[obj.window[0]] < obj.base.symbol[j].payment[obj.window[0]]:
                            #print('C')
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[i] += 1
                            tmp[j] -= 1
                            if tmp[i] > (1/obj.window[1])*sum(tmp) or tmp[j] < 0.05*sum(tmp):
                                print('ABSOLUTELY DEGENERATE')
                                break
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                            #print('1st +1, sec -1', tmp, i, j)

                        elif obj.base.symbol[i].payment[obj.window[0]] > obj.base.symbol[j].payment[obj.window[0]]:
                            #print('D')
                            tmp = copy.deepcopy(root.frequency[0])
                            tmp[j] += 1
                            tmp[i] -= 1
                            if tmp[j] > (1/obj.window[1])*sum(tmp) or tmp[i] < 0.05*sum(tmp):
                                print('ABSOLUTELY DEGENERATE')
                                break
                            frequency = [copy.deepcopy(tmp) for i in range(obj.window[0])]
                            if frequency not in prev:
                                self.neighbour.append(point(frequency))
                            #print('1st -1, sec +1', tmp, i, j)

    def fillParametrs(self, obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew):
        for i in range(len(self.neighbour)):
            obj.base.reel_generator(self.neighbour[i].frequency, obj.window[0], obj.window[1])
            obj.free.reel_generator(self.neighbour[i].frequency, obj.window[0], obj.window[1])
            obj.base.fill_frequency(self.neighbour[i].frequency)
            obj.free.fill_frequency(self.neighbour[i].frequency)

            obj.base.fill_count_killed(obj.window[0])
            #obj.base.create_simple_num_comb(obj.window, obj.line)
            obj.base.fill_simple_num_comb(obj.window, obj.line)
            obj.base.fill_scatter_num_comb(obj.window)

            obj.free.fill_count_killed(obj.window[0])
            #obj.free.create_simple_num_comb(obj.window, obj.line)
            obj.free.fill_simple_num_comb(obj.window, obj.line)
            obj.free.fill_scatter_num_comb(obj.window)

            self.neighbour[i].baseReel = obj.base.reels
            self.neighbour[i].freeReel = obj.free.reels


            params = obj.count_parameters()

            self.neighbour[i].base_rtp, self.neighbour[i].freemean, self.neighbour[i].rtp, self.neighbour[i].sdnew, self.neighbour[i].hitrate = params['base_rtp'], params['freemean'], params['rtp'], params['sdnew'], params['hitrate']

            self.neighbour[i].fillVal(base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
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
    print(out.scatter_index_with_frequency[11]/out.total_length) #количество скатеров с индексом 11 на одной ленте


    start_time = time.time()


    obj.base.reel_generator(distr, obj.window[0], obj.window[1])
    obj.free.reel_generator(distr, obj.window[0], obj.window[1])
    obj.base.fill_frequency(distr)
    obj.free.fill_frequency(distr)

    obj.base.fill_count_killed(obj.window[0])
    obj.base.create_simple_num_comb(obj.window, obj.line)
    obj.base.fill_simple_num_comb(obj.window, obj.line)
    obj.base.fill_scatter_num_comb(obj.window)

    obj.free.fill_count_killed(obj.window[0])
    obj.free.create_simple_num_comb(obj.window, obj.line)
    obj.free.fill_simple_num_comb(obj.window, obj.line)
    obj.free.fill_scatter_num_comb(obj.window)


    root = point(distr)
    root.baseReel = obj.base.reels
    root.freeReel = obj.free.reels

    params = obj.count_parameters()
    base_rtp, freemean, rtp, sdnew, hitrate = params['base_rtp'], params['freemean'], params['rtp'], params['sdnew'], params['hitrate']

    print('All combinations =', obj.base.all_combinations())
    print('Base RTP = ', base_rtp)
    print('FreeMean = ', freemean)
    print('RTP = ', rtp)
    print('SD new = ', sdnew)
    print('Hitrate = ', hitrate)

    root.base_rtp, root.freemean, root.rtp, root.sdnew, root.hitrate = base_rtp, freemean, rtp, sdnew, hitrate

    print(time.time() - start_time)

    return distr, base_rtp, freemean, rtp,sdnew, hitrate, obj, root


def F(base_rtp, freemean, rtp, sdnew, r_base_rtp, r_freemean, r_rtp, r_sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew):
    t1 = np.fabs(base_rtp - r_base_rtp)/err_base_rtp
    t2 = np.fabs(freemean - r_freemean)/err_freemean
    t3 = np.fabs(sdnew - r_sdnew)/err_sdnew
    t4 = np.fabs(rtp - r_rtp)/err_rtp
    return max([t1, t2, t4])



#1-ый метод. Работает в терминах окрестностей. Стартовой точкой является центральная - это та, в которой всех символов ~ поровну.
#Минус метода в том, что при добавлении sd функционал F имеет множество локальных минимумов

def FirstMethod(hitrate, err_hitrate, file_name):

    #file_name = 'Games\HappyBrauer.txt'
    #hitrate = 100

    out = sm.get_scatter_frequency(file_name, hitrate, err_hitrate)

    t_distr, r_base_rtp, r_freemean, r_rtp, r_sdnew, r_hitrate, obj, root = parametrs(file_name, out)

    print(root.frequency)



    #s = input()

    #s = s.split(', ')

    base_rtp, freemean, rtp, sdnew = 1.4, 1.5, 1.5, 6#float(s[0]), float(s[1]), float(s[2])
    err_base_rtp, err_freemean, err_rtp, err_sdnew = 0.1, 0.1, 0.1, 0.1

    print('assuming errors for base rtp, freemean, sd ', base_rtp, freemean, rtp, sdnew)
    print('assuming base rtp, freemean, sd ', err_base_rtp, err_freemean, err_rtp, err_sdnew)

    #s = input()

    #s = s.split(', ')

    #float(s[0]), float(s[1]), float(s[2])

    root.fillVal(base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
    print('root value ', root.value)

    print('assuming base_rtp, freemean, rtp, sdnew ', base_rtp, freemean, rtp, sdnew)

    print('assuming errors for base_rtp, freemean, rtp, sdnew ', err_base_rtp, err_freemean, err_rtp, err_sdnew)

    print(F(base_rtp, freemean, rtp, sdnew, r_base_rtp, r_freemean, r_rtp, r_sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew))

    #print(t_distr)



    neighbours = neighbourhood(root, obj, base_rtp)

    print('neigh', neighbours.neighbour[0].frequency)
    print(len(neighbours.neighbour))
    print(root.frequency)

    obj.base.create_simple_num_comb(obj.window, obj.line)
    obj.free.create_simple_num_comb(obj.window, obj.line)

    neighbours.fillParametrs(obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
    neighbours.neighbourVal()

    counter = 0
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
            tmp_neighbours.fillParametrs(obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
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
        neighbours.fillParametrs(obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
        neighbours.neighbourVal()
        print('iteration ', counter, ' value ', tmp_min.value, ' distribution ', tmp_min.frequency[0])
        if counter > 500:
            print('222')
            break

        counter += 1

#FirstMethod(100, 1,'Games\HappyBrauer.txt')


class group:
    def __init__(self, root, num, sortedSymbols, obj):
        self.root = root
        self.number = num
        k = len(sortedSymbols)//num
        self.groups = []
        for i in range(num):
            g = []
            for j in range(k):
                g.append(sortedSymbols[i*k + j])
            if i == num - 1:
                for j in range(1, len(sortedSymbols)%num + 1):
                    g.append(sortedSymbols[i*k + k - 1 + j])
            self.groups.append(g)
        distributions = []
        for i in range(num - 1):
            for j in range(i + 1, num):
                tmp1 = copy.deepcopy(root.frequency)
                tmp2 = copy.deepcopy(root.frequency)
                for l in range(len(tmp1)):
                    code = 0
                    for k in range(len(self.groups[i])):
                        tmp1[l][self.groups[i][k]] += 1
                        tmp2[l][self.groups[i][k]] -= 1
                        if  tmp1[l][self.groups[i][k]] > (1/obj.window[1])*sum(tmp1[l]) or tmp2[l][self.groups[i][k]] < 0.02*sum(tmp1[l]):
                            #print('ABSOLUTELY DEGENERATE')
                            code = -1
                            break
                    for k in range(len(self.groups[j])):
                        tmp1[l][self.groups[j][k]] -= 1
                        tmp2[l][self.groups[j][k]] += 1
                        if  tmp2[l][self.groups[j][k]] > (1/obj.window[1])*sum(tmp1[l]) or tmp1[l][self.groups[j][k]] < 0.02*sum(tmp1[l]):
                            #print('ABSOLUTELY DEGENERATE')
                            code = -1
                            break
                if code == 0:
                    distributions = distributions + [tmp1, tmp2]
        for p in distributions:
            for l in range(len(p)):
                for g in self.groups:
                    total = 0
                    for j in g:
                        total += p[l][j]
                    for j in g:
                        p[l][j] = total//len(g)
                    for j in range(total%len(g)):
                        p[l][g[j]] += 1
        self.points = [point(d) for d in distributions]

    def fillGroup(self, obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew):
        for p in self.points:
            p.fillPoint(obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)
    def printGroup(self):
        print('root ', self.root.frequency[0], ' root value ', self.root.value, ' root base rtp = ', self.root.base_rtp, ' freemean = ', self.root.freemean, ' rtp = ', self.root.rtp , ' sdnew = ', self.root.sdnew, ' hitrate = ', self.root.hitrate)
        for i in range(len(self.points)):
            print(self.points[i].frequency[0], ' value ', self.points[i].value)
    def findMin(self):
        index = -1
        current = copy.deepcopy(self.root.value)
        for i in range(len(self.points)):
            if self.points[i].value < current:
                current = self.points[i].value
                index = i
        if index == -1:
            print('no minimum found')
            return -1
        else:
            return copy.deepcopy(self.points[index])

def sortSymbols(obj):
    sortedSymbols = []
    for i in range(len(obj.base.symbol)):
        if not obj.base.symbol[i].scatter:
            sortedSymbols.append(i)
    #пузырьковая сортировка, не думаю, что стоит мудрить с другой
    for i in range(len(sortedSymbols) - 1):
        for j in range(i + 1, len(sortedSymbols)):
            if obj.base.symbol[sortedSymbols[i]].payment[obj.window[0]] < obj.base.symbol[sortedSymbols[j]].payment[obj.window[0]]:
                sortedSymbols[i], sortedSymbols[j] = sortedSymbols[j], sortedSymbols[i]
    return sortedSymbols


#Здесь происходит некоторая херня с hitrate.

def SecondMethod(hitrate, err_hitrate, file_name):

    out = sm.get_scatter_frequency(file_name, hitrate, err_hitrate)
    t_distr, r_base_rtp, r_freemean, r_rtp, r_sdnew, r_hitrate, obj, root = parametrs(file_name, out)

    print(root.frequency)

    base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew = 2.5, 2.5, 2, 14, 0.5, 0.5, 0.5, 0.5


    root.fillVal(base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew)

    print('assuming base rtp, freemean, rtp, sd ', base_rtp, freemean, rtp, sdnew)
    print('assuming errors for base rtp, freemean, rtp,  sd ', err_base_rtp, err_freemean, err_rtp, err_sdnew)

    print('root value ', root.value)

    obj.base.create_simple_num_comb(obj.window, obj.line)
    obj.free.create_simple_num_comb(obj.window, obj.line)
    sortedSymbols = sortSymbols(obj)

    min_is_found = False
    while not min_is_found:
        print('ITERATION \n')
        number_of_groups = 2
        while number_of_groups <= int(len(sortedSymbols)/2):
            print('is zis e los?')
            temp_group = group(root, number_of_groups, sortedSymbols, obj)
            print('группы ', temp_group.groups)
            temp_group.fillGroup(obj, base_rtp, freemean, rtp, sdnew, err_base_rtp, err_freemean, err_rtp, err_sdnew )
            temp_group.printGroup()
            if temp_group.findMin() != -1:
                if temp_group.findMin().value < 1:
                    min_is_found = True
                    print('ending with ', temp_group.findMin().value)
                    print('base ', temp_group.findMin().base_rtp)
                    print('freemean ', temp_group.findMin().freemean)
                    print('rtp ', temp_group.findMin().rtp)
                    print('sdnew ', temp_group.findMin().sdnew)
                    print('hitrate ', temp_group.findMin().hitrate)
                    root = copy.deepcopy(temp_group.findMin())
                    print(root.frequency[0])
                    break
                else:
                    print('path ', temp_group.findMin().value)
                    root = copy.deepcopy(temp_group.findMin())
            else:
                print(number_of_groups)
                number_of_groups += 1
        if not min_is_found:
            root = root.scaling()



SecondMethod(100, 1,'Games\HappyBrauer.txt')



