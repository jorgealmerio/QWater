from __future__ import absolute_import
from builtins import str
#! /usr/bin/env python
#
# This file is part of GHydraulics
#
# economicdiameter.py - economic diameters commandline interface
#
# Copyright 2007, 2009, 2014 Steffen Macke <sdteffen@sdteffen.de>
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
# The QGIS Python bindings are required to run this file
#

from qgis.core import *
from PyQt4.QtCore import *
import sys
from .GHydraulicsException import *
from .ghyeconomicdiameter import *

# Verify parameters

if 2 != len(sys.argv):
    sys.stderr.write("USAGE: economicdiameter.py shapefile")
    sys.exit()

# Supply path to where is your QGIS installed
QgsApplication.setPrefixPath("c:/OSGeo4W", True)

# Load providers
QgsApplication.initQgis()

vlayer = QgsVectorLayer(sys.argv[1], "Pipes", "ogr")

if not vlayer.isValid():
    sys.stderr.write("ERROR: Failed to load layer "+sys.argv[1])
    sys.exit()

if not vlayer.startEditing():
    sys.stderr.write("ERROR: Failed to edit layer "+sys.argv[1])
    sys.exit()

ecodia = GhyEconomicDiameter("RESULT_FLO", "DIAMETER",list(vlayer.getFeatures()))
try:
    ecodia.commitEconomicDiametersForLayer(vlayer)
except GHydraulicsException as e:
    sys.stderr(str(e))
    sys.exit()

if not vlayer.commitChanges():
    sys.stderr.write("ERROR: Failed to save edits to "+sys.argv[1])
    sys.exit()

QgsApplication.exitQgis()
