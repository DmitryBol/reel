from PyQt5.QtCore import *
import FrontEnd.structure_alpha as structure
import simulate


class Threaded(QObject):
    count_parameters_result = pyqtSignal(dict)
    simulation_result = pyqtSignal(dict)

    def __init__(self):
        super(Threaded, self).__init__()

    @pyqtSlot(structure.Game)
    def count_parameters(self, game):
        parameters = game.standalone_count_parameters()
        self.count_parameters_result.emit(parameters)

    @pyqtSlot(structure.Game)
    def simulation(self, game):
        simparam = simulate.make_spins(game)
        self.simulation_result.emit(simparam)
