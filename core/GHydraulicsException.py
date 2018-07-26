from builtins import str
#
# This file is part of GHydraulics
#
# GHydraulicsExceptions.py - Exceptions raised and handled by GHydraulics
#
# Copyright 2012 Steffen Macke <sdteffen@sdteffen.de>
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

class GHydraulicsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
