import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np
from simple_functions_for_fit import notice_positions

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015


class Point:
    def __init__(self, frequency_base, frequency_free, game):
        self.baseFrequency = notice_positions(frequency_base, game.base)
        self.freeFrequency = notice_positions(frequency_free, game.free)
        self.baseReel = '-1'
        self.freeReel = '-1'
        self.base_rtp = '-1'
        self.rtp = '-1'
        self.sdnew = '-1'
        self.hitrate = '-1'
        self.value = '-1'

    def getValue(self):
        return self.value

    def check(self, game):
       return game.base.check(self.baseFrequency) and game.free.check(self.freeFrequency)

    def F(self, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True, sd_flag=False):
        t = []

        if base:
            t.append(np.fabs(base_rtp - self.base_rtp)/err_base_rtp)
        else:
            t.append(np.fabs(rtp - self.rtp)/err_rtp)
            if sd_flag:
                t.append(np.fabs(sdnew - self.sdnew)/err_sdnew)

        return max(t)

    def fillVal(self, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True, sd_flag=False):
        self.value = self.F(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=base, sd_flag=sd_flag)

    def scaling(self, scale=2, base=True):
        if base:
            for i in range(len(self.baseFrequency)):
                for j in range(len(self.baseFrequency[i])):
                    self.baseFrequency[i][j] = scale*self.baseFrequency[i][j]
        else:
            for i in range(len(self.freeFrequency)):
                for j in range(len(self.freeFrequency[i])):
                    self.freeFrequency[i][j] = scale*self.freeFrequency[i][j]

    def fillPoint(self, obj, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=True, sd_flag=False):
        if base:
            obj.base.reel_generator(self.baseFrequency, obj.window[0], obj.window[1])
            self.baseReel = obj.base.reels
            obj.base.fill_frequency(self.baseFrequency)
            obj.base.fill_count_killed(obj.window[0])

            obj.base.fill_simple_num_comb(obj.window, obj.line)
            obj.base.fill_scatter_num_comb(obj.window)

        obj.free.reel_generator(self.freeFrequency, obj.window[0], obj.window[1])
        obj.free.fill_frequency(self.freeFrequency)

        obj.free.fill_count_killed(obj.window[0])
        obj.free.fill_simple_num_comb(obj.window, obj.line)
        obj.free.fill_scatter_num_comb(obj.window)

        self.freeReel = obj.free.reels

        params = obj.count_parameters(base, sd_flag)


        self.base_rtp, self.rtp, self.sdnew, self.hitrate = params['base_rtp'], params['rtp'], params['sdnew'], params['hitrate']

        self.fillVal(base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base, sd_flag)


    def printReel(self, file):
        max_length = 0
        file = file[:file.find('\\') + 1] + "Base Reels\\" + file[file.find('\\') + 1:]
        f = open(file, 'w')
        file1 = file[:file.find('\\') + 1] + "Free Reels\\" + file[file.find('\\') + 1:]
        f1 = open(file1, 'w')
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


        for l in range(len(self.freeReel)):
            if len(self.freeReel[l]) > max_length:
                max_length = len(self.freeReel[l])
        for i in range(max_length):
            s = ''
            for l in range(len(self.freeReel)):
                if i < len(self.freeReel[l]):
                    t = (15 - len(self.freeReel[l][i].name))*' '
                    s = s + self.freeReel[l][i].name + t
                else:
                    s = 15*' '
            f1.write(s + '\n')
            f1.write('\n')
            #print('\n')
            #print(s)
        f.close()
        f1.close()


