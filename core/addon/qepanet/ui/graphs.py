from builtins import range
from qgis.PyQt.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import numpy, numbers, math
#from ..model.binary_out_reader import OutputParamCodes
from ..model.options_report import Hour


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.figure.set_facecolor((1, 1, 1))
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.set_facecolor((1, 1, 1))
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes2 = None

    def compute_initial_figure(self):
        pass


class StaticMplCanvas(MyMplCanvas):

    def compute_initial_figure(self):
        pass

    def clear(self):
        self.axes.clear()
        if self.axes2 is not None:
            self.axes2.clear()
        self.draw()

    def draw_bars_graph(self, values, time_period=Hour(1, 0), y_axes_label='Multiplier'):

        width = 1.0
        lefts = []
        left_ticks_labels = []
        left_ticks = []
        max_val = -1

        multiplier_h = time_period.get_as_hours()
        ticks_nr = 10
        ticks_intv = math.ceil(len(values) / float(ticks_nr))

        for l in range(len(values)):
            lefts.append(l + 0.5)
            if isinstance((l * multiplier_h), int) and isinstance((l / ticks_intv), int):
                left_ticks.append(l)
                left_ticks_labels.append(l * multiplier_h)
            max_val = max(values[l], max_val)

        left_ticks.append(len(values))
        left_ticks_labels.append(len(values) * multiplier_h)

        if max_val == 0:
            max_val = 1

        # Average
        avg = numpy.average(values)

        if self.axes2 is None:
            self.axes2 = self.axes.twinx()

        self.axes2.cla()
        self.axes.cla()

        self.axes2.clear()
        self.axes2.plot([0, len(values)], [avg, avg], 'k--')
        self.axes2.set_ylim(0, max_val)
        self.axes2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

        self.axes.bar(lefts, values, width, color=(0, 0.5, 1), edgecolor=(0, 0, 0))
        self.axes.set_xlim(0, lefts[-1] + width)
        self.axes.set_ylim(0, max_val)
        self.axes.set_xticks(left_ticks)
        self.axes.set_xticklabels(left_ticks_labels)
        self.axes.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

        self.axes.set_xlabel('Time (Time period = ' + time_period.get_as_text() + ')')  # TODO: softcode
        self.axes.set_ylabel(y_axes_label)  # TODO: softcode
        self.axes.tick_params(axis=u'both', which=u'both', bottom=u'off', top=u'off', left=u'off', right=u'off')

        self.figure.tight_layout()

        self.draw()

    def draw_line_graph(self, xs, ys, x_label, y_label):

        self.axes.cla()
        self.axes.plot(xs, ys)

        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.tick_params(axis=u'both', which=u'both', bottom=u'off', top=u'off', left=u'off', right=u'off')
        self.axes.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        self.axes.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        self.figure.tight_layout()
        self.draw()

    def draw_output_line(self, xs, ys_d_d, params_count):

        self.figure.clf()

        # Convert secs to hours
        xs_h = [x / 3600 for x in xs]

        x_min = min(xs_h)
        x_max = max(xs_h)

        plot_pos = 1
        node_plot_count = -1
        link_plot_count = -1

        for param_id, ys_d in ys_d_d.items():

            param_type = OutputParamCodes.param_types[param_id]
            if param_type == OutputParamCodes.PARAM_TYPE_NODE:
                node_plot_count += 1
            elif param_type == OutputParamCodes.PARAM_TYPE_LINK:
                link_plot_count += 1

            axes = self.figure.add_subplot(params_count, 1, plot_pos)

            plot_args = []
            y_min = 1E6
            y_max = -1E6
            line_labels = []

            for element_id, ys in ys_d.items():

                y_min = min(y_min, min(ys[0]))
                y_max = max(y_max, max(ys[0]))

                plot_args.append(xs_h)
                plot_args.append(ys[0])
                # plot_args.append('-')

                line_labels.append(element_id)

            axes.tick_params(axis='both', which='major', labelsize=10)
            axes.set_title(OutputParamCodes.params_names[param_id], fontsize=10)

            # If this is not the last plot, hide the x ticks
            if plot_pos < params_count:
                axes.tick_params(axis='x', bottom='off', labelbottom='off')
            else:
                axes.set_xlabel('Time [h]', size='x-small')

            # Set axes limits
            axes.set_xlim(x_min, x_max)
            y_span = y_max - y_min
            axes.set_ylim(y_min - y_span * 0.1, y_max + y_span * 0.1)
            axes.set_ylabel(ys[1], size='x-small')

            # Format y axis label
            axes.yaxis.get_major_formatter().set_useOffset(False)
            axes.yaxis.get_major_formatter().set_scientific(False)

            # Plot lines
            lines = axes.plot(*plot_args)

            # If this is the first plot per type, add legend
            if param_type == OutputParamCodes.PARAM_TYPE_NODE and node_plot_count == 0 or \
                    param_type == OutputParamCodes.PARAM_TYPE_LINK and link_plot_count == 0:
                for l in range(len(lines)):
                    lines[l].set_label(line_labels[l])
                axes.legend(fontsize='x-small')

            plot_pos += 1

        self.figure.tight_layout(h_pad=0)
        self.draw()
