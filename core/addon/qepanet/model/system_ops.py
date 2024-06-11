from builtins import object
class Curve(object):
    section_name = 'CURVES'
    section_header = 'ID              	X-Value                 Y-Value'

    type_volume = 0
    type_pump = 1
    type_efficiency = 2
    type_headloss = 3

    type_names = {type_volume: 'Volume',
                  type_pump: 'Pump',
                  type_efficiency: 'Efficiency',
                  type_headloss: 'Headloss'}

    def __init__(self, id, type=None, desc=None):
        self.id = id
        self.type = type
        self.desc = desc
        self.xs = []
        self.ys = []

    def append_xy(self, x, y):
        self.xs.append(x)
        self.ys.append(y)


class Controls(object):
    section_name = 'CONTROLS'

    def __init__(self):
        pass


class Demand(object):
    section_name = 'DEMANDS'
    section_header = 'Junction        	Demand      	Pattern         	Category'

    def __init__(self):
        pass


class Energy(object):

    section_name = 'ENERGY'

    def __init__(self):
        self.pump_efficiency = 75
        self.energy_price = 0
        self.price_pattern = None
        self.demand_charge = 0


class Pattern(object):
    section_name = 'PATTERNS'
    section_header = 'ID              	Multipliers'

    def __init__(self, id, desc=None, values=None):
        self.id = id
        self.desc = desc
        if values is None:
            self.values = []
        else:
            self.values = values[:]

    def add_value(self, val):
        self.values.append(val)


class Rule(object):
    section_name = 'RULES'

    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action


class Status(object):
    section_name = 'STATUS'
    section_header = 'ID              	Status/Setting'

    def __init__(self):
        pass