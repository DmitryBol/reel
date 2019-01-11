import copy
from Descent.Point import Point
from Descent.Split import Split

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015


class Group:
    def __init__(self, game, type_name, root: Point, number_of_groups, params, rebalance=True, sd_flag=True, base_reels=None):
        self.root = root

        base_flag = True

        if type_name == 'base':
            gametype = game.base
            main_frequency = root.get_base_frequency()
            second_frequency = root.get_free_frequency()
        elif type_name == 'free':
            gametype = game.free
            main_frequency = root.get_free_frequency()
            second_frequency = root.get_base_frequency()
            base_flag = False
        else:
            raise Exception('Not supported gametype')

        self.total = [sum(i) for i in main_frequency]
        self.split = Split(gametype, number_of_groups, main_frequency)
        self.points = []
        for i in range(number_of_groups - 1):
            for j in range(i + 1, number_of_groups):
                group1 = self.split.group_transfer(gametype, i, j, balance=rebalance)
                # print('group1: ', group1)
                if group1:
                    new_point = Point(main_frequency=group1.frequency, second_frequency=second_frequency, game=game,
                                      main_type=type_name, base_reels=base_reels)
                    new_point.fill_point(game, params, base=base_flag, sd_flag=sd_flag)
                    self.points.append(new_point)
                group2 = self.split.group_transfer(gametype, j, i, balance=rebalance)
                if group2:
                    new_point = Point(main_frequency=group2.frequency, second_frequency=second_frequency, game=game,
                                      main_type=type_name, base_reels=base_reels)
                    new_point.fill_point(game, params, base=base_flag, sd_flag=sd_flag)
                    self.points.append(new_point)
        # print('group length: ', len(self.points))

    def find_best_point(self):
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

    def print_group(self, type_name='base'):
        for point in self.points:
            if type_name == 'base':
                print('point value: ', point.value, point.base.frequency)
            elif type_name == 'free':
                print('point value: ', point.value, 'rtp: ', point.rtp, 'base_rtp: ', point.base_rtp,
                      'sdnew: ', point.sdnew, point.base.frequency, point.free.frequency)
            else:
                raise Exception('Not supported gametype')
