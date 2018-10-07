from Descent.main_process import main_process

all_games = ['Games/Shining_Crown.txt']

L = len(all_games)

MAX_REBALANCE_COUNT = 5

for index in range(L):
    out_log = open('out_' + str(index) + '.txt', 'w')
    borders_plot_name = 'plot_' + str(index) + '.png'
    main_process(game_name=all_games[index], out_log=out_log,
                 max_rebalance_count=MAX_REBALANCE_COUNT, plot_name=borders_plot_name)
    out_log.close()

    # simulate_result = simulate.make_spins(game, count=1_000_000)
    # print('simulate rtp: ', simulate_result['rtp'], '\tsimulate sd: ', simulate_result['sd'])
