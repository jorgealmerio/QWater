from __future__ import absolute_import
from builtins import object
#! /usr/bin/env python
#
# This file is part of GHydraulics
#
# ghyeconomicdiameter.py - Assign economic diameters based on the flow results
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
# The QGIS Python bindings are required to run this file
#

from qgis.core import *
from qgis.PyQt.QtCore import *
import sys
from .GHydraulicsException import *

class GhyEconomicDiameter(object):
    flofieldname = "RESULT_FLO"
    diafieldname = "DIAMETER"
    # Create the dictionary of economic diameters
    # flows are in l/s, diameters in mm
    # Jorge Almerio: PBA CL12 (DN 50, 75 e 100) e PVC DEFoFo (DN 150,200,250,300,350,400,500); Formula de Bresse
    diceconomic = {0.98:  54.6,
                   2.49:  77.2,
                   6.20:  108.4,
                   16.48:  156.4,
                   33.49:  204.2,
                   58.51:  252,
                   92.69:  299.8,
                   137.07:  347.6,
                   191.62:  394.6,
                   338.16:  489.4,}

    def __init__(self, flowfieldname, diameterfieldname):
        self.flofieldname = flowfieldname
        self.diafieldname = diameterfieldname

    def commitEconomicDiametersForLayer(self, vlayer):
        feature = QgsFeature()
        provider = vlayer.dataProvider()
        allAttrs = provider.attributeIndexes()

        # Locate fields
        diafieldidx = provider.fieldNameIndex(self.diafieldname)
        flowfieldidx = provider.fieldNameIndex(self.flofieldname)

        if -1 == diafieldidx:
            raise GHydraulicsException('ERROR: Unable to locate the "'+self.diafieldname+'" field')
        if -1 == flowfieldidx:
            raise GHydraulicsException('ERROR: Unable to locate the "'+self.flofieldname+'" field')

        economicflows = list(self.diceconomic.keys())
        economicflows.sort()
        dicattributechanges = {}

        # Loop over all features
        iter = vlayer.getFeatures()
        for feature in iter:
            # Fetch result_flow attribute
            attrs = feature.attributes()
            flow = abs(attrs[flowfieldidx]) #Almerio: acrescentei a funcao 'abs' aqui para trazer o valor absoluto da vazao
            # Look up the economic diameter from the dictionary
            biggerflow = 4.0
            for economicflow in economicflows:
                if economicflow > flow:
                    biggerflow = economicflow
                    break
            economicdiameter = self.diceconomic[biggerflow]
            # Indicate when dictionary is not valid any more
            if flow > biggerflow:
                economicdiameter = 9999
            vlayer.changeAttributeValue(feature.id(), diafieldidx ,economicdiameter)
