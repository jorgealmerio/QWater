from __future__ import absolute_import
from builtins import str
from builtins import range
#
# This file is part of GHydraulics
#
# GHydraulictModelMaker.py - Create an EPANET model
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

from .EpanetModel import *
from .GHydraulicsCommon import *
from .GHydraulicsException import *
from .GHydraulicsModel import *
from .GHydraulicsModelChecker import *
from .GHydraulicsInpReader import *
from math import *
import re

# Create the node1 node2 topology
class GHydraulicsModelMaker(GHydraulicsCommon):
    # ID field in the spatial index data
    ID = 0
    PREFIX = 'G'

    # Fill node1, node2, return number of missing junctions
    def make(self):
        if not hasattr(self.checker, 'crss'):
            return 0
        self.buildNodeSpatialIndex()
        # temporary layer to cache missing junctions
        self.vjunctions = QgsVectorLayer("Point?crs="+list(self.checker.crss.keys())[0], "missing_junctions", "memory")
        self.vcount = 0
        provider = self.vjunctions.dataProvider()
        attributes = []
        #loop over required fields
        for fieldname in EpanetModel.COLUMNS[EpanetModel.JUNCTIONS]:
            attributes.append(QgsField(fieldname, GHydraulicsModel.COLUMN_TYPES[fieldname]))
        provider.addAttributes(attributes)
        self.vjunctions.updateFields()

        # loop over all pipe layers
        if EpanetModel.PIPES in self.layers:
            for name in self.layers[EpanetModel.PIPES]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        # Map node fields
                        nodes = {}
                        provider = layer.dataProvider()
                        feature = QgsFeature()
                        ididx = self.fieldNameIndex(layer, GHydraulicsModel.ID_FIELD)
                        for fieldname in EpanetModel.NODE_FIELDS:
                            nodeidx = provider.fieldNameIndex(fieldname)
                            if -1 == nodeidx:
                                raise GHydraulicsException('ERROR: Failed to locate '+fieldname+' field in layer '+name)
                            nodes[fieldname] = nodeidx
                        # loop over all features
                        allAttrs = provider.attributeIndexes()
                        iter = layer.getFeatures()
                        for feature in iter:
                            geometry = feature.geometry()
                            if geometry.type() == QgsWkbTypes.LineGeometry:
                                attrs = feature.attributes()
                                #if the line is multipart, first part's first vertex and last part's last
                                collection = geometry.asGeometryCollection();
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
                                    if 0 < snap_radius:
                                        points = {EpanetModel.NODE1: first, EpanetModel.NODE2: last}
                                        map = feature.attributes()
                                        for fieldname in EpanetModel.NODE_FIELDS:
                                            nodeidx = nodes[fieldname]
                                            nodeid = str(self.getNodeId(points[fieldname], snap_radius))
                                            if nodeid != str(map[nodeidx]):
                                                if not layer.isEditable() and not layer.startEditing():
                                                    raise GHydraulicsException('ERROR: Unable to edit layer '+name)
                                                layer.changeAttributeValue(feature.id(), nodeidx ,nodeid)
                                                self.log('Changing '+fieldname+' of pipe '+str(map[ididx])+' from '+str(map[nodeidx])+' to '+ nodeid)
        return self.vcount

    # Calculate the pipe length from GIS data
    def calculateLength(self):
        inp = GHydraulicsInpReader(self.templateFilename)
        inpunits = inp.getValue('OPTIONS', 'Units')
        mapunits = QgsUnitTypes.DistanceMeters
        if inpunits in EpanetModel.FEET_UNITS:
            mapunits = QgsUnitTypes.DistanceFeet
        # loop over all pipe layers
        if EpanetModel.PIPES in self.layers:
            for name in self.layers[EpanetModel.PIPES]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        # Map node fields
                        provider = layer.dataProvider()
                        feature = QgsFeature()
                        lengthidx = self.fieldNameIndex(layer, EpanetModel.LENGTH)
                        if -1 == lengthidx:
                            raise GHydraulicsException('ERROR: Failed to locate '+EpanetModel.LENGTH+' field in layer '+name)
                        reproject = (layer.crs().mapUnits() != mapunits)
                        reprojectgeographic = not layer.crs().isGeographic()
                        if reprojectgeographic:
                            epsg4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
                            reprojectgeographic = QgsCoordinateTransform(layer.crs(), epsg4326, QgsProject.instance())
                        utmsrs = False
                        # loop over all features
                        allAttrs = provider.attributeIndexes()
                        iter = layer.getFeatures()
                        for feature in iter:
                            geometry = feature.geometry()
                            if geometry.type() == QgsWkbTypes.LineGeometry:
                                attrs = feature.attributes()
                                l = 0
                                if reproject:
                                    collection = geometry.asGeometryCollection()
                                    if 0 < len(collection):
                                        for part in collection:
                                            line = part.asPolyline()
                                            if 0 < len(line):
                                            # Determine UTM zone
                                                if not utmsrs:
                                                    geographicpoint = line[0]
                                                    if reprojectgeographic:
                                                        geographicpoint = reprojectgeographic.transform(geographicpoint)
                                                    utmzone = int((geographicpoint.x()+180)/6)+1
                                                    proj4 = '+proj=utm +zone='+str(utmzone)+' +ellps=WGS84 +datum=WGS84 +units=m +no_defs +towgs84=0,0,0'
                                                    sn = 'N'
                                                    if 0 > geographicpoint.y():
                                                        proj4 = proj4 + ' +south'
                                                        sn = 'S'
                                                    self.log('Using UTM Zone '+str(utmzone)+sn+' for length calculation')
                                                    utmsrs = QgsCoordinateReferenceSystem()
                                                    utmsrs.createFromProj4(proj4)
                                                reproject = QgsCoordinateTransform(layer.crs(), utmsrs, QgsProject.instance())
                                                previous = False
                                                for point in line:
                                                    reprojected = reproject.transform(point)
                                                    if previous:
                                                        l = l + sqrt(reprojected.sqrDist(previous))
                                                    previous = reprojected
                                        if QgsUnitTypes.DistanceUnit.DistanceFeet == mapunits: #Almerio mudou o Original: QGis.Feet == mapunits:
                                            l = l * 3.2808399
                                else:
                                    l = geometry.length()
                                old = str(attrs[lengthidx])
                                precision = len(re.sub(r'[0-9]*[^0-9]', '', old))
                                l = round(l, precision)
                                if old != str(l):
                                    if not layer.isEditable() and not layer.startEditing():
                                        raise GHydraulicsException('ERROR: Unable to edit layer '+name)
                                    layer.changeAttributeValue(feature.id(), lengthidx, l)

    # In each model layer, replace the duplicate ids
    def enforceUniqueIds(self):
        self.eachLayer(self.enforceUniqueIdsInLayer)

    # Replace duplicate ids in the given layer
    def enforceUniqueIdsInLayer(self, layer):
        provider = layer.dataProvider()
        ididx = self.fieldNameIndex(layer, GHydraulicsModel.ID_FIELD)
        allAttrs = provider.attributeIndexes()
        feature = QgsFeature()
        duplicate = self.checker.duplicate
        iter = layer.getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            if not ididx < len(attrs) or str(attrs[ididx]) in duplicate:
                if not layer.isEditable() and not layer.startEditing():
                    raise GHydraulicsException('ERROR: Unable to edit layer '+layer.name())
                layer.changeAttributeValue(feature.id(), ididx, self.checker.max)
                self.log('Replaced '+GHydraulicsModel.ID_FIELD+' "'+str(attrs[ididx])+'" with '+str(self.checker.max))
                self.checker.max = self.checker.max + 1

    # delete generated data
    def cleanup(self):
        if hasattr(self, 'allnodes'):
            del self.allnodes
        if hasattr(self, 'nodemap'):
            del self.nodemap
        if hasattr(self, 'vjunctions'):
            del self.vjunctions
        if hasattr(self, 'vcount'):
            del self.vcount

    # Add to missing junctions layer, return ID
    def addJunction(self, point):
        feature = QgsFeature(self.nodeid)
        self.nodeid = self.nodeid + 1
        provider = self.vjunctions.dataProvider()
        feature.setGeometry(QgsGeometry.fromPointXY(point))#Almerio: updated 'fromPoint' to 'fromPointXY'
        self.vcount = self.vcount + 1
        id = self.PREFIX + str(self.vcount)
        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
        feature.initAttributes(1)
        feature.setAttribute(ididx, id)
        provider.addFeatures( [ feature ] )
        self.addFeatureToSpatialIndex(feature, ididx)
        return id

    # Get the node id for a certain point
    def getNodeId(self, point, snap_radius):
        id = self.allnodes.nearestNeighbor(point, 1)
        feature = self.nodemap[id.pop()]
        geometry = feature.geometry()
        nearest = self.getFirstMultiPoint(geometry)
        if nearest.sqrDist(point) >= snap_radius:
            # self.log('snap radius '+str(snap_radius)+' nearest: '+str(nearest.x())+' '+str(nearest.y()))
            return self.addJunction(point)
        attrs = feature.attributes()
        return str(attrs[self.ID])

    # Add the missing junctions to the first junction layer
    def addMissingJunctions(self):
        maplayers = QgsProject.instance().mapLayers()
        for layername in self.layers[EpanetModel.JUNCTIONS]:
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layername:
                    if not layer.isEditable() and not layer.startEditing():
                        raise GHydraulicsException('ERROR: Unable to edit layer '+layername)
                    provider = layer.dataProvider()
                    ididx = self.fieldNameIndex(layer, GHydraulicsModel.ID_FIELD)
                    vprovider = self.vjunctions.dataProvider()
                    vfeature = QgsFeature()
                    attidx = vprovider.attributeIndexes()
                    iter = self.vjunctions.getFeatures()
                    for vfeature in iter:
                        feature = QgsFeature()
                        geometry = QgsGeometry(vfeature.geometry())
                        #Almerio alterou o Original que era: if self.ismultipart[layername] and not geometry.convertToMultiType():
                        if geometry.isMultipart() and not geometry.convertToMultiType(): 
                            raise GHydraulicsException('ERROR: convertToMultiType() failed')
                        feature.setGeometry(geometry)
                        feature.initAttributes(1)
                        feature.setFields(layer.fields()) #Almerio added this line because of KeyError below
                        feature.setAttribute(ididx, str(self.checker.max)) #There was a KeyError HERE
                        if not provider.addFeatures([feature]):
                            raise GHydraulicsException('ERROR: Unable to add feature to layer '+layername)
                        self.log('Added junction '+str(self.checker.max)+' with feature id '+str(self.nodeid)+' ('+str(geometry.asPoint().x())+' ' +str(geometry.asPoint().y())+')')
                        self.checker.max = self.checker.max + 1
                    return

    # Get a QgsSpatialIndex object over all node layers and the given field list
    def buildNodeSpatialIndex(self):
        self.allnodes = QgsSpatialIndex()
        self.nodemap = {}
        self.nodeid = 0
        self.ismultipart = {}
        maplayers = QgsProject.instance().mapLayers() #Almerio: Eu tirei os parenteses de QgsProject
        for name in GHydraulicsModel.NODE_SECTIONS:
            if name not in self.layers:
                continue
            for layername in self.layers[name]:
                # self.log('Processing '+layername)
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layername:
                        provider = layer.dataProvider()
                        feature = QgsFeature()
                        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
                        iter = layer.getFeatures()
                        hasfeatures = False
                        for feature in iter:
                            self.addFeatureToSpatialIndex(feature, ididx)
                            hasfeatures = True
                        if hasfeatures:
                            self.ismultipart[layername] = feature.geometry().isMultipart()


    #todo simplify id handling
    def addFeatureToSpatialIndex(self, feature, ididx):
        geometry = feature.geometry()
        if geometry.type() == QgsWkbTypes.PointGeometry:
            self.nodeid = max(self.nodeid, feature.id()) + 1
            point = QgsFeature(self.nodeid)
            point.setGeometry(geometry)
            attrs = feature.attributes()
            point.setAttributes([str(attrs[ididx])])
            self.allnodes.insertFeature(point)
            self.nodemap[point.id()] = point
            # self.log('Added to spatial index: '+str(attrs[ididx])+' '+str(geometry.asPoint().x())+' '+str(geometry.asPoint().y()))

    # explode all multipart pipes
    def explodeMultipartPipes(self):
        if EpanetModel.PIPES not in self.layers:
            return
        for name in self.layers[EpanetModel.PIPES]:
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    if not layer.isEditable() and not layer.startEditing():
                        raise GHydraulicsException('ERROR: Unable to edit layer '+layername)
                    provider = layer.dataProvider()
                    feature = QgsFeature()
                    # loop over all features
                    allAttrs = provider.attributeIndexes()
                    ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
                    iter = layer.getFeatures()
                    for feature in iter:
                        geometry = feature.geometry()
                        if geometry.type() == QgsWkbTypes.LineGeometry:
                            collection = geometry.asGeometryCollection();
                            parts = len(collection)
                            if 1 < parts:
                                map = feature.attributes()
                                collection[0].convertToMultiType()
                                if not layer.changeGeometry(feature.id(), collection[0]):
                                    raise GHydraulicsException('ERROR: Unable to change geometry on layer '+layername)
                                self.log('Changed geometry of pipe ' + str(map[ididx]) + ' to single part')
                                for i in range(1, parts):
                                    pfeature = QgsFeature()
                                    collection[i].convertToMultiType()
                                    feature.setGeometry(collection[i])
                                    map[ididx] = self.checker.max
                                    for id in map:
                                        feature.setAttribute(id, map[i])
                                    if not provider.addFeatures([feature]):
                                        raise GHydraulicsException('ERROR: Unable to add feature to layer '+layername)
                                    self.log('Added pipe '+str(self.checker.max))
                                    self.checker.max = self.checker.max + 1


    def __init__(self, templateFilename):
        self.templateFilename = templateFilename
        self.getLayers()
        self.checker = GHydraulicsModelChecker()
