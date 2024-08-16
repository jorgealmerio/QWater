# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWater_00Common
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
from builtins import object
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.utils import *
import os.path
#        from qgis.gui import QgsMessageBar
ClassName='QWater_00Common'
class QWater_00Common(object):
    # Store all configuration data under this key
    SETTINGS = 'QWater'
    def tr(self, Texto):
        return QCoreApplication.translate(ClassName,Texto)
    def CompRealGeom(self,vLayer):
        totAcum=0
        geoAcum=0
        for feat in vLayer.getFeatures():
            ext=feat['LENGTH']
            geo=feat.geometry().length()
            if ext!= NULL:
                totAcum+=ext
            geoAcum+=geo
        return totAcum,geoAcum
    def startProgressBar(self, iniMsg):
        #iniMsg ="Disabling Snapping to Layer: "
        #iface=self.iface
        progressMessageBar = iface.messageBar().createMessage(self.SETTINGS,iniMsg)
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        #pass the progress bar to the message Bar
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar)
        return progress,progressMessageBar
    def PegaQWaterLayer(self, aForma, silent=False):
        proj = QgsProject.instance()
        #aForma='PIPES'
        ProjVar=proj.readEntry(self.SETTINGS, aForma)[0]
        if ProjVar=='':
            msgTxt=self.tr('Undefined Layer: ') +aForma
            if not silent:
                iface.messageBar().pushMessage("QWater", msgTxt, level=Qgis.Warning, duration=10)
            return False
        LayerLst=proj.mapLayersByName(ProjVar)
        if LayerLst:
            layer = proj.mapLayersByName(ProjVar)[0]
            return layer
        else:
            msgTxt=aForma+'='+ProjVar+self.tr(' (Layer not found)')
            if not silent:
                iface.messageBar().pushMessage("QWater:", msgTxt, level=Qgis.Warning, duration=10)
            return False
    
    def getUser_iterFeat(self):
        layer = self.PegaQWaterLayer('PIPES')
        if layer.selectedFeatureCount()==0:
            iterFeat=layer.getFeatures()
        else:
            resp=QMessageBox.question(None,'QWater',QCoreApplication.translate('QWater','Size Diameters only for selected features?'),
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if resp==QMessageBox.Cancel:
                iface.messageBar().pushMessage("QWater",'QWater: Operation cancelled. Nothing done!',level=Qgis.Info, duration=10)
                iterFeat=None
            else:
                if resp==QMessageBox.Yes:
                    iterFeat=layer.selectedFeatures()
                else:
                    iterFeat=layer.getFeatures()
        return list(iterFeat)