# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
# Profile
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

import os
import platform
import processing

from qgis.PyQt import QtCore, QtGui, uic
from ..tools.utils import isProfilable

try:
    from qgis.PyQt.QtGui import QDockWidget
except:
    from qgis.PyQt.QtWidgets import QDockWidget

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import *
from qgis.gui import *

# plugin import
from ..tools.plottingtool import *
from ..tools.tableviewtool import TableViewTool
from ....QWater_00Common import *
#from ..tools.QW_identifyfeaturetool import QW_IdentifyFeatureTool

try:
    from PyQt4.Qwt5 import *
    Qwt5_loaded = True
except ImportError:
    Qwt5_loaded = False

try:
    import matplotlib
    from matplotlib import *
    matplotlib_loaded = True
except ImportError:
    matplotlib_loaded = False


uiFilePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "profiletool.ui"))
FormClass = uic.loadUiType(uiFilePath)[0]


class PTDockWidget(QDockWidget, FormClass):

    TITLE = "ProfileTool"
    TYPE = None

    closed = QtCore.pyqtSignal()

    def __init__(self, iface1, profiletoolcore, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.profiletoolcore = profiletoolcore
        self.iface = iface1
        # Apperance
        self.location = QtCore.Qt.BottomDockWidgetArea
        minsize = self.minimumSize()
        maxsize = self.maximumSize()
        self.setMinimumSize(minsize)
        self.setMaximumSize(maxsize)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # init scale widgets
        self.sbMaxVal.setValue(0)
        self.sbMinVal.setValue(0)
        self.sbMaxVal.setEnabled(False)
        self.sbMinVal.setEnabled(False)
        self.plotComboBox.setEnabled(False) # Disable height/slope selection option
        self.connectYSpinbox()

        # model
        self.mdl = QStandardItemModel(0, 6)  # the model whitch in are saved layers analysed caracteristics
        self.tableView.setModel(self.mdl)
        self.tableView.setColumnWidth(0, 20)
        self.tableView.setColumnWidth(1, 20)
        # self.tableView.setColumnWidth(2, 150)
        hh = self.tableView.horizontalHeader()
        hh.setStretchLastSection(True)
        self.tableView.setColumnHidden(5, True)
        self.mdl.setHorizontalHeaderLabels(["", "", "Layer", "Band/Field", "Search buffer"])
        self.tableViewTool = TableViewTool()

        # other
        self.addOptionComboboxItems()
        self.selectionmethod = 0
        self.plotlibrary = None  # The plotting library to use
        self.showcursor = True
        self.grpByJunctions.setVisible(False)
        
        #QWaterProfile
        self.common=QWater_00Common()
        self.junctionLayer = None
        
        #debug purpose
        #myText = '91\n128\n129\n130\n131\n132\n133\n134\n135'
        #self.txtJunctions.setPlainText(myText)

        # Signals
        self.butSaveAs.clicked.connect(self.saveAs)
        self.tableView.clicked.connect(self._onClick)
        self.mdl.itemChanged.connect(self._onChange)
        self.pushButton_2.clicked.connect(self.addLayer)
        self.pushButton.clicked.connect(self.removeLayer)
        self.comboBox.currentIndexChanged.connect(self.selectionMethod)
        self.cboLibrary.currentIndexChanged.connect(self.changePlotLibrary)
        self.tableViewTool.layerAddedOrRemoved.connect(self.refreshPlot)
        self.pushButton_reinitview.clicked.connect(self.reScalePlot)
        self.checkBox_showcursor.stateChanged.connect(self.showCursor)
        self.fullResolutionCheckBox.stateChanged.connect(self.refreshPlot)
        self.profileInterpolationCheckBox.stateChanged.connect(self.refreshPlot)

        self.cbSameAxisScale.stateChanged.connect(self._onSameAxisScaleStateChanged)
        #QWater
        self.btnPlotPath.clicked.connect(self.QW_plotpath_clicked)
        #self.btnFindPath.clicked.connect(self.QW_find_Path)
        self.btnFrom.clicked.connect(self.QW_btnFrom_clicked)
        self.btnTo.clicked.connect(self.QW_btnTo_clicked)
        self.btnTest.clicked.connect(self.QW_removeQWaterLayers)

    #********************************************************************************
    #QWater things ****************************************************************
    #********************************************************************************
    
    #not used, has bug
    def QW_willBeDeleted(self, layer=None):
        if layer:
            print('QW_willBeDeleted!'+layer.name())
        else:
            print('layer falso')
        #for campo in ['RESULT_HEA','ELEVATION']:
        #    linha = self.QW_findRow(campo)
        #    self.removeLayer(linha)
        
        #self.profiletoolcore.toolrenderer.deactivate()
        #model1 = self.mdl
        #model1.setRowCount(0)
        #for i in range(0, model1.rowCount()):
        #    self.removeLayer(i)
        
    # NOT USED ANYMORE
    # Create a List of nodes along path and put on txtJunctions (QTextEdit removed from ui)
    def QW_find_Path(self):
        layer = self.common.PegaQWaterLayer('JUNCTIONS',silent=True)
        if layer:            
            self.junctionLayer = layer
            request1 = self.cmbFeat_From.currentFeatureRequest()
            lstFrom = list(layer.getFeatures(request1))
            request2 = self.cmbFeat_To.currentFeatureRequest()
            lstTo = list(layer.getFeatures(request2))
            if lstFrom and lstTo:
                ptoFrom = lstFrom[0]
                ptoTo = lstTo[0]
                layer.removeSelection()
                [layer.select(id) for id in [ptoFrom.id(),ptoTo.id()]]
                iface.mapCanvas().zoomToSelected(layer)
                
                pathLayer = self.QW_createPath_byPoints(ptoFrom.geometry(), ptoTo.geometry())
                #pathLayer = self.QW_createPath_byPoints(self.QW_reproject(layer, ptoFrom.geometry()), self.QW_reproject(layer, ptoTo.geometry()))
                if pathLayer:
                    juncIDs = self.QW_list_Junctions(layer, pathLayer,'DC_ID')
                    myText='\n'.join(juncIDs)
                    self.txtJunctions.setPlainText(myText)
            else:
                layer.removeSelection()

        
    def QW_plotpath_clicked(self):
        #layer = self.common.PegaQWaterLayer('JUNCTIONS',silent=True)
        proj = QgsProject.instance()
        layer = proj.mapLayersByName("QW_LayerNodes")[0]
        if layer:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.junctionLayer = layer
            request1 = self.cmbFeat_From.currentFeatureRequest()
            lstFrom = list(layer.getFeatures(request1))
            request2 = self.cmbFeat_To.currentFeatureRequest()
            lstTo = list(layer.getFeatures(request2))            
            if self.QW_HasDEM() or True: #by passed DEM requirement
                if lstFrom and lstTo:
                    ptoFrom = lstFrom[0]
                    ptoTo = lstTo[0]
                    layer.removeSelection()
                    [layer.select(id) for id in [ptoFrom.id(),ptoTo.id()]]
                    iface.mapCanvas().zoomToSelected(layer)
                    pathLayer = self.QW_createPath_byPoints(ptoFrom.geometry(), ptoTo.geometry())
                    if pathLayer:
                        pathLayer.setName("QW_ProfilePath")
                        proj = QgsProject.instance()
                        #delete all QW_ProfilePath layers from project before add new
                        for profLayer in proj.mapLayersByName("QW_ProfilePath"):
                            proj.removeMapLayer(profLayer.id())
                        proj.addMapLayer(pathLayer)
                        #proj.layerTreeRoot().findLayer(pathLayer.id()).setItemVisibilityChecked(False) #Turn off layer
                        iface.setActiveLayer(pathLayer)
                        #Changed selection method combobox to update plot
                        self.comboBox.setCurrentIndex(2) #2=Selection by layer
                        self.comboBox.setCurrentIndex(3) #3=Selection by path
                        
                        #restore last selected combobox items
                        self.cmbFeat_From.setCurrentFeature(ptoFrom)
                        self.cmbFeat_To.setCurrentFeature(ptoTo)

                        #self.tableViewTool.addLayer(self.mdl, pathLayer)
                    else:
                        iface.messageBar().pushMessage('QWater', 'Path not found!', level=Qgis.Warning, duration=2)
                else:
                    iface.messageBar().pushMessage('QWater', 'Select from and to Junctions first!', level=Qgis.Warning, duration=2)
            else:
                iface.messageBar().pushMessage('QWater', 'Add a DEM to the profile view first!', level=Qgis.Warning, duration=2)
            QApplication.restoreOverrideCursor()
        else:
            iface.messageBar().pushMessage('QWater', 'JUNCTIONS Layer undefined!', level=Qgis.Warning, duration=2)
        
    #not used yet, because profileTool plugin has a bug
    def QW_removeQWaterLayers(self):
        model1 = self.mdl
        for campo in ['RESULT_HEA','ELEVATION']:
            linha = self.QW_findRow(campo)
            if linha>=0:
                model1.removeRow(linha)
        
    def QW_plotByJunction_selected(self, ativa=True):
        #Cria um layer com as feicoes do tipo nós
        layer = self.QW_mergeNodes_layer()
        if layer:
            layer.setName("QW_LayerNodes")
            proj = QgsProject.instance()
            #delete all QW_LayerNodes layers from project before add new
            for profLayer in proj.mapLayersByName("QW_LayerNodes"):
                proj.removeMapLayer(profLayer.id())
            proj.addMapLayer(layer)
            proj.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False) #Turn off layer
            if layer:
                campos = layer.fields().names()
                campo = 'DC_ID'
                #self.QW_removeQWaterLayers()
                if campo in campos:
                    self.cmbFeat_From.clear()
                    self.cmbFeat_From.setSourceLayer (layer)
                    self.cmbFeat_From.setIdentifierFields(['DC_ID'])
                    self.cmbFeat_From.setDisplayExpression(str("DC_ID"))
                    self.cmbFeat_To.clear()
                    self.cmbFeat_To.setSourceLayer (layer)
                    self.cmbFeat_To.setIdentifierFields(['DC_ID'])
                    self.cmbFeat_To.setDisplayExpression(str("DC_ID"))
                campo = 'RESULT_HEA'
                if campo in campos and (self.QW_findRow(campo)<0):
                    self.tableViewTool.QW_addLayer(self.mdl, layer, campo, corIndex=0)
                
                campo = 'STATIC_HEA'
                junctionLayer = self.common.PegaQWaterLayer('JUNCTIONS',silent=True)
                if campo in campos and (self.QW_findRow(campo)<0) and junctionLayer:
                    self.tableViewTool.QW_addLayer(self.mdl, junctionLayer, campo, corIndex=2)
                    
                # layer.willBeDeleted.connect(self.QW_willBeDeleted(layer))
                #campo = 'ELEVATION' #Almerio desliguei o elevation
                #if campo in campos and (self.QW_findRow(campo)<0):
                #    self.tableViewTool.QW_addLayer(self.mdl, layer, campo, corIndex=1)
                
                #Add DEM layer            
                demLyr = self.common.PegaQWaterLayer('DEM',silent=True)          
                if demLyr and (self.QW_findRow(demLyr.name())<0):
                    self.addLayer(demLyr)
    
    def getPointOffset_Along(self, pathLayer, RefPoint, distance):
        for feat in pathLayer.getFeatures(): #get the first and unique feature from layer
            LineString = feat.geometry()
            
        distRefPoint = LineString.lineLocatePoint(RefPoint)
        lineToPath = LineString.shortestLine(RefPoint)
        minDist = lineToPath.length()
        if (distRefPoint==-1) or (minDist>2):
            return 0 #Error
        else:            
            return LineString.interpolate(distRefPoint+distance)
            
    def QW_mergeNodes_layer(self):
        NodesLyr = {'RESERVOIRS': 'HEAD',
                   'TANKS': 'ELEVATION',
                   'PUMPS': 'ELEVATION',                   
                   'JUNCTIONS': 'ELEVATION'}
        NodesAjust = ['PUMPS'] #Camadas que precisam ter valores revisados para o plotar no perfil, futuramente adicionar valvulas
        lyrTipos = list(NodesLyr.keys())
        lyrList=[]
        proj=QgsProject.instance()
        lyrSearch = proj.mapLayersByName("QW_ProfilePath")
        if lyrSearch:
            pathLayer = lyrSearch[0]
        for lyrTipo in lyrTipos:
            ProjNode=proj.readEntry("QWater", lyrTipo)[0]
            if ProjNode!='':
                vLayerLst=proj.mapLayersByName(ProjNode)
                if vLayerLst:
                    vLayer=vLayerLst[0]                    
                    if lyrTipo in NodesAjust:
                        clone = vLayer.clone()
                        clone.startEditing()
                        campos = ['RES_HEA_UP','RES_HEA_DN']
                        for feat in clone.getFeatures():                            
                            feat['RESULT_HEA']=feat[campos[0]]
                            clone.updateFeature(feat)
                        for feat in clone.getFeatures():
                            if lyrSearch and pathLayer:
                                geom = feat.geometry()
                                geomDN = self.getPointOffset_Along(pathLayer, geom, 1)
                                if geomDN!= 0:
                                    feat.setGeometry(geomDN)
                                    feat['DC_ID']+='dn'
                                    feat['RESULT_HEA']=feat[campos[1]]
                                    clone.addFeature(feat)
                        lyrList.append(clone)
                    else:
                        lyrList.append(vLayer)
                    
        if lyrList:
            algresult = processing.run("native:mergevectorlayers", 
                {'LAYERS':lyrList,
                'CRS':None,
                'OUTPUT':'memory:'
                })            
            mergedLyr = algresult['OUTPUT']
            return mergedLyr
        else:
            msgTxt= QCoreApplication.translate('QWater','No QWater Node Layers!')
            iface.messageBar().pushMessage("QWater:", msgTxt, level=Qgis.Warning, duration=5)
            return False

    def QW_HasDEM(self):
        mdl = self.mdl        
        for row in range(mdl.rowCount()):
            mdlCol5 = mdl.item(row, 5).data(QtCore.Qt.EditRole) #layer
            layer = mdlCol5
            if (layer.type() == layer.RasterLayer) or (layer.type() == layer.MeshLayer):
                return True
        return False
    
    
    def QW_findRow(self, nome):
        resp=False
        mdl = self.mdl        
        for row in range(mdl.rowCount()):
            fieldName = mdl.item(row, 2).data(QtCore.Qt.EditRole)
            if fieldName==nome:
                return row
            row+=1
        return -1
    
    def QW_createPath_byPoints(self, ptoFrom, ptoTo):
        #return polyline path
        layer = self.common.PegaQWaterLayer('PIPES',silent=True)
        if layer:
            try:
                algresult = processing.run("native:shortestpathpointtopoint", 
                    {'INPUT': layer,
                     'STRATEGY': 0,
                     'TOLERANCE' : 1,
                     'START_POINT': ptoFrom,
                     'END_POINT': ptoTo,
                     'OUTPUT': 'memory:'
                    })
                pathPolyline = algresult['OUTPUT']
                #QgsProject.instance().addMapLayer(pathPolyline)
                for feat in pathPolyline.getFeatures():
                    geom = feat.geometry()
                    geomProj = self.QW_reproject(layer, geom)
                    iface.mapCanvas().setExtent(geomProj.boundingBox().scaled(1.2))
                return pathPolyline
            except Exception as e:
                iface.messageBar().pushMessage('QWater', 'Path not found! '+str(e), level=Qgis.Warning, duration=2)
                return None
    
    def QW_list_Junctions(self, nodeLayer, pathLayer, fieldName):
        featList = list(pathLayer.getFeatures()) #only the first feature
        juncIDs=[]
        if featList:
            geom = featList[0].geometry()
            if geom.isMultipart():
                polyline=geom.asMultiPolyline()[0]
            else:
                polyline=geom.asPolyline()
        
            spIndex = QgsSpatialIndex()
            for feat in nodeLayer.getFeatures():
                spIndex.addFeature(feat)
                
            for pnt in polyline:                
                nearestIds = spIndex.nearestNeighbor(pnt,1) #return 1 nearest Neighbor            
                feats = list(nodeLayer.getFeatures(QgsFeatureRequest().setFilterFids(nearestIds)))
                if feats:
                    feat=feats[0]
                    juncIDs.append(feat[fieldName])
                else:
                    iface.messageBar().pushMessage('QWater', 'Near Junction not found!', level=Qgis.Warning, duration=2)
            return juncIDs
        else:
            iface.messageBar().pushMessage('QWater', 'Path null!', level=Qgis.Warning, duration=2)
            return None   
       
    def QW_reproject(self, layer, geom):
        #reproject to canvas CRS
        source_crs = layer.crs()
        dest_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        coordTransf = QgsCoordinateTransform(source_crs, dest_crs,QgsProject.instance())
        geom.transform(coordTransf)
        return geom
        
    def QW_onFeatureIdentified(self, feature):
        layer = self.junctionLayer
        fid = feature.id()
        layer.select(fid)
        iface.mapCanvas().flashFeatureIds(layer, [fid])
        if self.btnFrom.isChecked():
            self.cmbFeat_From.setCurrentFeature(feature)
            self.QW_identify_deactivate(self.btnFrom)
        elif self.btnTo.isChecked():
            self.cmbFeat_To.setCurrentFeature(feature)
            self.QW_identify_deactivate(self.btnTo)
    
    def QW_identify_activate(self, layer, btn):
        mc=iface.mapCanvas()
        mapTool = QgsMapToolIdentifyFeature(mc)
        mapTool.setLayer(layer)
        btn.setChecked(True)
        mc.setMapTool(mapTool)
        mapTool.featureIdentified.connect(self.QW_onFeatureIdentified)
        mapTool.deactivated.connect(self.QW_identify_deactivated)
        self.QW_identifymapTool = mapTool
    
    def QW_identify_deactivated(self):
        self.btnTo.setChecked(False)
        self.btnFrom.setChecked(False)
        mc=iface.mapCanvas().unsetMapTool(self.QW_identifymapTool)
    
    def QW_identify_deactivate(self, btn):
        #btn.setCheckable(False)
        btn.setChecked(False)
        mc=iface.mapCanvas().unsetMapTool(self.QW_identifymapTool)        
        
    def QW_btnFrom_clicked(self):
        proj=QgsProject.instance()
        vLayerLst=proj.mapLayersByName('QW_LayerNodes')
        if vLayerLst:
            layer=vLayerLst[0]
        else:
            layer = self.common.PegaQWaterLayer('JUNCTIONS',silent=True)
        canvas = self.iface.mapCanvas()
        if layer: 
            self.junctionLayer = layer
            self.QW_identify_activate(layer, self.btnFrom)
        else:
            print('nao achou layer')

    def QW_btnTo_clicked(self):
        proj=QgsProject.instance()
        vLayerLst=proj.mapLayersByName('QW_LayerNodes')
        if vLayerLst:
            layer=vLayerLst[0]
        else:
            layer = self.common.PegaQWaterLayer('JUNCTIONS',silent=True)
        canvas = self.iface.mapCanvas()
        if layer: 
            self.junctionLayer = layer
            self.QW_identify_activate(layer, self.btnTo)
        else:
            print('nao achou layer')


    #********************************************************************************
    #init things ****************************************************************
    #********************************************************************************


    def addOptionComboboxItems(self):
        self.cboLibrary.addItem("PyQtGraph")
        if matplotlib_loaded:
            self.cboLibrary.addItem("Matplotlib")
        if Qwt5_loaded:
            self.cboLibrary.addItem("Qwt5")

    def selectionMethod(self, item):
        self.profiletoolcore.toolrenderer.setSelectionMethod(item)
        if item==3:
            self.QW_plotByJunction_selected(True)
        self.grpByJunctions.setVisible(item==3)
        if (item in [0,1,2]) or self.iface.mapCanvas().mapTool() == self.profiletoolcore.toolrenderer.tool:
            self.iface.mapCanvas().setMapTool(self.profiletoolcore.toolrenderer.tool)
            self.profiletoolcore.toolrenderer.connectTool()

    def changePlotLibrary(self, item):
        self.plotlibrary = self.cboLibrary.itemText(item)
        self.addPlotWidget(self.plotlibrary)

        if self.plotlibrary == "PyQtGraph":
            self.checkBox_mpl_tracking.setEnabled(True)
            self.checkBox_showcursor.setEnabled(True)
            self.checkBox_mpl_tracking.setCheckState(2)
            self.profiletoolcore.activateMouseTracking(2)
            self.checkBox_mpl_tracking.stateChanged.connect(self.profiletoolcore.activateMouseTracking)
            self._onSameAxisScaleStateChanged(self.cbSameAxisScale.checkState())

        elif self.plotlibrary == 'Matplotlib':
            self.checkBox_mpl_tracking.setEnabled(True)
            self.checkBox_showcursor.setEnabled(False)
            self.checkBox_mpl_tracking.setCheckState(2)
            self.profiletoolcore.activateMouseTracking(2)
            self.checkBox_mpl_tracking.stateChanged.connect(self.profiletoolcore.activateMouseTracking)
            self.cbSameAxisScale.setCheckState(Qt.Unchecked)

        else:
            self.checkBox_mpl_tracking.setCheckState(0)
            self.checkBox_mpl_tracking.setEnabled(False)
            self.cbSameAxisScale.setCheckState(Qt.Unchecked)

        self.cbSameAxisScale.setEnabled(self.plotlibrary == 'PyQtGraph')

    def addPlotWidget(self, library):
        layout = self.frame_for_plot.layout()
        while layout.count():
            child = layout.takeAt(0)
            child.widget().deleteLater()

        if library == "PyQtGraph":
            self.stackedWidget.setCurrentIndex(0)
            self.plotWdg = PlottingTool().changePlotWidget("PyQtGraph", self.frame_for_plot)
            layout.addWidget(self.plotWdg)
            self.TYPE = "PyQtGraph"
            self.cbxSaveAs.clear()
            self.cbxSaveAs.addItems(["Graph - PNG", "Graph - SVG", "3D line - DXF", "2D Profile - DXF"])

        elif library == "Qwt5":
            self.stackedWidget.setCurrentIndex(0)
            widget1 = self.stackedWidget.widget(1)            
            if widget1:
                self.stackedWidget.removeWidget(widget1)
                widget1 = None
            # self.widget_save_buttons.setVisible( True )
            self.plotWdg = PlottingTool().changePlotWidget("Qwt5", self.frame_for_plot)
            layout.addWidget(self.plotWdg)

            if QT_VERSION < 0x040100:
                idx = self.cbxSaveAs.model().index(0, 0)
                self.cbxSaveAs.model().setData(idx, QVariant(0), QtCore.Qt.UserRole - 1)
                self.cbxSaveAs.setCurrentIndex(1)
            if QT_VERSION < 0x040300:
                idx = self.cbxSaveAs.model().index(1, 0)
                self.cbxSaveAs.model().setData(idx, QVariant(0), QtCore.Qt.UserRole - 1)
                self.cbxSaveAs.setCurrentIndex(2)
            self.TYPE = "Qwt5"

        elif library == "Matplotlib":
            self.stackedWidget.setCurrentIndex(0)
            # self.widget_save_buttons.setVisible( False )
            self.plotWdg = PlottingTool().changePlotWidget("Matplotlib", self.frame_for_plot)
            layout.addWidget(self.plotWdg)

            if int(qgis.PyQt.QtCore.QT_VERSION_STR[0]) == 4:
                # from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
                mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QTAgg(
                    self.plotWdg, self.frame_for_plot
                )
                # layout.addWidget( mpltoolbar )
                self.stackedWidget.insertWidget(1, mpltoolbar)
                self.stackedWidget.setCurrentIndex(1)
                lstActions = mpltoolbar.actions()
                mpltoolbar.removeAction(lstActions[7])
                mpltoolbar.removeAction(lstActions[8])

            elif int(qgis.PyQt.QtCore.QT_VERSION_STR[0]) == 5:
                # from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
                # mpltoolbar = matplotlib.backends.backend_qt5agg.NavigationToolbar2QTAgg(self.plotWdg, self.frame_for_plot)
                pass
            self.TYPE = "Matplotlib"
            self.cbxSaveAs.clear()
            self.cbxSaveAs.addItems(
                ["Graph - PDF", "Graph - PNG", "Graph - SVG", "Graph - print (PS)", "3D line - DXF", "2D Profile - DXF"]
            )

    # ********************************************************************************
    # graph things ****************************************************************
    # ********************************************************************************

    def connectYSpinbox(self):
        self.sbMinVal.valueChanged.connect(self.reScalePlot)
        self.sbMaxVal.valueChanged.connect(self.reScalePlot)

    def disconnectYSpinbox(self):
        try:
            self.sbMinVal.valueChanged.disconnect(self.reScalePlot)
        except:
            pass
        try:
            self.sbMaxVal.valueChanged.disconnect(self.reScalePlot)
        except:
            pass

    def connectPlotRangechanged(self):
        self.plotWdg.getViewBox().sigRangeChanged.connect(self.plotRangechanged)

    def disconnectPlotRangechanged(self):
        try:
            self.plotWdg.getViewBox().sigRangeChanged.disconnect(self.plotRangechanged)
        except:
            pass

    def plotRangechanged(self, param=None):  # called when pyqtgraph view changed
        PlottingTool().plotRangechanged(self, self.cboLibrary.currentText())

    def reScalePlot(self, param):  # called when a spinbox value changed
        if type(param) == bool:  # comes from button
            PlottingTool().reScalePlot(self, self.profiletoolcore.profiles, self.cboLibrary.currentText(), True)

        else:  # spinboxchanged
            if self.sbMinVal.value() == self.sbMaxVal.value() == 0:
                # don't execute it on init
                pass
            else:
                PlottingTool().reScalePlot(self, self.profiletoolcore.profiles, self.cboLibrary.currentText())

    def showCursor(self, int1):
        # For pyqtgraph mode
        if self.plotlibrary == "PyQtGraph":
            if int1 == 2:
                self.showcursor = True
                self.profiletoolcore.doTracking = bool(self.checkBox_mpl_tracking.checkState())
                self.checkBox_mpl_tracking.setEnabled(True)
                for item in self.plotWdg.allChildItems():
                    if str(type(item)) == "<class 'profiletool.pyqtgraph.graphicsItems.InfiniteLine.InfiniteLine'>":
                        if item.name() == "cross_vertical":
                            item.show()
                        elif item.name() == "cross_horizontal":
                            item.show()
                    elif str(type(item)) == "<class 'profiletool.pyqtgraph.graphicsItems.TextItem.TextItem'>":
                        if item.textItem.toPlainText()[0] == "X":
                            item.show()
                        elif item.textItem.toPlainText()[0] == "Y":
                            item.show()
            elif int1 == 0:
                self.showcursor = False
                self.profiletoolcore.doTracking = False
                self.checkBox_mpl_tracking.setEnabled(False)

                for item in self.plotWdg.allChildItems():
                    if str(type(item)) == "<class 'profiletool.pyqtgraph.graphicsItems.InfiniteLine.InfiniteLine'>":
                        if item.name() == "cross_vertical":
                            item.hide()
                        elif item.name() == "cross_horizontal":
                            item.hide()
                    elif str(type(item)) == "<class 'profiletool.pyqtgraph.graphicsItems.TextItem.TextItem'>":
                        if item.textItem.toPlainText()[0] == "X":
                            item.hide()
                        elif item.textItem.toPlainText()[0] == "Y":
                            item.hide()
            self.profiletoolcore.plotProfil()

    # ********************************************************************************
    # tablebiew things ****************************************************************
    # ********************************************************************************

    def addLayer(self, layer1=None):
        if isinstance(layer1, bool):  # comes from click
            layer1 = self.iface.activeLayer()

        self.tableViewTool.addLayer(self.iface, self.mdl, layer1)
        self.profiletoolcore.updateProfil(self.profiletoolcore.pointstoDraw, False)
        layer1.dataChanged.connect(self.refreshPlot)

    def removeLayer(self, index=None):
        if isinstance(index, bool):  # come from button
            index = self.tableViewTool.chooseLayerForRemoval(self.iface, self.mdl)

        if index is not None:
            layer = self.mdl.index(index, 4).data()
            try:
                layer.dataChanged.disconnect(self.refreshPlot)
            except:
                pass
            self.tableViewTool.removeLayer(self.mdl, index)

        self.profiletoolcore.updateProfil(self.profiletoolcore.pointstoDraw, False, True)

    def refreshPlot(self):
        #
        #    Refreshes/updates the plot without requiring the user to
        #    redraw the plot line (rubberband)
        #
        self.profiletoolcore.updateProfil(self.profiletoolcore.pointstoDraw, False, True)

    def _onClick(self, index1):  # action when clicking the tableview
        self.tableViewTool.onClick(self.iface, self, self.mdl, self.plotlibrary, index1)

    def _onChange(self, item):
        if (
            not self.mdl.item(item.row(), 5) is None
            and item.column() == 4
            and self.mdl.item(item.row(), 5).data(QtCore.Qt.EditRole).type() == qgis.core.QgsMapLayer.VectorLayer
        ):

            self.profiletoolcore.plotProfil()

    def _onSameAxisScaleStateChanged(self, state):
        """
        Called whenever the checkbox button for same scale axis status has changed
        if checked, plot will always keep same scale on both axis (aspect ratio of 1)

        Only supported with PyQtGraph
        """

        if ( self.plotlibrary == 'PyQtGraph' ):
            self.plotWdg.getViewBox().setAspectLocked(state == Qt.Checked)

    #********************************************************************************
    #coordinate tab ****************************************************************
    #********************************************************************************
    @staticmethod
    def _profile_name(profile):
        groupTitle = profile["layer"].name()
        band = profile["band"]
        if band is not None and band > -1:
            groupTitle += "_band_{}".format(band)
        return groupTitle.replace(" ", "_")

    def updateCoordinateTab(self):

        try:  # Reinitializing the table tab
            self.VLayout = self.scrollAreaWidgetContents.layout()
            while 1:
                child = self.VLayout.takeAt(0)
                if not child:
                    break
                child.widget().deleteLater()
        except:
            self.VLayout = QVBoxLayout(self.scrollAreaWidgetContents)
            self.VLayout.setContentsMargins(9, -1, -1, -1)
        # Setup the table tab
        self.groupBox = []
        self.profilePushButton = []
        self.coordsPushButton = []
        self.tolayerPushButton = []
        self.tableView = []
        self.verticalLayout = []
        if self.mdl.rowCount() != self.profiletoolcore.profiles:
            # keep the number of profiles and the model in sync.
            self.profiletoolcore.updateProfil(self.profiletoolcore.pointstoDraw, False, False)
        for i in range(0, self.mdl.rowCount()):
            self.groupBox.append(QGroupBox(self.scrollAreaWidgetContents))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.groupBox[i].setSizePolicy(sizePolicy)
            profileTitle = self._profile_name(self.profiletoolcore.profiles[i])

            try:  # qgis2
                self.groupBox[i].setTitle(
                    QApplication.translate("GroupBox" + str(i), profileTitle, None, QApplication.UnicodeUTF8)
                )
            except:  # qgis3
                self.groupBox[i].setTitle(QApplication.translate("GroupBox" + str(i), profileTitle, None))
            self.groupBox[i].setObjectName("groupBox" + str(i))

            self.verticalLayout.append(QVBoxLayout(self.groupBox[i]))
            self.verticalLayout[i].setObjectName("verticalLayout")
            # The table
            self.tableView.append(QTableView(self.groupBox[i]))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.tableView[i].setSizePolicy(sizePolicy)
            self.tableView[i].setObjectName("tableView" + str(i))
            # font = QFont("Arial", 8)
            column = len(self.profiletoolcore.profiles[i]["l"])
            self.mdl2 = QStandardItemModel(2, column)
            for j in range(len(self.profiletoolcore.profiles[i]["l"])):
                self.mdl2.setData(self.mdl2.index(0, j, QModelIndex()), self.profiletoolcore.profiles[i]["l"][j])
                # self.mdl2.setData(self.mdl2.index(0, j, QModelIndex())  ,font ,QtCore.Qt.FontRole)
                self.mdl2.setData(self.mdl2.index(1, j, QModelIndex()), self.profiletoolcore.profiles[i]["z"][j])
                # self.mdl2.setData(self.mdl2.index(1, j, QModelIndex())  ,font ,QtCore.Qt.FontRole)
            self.tableView[i].verticalHeader().setDefaultSectionSize(18)
            self.tableView[i].horizontalHeader().setDefaultSectionSize(60)
            self.tableView[i].setModel(self.mdl2)
            # 2 * header (1 header + 1 horz slider) + nrows + a small margin
            minTableHeight = (
                2 * self.tableView[i].horizontalHeader().height()
                + sum(self.tableView[i].rowHeight(j) for j in range(self.tableView[i].model().rowCount()))
                + 6
            )  # extra safety margin
            self.tableView[i].setMinimumHeight(minTableHeight)

            self.verticalLayout[i].addWidget(self.tableView[i])

            self.horizontalLayout = QHBoxLayout()

            # the copy to clipboard button
            self.profilePushButton.append(QPushButton(self.groupBox[i]))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            self.profilePushButton[i].setSizePolicy(sizePolicy)
            try:  # qgis2
                self.profilePushButton[i].setText(
                    QApplication.translate("GroupBox", "Copy to clipboard", None, QApplication.UnicodeUTF8)
                )
            except:  # qgis3
                self.profilePushButton[i].setText(QApplication.translate("GroupBox", "Copy to clipboard", None))
            self.profilePushButton[i].setObjectName(str(i))
            self.horizontalLayout.addWidget(self.profilePushButton[i])

            # button to copy to clipboard with coordinates
            self.coordsPushButton.append(QPushButton(self.groupBox[i]))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            self.coordsPushButton[i].setSizePolicy(sizePolicy)
            try:  # qgis2
                self.coordsPushButton[i].setText(
                    QApplication.translate(
                        "GroupBox", "Copy to clipboard (with coordinates)", None, QApplication.UnicodeUTF8
                    )
                )
            except:  # qgis3
                self.coordsPushButton[i].setText(
                    QApplication.translate("GroupBox", "Copy to clipboard (with coordinates)", None)
                )

            # button to copy to clipboard with coordinates
            self.tolayerPushButton.append(QPushButton(self.groupBox[i]))
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            self.tolayerPushButton[i].setSizePolicy(sizePolicy)
            try:  # qgis2
                self.tolayerPushButton[i].setText(
                    QApplication.translate("GroupBox", "Create Temporary layer", None, QApplication.UnicodeUTF8)
                )
            except:  # qgis3
                self.tolayerPushButton[i].setText(QApplication.translate("GroupBox", "Create Temporary layer", None))

            self.coordsPushButton[i].setObjectName(str(i))
            self.horizontalLayout.addWidget(self.coordsPushButton[i])

            self.tolayerPushButton[i].setObjectName(str(i))
            self.horizontalLayout.addWidget(self.tolayerPushButton[i])

            self.horizontalLayout.addStretch(0)
            self.verticalLayout[i].addLayout(self.horizontalLayout)

            self.VLayout.addWidget(self.groupBox[i])

            self.profilePushButton[i].clicked.connect(self.copyTable)
            self.coordsPushButton[i].clicked.connect(self.copyTableAndCoords)
            self.tolayerPushButton[i].clicked.connect(self.createTemporaryLayer)

    def copyTable(self):  # Writing the table to clipboard in excel form
        nr = int(self.sender().objectName())
        self.clipboard = QApplication.clipboard()
        text = ""
        for i in range(len(self.profiletoolcore.profiles[nr]["l"])):
            text += (
                str(self.profiletoolcore.profiles[nr]["l"][i])
                + "\t"
                + str(self.profiletoolcore.profiles[nr]["z"][i])
                + "\n"
            )
        self.clipboard.setText(text)

    def copyTableAndCoords(self):  # Writing the table with coordinates to clipboard in excel form
        nr = int(self.sender().objectName())
        self.clipboard = QApplication.clipboard()
        text = ""
        for i in range(len(self.profiletoolcore.profiles[nr]["l"])):
            text += (
                str(self.profiletoolcore.profiles[nr]["l"][i])
                + "\t"
                + str(self.profiletoolcore.profiles[nr]["x"][i])
                + "\t"
                + str(self.profiletoolcore.profiles[nr]["y"][i])
                + "\t"
                + str(self.profiletoolcore.profiles[nr]["z"][i])
                + "\n"
            )
        self.clipboard.setText(text)

    def createTemporaryLayer(self):
        nr = int(self.sender().objectName())
        type = "Point?crs=" + str(self.profiletoolcore.profiles[nr]["layer"].crs().authid())
        name = "ProfileTool_{}".format(self._profile_name(self.profiletoolcore.profiles[nr]))
        vl = QgsVectorLayer(type, name, "memory")
        pr = vl.dataProvider()
        vl.startEditing()
        # add fields
        pr.addAttributes([QgsField("Value", QVariant.Double)])
        vl.updateFields()
        # Add features to layer
        for i in range(len(self.profiletoolcore.profiles[nr]["l"])):
            fet = QgsFeature(vl.fields())
            # set geometry
            fet.setGeometry(
                QgsGeometry.fromPointXY(
                    QgsPointXY(self.profiletoolcore.profiles[nr]["x"][i], self.profiletoolcore.profiles[nr]["y"][i])
                )
            )
            # set attributes
            fet.setAttributes([self.profiletoolcore.profiles[nr]["z"][i]])
            pr.addFeatures([fet])
        vl.commitChanges()
        # labeling/enabled
        if False:
            labelsettings = vl.labeling().settings()
            labelsettings.enabled = True

        # vl.setCustomProperty("labeling/enabled", "true")
        # show layer
        try:  # qgis2
            qgis.core.QgsMapLayerRegistry.instance().addMapLayer(vl)
        except:  # qgis3
            qgis.core.QgsProject.instance().addMapLayer(vl)

    # ********************************************************************************
    # other things ****************************************************************
    # ********************************************************************************

    def closeEvent(self, event):        
        self.closed.emit()
        self.profiletoolcore.cleaning()
        # self.butSaveAs.clicked.disconnect(self.saveAs)
        # return QDockWidget.closeEvent(self, event)

    # generic save as button
    def saveAs(self):
        idx = self.cbxSaveAs.currentText()
        if idx == "Graph - PDF":
            self.outPDF()
        elif idx == "Graph - PNG":
            self.outPNG()
        elif idx == "Graph - SVG":
            self.outSVG()
        elif idx == "Graph - print (PS)":
            self.outPrint()
        elif idx == "3D line - DXF":
            self.outDXF("3D")
        elif idx == "2D Profile - DXF":
            self.outDXF("2D")
        else:
            print("plottingtool: invalid index " + str(idx))

    def outPrint(self):  # Postscript file rendering doesn't work properly yet.
        PlottingTool().outPrint(self.iface, self, self.mdl, self.cboLibrary.currentText())

    def outPDF(self):
        PlottingTool().outPDF(self.iface, self, self.mdl, self.cboLibrary.currentText())

    def outSVG(self):
        PlottingTool().outSVG(self.iface, self, self.mdl, self.cboLibrary.currentText())

    def outPNG(self):
        PlottingTool().outPNG(self.iface, self, self.mdl, self.cboLibrary.currentText())

    def outDXF(self, type):
        PlottingTool().outDXF(
            self.iface, self, self.mdl, self.cboLibrary.currentText(), self.profiletoolcore.profiles, type
        )
