# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name		     : QWater Rename Tools
Description          : 
Date                 : 18/Set/2018/ 
copyright            : (C) 2018 by Jorge Almerio
email                : jorgealmerio@yahoo.com.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
# Import the PyQt and QGIS libraries
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QApplication
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *
#import math

import qgis.utils
#from .QWater_01Campos import *
import os
#from .QWater_04Estilos import *

class Rename_Tools(object):
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        #self.EstiloClasse=Estilos()

    def initGui(self):
        # Create action that will start plugin configuration
        #self.action = QAction(QIcon(":/plugins/network_tools/icon.png"), "Renumber Network", self.iface.mainWindow())
        #Add toolbar button and menu item
        #self.iface.addPluginToMenu("&Renomeia Rede", self.action)
        #self.iface.addToolBarIcon(self.action)
        
        proj = QgsProject.instance()
        aForma='PIPES'
        ProjVar=proj.readEntry("QWater", aForma)[0]
        if ProjVar=='':
            msgTxt=QCoreApplication.translate('QWater','Undefined layer: ') +aForma+ '\n'
            self.iface.messageBar().pushMessage('QWater', msgTxt, level=Qgis.Warning, duration=4)
            return False
        else:
            vLayerLst=proj.mapLayersByName(ProjVar)
            if not vLayerLst:                
                msgTxt=aForma+'='+ProjVar+QCoreApplication.translate('QWater',u' (Layer not found)')
                self.iface.messageBar().pushMessage('QWater', msgTxt, level=Qgis.Warning, duration=4)
                return False
        
        #load the form
        path = os.path.dirname(os.path.abspath(__file__))
        self.dock = uic.loadUi(os.path.join(path, "QWater_Rename_dialog.ui"))
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)#Qt.RightDockWidgetArea
        
        self.sourceIdEmitPoint = QgsMapToolEmitPoint(self.iface.mapCanvas())
        
        #connect the action to each method
        #self.action.triggered.connect(self.show)
        self.dock.buttonSelectSourceId.clicked.connect(self.selectSourceId)
        self.sourceIdEmitPoint.canvasClicked.connect(self.setSourceId)
        self.dock.buttonRun.clicked.connect(self.run)
        self.dock.buttonClear.clicked.connect(self.clear)
        self.dock.buttonVerifica.clicked.connect(self.call_Verifica)

        self.sourceFeatID = None
        self.TrechosChained=[]
        self.PVfim='FIM'
        
        #Chama a rotina que Verifica se existem multipartes ou polilinhas
        self.call_Verifica() #self.CheckPolylines(vl,SilentRun=True)
        
    def show(self):
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
       
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Renumber Network", self.action)
        self.iface.removeDockWidget(self.dock)

    def selectSourceId(self, checked):
        if checked:
            self.toggleSelectButton(self.dock.buttonSelectSourceId)
            self.iface.mapCanvas().setMapTool(self.sourceIdEmitPoint)
        else:
            self.iface.mapCanvas().unsetMapTool(self.sourceIdEmitPoint)

    def PegaPipeLayer(self):
        proj = QgsProject.instance()
        aForma='PIPES'
        ProjVar=proj.readEntry("QWater", aForma)[0]
        if ProjVar=='':
            msgTxt=QCoreApplication.translate('QWater','Undefined layer: ') +aForma
            QMessageBox.warning(None,'QWater',msgTxt)
            return False
        LayerLst=proj.mapLayersByName(ProjVar)
        if LayerLst:
            layer = proj.mapLayersByName(ProjVar)[0]
            return layer
        else:
            msgTxt=aForma+'='+ProjVar+QCoreApplication.translate('QWater',u' (Layer not found)')
            QMessageBox.warning(None,'QWater',msgTxt)
            return False

    def setSourceId(self, pt):
        proj = QgsProject.instance()
        aForma='PIPES'
        ProjVar=proj.readEntry("QWater", aForma)[0]
        if ProjVar=='':
            msgTxt=QCoreApplication.translate('QWater','Undefined layer: ') +aForma
            QMessageBox.warning(None,'QWater',msgTxt)
            return
        layer = proj.mapLayersByName(ProjVar)[0]
        layer.removeSelection()
        width = self.iface.mapCanvas().mapUnitsPerPixel() * 4
        rect = QgsRectangle(pt.x() - width,
                                  pt.y() - width,
                                pt.x() + width,
                                pt.y() + width)
        layer.selectByRect(rect,True)
        selected_features = layer.selectedFeatures()
        if layer.selectedFeatureCount()>1:
            QMessageBox.warning(None, 'QWater','More than one feature selected!\n')
            return
        if layer.selectedFeatureCount()==0:
            return
        for feat in selected_features:
            sourceID='1-1'#feat['DC_ID']
            self.sourceFeatID=feat.id()
            self.selectDownstream(layer)

    def getLength(self,layer):
        totalLen = 0
        count = 0
        for feature in layer.selectedFeatures():
            geom = feature.geometry()
#            idtxt = feature[str(self.dock.comboFields.currentText())]
#            self.dock.textEditLog.append(idtxt)
            totalLen = totalLen + geom.length()
            count = count + 1
        return totalLen, count

    def run(self):
#        QMessageBox.warning(self.dock, self.dock.windowTitle(),
#                'WARNING: run action, renomear')
        QApplication.setOverrideCursor(Qt.WaitCursor)
        proj = QgsProject.instance()
        aForma='PIPES'
        ProjVar=proj.readEntry("QWater", aForma)[0]
        if ProjVar=='':
            msgTxt='Layer Indefinido: ' +aForma+ '\n'
            QMessageBox.warning(None,'QWater',msgTxt)
            return
        layer = proj.mapLayersByName(ProjVar)[0]
        
        campoID='DC_ID'        
        Trecho=self.dock.spinColetor.value()
        NroDigitos = self.dock.spinColetorDigitos.value()
        PVpref =self.dock.lineEditPV_pref.text()
        OrdCresc=self.dock.radioCrescente.isChecked()
        NroElems=len(self.TrechosChained)
        if OrdCresc:
            Dir=1
        else:
            Trecho=Trecho+NroElems-1
            Dir=-1
        layer.startEditing()
        for index, elem in enumerate(self.TrechosChained):
#            print(index, elem)
            request = QgsFeatureRequest().setFilterFid(elem)
            feat=next(layer.getFeatures(request))
            #feat['Coletor']=Coletor
            #feat['Trecho']=Trecho
            feat['DC_ID']=PVpref+str(Trecho).rjust(NroDigitos,'0')
            Trecho += 1*Dir
            '''
            if index==0:#No primeiro trecho Verifica se tem algum trecho saindo do mesmo PV de montante
                Tem, NomePVM = self.VerificaPVMont_comun_comID(layer, feat)
                if Tem:
                    feat['PVM']=NomePVM
                else:
                    feat['PVM']=PVpref+str(PVnro).rjust(NroDigitosPV,'0')
            else:
                feat['PVM']=PVpref+str(PVnro).rjust(NroDigitosPV,'0')
            PVnro += Dir
            if index<NroElems-1:#Numera o PVJ final do coletor
                feat['PVJ']=PVpref+str(PVnro).rjust(NroDigitosPV,'0')
            else:
                feat['PVJ']=self.PVfim
            '''
            layer.updateFeature(feat)
        self.dock.textEditLog.append("N. of Renamed: "+str(len(self.TrechosChained)))
        #self.EstiloClasse.CarregaEstilo(layer, 'rede_nomes.qml')
        layer.triggerRepaint()
        
        if self.dock.buttonSelectSourceId.isChecked():
            self.dock.buttonSelectSourceId.click()
        QApplication.restoreOverrideCursor()
        
    def VerificaPVMont_Duplicado(self, layer):
        features = layer.getFeatures()
        valueLst=[None, 'NULL']
        AchouDuplic=False
        for feature in features:
            pipeID=feature['DC_ID'] or 'NULL'
            if pipeID not in valueLst:
                valueLst.append(pipeID)
            else:
                AchouDuplic=True
                self.dock.textEditLog.append("DC_ID duplicated: "+pipeID)
        return AchouDuplic
    
    # ESSA ROTINA NAO ESTA SENDO UTILIZADA
    # Verifica Se ja tem um trecho saindo do mesmo PV de Montante 
    def VerificaPVMont_comun_comID(self, layer, feat):
        tol = self.dock.spinBoxTol.value()
        # get list of nodes
        nodes = self.getNodes(feat)
        # get end node upstream 
        up_end_node = nodes[0]
        # select all features around upstream coordinate using a bounding box
        rectangle = QgsRectangle(up_end_node.x() - tol, up_end_node.y() - tol, up_end_node.x() + tol, up_end_node.y() + tol)
        request = QgsFeatureRequest().setFilterRect(rectangle)
        features = layer.getFeatures(request)
        # start nodes into tolerance        
        n_start_node=0
        features = layer.getFeatures(request)
        #iterate thru requested features
        for feature in features:
            if feat.id()!=feature.id():
                #get list of nodes
                nodes = self.getNodes(feature)
                #get start node upstream
                outro_up_node = nodes[0]
                #setup distance
                distance = QgsDistanceArea()
                #get distance from up_end_node to outro_up_node
                dist = distance.measureLine(up_end_node, outro_up_node)
                if dist < tol:
                    n_start_node=n_start_node+1
                    #add feature to selection list to iterate over it (if it not is the target)
                    pvm=feature['PVM']
                    if pvm!=NULL:
                        return True, pvm
        return False, 0
    def selectDownstream(self,layer):
        self.dock.textEditLog.clear()
        campo='DC_ID' 
        #QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    
        final_list = self.TrechosChained
        selection_list = []
        tol = self.dock.spinBoxTol.value()
        self.dock.textEditLog.append("Starting...")

        layer.removeSelection()
        
        layer.select(self.sourceFeatID)
        provider = layer.dataProvider()
        selection_list.append(self.sourceFeatID)
        final_list.append(self.sourceFeatID)
        # this part partially based on flowTrace by "Ed B"
        while selection_list:
            request = QgsFeatureRequest().setFilterFid(selection_list[0])
            feature = next(layer.getFeatures(request))
            # get list of nodes
            nodes = self.getNodes(feature)
            # get end node downstream 
            up_end_node = nodes[-1]
            # select all features around downstream coordinate using a bounding box
            rectangle = QgsRectangle(up_end_node.x() - tol, up_end_node.y() - tol, up_end_node.x() + tol, up_end_node.y() + tol)
            request = QgsFeatureRequest().setFilterRect(rectangle)
            features = layer.getFeatures(request)
            # start nodes into tolerance        
            n_start_node=0
            features = layer.getFeatures(request)
            #iterate thru requested features
            for feature in features:
                #get list of nodes
                nodes = self.getNodes(feature)
                #get start node upstream
                down_start_node = nodes[0]
                #setup distance
                distance = QgsDistanceArea()
                #get distance from up_end_node to down_start_node
                dist = distance.measureLine(up_end_node, down_start_node)
                if dist < tol:
                    n_start_node=n_start_node+1
                    #add feature to final list
                    final_list.append(feature.id())
                    #add feature to selection list to iterate over it (if it not is the target)
                    dcID = feature['DC_ID']
                    if self.dock.checkUndefined.isChecked() and (dcID != NULL):
                        final_list[len(final_list)-n_start_node:len(final_list)] = []
                        self.dock.textEditLog.append("Stopped at bifurcation!")
                        break
                    if feature.id() not in selection_list:
                        selection_list.append(feature.id())
            #if n_start_node > 1:
            #    self.dock.textEditLog.append("Bifurcation at end of: ")#+    feature[campo])
            if n_start_node > 1:
                #remove last n_start_node items from final_list                
                final_list[len(final_list)-n_start_node:len(final_list)] = []
                self.dock.textEditLog.append("Stopped at bifurcation!")
                break            
            #remove feature "0" from selection list
            selection_list.pop(0)
        #select features using final_list            
        layer.selectByIds(final_list)
        self.TrechosChained=final_list
        tot = self.getLength(layer)
        self.dock.textEditLog.append("")
        self.dock.textEditLog.append("N. of selected feature(s): " + str(tot[1]))
        self.dock.textEditLog.append("Length of selected feature(s): " + str(round(tot[0],3)))
        #zoom to selected feature if requested by ui
        if self.dock.checkZoomToSel.isChecked():
            mapCanvas = self.iface.mapCanvas()
            mapCanvas.zoomToSelected(layer)
        QApplication.restoreOverrideCursor()
            
    def call_Verifica(self):
#        qgis.utils.showPluginHelp()
        proj = QgsProject.instance()
        aForma='PIPES'
        ProjVar=proj.readEntry("QWater", aForma)[0]
        if ProjVar=='':
            msgTxt=QCoreApplication.translate('QWater','Undefined layer: {}').format(aForma)
            QMessageBox.warning(None,'QWater',msgTxt)
            return
        layer = proj.mapLayersByName(ProjVar)[0]
        LinesOK, nSplitted, nCreated = self.CheckPolylines(layer)
        if LinesOK:            
            if nSplitted > 0:
                msgTxt = self.tr("Splitted {} multipart feature(s) into {} "
                              "singlepart ones. ".format(nSplitted,
                                                        nSplitted +
                                                        nCreated))
            else:
                msgTxt = self.tr("No multipart features found! ")
        else:            
            msgTxt = self.tr("Multipart features found. Better fix it first! ")  
        
        self.dock.textEditLog.clear()
        
        AchouDuplic = self.VerificaPVMont_Duplicado(layer)
        if AchouDuplic:
            msgTxt += self.tr("Pipes with duplicated nodes ID found!")
        else:
            msgTxt += self.tr("No duplicated nodes ID found!")
        
        if LinesOK and (not AchouDuplic):
            msgNivel = Qgis.Info
        else:
            msgNivel = Qgis.Warning
        
        self.iface.messageBar().pushMessage("QWater",msgTxt,level=msgNivel,duration=10)

    # Funcao verifica e retorna verdadeiro se nao existirem multipartes ou se tiverem sido tratadas
    # indicando a quantidade de splitted e criadas
    # retorna Falso, 0 ,0 se existirem e nao forem tratadas
    def CheckPolylines(self, layer):
        for feature in layer.getFeatures():
            geom=feature.geometry()
            if geom.isMultipart():
                NroParts = len(list(geom.parts()))
                if NroParts>1:
                    layer.removeSelection()
                    layer.select(feature.id())
                    self.iface.mapCanvas().zoomToSelected(layer)
                    msgTxt=QCoreApplication.translate('QWater',u'Multipart feature with {:d} parts found!').format(NroParts)
                    resp=QMessageBox.question(None,'QWater',msgTxt+QCoreApplication.translate('QWater',u' Convert all features to single parts?'),QMessageBox.Yes, QMessageBox.No)
                    if resp==QMessageBox.Yes:
                        nSplitted, nCreated  = self.convertToSinglePart(layer)
                        return True, nSplitted, nCreated
                    else:
                        return False, 0, 0
        return True, 0, 0

    def convertToSinglePart(self, layer):
        n_split_feats = 0
        n_new_feats = 0        
        layer.beginEditCommand(self.tr('Split feature(s) parts'))
        # Iterate over all selected feature to find multipart features
        for feature in layer.getFeatures():
            geom = feature.geometry()
            # if feature geometry is multipart starts split processing
            if geom != None:
                if geom.isMultipart():
                    # isMultipart returns True even to singleparts elements when they are in Multipart layer
                    # so I needed to check number of parts
                    NroParts = len(list(geom.parts()))
                    if NroParts>1:
                        n_split_feats += 1
                        parts = geom.asGeometryCollection()
                        
                        # Convert part to multiType to prevent errors in Spatialite
                        for part in parts:
                            part.convertToMultiType()

                        #Convert list of attributes to dict
                        attributes = {i: v for i, v in enumerate(
                            feature.attributes())}

                        # from 2nd to last part create a new features using their
                        # single geometry and the attributes of the original feature
                        for i in range(1,len(parts)):
                            n_new_feats += 1
                            new_feat = QgsVectorLayerUtils.createFeature(layer,
                                                                         parts[i],
                                                                         attributes)
                            layer.addFeature(new_feat)
                        # update feature geometry to hold first part of geometry
                        # (this way one of the output features keeps the original Id)
                        feature.setGeometry(parts[0])
                        layer.updateFeature(feature)
        
        # End process and return the results
        if n_new_feats > 0:
            layer.endEditCommand()
        else:
            layer.destroyEditCommand()        
        
        return n_split_feats, n_new_feats + n_split_feats
        
    def tr(self, text):
        return QCoreApplication.translate("QWater", text)
    
    def clear(self):
        nroTrechos = len(self.TrechosChained)
        anterior = self.dock.spinColetor.value()
        self.dock.spinColetor.setValue(anterior+nroTrechos)
        self.TrechosChained=[]
        self.dock.textEditLog.clear()
        #self.dock.buttonSelectSourceId.click()
        layer=self.PegaPipeLayer()
        if layer!=False:
            layer.removeSelection()
        self.iface.mapCanvas().unsetMapTool(self.sourceIdEmitPoint)
        self.iface.mapCanvas().setMapTool(self.sourceIdEmitPoint)
        if not self.dock.buttonSelectSourceId.isChecked():
            self.dock.buttonSelectSourceId.click()
        QApplication.restoreOverrideCursor()

    def LimpaNomesColetores(self):
        vLayer=self.PegaPipeLayer()
        if vLayer==False:
            return
        if vLayer.selectedFeatureCount()==0:
            feicoes=vLayer.getFeatures()
        else:
            resp=QMessageBox.question(None,'QWater',QCoreApplication.translate('QWater','Clear pipes names?'),
                                      QMessageBox.Yes, QMessageBox.No)
            if resp==QMessageBox.Yes:
                feicoes=vLayer.selectedFeatures()
            else:
                feicoes=vLayer.getFeatures()
        vLayer.startEditing()
        campos=['DC_ID']#,'Coletor','Trecho','PVM','PVJ']
        for feicao in feicoes:
            for campo in campos:
                feicao[campo]=NULL
            vLayer.updateFeature(feicao)
        vLayer.triggerRepaint()
        self.iface.mapCanvas().refresh()

    def toggleSelectButton(self, button):
        selectButtons = [
            self.dock.buttonSelectSourceId
        ]
        for selectButton in selectButtons:
            if selectButton != button:
                if selectButton.isChecked():
                    selectButton.click()
    def getNodes(self, aFeat):
        aGeom = aFeat.geometry()
        if aGeom.isMultipart():
            return aGeom.asMultiPolyline()[0] #pega a primeira
        else:
            return aGeom.asPolyline()
        

