from builtins import str
from builtins import object


class Options(object):

    section_name = 'OPTIONS'

    unit_sys_si = 'SI'
    unit_sys_us = 'US'
    units_sys = [unit_sys_si, unit_sys_us]
    units_sys_text = {unit_sys_si: 'SI METRIC',
                      unit_sys_us: 'US CUSTOMARY'}

    units_diameter_pipes = {unit_sys_si: 'mm',
                            unit_sys_us: 'in'}

    units_diameter_tanks = {unit_sys_si: 'm',
                            unit_sys_us: 'ft'}

    units_flow = {unit_sys_si:
                      ['LPS', 'LPM', 'MLD', 'CMH', 'CMD'],
                  unit_sys_us:
                      ['CFS', 'GPM', 'MGD', 'IMGD', 'AFD']}

    units_flow_text = {'LPS': 'LPS - liters per second',
                       'LPM': 'LPM - liters per minute',
                       'MLD': 'MLD - million liters per day',
                       'CMH': 'CMH - cubic meters per hour',
                       'CMD': 'CMD - cubic meters per day',
                       'CFS': 'CFS - cubic feet per second',
                       'GPM': 'GPM - gallons per minute',
                       'MGD': 'MGD - million gallons per day',
                       'IMGD': 'IMGD - Imperial MGD',
                       'AFD': 'AFD - acre-feet per day'}  # TODO: sofcode

    units_deltaz = {unit_sys_si: 'm',
                   unit_sys_us: 'ft'}

    units_velocity = {unit_sys_si: 'm/s',
                      unit_sys_us: 'ft/s'}

    units_volume = {unit_sys_si: 'm3',
                    unit_sys_us: 'cb.ft'}

    headloss_hw = 'H-W'
    headloss_dw = 'D-W'
    headloss_cm = 'C-M'
    headlosses_text = {headloss_hw: 'Hazen-Williams',
                       headloss_dw: 'Darcy-Weisbach',
                       headloss_cm: 'Chezy-Manning'}

    units_power = {unit_sys_si: 'kW',
                   unit_sys_us: 'hp'}

    units_pressure = {unit_sys_si: 'm',
                      unit_sys_us: 'psi'}

    units_roughness = {unit_sys_si:
                           {headloss_hw: '-',
                            headloss_dw: 'mm',
                            headloss_cm: '-'},
                       unit_sys_us:
                           {headloss_hw: '-',
                            headloss_dw: '10-3 ft',
                            headloss_cm: '-'}
                       }

    def __init__(self):
        self.units = Options.unit_sys_si
        self.flow_units = Options.units_flow[self.units][0]
        self.headloss = Options.headloss_cm
        self.hydraulics = Hydraulics()
        self.quality = Quality()
        self.viscosity = 1
        self.spec_gravity = 1
        self.trials = 40
        self.accuracy = 0.001
        self.unbalanced = Unbalanced()
        self.pattern = None
        self.demand_mult = 1
        self.emitter_exp = 0.5
        self.diffusivity = 1
        self.tolerance = 0.01


class Hydraulics(object):

    action_use = 0
    action_save = 1

    action_names = {action_use: 'USE',
                    action_save: 'SAVE'}

    def __init__(self):
        self.use_hydraulics = False
        self.action = None
        self.file = None


class Quality(object):

    section_name = 'QUALITY'

    quality_none = 0
    quality_chemical = 1
    quality_age = 2
    quality_trace = 3

    quality_text = {quality_none: 'None',
                    quality_chemical: 'Chemical',
                    quality_age: 'Age',
                    quality_trace: 'Trace'}

    quality_units_mgl = 'mgL'
    quality_units_ugl = 'ugL'

    quality_units_text = {quality_units_mgl: 'mg/L',
                          quality_units_ugl: 'ug/L'}

    def __init__(self):
        self.parameter = Quality.quality_none
        self.mass_units = Quality.quality_units_mgl
        # self.diffusivity = 1
        self.trace_junction_id = None
        self.quality_tol = 0.01


class Unbalanced(object):
    unb_stop = 0
    unb_continue = 1

    unb_text = {unb_stop: 'Stop',
                unb_continue: 'Continue'}

    def __init__(self):
        self.unbalanced = Unbalanced.unb_stop
        self.trials = 0


class Times(object):

    section_name = 'TIMES'

    unit_sec = 0
    unit_min = 1
    unit_hr = 2
    unit_day = 3
    unit_text = {0: 'Second', 1: 'Minute', 2: 'Hour', 3: 'Day'}

    stats_avg = 0
    stats_min = 1
    stats_max = 2
    stats_range = 3
    stats_none = 4
    stats_text = {0: 'Average', 1: 'Minimum', 2: 'Maximum', 3: 'Range', 4: 'None'}

    def __init__(self):
        self.units = Times.unit_hr
        self.duration = Hour(1, 0)
        self.hydraulic_timestep = Hour(1, 0)
        self.quality_timestep = Hour(0, 5)
        self.rule_timestep = Hour(1, 0)
        self.pattern_timestep = Hour(1, 0)
        self.pattern_start = Hour(0, 0)
        self.report_timestep = Hour(1, 0)
        self.report_start = Hour(0, 0)
        self.clocktime_start = Hour(0, 0)
        self.statistic = Times.stats_none


class Hour(object):

    def __init__(self, hours, mins):
        self.hours = hours
        self.mins = mins

    @classmethod
    def from_string(cls, hhmm_string):

        words = hhmm_string.strip().split(':')
        return cls(int(words[0]), int(words[1]))

    def get_as_text(self, padding=2):
        return str(self.hours).zfill(padding) + ':' + str(self.mins).zfill(2)

    def get_as_hours(self):
        return self.hours + self.mins / 60.

    def get_as_mins(self):
        return self.hours * 60 + self.mins

    def set_from_string(self, hhmm_string):
        self.hours = int(hhmm_string[0:2])
        self.mins = int(hhmm_string[3:5])


class Report(object):

    section_name = 'REPORT'
    status_yes = 0
    status_no = 1
    status_full = 2

    summary_yes = 0
    summary_no = 1

    energy_yes = 0
    energy_no = 1

    nodes_none = 0
    nodes_all = 1
    nodes_ids = 2

    links_none = 0
    links_all = 1
    links_ids = 2

    status_names = {0: 'YES',
                    1: 'NO',
                    2: 'FULL'}

    summary_names = {0: 'YES',
                     1: 'NO'}

    energy_names = {0: 'YES',
                    1: 'NO'}

    nodes_names = {0: 'NONE',
                   1: 'ALL'}

    links_names = {0: 'NONE',
                   1: 'ALL'}

    def __init__(self):
        self.page_size = 0
        self.file = None
        self.status = Report.status_full
        self.summary = Report.summary_yes
        self.energy = Report.energy_yes
        self.nodes = Report.nodes_all
        self.nodes_ids = None
        self.links = Report.links_all
        self.links_ids = None

        # TODO: add parameters
