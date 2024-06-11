# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Profile
# Copyright (C) 2008  Borys Jurgiel
# Copyright (C) 2012  Patrice Verchere
# -----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, print to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ---------------------------------------------------------------------
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
"""
import qgis
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from .selectlinetool import SelectLineTool


class ProfiletoolMapToolRenderer:
    def __init__(self, profiletool):
        self.profiletool = profiletool
        self.iface = self.profiletool.iface
        self.canvas = self.profiletool.iface.mapCanvas()
        self.tool = ProfiletoolMapTool(self.canvas, self.profiletool.plugincore.action)  # the mouselistener
        self.pointstoDraw = []  # Polyline being drawn in freehand mode
        self.dblclktemp = None  # enable disctinction between leftclick and doubleclick
        # the rubberband
        self.polygon = QgsWkbTypes.GeometryType.Polygon #estava False
        self.rubberband = QgsRubberBand(self.iface.mapCanvas(), self.polygon)
        self.rubberband.setWidth(2)
        self.rubberband.setColor(QColor(Qt.red))

        self.rubberbandpoint = QgsVertexMarker(self.iface.mapCanvas())
        self.rubberbandpoint.setColor(QColor(Qt.red))
        self.rubberbandpoint.setIconSize(5)
        self.rubberbandpoint.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
        self.rubberbandpoint.setPenWidth(3)

        self.rubberbandbuf = QgsRubberBand(self.iface.mapCanvas())
        self.rubberbandbuf.setWidth(1)
        self.rubberbandbuf.setColor(QColor(Qt.blue))

        self.textquit0 = "Click for polyline and double click to end (right click to cancel then quit)"
        self.textquit1 = "Select the polyline feature in a vector layer (Right click to quit)"
        self.textquit2 = "Select the polyline vector layer (Right click to quit)"

        self.setSelectionMethod(0)

    def resetRubberBand(self):
        # TODO: use version check for qgis3 too.
        try:  # qgis2
            if QGis.QGIS_VERSION_INT >= 10900:
                self.rubberband.reset(QGis.Line)
            else:
                self.rubberband.reset(self.polygon)
        except:  # qgis3
            self.rubberband.reset(qgis.core.QgsWkbTypes.LineGeometry)

    # ************************************* Mouse listener actions ***********************************************

    def moved(self, position):  # draw the polyline on the temp layer (rubberband)
        if self.selectionmethod == 0:
            if len(self.pointstoDraw) > 0:
                # Get mouse coords
                mapPos = self.canvas.getCoordinateTransform().toMapCoordinates(position["x"], position["y"])
                # Draw on temp layer
                self.resetRubberBand()
                for i in range(0, len(self.pointstoDraw)):
                    self.rubberband.addPoint(QgsPointXY(self.pointstoDraw[i][0], self.pointstoDraw[i][1]))
                self.rubberband.addPoint(QgsPointXY(mapPos.x(), mapPos.y()))
        if self.selectionmethod in (1, 2):
            return

    def rightClicked(self, position):  # used to quit the current action
        self.profiletool.clearProfil()
        self.cleaning()

    def leftClicked(self, position):  # Add point to analyse
        mapPos = self.canvas.getCoordinateTransform().toMapCoordinates(position["x"], position["y"])
        newPoints = [[mapPos.x(), mapPos.y()]]
        if self.profiletool.doTracking:
            self.rubberbandpoint.hide()

        if self.selectionmethod == 0:
            if newPoints == self.dblclktemp:
                self.dblclktemp = None
                return
            else:
                if len(self.pointstoDraw) == 0:
                    self.resetRubberBand()
                    self.rubberbandbuf.reset()
                self.pointstoDraw += newPoints
                self.profiletool.updateProfil(self.pointstoDraw)
        if self.selectionmethod in (1, 2):
            if self.selectionmethod == 1:
                method = "feature"
                message = self.textquit1
            else:
                method = "layer"
                message = self.textquit2
            result = SelectLineTool(selectionMethod=method).getPointTableFromSelectedLine(
                self.iface, self.tool, newPoints
            )
            self.profiletool.updateProfilFromFeatures(result[0], result[1])

            self.iface.mainWindow().statusBar().showMessage(message)

    def doubleClicked(self, position):
        if self.selectionmethod == 0:
            # Validation of line
            mapPos = self.canvas.getCoordinateTransform().toMapCoordinates(position["x"], position["y"])
            newPoints = [[mapPos.x(), mapPos.y()]]
            self.pointstoDraw += newPoints
            # launch analyses
            self.iface.mainWindow().statusBar().showMessage(str(self.pointstoDraw))
            self.profiletool.updateProfil(self.pointstoDraw)
            # Reset
            self.pointstoDraw = []
            # temp point to distinct leftclick and dbleclick
            self.dblclktemp = newPoints
            self.iface.mainWindow().statusBar().showMessage(self.textquit0)
        if self.selectionmethod in (1, 2):
            return
    
    # QWaterProfile by junctions
    def QWprofileByJunctions(self, ptos2Draw):
        # Reset
        self.pointstoDraw = []
        self.pointstoDraw = ptos2Draw
        self.resetRubberBand()
        for i in range(0, len(self.pointstoDraw)):
            self.rubberband.addPoint(QgsPointXY(self.pointstoDraw[i][0], self.pointstoDraw[i][1]))            
        self.profiletool.updateProfil(self.pointstoDraw)        
        
    def currentLayerChanged(self, layer):
        if self.selectionmethod == 2:
            if SelectLineTool.checkIsLineLayer(layer) or SelectLineTool.checkIsPointLayer(layer):
                self.profiletool.updateProfilFromFeatures(
                    layer, SelectLineTool.select_layer_features(None, layer, None)
                )
            else:
                self.profiletool.clearProfil()

    def setSelectionMethod(self, method):
        self.cleaning()
        self.selectionmethod = method
        if method == 0:
            self.tool.setCursor(Qt.CrossCursor)
            self.iface.mainWindow().statusBar().showMessage(self.textquit0)
        elif method == 1:
            self.tool.setCursor(Qt.PointingHandCursor)
            self.iface.mainWindow().statusBar().showMessage(self.textquit1)
        elif method == 2:
            self.tool.setCursor(Qt.PointingHandCursor)
            self.iface.mainWindow().statusBar().showMessage(self.textquit2)
        #elif method == 3:
        #    self.iface.messageBar().pushMessage('QWater','By Path')
        self.currentLayerChanged(self.iface.activeLayer())

    def setBufferGeometry(self, geoms):
        self.rubberbandbuf.reset()
        for g in geoms:
            self.rubberbandbuf.addGeometry(g, None)

    def cleaning(self):  # used on right click
        self.pointstoDraw = []
        self.rubberbandpoint.hide()
        self.resetRubberBand()
        self.rubberbandbuf.reset()
        self.iface.mainWindow().statusBar().showMessage("")

    def connectTool(self):
        self.tool.moved.connect(self.moved)
        self.tool.rightClicked.connect(self.rightClicked)
        self.tool.leftClicked.connect(self.leftClicked)
        self.tool.doubleClicked.connect(self.doubleClicked)
        self.tool.desactivate.connect(self.deactivate)
        self.iface.currentLayerChanged.connect(self.currentLayerChanged)

    def deactivate(self):  # enable clean exit of the plugin
        self.cleaning()
        self.tool.moved.disconnect(self.moved)
        self.tool.rightClicked.disconnect(self.rightClicked)
        self.tool.leftClicked.disconnect(self.leftClicked)
        self.tool.doubleClicked.disconnect(self.doubleClicked)
        self.tool.desactivate.disconnect(self.deactivate)
        self.iface.currentLayerChanged.disconnect(self.currentLayerChanged)
        self.canvas.unsetMapTool(self.tool)
        self.canvas.setMapTool(self.profiletool.saveTool)


class ProfiletoolMapTool(QgsMapTool):

    moved = pyqtSignal(dict)
    rightClicked = pyqtSignal(dict)
    leftClicked = pyqtSignal(dict)
    doubleClicked = pyqtSignal(dict)
    desactivate = pyqtSignal()

    def __init__(self, canvas, button):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
        self.button = button

    def canvasMoveEvent(self, event):
        self.moved.emit({"x": event.pos().x(), "y": event.pos().y()})

    def canvasReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightClicked.emit({"x": event.pos().x(), "y": event.pos().y()})
        else:
            self.leftClicked.emit({"x": event.pos().x(), "y": event.pos().y()})

    def canvasDoubleClickEvent(self, event):
        self.doubleClicked.emit({"x": event.pos().x(), "y": event.pos().y()})

    def activate(self):
        QgsMapTool.activate(self)
        self.canvas.setCursor(self.cursor)
        self.button.setCheckable(True)
        self.button.setChecked(True)

    def deactivate(self):
        self.desactivate.emit()
        self.button.setCheckable(False)
        QgsMapTool.deactivate(self)

    def isZoomTool(self):
        return False

    def setCursor(self, cursor):
        self.cursor = QCursor(cursor)
