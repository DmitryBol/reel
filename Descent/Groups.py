import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np
from Descent.Point import Point
from Descent.Split import Split
from simple_functions_for_fit import notice_positions

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015


class Group:
    def __init__(self, game, type, root, number, params):
        self.root = root
        base_rtp = params['base_rtp']
        rtp = params['rtp']
        sdnew = params['sdnew']
        err_base_rtp = params['err_base_rtp']
        err_rtp = params['err_rtp']
        err_sdnew = params['err_sdnew']

        if type == 'base':
            gametype = game.base

            self.total = [sum(i) for i in root.baseFrequency]
            self.split = Split(gametype, number, root.baseFrequency)
            self.points = []
            for i in range(number - 1):
                for j in range(i + 1, number):
                    group1 = self.split.groupTransfer(gametype, i, j)
                    if group1:
                        self.points.append(
                            Point(root.baseFrequency, group1.frequency, game).fillPoint(
                                game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
                        )
                    group2 = self.split.groupTransfer(gametype, j, i)
                    if group2:
                        self.points.append(
                            Point(root.baseFrequency, group2.frequency, game).fillPoint(
                                game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew)
                        )

        elif type == 'free':
            gametype = game.free
            self.total = [sum(i) for i in root.freeFrequency]
            self.split = Split(gametype, number, root.freeFrequency)
            self.points = []
            for i in range(number - 1):
                for j in range(i + 1, number):
                    group1 = self.split.groupTransfer(gametype, i, j)
                    if group1:
                        self.points.append(
                            Point(root.baseFrequency, group1.frequency, game).fillPoint(
                                game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False, sd_flag=True)
                        )
                    group2 = self.split.groupTransfer(gametype, j, i)
                    if group2:
                        self.points.append(
                            Point(root.baseFrequency, group2.frequency, game).fillPoint(
                                game, base_rtp, rtp, sdnew, err_base_rtp, err_rtp, err_sdnew, base=False, sd_flag=True)
                        )
        else:
            exit('Not supported gametype')

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
