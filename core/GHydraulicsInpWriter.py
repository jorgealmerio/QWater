from __future__ import absolute_import
from builtins import str
from builtins import range
#
# This file is part of GHydraulics
#
# GHydraulicsInpWriter.py - Write INP files
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
#

import math
import re
import numpy
import numpy.linalg
import os
from pickle import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis import *
from .EpanetModel import *
from .GHydraulicsCommon import *
from .GHydraulicsException import *
from .GHydraulicsModel import *

# Write EPANET INP file
class GHydraulicsInpWriter(GHydraulicsCommon):
    TITLE = 'Save EPANET INP file'
    SETTINGS='QWater'
    '''
    def tr(self, message):
        return QCoreApplication.translate('QWater',message)
    '''
    # Write to the given filename
    def write(self, filename, backdrop, silent=False):
        self.filename = filename
        self.backdrop = backdrop
        template = open(self.templateFilename)
        self.inpfile = open(filename, 'w')
        section = None
        for line in template.readlines():
            sectionname = re.match(' *\[([A-Z]+)\].*', line)
            if None != sectionname:
                section = self.writeSection(sectionname.group(1))
            if None == section:
                self.inpfile.write(line)
        self.inpfile.close()
        template.close()
        if silent==False:
            self.iface.messageBar().pushMessage(self.SETTINGS, filename+QCoreApplication.translate('QWater',' successfully created!'), level=Qgis.Info, duration=4)

    # Write the given section to the INP file
    def writeSection(self, section):
        if section in self.sections and 0 < len(self.sections[section]):
            self.writeSectionLabel(section)
            if section in self.sections:
                self.inpfile.write(self.sections[section])
                return section
        elif 'BACKDROP' == section and self.backdrop:
            self.writeBackdropSection()
            return section
        elif 'CURVES' == section:
            self.writeCurvesSection()
            return section
        return None

    #prevent NULL values in INP file
    def getString(self, value):
        v = str(value)
        if 'NULL' == v:
            return ''
        return v

    # Setup coordinate transformation where necessary
    def setLayerCrs(self, crs):
        self.crstransform = False
        canvascrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        if crs.isValid() and canvascrs.isValid():
            self.crstransform = QgsCoordinateTransform(crs, canvascrs, QgsProject.instance())
        if self.crstransform.isShortCircuited():
            self.crstransform = False

    # Transform coordinates where necessary from layer to canvas crs
    def transformXY(self, x, y):
        if self.crstransform:
            pnt = self.crstransform.transform(QgsPointXY(x,y))
            x = pnt.x()
            y = pnt.y()
        return [x,y]

    # Extract nodes from the model and write to string
    def getNodes(self, section):
        nodes = ''
        if section in self.sections:
            nodes = self.sections[section]
        if section not in self.layers:
            return
        for name in self.layers[section]:
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    feature = QgsFeature()
                    provider = layer.dataProvider()
                    allAttrs = provider.attributeIndexes()
                    fieldIndices = []
                    self.setLayerCrs(layer.crs())
                    for field in EpanetModel.COLUMNS[section]:
                        fieldidx = provider.fieldNameIndex(field)
                        if -1 == fieldidx:
                            raise GHydraulicsException('ERROR: Failed to locate '+field+' field in layer '+name)
                        fieldIndices.append(fieldidx)
                    iter = layer.getFeatures()
                    # Loop over all features
                    for feature in iter:
                        geometry = feature.geometry()
                        if geometry.type() == QgsWkbTypes.PointGeometry:
                            attrs = feature.attributes()
                            # write node
                            id = ''
                            for fieldidx in fieldIndices:
                                attribute = self.getString(attrs[fieldidx])
                                nodes = nodes + attribute + ' '
                                if '' == id:
                                    id = attribute
                            nodes = nodes + '\n'
                            # write coordinate
                            point = self.getFirstMultiPoint(geometry)
                            (x,y) = self.transformXY(point.x(), point.y())
                            p = str(x) + ' ' + str(y)
                            self.sections['COORDINATES'] = self.sections['COORDINATES'] + id + ' ' + p + '\n'
                            self.xcoords.append(float(x))
                            self.ycoords.append(float(y))
        self.sections[section] = nodes + '\n'

    # Extract pipes from model, write to INP format string
    def getPipes(self):
        if EpanetModel.PIPES not in self.layers:
            return
        if EpanetModel.PIPES in self.sections:
            pipes = self.sections[EpanetModel.PIPES]
        for name in self.layers[EpanetModel.PIPES]:
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    feature = QgsFeature()
                    provider = layer.dataProvider()
                    allAttrs = provider.attributeIndexes()
                    fieldIndices = []
                    node1idx = -1
                    self.setLayerCrs(layer.crs())
                    for field in EpanetModel.COLUMNS[EpanetModel.PIPES]:
                        fieldidx = provider.fieldNameIndex(field)
                        if -1 == fieldidx:
                            raise GHydraulicsException('ERROR: Failed to locate '+field+' field in layer '+name)
                        fieldIndices.append(fieldidx)
                        if EpanetModel.NODE1 == field:
                            node1idx = fieldidx
                    iter = layer.getFeatures()
                    # Loop over all features
                    for feature in iter:
                        geometry = feature.geometry()
                        if geometry.type() == QgsWkbTypes.LineGeometry:
                            attrs = feature.attributes()
                            # write node
                            id = ''
                            skip = False
                            for fieldidx in fieldIndices:
                                attribute = str(attrs[fieldidx])
                                if '' == id:
                                    id = attribute
                                    if id in self.skippipes:
                                        skip = True
                                        break
                                # Use dynamic nodes where necessary
                                if fieldidx == node1idx and attribute in self.virtualnodes:
                                    attribute = self.virtualnodes[attribute]
                                pipes = pipes + attribute + ' '
                            if skip:
                                continue
                            pipes = pipes + '\n'
                            # vertices
                            if geometry.isMultipart(): #.wkbType()==QgsWkbTypes.MultiLineString: #geometry.isMultipart(): #Almerio: Adicionei esse "if" para resolver MultiLineStrings
                                line = geometry.asMultiPolyline()[0] #if is multipart get only first polyline
                            else:
                                line = geometry.asPolyline()
                            for p in range(1,len(line)-1):
                                (x,y) = self.transformXY(line[p].x(), line[p].y())
                                self.xcoords.append(float(x))
                                self.ycoords.append(float(y))
                                self.sections['VERTICES'] = self.sections['VERTICES'] + id + ' ' + self.getString(x) + ' ' + self.getString(y) + '\n'
        self.sections['PIPES'] = pipes + '\n'

    # Generate a dictionary of node1, node2 values linking to pipe ids
    def fillTopology(self, layer):
        provider = layer.dataProvider()
        allAttrs = provider.attributeIndexes()
        indexes = {}
        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
        for field in EpanetModel.NODE_FIELDS:
            indexes[field] = provider.fieldNameIndex(field)
            if -1 == indexes[field]:
                raise GHydraulicsException('ERROR: Failed to locate '+field+' field in layer '+layer.name())
        iter = layer.getFeatures()
        for feature in iter:
            attrs = feature.attributes()
            id = str(attrs[ididx])
            node1 = str(attrs[indexes[EpanetModel.NODE1]])
            node2 = str(attrs[indexes[EpanetModel.NODE2]])
            if node1 not in self.pipes[EpanetModel.NODE1]:
                self.pipes[EpanetModel.NODE1][node1] = {}
            self.pipes[EpanetModel.NODE1][node1][id] = node2
            if node2 not in self.pipes[EpanetModel.NODE2]:
                self.pipes[EpanetModel.NODE2][node2] = {}
            self.pipes[EpanetModel.NODE2][node2][id] = node1


    # Virtual lines are lines in EPANET and nodes in QGIS
    # There are 3 options:
    # a) virtual line and connected pipes have individual ids (DC Water Design style), new link will be created
    # b) virtual line shares id with one connected pipe, this pipe will become the EPANET link
    # c) virtual line shares id with both connected pipes (inp2shp style), pipes will become EPANET link
    def getVirtualLines(self, section):
        lines = ''
        if section not in self.layers:
            return
        for name in self.layers[section]:
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    # Examine type field for SOV handling
                    typeidx = -1
                    diameteridx = -1
                    minorlossidx = -1
                    settingidx = -1
                    feature = QgsFeature()
                    provider = layer.dataProvider()
                    allAttrs = provider.attributeIndexes()
                    fieldIndices = []
                    self.setLayerCrs(layer.crs())
                    for field in EpanetModel.COLUMNS[section]:
                        fieldidx = provider.fieldNameIndex(field)
                        if -1 == fieldidx:
                            raise GHydraulicsException('ERROR: Failed to locate '+field+' field in layer '+name)
                        if EpanetModel.VALVES == section:
                            if EpanetModel.TYPE == field:
                                typeidx = fieldidx
                            if EpanetModel.DIAMETER == field:
                                diameteridx = fieldidx
                            if EpanetModel.MINORLOSS == field:
                                minorlossidx = fieldidx
                            if EpanetModel.SETTING == field:
                                settingidx = fieldidx
                            if field.lower() != 'ELEVATION'.lower(): #ignore elevation field for valves
                                fieldIndices.append(fieldidx)
                        else:
                            fieldIndices.append(fieldidx)
                    if EpanetModel.VALVES == section and (-1 == typeidx or -1 == diameteridx or -1 == minorlossidx or -1 == settingidx):
                        raise GHydraulicsException('ERROR: Failed to locate type, diameter, minorloss or status in layer '+name)
                    iter = layer.getFeatures()
                    elevationidx = provider.fieldNameIndex('ELEVATION')
                    # Loop over all features
                    for feature in iter:
                        geometry = feature.geometry()
                        if geometry.type() == QgsWkbTypes.PointGeometry:
                            attrs = feature.attributes()
                            # write node
                            id = ''
                            virtual_id = ''
                            sov = False
                            if -1 != typeidx and str(attrs[typeidx]) == 'SOV':
                                # Handle shut off valves
                                sov = True
                            # Leave out the elevation
                            writenode1 = True
                            writenode2 = True
                            for i in range(len(fieldIndices)): #range(1,len(fieldIndices))
                                if fieldIndices[i] != elevationidx: #Almerio: leave out the elevation
                                    attribute = str(attrs[fieldIndices[i]])
                                    if not sov:
                                        lines = lines + attribute + ' '
                                    if '' == id:
                                        id = attribute
                                        if id in self.pipes[EpanetModel.NODE1] and id in self.pipes[EpanetModel.NODE1][id]:
                                            writenode2 = False
                                            virtual_id = self.pipes[EpanetModel.NODE1][id][id]
                                            self.skippipes[id] = id
                                        if id in self.pipes[EpanetModel.NODE2] and id in self.pipes[EpanetModel.NODE2][id]:
                                            writenode1 = False
                                            id = self.pipes[EpanetModel.NODE2][id][id]
                                            self.skippipes[id] = id
                                        if writenode2:
                                            virtual_id = id + GHydraulicsModel.VIRTUAL_POSTFIX
                                            self.virtualnodes[id] = virtual_id
                                        if not sov:
                                            lines = lines + id + ' ' + virtual_id + ' '
                            if not sov:
                                lines = lines + '\n'
                            # write first point
                            if writenode1:
                                point = self.getFirstMultiPoint(geometry)
                                elevation = str(attrs[elevationidx]) or 0 #Almerio fieldIndices[0]
                                self.addJunction(id, elevation, '0', '', point.x(), point.y())
                            # write the second point
                            # todo calculate length for all cases
                            length = 1
                            if writenode2:
                                length = self.getSecondVirtualLineJunction(id, elevation)
                            if sov:
                                pipes = self.sections[EpanetModel.PIPES]
                                    #;ID                Node1                   Node2                   Length          Diameter        Roughness       MinorLoss       Status
                                pipes = pipes + id + ' ' + id + ' ' + virtual_id + ' ' + self.getString(length) + ' ' + self.getString(attrs[diameteridx]) + ' 1 ' + self.getString(attrs[minorlossidx]) + ' '+self.getString(attrs[settingidx]) + '\n'
                                self.sections[EpanetModel.PIPES] = pipes

        self.sections[section] = lines + '\n'

    # Insert virtual node into line (DC Water Design style)
    def getSecondVirtualLineJunction(self, id, elevation):
        node = ''
        virtual_id = self.virtualnodes[id]
        # Find the referenced pipe
        for name in self.layers[EpanetModel.PIPES]:
            maplayers = QgsProject.instance().mapLayers()
            for l,layer in maplayers.items():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                    feature = QgsFeature()
                    provider = layer.dataProvider()
                    allAttrs = provider.attributeIndexes()
                    node1idx = provider.fieldNameIndex(EpanetModel.NODE1)
                    self.setLayerCrs(layer.crs())
                    if -1 == node1idx:
                        raise GHydraulicsException('ERROR: Failed to locate '+EpanetModel.NODE1+' field in layer '+name)
                    iter = layer.getFeatures()
                    # Loop over all features
                    for feature in iter:
                        geometry = feature.geometry()
                        if geometry.type() == QgsWkbTypes.LineGeometry:
                            attrs = feature.attributes()
                            node1 = self.getString(attrs[node1idx])
                            if  node1 == id or node1 == virtual_id:
                                if geometry.isMultipart(): #geometry.isMultipart(): #Almerio: Adicionei esse "if" para resolver MultiLineStrings #estava: geometry.wkbType()==QgsWkbTypes.MultiLineString
                                    g=geometry.asMultiPolyline()
                                    s=g[0][0]
                                    e=g[-1][-1]
                                else:
                                    line = geometry.asPolyline()
                                    s = line[0]
                                    e = line[1]
                                if GHydraulicsModel.VIRTUAL_LINE_LENGTH > s.sqrDist(e):
                                    p = [(s.x()+e.x())/2,(s.y()+e.y())/2]
                                else:
                                    sv = numpy.array([s.x(), s.y()])
                                    ev = numpy.array([e.x(), e.y()])
                                    dv = ev - sv
                                    nv = dv/numpy.linalg.norm(dv)
                                    p = sv + nv
                                self.addJunction(virtual_id, elevation, '0', '', p[0], p[1])
                                return math.sqrt(math.pow(p[0]-s[0], 2) + math.pow(p[1]-s[1], 2))
        raise GHydraulicsException('ERROR: Failed to locate Pipe with NODE1 named '+id)

    # Add a junction to the buffer
    def addJunction(self, id, elevation, demand, pattern, x, y):
        (x,y) = self.transformXY(x, y)
        self.sections[EpanetModel.JUNCTIONS] = self.sections[EpanetModel.JUNCTIONS] + id + ' ' + elevation+ ' ' + demand + ' ' + pattern + '\n'
        self.addXY(EpanetModel.COORDINATES, id, x, y)

    # section is one of COORDINATES or VERTICES
    def addXY(self, section, id, x, y):
        self.sections[section] = self.sections[section] + id + ' ' + self.getString(x) + ' ' + self.getString(y) + '\n'

    # Write a section label to the INP file
    def writeSectionLabel(self, section):
        self.inpfile.write('['+section+'] ; created by QWater\n')

    # Write out the backdrop section
    def writeBackdropSection(self):
        self.writeSectionLabel('BACKDROP')
        backdropfile = self.getBackdropFromInp(str(self.filename))
        canvas = self.iface.mapCanvas()
        canvas.saveAsImage(backdropfile, None, 'BMP')
        # Use current view extent, if there are no network elements
        extent = canvas.extent()
        mins = str(extent.xMinimum()) + ' ' + str(extent.yMinimum())
        maxs = str(extent.xMaximum()) + ' ' + str(extent.yMaximum())
        self.inpfile.write('DIMENSIONS ' + mins + ' ' + maxs + '\n')
        units = 'None'
        mapunits = canvas.mapUnits()
        if not canvas.mapRenderer().destinationCrs().isValid():
            for section in EpanetModel.GIS_SECTIONS:
                if section in self.layers:
                    for name in self.layers[EpanetModel.PIPES]:
                        maplayers = QgsProject.instance().mapLayers()
                        for l,layer in maplayers.items():
                            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                                mapunits = layer.crs().mapUnits()
        if mapunits in GHydraulicsModel.UNITMAP:
            units = GHydraulicsModel.UNITMAP[mapunits]
        self.inpfile.write('UNITS '+units+'\n')
        self.inpfile.write('FILE "' + os.path.basename(backdropfile) + '"\n')
        self.inpfile.write('OFFSET 0.00 0.00\n\n')

    # Canonical backdrop name from inp file
    def getBackdropFromInp(self, inpfilename):
        return os.path.splitext(inpfilename)[0]+'.bmp'
    
    # Write out the Curves section
    def writeCurvesSection(self):
        self.writeSectionLabel('CURVES')
        curvesDict = self.curvesDict
        type_names = {0: 'VOLUME',
                  1: 'PUMP',
                  2: 'EFFICIENCY',
                  3: 'HEADLOSS'}
        
        #write section header
        self.inpfile.write(';ID              	X-Value     	Y-Value\n')
        if curvesDict: #19/01/2024: To avoid create null curves
            for curvaID in curvesDict:
                curvaArray = curvesDict[curvaID]                    
                i=0                    
                for linha in curvaArray:
                    if i==0: #First line has description and curve type                    
                        curve_desc = linha[0]
                        curve_type = linha[1]
                        curve_type_name = type_names[curve_type]
                        #write curve description
                        self.inpfile.write(';{}: {}\n'.format(curve_type_name, curve_desc))
                        i+=1
                    else:
                        x = linha[1]
                        y = linha[2]
                        #write curve description
                        self.inpfile.write(' {}\t{}\t{}\n'.format(curvaID, x, y))
        
    def Project_Curves_to_Dict(self):
        proj = QgsProject.instance()
        curvesStr = proj.readEntry(self.SETTINGS, "CURVES","0")[0]
        curves_d = {}
        resp = False
        if curvesStr:
            curvesDict = eval(curvesStr)
            if curvesDict:                               
                resp = curvesDict
        return resp

    def __init__(self, templateFilename, iface):
        self.templateFilename = templateFilename
        self.iface = iface
        # Calculate map extent
        self.xcoords = []
        self.ycoords = []
        self.getLayers()
        self.sections = {EpanetModel.JUNCTIONS: '', EpanetModel.PIPES: ''}
        
        #if Epanet Curves (for while only Pumps curves) is defined in current Qgis Project 
        self.curvesDict = self.Project_Curves_to_Dict()
        if self.curvesDict:
            self.sections['CURVES'] = ''
        # Dictionary of those node1 values that change because of virtual lines
        self.virtualnodes = {}
        # Dictionary of those pipes that are merged into virtual lines
        self.skippipes = {}
        # Dictionary to look up pipe ids
        self.pipes = {EpanetModel.NODE1: {}, EpanetModel.NODE2: {}}
        # Transform coordinates, where necessary
        self.crstransform = False
        for section in EpanetModel.COORDINATE_DATA_SECTIONS:
            self.sections[section] = ''
        self.eachLayer(self.fillTopology, [EpanetModel.PIPES])
        for section in EpanetModel.VIRTUAL_LINE_SECTIONS:
            self.getVirtualLines(section)
        for section in EpanetModel.COORDINATE_SECTIONS:
            self.getNodes(section)
        self.getPipes()
