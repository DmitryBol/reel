import json
import FrontEnd.structure_alpha as Q
import time
import simple_functions_for_fit as sm
import copy
import numpy as np
from simple_functions_for_fit import notice_positions
from random import shuffle

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005


def sortSymbols(gametype):
    sortedSymbols = []
    for i in range(len(gametype.symbol)):
        if not gametype.symbol[i].scatter and not gametype.symbol[i].wild:
            sortedSymbols.append(i)
    #пузырьковая сортировка, не думаю, что стоит мудрить с другой
    for i in range(len(sortedSymbols) - 1):
        for j in range(i + 1, len(sortedSymbols)):
            #print(sortedSymbols)
            #print(sortedSymbols[i])

            if gametype.symbol[sortedSymbols[i]].payment[len(gametype.symbol[0].payment) - 1] < gametype.symbol[sortedSymbols[j]].payment[len(gametype.symbol[0].payment) - 1]:
                sortedSymbols[i], sortedSymbols[j] = sortedSymbols[j], sortedSymbols[i]
    return sortedSymbols

class Split:
    def __init__(self, gametype, number, frequency):
        self.frequency = frequency
        self.number = number

        sortedSymbols = sortSymbols(gametype)
        self.groups = []

        blocked_scatters = []
        for scatter_id in gametype.scatterlist:
            if max(gametype.symbol[scatter_id].scatter) > 0:
                blocked_scatters.append(scatter_id)
        if gametype.name == 'free':
            blocked_scatters = []

        for i in range(len(gametype.symbol)):
            if gametype.symbol[i].wild != False:
                self.groups.append([i])
            if gametype.symbol[i].scatter and i not in blocked_scatters:
                self.groups.append([i])

        c = 0
        t_number = number - len(self.groups)
        k = len(sortedSymbols)//t_number
        for i in range(t_number):
            g = []
            if c < len(sortedSymbols)%t_number:
                for j in range(c, k + c + 1):
                    g.append(sortedSymbols[i*k + j])
                c += 1
            else:
                for j in range(c, k + c):
                    g.append(sortedSymbols[i*k + j])
            self.groups.append(g)

    def balance(self, gametype):
        for group_ in self.groups:
            if len(group_) < 2:
                continue
            for reel_id in range(len(self.frequency)):
                blocked_symbols = [symbol_id for symbol_id in group_
                                   if reel_id not in gametype.symbol[symbol_id].position]
                group = list(set(group_) - set(blocked_symbols))
                group_count = sum([self.frequency[reel_id][group[i]] for i in range(len(group))])
                k = group_count // len(group)
                ost = group_count % len(group)
                for symbol_id in group:
                    self.frequency[reel_id][symbol_id] = k
                for j in range(ost):
                    self.frequency[reel_id][group[len(group) - 1 - j]] += 1



    def transfer(self, gametype ,source, destination, amount=1):
        new_frequency = copy.deepcopy(self.frequency)
        new_groups = copy.deepcopy(self.groups)
        totals = [sum(self.frequency[reel_id]) for reel_id in range(len(self.frequency))]

        for reel_id in range(len(new_frequency)):
            statement1 =  new_frequency[reel_id][source] - amount < 0
            statement2 = new_frequency[reel_id][destination] + amount > 0 and reel_id not in gametype.symbol[destination].position
            statement3 = False
            statement4 = False
            if source in gametype.wildlist:
                statement3 = new_frequency[reel_id][source] - amount < wildInf*totals[reel_id]
            if source in gametype.ewildlist:
                statement4 = new_frequency[reel_id][source] - amount < ewildInf*totals[reel_id]
            statement5 = new_frequency[reel_id][source] - amount < Inf*totals[reel_id]
            statement6 = new_frequency[reel_id][destination] + amount > gametype.max_border*totals[reel_id]

            if statement1 or statement2 or statement3 or statement4 or statement5 or statement6:
                continue
            else:
                new_frequency[reel_id][new_groups[source]] -= amount
                new_frequency[reel_id][new_groups[destination]] += amount

        if new_frequency == self.frequency:
            return None
        if gametype.check(new_frequency):
            return Split(gametype, self.number, new_frequency)
        return None
    '''
    def groupTransfer(self, gametype ,sourceGroup, destinationGroup):

        new_frequency = copy.deepcopy(self.frequency)
        k = len(self.groups[destinationGroup]) // len(self.groups[sourceGroup])
        ost = len(self.groups[destinationGroup]) % len(self.groups[sourceGroup])
        source_count = 0
        destination_count = 0
        totals = [sum(self.frequency[reel_id]) for reel_id in range(len(self.frequency))]
        for reel_id in range(len(new_frequency)):
            for i in range(len(self.groups[sourceGroup])):
                source = self.groups[sourceGroup][i]
                statement1 =  new_frequency[reel_id][source] - 1 < 0
                statement3 = False
                statement4 = False
                statement5 = False
                if source in gametype.wildlist:
                    statement3 = new_frequency[reel_id][source] - 1 < wildInf*totals[reel_id]
                if source in gametype.ewildlist:
                    statement4 = new_frequency[reel_id][source] - 1 < ewildInf*totals[reel_id]
                if source not in gametype.wildlist and source not in gametype.ewildlist and source not in gametype.scatterlist:
                    statement5 = new_frequency[reel_id][source] - 1 < Inf*totals[reel_id]

                if statement1 or statement3 or statement4 or statement5:
                    continue

                #new_frequency[reel_id][self.groups[sourceGroup][i]] = -1
                source_count += 1
            for i in range(len(self.groups[destinationGroup])):

                destination = self.groups[destinationGroup][i]
                statement2 = new_frequency[reel_id][destination] + k > 0 and reel_id not in gametype.symbol[destination].position
                statement6 = new_frequency[reel_id][destination] + k > gametype.max_border*totals[reel_id]

                if   statement2 or  statement6:
                    continue
                #new_frequency[reel_id][self.groups[destinationGroup][i]] = +k
                destination_count += 1

            for i in range(ost):
                destination = self.groups[destinationGroup][len(self.groups[destinationGroup]) - i - 1]
                statement2 = new_frequency[reel_id][destination] + 1 > 0 and reel_id not in gametype.symbol[destination].position
                statement6 = new_frequency[reel_id][destination] + 1 > gametype.max_border*totals[reel_id]
                if   statement2 or  statement6:
                    continue
                new_frequency[reel_id][self.groups[destinationGroup][len(self.groups[destinationGroup]) - i - 1]] = +1

        new_split = Split(gametype, self.number, new_frequency)
        new_split.balance(gametype)
        if gametype.check(new_split.frequency):
            return new_split
        else:
            return None
    '''

    def groupTransfer(self, gametype, sourceGroup, destinationGroup, rebalance=True):

        new_frequency = copy.deepcopy(self.frequency)

        totals = [sum(self.frequency[reel_id]) for reel_id in range(len(self.frequency))]
        moving_count = []
        for reel_id in range(len(new_frequency)):
            source_position = []
            for i in range(len(self.groups[sourceGroup])):
                source = self.groups[sourceGroup][i]
                statement1 =  new_frequency[reel_id][source] - 1 < 0
                statement3 = False
                statement4 = False
                statement5 = False
                statement7 = False
                if source in gametype.wildlist:
                    statement3 = new_frequency[reel_id][source] - 1 < wildInf*totals[reel_id]
                if source in gametype.ewildlist:
                    statement4 = new_frequency[reel_id][source] - 1 < ewildInf*totals[reel_id]
                if source not in gametype.wildlist and source not in gametype.ewildlist and source not in gametype.scatterlist:
                    statement5 = new_frequency[reel_id][source] - 1 < Inf*totals[reel_id]
                if source in gametype.scatterlist:
                    statement7 = new_frequency[reel_id][source] - 1 < scatterInf*totals[reel_id]

                if statement1 or statement3 or statement4 or statement5 or statement7:
                    continue
                source_position.append(source)

            destination_position = []
            for i in range(len(self.groups[destinationGroup])):

                destination = self.groups[destinationGroup][i]
                statement2 = new_frequency[reel_id][destination] + 1 > 0 and reel_id not in gametype.symbol[destination].position
                statement6 = new_frequency[reel_id][destination] + 1 > gametype.max_border*totals[reel_id]

                if   statement2 or  statement6:
                    continue
                destination_position.append(destination)

            moving_count.append(min(len(destination_position), len(source_position)))

            shuffle(source_position)
            shuffle(destination_position)
            for i in range(moving_count[reel_id]):
                new_frequency[reel_id][source_position[i]] -= 1
                new_frequency[reel_id][destination_position[i]] += 1

        if max(moving_count) == 0:
            return None
        new_split = Split(gametype, self.number, new_frequency)
        if rebalance:
            new_split.balance(gametype)
        if gametype.check(new_split.frequency):
            #print('new_split: ', new_split.frequency, new_split.groups)
            return new_split
        else:
            return None
