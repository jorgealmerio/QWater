from __future__ import absolute_import
from builtins import str
#
# This file is part of GHydraulics
#
# GHydraulicModelChecker.py - Create an EPANET model
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

import re
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from .EpanetModel import *
from .GHydraulicsCommon import *
from .GHydraulicsException import *
from .GHydraulicsModel import *

# Check for the necessary fields
class GHydraulicsModelChecker(GHydraulicsCommon):
    TITLE = 'Check Model'

    # Check that ids are unique throughout the model. There are two id
    # namespaces: One for Epanet nodes and one for links
    # Returns a dictionary of duplicate ids.
    # When checking for duplicate ids, there is one exception: Two pipes
    # connected to a virtual line can share the virtual line id.
    def checkIds(self):
        self.duplicate = {}
        self.unique = {}
        self.max = 1
        self.eachLayer(self.checkNodeLayerIds, EpanetModel.NODE_SECTIONS)
        self.geometry = {}
        self.eachLayer(self.checkLinkLayerIds, EpanetModel.LINK_SECTIONS)
        for id in self.geometry:
            geometries = len(self.geometry[id])
            if 1 == geometries:
                continue
            point = False
            points = 0
            lines = []
            for geometry in self.geometry[id]:
                geometry = QgsGeometry.fromWkt(geometry)
                if geometry.type() != QgsWkbTypes.LineGeometry:
                    points = points + 1
                    point = geometry.asPoint()
                else:
                    lines.append(geometry)
            if (3 < geometries) or (1 < points) or (0 == points):
                self.duplicate[id] = id
            for line in lines:
                if line.type() == QgsWkbTypes.LineGeometry:
                    connected = 0
                    # if the line is multipart, first part's first vertex and last part's last
                    collection = line.asGeometryCollection();
                    if 0 < len(collection):
                        first = False
                        last = False
                        for part in collection:
                            line = part.asPolyline()
                            if 1 < len(line):
                                if False == first:
                                    first = line[0]
                                last = line.pop()
                    if False != first:
                        snap_radius = first.sqrDist(last)/len(line)
                        if (0 < snap_radius) and (point != False): #Almerio: acrescentei ' and (point != False)'
                            for node in [first, last]:
                                if snap_radius > node.sqrDist(point):
                                    connected = connected + 1
                            if 1 != connected:
                                self.duplicate[id] = id
        for id in self.duplicate:
            self.log('Found duplicate '+GHydraulicsModel.ID_FIELD+' value: '+id)
        self.max = self.max + 1
        return self.duplicate

    # Loop over the id values in the given layer
    def checkNodeLayerIds(self, layer):
        provider = layer.dataProvider()
        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
        feature = QgsFeature()
        # loop over all features
        allAttrs = provider.attributeIndexes()
        iter = layer.getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            if len(attrs) > ididx:
                id = str(attrs[ididx])
                if id in self.unique:
                    self.duplicate[id] = id
                else:
                    self.unique[id] = id
                    if None != re.search('^[0-9]+$', id):
                        self.max = max(self.max, int(id))
            else:
                self.duplicate[''] = ''
                self.log('Found missing '+GHydraulicsModel.ID_FIELD)

    # Aggregate geometries by ID for the given layer
    def checkLinkLayerIds(self, layer):
        provider = layer.dataProvider()
        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
        feature = QgsFeature()
        # loop over all features
        allAttrs = provider.attributeIndexes()
        iter = layer.getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            if len(attrs) > ididx:
                id = str(attrs[ididx])
                if id not in self.geometry:
                    self.geometry[id] = []
                self.geometry[id].append(feature.geometry().asWkt())
                if None != re.search('^[0-9]+$', id):
                    self.max = max(self.max, int(id))

    # Check for all fields
    def checkFields(self):
        missing = {}
        # loop over all sections
        for section in EpanetModel.GIS_SECTIONS:
            #loop over all layers
            if section not in self.layers:
                continue
            for name in self.layers[section]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        provider = layer.dataProvider()
                        #loop over required fields
                        #Almerio: Added additional columns to table
                        allColumns = EpanetModel.COLUMNS[section]+EpanetModel.EXTRACOLUMNS[section]
                        for fieldname in allColumns:
                            if -1 == provider.fieldNameIndex(fieldname):
                                if name not in missing:
                                    missing[name] = []
                                missing[name].append(fieldname)
        return missing

    # Add fields
    def addFields(self, missing):
        success = True
        # loop over all layers with missing fields
        for name in list(missing.keys()):
            #loop over all layers
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    provider = layer.dataProvider()
                    if not layer.isEditable() and not layer.startEditing():
                        raise GHydraulicsException('ERROR: Unable to edit layer '+name)
                    attributes = []
                    #loop over required fields
                    for fieldname in missing[name]:
                        attributes.append(QgsField(fieldname, GHydraulicsModel.COLUMN_TYPES[fieldname]))
                    success = success and provider.addAttributes(attributes)
                    layer.updateFields()
        return success

    # return a list of modified layers that are part of the model
    def getModifiedLayers(self):
        modified = []
        # loop over all sections
        for section in EpanetModel.GIS_SECTIONS:
            if section not in self.layers:
                continue
            #loop over all layers
            for name in self.layers[section]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name and layer.isEditable():
                        modified.append(name)
        return modified

    # Make sure that no layer of the model has uncommmitted changes
    def commitChanges(self):
        for section in EpanetModel.GIS_SECTIONS:
            if section not in self.layers:
                continue
            #loop over all layers
            for name in self.layers[section]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name and layer.isModified():
                        if not layer.commitChanges():
                            raise GHydraulicsException('ERROR: Unable to commit layer '+name)

    # return the number of multipart pipes
    def getMultipartCount(self):
        multis = 0
        if EpanetModel.PIPES in self.layers:
            for name in self.layers[EpanetModel.PIPES]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        provider = layer.dataProvider()
                        feature = QgsFeature()
                        # loop over all features
                        allAttrs = provider.attributeIndexes()
                        iter = layer.getFeatures()
                        for feature in iter:
                            geometry = feature.geometry()
                            if geometry.type() == QgsWkbTypes.LineGeometry: 
                                #type()     -> Enum=[0=Point,1=Line,2=Polygon]
                                #wkbType()  -> Enum=[Point, LineString, Polygon, Triangle, MultiPoint, MultiLineString, etc...] 	
                                collection = geometry.asGeometryCollection();
                                if 1 < len(collection):
                                    multis = multis + 1
        return multis

    # Return the number of layers in the given section
    def getLayerCount(self, section):
        return len(self.layers[section]) if self.layers.get(section) else 0

    # Return a dictionary of coordinate reference systems used
    def getCrsDictionary(self):
        self.crss = {}
        self.eachLayer(self.getLayerCrs)
        return self.crss

    # For a given layer, return the coordinate reference system
    def getLayerCrs(self, layer):
        crs = layer.crs().authid()
        self.crss[crs] = crs

    def __init__(self):
        self.getLayers()
