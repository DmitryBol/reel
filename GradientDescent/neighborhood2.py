import json
import FrontEnd.structure_alpha as Q
import simple_functions_for_fit as sm


def parse_scatter_frequency(out, hitrate, game):

    if out == -1 and hitrate != -1:
        exit('no free games but you asked them')
    elif out == -1:
        out = sm.OutResult(game.base.scatterlist)
        out.add_symbols(game.base.symbol)

    blocked_scatters = []
    for scatter_id in game.base.scatterlist:
        if max(game.base.symbol[scatter_id].scatter) > 0:
            blocked_scatters.append(scatter_id)
    return out, blocked_scatters


def fill_roots():
    res = []
    return res


def fit_base_rtp(file_name, hitrate, err_hitrate, base_rtp, err_base_rtp):
    file = open(file_name, 'r')
    j = file.read()
    interim = json.loads(j)
    game = Q.Game(interim)
    file.close()
    out = sm.get_scatter_frequency(file_name, hitrate, err_hitrate)
    out, blocked_scatters = parse_scatter_frequency(out=out, hitrate=hitrate, game=game)
    all_wilds = game.base.wildlist + game.base.ewildlist
    game.base.create_simple_num_comb(game.window, game.line)

    print('blocked_scatters:', blocked_scatters, 'all_wilds:', all_wilds)
    print(out.total_scats, out.total_length, out.scatter_index_with_frequency)

    roots = fill_roots
