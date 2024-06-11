from builtins import str
from builtins import range
from builtins import object
import codecs
import os

from collections import OrderedDict
#from .network import Title, Junction, Reservoir, Tank, Pipe, Pump, Valve, Emitter, Coordinate, Tag, QJunction,\
#    QReservoir, QTank, QPipe, Vertex, QOptions, QVertices
#from qgis.core import NULL, QgsSpatialIndex, QgsVertexId
from .system_ops import Controls, Curve, Demand, Energy, Pattern, Rule, Status
import math
from ..model.options_report import Times, Report
from .options_report import Options, Quality
#from ..model.network_handling import NetworkUtils
#from ..model.water_quality import Reactions


class InpFile():
    
    pad_19 = 19
    pad_22 = 22

    def __init__(self):
        self.tags = []

    @staticmethod
    def read_patterns(params, patterns_file):

        if not os.path.isfile(patterns_file):
            return []

        start_line = None
        end_line = None
        with codecs.open(patterns_file, 'r', encoding='UTF-8') as inp_f:

            lines = inp_f.read().splitlines()
            patterns_started = False
            for l in range(len(lines)):
                if lines[l].upper().startswith('[PATTERNS]'):
                    patterns_started = True
                    start_line = l + 1
                    continue
                if lines[l].startswith('[') and patterns_started:
                    end_line = l - 1
                    break

        if start_line is None:
            params.patterns = OrderedDict()
            return

        if end_line is None:
            end_line = len(lines)

        patterns_d = OrderedDict()
        for l in range(start_line, end_line):
            if not lines[l].startswith(';') and lines[l].strip(' \t') != '':
                words = lines[l].strip().replace('\t', ' ').split()
                if words[0] not in patterns_d:
                    if lines[l-1].strip().startswith(';') and lines[l-3].startswith('['):
                        pattern_desc = lines[l - 1][1:]
                    else:
                        pattern_desc = ''
                    patterns_d[words[0]] = Pattern(words[0], pattern_desc)
                    for w in range(1, len(words)):
                        patterns_d[words[0]].add_value(float(words[w]))
                    continue
                else:
                    for w in range(1, len(words)):
                        patterns_d[words[0]].add_value(float(words[w]))

        params.patterns = patterns_d

    def write_patterns(self, params, inp_file_path):

        # Rewrite whole file
        with codecs.open(inp_file_path, 'w', encoding='UTF-8') as p_file:

            out = []
            InpFile._append_patterns(params, out)

            for line in out:
                p_file.write(line + '\n')

    def write_lines(self, inp_file, lines):

        if type(lines) is str:
            inp_file.write(lines + '\n')
        else:
            for line in lines:
                inp_file.write(line + '\n')

    @staticmethod
    def read_curves(params, curves_file):

        if not os.path.isfile(curves_file):
            return []

        start_line = 0
        end_line = None
        with codecs.open(curves_file, 'r', encoding='UTF-8') as inp_f:

            lines = inp_f.read().splitlines()
            for l in range(len(lines)):
                lines[l] = lines[l].strip()

            curves_started = False
            for l in range(len(lines)):
                if lines[l].upper().startswith('[CURVES]'):
                    curves_started = True
                    start_line = l + 1
                    continue
                if lines[l].startswith('[') and curves_started:
                    end_line = l - 1
                    break

        if end_line is None:
            end_line = len(lines)

        curves_d = {}

        for l in range(start_line, end_line):
            if not lines[l].startswith(';'):
                if len(lines[l].strip()) == 0:
                    continue
                words = lines[l].replace('\t', ' ').split()
                if words[0] not in curves_d:

                    curve_metadata = lines[l-1]
                    curve_type = 0
                    curve_desc = None
                    if curve_metadata.startswith(';'):

                        curve_type = 0
                        cruve_desc = None
                        for type_id, type_name in Curve.type_names.items():
                            if curve_metadata.lower()[1:].startswith(type_name.lower()):
                                curve_type = type_id
                                curve_metadatas = curve_metadata.split(':')
                                if len(curve_metadatas) > 1:
                                    curve_desc = curve_metadatas[1].strip()
                                break

                    curves_d[words[0]] = Curve(words[0], curve_type, curve_desc)
                    x = words[1]
                    y = words[2]
                    curves_d[words[0]].append_xy(x, y)
                    continue
                else:
                    x = words[1]
                    y = words[2]
                    curves_d[words[0]].append_xy(x, y)

        params.curves = curves_d

    def write_curves(self, params, inp_file_curve):

        # Rewrite whole file
        with codecs.open(inp_file_curve, 'w', encoding='UTF-8') as c_file:
            out = []
            InpFile._append_curves(params, out)

            for line in out:
                c_file.write(line + '\n')

    def write_inp_file(self, params, inp_file_path, title):

        out = []

        print(0)

        with codecs.open(inp_file_path, 'w', encoding='UTF-8') as inp_f:

            print(1)

            # Network --------------------
            # Title
            if title is not None:
                out.extend(InpFile.build_section_keyword(Title.section_name))
                out.extend(InpFile.split_line(title))

            print(2)

            # Junctions
            self._append_junctions(params, out)

            print(3)

            # Reservoirs
            self._append_reservoirs(params, out)

            print(4)

            # Tanks
            self._append_tanks(params, out)

            print(5)

            # Pipes
            self._append_pipes(params, out)

            print(6)

            # Pumps
            self._append_pumps(params, out)

            print(7)

            # Valves
            self._append_valves(params, out)

            print(8)

            # Tags
            self._append_tags(params, out)

            print(9)

            # Demands
            self._append_demands(params, out)

            print(10)

            # Status
            self._append_status(params, out)

            print(11)

            # SYSTEM OPERATIONS
            # Patterns
            self._append_patterns(params, out)

            print(12)

            # Curves
            self._append_curves(params, out)

            print(13)

            # Controls
            self._append_controls(params, out)

            print(14)

            # Rules
            self._append_rules(params, out)

            print(15)

            # Energy
            self._append_energy(params, out)

            print(16)

            # Emitters
            self._append_emitters(params, out)

            print(17)

            # WATER QUALITY
            # Quality
            # TODO

            # Sources
            # TODO

            # Reactions
            self._append_opt_reactions(params, out)

            print(19)

            # Mixing
            # TODO

            # OPTIONS AND REPORTING
            # Options / reporting
            self._append_options(params, out)

            print(20)

            # Times
            self._append_times(params, out)

            print(21)

            # NETWORK MAP/TAG
            # Coordinates
            self._append_coordinates(params, out)

            print(22)

            # Vertices
            self._append_vertices(params, out)

            # Labels
            # NO

            # Backdrop
            # NO

            # End
            out.append('[END]')

            print(23)

            # Write QEPANET proprietary stuff
            self._append_qepanet(params, out)

            print(24)

            # Write
            for line in out:
                print(line)
                inp_f.write(line + '\n')

    def _append_controls(self, params, out):
        out.extend(InpFile.build_section_keyword(Controls.section_name))
        # TODO

    def _append_coordinates(self, params, out):
        out.extend(InpFile.build_section_keyword(Coordinate.section_name))
        out.append(InpFile.build_section_header(Coordinate.section_header))

        for j_ft in params.junctions_vlay.getFeatures():
            eid = j_ft.attribute(Junction.field_name_eid)
            pt = j_ft.geometry().asPoint()

            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.x()), InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.y()), InpFile.pad_19)

            out.append(line)

        for r_ft in params.reservoirs_vlay.getFeatures():
            eid = r_ft.attribute(Reservoir.field_name_eid)
            pt = r_ft.geometry().asPoint()

            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.x()), InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.y()), InpFile.pad_19)

            out.append(line)

        for t_ft in params.tanks_vlay.getFeatures():
            eid = t_ft.attribute(Tank.field_name_eid)
            pt = t_ft.geometry().asPoint()

            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.x()), InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(pt.y()), InpFile.pad_19)

            out.append(line)

    def _append_curves(self, params, out):
        out.extend(InpFile.build_section_keyword(Curve.section_name))
        out.append(InpFile.build_section_header(Curve.section_header))

        for curve in params.curves.values():

            type_desc = None
            if curve.type is not None:
                type_desc = Curve.type_names[curve.type]

            if curve.desc is not None:
                if type_desc is None:
                    type_desc = curve.desc
                else:
                    type_desc += ': ' + curve.desc

            if type_desc is not None:
                out.extend(InpFile.build_comment(type_desc))

            for v in range(len(curve.xs)):
                out.append(
                    InpFile.pad(str(curve.id), InpFile.pad_19) +
                    InpFile.pad(str(curve.xs[v])) +
                    InpFile.pad(str(curve.ys[v])))

    def _append_demands(self, params, out):
        out.extend(InpFile.build_section_keyword(Demand.section_name))
        out.append(InpFile.build_section_header(Demand.section_header))
        # TODO

    def _append_energy(self, params, out):
        out.extend(InpFile.build_section_keyword(Energy.section_name))

        out.append(InpFile.pad('GLOBAL EFFICIENCY', InpFile.pad_19) + str(params.energy.pump_efficiency))
        out.append(InpFile.pad('GLOBAL PRICE', InpFile.pad_19) + str(params.energy.energy_price))
        out.append(InpFile.pad('DEMAND CHARGE', InpFile.pad_19) + str(params.energy.demand_charge))

    def _append_emitters(self, params, out):
        out.extend(InpFile.build_section_keyword(Emitter.section_name))
        out.append(InpFile.build_section_header(Emitter.section_header))

        j_fts = params.junctions_vlay.getFeatures()
        for j_ft in j_fts:
            eid = j_ft.attribute(Junction.field_name_eid)
            emitter_coeff = j_ft.attribute(Junction.field_name_emitter_coeff)
            if emitter_coeff is not None and emitter_coeff != NULL and emitter_coeff != '':
                line = InpFile.pad(eid, InpFile.pad_19)
                line += InpFile.pad('{0:.2f}'.format(float(emitter_coeff)))
                out.append(line)

    def _append_junctions(self, params, out):

        out.extend(InpFile.build_section_keyword(Junction.section_name))
        out.append(InpFile.build_section_header(Junction.section_header))

        j_fts = params.junctions_vlay.getFeatures()

        for j_ft in j_fts:
            eid = j_ft.attribute(Junction.field_name_eid)
            demand = j_ft.attribute(Junction.field_name_demand)
            elev = j_ft.attribute(Junction.field_name_elev)
            delta_z = j_ft.attribute(Junction.field_name_delta_z)
            pattern = j_ft.attribute(Junction.field_name_pattern)
            description = j_ft.attribute(Junction.field_name_description)
            tag_name = j_ft.attribute(Junction.field_name_tag)

            if pattern == NULL:
                pattern = ''

            if elev is None or elev == NULL:
                elev = 0

            if delta_z is None or delta_z == NULL:
                delta_z = 0

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_node, eid, tag_name))

            elev += delta_z

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(elev)))
            if demand is not None:
                line += InpFile.pad('{0:.5f}'.format(float(demand)))
            else:
                line += InpFile.pad('')

            if pattern is not None:
                line += InpFile.pad(str(pattern))
            else:
                line += InpFile.pad('')

            if description is not None and description != '':
                line += ';' + description

            out.append(line)

    def _append_options(self, params, out):

        # Options
        out.extend(InpFile.build_section_keyword(Options.section_name))

        out.append(InpFile.pad('UNITS', InpFile.pad_22) + params.options.flow_units)
        out.append(InpFile.pad('HEADLOSS', InpFile.pad_22) + params.options.headloss)
        if params.options.hydraulics.use_hydraulics:
            out.append(InpFile.pad('HYDRAULICS', InpFile.pad_22) +
                       params.options.hydraulics.action_names[params.options.hydraulics.action])

        # Quality
        quality_line = InpFile.pad('QUALITY', InpFile.pad_22) + InpFile.pad(params.options.quality.quality_text[params.options.quality.parameter])
        if params.options.quality.parameter == Quality.quality_chemical:
            quality_line += InpFile.pad(params.options.quality.mass_units)
        elif params.options.quality.parameter == Quality.quality_trace:
            quality_line += InpFile.pad(params.options.quality.trace_junction_id)

        out.append(InpFile.pad('VISCOSITY', InpFile.pad_22) + str(params.options.viscosity))
        out.append(InpFile.pad('DIFFUSIVITY', InpFile.pad_22) + str(params.options.diffusivity))
        out.append(InpFile.pad('SPECIFIC GRAVITY', InpFile.pad_22) + str(params.options.spec_gravity))
        out.append(InpFile.pad('TRIALS', InpFile.pad_22) + str(int(params.options.trials)))
        out.append(InpFile.pad('ACCURACY', InpFile.pad_22) + str(params.options.accuracy))
        out.append(InpFile.pad('UNBALANCED', InpFile.pad_22) +
                   params.options.unbalanced.unb_text[params.options.unbalanced.unbalanced] +
                   ' ' +
                   str(params.options.unbalanced.trials))
        if params.options.pattern is not None:
            pattern_val = params.options.pattern.id
        else:
            pattern_val = 1
        out.append(InpFile.pad('PATTERN', InpFile.pad_22) + str(pattern_val))
        out.append(InpFile.pad('DEMAND MULTIPLIER', InpFile.pad_22) + str(params.options.demand_mult))
        out.append(InpFile.pad('EMITTER EXPONENT', InpFile.pad_22) + str(params.options.emitter_exp))
        out.append(InpFile.pad('TOLERANCE', InpFile.pad_22) + str(params.options.tolerance))

        # Report
        out.extend(InpFile.build_section_keyword(Report.section_name))

        out.append(InpFile.pad('PAGESIZE', InpFile.pad_22) + str(params.report.page_size))
        if params.report.file is not None:
            out.append(InpFile.pad('FILE', InpFile.pad_22) + str(params.report.file))
        out.append(InpFile.pad('STATUS', InpFile.pad_22) + params.report.status_names[params.report.status])
        out.append(InpFile.pad('SUMMARY', InpFile.pad_22) + params.report.summary_names[params.report.summary])
        out.append(InpFile.pad('ENERGY', InpFile.pad_22) + params.report.energy_names[params.report.energy])

        # TODO: nodes and links need support for multi-line
        nodes_line = InpFile.pad('NODES', InpFile.pad_22)
        if params.report.nodes == params.report.nodes_none or params.report.nodes == params.report.nodes_all:
            nodes_line += params.report.nodes_names[params.report.nodes]
        else:
            nodes_ids = ''
            for node_id in params.report.nodes_ids:
                nodes_ids += node_id + ' '
            nodes_line += nodes_ids

        out.append(nodes_line)

        links_line = InpFile.pad('LINKS', InpFile.pad_22)
        if params.report.links == params.report.links_none or params.report.links == params.report.links_all:
            links_line += params.report.links_names[params.report.links]
        else:
            links_ids = ''
            for link_id in params.report.links_ids:
                links_ids += link_id + ' '
                links_line += links_ids

        out.append(links_line)

    def _append_patterns(self, params, out):
        out.extend(InpFile.build_section_keyword(Pattern.section_name))
        out.append(InpFile.build_section_header(Pattern.section_header))

        for pattern in params.patterns.values():
            if pattern.desc is not None:
                out.extend(InpFile.build_comment(pattern.desc))

            lines = InpFile.from_values_to_lines(pattern.values, line_header=pattern.id, vals_per_line=6)
            for line in lines:
                out.append(line)

    def _append_pipes(self, params, out):

        out.extend(InpFile.build_section_keyword(Pipe.section_name))
        out.append(InpFile.build_section_header(Pipe.section_header))
        # out.append(InpFile.build_dashline(Pipe.section_header))

        pipe_fts = params.pipes_vlay.getFeatures()

        # Build nodes spatial index
        sindex = QgsSpatialIndex()
        for feat in params.junctions_vlay.getFeatures():
            sindex.addFeature(feat)
        for feat in params.reservoirs_vlay.getFeatures():
            sindex.addFeature(feat)
        for feat in params.tanks_vlay.getFeatures():
            sindex.addFeature(feat)

        for pipe_ft in pipe_fts:

            eid = pipe_ft.attribute(Pipe.field_name_eid)

            # Find start/end nodes
            # adj_nodes = NetworkUtils.find_start_end_nodes(params, pipe_ft.geometry())
            adj_nodes = NetworkUtils.find_start_end_nodes_sindex(params, sindex, pipe_ft.geometry())

            start_node_id = adj_nodes[0].attribute(Junction.field_name_eid)
            end_node_id = adj_nodes[1].attribute(Junction.field_name_eid)

            length = pipe_ft.attribute(Pipe.field_name_length)
            diameter = pipe_ft.attribute(Pipe.field_name_diameter)
            roughness = pipe_ft.attribute(Pipe.field_name_roughness)
            minor_loss = pipe_ft.attribute(Pipe.field_name_minor_loss)
            status = pipe_ft.attribute(Pipe.field_name_status)
            description = pipe_ft.attribute(Pipe.field_name_description)
            tag_name = pipe_ft.attribute(Pipe.field_name_tag)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad(start_node_id, InpFile.pad_19)
            line += InpFile.pad(end_node_id, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(length)), InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(diameter)), InpFile.pad_19)
            line += InpFile.pad('{0:.4f}'.format(float(roughness)), InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(minor_loss)), InpFile.pad_19)
            line += InpFile.pad(status)

            if description is not None and description != '':
                line += ';' + description

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_link, eid, tag_name))

            out.append(line)

    def _append_pumps(self, params, out):

        out.extend(InpFile.build_section_keyword(Pump.section_name))
        out.append(InpFile.build_section_header(Pump.section_header))
        # out.append(InpFile.build_dashline(Pump.section_header))

        p_fts = params.pumps_vlay.getFeatures()
        for p_ft in p_fts:
            eid = p_ft.attribute(Pump.field_name_eid)

            # Find start/end nodes
            adj_nodes = NetworkUtils.find_start_end_nodes(params, p_ft.geometry())
            start_node_id = adj_nodes[0].attribute(Junction.field_name_eid)
            end_node_id = adj_nodes[1].attribute(Junction.field_name_eid)

            # Parameters
            pump_param = p_ft.attribute(Pump.field_name_param)
            speed = p_ft.attribute(Pump.field_name_speed)
            speed_pattern = p_ft.attribute(Pump.field_name_speed_pattern)
            description = p_ft.attribute(Pump.field_name_description)
            tag_name = p_ft.attribute(Pump.field_name_tag)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad(start_node_id, InpFile.pad_19)
            line += InpFile.pad(end_node_id, InpFile.pad_19)

            if pump_param == Pump.parameters_power:
                power = p_ft.attribute(Pump.field_name_power)
                line += InpFile.pad(pump_param + ' ' + '{0:2f}'.format(float(power)), InpFile.pad_19)
            elif pump_param == Pump.parameters_head:
                head = p_ft.attribute(Pump.field_name_head)
                if head is not None and head != NULL:
                    line += InpFile.pad(pump_param + ' ' + head, InpFile.pad_19)

            if speed is not None and speed != NULL:
                line += ' SPEED ' + str(speed)

            if speed_pattern is not None and speed_pattern != NULL and speed_pattern != '':
                line += ' PATTERN ' + speed_pattern

            if description is not None and description != '':
                line += ';' + description

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_link, eid, tag_name))

            out.append(line)

    def _append_opt_reactions(self, params, out):

        out.extend(InpFile.build_section_keyword(Reactions.section_name))

        out.append(InpFile.pad('ORDER BULK', InpFile.pad_22) + str(params.reactions.order_bulk))
        out.append(InpFile.pad('ORDER TANK', InpFile.pad_22) + str(params.reactions.order_tank))
        out.append(InpFile.pad('ORDER WALL', InpFile.pad_22) + str(params.reactions.order_wall))

        out.append(InpFile.pad('GLOBAL BULK', InpFile.pad_22) + str(params.reactions.global_bulk))
        out.append(InpFile.pad('GLOBAL WALL', InpFile.pad_22) + str(params.reactions.global_wall))

        out.append(InpFile.pad('LIMITING POTENTIAL', InpFile.pad_22) + str(params.reactions.limiting_potential))
        out.append(InpFile.pad('ROUGHNESS CORRELATION', InpFile.pad_22) + str(params.reactions.roughness_corr))

    def _append_rules(self, params, out):
        out.extend(InpFile.build_section_keyword(Rule.section_name))
        rules = params.rules
        for rule in rules:
            out.append(rule.name)
            out.append(rule.condition)
            out.append(rule.action)

    def _append_status(self, params, out):
        out.extend(InpFile.build_section_keyword(Status.section_name))
        out.append(InpFile.build_section_header(Status.section_header))

        # Pumps
        p_fts = params.pumps_vlay.getFeatures()
        for p_ft in p_fts:
            eid = p_ft.attribute(Pump.field_name_eid)

            # Speed
            pump_speed = p_ft.attribute(Pump.field_name_speed)
            if pump_speed != NULL and pump_speed != '':
                line = InpFile.pad(eid, InpFile.pad_19)
                line += InpFile.pad('{0:.2f}'.format(float(pump_speed)), InpFile.pad_19)
                out.append(line)

            # Status
            pump_status = p_ft.attribute(Pump.field_name_status)
            if pump_status == Pump.status_closed:
                line = InpFile.pad(eid, InpFile.pad_19)
                line += InpFile.pad(pump_status.upper(), InpFile.pad_19)
                out.append(line)

        # Valves
        v_fts = params.valves_vlay.getFeatures()
        for v_ft in v_fts:
            eid = v_ft.attribute(Valve.field_name_eid)
            valve_status = v_ft.attribute(Valve.field_name_status)
            if valve_status != Valve.status_none:
                line = InpFile.pad(eid, InpFile.pad_19)
                line += InpFile.pad(valve_status.upper(), InpFile.pad_19)
                out.append(line)

            # valve_setting = v_ft.attribute(Valve.field_name_setting)
            # if valve_setting != NULL and valve_setting != '':
            #     line = InpFile.pad(eid, InpFile.pad_19)
            #     line += InpFile.pad(valve_setting, InpFile.pad_19)
            #     out.append(line)

        # # Pipes
        # p_fts = params.pipes_vlay.getFeatures()
        # for p_ft in p_fts:
        #     eid = p_ft.attribute(Pipe.field_name_eid)
        #     pipe_status = p_ft.attribute(Pipe.field_name_status)
        #     line = InpFile.pad(eid, InpFile.pad_19)
        #     line += InpFile.pad(pipe_status.upper(), InpFile.pad_19)
        #     out.append(line)

    def _append_reservoirs(self, params, out):

        out.extend(InpFile.build_section_keyword(Reservoir.section_name))
        out.append(InpFile.build_section_header(Reservoir.section_header))
        # out.append(InpFile.build_dashline(Reservoir.section_header))

        r_fts = params.reservoirs_vlay.getFeatures()
        for r_ft in r_fts:
            eid = r_ft.attribute(Reservoir.field_name_eid)
            elev = r_ft.attribute(Reservoir.field_name_elev)
            deltaz = r_ft.attribute(Reservoir.field_name_delta_z)
            pressure_head = r_ft.attribute(Reservoir.field_name_pressure_head)
            pattern = r_ft.attribute(Reservoir.field_name_pattern)
            description = r_ft.attribute(Reservoir.field_name_description)
            tag_name = r_ft.attribute(Reservoir.field_name_tag)

            if elev is None or elev == NULL:
                elev = 0
            if deltaz is None or deltaz == NULL:
                deltaz = 0
            if pressure_head is None or pressure_head == NULL:
                pressure_head = 0

            head = elev + deltaz + pressure_head

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(head)))

            if pattern != NULL:
                line += InpFile.pad(pattern)

            if description is not None and description != '':
                line += ';' + description

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_node, eid, tag_name))

            out.append(line)

    def _append_tanks(self, params, out):

        out.extend(InpFile.build_section_keyword(Tank.section_name))
        out.append(InpFile.build_section_header(Tank.section_header))
        # out.append(InpFile.build_dashline(Tank.section_header))

        t_fts = params.tanks_vlay.getFeatures()
        for t_ft in t_fts:
            eid = t_ft.attribute(Tank.field_name_eid)
            curve = t_ft.attribute(Tank.field_name_curve)
            diameter = t_ft.attribute(Tank.field_name_diameter)
            elev = t_ft.attribute(Tank.field_name_elev)
            deltaz = t_ft.attribute(Tank.field_name_delta_z)
            level_init = t_ft.attribute(Tank.field_name_level_init)
            level_max = t_ft.attribute(Tank.field_name_level_max)
            level_min = t_ft.attribute(Tank.field_name_level_min)
            vol_min = t_ft.attribute(Tank.field_name_vol_min)
            description = t_ft.attribute(Tank.field_name_description)
            tag_name = t_ft.attribute(Tank.field_name_tag)

            if elev is None or elev == NULL:
                elev = 0

            if deltaz is None or deltaz == NULL:
                deltaz = 0

            elev += deltaz

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(elev)))
            line += InpFile.pad('{0:.4f}'.format(float(level_init)))
            line += InpFile.pad('{0:.4f}'.format(float(level_min)))
            line += InpFile.pad('{0:.4f}'.format(float(level_max)))
            line += InpFile.pad('{0:.1f}'.format(float(diameter)))
            line += InpFile.pad('{0:.4f}'.format(float(vol_min)))

            if curve is not None and curve != NULL:
                line += InpFile.pad(curve)

            if description is not None and description != '':
                line += ';' + description

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_node, eid, tag_name))

            out.append(line)

    def _append_times(self, params, out):

        out.extend(InpFile.build_section_keyword(Times.section_name))
        out.append(InpFile.pad('DURATION', InpFile.pad_22) + params.times.duration.get_as_text(4))

        out.append(InpFile.pad('HYDRAULIC TIMESTEP', InpFile.pad_22) + params.times.hydraulic_timestep.get_as_text())
        out.append(InpFile.pad('QUALITY TIMESTEP', InpFile.pad_22) + params.times.quality_timestep.get_as_text())
        out.append(InpFile.pad('RULE TIMESTEP', InpFile.pad_22) + params.times.rule_timestep.get_as_text())
        out.append(InpFile.pad('PATTERN TIMESTEP', InpFile.pad_22) + params.times.pattern_timestep.get_as_text())
        out.append(InpFile.pad('PATTERN START', InpFile.pad_22) + params.times.pattern_start.get_as_text())
        out.append(InpFile.pad('REPORT TIMESTEP', InpFile.pad_22) + params.times.report_timestep.get_as_text())
        out.append(InpFile.pad('REPORT START', InpFile.pad_22) + params.times.report_start.get_as_text())
        out.append(InpFile.pad('START CLOCKTIME', InpFile.pad_22) + params.times.clocktime_start.get_as_text())
        out.append(InpFile.pad('STATISTIC', InpFile.pad_22) + Times.stats_text[params.times.statistic])

    def _append_valves(self, params, out):

        out.extend(InpFile.build_section_keyword(Valve.section_name))
        out.append(InpFile.build_section_header(Valve.section_header))
        # out.append(InpFile.build_dashline(Valve.section_header))

        v_fts = params.valves_vlay.getFeatures()
        for v_ft in v_fts:
            eid = v_ft.attribute(Valve.field_name_eid)

            # Find start/end nodes
            adj_nodes = NetworkUtils.find_start_end_nodes(params, v_ft.geometry())
            start_node_id = adj_nodes[0].attribute(Junction.field_name_eid)
            end_node_id = adj_nodes[1].attribute(Junction.field_name_eid)

            diameter = str(v_ft.attribute(Valve.field_name_diameter))
            valve_type = v_ft.attribute(Valve.field_name_type)
            setting = str(v_ft.attribute(Valve.field_name_setting))
            minor_loss = str(v_ft.attribute(Valve.field_name_minor_loss))
            description = v_ft.attribute(Valve.field_name_description)
            tag_name = v_ft.attribute(Valve.field_name_tag)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad(start_node_id, InpFile.pad_19)
            line += InpFile.pad(end_node_id, InpFile.pad_19)
            line += InpFile.pad(str(diameter))
            line += InpFile.pad(valve_type)
            line += InpFile.pad(setting)
            line += InpFile.pad(minor_loss)

            if description is not None and description != '':
                line += ';' + description

            if tag_name is not None and tag_name != NULL and tag_name != '':
                self.tags.append(Tag(Tag.element_type_link, eid, tag_name))

            out.append(line)

    def _append_tags(self, params, out):
        out.extend(InpFile.build_section_keyword(Tag.section_name))
        for tag in self.tags:
            line = InpFile.pad(tag.element_type, InpFile.pad_19)
            line += InpFile.pad(tag.element_id, InpFile.pad_19)
            line += InpFile.pad(tag.tag, InpFile.pad_19)

            out.append(line)

    @staticmethod
    def _append_vertices(params, out):
        out.extend(InpFile.build_section_keyword(Vertex.section_name))
        out.append(InpFile.build_section_header(Vertex.section_header))
        # out.append(InpFile.build_dashline(Vertex.section_header))

        for p_ft in params.pipes_vlay.getFeatures():
            eid = p_ft.attribute(Pipe.field_name_eid)
            pts = p_ft.geometry().asPolyline()
            if len(pts) > 2:
                for pt in pts[1:-1]:
                    line = InpFile.pad(eid, InpFile.pad_19)
                    line += InpFile.pad('{0:.2f}'.format(pt.x()), InpFile.pad_19)
                    line += InpFile.pad('{0:.2f}'.format(pt.y()), InpFile.pad_19)

                    out.append(line)

    @staticmethod
    def _append_qepanet(params, out):

        # QJUNCTIONS
        out.extend(InpFile.build_section_keyword(QJunction.section_name))
        out.append(InpFile.build_section_header(QJunction.section_header))

        j_fts = params.junctions_vlay.getFeatures()
        for j_ft in j_fts:
            eid = j_ft.attribute(Junction.field_name_eid)
            delta_z = j_ft.attribute(Junction.field_name_delta_z)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(delta_z)))

            out.append(line)

        # QRESERVOIRS
        out.extend(InpFile.build_section_keyword(QReservoir.section_name))
        out.append(InpFile.build_section_header(QReservoir.section_header))

        j_fts = params.reservoirs_vlay.getFeatures()
        for j_ft in j_fts:
            eid = j_ft.attribute(Reservoir.field_name_eid)
            delta_z = j_ft.attribute(Reservoir.field_name_delta_z)
            pressure_head = j_ft.attribute(Reservoir.field_name_pressure_head)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(delta_z)))
            line += InpFile.pad('{0:.2f}'.format(float(pressure_head)))

            out.append(line)

        # QTANKS
        out.extend(InpFile.build_section_keyword(QTank.section_name))
        out.append(InpFile.build_section_header(QTank.section_header))

        j_fts = params.tanks_vlay.getFeatures()
        for j_ft in j_fts:
            eid = j_ft.attribute(Tank.field_name_eid)
            delta_z = j_ft.attribute(Tank.field_name_delta_z)

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad('{0:.2f}'.format(float(delta_z)))

            out.append(line)

        # QPIPES
        out.extend(InpFile.build_section_keyword(QPipe.section_name))
        out.append(InpFile.build_section_header(QPipe.section_header))

        p_fts = params.pipes_vlay.getFeatures()
        for p_ft in p_fts:
            eid = p_ft.attribute(Pipe.field_name_eid)
            material = p_ft.attribute(Pipe.field_name_material)
            # print 'material', material, type(material)
            if material == NULL:
                material = ''

            # Line
            line = InpFile.pad(eid, InpFile.pad_19)
            line += InpFile.pad(material)

            out.append(line)

        # QVERTICES
        out.extend(InpFile.build_section_keyword(QVertices.section_name))

        for p_ft in params.pipes_vlay.getFeatures():
            eid = p_ft.attribute(Pipe.field_name_eid)
            geom_v2 = p_ft.geometry().get()

            if geom_v2.vertexCount() > 2:

                for v in range(1, geom_v2.vertexCount() - 1):
                    p2_v2 = geom_v2.vertexAt(QgsVertexId(0, 0, v, QgsVertexId.SegmentVertex))

                    line = InpFile.pad(eid, InpFile.pad_19)
                    line += InpFile.pad('{0:.2f}'.format(p2_v2.z()), InpFile.pad_19)

                    out.append(line)
            #
            # # pts = p_ft.geometry().asPolyline()
            # if len(pts) > 2:
            #     for pt in pts[1:-1]:
            #         line = InpFile.pad(eid, InpFile.pad_19)
            #         line += InpFile.pad('{0:.2f}'.format(pt.z()), InpFile.pad_19)
            #
            #         out.append(line)

        # QOPTIONS
        out.extend(InpFile.build_section_keyword(QOptions.section_name))

    @staticmethod
    def split_line(line, n=255):
        lines = [line[i:i + n] for i in range(0, len(line), n)]
        return lines

    @staticmethod
    def from_values_to_lines(values, decimal_places=2, n=255, element_size=10, line_header=None, vals_per_line=None):

        if line_header is not None:
            header = str(InpFile.pad(line_header, InpFile.pad_19))
        else:
            header = ''

        svalues = []
        for value in values:
            formatter = '{0:.' + str(decimal_places) + 'f}'
            svalue = formatter.format(value)
            svalue = InpFile.pad(svalue, element_size)
            svalues.append(svalue)

        # Calc elements per line
        if vals_per_line is None:
            vals_per_line = int(math.floor((n - len(header)) / (element_size + 1)))

        if len(values) < vals_per_line:
            vals_per_line = len(values)

        if not svalues:
            return []

        lines_nr = int(math.ceil(len(svalues) / float(vals_per_line)))

        lines = []
        v = 0
        for l in range(lines_nr):
            line = header
            for vpl in range(vals_per_line):
                line += svalues[v]
                v += 1
                if v >= len(svalues):
                    break
            lines.append(line)

        return lines

    @staticmethod
    def pad(text, blanks_nr=10):
        for t in range(blanks_nr - len(text)):
            text += ' '
        text += '\t'
        return text

    @staticmethod
    def build_section_keyword(section_name):
        return ['',
                '[' + section_name + ']']

    @staticmethod
    def build_section_header(section_header):
        return ';' + section_header

    @staticmethod
    def build_comment(comment):
        comments = InpFile.split_line(comment)
        for c in range(len(comments)):
            comments[c] = ';' + comments[c]
        return comments

    @staticmethod
    def build_dashline(text):
        dashline = ';'
        for d in range(len(text)):
            dashline += '-'
        return dashline


class PatFile:

    def __init__(self):
        pass

    @staticmethod
    def read_pattern(params,pattern_file):

        if not os.path.isfile(pattern_file):
            return []

        pattern_started = False
        with codecs.open(pattern_file, 'r', encoding='UTF-8') as inp_f:
            lines = inp_f.read().splitlines()

        pattern_desc = None
        values = []
        for l in range(len(lines)):
            if lines[l].upper().startswith('EPANET PATTERN DATA'):
                pattern_started = True
                continue

            if pattern_started:
                if l == 1:
                    pattern_desc = lines[l].strip()
                else:
                    value = float(lines[l].strip())
                    values.append(value)

        patterns = params.patterns
        pattern_ids = []
        for p, pattern in enumerate(patterns):
            pattern_ids.append(pattern.id)

        new_id = None
        new_id_temp = 0
        while new_id is None:
            new_id_temp += 1
            if new_id_temp not in pattern_ids:
                new_id = new_id_temp

        print('new', new_id, pattern_desc, values)
        params.patterns[new_id] = Pattern(str(new_id), pattern_desc, values)
