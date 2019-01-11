import simulate
from Descent.main_process import main_process

all_games = ['Games/HappyBrauer.txt']

L = len(all_games)

for index in range(L):
    out_log = open('out_' + str(index) + '.txt', 'w')
    borders_plot_name = 'plot_' + str(index) + '.png'
    game = main_process(game_name=all_games[index], out_log=out_log, plot_name=borders_plot_name)
    out_log.close()

    simulate_result = simulate.make_spins(game, count=1_000_000)
    print('\n\nsimulate base rtp: ', simulate_result['base_rtp'], '\nsimulate rtp: ', simulate_result['rtp'],
          '\nsimulate sd: ', simulate_result['sd'])
