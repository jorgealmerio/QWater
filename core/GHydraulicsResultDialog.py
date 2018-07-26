from __future__ import absolute_import
#
# This file is part of GHydraulics
#
# GHydraulicsResultDialog.py - Display EPANET results
#
# Copyright 2014 Steffen Macke <sdteffen@sdteffen.de>
#
# GHydraulics is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2, or (at your option) any later version.
#
# GHydraulics is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with program; see the file COPYING. If not,
# write to the Free Software Foundation, Inc., 59 Temple Place
# - Suite 330, Boston, MA 02111-1307, USA.
#
# QGIS 2.0.0 or better required to run this file
#
from pickle import *
import os
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import *
from qgis.gui import *
from .Ui_GHydraulicsResultDialog import *

class GHydraulicsResultDialog(QDialog):

    # User clicked "OK"
    def accepted(self):
        if 0 < self.ui.comboStep.count():
            self.setStep(self.ui.comboStep.currentIndex())

    def __init__(self, setStepCallback):
        QDialog.__init__(self)
        self.setStep = setStepCallback
        self.ui = Ui_GHydraulicsResultDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accepted)
