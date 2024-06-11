# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWater_03Export
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
from PyQt5.QtWidgets import QFileDialog
from qgis.utils import *
import os.path
import os
import math

import qgis
from numpy import insert
from os.path import join
from .QWater_03Export_dialog import dxfExport_Dialog
from .QWater_00Common import *
from .addon.waterNet.QWaterNet import QWaterNet_addon
#from formatter import NullWriter

ClassName='QWater_03Export'
class QWater_03Export(object):
    def __init__(self):
        global ClassName
        self.Common=QWater_00Common()

        # Create the dialog and keep reference
        self.dlg = dxfExport_Dialog()
        self.dlg.btnBrowse.clicked.connect(self.LoadFileName)        
        
    def ImportDxf_Lib(self):
        try:
            from .addon import ezdxf as dxf
        except ImportError:
            self.dirname, filename = os.path.split(os.path.abspath(__file__))
            addonPath = os.path.join(self.dirname,'addon')
            sys.path.append(addonPath)
            import ezdxf as dxf
            QgsMessageLog.logMessage('ezdxf imported, but PATH variable had to be changed',ClassName)
        self.dxf=dxf
        
    def tr(self, Texto):
        return QCoreApplication.translate(ClassName,Texto)
    def nz(self, Valor):
        global TemCTNula
        #function to treat Null values
        if Valor==NULL:
            TemCTNula=True
            return 0
        else:
            return Valor
    def run(self):        
        self.ImportDxf_Lib()
        noth=['',' ','.dxf']
        if self.dlg.txtFile.text() in noth:
            proj = QgsProject.instance()            
            prjfi = os.path.splitext(QgsProject.instance().fileName())[0]+'.dxf'
            self.dlg.txtFile.setText(prjfi)

        vLayer=self.Common.PegaQWaterLayer('PIPES')
        if vLayer==False:            
            aviso=self.tr(u'\'PIPES\' Layer undefined or not found!')
            iface.messageBar().pushMessage(ClassName, aviso, level=Qgis.Warning, duration=4)
            self.dlg.chkPipes.setChecked(False)
            self.dlg.chkPipes.setEnabled(False)
            #return False
        
        junctLayer=self.Common.PegaQWaterLayer('JUNCTIONS',silent=True)
        if junctLayer==False:
            self.dlg.chkFittings.setChecked(False)
            self.dlg.chkFittings.setEnabled(False)
        else:
            if not self.checkFittings(junctLayer):
                self.dlg.chkFittings.setChecked(False)
                self.dlg.chkFittings.setEnabled(False)
            else:
                self.dlg.chkFittings.setChecked(True)
                self.dlg.chkFittings.setEnabled(True)
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            dxfPath=self.dlg.txtFile.text()
            Invalidos=['',' ',None,NULL]
            if dxfPath in Invalidos:
                aviso=self.tr(u'Cancelled!')
                iface.messageBar().pushMessage(ClassName, aviso, level=Qgis.Info, duration=4)
                return
            dxf=self.dxf           
            
            # Open DXF template
            basepath = os.path.dirname(__file__)#os.path.realpath(
            filename=os.path.join(basepath, 'etc/QWater_template.dxf')
            drawing = dxf.readfile(filename)
            self.drawing=drawing
            
            # Try to Save the drawing before begin.
            try:
                drawing.saveas(dxfPath)
            except:
                WriteErr=self.tr("Can NOT write to file!")
                iface.messageBar().pushMessage(ClassName, WriteErr, level=Qgis.Warning, duration=4)
                return False 
            
            #Cria layers
            prefix=self.dlg.txtPrefix.text()
            self.criaLayers(drawing,prefix)
            
            #Add network to DXF if enabled
            if self.dlg.chkPipes.isChecked():
                self.criaRede(vLayer)
            
            #Add fittings to DXF if enabled
            if self.dlg.chkFittings.isChecked():
                self.criaFittings(junctLayer)            
            
            # Get the modelspace of the drawing.
            msp = drawing.modelspace()  
            #Zoom to extents
            from ezdxf import zoom
            zoom.extents(msp)            

            # Try to Save the drawing after edits.
            try:
                drawing.saveas(dxfPath)
            except:
                WriteErr=self.tr("Can NOT write to file!")
                iface.messageBar().pushMessage(ClassName, WriteErr, level=Qgis.Warning, duration=4)
                return False            
            
            aviso=self.tr("Saved to:") + dxfPath
            iface.messageBar().pushMessage(ClassName, aviso, level=Qgis.Info, duration=4)
    
    #Check if it has Fittings placed in water network
    def checkFittings(self, layer):
        resp = False
        fits = list(QWaterNet_addon.FITS_FLDS.keys())
        fitsVals = list(QWaterNet_addon.FITTINGS.values())
        
        field_name = fits[0]
        idx = layer.fields().indexFromName(field_name)
        if idx == -1:
            resp=False
        else: 
            resp=True
            values = set()
            for f in layer.getFeatures():
                valor=f[field_name]                
                values.add(valor)
            if any(x in values for x in fitsVals):
                resp=True
            else:
                resp=False
        return resp
        
    def LoadFileName(self):
        prjfi = self.dlg.txtFile.text()
        dxfPath, __ =QFileDialog.getSaveFileName(caption=self.tr(u'Save DXF as:'),
                                                 directory=prjfi,filter="AutoCAD DXF (*.dxf *.DXF)")
        if dxfPath:
            self.dlg.txtFile.setText(dxfPath)
    
    def criaFittings(self, layer):
        global ClassName

        drawing=self.drawing
        
        # Get Scale Factor
        fatScale=self.dlg.spinScale.value()
        sc=fatScale/2000.        
        
        # Get the modelspace of the drawing.
        msp = drawing.modelspace()        
        
        # Import TextEntityAlignment
        from ezdxf.enums import TextEntityAlignment
        
        fits = list(QWaterNet_addon.FITS_FLDS.keys())
        fitsVals = list(QWaterNet_addon.FITTINGS.values())
        
        lyr='PEÇAS REDE'
        
        fitField = fits[0]
        rotField = fits[1]
        dn1Field = fits[2]
        dn2Field = fits[3]
        for feat in layer.getFeatures():
            blkName = feat[fitField]
            if blkName in fitsVals:
                geom=feat.geometry()
                pos=geom.asPoint()
                rot = self.nz(feat[rotField])
                #rotation is negative because Autocad use counter-clockwise refence
                blockref = msp.add_blockref(blkName, pos, dxfattribs={'color':256,'layer':lyr,                                             
                                        'rotation': -rot}).set_scale(sc*2)
                
                #Add fitting label
                #texto='c90x50' #Replace by fitting label function
                texto=self.criaFitting_Label(feat[fitField], feat[dn1Field], feat[dn2Field])
                succes = geom.translate(1, 2.5*sc)
                posUp = geom.asPoint()
                msp.add_text(texto,
                            height=4.8*sc,
                            dxfattribs={'rotation':0,'style':'ROMANS','color':256, 'layer':lyr}).set_placement(posUp,align=TextEntityAlignment.BOTTOM_LEFT)
    
    def criaFitting_Label(self,fitting, dn1, dn2):
        resp = fitting.upper()
        if dn1 > 50:
            resp = resp + 'x{}'.format(dn1)
            if dn2 not in [dn1, NULL]:
                resp = resp + ('x{}'.format(dn2) or '')
        return resp
        
    def criaRede(self, vLayer):
        global ClassName

        drawing=self.drawing

        
        try:
            drawing.styles.new('ROMANS',{'font':'romans.shx'})
        except:
            pass        
        
        # Get Scale Factor
        fatScale=self.dlg.spinScale.value()
        sc=fatScale/2000.        
        
        # Get the modelspace of the drawing.
        msp = drawing.modelspace()        

        for feat in vLayer.getFeatures():
            geom=feat.geometry()
            if geom.isMultipart():
                polilinha=geom.asMultiPolyline()[0] #Pega apenas a primeira parte das multipartes
            else:
                polilinha=geom.asPolyline()         

            dn = feat["DN"] #or 'x'
            
            #UI Dialog 
            #<widget class="QLineEdit" name="txtPrefix">
            #<string>REDE PROJ DN </string>
            #prefix='REDE PROJ DN '
            prefix=self.dlg.txtPrefix.text()
            lyr=prefix+'{}'.format(dn)
            line = msp.add_lwpolyline(polilinha, dxfattribs={'color':256, 'layer':lyr})            
        
            #Add Pipe ID text above pipe line
            from ezdxf.enums import TextEntityAlignment

            singGeom = geom
            singGeom.convertToSingleType()
            midDist = singGeom.length()/2            
            v1= singGeom.interpolate(midDist-0.1).asPoint()
            v2= singGeom.interpolate(midDist+0.1).asPoint()
            
            #nroVerts = len(polilinha)
            #midVert=nroVerts//2
            #v1=polilinha[midVert-1]
            #v2=polilinha[midVert]            
            
            #Add Pipe data (diameter-length) text above polyline                
            lyr='TEXTO'
            ext=self.nz(feat["LENGTH"])
            dn=self.nz(dn)
            if dn>50:
                texto='DN{:.0f}-{:.0f}m'.format(dn,ext)
            else:
                texto='{:.0f}m'.format(ext)
            
            # Check if is a short reach (>0 to temporary bypass)
            if feat['LENGTH']>0*sc:
                pos,rot=self.textIns(v1,v2,-1.25*sc)
                #texto='DN{:.0f}'.format(dn)
                msp.add_text(texto,
                            height=4.8*sc,
                            dxfattribs={'rotation':rot,'style':'ROMANS','color':256, 'layer':lyr}).set_placement(pos,align=TextEntityAlignment.BOTTOM_CENTER)                            
            else:
                pos,rot=self.textIns(v1,v2,0)
                blockref = msp.add_blockref('tr_curto', pos, dxfattribs={'color':256,'layer':lyr,                                             
                                        'rotation': 0}).set_scale(sc*2)                
                values = {
                            'DIST-DIAM-DECLV': texto
                        }
                blockref.add_auto_attribs(values)

    def criaLayers(self,drawing,prefix):
        #[Layer,Color]
        #[['AUX',241],['LIDER',2],['NO',3],['NUMERO',3],['NUMPV',3],['PV',3],['REDE',172],['SETA',172],['TEXTO',3],['TEXTOPVS',7]]
        
        #Add Texto layer separately
        drawing.layers.new('TEXTO', dxfattribs={'color': 3})        
        
        dxfLayers=[['50',240],
                   ['75',104],
                   ['100',170],
                   ['150',(101,137,246)],
                   ['200',32],
                   ['250',(134,36,255)]]
        for lyr,aColor in dxfLayers:
            NomeLyr=prefix+lyr
            #drawing.layers.new(NomeLyr, dxfattribs={'color': aColor})
            if isinstance(aColor, int):
                drawing.layers.add(name=NomeLyr, color=aColor)
            else:
                newLyr = drawing.layers.add(name=NomeLyr)
                newLyr.rgb=aColor
            
    def textIns(self,v1,v2,offset):
        azim=v1.azimuth(v2)
        if azim<0:
            azim+=360
        rot=90.-azim
        if 180<=azim<360:
            rot-=180
        pos=self.mid(v1,v2, offset, azim)
        return pos,rot
    def mid(self, pt1, pt2, offset, azim):
       if 180<=azim<360:
            sign=-1*math.copysign(1,offset)
       else:
            sign=1*math.copysign(1,offset)
       mx = (pt1.x() + pt2.x())/2
       my = (pt1.y() + pt2.y())/2
       Len = math.sqrt(pt1.sqrDist(pt2)) 
       x=mx+sign*abs(offset)*(pt2.y()-pt1.y())/Len
       y=my+sign*abs(offset)*(pt1.x()-pt2.x())/Len
       return QgsPointXY(x,y)
    def PtoAlong(self,pt1,pt2,Dist):
       Len = math.sqrt(pt1.sqrDist(pt2)) 
       x=pt1.x()+Dist/Len*(pt2.x()-pt1.x())
       y=pt1.y()+Dist/Len*(pt2.y()-pt1.y())
       return QgsPointXY(x,y)
    #Cria um ponto perpendicular ao segmento e distante em relacao ao pt1 em offset
    def PtoPerp(self,pt1,pt2,Offset):
       Len = math.sqrt(pt1.sqrDist(pt2)) 
       x=pt1.x()+Offset/Len*(pt2.y()-pt1.y())
       y=pt1.y()+Offset/Len*(pt1.x()-pt2.x())
       return QgsPointXY(x,y)
