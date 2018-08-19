class Neighbourhood(object):
    def __init__(self, root, game, blocked_scatters, all_wilds, groups):
        self.root = root
        self.neighbour = []


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