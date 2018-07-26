from builtins import object
#
# This file is part of GHydraulics
#
# GHydraulicsInpReader.py - parse EPANET Inp files
#
# Copyright 2013 Steffen Macke <sdteffen@sdteffen.de>
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

import shlex

class GHydraulicsInpReader(object):
    SECTIONSTART = '['

    def getValue(self, section, variable):
        handle = open(self.filename, "r")
        lexer = shlex.shlex(handle)
        value = ''
        sectionstart = False
        currentsection = ''
        currentvariable = ''
        while True:
            token = lexer.get_token()
            if not token:
                break
            if sectionstart:
                currentsection = token
            sectionstart = (self.SECTIONSTART == token)
            if currentsection == section:
                if currentvariable == variable:
                    value = token
                    break
                currentvariable = token
        handle.close()
        return value

    def __init__(self, filename):
        self.filename = filename
