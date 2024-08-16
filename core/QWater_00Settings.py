from __future__ import absolute_import
from builtins import str
from builtins import range
#
# This file is part of QWater
#
# QWater_00Settings.py - Manage settings for projects
#
# Copyright 2017 - 2017 Jorge Almerio <jorgealmerio@yahoo.com.br>
#
# QWater is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2, or (at your option) any later version.
#
# QWater is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with program; see the file COPYING. If not,
# write to the Free Software Foundation, Inc., 59 Temple Place
# - Suite 330, Boston, MA 02111-1307, USA.
#
# QGIS 2.0.0 or better required to run this file
#
from pickle import *
import os,csv
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QLineEdit, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QCheckBox
from qgis.core import *
from qgis.gui import *
from .EpanetModel import *
from .QWater_Settings_dialog import QWater_SettingsDialog
import qgis

class QWaterSettingsDialog(QDialog):
    # Store all configuration data under this key
    SETTINGS = 'QWater'
    # Store auto length configuration under this key
    AUTO_LENGTH = 'autolength'
        # Store backdrop map configuration under this key
    WRITE_BACKDROP = 'writebackdrop'

    STRING_TRUE = '1'
    STRING_FALSE = '0'
    UNUSED_ITEM = 6
    UNUSED = 'Unused'

    def selectInpFile(self):
        prjfi = self.ui.inpFileLineEdit.text()
        f, __ = QFileDialog.getOpenFileName(caption=self.tr(u'Select Epanet INP File:'),
                                                 directory=prjfi,filter="Epanet INP File (*.inp *.INP);;All files (*.*)")
        if 0 < len(f):
            self.ui.inpFileLineEdit.setText(f)

    def getTemplate(self):
        project = QgsProject.instance()
        template = str(project.readEntry(self.SETTINGS, "templateinpfile")[0])
        if not template:
            template = str(project.readEntry("ghydraulics", "templateinpfile")[0])
        if os.path.isfile(template):
            return template
        templatedir = os.path.join(os.path.dirname(__file__), 'etc')
        templatepath = os.path.join(templatedir, template)
        if os.path.isfile(templatepath):
            return templatepath
        return os.path.join(templatedir, 'template_d-w_lps.inp')

    # True if length should be calculated automatically, otherwise false
    def getAutoLength(self):
        project = QgsProject.instance()
        return  self.STRING_TRUE == str(project.readEntry(self.SETTINGS, self.AUTO_LENGTH)[0])

        # True if backdrop map should be written, otherwise false
    def getWriteBackdrop(self):
        project = QgsProject.instance()
        return self.STRING_TRUE == str(project.readEntry(self.SETTINGS, self.WRITE_BACKDROP)[0])

    def ClearSettings(self):
        proj = QgsProject.instance()
        QWaterEntries=proj.entryList(self.SETTINGS, '')
        if QWaterEntries:
            proj.removeEntry(self.SETTINGS,"")
            MsgTxt=self.tr(u'The Plugin settings was removed from project!')
            self.iface.messageBar().pushMessage(self.SETTINGS, MsgTxt, duration=3)
            self.close()
        else:
            MsgTxt=self.tr(u'QWater settings NOT found in this project!')
            self.iface.messageBar().pushMessage(self.SETTINGS,MsgTxt, duration=3)
        #listaEntry = proj.readListEntry()

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate(self.SETTINGS, message)
    def __init__(self):
        QDialog.__init__(self)
        self.iface=qgis.utils.iface
        self.ui = QWater_SettingsDialog()
        self.ui.setupUi(self)
        #QObject.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accepted)
        self.ui.inpFilePushButton.clicked.connect(self.selectInpFile)
        self.ui.btnLimpaSettings.clicked.connect(self.ClearSettings)
        
        #Not working #QDialog.setWindowFlags(self.ui, Qt.CustomizeWindowHint | Qt.WindowMaximizeButtonHint | Qt.WindowContextHelpButtonHint | Qt.WindowMinimizeButtonHint)# | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.Window)
        
        #Conecta aos Botoes
        self.ui.btnImport.clicked.connect(self.ImportaTubos)
        self.ui.btnExport.clicked.connect(self.ExportaTubos)
        self.ui.btnFlow.clicked.connect(self.btnFlow_push)
        self.ui.btnDel.clicked.connect(self.btnDel_push)
        self.ui.btnIns.clicked.connect(self.btnIns_push)
        
                
        #Conecta Combobox Zones
        self.ui.CMBZONES.activated.connect(self.CMBZONES_Change)

        #Conecta CopyFlow buttons
        self.ui.btnCopyFlowIni.clicked.connect(self.btnCopyFlowIni_Click)
        self.ui.btnCopyFlowFim.clicked.connect(self.btnCopyFlowFim_Click)        
        
        #Conecta PopFields
        self.popLineEdits = [self.ui.Txt_POPINI, self.ui.Txt_POPFIM, self.ui.Txt_PERCAPTA, self.ui.Txt_K1_DIA, self.ui.Txt_K2_HORA, self.ui.Txt_COEF_ATEND]
        for LineEdit in self.popLineEdits:
            LineEdit.editingFinished.connect(self.calcFlowsByPop)            
        
    def btnFlow_push(self):
        frm = self.ui
        tableWidget=frm.tableWidget
        cabecalho = self.LeCabecalho(tableWidget)
        
        #CheckFields
        campos=['Diameter','Roughness','Headloss']
        missingFields=[]
        for campo in campos:
            if not campo in cabecalho:
                missingFields.append(campo)      
        if missingFields:
            self.iface.messageBar().pushMessage(self.SETTINGS,'Missing fields: ['+''.join(missingFields)+']', level=Qgis.Warning, duration=3)
            return False

        #Check Max Flow field
        nroCols = tableWidget.columnCount()        
        maxFlowFld = 'Max Flow'
        if maxFlowFld not in cabecalho:
            tableWidget.insertColumn(nroCols)
            cabecalho.append(maxFlowFld)
            tableWidget.setHorizontalHeaderLabels(cabecalho)
        
        #get Columns Index
        diamIdx = cabecalho.index(campos[0])
        roughIdx = cabecalho.index(campos[1])
        headIdx = cabecalho.index(campos[2])
        maxFlowIdx = cabecalho.index(maxFlowFld)
        
        #import GhyEconomicDiameter class to get colebrook function
        from .ghyeconomicdiameter import GhyEconomicDiameter as ghyDiam        
        
        #iterate throught table widget rows
        for row in range(tableWidget.rowCount()):
            d=float(eval(tableWidget.item(row, diamIdx).text()))            
            e=float(eval(tableWidget.item(row, roughIdx).text()))
            j=float(eval(tableWidget.item(row, headIdx).text()))
            # arguments 'Flow','Diameter' not used, it is only for instance creation
            
            vazao = ghyDiam('Flow','Diameter', []).ColebrookVazao(j,d,e)
            
            item = QTableWidgetItem('{0:.3f}'.format(vazao)) #.decode('utf8')
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            tableWidget.setItem(row, maxFlowIdx, item)
        
        #self.iface.messageBar().pushMessage(self.SETTINGS,'Max Flow Button clicked', duration=3)
    def btnCopyFlowIni_Click(self):
        frm = self.ui
        Flow = frm.edtFlowIni.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(Flow)
    def btnCopyFlowFim_Click(self):
        frm = self.ui
        Flow = frm.edtFlowFim.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(Flow)
    def CMBZONES_Change(self, indice):        
        #print('changed signal indice={} valor={}'.format(indice, unicode(self.ui.CMBZONES.currentText())))
        #Enable pop fields if Hydraulic Zone is unset (indice<=0)
        if indice<=0:
            self.enablePopFields(True)
        else:
            self.enablePopFields(False)
    def enablePopFields(self, enable):
        popLineEdits = self.popLineEdits
        if enable:
            cor = "color:#000000;"
            tipTxt=''
        else:
            cor = "color:#ff00ff;"
            tipTxt='Hydraulic Zones layer flow values used instead of this!'
        for LineEdit in popLineEdits:
            LineEdit.setStyleSheet(cor)# rgb(255, 0, 255);")
            LineEdit.setToolTip(tipTxt)        
        #LineEdit.setEnabled(enable)
    def calcFlowsByPop(self):
        frm = self.ui
        PopIni = float(frm.Txt_POPINI.text())
        PopFim = float(frm.Txt_POPFIM.text())
        perCap = float(frm.Txt_PERCAPTA.text())
        k1 = float(frm.Txt_K1_DIA.text())
        k2 = float(frm.Txt_K2_HORA.text())
        att = float(frm.Txt_COEF_ATEND.text())
        flowIni = PopIni*perCap*k1*k2*att/86400
        flowFim = PopFim*perCap*k1*k2*att/86400
        frm.edtFlowIni.setText('{0:.3f}'.format(flowIni))
        frm.edtFlowFim.setText('{0:.3f}'.format(flowFim))
    def btnDel_push(self):
        tableWidget=self.ui.tableWidget
        tableWidget.removeRow(tableWidget.currentRow())
    def btnIns_push(self):
        tableWidget=self.ui.tableWidget
        tableWidget.insertRow(tableWidget.currentRow()+1)
        cell_widget = QWidget()
        lay_out = QHBoxLayout(cell_widget)
        chk_bx = QCheckBox()
        chk_bx.setCheckState(QtCore.Qt.Checked)
        lay_out.addWidget(chk_bx)
        lay_out.setAlignment(Qt.AlignCenter)
        lay_out.setContentsMargins(0,0,0,0)
        cell_widget.setLayout(lay_out)
        tableWidget.setCellWidget(tableWidget.currentRow()+1, 0, cell_widget)
    def ImportaTubos(self):
        #MsgTxt=self.tr(u'Importa tubos!')
        #QMessageBox.information(None,self.SETTINGS,MsgTxt)
        self.table=self.ui.tableWidget
        prjfi = os.path.splitext(QgsProject.instance().fileName())[0]+'.csv'
        path, __ = QFileDialog.getOpenFileName(
                self, 'Open File', prjfi, 'CSV(*.csv)')
        if path:
            if os.path.exists(path):
                with open(str(path), 'r', newline='') as stream:
                    self.table.setRowCount(0)
                    self.table.setColumnCount(0)
                    for rowdata in csv.reader(stream):
                        self.table.setColumnCount(len(rowdata))
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        if row<1:                            
                            self.table.setHorizontalHeaderLabels(rowdata)
                        else:
                            for column, data in enumerate(rowdata):
                                valor=data#.decode('utf8')
                                if column==0:
                                    cell_widget = QWidget()
                                    lay_out = QHBoxLayout(cell_widget)
                                    chk_bx = QCheckBox()
                                    if valor in [1,'1','t','True']:
                                        chk_bx.setCheckState(QtCore.Qt.Checked)
                                    else:
                                        chk_bx.setCheckState(QtCore.Qt.Unchecked)
                                    lay_out.addWidget(chk_bx)
                                    lay_out.setAlignment(Qt.AlignCenter)
                                    lay_out.setContentsMargins(0,0,0,0)
                                    cell_widget.setLayout(lay_out)
                                    self.table.setCellWidget(row, 0, cell_widget)
                                else:
                                    item = QTableWidgetItem(data) #.decode('utf8')
                                    item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                                    self.table.setItem(row, column, item)
                    #self.table.setHorizontalHeaderLabels(['On','DN','Diameter','Roughness','Pressure','Referencia'])
                    #for i in range(1,4):
                    #    self.table.resizeColumnToContents(i)
                    self.table.removeRow(0) #Remove a primeira linha em branco auxiliar para inserir o cabecalho
                    self.table.resizeColumnsToContents()#Para ajustar todas as colunas de vez
    def LeCabecalho(self, tblWid):
        header=[]
        for column in range(tblWid.columnCount()):
            header.append(tblWid.horizontalHeaderItem(column).text())
        return header
    def ExportaTubos(self):
        prjfi = os.path.splitext(QgsProject.instance().fileName())[0]+'.csv'
        path, __ = QFileDialog.getSaveFileName(
                self, 'Save File', prjfi, 'CSV(*.csv)')
        self.table=self.ui.tableWidget
        if path:
            with open(str(path), 'w', newline='') as stream:
                writer = csv.writer(stream)
                #grava cabecalho
                writer.writerow(self.LeCabecalho(self.table))
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if column==0:
                            cell_widget = self.table.cellWidget(row,column).findChild(type(QCheckBox()))
                            if cell_widget.isChecked():#QTableWidget.item(row,column).checkState()==QtCore.Qt.Checked:
                                rowdata.append('1')
                            else:
                                rowdata.append('0')
                        else:
                            if item is not None:
                                rowdata.append(str(item.text())) #.encode('utf8')
                            else:
                                rowdata.append('')
                    writer.writerow(rowdata)