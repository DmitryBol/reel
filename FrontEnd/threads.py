from PyQt5.QtCore import *
import FrontEnd.structure_alpha as structure
from Descent.main_process import main_process
import simulate


class Threaded(QObject):
    generate_reels_result = pyqtSignal(str)
    count_parameters_result = pyqtSignal(dict)
    simulation_result = pyqtSignal(dict)

    def __init__(self):
        super(Threaded, self).__init__()

    @pyqtSlot(structure.Game, str)
    def generate_reels(self, game, output):
        main_process(game_structure=game, out_log=output)
        self.generate_reels_result.emit()

    @pyqtSlot(structure.Game)
    def count_parameters(self, game):
        parameters = game.standalone_count_parameters()
        self.count_parameters_result.emit(parameters)

    @pyqtSlot(structure.Game)
    def simulation(self, game):
        simparam = simulate.make_spins(game)
        self.simulation_result.emit(simparam)
