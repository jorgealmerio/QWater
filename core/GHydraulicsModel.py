from builtins import object
#
# This file is part of GHydraulics
#
# GHydraulicsModel.py - Encapsulates GHydraulics model stucture and logic
#
# Copyright 2012 - 2014 Steffen Macke <sdteffen@sdteffen.de>
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

from qgis.PyQt.QtCore import *
from qgis.core import *

# Describe the model structure
class GHydraulicsModel(object):
    # GIS nodes are different. See EpanetModel.NODE_SECTIONS
    NODE_SECTIONS = ['JUNCTIONS', 'RESERVOIRS', 'PUMPS', 'VALVES', 'TANKS']
    ID_FIELD = 'DC_ID'

    # maximum distance between nodes and line end vertices
    SNAP_RADIUS = 0.1

    # Intended length of virtual lines. Actual virtual lines might be shorter,
    # depending on the length of the first segment
    VIRTUAL_LINE_LENGTH = 1.0
    VIRTUAL_POSTFIX = 'dn'

    # Preferred column types
    COLUMN_TYPES = {
        'DC_ID': QVariant.String,
        'DIAMETER': QVariant.Double,
        'DEMAND': QVariant.Double,
        'DEMAND_PTO': QVariant.Double,
        'ELEVATION': QVariant.Double,
        'HEAD': QVariant.Double,
        'LENGTH': QVariant.Double,
        'INITIALLEV': QVariant.Double,
        'MAXIMUMLEV': QVariant.Double,
        'MINIMUMLEV': QVariant.Double,
        'MINIMUMVOL': QVariant.Double,
        'MINORLOSS': QVariant.Double,
        'NODE1': QVariant.String,
        'NODE2': QVariant.String,
        'PATTERN': QVariant.String,
        'PROPERTIES':QVariant.String,
        'ROUGHNESS': QVariant.Double, #Almerio: mudei esse campo de String para Double
        'SETTING': QVariant.String,
        'STATUS': QVariant.String,
        'TYPE': QVariant.String,
        'VOLUMECURV': QVariant.String,
        'RES_HEA_UP': QVariant.Double, #Almerio: adicionei esse campo para guardar a piezometrica a montante das bombas
        'RES_HEA_DN': QVariant.Double #Almerio: adicionei esse campo para guardar a piezometrica a jusante das bombas
        }
    # Node Input data column names by Almerio 
    NODE_INPUT = ['DEMAND_PTO']
    # Node result column names
    NODE_RESULTS = [
        'RESULT_DEM', 'RESULT_HEA', 'RESULT_PRE', 'RESULT_QUA'
    ]
    # Link result column names
    LINK_RESULTS = [
        'RESULT_FLO', 'RESULT_VEL', 'RESULT_HEA', 'RESULT_QUA', 'RESULT_STA', 'RESULT_REA', 'RESULT_FRI'
    ]

    STRING_TRUE = '1'
    STRING_FALSE = '0'

    UNITMAP = {QgsUnitTypes.DistanceDegrees: 'Degrees', QgsUnitTypes.DistanceFeet: 'Feet', QgsUnitTypes.DistanceMeters: 'Meters'}

    RESULT_FLO = 'RESULT_FLO'
