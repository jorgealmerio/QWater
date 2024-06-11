from __future__ import absolute_import
from builtins import range
from builtins import object
#
# This file is part of GHydraulics
#
# EpanetResultReader.py - Read EPANET binary result files
#
# Copyright 2013, 2014 Steffen Macke <sdteffen@sdteffen.de>
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

import array
import os

from .GHydraulicsModel import *

# Read EPANET binary result files
class EpanetResultReader(object):
    # Describe the file structure, 4byte offsets(SEEK_SET)
    NODECOUNT = 2
    TANKCOUNT = 3
    LINKCOUNT = 4
    PUMPCOUNT = 5
    REPORTSTART = 12
    REPORTTIMESTEP = 13
    DURATION = 14

    #byte offsets (SEEK_SET)
    OFFSET_NODES = 884

    # close the underlying file
    def close(self):
        self.b.close()

    # Return a dictionary of node results for the given timestep and id
    def getNodeResult(self, step, id):
        results = {}
        offset = self.nodes[id.encode()] + step * (4 * self.nodecount + 8 * self.linkcount)
        #print('step={},len(self.nfa)={},offset={}'.format(step,len(self.nfa),offset))
        for field in GHydraulicsModel.NODE_RESULTS:
            results[field] = self.nfa[offset]
            offset = offset + self.nodecount
        return results

    # Return a dictionary of link results for the given timestep and id
    def getLinkResult(self, step, id):
        results = {}
        offset = self.links[id.encode()] + step * (4 * self.nodecount + 8 * self.linkcount)
        for field in GHydraulicsModel.LINK_RESULTS:
            results[field] = self.lfa[offset]
            offset = offset + self.linkcount
        return results


    # Read the given binary result file
    def __init__(self, filename):
        self.b = open(filename, 'rb')
        # store base data
        self.ia = array.array('i')
        self.ia.fromfile(self.b, 15)
        periods = self.ia[self.DURATION]//self.ia[self.REPORTTIMESTEP] + 1
        self.nodecount = self.ia[self.NODECOUNT]
        self.linkcount = self.ia[self.LINKCOUNT]
        # store node data
        self.nca = array.array('u') #Almerio: was 'c' character type, but is python>3 deprecated
        self.b.seek(self.OFFSET_NODES)
        self.nodes = {}
        for i in range(0,self.nodecount):
            lido = self.b.read(32)
            ind = lido.replace(b'\00',''.encode())
            self.nodes[ind] = i
        self.nfa = array.array('f')
        resultoffset = self.OFFSET_NODES + (36*self.nodecount) + (52*self.linkcount) + (8*self.ia[self.TANKCOUNT]) + (28*self.ia[self.PUMPCOUNT]) +  4
        self.b.seek(resultoffset)
        self.nfa.fromfile(self.b, 4 * self.nodecount * periods)
        # store link data
        self.lca = array.array('u') #Almerio: was 'c' character type, but is python>3 deprecated
        self.b.seek(self.OFFSET_NODES + (32*self.nodecount))
        self.links = {}
        for i in range(0,self.linkcount):
            lido = self.b.read(32)
            ind = lido.replace(b'\00',''.encode())
            self.links[ind] = i
        self.lfa = array.array('f')
        self.b.seek(resultoffset +  (16*self.nodecount))
        self.lfa.fromfile(self.b, 7 * self.linkcount * periods)
