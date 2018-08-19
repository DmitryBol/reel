import math


def F(real_base_rtp, base_rtp, err_base_rtp, real_hitrate, hitrate, err_hitrate):
    params_list = [math.fabs((real_base_rtp - base_rtp) / err_base_rtp),
                   math.fabs((real_hitrate - hitrate) / err_hitrate)]
    return max(params_list)


class Point:
    def __init__(self, frequency):
        self.frequency = frequency
        self.base_rtp = -1
        self.hitrate = -1
        self.value = -1
        self.base_reels = []
        return

    def fill_val(self, base_rtp, err_base_rtp, hitrate, err_hitrate):
        return F(self.base_rtp, base_rtp, err_base_rtp, self.hitrate, hitrate, err_hitrate)

    def scaling(self, scale=2):
        window_width = len(self.frequency)
        n_symbols = 0
        if window_width > 0:
            n_symbols = len(self.frequency[0])
        for reel_id in range(window_width):
            for symbol_id in range(n_symbols):
                self.frequency[reel_id][symbol_id] *= scale
        return

    def fill_point(self, obj, base_rtp, err_base_rtp, hitrate, err_hitrate):

        n_symbols = len(obj.base.symbol)
        for symbol_id in range(n_symbols):
            for reel_id in range(obj.window[0]):
                if reel_id in obj.base.symbol[symbol_id].position:
                    continue
                else:
                    self.frequency[reel_id][symbol_id] = 0

        obj.base.reel_generator(self.frequency, obj.window[0], obj.window[1])
        obj.base.fill_frequency(self.frequency)

        obj.base.fill_count_killed(obj.window[0])
        # obj.base.create_simple_num_comb(obj.window, obj.line)
        obj.base.fill_simple_num_comb(obj.window, obj.line)
        obj.base.fill_scatter_num_comb(obj.window)

        self.base_reels = obj.base.reels

        params = obj.count_parameters()
        self.base_rtp, self.hitrate = params['base_rtp'], params['hitrate']
        self.fill_val(base_rtp=base_rtp, err_base_rtp=err_base_rtp,
                      hitrate=hitrate, err_hitrate=err_hitrate)
        return

    def printBaseReel(self, file):
        max_length = 0
        file = file[:file.find('\\') + 1] + "Base Reels\\" + file[file.find('\\') + 1:]
        f = open(file, 'w')
        for l in range(len(self.base_reels)):
            if len(self.base_reels[l]) > max_length:
                max_length = len(self.base_reels[l])
        for i in range(max_length):
            s = ''
            for l in range(len(self.base_reels)):
                if i < len(self.base_reels[l]):
                    t = (15 - len(self.base_reels[l][i].name)) * ' '
                    s = s + self.base_reels[l][i].name + t
                else:
                    s = 15 * ' '
            f.write(s + '\n')
            f.write('\n')
        f.close()
