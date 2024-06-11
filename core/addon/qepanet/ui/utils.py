import math
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QSize

from ..geo_utils import raster_utils


def dist(x1, y1, x2, y2, pt_x, pt_y):  # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u = ((pt_x - x1) * px + (pt_y - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - pt_x
    dy = y - pt_y

    return math.sqrt(dx*dx + dy*dy)


def prepare_label(label, units):

        if units is not None:
            label += ' ['
            label += units
            label += ']:'

        return label


def set_up_button(button, icon_path, checkable=False, w=None, h=None, tooltip_text=None):
    button.setText('')
    button.setIcon(QIcon(icon_path))
    if w is not None and h is not None:
        button.setIconSize(QSize(w, h))
    button.setCheckable(checkable)
    if tooltip_text is not None:
        button.setToolTip(tooltip_text)



