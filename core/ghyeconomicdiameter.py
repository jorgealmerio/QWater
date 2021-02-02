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
from qgis.PyQt.QtWidgets import QMessageBox
import sys
import math
#import operator
from .GHydraulicsException import *
from qgis.utils import iface

class GhyEconomicDiameter(object):
    SETTINGS ="QWater"
    flofieldname = "RESULT_FLO"
    diafieldname = "DIAMETER"
    roufieldname = "ROUGHNESS"
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
    #Calcula a vazao em L/s pela formulal de colebrook 
    #a partir da perda unitaria m/km, diametro em mm, rugosidade em mm, viscosidade em m2/s
    def ColebrookVazao(self, j_mkm, D_mm, e_mm=1, v=0.000001):
        g=9.81
        j=j_mkm/1000 #convert to m/m
        D=D_mm/1000 #convert to m
        e=e_mm/1000 #convert to m
        Vazao = -(math.pi / math.sqrt(2)) * math.log10(0.27 * e / D + 1.78 * v / (D * math.sqrt(g * D * j))) * D ** 2 * math.sqrt(g * D * j)
        return Vazao*1000 #convert to L/s
    def getFlows(self, tubos): #return to dicts: flowsXdiam and flowsXroughness
        #CheckFields
        campos=['On','Diameter','Roughness','Headloss']
        colIdx={}
        cabecalho=tubos[0]
        for campo in campos:
            if not campo in cabecalho:
                raise GHydraulicsException('ERROR: Unable to locate the "'+campo+'" field')
            colIdx[campo]=cabecalho.index(campo)            
        
        flows={}
        roughs={}
        nroLins = len(tubos) #exclude header
        for linha in range(1,nroLins):
            On=float(tubos[linha][colIdx['On']])
            if On==1:
                j=float(eval(tubos[linha][colIdx['Headloss']]))
                d=float(eval(tubos[linha][colIdx['Diameter']]))
                e=float(eval(tubos[linha][colIdx['Roughness']]))
                vazao=self.ColebrookVazao(j,d,e)
                flows[vazao]=d
                roughs[d]=e
        return flows, roughs
        #flowsOrdered = sorted(flows.items(),key=lambda kv:kv[0])
    def commitEconomicDiametersForLayer(self, vlayer):
        feature = QgsFeature()
        provider = vlayer.dataProvider()
        allAttrs = provider.attributeIndexes()

        # Locate fields
        diafieldidx = provider.fieldNameIndex(self.diafieldname)
        flowfieldidx = provider.fieldNameIndex(self.flofieldname)
        roufieldidx = provider.fieldNameIndex(self.roufieldname)

        if -1 == diafieldidx:
            raise GHydraulicsException('ERROR: Unable to locate the "'+self.diafieldname+'" field')
        if -1 == flowfieldidx:
            raise GHydraulicsException('ERROR: Unable to locate the "'+self.flofieldname+'" field')
        if -1 == roufieldidx:
            raise GHydraulicsException('ERROR: Unable to locate the "'+self.roufieldname+'" field')
            
        #Carrega Tubos 
        proj = QgsProject.instance()
        tubosMat=proj.readEntry(self.SETTINGS, "TUBOS_MAT","0")[0]            
        if tubosMat=='0':
            raise GHydraulicsException('ERROR: Please, Define Pipes on settings dialog First!')
            #tubos=QWaterModel.TUBOS_MAT
        else:
            tubos=eval(tubosMat)
            if not isinstance(tubos[0][0], str):
                raise GHydraulicsException('ERROR: Incorrect Pipes definition!. Please, Define Pipes on settings dialog First!')
        
        tubosFlow, tubosRough = self.getFlows(tubos)
        #raise GHydraulicsException('TESTE: Interrommpido!')
        
        self.diceconomic=tubosFlow
        economicflows = list(self.diceconomic.keys())
        economicflows.sort()

        dicattributechanges = {}

        if vlayer.selectedFeatureCount()==0:
            iter=vlayer.getFeatures()
        else:
            '''
            msgBox = QMessageBox()
            msgBox.setWindowTitle('QWater')
            msgBox.setInformativeText('Diameter size only for selected features?')
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Yes)
            resp=msgBox.exec_()
            '''
            resp=QMessageBox.question(None,'QWater',QCoreApplication.translate('QWater','Size Diameters only for selected features?'),
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel) #QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel)
            if resp==QMessageBox.Cancel:
                raise GHydraulicsException('QWater: Operation cancelled. Nothing done!')
            else:
                if resp==QMessageBox.Yes:
                    iter=vlayer.selectedFeatures()
                else:
                    iter=vlayer.getFeatures()        
        
        # Loop over selected or all features depend on last user option
        LowDiam=False
        for feature in iter:
            # Fetch result_flow attribute
            attrs = feature.attributes()
            flow = abs(attrs[flowfieldidx]) #Almerio: acrescentei a funcao 'abs' aqui para trazer o valor absoluto da vazao
            # Look up the economic diameter from the dictionary
            biggerflow = economicflows[-1] #pega o ultimo/maior valor
            for economicflow in economicflows:
                if economicflow > flow:
                    biggerflow = economicflow
                    break
            economicdiameter = self.diceconomic[biggerflow]
            # Indicate when dictionary is not valid any more
            if flow > biggerflow:
                #economicdiameter = 9999
                LowDiam=True
            vlayer.changeAttributeValue(feature.id(), diafieldidx ,economicdiameter) # modifica o diametro
            vlayer.changeAttributeValue(feature.id(), roufieldidx ,tubosRough[economicdiameter])#modifica a rugosidade
        iface.mapCanvas().refreshAllLayers()
        if LowDiam:
            MsgTxt='Pipes with insufficient diameter found! Please, insert bigger diameters Pipes on settings dialog!'
            iface.messageBar().pushMessage(self.SETTINGS,MsgTxt, level= Qgis.Warning, duration=0)
        
