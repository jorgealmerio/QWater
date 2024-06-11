from builtins import str
from builtins import range
from qgis.PyQt.QtWidgets import QDialog, QFormLayout, QLabel, QComboBox, QLineEdit, QCheckBox, QPushButton, QFrame, QHBoxLayout, QMessageBox, QFileDialog, QVBoxLayout
from qgis.PyQt import QtCore
from ..tools.parameters import Parameters, RegExValidators
from ..model.network import Valve
from ..model.options_report import Hour, Report, Times, Options
from .utils import prepare_label as pre_l
import os

min_width = 200
min_height = 400


class HydraulicsDialog(QDialog):

    def __init__(self, parent, params, new_proj=False):
        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params
        self.new_proj = new_proj

        self.setMinimumWidth(min_width)
        # self.setMinimumHeight(min_height)

        # Build dialog
        self.setWindowTitle('Options - Hydraulics')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_units = QLabel('Units system:') # TODO: softocode
        self.cbo_units = QComboBox()
        fra_form_lay.addRow(self.lbl_units, self.cbo_units)

        self.lbl_flow_units = QLabel('Flow units:')  # TODO: softocode
        self.cbo_flow_units = QComboBox()
        fra_form_lay.addRow(self.lbl_flow_units, self.cbo_flow_units)

        self.lbl_headloss = QLabel('Head loss:')  # TODO: softocode
        self.cbo_headloss = QComboBox()
        fra_form_lay.addRow(self.lbl_headloss, self.cbo_headloss)

        self.chk_hydraulics = QCheckBox('Hydraulics:') # TODO: softcode
        self.cbo_hydraulics = QComboBox()
        fra_form_lay.addRow(self.chk_hydraulics, self.cbo_hydraulics)

        self.txt_hydraulics_file = QLineEdit()
        fra_form_lay.addRow(None, self.txt_hydraulics_file)

        self.btn_hydraulics_file = QPushButton('File...')  # TODO: softcode
        fra_form_lay.addRow(None, self.btn_hydraulics_file)

        self.lbl_viscosity = QLabel('Viscosity:')  # TODO: softocode
        self.txt_viscosity = QLineEdit()
        fra_form_lay.addRow(self.lbl_viscosity, self.txt_viscosity)

        # self.lbl_diffusivity = QLabel('Diffusivity:')  # TODO: softocode
        # self.txt_diffusivity = QLineEdit()
        # fra_form_lay.addRow(self.lbl_diffusivity, self.txt_diffusivity)

        self.lbl_spec_gravity = QLabel('Specific gravity:')  # TODO: softocode
        self.txt_spec_gravity = QLineEdit()
        fra_form_lay.addRow(self.lbl_spec_gravity, self.txt_spec_gravity)

        self.lbl_max_trials = QLabel('Max trials:')  # TODO: softocode
        self.txt_max_trials = QLineEdit()
        fra_form_lay.addRow(self.lbl_max_trials, self.txt_max_trials)

        self.lbl_accuracy = QLabel('Accuracy:')  # TODO: softocode
        self.txt_accuracy = QLineEdit()
        fra_form_lay.addRow(self.lbl_accuracy, self.txt_accuracy)

        self.lbl_unbalanced = QLabel('Unbalanced:') # TODO: softcode
        self.fra_unbalanced = QFrame(self)
        fra_unbalanced_lay = QHBoxLayout(self.fra_unbalanced)
        fra_unbalanced_lay.setContentsMargins(0, 0, 0, 0)
        self.cbo_unbalanced = QComboBox()
        self.txt_unbalanced = QLineEdit()
        fra_unbalanced_lay.addWidget(self.cbo_unbalanced)
        fra_unbalanced_lay.addWidget(self.txt_unbalanced)
        fra_form_lay.addRow(self.lbl_unbalanced, self.fra_unbalanced)

        self.lbl_pattern = QLabel('Pattern:')  # TODO: softocode
        self.cbo_pattern = QComboBox()
        fra_form_lay.addRow(self.lbl_pattern, self.cbo_pattern)

        self.lbl_demand_mult = QLabel('Demand multiplier:')  # TODO: softocode
        self.txt_demand_mult = QLineEdit()
        fra_form_lay.addRow(self.lbl_demand_mult, self.txt_demand_mult)

        self.lbl_emitter_exp = QLabel('Emitter exponent:')  # TODO: softocode
        self.txt_emitter_exp = QLineEdit()
        fra_form_lay.addRow(self.lbl_emitter_exp, self.txt_emitter_exp)

        self.lbl_tolerance = QLabel('Tolerance:')  # TODO: softocode
        self.txt_tolerance = QLineEdit()
        fra_form_lay.addRow(self.lbl_tolerance, self.txt_tolerance)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Cancel = QPushButton('Cancel')
        self.btn_Ok = QPushButton('OK')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):

        # Fill units system combo box
        for unit in self.params.options.units_sys:
            self.cbo_units.addItem(self.params.options.units_sys_text[unit], unit)

        # Fill flow units combo box
        for fu in Options.units_flow[self.params.options.units]:
            self.cbo_flow_units.addItem(Options.units_flow_text[fu], fu)

        self.cbo_units.activated.connect(self.cbo_units_activated)
        # self.cbo_flow_units.activated.connect(self.cbo_flow_units_activated)

        for key, value in self.params.options.headlosses_text.items():
            self.cbo_headloss.addItem(value, key)

        self.cbo_headloss.activated.connect(self.cbo_headloss_activated)

        self.chk_hydraulics.stateChanged.connect(self.chk_hydraulics_changed)
        self.btn_hydraulics_file.clicked.connect(self.btn_hydraulics_clicked)
        self.cbo_hydraulics.addItem(
            self.params.options.hydraulics.action_names[self.params.options.hydraulics.action_use],
            self.params.options.hydraulics.action_use)
        self.cbo_hydraulics.addItem(
            self.params.options.hydraulics.action_names[self.params.options.hydraulics.action_save],
            self.params.options.hydraulics.action_save)
        self.txt_hydraulics_file.setReadOnly(True)

        # - Unbalanced
        for id, text in self.params.options.unbalanced.unb_text.items():
            self.cbo_unbalanced.addItem(text, id)

        self.cbo_unbalanced.activated.connect(self.cbo_unbalanced_changed)
        self.txt_unbalanced.setValidator(RegExValidators.get_pos_int_no_zero())
        self.txt_unbalanced.setText('1')

        # - Pattern
        self.cbo_pattern.addItem('None (=1.0)', None)
        for pattern_id, pattern in self.params.patterns.items():
            self.cbo_pattern.addItem(pattern_id, pattern)

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

        # Validators
        self.txt_viscosity.setValidator(RegExValidators.get_pos_decimals())
        self.txt_spec_gravity.setValidator(RegExValidators.get_pos_decimals())
        self.txt_max_trials.setValidator(RegExValidators.get_pos_int_no_zero())
        self.txt_accuracy.setValidator(RegExValidators.get_pos_decimals())
        self.txt_demand_mult.setValidator(RegExValidators.get_pos_decimals())
        self.txt_emitter_exp.setValidator(RegExValidators.get_pos_decimals())
        self.txt_tolerance.setValidator(RegExValidators.get_pos_decimals())

    def show(self):
        super(HydraulicsDialog, self).show()

        self.cbo_units.setCurrentIndex(self.cbo_units.findData(self.params.options.units))
        self.cbo_flow_units.setCurrentIndex(self.cbo_flow_units.findData(self.params.options.flow_units))
        self.cbo_headloss.setCurrentIndex(self.cbo_headloss.findData(self.params.options.headloss))

        self.chk_hydraulics.setChecked(self.params.options.hydraulics.use_hydraulics)
        self.btn_hydraulics_file.setEnabled(self.chk_hydraulics.isChecked())
        self.cbo_hydraulics.setEnabled(self.chk_hydraulics.isChecked())
        self.txt_hydraulics_file.setEnabled(self.chk_hydraulics.isChecked())

        if self.params.options.hydraulics.action is not None:
            self.cbo_hydraulics.setCurrentIndex(self.cbo_hydraulics.findData(self.params.options.hydraulics.action))
        if self.params.options.hydraulics.file is not None:
            self.txt_hydraulics_file.setText(self.params.options.hydraulics.file)

        self.txt_viscosity.setText(str(self.params.options.viscosity))
        self.txt_spec_gravity.setText(str(self.params.options.spec_gravity))
        self.txt_max_trials.setText(str(self.params.options.trials))
        self.txt_accuracy.setText(str(self.params.options.accuracy))

        self.cbo_unbalanced.setCurrentIndex(self.cbo_unbalanced.findData(self.params.options.unbalanced.unbalanced))
        self.txt_unbalanced.setEnabled(self.cbo_unbalanced.currentIndex() != 0)
        self.txt_unbalanced.setText(str(self.params.options.unbalanced.trials))

        # Patterns
        if self.params.options.pattern is not None:
            if self.params.options.pattern is None:
                self.cbo_pattern.setCurrentIndex(0)
            else:
                for i in range(self.cbo_pattern.count()):
                    if self.params.options.pattern.id == self.cbo_pattern.itemText(i):
                        self.cbo_pattern.setCurrentIndex(i)
                        break

        self.txt_demand_mult.setText(str(self.params.options.demand_mult))
        self.txt_emitter_exp.setText(str(self.params.options.emitter_exp))
        self.txt_tolerance.setText(str(self.params.options.tolerance))

    def cbo_units_activated(self):

        self.params.options.units = self.cbo_units.itemData(self.cbo_units.currentIndex())

        # Parameters combo box
        self.cbo_flow_units.clear()
        for fu in Options.units_flow[self.params.options.units]:
            self.cbo_flow_units.addItem(Options.units_flow_text[fu], fu)

    def cbo_headloss_activated(self):

        # Warning
        if not self.new_proj:
            QMessageBox.warning(
                self,
                Parameters.plug_in_name,
                u'Head loss units changed: the head loss values already present might need to be reviewed.',
                QMessageBox.Ok)

    def chk_hydraulics_changed(self):

        self.btn_hydraulics_file.setEnabled(self.chk_hydraulics.isChecked())
        self.cbo_hydraulics.setEnabled(self.chk_hydraulics.isChecked())
        self.txt_hydraulics_file.setEnabled(self.chk_hydraulics.isChecked())

    def btn_hydraulics_clicked(self):
        file_dialog = QFileDialog(self, 'Select hydraulics file')
        file_dialog.setLabelText(QFileDialog.Accept, 'Select')
        file_dialog.setLabelText(QFileDialog.Reject, 'Cancel')
        file_dialog.setFileMode(QFileDialog.AnyFile)

        file_dialog.exec_()

        hydraulics_file_path = file_dialog.selectedFiles()

        if not hydraulics_file_path or hydraulics_file_path[0] is None or hydraulics_file_path[0] == '':
            return

        self.txt_hydraulics_file.setText(hydraulics_file_path[0])

    def cbo_unbalanced_changed(self):
        self.txt_unbalanced.setEnabled(
            self.cbo_unbalanced.itemData(
                self.cbo_unbalanced.currentIndex()) == self.params.options.unbalanced.unb_continue)

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        if not self.check_params():
            return

        # Update parameters and options
        self.params.options.units = self.cbo_units.itemData(self.cbo_units.currentIndex())
        self.params.options.flow_units = self.cbo_flow_units.itemData(self.cbo_flow_units.currentIndex())
        self.params.options.headloss = self.cbo_headloss.itemData(self.cbo_headloss.currentIndex())
        self.params.options.hydraulics.use_hydraulics = self.chk_hydraulics.isChecked()

        if self.params.options.hydraulics.action is not None:
            self.params.options.hydraulics.action = self.cbo_hydraulics.itemData(self.cbo_hydraulics.currentIndex())
            self.params.options.hydraulics.file = self.txt_hydraulics_file.text()

        self.params.options.viscosity = float(self.txt_viscosity.text())
        # self.params.options.diffusivity = float(self.txt_diffusivity.text())
        self.params.options.spec_gravity = float(self.txt_spec_gravity.text())
        self.params.options.trials = float(self.txt_max_trials.text())
        self.params.options.accuracy = float(self.txt_accuracy.text())

        self.params.options.unbalanced.unbalanced = self.cbo_unbalanced.itemData(self.cbo_unbalanced.currentIndex())
        self.params.options.unbalanced.trials = int(self.txt_unbalanced.text())

        self.params.options.pattern = self.cbo_pattern.itemData(self.cbo_pattern.currentIndex())
        self.params.options.demand_mult = float(self.txt_demand_mult.text())
        self.params.options.emitter_exp = float(self.txt_emitter_exp.text())
        self.params.options.tolerance = float(self.txt_tolerance.text())

        # Junctions
        self.parent.lbl_junction_demand.setText(pre_l('Demand', Options.units_flow[self.params.options.units][0]))  # TODO: softcode
        self.parent.lbl_junction_deltaz.setText(pre_l('Delta Z', Options.units_deltaz[self.params.options.units]))  # TODO: softcode

        # Reservoirs
        self.parent.lbl_reservoir_deltaz.setText(
            pre_l('Delta Z', Options.units_deltaz[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_reservoir_pressure_head.setText(
            pre_l('Pressure head', Options.units_deltaz[self.params.options.units]))  # TODO: softcode

        # Tanks
        self.parent.lbl_tank_deltaz.setText(pre_l('Delta Z', Options.units_deltaz[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_tank_level_init.setText(pre_l('Level init.', Options.units_deltaz[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_tank_level_min.setText(pre_l('Level min', Options.units_deltaz[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_tank_level_max.setText(pre_l('Level max', Options.units_deltaz[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_tank_diameter.setText(pre_l('Diameter', Options.units_diameter_tanks[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_tank_vol_min.setText(pre_l('Volume min', Options.units_volume[self.params.options.units]))  # TODO: softcode

        # Pipes
        self.parent.lbl_pipe_demand.setText(pre_l('Demand', Options.units_flow[self.params.options.units][0]))  # TODO: softcode
        self.parent.lbl_pipe_diameter.setText(pre_l('Diameter', Options.units_diameter_pipes[self.params.options.units]))  # TODO: softcode
        self.parent.lbl_pipe_roughness_val.setText(pre_l('Value', Options.units_roughness[self.params.options.units][self.params.options.headloss]))  # TODO: softcode

        self.params.options.headloss_units = self.cbo_headloss.itemData(self.cbo_headloss.currentIndex())

        self.parent.update_roughness_params(
            self.parent.cbo_pipe_roughness.itemData(self.parent.cbo_pipe_roughness.currentIndex())[self.params.options.headloss])

        # self.parent.lbl_pipe_roughness.setText(
        #     pre_l(
        #         'Roughness',
        #         self.params.options.units_roughness[self.params.options.units][self.params.options.headloss_units]))


        # Pumps
        self.parent.lbl_pump_head.setText(pre_l('Head', self.params.options.units_deltaz[self.params.options.units]))
        self.parent.lbl_pump_power.setText(pre_l('Power', self.params.options.units_power[self.params.options.units]))

        # Valves
        valve_type = self.parent.cbo_valve_type.itemData(self.parent.cbo_valve_type.currentIndex())

        # Pressure valves
        if valve_type == Valve.type_psv or valve_type == Valve.type_prv or valve_type == Valve.type_pbv:
            self.parent.lbl_valve_setting.setText(
                pre_l('Pressure', self.params.options.units_pressure[self.params.options.units]))
        # FCV valve: Flow
        if valve_type == Valve.type_fcv:
            self.parent.lbl_valve_setting.setText(
                pre_l('Flow', self.params.options.flow_units))
        # Throttle control valve
        elif valve_type == Valve.type_tcv:
            self.parent.lbl_valve_setting.setText(
                pre_l('Loss coeff.', '-'))
        # self.parent.lbl_valve_diameter.setText(pre_l('Pressure', self.params.options.units_diameter_pipes[self.params.options.units]))

        # Flow units
        units = self.cbo_flow_units.itemData(self.cbo_flow_units.currentIndex())
        self.parent.lbl_junction_demand.setText(pre_l('Demand', units))  # TODO: softcode
        self.parent.lbl_pipe_demand.setText(pre_l('Demand', units))  # TODO: softcode

        self.setVisible(False)

    def check_params(self):

        if self.chk_hydraulics.isChecked():
            if not os.path.isfile(self.txt_hydraulics_file.text()):
                QMessageBox.warning(
                    self,
                    Parameters.plug_in_name,
                    u'Hydraulics option slected, but no valid file specified.',
                    QMessageBox.Ok)
                return False

        return True


class QualityDialog(QDialog):

    def __init__(self, parent, params):

        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params

        self.setMinimumWidth(min_width)
        # self.setMinimumHeight(min_height)

        # Build dialog
        self.setWindowTitle('Options - Quality')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_parameter = QLabel('Parameter:')  # TODO: softocode
        self.cbo_parameter = QComboBox()
        fra_form_lay.addRow(self.lbl_parameter, self.cbo_parameter)

        self.lbl_mass_units = QLabel('Mass units:')  # TODO: softocode
        self.cbo_mass_units = QComboBox()
        fra_form_lay.addRow(self.lbl_mass_units, self.cbo_mass_units)

        self.lbl_diffusivity = QLabel('Relative diffusivity:')  # TODO: softocode
        self.txt_diffusivity = QLineEdit()
        fra_form_lay.addRow(self.lbl_diffusivity, self.txt_diffusivity)

        self.lbl_trace_node = QLabel('Trace node:')  # TODO: softocode
        self.txt_trace_node = QLineEdit()
        fra_form_lay.addRow(self.lbl_trace_node, self.txt_trace_node)

        self.lbl_quality_tol = QLabel('Quality tolerance:')  # TODO: softocode
        self.txt_quality_tol = QLineEdit()
        fra_form_lay.addRow(self.lbl_quality_tol, self.txt_quality_tol)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Ok = QPushButton('OK')
        self.btn_Cancel = QPushButton('Cancel')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):
        for key, value in self.params.options.quality.quality_text.items():
            self.cbo_parameter.addItem(value, key)

        for key, value in self.params.options.quality.quality_units_text.items():
            self.cbo_mass_units.addItem(value, key)

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

        # Validators
        self.txt_diffusivity.setValidator(RegExValidators.get_pos_decimals())
        self.txt_quality_tol.setValidator(RegExValidators.get_pos_decimals())

    def show(self):
        super(QualityDialog, self).show()

        self.cbo_parameter.setCurrentIndex(self.cbo_parameter.findData(self.params.options.quality.parameter))
        self.cbo_mass_units.setCurrentIndex(self.cbo_mass_units.findData(self.params.options.quality.mass_units))
        self.txt_diffusivity.setText(str(self.params.options.diffusivity))
        self.txt_trace_node.setText(str(self.params.options.quality.trace_junction_id))
        self.txt_quality_tol.setText(str(self.params.options.quality.quality_tol))

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        # Update parameters and options
        self.params.options.quality.parameter = self.cbo_parameter.itemData(self.cbo_parameter.currentIndex())
        self.params.options.quality.mass_units = self.cbo_mass_units.itemData(self.cbo_mass_units.currentIndex())

        self.params.options.diffusivity = float(self.txt_diffusivity.text())
        self.params.options.quality.trace_junction_id = self.txt_trace_node.text()
        self.params.options.quality.quality_tol = float(self.txt_quality_tol.text())

        self.setVisible(False)


class ReactionsDialog(QDialog):

    def __init__(self, parent, params):

        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params

        self.setMinimumWidth(min_width)

        # Build dialog
        self.setWindowTitle('Options - Reactions')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_bulk_reaction_order = QLabel('Bulk reaction order:')  # TODO: softocode
        self.txt_bulk_reaction_order = QLineEdit('1')
        fra_form_lay.addRow(self.lbl_bulk_reaction_order, self.txt_bulk_reaction_order)

        self.lbl_tank_reaction_order = QLabel('Tank reaction order:')  # TODO: softocode
        self.txt_tank_reaction_order = QLineEdit('1')
        fra_form_lay.addRow(self.lbl_tank_reaction_order, self.txt_tank_reaction_order)

        self.lbl_wall_reaction_order = QLabel('Wall reaction order:')  # TODO: softocode
        self.txt_wall_reaction_order = QLineEdit('1')
        fra_form_lay.addRow(self.lbl_wall_reaction_order, self.txt_wall_reaction_order)

        self.lbl_global_bulk_coeff = QLabel('Global bulk coeff.:')  # TODO: softocode
        self.txt_global_bulk_coeff = QLineEdit('1')
        fra_form_lay.addRow(self.lbl_global_bulk_coeff, self.txt_global_bulk_coeff)

        self.lbl_global_wall_coeff = QLabel('Global wall coeff.:')  # TODO: softocode
        self.txt_global_wall_coeff = QLineEdit('0')
        fra_form_lay.addRow(self.lbl_global_wall_coeff, self.txt_global_wall_coeff)

        self.lbl_limiting_conc = QLabel('Limiting concentration:')  # TODO: softocode
        self.txt_limiting_conc = QLineEdit('0')
        fra_form_lay.addRow(self.lbl_limiting_conc, self.txt_limiting_conc)

        self.lbl_wall_coeff_corr = QLabel('Wall coeff. correlation:')  # TODO: softocode
        self.txt_wall_coeff_corr = QLineEdit('0')
        fra_form_lay.addRow(self.lbl_wall_coeff_corr, self.txt_wall_coeff_corr)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Ok = QPushButton('OK')
        self.btn_Cancel = QPushButton('Cancel')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

        self.txt_bulk_reaction_order.setValidator(RegExValidators.get_pos_01())
        self.txt_wall_reaction_order.setValidator(RegExValidators.get_pos_01())
        self.txt_tank_reaction_order.setValidator(RegExValidators.get_pos_01())
        self.txt_global_bulk_coeff.setValidator(RegExValidators.get_pos_01())
        self.txt_global_wall_coeff.setValidator(RegExValidators.get_pos_01())
        self.txt_limiting_conc.setValidator(RegExValidators.get_pos_decimals())
        self.txt_wall_coeff_corr.setValidator(RegExValidators.get_pos_decimals())

    def show(self):
        super(ReactionsDialog, self).show()

        self.txt_bulk_reaction_order.setText(str(self.params.reactions.order_bulk))
        self.txt_tank_reaction_order.setText(str(self.params.reactions.order_tank))
        self.txt_wall_reaction_order.setText(str(self.params.reactions.order_wall))
        self.txt_global_bulk_coeff.setText(str(self.params.reactions.global_bulk))
        self.txt_global_wall_coeff.setText(str(self.params.reactions.global_wall))
        self.txt_limiting_conc.setText(str(self.params.reactions.limiting_potential))
        self.txt_wall_coeff_corr.setText(str(self.params.reactions.roughness_corr))

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        # Update parameters and options
        self.params.reactions.order_bulk = int(self.txt_bulk_reaction_order.text())
        self.params.reactions.order_tank = int(self.txt_tank_reaction_order.text())
        self.params.reactions.order_wall = int(self.txt_wall_reaction_order.text())
        self.params.reactions.global_bulk = int(self.txt_global_bulk_coeff.text())
        self.params.reactions.global_wall = int(self.txt_global_wall_coeff.text())
        self.params.reactions.limiting_potential = float(self.txt_limiting_conc.text())
        self.params.reactions.roughness_corr = float(self.txt_wall_coeff_corr.text())

        self.setVisible(False)


class TimesDialog(QDialog):

    def __init__(self, parent, params):

        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params

        self.setMinimumWidth(min_width)

        # Build dialog
        self.setWindowTitle('Options - Times')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_units = QLabel('Units:')  # TODO: softocode
        self.cbo_units = QComboBox()
        fra_form_lay.addRow(self.lbl_units, self.cbo_units)

        self.lbl_duration = QLabel('Duration:')  # TODO: softocode
        self.txt_duration = QLineEdit()
        fra_form_lay.addRow(self.lbl_duration, self.txt_duration)

        self.lbl_hydraulic_timestep = QLabel('Hydraulic timestep:')  # TODO: softocode
        self.txt_hydraulic_timestep = QLineEdit()
        fra_form_lay.addRow(self.lbl_hydraulic_timestep, self.txt_hydraulic_timestep)

        self.lbl_quality_timestep = QLabel('Quality timestep:')  # TODO: softocode
        self.txt_quality_timestep = QLineEdit()
        fra_form_lay.addRow(self.lbl_quality_timestep, self.txt_quality_timestep)

        self.lbl_rule_timestep = QLabel('Rule timestep:')  # TODO: softocode
        self.txt_rule_timestep = QLineEdit()
        fra_form_lay.addRow(self.lbl_rule_timestep, self.txt_rule_timestep)

        self.lbl_pattern_timestep = QLabel('Pattern timestep:')  # TODO: softocode
        self.txt_pattern_timestep = QLineEdit()
        fra_form_lay.addRow(self.lbl_pattern_timestep, self.txt_pattern_timestep)

        self.lbl_pattern_start = QLabel('Pattern start:')  # TODO: softocode
        self.txt_pattern_start = QLineEdit()
        fra_form_lay.addRow(self.lbl_pattern_start, self.txt_pattern_start)

        self.lbl_report_timestep = QLabel('Report timestep:')  # TODO: softocode
        self.txt_report_timestep = QLineEdit()
        fra_form_lay.addRow(self.lbl_report_timestep, self.txt_report_timestep)

        self.lbl_report_start = QLabel('Report start:')  # TODO: softocode
        self.txt_report_start = QLineEdit()
        fra_form_lay.addRow(self.lbl_report_start, self.txt_report_start)

        self.lbl_clock_time_start = QLabel('Clock start time:')  # TODO: softocode
        self.txt_clock_time_start = QLineEdit()
        fra_form_lay.addRow(self.lbl_clock_time_start, self.txt_clock_time_start)

        self.lbl_statistic = QLabel('Statistic:')  # TODO: softocode
        self.cbo_statistic = QComboBox()
        fra_form_lay.addRow(self.lbl_statistic, self.cbo_statistic)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Ok = QPushButton('OK')
        self.btn_Cancel = QPushButton('Cancel')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):

        for key, text in self.params.times.unit_text.items():
            self.cbo_units.addItem(text, key)

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

        # Validators
        self.txt_duration.setValidator(RegExValidators.get_pos_int())

        self.txt_duration.setInputMask('0009:99')
        self.txt_duration.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_hydraulic_timestep.setInputMask('009:99')
        self.txt_hydraulic_timestep.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_quality_timestep.setInputMask('009:99')
        self.txt_quality_timestep.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_rule_timestep.setInputMask('009:99')
        self.txt_rule_timestep.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_pattern_timestep.setInputMask('009:99')
        self.txt_pattern_timestep.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_pattern_start.setInputMask('09:99')
        self.txt_pattern_start.setValidator(RegExValidators.get_time_hh_mm())

        self.txt_report_timestep.setInputMask('009:99')
        self.txt_report_timestep.setValidator(RegExValidators.get_time_hs_mm())

        self.txt_report_start.setInputMask('09:99')
        self.txt_report_start.setValidator(RegExValidators.get_time_hh_mm())

        self.txt_clock_time_start.setInputMask('09:99')
        self.txt_clock_time_start.setValidator(RegExValidators.get_time_hh_mm())

        for key, text in self.params.times.stats_text.items():
            self.cbo_statistic.addItem(text, key)

    def show(self):
        super(TimesDialog, self).show()

        # self.cbo_units.setCurrentIndex(self.cbo_units.findData(self.params.times.units))
        self.txt_duration.setText(self.params.times.duration.get_as_text(4))
        self.txt_hydraulic_timestep.setText(self.params.times.hydraulic_timestep.get_as_text(3))
        self.txt_quality_timestep.setText(self.params.times.quality_timestep.get_as_text(3))
        self.txt_rule_timestep.setText(self.params.times.rule_timestep.get_as_text(3))
        self.txt_pattern_timestep.setText(self.params.times.pattern_timestep.get_as_text(3))
        self.txt_pattern_start.setText(self.params.times.pattern_start.get_as_text())
        self.txt_report_timestep.setText(self.params.times.report_timestep.get_as_text(3))
        self.txt_report_start.setText(self.params.times.report_start.get_as_text())
        self.txt_clock_time_start.setText(self.params.times.clocktime_start.get_as_text())
        self.cbo_statistic.setCurrentIndex(self.cbo_statistic.findData(self.params.times.statistic))

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        # Update parameters and options
        # self.params.times.units = self.cbo_units.itemData(self.cbo_units.currentIndex())
        self.params.times.duration = Hour.from_string(self.txt_duration.text())
        self.params.times.hydraulic_timestep = Hour.from_string(self.txt_hydraulic_timestep.text())
        self.params.times.quality_timestep = Hour.from_string(self.txt_quality_timestep.text())
        self.params.times.rule_timestep = Hour.from_string(self.txt_rule_timestep.text())
        self.params.times.pattern_timestep = Hour.from_string(self.txt_pattern_timestep.text())
        self.params.times.pattern_start = Hour.from_string(self.txt_pattern_start.text())
        self.params.times.report_timestep = Hour.from_string(self.txt_report_timestep.text())
        self.params.times.report_start= Hour.from_string(self.txt_report_start.text())
        self.params.times.clocktime_start = Hour.from_string(self.txt_clock_time_start.text())
        self.params.times.statistic = self.cbo_statistic.currentIndex()

        self.setVisible(False)


class EnergyDialog(QDialog):

    def __init__(self, parent, params):

        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params

        self.setMinimumWidth(min_width)
        # self.setMinimumHeight(min_height)

        # Build dialog
        self.setWindowTitle('Options - Energy')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_pump_efficiency = QLabel('Pump efficiency [%]:')  # TODO: softocode
        self.txt_pump_efficiency = QLineEdit()
        fra_form_lay.addRow(self.lbl_pump_efficiency, self.txt_pump_efficiency)

        self.lbl_energy_price = QLabel('Energy price/kwh:')  # TODO: softocode
        self.txt_energy_price = QLineEdit()
        fra_form_lay.addRow(self.lbl_energy_price, self.txt_energy_price)

        self.lbl_price_pattern = QLabel('Price pattern:')  # TODO: softocode
        self.txt_price_pattern = QLineEdit() # TODO: replace with dropdown
        fra_form_lay.addRow(self.lbl_price_pattern, self.txt_price_pattern)

        self.lbl_demand_charge = QLabel('Demand charge:')  # TODO: softocode
        self.txt_demand_charge = QLineEdit()
        fra_form_lay.addRow(self.lbl_demand_charge, self.txt_demand_charge)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Ok = QPushButton('OK')
        self.btn_Cancel = QPushButton('Cancel')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

        # Validators
        self.txt_pump_efficiency.setValidator(RegExValidators.get_pos_decimals())
        self.txt_energy_price.setValidator(RegExValidators.get_pos_decimals())
        self.txt_price_pattern.setValidator(RegExValidators.get_pos_int())
        self.txt_demand_charge.setValidator(RegExValidators.get_pos_decimals())

    def show(self):
        super(EnergyDialog, self).show()
        self.txt_pump_efficiency.setText(str(self.params.energy.pump_efficiency))
        self.txt_energy_price.setText(str(self.params.energy.energy_price))
        self.txt_price_pattern.setText(str(self.params.energy.price_pattern) if self.params.energy.price_pattern is not None else '')

        self.lbl_price_pattern.setEnabled(False) # TODO
        self.txt_price_pattern.setEnabled(False) # TODO

        self.txt_demand_charge.setText(str(self.params.energy.demand_charge))

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        self.params.energy.pump_efficiency =  float(self.txt_pump_efficiency.text())
        self.params.energy.energy_price = float(self.txt_energy_price.text())
        self.params.energy.price_pattern = self.txt_price_pattern.text()
        self.params.energy.demand_charge = float(self.txt_demand_charge.text())

        self.setVisible(False)


class ReportDialog(QDialog):

    def __init__(self, parent, params):

        QDialog.__init__(self, parent)

        self.parent = parent
        self.params = params

        self.setMinimumWidth(min_width)
        # self.setMinimumHeight(min_height)

        # Build dialog
        self.setWindowTitle('Options - Report')  # TODO: softcode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.fra_form = QFrame(self)
        fra_form_lay = QFormLayout(self.fra_form)
        fra_form_lay.setContentsMargins(10, 10, 10, 10)

        self.lbl_status = QLabel('Hydraulic status:')  # TODO: softocode
        self.cbo_status = QComboBox()
        fra_form_lay.addRow(self.lbl_status, self.cbo_status)

        self.lbl_summary = QLabel('Summary')  # TODO: softocode
        self.cbo_summary = QComboBox()
        fra_form_lay.addRow(self.lbl_summary, self.cbo_summary)

        self.lbl_energy = QLabel('Energy')  # TODO: softocode
        self.cbo_energy = QComboBox()
        fra_form_lay.addRow(self.lbl_energy, self.cbo_energy)

        self.lbl_nodes = QLabel('Nodes')  # TODO: softocode
        self.cbo_nodes = QComboBox()
        fra_form_lay.addRow(self.lbl_nodes, self.cbo_nodes)

        self.lbl_links = QLabel('Links')  # TODO: softocode
        self.cbo_links = QComboBox()
        fra_form_lay.addRow(self.lbl_links, self.cbo_links)

        # Buttons
        self.fra_buttons = QFrame(self)
        fra_buttons_lay = QHBoxLayout(self.fra_buttons)
        self.btn_Ok = QPushButton('OK')
        self.btn_Cancel = QPushButton('Cancel')
        fra_buttons_lay.addWidget(self.btn_Ok)
        fra_buttons_lay.addWidget(self.btn_Cancel)

        # Add to main
        fra_main_lay = QVBoxLayout(self)
        fra_main_lay.setContentsMargins(0, 0, 0, 0)
        fra_main_lay.addWidget(self.fra_form)
        fra_main_lay.addWidget(self.fra_buttons)

        self.setup()

    def setup(self):

        # Combos
        for key, value in Report.status_names.items():
            self.cbo_status.addItem(value, key)

        for key, value in Report.summary_names.items():
            self.cbo_summary.addItem(value, key)

        for key, value in Report.energy_names.items():
            self.cbo_energy.addItem(value, key)

        for key, value in Report.nodes_names.items():
            self.cbo_nodes.addItem(value, key)

        for key, value in Report.links_names.items():
            self.cbo_links.addItem(value, key)

        # Buttons
        self.btn_Cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_Ok.clicked.connect(self.btn_ok_clicked)

    def show(self):
        super(ReportDialog, self).show()
        self.cbo_status.setCurrentIndex(self.cbo_status.findData(self.params.report.status))
        self.cbo_summary.setCurrentIndex(self.cbo_summary.findData(self.params.report.summary))
        self.cbo_energy.setCurrentIndex(self.cbo_energy.findData(self.params.report.energy))
        self.cbo_nodes.setCurrentIndex(self.cbo_nodes.findData(self.params.report.nodes))
        self.cbo_links.setCurrentIndex(self.cbo_links.findData(self.params.report.links))

    def btn_cancel_clicked(self):
        self.setVisible(False)

    def btn_ok_clicked(self):

        self.params.report.status = self.cbo_status.itemData(self.cbo_status.currentIndex())
        self.params.report.summary = self.cbo_summary.itemData(self.cbo_summary.currentIndex())
        self.params.report.energy = self.cbo_energy.itemData(self.cbo_energy.currentIndex())
        self.params.report.nodes = self.cbo_nodes.itemData(self.cbo_nodes.currentIndex())
        self.params.report.links = self.cbo_links.itemData(self.cbo_links.currentIndex())

        self.setVisible(False)
