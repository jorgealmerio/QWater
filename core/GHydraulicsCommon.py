from __future__ import absolute_import
from builtins import str
from builtins import object
#
# This file is part of GHydraulics
#
# GHydraulicsCommon.py - Base class
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

from pickle import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis import *
from .EpanetModel import *
from .GHydraulicsException import *

# Base class with common functionality
class GHydraulicsCommon(object):
    NAME = 'QWater'
    SETTINGS='QWater'#Almerio: acrescentei essa variavel

    # message logging
    def log(self, message):
        QgsMessageLog.logMessage(message, self.NAME)

    # Read the layers from the project
    def getLayers(self):
        self.layers = {}
        project = QgsProject.instance()
        for section in EpanetModel.GIS_SECTIONS:
            pickle_list = str(project.readEntry(self.SETTINGS, section, "")[0])
            if '' != pickle_list:
                l = [pickle_list]
                self.layers[section] = l
            else:
                self.layers[section] = []

    # Ensure that we work with a point geometry
    def getFirstMultiPoint(self, geometry):
        collection = geometry.asGeometryCollection()
        if 0 < len(collection):
            return collection[0].asPoint()
        return geometry.asPoint()

    # Run the given callback function on each layer
    def eachLayer(self, callback, sections=EpanetModel.GIS_SECTIONS):
        # loop over all sections
        for section in sections:
            #loop over all layers
            if section not in self.layers:
                continue
            for name in self.layers[section]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        callback(layer)

    # Begin an edit command on all model layers
    def beginEditCommand(self, command):
        self.editCommand = command
        self.log(command)
        self.eachLayer(self.beginEditLayer)

    # Ensure editable layer, issue edit command
    def beginEditLayer(self, layer):
        if not layer.isEditable() and not layer.startEditing():
            raise GHydraulicsException('ERROR: Unable to edit layer '+layer.name())
        layer.beginEditCommand(self.editCommand)

    # Finish editing command on all layers
    def endEditCommand(self):
        self.eachLayer(self.endEditLayer)

    # Finish editing command on a given layer
    def endEditLayer(self, layer):
        layer.endEditCommand()

    # Return the field name index or raise an exception
    def fieldNameIndex(self, layer, fieldname):
        idx = layer.dataProvider().fieldNameIndex(fieldname)
        if -1 == idx:
            raise GHydraulicsException('ERROR: Failed to locate '+fieldname+' field in layer '+layer.name())
        return idx
