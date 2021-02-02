from builtins import object
#
# This file is part of GHydraulics
#
# EpanetModel.py - Encapsulates EPANET model stucture and logic
#
# Copyright 2007 - 2014 Steffen Macke <sdteffen@sdteffen.de>
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

# Describe the model structure
class EpanetModel(object):
    GIS_SECTIONS = ['JUNCTIONS', 'PIPES', 'RESERVOIRS', 'ZONES', 'PUMPS', 'VALVES', 'TANKS']
    COLUMNS = {'JUNCTIONS': ['DC_ID', 'ELEVATION', 'DEMAND', 'PATTERN'],
               'PIPES': ['DC_ID', 'NODE1', 'NODE2', 'LENGTH', 'DIAMETER', 'ROUGHNESS', 'MINORLOSS', 'STATUS'],
               'RESERVOIRS': ['DC_ID', 'HEAD', 'PATTERN'],
               'ZONES': ['DC_ID', 'DEMAND'],
               'TANKS': ['DC_ID', 'ELEVATION', 'INITIALLEV', 'MINIMUMLEV', 'MAXIMUMLEV', 'DIAMETER', 'MINIMUMVOL', 'VOLUMECURV'],
               'PUMPS': ['DC_ID','ELEVATION', 'PROPERTIES'],
               'VALVES': ['DC_ID', 'ELEVATION', 'DIAMETER', 'TYPE', 'SETTING', 'MINORLOSS']}
    #Almerio: Additional columns to be created, but not part of Epanet fields
    EXTRACOLUMNS = {'JUNCTIONS': ['DEMAND_PTO'],
                    'PIPES': [],
                    'RESERVOIRS': [],
                    'ZONES': [],
                    'TANKS': [],
                    'PUMPS': [],
                    'VALVES': []}
    COORDINATE_SECTIONS = ['JUNCTIONS', 'RESERVOIRS', 'TANKS']
    COORDINATE_DATA_SECTIONS = ['COORDINATES','VERTICES']
    VIRTUAL_LINE_SECTIONS = ['PUMPS','VALVES']
    # Link sections share common ID namespace
    LINK_SECTIONS = ['PIPES','PUMPS','VALVES']
    # GIS nodes are different, see GHydraulicsModel.NODE_SECTIONS
    NODE_SECTIONS = ['JUNCTIONS', 'RESERVOIRS', 'TANKS']

    # List of units where length is in feet
    FEET_UNITS = ['CFS', 'GPM', 'MGD', 'IMGD', 'AFD']

    NODE1 = 'NODE1'
    NODE2 = 'NODE2'
    NODE_FIELDS = [NODE1, NODE2]
    COORDINATES = 'COORDINATES'
    DIAMETER = 'DIAMETER'
    JUNCTIONS = 'JUNCTIONS'
    MINORLOSS = 'MINORLOSS'
    PIPES = 'PIPES'
    SETTING = 'SETTING'
    STATUS = 'STATUS'
    TYPE = 'TYPE'
    VALVES = 'VALVES'
    VERTICES = 'VERTICES'
    LENGTH = 'LENGTH'
    LPS = 'LPS'
