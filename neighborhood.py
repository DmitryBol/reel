import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np

scaleLimit = 2
Inf = 0.05
wildInf = 0.025

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
        self.sdnew = '-1'
        self.hitrate = '-1'
        self.value = '-1'
    def fillVal(self, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew):
        self.value = F(base_rtp, rtp, sdnew, self.base_rtp, self.rtp, self.sdnew, err_base_rtp, err_rtp, err_sdnew)
    def scaling(self, scale=2):
        for i in range(len(self.frequency)):
            for j in range(len(self.frequency[i])):
                self.frequency[i][j] = scale*self.frequency[i][j]
        return self
    def fillPoint(self, obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew):
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

        self.base_rtp, self.rtp, self.sdnew, self.hitrate = params['base_rtp'], params['rtp'], params['sdnew'], params['hitrate']

        self.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)

    def printBaseReel(self, file):
        max_length = 0
        file = file[:file.find('\\') + 1] + "Base Reels\\" + file[file.find('\\') + 1:]
        f = open(file, 'w')
        for l in range(len(self.baseReel)):
            if len(self.baseReel[l]) > max_length:
                max_length = len(self.baseReel[l])
        for i in range(max_length):
            s = ''
            for l in range(len(self.baseReel)):
                if i < len(self.baseReel[l]):
                    t = (15 - len(self.baseReel[l][i].name))*' '
                    s = s + self.baseReel[l][i].name + t
                else:
                    s = 15*' '
            f.write(s + '\n')
            f.write('\n')
            #print('\n')
            #print(s)
        f.close()



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

    root.base_rtp, root.rtp, root.sdnew, root.hitrate = params['base_rtp'], params['rtp'], params['sdnew'], params['hitrate']

    roots = [root]

    roots = roots + initialDistributions(obj, out)

    print(time.time() - start_time)

    return distr, params['base_rtp'], params['rtp'], params['sdnew'], params['hitrate'], obj, roots

def initialDistributions(obj, out):
    t = [0 for j in range(len(obj.base.symbol))]
    numb_of_scatters = 0
    for j in range(len(obj.base.scatterlist)):
        t[obj.base.scatterlist[j]] = out.scatter_index_with_frequency[obj.base.scatterlist[j]]
        numb_of_scatters += t[obj.base.scatterlist[j]]
    num = (len(obj.base.symbol) - len(obj.base.scatterlist) - 1)#число доступных символов

    Sup = 1/obj.window[1]
    wildSup = 1/obj.window[1]


    initial = []
    for i in range(len(obj.base.symbol)):
        temp = copy.deepcopy(t)
        temp_ = copy.deepcopy(t)
        if not obj.base.symbol[i].scatter:
            if not obj.base.symbol[i].wild:
                temp[i] = int(Inf*out.total_length) + 1
                temp_[i] = int(Sup*out.total_length) - 1
            else:
                temp[i] = int(wildInf*out.total_length) + 1
                temp_[i] = int(wildSup*out.total_length) - 1
            total = out.total_length - sum(temp)
            total_ = out.total_length - sum(temp_)
            avg = total // num
            avg_ = total_ // num
            for j in range(len(obj.base.symbol)):
                if j not in obj.base.scatterlist and j != i:
                    temp[j] = avg
                    temp_[j] = avg_
            counter = 0
            for j in range(len(obj.base.symbol)):
                if j not in obj.base.scatterlist and j != i:
                    temp[j] += 1
                    counter += 1
                if counter >= total % num:
                    break
            counter = 0
            for j in range(len(obj.base.symbol)):
                if j not in obj.base.scatterlist and j != i:
                    temp_[j] += 1
                    counter += 1
                if counter >= total_ % num:
                    break
            temp2 = [temp for j in range(obj.window[0])]
            temp_2 = [temp_ for j in range(obj.window[0])]
            initial = initial + [point(temp2),point(temp_2)]

    for i in initial :
        i.baseReel = obj.base.reels
        i.freeReel = obj.free.reels

        params = obj.count_parameters()

        i.base_rtp, i.rtp, i.sdnew, i.hitrate = params['base_rtp'], params['rtp'], params['sdnew'], params['hitrate']
        #print(i.frequency[0], sum(i.frequency[0]))
    return initial

def F(base_rtp, rtp, sdnew, r_base_rtp, r_rtp, r_sdnew, err_base_rtp, err_rtp, err_sdnew):
    t1 = np.fabs(base_rtp - r_base_rtp)/err_base_rtp
    t2 = np.fabs(rtp - r_rtp)/err_rtp
    t3 = np.fabs(sdnew - r_sdnew)/err_sdnew
    return max([t1])



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

        self.total = [sum(i) for i in root.frequency]

        self.groups = []
        for i in range(len(obj.base.symbol)):
            if obj.base.symbol[i].wild != False:
                self.groups.append([i])
        c = 0
        t_num = num - len(self.groups)
        k = len(sortedSymbols)//t_num
        for i in range(t_num):
            g = []
            if c < len(sortedSymbols)%t_num:
                for j in range(c, k + c + 1):
                    g.append(sortedSymbols[i*k + j])
                c += 1
            else:
                for j in range(c, k + c):
                    g.append(sortedSymbols[i*k + j])

            self.groups.append(g)



        distributions = []
        for i in range(num - 1):
            for j in range(i + 1, num):
                tmp1 = [copy.deepcopy(f) for f in root.frequency]
                tmp2 = [copy.deepcopy(f) for f in root.frequency]
                for l in range(obj.window[0]):
                    for k in  range(min(len(self.groups[i]), len(self.groups[j]))):
                        tmp1[l][self.groups[i][k]] += 1
                        tmp2[l][self.groups[j][k]] += 1
                        tmp1[l][self.groups[j][k]] -= 1
                        tmp2[l][self.groups[i][k]] -= 1

                for l in range(obj.window[0]):
                    total_i_1 = 0
                    total_i_2 = 0
                    total_j_1 = 0
                    total_j_2 = 0
                    for k in self.groups[i]:
                        total_i_1 += tmp1[l][k]
                        total_i_2 += tmp2[l][k]
                    for k in self.groups[j]:
                        total_j_1 += tmp1[l][k]
                        total_j_2 += tmp2[l][k]


                    for k in self.groups[i]:
                        tmp1[l][k] = total_i_1 // len(self.groups[i])
                        tmp2[l][k] = total_i_2 // len(self.groups[i])
                    for k in self.groups[j]:
                        tmp1[l][k] = total_j_1 // len(self.groups[j])
                        tmp2[l][k] = total_j_2 // len(self.groups[j])


                    for k in range(total_i_1 % len(self.groups[i])):
                        tmp1[l][self.groups[i][k]] += 1
                    for k in range(total_i_2 % len(self.groups[i])):
                        tmp2[l][self.groups[i][k]] += 1

                    for k in range(total_j_1 % len(self.groups[j])):
                        tmp1[l][self.groups[j][k]] += 1
                    for k in range(total_j_2 % len(self.groups[j])):
                        tmp2[l][self.groups[j][k]] += 1
                tmp1_ok = True
                tmp2_ok = True
                '''if flag:
                    print('tmp1: ', tmp1)
                    print('tmp2: ', tmp2)'''
                for l in range(obj.window[0]):
                    for s in range(len(tmp1[l])):
                        if s not in obj.base.scatterlist:
                            if s not in obj.base.wildlist and s not in obj.base.ewildlist:
                                if tmp1[l][s] > (1/obj.window[1])*self.total[l] or tmp1[l][s] < Inf*self.total[l]:
                                    tmp1_ok = False
                                    break
                            else:
                                if tmp1[l][s] > (1/obj.window[1])*self.total[l] or tmp1[l][s] < wildInf*self.total[l]:
                                    tmp1_ok = False
                                    break
                    for s in range(len(tmp2[l])):
                        if s not in obj.base.scatterlist:
                            if s not in obj.base.wildlist and s not in obj.base.ewildlist:
                                if tmp2[l][s] > (1/obj.window[0])*self.total[l] or tmp2[l][s] < Inf*self.total[l]:
                                    tmp2_ok = False
                                    break
                            else:
                                if tmp2[l][s] > (1/obj.window[1])*self.total[l] or tmp2[l][s] < wildInf*self.total[l]:
                                    tmp2_ok = False
                                    break
                if tmp1_ok:
                    distributions = distributions + [tmp1]
                if tmp2_ok:
                    distributions = distributions + [tmp2]

        #print('AAAA')
        self.points = [point(d) for d in distributions]

    def fillGroup(self, obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew):
        for p in self.points:
            p.fillPoint(obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
    def printGroup(self):
        print('root ', self.root.frequency[0], ' root value ', self.root.value, ' root base rtp = ', self.root.base_rtp, ' rtp = ', self.root.rtp , ' sdnew = ', self.root.sdnew, ' hitrate = ', self.root.hitrate)
        for i in range(len(self.points)):
            print(self.points[i].frequency[0], 'total = ', sum(self.points[i].frequency[0]),' value ', self.points[i].value)
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
        if not obj.base.symbol[i].scatter and not obj.base.symbol[i].wild:
            sortedSymbols.append(i)
    #пузырьковая сортировка, не думаю, что стоит мудрить с другой
    for i in range(len(sortedSymbols) - 1):
        for j in range(i + 1, len(sortedSymbols)):
            if obj.base.symbol[sortedSymbols[i]].payment[obj.window[0]] < obj.base.symbol[sortedSymbols[j]].payment[obj.window[0]]:
                sortedSymbols[i], sortedSymbols[j] = sortedSymbols[j], sortedSymbols[i]
    return sortedSymbols


def double_bouble(a, b):
    for i in range(len(a) - 1):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                b[i], b[j] = b[j], b[i]

#Здесь происходит некоторая херня с hitrate.

def SecondMethod(hitrate, err_hitrate, file_name):

    out = sm.get_scatter_frequency(file_name, hitrate, err_hitrate)
    if out == -1:
        exit('no free spins')

    t_distr, r_base_rtp, r_rtp, r_sdnew, r_hitrate, obj, roots = parametrs(file_name, out)



    base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew = 0.65, 0.9, 14, 0.001, 0.01, 0.01

    print('INITIAL POINTS, THEIR DISTRIBUTIONS, VALUES AND PARAMETRES:')
    a = []
    for root in roots:
        root.fillPoint(obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
        root.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
        print(root.frequency[0], ' value is ', root.value,'base_rtp, rtp, sdnew, hitrate :', root.base_rtp, root.rtp, root.sdnew, root.hitrate)
        a = a + [root.value]
    b = [i for i in range(len(a))]
    double_bouble(a, b) # здесь массив b - массив индексов начальных точек, упорядоченных по значению F


    print('assuming base rtp, rtp, sd ', base_rtp, rtp, sdnew)
    print('assuming errors for base rtp, rtp,  sd ', err_base_rtp, err_rtp, err_sdnew)

    b = [0] + b

    for i in b:
        print('TRYING POINT', roots[i].frequency[0], ' value is ', roots[i].value,'base_rtp, rtp, sdnew, hitrate :', roots[i].base_rtp, roots[i].rtp, roots[i].sdnew, roots[i].hitrate)

        root = roots[i]

        obj.base.create_simple_num_comb(obj.window, obj.line)
        obj.free.create_simple_num_comb(obj.window, obj.line)
        sortedSymbols = sortSymbols(obj)
        check = False
        min_is_found = False
        currentScale = 0
        while not min_is_found and currentScale < scaleLimit:
            number_of_groups = len(obj.base.wildlist) + len(obj.base.ewildlist) + 1
            while number_of_groups < len(sortedSymbols) + len(obj.base.wildlist) + len(obj.base.ewildlist) + 1:
                #print('is zis e los?')
                temp_group = group(root, number_of_groups, sortedSymbols, obj)
                print('группы ', temp_group.groups)
                temp_group.fillGroup(obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew )
                print('точки групп и значения в них')
                temp_group.printGroup()
                if temp_group.findMin() != -1:
                    if temp_group.findMin().value < 1:
                        min_is_found = True
                        print('ending with ', temp_group.findMin().value)
                        print('base ', temp_group.findMin().base_rtp)
                        print('rtp ', temp_group.findMin().rtp)
                        print('sdnew ', temp_group.findMin().sdnew)
                        print('hitrate ', temp_group.findMin().hitrate)
                        root = copy.deepcopy(temp_group.findMin())
                        print(root.frequency[0])
                        check = True
                        temp_group.findMin().printBaseReel(file_name)
                        break
                    else:
                        print('path ', temp_group.findMin().value)
                        root = copy.deepcopy(temp_group.findMin())
                else:
                    print(number_of_groups)
                    number_of_groups += 1
                    if number_of_groups >  (len(obj.base.wildlist) + len(obj.base.ewildlist) + len(sortedSymbols))/2:# and number_of_groups < len(sortedSymbols):
                        number_of_groups = len(sortedSymbols) + len(obj.base.wildlist) + len(obj.base.ewildlist)

            if not min_is_found:

                root = root.scaling()
                currentScale += 1
                print('SCALING ', currentScale)
            else:
                break
        if check:
            print('Блеск')
            break



SecondMethod(100, 1,'Games\HappyBrauer.txt')



