# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWater_04Static_Head
                                 A QGIS plugin
 
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
from __future__ import absolute_import
from builtins import object
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from qgis.utils import *
import os.path
import os
import math
from .EpanetModel import *
from .QWater_00Settings import *
from .QWater_Settings_dialog import QWater_SettingsDialog
from .GHydraulicsInpReader import *
from .GHydraulicsInpWriter import *
from .GHydraulicsModelRunner import *


import qgis

from os.path import join
from .QWater_00Common import *

ClassName='QWater_04Static_Head'
staticHeadfld = 'STATIC_HEA'
class QWater_04Static_Head(object):
    def __init__(self, iface):
        global ClassName
        self.iface = iface
        self.common=QWater_00Common() 
        self.dlg = QWaterSettingsDialog()
    
    def tr(self, Texto):
        return QCoreApplication.translate(ClassName,Texto)
    
    def warning(self, message, nivel=Qgis.Warning):
        self.iface.messageBar().pushMessage(ClassName, message, level=nivel, duration=4)
        
    def nz(self, Valor):
        global TemCTNula
        #function to treat Null values
        if Valor==NULL:
            TemCTNula=True
            return 0
        else:
            return Valor
    def StaticHead_calculate(self):        
        #proj = QgsProject.instance()
        layer = self.common.PegaQWaterLayer('JUNCTIONS')
        if not layer:
            self.warning(self.tr("No Junction layer!"))
            return
        if self.check_isEditing():
            self.warning(self.tr("Stop Qwater layer(s) editing first!"))
            return
        
        #Check if field exists
        fldName = 'DEMAND'
        field_index = layer.fields().indexFromName(fldName)
        if field_index == -1:
            self.warning(self.tr('Field {} not found!').format(fldName))
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        #Colocar Demand zero em todos os nós
        layer.startEditing()
        for feat in layer.getFeatures():
            feat[fldName]=0
            layer.updateFeature(feat)
        
        #Roda a simulação e grava os resultados em um dictionary
        junctionResults0 = self.RunEpanet()
        
        #rollback layer edits from simulation
        self.rollBack_results()
        
        if junctionResults0:        
            #Check and create field fldName
            fldName = staticHeadfld
            field_index = layer.fields().indexFromName(fldName)
            
            layer.startEditing()
            if field_index == -1:
                #if field does not exist create it
                layer.addAttribute(QgsField(fldName, QVariant.Double,'Real', len=15, prec=2))
                layer.updateFields()
                field_index = layer.fields().indexFromName(fldName)
            
            #grava os resultados no campo novo            
            for feat in layer.getFeatures():
                dcid = feat["DC_ID"]
                feat[fldName]=junctionResults0[dcid]
                layer.updateFeature(feat)
            
            self.selectStyle(layer, 'Static Pressure')
            
            aviso=self.tr("Static Head Calculated!")
            self.warning( aviso, nivel=Qgis.Info)
        else:
            aviso=self.tr("Simulation returned no results!")
            self.warning(aviso)
        
        QApplication.restoreOverrideCursor()
    
    def selectStyle(self, layer, styleName):
        # muda o estilo para fittings
        style_manager = layer.styleManager()

        # read valid style from layer
        style = QgsMapLayerStyle()
        style.readFromLayer(layer)
        
        style_manager.setCurrentStyle(styleName)   
    
    def rollBack_results(self):
        proj = QgsProject.instance()
        plugName = self.common.SETTINGS
        QWaterEntries=proj.entryList(plugName, '')
        for secao in EpanetModel.GIS_SECTIONS:
            if secao in QWaterEntries:
                lyrName=proj.readEntry(plugName, secao, "")[0]
                layerEntry=proj.mapLayersByName(lyrName)                
                if layerEntry:
                    layer = layerEntry[0]
                    if layer.isEditable():
                        layer.rollBack()
                    
    def check_isEditing(self):
        proj = QgsProject.instance()
        plugName = self.common.SETTINGS
        QWaterEntries=proj.entryList(plugName, '')
        for secao in EpanetModel.GIS_SECTIONS:
            if secao in QWaterEntries:
                lyrName=proj.readEntry(plugName, secao, "")[0]
                layerEntry=proj.mapLayersByName(lyrName)
                if layerEntry: 
                    layer = layerEntry[0]
                    if layer.isEditable():
                        return True
        return False

    #Read specific epanet results
    def readResults(self, Section, ResultColumn, runner):
        # loop over features
        layer = self.common.PegaQWaterLayer(Section)
        iter = layer.getFeatures()
        ID_fld = GHydraulicsModel.ID_FIELD
        step=0
        Results={} #Dictionary of junctions or pipes with IDs and specific results, i.g.: {DC_ID: RESULT_PRE}
        for feature in iter:
            dcid=feature[ID_fld]
            if Section=='JUNCTIONS':
                results = runner.e.getNodeResult(step, dcid)
            else:
                results = runner.e.getLinkResult(step, dcid)
            Results[dcid]=results[ResultColumn]
        return Results
    
    def RunEpanet(self):
        dlg = self.dlg #self.dlg #GHydraulicsSettingsDialog()
        template = dlg.getTemplate()
        
        inp = GHydraulicsInpReader(template)
        inpunits = inp.getValue('OPTIONS', 'Units').upper()
        if inpunits != EpanetModel.LPS:
            self.warning(self.tr('Requires "LPS" flow units instead of "{}". Please change the template INP file').format(inpunits))
            return
        
        # Get a temporary file
        t = tempfile.mkstemp(suffix='.inp')
        os.close(t[0])        
        erros = ['erros','erro']
        warnings = ['warnings','warnings']
        try:
            writer = GHydraulicsInpWriter(template, self.iface)
            writer.write(t[1], False, silent=True)
        except GHydraulicsException as e:
            self.warning(self.tr('Saving an INP file failed :') + str(e))
            return None
        try:
            runner = GHydraulicsModelRunner()
            output, report, steps = runner.run(t[1])
            
            #if has errors or warnings
            if any(x in output for x in erros):
                msgTxt = self.tr('QWater can NOT Calculate "STATIC HEAD" while there are errors or warnings!')
                dlg = GHydraulicsResultDialog(runner.setStep)                
                dlg.ui.textOutput.setText(output+msgTxt)
                self.StyleOutput(output,dlg.ui)
                dlg.ui.textReport.setText(report+msgTxt)
                dlg.ui.comboStep.clear()
                dlg.ui.comboStep.addItems([str(x) for x in range(1, steps+1)])
                dlg.show()                
                result = dlg.exec_()
                return
            
            '''
            #if has warnings
            elif any(x in output for x in warnings):
                # Let user agree to the begin iteration even with warnings
                msgTxt = '\n\n QWater can try to Calculate Economic Diameters (Iterative way) while there are warnings, but may NOT converge!\n Click OK to continue at your own risk!'
            '''
            if any(x in output for x in erros):
                print('First run had warnings! Trying to Continue...')
            print("Reading simulation results...")
            runner.setStep(0) #Load simulation Step 1 (first step=0) to features, First Time
            junctionResults0 = self.readResults('JUNCTIONS', 'RESULT_HEA', runner) #Junction head results
            return junctionResults0
        except GHydraulicsException as e:
            self.warning(self.tr('Running a simulation failed :') + str(e))
            return None
            
        os.unlink(t[1])
        layer.triggerRepaint()