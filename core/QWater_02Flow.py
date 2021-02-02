# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWater_02Flow
                                 A QGIS plugin
 Plugin for Water network design
                              -------------------
        begin                : 2016-03-15
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Jorge Almerio
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
from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.utils import *
import os.path
import processing
from .QWater_00Common import *
#        from qgis.gui import QgsMessageBar

class QWater_02Flow(object):
    # Store all configuration data under this key
    common=QWater_00Common()
    SETTINGS = common.SETTINGS
    progress = None
    progressMBar = None
    cont = 0
    nroNos = 0
    NoDemNodes=[]#self.ListNoDemandNodes()
    LstNetwork=[]#self.ListNetwork()
    SrcNodes = []#self.ListSourcesNodes()
    interPipes = []#Pipes that connects Hydraulic Zones (Crossed by Zone boundaries)
    fieldDemPto_idx= None
    def CalcFlow(self):
        '''MsgTxt=self.tr(u'Calc Vazao!')
        QMessageBox.information(None,self.SETTINGS,MsgTxt)'''
        proj = QgsProject.instance()
        PipesVar=proj.readEntry(self.SETTINGS, 'PIPES')[0]
        NodesVar=proj.readEntry(self.SETTINGS, 'JUNCTIONS')[0]
        
        if PipesVar!='' and NodesVar!='':
            PipesLayer=proj.mapLayersByName(PipesVar)[0]
            NodesLayer=proj.mapLayersByName(NodesVar)[0]
            ZonesVar=proj.readEntry(self.SETTINGS, 'ZONES')[0]
            
            self.NoDemNodes=self.ListNoDemandNodes()
            self.LstNetwork=self.ListNetwork()
            self.SrcNodes = self.ListSourcesNodes()
            self.fieldDemPto_idx = NodesLayer.fields().lookupField('DEMAND_PTO')
            self.nroNos=NodesLayer.featureCount()
            self.cont = 0
            #if Zones layer is undefined calculate using global population settings
            if ZonesVar=='':
                self.progress, self.progressMBar=self.common.startProgressBar('Starting Flow calcution...')
                self.interPipes = []
                popfim=float(proj.readEntry(self.SETTINGS, 'POPFIM')[0])
                perCapt=float(proj.readEntry(self.SETTINGS, 'PERCAPTA')[0])
                k1=float(proj.readEntry(self.SETTINGS, 'K1_DIA')[0])
                k2=float(proj.readEntry(self.SETTINGS, 'K2_HORA')[0])
                coefAtend=float(proj.readEntry(self.SETTINGS, 'COEF_ATEND')[0])
                tot=self.CalcExt(PipesLayer.getFeatures())
                Qfim=popfim*perCapt*k1*k2*coefAtend/86400
                NodesLayer.startEditing()
                self.CalcFlowSub(Qfim, PipesLayer, NodesLayer, PipesLayer.getFeatures(), NodesLayer.getFeatures())
            else: # if Zones layer is defined calculate using Polygon Zones Demands               
                ZonesLayer=proj.mapLayersByName(ZonesVar)[0]
                self.progress, self.progressMBar=self.common.startProgressBar('Starting Flow calcution by Zones...')
                self.interPipes = self.ListInterPipes(PipesLayer, ZonesLayer)
                NodesLayer.startEditing()
                for zona in ZonesLayer.getFeatures():                    
                    ZonesLayer.selectByIds([zona.id()])
                    self.selectByLocation(NodesLayer,QgsProcessingFeatureSourceDefinition(ZonesLayer.id(),True),6)#6:within
                    #self.selectByLocation(PipesLayer,QgsProcessingFeatureSourceDefinition(NodesLayer.id(),True),4)#4:touch
                    pipesSel = self.selectByExpression(PipesLayer,NodesLayer.getSelectedFeatures())                    
                    QZone=zona['DEMAND'] or 0
                    Zone=zona['DC_ID'] or ''
                    self.CalcFlowSub(QZone, PipesLayer, NodesLayer, pipesSel, NodesLayer.getSelectedFeatures(),Zone)#PipesLayer.getSelectedFeatures()
                ZonesLayer.removeSelection()
            PipesLayer.removeSelection()
            NodesLayer.removeSelection()
            iface.messageBar().clearWidgets()
            msgTxt = QCoreApplication.translate('QWater','Flow sucessfully calculated at {} de {} Nodes!'.format(self.cont,self.nroNos))
            if self.cont < self.nroNos:
                msgTxt += QCoreApplication.translate('QWater',' Hydraulic Zones does not contain all nodes!')                
            iface.messageBar().pushMessage(self.SETTINGS, msgTxt, level=Qgis.Info, duration=0)
        else:
            self.warning('Pipes or Junctions Layers undefined!')
            
 
    #Subroutina para calculo da vazao
    def CalcFlowSub(self, QZone, PipesLayer, NodesLayer, PipesIter, NodesIter, Zone=''):
        tot=self.CalcExt(PipesIter)            
        #Vazao unitaria
        qUnit=QZone/tot
        logTxt = 'qUnit={:f}' 
        if Zone!='':
            logTxt+= ' (Zone {})'.format(Zone) 
        QgsMessageLog.logMessage(logTxt.format(qUnit), self.SETTINGS, Qgis.Info)        
        for node in NodesIter:
            self.cont+=1
            percent = (self.cont/float(self.nroNos)) * 100
            self.progress.setValue(percent)
            dc_id=node['DC_ID']
            txtZone = '' if Zone=='' else 'Zone: '+Zone
            self.progressMBar.setText(txtZone +' calculating Demand for Junction '+dc_id)

            #Filtro para pegar os tubos que chegam no noh (NODE2=dc_id)
            UpNodes=self.GetUpStreamNodes(dc_id,self.NoDemNodes,self.LstNetwork)
            UpNodes.append(dc_id) #Acrescenta o proprio no
            filterUp='"NODE2" in (\''+"\',\'".join(UpNodes)+'\')'
            
            #Filtro para pegar os tubos que saem do noh (NODE1=dc_id)
            DownNodes=self.GetDownStreamNodes(dc_id,self.NoDemNodes,self.LstNetwork)
            DownNodes.append(dc_id) #Acrescenta o proprio no
            filterDown='"NODE1" in (\''+"\',\'".join(DownNodes)+'\')'

            filter=filterUp + " or "+ filterDown

            request = QgsFeatureRequest()
            request.setFilterExpression(filter)# '"NODE2" =\''+dc_id+'\'' 
            iterator=PipesLayer.getFeatures( request )
            ext=0
            for tubo in iterator:
                #if pipe node1 is very upstream node adds full length
                if tubo['NODE1'] in self.SrcNodes:
                    ext+=tubo['LENGTH']
                else:
                    ext+=tubo['LENGTH']/2.
            #print 'ext=',ext,"qUnit",qUnit
            #Gets Point Demand from field and adds
            if self.fieldDemPto_idx>=0:
                DemPto = node['DEMAND_PTO'] or 0  # if Field has null replace with zero
            else:
                DemPto = 0
            node['DEMAND']=ext*qUnit+DemPto
            NodesLayer.updateFeature(node)   
    def selectByLocation(self, srcLayer, intLayer, Predicate=6):
        myresult = processing.run("native:selectbylocation", 
            {'INPUT': srcLayer, 
            'PREDICATE':Predicate, # 4:touch ; 6:are within; 7:cross
            'INTERSECT': intLayer, #for only selected feature use QgsProcessingFeatureSourceDefinition(intLayer,True)
            'METHOD':0}) #0: creating new selection
        return myresult['OUTPUT']
    
    #Retorna um Iterator
    def selectByExpression(self, PipesLayer, nodeIterator):
        lstNodes=[f['DC_ID'] for f in nodeIterator]
        
        #Filtro para pegar os tubos que chegam no noh (NODE2=dc_id)
        filterUp='"NODE2" in (\''+"\',\'".join(lstNodes)+'\')'
        
        #Filtro para pegar os tubos que saem do noh (NODE1=dc_id)
        filterDown='"NODE1" in (\''+"\',\'".join(lstNodes)+'\')'


        filter=filterUp + " or "+ filterDown

        request = QgsFeatureRequest()
        request.setFilterExpression(filter)# '"NODE2" =\''+dc_id+'\'' 
        iterator=PipesLayer.getFeatures( request )
        return iterator
        #ids = [i.id() for i in iterator]
        #PipesLayer.selectByIds(ids)
        
    def CalcExt(self,Iterator):
        totAcum=0
        for feat in Iterator:
            ext=feat['LENGTH']
            if ext!= NULL:
                if feat.id() in self.interPipes:
                    totAcum+=ext/2
                else:
                    totAcum+=ext
        return totAcum
    def ListInterPipes(self, pipesLyr, ZoneLyr):
        result=[]
        self.selectByLocation(pipesLyr, ZoneLyr, 7)
        for pipe in pipesLyr.getSelectedFeatures():
            result.append(pipe.id())
        return result
    def testeVazao(self):
        #QInputDialog.getText(qid, title, label, mode, default)
        text, ok = QInputDialog.getText(QInputDialog(), 'testeVazao', "No:", QLineEdit.Normal, "20")
        if ok:
            NoDemNodes=self.ListNoDemandNodes()
            LstNetwork=self.ListNetwork()
            UpNodes=self.GetUpStreamNodes(text,NoDemNodes,LstNetwork)
            DownNodes=self.GetDownStreamNodes(text,NoDemNodes,LstNetwork)
            # fix_print_with_import
            print("No=",text)
            # fix_print_with_import
            print("NoDemNodes=",NoDemNodes)
            # fix_print_with_import
            print("UpNodes=",UpNodes)
            # fix_print_with_import
            print("DownNodes=",DownNodes)
        else:
            self.warning('Cancelado!')
    #Recursive function to find all connected upstream No Demand nodes
    def GetUpStreamNodes(self,Node,NoDemNodes,LstNetwork):
        UpNodes=[row[1] for row in LstNetwork if (row[2]==Node) and (row[1] in NoDemNodes)]
        for upNode in UpNodes:
            UpNodes=UpNodes+self.GetUpStreamNodes(upNode,NoDemNodes,LstNetwork)
        return UpNodes
    #Recursive function to find all connected Downstream No Demand nodes
    def GetDownStreamNodes(self,Node,NoDemNodes,LstNetwork):
        DownNodes=[row[2] for row in LstNetwork if (row[1]==Node) and (row[2] in NoDemNodes)]
        for downNode in DownNodes:
            DownNodes=DownNodes+self.GetUpStreamNodes(downNode,NoDemNodes,LstNetwork)
        return DownNodes
    def ListNoDemandNodes(self): #Pumps, Valves, Tanks, Reservoirs
        proj = QgsProject.instance()
        noDemNodeTypes = ['RESERVOIRS', 'PUMPS', 'VALVES', 'TANKS']
        result=[]
        for noDemNodeType in noDemNodeTypes: 
            noDemNodeEntry=proj.readEntry(self.SETTINGS, noDemNodeType)[0]
            if noDemNodeEntry !='':
                NodesLayer=proj.mapLayersByName(noDemNodeEntry)[0]
                for node in NodesLayer.getFeatures():
                    result.append(node['DC_ID'])
        return result

    #List Reservoirs or tanks of very upstream Nodes (Sources)
    def ListSourcesNodes(self):
        proj = QgsProject.instance()
        ResTypes = ['RESERVOIRS', 'TANKS']
        result=reservs=[]
        for ResNodeType in ResTypes: 
            ResNodeEntry=proj.readEntry(self.SETTINGS, ResNodeType)[0]
            if ResNodeEntry !='':
                NodesLayer=proj.mapLayersByName(ResNodeEntry)[0]
                for node in NodesLayer.getFeatures():
                    reservs.append(node['DC_ID'])
        filter='"NODE2" not in (\''+"\',\'".join(reservs)+'\')'
        request = QgsFeatureRequest()
        request.setFilterExpression(filter)
        NodesVar=proj.readEntry(self.SETTINGS, 'JUNCTIONS')[0]
        NodesLayer=proj.mapLayersByName(NodesVar)[0]
        iterator=NodesLayer.getFeatures( request )
        for node in iterator:
            result.append(node['DC_ID'])
        return result
    #Return Topology network as Array [[DC_ID, NODE1, NODE2]]]
    def ListNetwork(self):
        proj = QgsProject.instance()
        PipesVar=proj.readEntry(self.SETTINGS, 'PIPES')[0]
        result=[]
        if PipesVar!='':
            PipesLayer=proj.mapLayersByName(PipesVar)[0]
            request = QgsFeatureRequest()
            iterator=PipesLayer.getFeatures()
            for tubo in iterator:
                result.append([tubo['DC_ID'],tubo['NODE1'],tubo['NODE2']])
            return result

    # Display warning message
    def warning(self, message):
        iface.messageBar().pushMessage(self.SETTINGS, message, level=Qgis.Warning, duration=4)