import copy
from random import shuffle
from FrontEnd.structure_alpha import Gametype

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015
scatterInf = 0.005


def sort_symbols(gametype):
    sorted_symbols = []
    for i in range(len(gametype.symbol)):
        if not gametype.symbol[i].scatter and not gametype.symbol[i].wild:
            sorted_symbols.append(i)
    # пузырьковая сортировка, не думаю, что стоит мудрить с другой
    for i in range(len(sorted_symbols) - 1):
        for j in range(i + 1, len(sorted_symbols)):
            if gametype.symbol[sorted_symbols[i]].payment[len(gametype.symbol[0].payment) - 1] < \
                    gametype.symbol[sorted_symbols[j]].payment[len(gametype.symbol[0].payment) - 1]:
                sorted_symbols[i], sorted_symbols[j] = sorted_symbols[j], sorted_symbols[i]
    return sorted_symbols


class Split:
    def __init__(self, gametype, number_of_partition_groups, frequency):
        self.frequency = frequency
        self.number_of_partition_groups = number_of_partition_groups

        sortedSymbols = sort_symbols(gametype)
        self.groups = []

        blocked_scatters = []
        for scatter_id in gametype.scatterlist:
            if max(gametype.symbol[scatter_id].scatter) > 0:
                blocked_scatters.append(scatter_id)
        if gametype.name == 'free':
            blocked_scatters = []

        for symbol_id in range(len(gametype.symbol)):
            if gametype.symbol[symbol_id].wild and symbol_id not in blocked_scatters:
                self.groups.append([symbol_id])
            if gametype.symbol[symbol_id].scatter and symbol_id not in blocked_scatters:
                self.groups.append([symbol_id])

        c = 0
        max_partition_len = number_of_partition_groups - len(self.groups)
        changed_partition_groups_count = len(sortedSymbols) // max_partition_len
        for symbol_id in range(max_partition_len):
            g = []
            if c < len(sortedSymbols) % max_partition_len:
                for j in range(c, changed_partition_groups_count + c + 1):
                    g.append(sortedSymbols[symbol_id * changed_partition_groups_count + j])
                c += 1
            else:
                for j in range(c, changed_partition_groups_count + c):
                    g.append(sortedSymbols[symbol_id * changed_partition_groups_count + j])
            self.groups.append(g)
        return

    def balance(self, gametype):
        for group_ in self.groups:
            if len(group_) < 2:
                continue
            for reel_id in range(len(self.frequency)):
                blocked_symbols = [symbol_id for symbol_id in group_
                                   if reel_id not in gametype.symbol[symbol_id].position]
                group = list(set(group_) - set(blocked_symbols))
                group_sum = sum([self.frequency[reel_id][group[i]] for i in range(len(group))])
                partition_len = group_sum // len(group)
                ost = group_sum % len(group)
                for symbol_id in group:
                    self.frequency[reel_id][symbol_id] = partition_len
                for j in range(ost):
                    self.frequency[reel_id][group[len(group) - 1 - j]] += 1
        return

    def group_transfer(self, gametype: Gametype, source_group, destination_group, balance=True):
        new_frequency = copy.deepcopy(self.frequency)

        totals = [sum(self.frequency[reel_id]) for reel_id in range(len(self.frequency))]
        moving_count = []
        for reel_id in range(len(new_frequency)):
            source_position = []
            for i in range(len(self.groups[source_group])):
                source = self.groups[source_group][i]
                zero_symbols_after_take = new_frequency[reel_id][source] - 1 < 0
                less_that_wild_inf = False
                less_than_ewild_inf = False
                less_than_inf = False
                less_than_scatter_inf = False
                if source in gametype.wildlist:
                    less_that_wild_inf = new_frequency[reel_id][source] - 1 < wildInf * totals[reel_id]
                if source in gametype.ewildlist:
                    less_than_ewild_inf = new_frequency[reel_id][source] - 1 < ewildInf * totals[reel_id]
                if source not in gametype.wildlist and source not in gametype.ewildlist and source not in gametype.scatterlist:
                    less_than_inf = new_frequency[reel_id][source] - 1 < Inf * totals[reel_id]
                if source in gametype.scatterlist:
                    less_than_scatter_inf = new_frequency[reel_id][source] - 1 < scatterInf * totals[reel_id]

                if zero_symbols_after_take or less_that_wild_inf or less_than_ewild_inf or less_than_inf or less_than_scatter_inf:
                    continue
                source_position.append(source)

            destination_position = []
            for i in range(len(self.groups[destination_group])):

                destination = self.groups[destination_group][i]
                cant_be_on_reel = new_frequency[reel_id][destination] + 1 > 0 and reel_id not in gametype.symbol[
                    destination].position
                more_than_max_border = new_frequency[reel_id][destination] + 1 > gametype.max_border * totals[reel_id]

                if cant_be_on_reel or more_than_max_border:
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
        new_split = Split(gametype, self.number_of_partition_groups, new_frequency)
        if balance:
            new_split.balance(gametype)
        if gametype.check(new_split.frequency):
            return new_split
        else:
            return None
