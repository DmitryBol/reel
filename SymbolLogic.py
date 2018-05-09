import copy


class Wild:
    multiplier = 1
    expand = False
    substitute = []

    def __init__(self):
        self.multiplier = 1
        self.expand = False
        self.substitute = []

    def __init__(self, _multiplier=1, _expand=False, _substitute=None):
        if _multiplier is not None:
            self.multiplier = copy.deepcopy(_multiplier)
        else:
            self.multiplier = 1
        if _expand is not None:
            self.expand = copy.deepcopy(_expand)
        else:
            self.expand = False
        if _substitute is not None:
            self.substitute = copy.deepcopy(_substitute)
        else:
            self.substitute = None


class SymbolLogic:
    direction = 'left'
    position = None
    scatter = None
    wild = Wild()

    def set_position(self, _position, _length):
        if _position is None:
            self.position = [i + 1 for i in range(_length)]
        else:
            self.position = copy.deepcopy(_position)

    def set_direction(self, _direction):
        if _direction is None:
            self.direction = 'left'
        else:
            self.direction = copy.deepcopy(_direction)

    def set_scatter(self, _scatter):
        if _scatter is None:
            self.scatter = None
        else:
            self.scatter = copy.deepcopy(_scatter)

    def set_wild(self, _wild):
        if _wild is None:
            self.wild = None
        else:
            self.wild = Wild(_wild.get('multiplier'), _wild.get('expand'), _wild.get('substitute'))

    def __init__(self, window_length):
        self.direction = 'left'
        self.position = [i + 1 for i in range(window_length)]
        self.scatter = None
        self.wild = Wild()

    def __init__(self, json_data, window_length):
        if json_data is not None:
            self.set_position(json_data.get('position'), window_length)
            self.set_direction(json_data.get('direction'))
            self.set_scatter(json_data.get('scatter'))
            self.set_wild(json_data.get('wild'))
        else:
            self.direction = 'left'
            self.position = [i + 1 for i in range(window_length)]
            self.scatter = None
            self.wild = Wild()

    def copy_structure(self, logic):
        self.wild = copy.deepcopy(logic.wild)
        self.scatter = copy.deepcopy(logic.scatter)
        self.direction = copy.deepcopy(logic.direction)
        self.position = copy.deepcopy(logic.position)

    def __init__(self, base_logic, json_data, window_length):
        self.copy_structure(base_logic)
        if json_data is not None:
            if json_data.get('position') is not None:
                self.set_position(json_data.get('position'), window_length)
            if json_data.get('direction') is not None:
                self.set_direction(json_data.get('direction'))
            if json_data.get('scatter') is not None:
                self.set_scatter(json_data.get('scatter'))
            if json_data.get('wild') is not None:
                self.set_wild(json_data.get('wild'))
