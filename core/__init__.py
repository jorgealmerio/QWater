#! /usr/bin/env python
#
# This file is part of GHydraulics
#
# __init__.py - load GHydraulicsPlugin class from file ghydraulicsplugin.py
#
# Copyright 2007 - 2013 Steffen Macke <sdteffen@sdteffen.de>
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

from __future__ import absolute_import
from .QWaterPlugin import QWaterPlugin

def name():
    return "QWater"

def description():
    return "Hydraulic network analysis functionality (using EPANET)."

def version():
    return "Version "+QWaterPlugin.VERSION

def qgisMinimumVersion():
    return "3.0"

def classFactory(iface):
    return QWaterPlugin(iface)
