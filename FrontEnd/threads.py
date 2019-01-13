from PyQt5.QtCore import *
import FrontEnd.structure_alpha as structure
from Descent.main_process import main_process
import simulate


class Threaded(QObject):
    generate_reels_result = pyqtSignal()
    count_parameters_result = pyqtSignal(dict)
    simulation_result = pyqtSignal(dict)

    def __init__(self):
        super(Threaded, self).__init__()

    @pyqtSlot(structure.Game, str)
    def generate_reels(self, game: structure.Game, output):
        output_file = open(output, "w")
        game = main_process(game_structure=game, out_log=output_file)
        output_file.close()
        print("reels on generate_reels end: ", game.base.reels)
        self.generate_reels_result.emit()

    @pyqtSlot(structure.Game)
    def count_parameters(self, game: structure.Game):
        print("reels on count_parameters start: ", game.base.reels)
        print("frequency on count_parameters start: ", game.base.frequency)
        parameters = game.standalone_count_parameters()
        self.count_parameters_result.emit(parameters)

    @pyqtSlot(structure.Game)
    def simulation(self, game):
        simparam = simulate.make_spins(game)
        self.simulation_result.emit(simparam)
