import copy
import numpy as np
from simple_functions_for_fit import notice_positions
from FrontEnd.structure_alpha import Gametype
from FrontEnd.structure_alpha import Game
from FrontEnd.reelWork.reel_generator_alpha import reel_generator

Inf = 0.05
wildInf = 0.025
ewildInf = 0.015


class GametypePoint:
    def __init__(self, frequency, gametype):
        self.frequency = notice_positions(frequency, gametype)
        self.reels = None
        self.type_name = gametype.name
        return

    def generate_reels(self, gametype: Gametype, frequency=None):
        if self.frequency is None and frequency is None:
            raise Exception('None frequency during reel generator')
        if frequency is not None:
            self.frequency = frequency
        self.reels = reel_generator(gametype=gametype, frequency_array=self.frequency, window_width=gametype.window[0],
                                    reel_distance=gametype.distance, validate=False)
        return

    def scaling(self, scale=2):
        for reel_id in range(len(self.frequency)):
            for symbol_id in range(len(self.frequency[reel_id])):
                self.frequency[reel_id][symbol_id] *= scale
        return

    def fill(self, gametype, frequency=None, shuffle=False):
        if shuffle:
            self.generate_reels(gametype, frequency)

        gametype.fill_frequency(self.frequency)
        gametype.fill_reels(self.reels)

        gametype.fill_count_killed(gametype.window[0])
        gametype.fill_simple_num_comb(gametype.window, gametype.lines)
        gametype.fill_scatter_num_comb(gametype.window)
        return

    def print_reels(self, file, max_symbol_length=15):
        max_length = 0
        for reel_id in range(len(self.reels)):
            if len(self.reels[reel_id]) > max_length:
                max_length = len(self.reels[reel_id])
        for symbol_id in range(max_length):
            out_str = ''
            for reel_id in range(len(self.reels)):
                if symbol_id < len(self.reels[reel_id]):
                    t = (max_symbol_length - len(self.reels[reel_id][symbol_id].name)) * ' '
                    out_str = out_str + self.reels[reel_id][symbol_id].name + t
                else:
                    out_str = max_symbol_length * ' '
            file.write(out_str + '\n')
            file.write('\n')


class Point:
    def __init__(self, main_frequency, second_frequency, game: Game, main_type='base'):
        if main_type == 'base':
            self.base = GametypePoint(main_frequency, game.base)
            self.free = GametypePoint(second_frequency, game.free)
        elif main_type == 'free':
            self.base = GametypePoint(second_frequency, game.base)
            self.free = GametypePoint(main_frequency, game.free)
        else:
            raise Exception('Not supported gametype')

        self.base_rtp = '-1'
        self.rtp = '-1'
        self.sdnew = '-1'
        self.hitrate = '-1'
        self.value = '-1'

    def get_value(self):
        return self.value

    def get_base_frequency(self):
        return self.base.frequency

    def get_free_frequency(self):
        return self.free.frequency

    def check(self, game: Game):
        return game.base.check(self.get_base_frequency()) and game.free.check(self.get_free_frequency())

    def metric(self, params, base=True, sd_flag=False):
        base_rtp = params['base_rtp']
        rtp = params['rtp']
        sdnew = params['sdnew']
        err_base_rtp = params['err_base_rtp']
        err_rtp = params['err_rtp']
        err_sdnew = params['err_sdnew']
        metrics_list = []

        if base:
            metrics_list.append(np.fabs(base_rtp - self.base_rtp) / err_base_rtp)
        else:
            metrics_list.append(np.fabs(rtp - self.rtp) / err_rtp)
            if sd_flag:
                metrics_list.append(np.fabs(sdnew - self.sdnew) / err_sdnew)
        return max(metrics_list)

    def fill_point_metric(self, params, base=True, sd_flag=False):
        self.value = self.metric(params, base=base, sd_flag=sd_flag)

    def scaling(self, scale=2, base=True):
        if base:
            self.base.scaling(scale=scale)
        else:
            self.free.scaling(scale=scale)

    def fill_point(self, game, params, base=True, sd_flag=False,
                   base_shuffle=True, free_shuffle=True):
        if base:
            self.base.fill(game.base, shuffle=base_shuffle)
        self.free.fill(game.free, shuffle=free_shuffle)

        point_params = game.count_parameters(base, sd_flag)

        self.base_rtp, self.rtp, self.sdnew, self.hitrate = point_params['base_rtp'], point_params['rtp'], point_params[
            'sdnew'], point_params['hitrate']

        self.fill_point_metric(params, base, sd_flag)

    def print_reels(self, file_name):
        file_name_base = file_name[:file_name.find('\\') + 1] + "Base Reels\\" + file_name[file_name.find('\\') + 1:]
        file_base = open(file_name_base, 'w')
        file_name_free = file_name[:file_name.find('\\') + 1] + "Free Reels\\" + file_name[file_name.find('\\') + 1:]
        file_free = open(file_name_free, 'w')

        self.base.print_reels(file_base)
        self.free.print_reels(file_free)

        file_base.close()
        file_free.close()

    def collect_params(self, game):
        temp_game = copy.deepcopy(game)
        temp_game.base.reels = copy.deepcopy(self.base.reels)
        temp_game.free.reels = copy.deepcopy(self.free.reels)
        temp_game.base.frequency = copy.deepcopy(self.base.frequency)
        temp_game.free.frequency = copy.deepcopy(self.free.frequency)
        params = temp_game.standalone_count_parameters(shuffle=False)
        self.base_rtp = params['base_rtp']
        self.rtp = params['rtp']
        self.sdnew = params['sdnew']
        self.hitrate = params['hitrate']
