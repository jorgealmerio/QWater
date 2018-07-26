from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
# -*- coding: utf-8 -*-#
# This file is part of GHydraulics
#
# QWaterPlugin.py - The GHydraulics plugin
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

import os
import tempfile
from pickle import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QLineEdit, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QCheckBox
from qgis.core import *
from qgis.gui import *
from .ghyeconomicdiameter import *
from .EpanetModel import *
from .GHydraulicsModel import *
from .GHydraulicsModelChecker import *
from .GHydraulicsModelMaker import *
from .GHydraulicsModelRunner import *
from .GHydraulicsException import *
from .GHydraulicsInpWriter import *
from .GHydraulicsResultDialog import *
from .QWater_00Settings import *
from .QWater_Settings_dialog import QWater_SettingsDialog
from .QWater_00Model import *
from .QWater_02Flow import *
from .QWater_00Common import *
import configparser

# initialize Qt resources from file resouces.py
from . import resources

class QWaterPlugin(object):
    # Store settings in QGIS projects under this key
    SETTINGS ="QWater" #"ghydraulics""QWater"        

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        
        # Create the dialog (after translation) and keep reference
        self.dlg = QWaterSettingsDialog()#QWater_SettingsDialog()
        self.VazaoClasse=QWater_02Flow()
        self.common=QWater_00Common()
        try:
            pluginMetadata = configparser.ConfigParser()
            pluginMetadata.read(os.path.join(os.path.dirname(__file__), 'metadata.txt'))
            self.VERSION = pluginMetadata.get('general', 'version')
            '''
            from qgis.gui import QgsPluginManagerInterface
            plugInter = iface.pluginManagerInterface()
            #plugInter.showPluginManager()
            meta = plugInter.pluginMetadata(self.SETTINGS)#'QWater'
            self.VERSION = meta['version_installed']
            '''
            QgsMessageLog.logMessage('Version:'+self.VERSION, self.SETTINGS, Qgis.Info)
        except:
            self.VERSION = "3.0.0"

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate(QWaterPlugin.SETTINGS, message)
    def initGui(self):
        # create actions
        defIconPath=":/plugins/QWater/icons/qwater.svg"
        self.action = QAction(QIcon(defIconPath), "Calculate economic diameters", self.iface.mainWindow())
        self.action.setWhatsThis("Calculate economic pipe diameters based on flow data.")
        self.settingsAction = QAction(QIcon(':/plugins/QWater/icons/00settings.svg'), 'Settings', self.iface.mainWindow())
        self.makeModelAction = QAction(QIcon(':/plugins/QWater/icons/makemodel.svg'), 'Make EPANET Model', self.iface.mainWindow())
        self.fillFieldsAction = QAction(QIcon(':/plugins/QWater/icons/fields_fill.svg'), 'Fill up Fields', self.iface.mainWindow())
        self.writeInpAction = QAction(QIcon(':/plugins/QWater/icons/qwater.svg'), 'Write EPANET INP file', self.iface.mainWindow())
        self.runEpanetAction = QAction(QIcon(':/plugins/QWater/icons/run.svg'), 'Run EPANET simulation', self.iface.mainWindow())
        self.aboutAction = QAction(QIcon(":/plugins/QWater/icons/qwater.svg"), QCoreApplication.translate('GHydraulics', "&About"), self.iface.mainWindow())
        
        self.LoadStylesAction = QAction(QIcon(":/plugins/QWater/icons/style.svg"), "Load default styles", self.iface.mainWindow())
        self.vazaoAction = QAction(QIcon(':/plugins/QWater/icons/01vazao.svg'), self.tr('Calc Flow'), self.iface.mainWindow())
        
        self.action.triggered.connect(self.run)
        self.settingsAction.triggered.connect(self.showSettings)
        self.makeModelAction.triggered.connect(self.makeModel)
        self.fillFieldsAction.triggered.connect(self.fillFields)
        self.writeInpAction.triggered.connect(self.writeInpFile)
        self.runEpanetAction.triggered.connect(self.runEpanet)
        self.aboutAction.triggered.connect(self.about)
        
        Qwflow=QWater_02Flow().CalcFlow
        self.vazaoAction.triggered.connect(self.VazaoClasse.CalcFlow) #self.Vazao #ListNoDemandNodes #QWater_02Flow.CalcFlow
        
        self.LoadStylesAction.triggered.connect(self.LoadStyles)

        #Create toolbar
        self.toolbar = self.iface.addToolBar('&QWater')
        self.toolbar.setObjectName('&QWater')

        # add toolbar buttons
        self.toolbar.addAction(self.settingsAction)
        self.toolbar.addAction(self.makeModelAction)
        self.toolbar.addAction(self.fillFieldsAction)
        self.toolbar.addAction(self.vazaoAction)
        self.toolbar.addAction(self.runEpanetAction)

        #self.iface.addToolBarIcon(self.settingsAction)
        
        # add menu items
        self.iface.addPluginToMenu("&QWater", self.settingsAction)
        self.iface.addPluginToMenu('&QWater', self.LoadStylesAction)
        self.iface.addPluginToMenu('&QWater', self.makeModelAction)
        self.iface.addPluginToMenu('&QWater', self.fillFieldsAction)
        self.iface.addPluginToMenu('&QWater', self.vazaoAction)
        self.iface.addPluginToMenu("&QWater", self.writeInpAction)
        self.iface.addPluginToMenu('&QWater', self.runEpanetAction)
        self.iface.addPluginToMenu("&QWater", self.action)

        # Projects submenu
        self.project_menu = QMenu('&Projects')

        self.newProjectAction = QAction(self.iface.actionNewProject().icon(), 'New Project', self.iface.mainWindow())
        self.newProjectAction.triggered.connect(self.newProject)
        self.project_menu.addAction(self.newProjectAction)

        self.sampleDwCmdAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), 'Sample Darcy-Weisbach, cubic meters/day', self.iface.mainWindow())
        self.sampleDwCmdAction.triggered.connect(self.openDwCmdSample)
        self.project_menu.addAction(self.sampleDwCmdAction)

        self.sampleDwLpsAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), 'Sample Darcy-Weisbach, liters/second', self.iface.mainWindow())
        self.sampleDwLpsAction.triggered.connect(self.openDwLpsSample)
        self.project_menu.addAction(self.sampleDwLpsAction)

        self.sampleHwGpmAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), 'Sample Hazen-Williams, gallons/min', self.iface.mainWindow())
        self.sampleHwGpmAction.triggered.connect(self.openHwGpmSample)
        self.project_menu.addAction(self.sampleHwGpmAction)

        # Back in main menu
        self.iface.addPluginToMenu("&QWater", self.project_menu.menuAction())
        self.iface.addPluginToMenu("&QWater", self.aboutAction)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&QWater", self.aboutAction)
        self.iface.removePluginMenu('&QWater', self.runEpanetAction)
        self.iface.removePluginMenu("&QWater", self.writeInpAction)
        self.iface.removePluginMenu("&QWater", self.LoadStylesAction)
        self.iface.removePluginMenu('&QWater', self.vazaoAction)
        self.iface.removePluginMenu('&QWater', self.makeModelAction)
        self.iface.removePluginMenu('&QWater', self.fillFieldsAction)
        self.iface.removePluginMenu("&QWater", self.settingsAction)
        self.iface.removePluginMenu("&QWater", self.action)
        self.iface.removePluginMenu("&QWater", self.project_menu.menuAction())
        self.iface.removeToolBarIcon(self.settingsAction)
        self.toolbar.removeAction(self.settingsAction)
        self.toolbar.removeAction(self.LoadStylesAction)
        self.toolbar.removeAction(self.vazaoAction)
        self.toolbar.removeAction(self.runEpanetAction)

        # remove the toolbar
        del self.toolbar
    
    def fillFields(self):
        self.warning('Fill Fields call not working yet')
    
    # Calculate economic diameters
    def run(self):
        # Check for "LPS" flow units
        dlg = self.dlg #GHydraulicsSettingsDialog()
        template = dlg.getTemplate()
        inp = GHydraulicsInpReader(template)
        inpunits = inp.getValue('OPTIONS', 'Units').upper()
        if inpunits != EpanetModel.LPS:
            self.warning('"Calculate economic diameters" requires "LPS" flow units instead of "'+inpunits+'". Please change the template INP file.')
            return

        maker = GHydraulicsModelMaker(template)
        self.checkModel(maker)

        # Let user agree to the change
        selectedbutton = QMessageBox.question(self.iface.mainWindow(), "GHydraulics", "This will overwrite all DIAMETER field values. Do you want to continue?", QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Cancel)
        if QMessageBox.Cancel == selectedbutton:
            return

        # Execute the action
        ecodia = GhyEconomicDiameter(GHydraulicsModel.RESULT_FLO, EpanetModel.DIAMETER)
        maker.beginEditCommand('Calculate economic diameters')
        try:
            maker.eachLayer(ecodia.commitEconomicDiametersForLayer, [EpanetModel.PIPES])
        except GHydraulicsException as e:
            self.warning(str(e))
        maker.endEditCommand()

    # Display the About dialog
    def about(self):
        infoString = self.tr(self.SETTINGS+" Plugin "+self.VERSION+"<br />This plugin integrates EPANET with QGIS.<br />Copyright (c) 2017 - 2017 Jorge Almerio<br /><a href=\"https://github.com/jorgealmerio/QWater/blob/master/README.md\">github.com/jorgealmerio/QWater</a>\n")
        QMessageBox.information(self.iface.mainWindow(), "About "+self.SETTINGS, infoString)

    # Display the settings dialog
    def showSettings(self):
        dlg = self.dlg #QWaterSettingsDialog()
        proj = QgsProject.instance()
        layers = proj.mapLayers()        
        hasVectorLayers = False

        msgs=''
        QWaterEntries=proj.entryList(QWaterPlugin.SETTINGS, '')
        GhydraulicsEntries=proj.entryList('ghydraulics', '')
        # Restore selected layers        
        for secao in EpanetModel.GIS_SECTIONS:
            #Create QgsMapLayerComboBox filters
            widget=dlg.findChild(QgsMapLayerComboBox,'CMB'+secao)
            if secao in GHydraulicsModel.NODE_SECTIONS:
                widget.setFilters(QgsMapLayerProxyModel.PointLayer)
            else:
                widget.setFilters(QgsMapLayerProxyModel.LineLayer)
            widget.setAllowEmptyLayer(True) #added in QGIS 3.0: Sets whether an optional empty layer ("not set") option is shown in the combo box
            #Read and restore file Entries
            if secao in QWaterEntries:
                lyrName=proj.readEntry(QWaterPlugin.SETTINGS, secao, "")[0]
                layerEntry=proj.mapLayersByName(lyrName)
                if layerEntry:
                    widget.setLayer(layerEntry[0])
                    msgs+='\n{}:{} -> QWater Layer found'.format(secao,lyrName)
                else:
                    msgs+='\n{}:{} -> QWater Layer NOT found'.format(secao,lyrName)
                    widget.setLayer(None)
            elif secao in GhydraulicsEntries:#if has Not QWater settings try to get ghydraulics settings
                pickle_list = str(proj.readEntry('ghydraulics', secao, "")[0])
                if '' != pickle_list:
                    # Windows QGIS injects some carriage returns here
                    pickle_list = pickle_list.replace('\r','').encode() #use encode convet to byte
                    try:
                        l = loads(pickle_list)
                        valor=l
                        if valor:
                            layerEntry=proj.mapLayersByName(valor[0])
                            if layerEntry:
                                widget.setLayer(layerEntry[0])
                                msgs+='\n{}:{} -> GHydraulics Layer found'.format(secao,layerEntry[0].name())
                            else:
                                widget.setLayer(None)
                                msgs+='\n{}:{} -> GHydraulics Layer NOT found'.format(secao,valor[0])
                        else:
                            widget.setLayer(None)
                            msgs+='\n{} -> GHydraulics Previous Settings Null'.format(secao)
                    except(KeyError):
                        widget.setLayer(None)
                        # fix_print_with_import
                        print('Error on section:'+secao)
                        continue
            else:
                msgs+='\n{} -> Previous Settings NOT found'.format(secao)
                widget.setLayer(None)

        #if msgs!='':
        #    print msgs

        # Restore template inp file
        template = dlg.getTemplate()
        dlg.ui.inpFileLineEdit.setText(template)
        # Restore auto length checkbox
        dlg.ui.autoLengthCB.setChecked(dlg.getAutoLength())
        # Restore backdrop checkbox
        dlg.ui.writeBackdropCB.setChecked(dlg.getWriteBackdrop())

        # Restore data variables
        dataDefs=QWaterModel.DATA_DEFS
        for dataDf,defVal in dataDefs.items():
            #Get widget
            widget=dlg.findChild(QLineEdit,'Txt_'+dataDf)
            inVar=proj.readEntry(QWaterPlugin.SETTINGS, dataDf, defVal)[0]
            widget.setText(inVar)
        
        #Carrega Tubos 
        tubosMat=proj.readEntry(QWaterPlugin.SETTINGS, "TUBOS_MAT","0")[0]
        if tubosMat=='0':#se nao tiver lista de materiais definidas carrega o padrao do modelo
            tubos=QWaterModel.TUBOS_MAT
        else:
            tubos=eval(tubosMat)
        self.carregaTabMats(tubos)
        
        # Exibe o resumo de extensoes de rede se tiver PIPES definido
        ProjVar=proj.readEntry(QWaterPlugin.SETTINGS, 'PIPES')[0]
        
        if ProjVar!='':
            try:
                myLayer=proj.mapLayersByName(ProjVar)[0]
                tot,geo=QWater_00Common().CompRealGeom(myLayer)

                msgTxt=self.tr(u'<span style=" color:#0000ff;">Geometric Length: {0:.2f} m</span>').format(geo)
                dlg.ui.lbl_extGeo.setText(msgTxt)
                msgTxt=''
    
                if tot>0:
                    msgTxt=self.tr(u'<span style=" color:#37c322;">Length Field Sum: {0:.2f} m</span>').format(tot)
                dlg.ui.lbl_extReal.setText(msgTxt)
                msgTxt=''
            except: 
                pass
        # show the dialog
        dlg.show()
        #for i in range(0, dlg.UNUSED_ITEM+1):
        #    dlg.ui.treeWidget.topLevelItem(i).setExpanded(True)
        #result = dlg.exec_()
        result = dlg.exec_()
        if result:
            self.accepted()
    def accepted(self):
        # Store layers
        dlg = self.dlg #QWaterSettingsDialog()
        proj = QgsProject.instance()
        for secao in EpanetModel.GIS_SECTIONS:
            #Get QgsMapLayerComboBoxs 
            widget=dlg.findChild(QgsMapLayerComboBox,'CMB'+secao)
            curlyr=widget.currentLayer()
            if not(curlyr is None):
                lyrName=curlyr.name()
            else:
                lyrName=''
            #print secao,widget,lyrName
            proj.writeEntry(self.SETTINGS,secao, lyrName)

        #proj.writeEntry("ghydraulics",EpanetModel.GIS_SECTIONS[i], dumps(layers))
        # Store Inp file
        templatedir = os.path.join(os.path.dirname(__file__), 'etc')
        template = str(dlg.ui.inpFileLineEdit.text()).replace(templatedir+os.path.sep, '')
        proj.writeEntry(self.SETTINGS,"templateinpfile", template)
        # Store auto length configuration
        autoLength = dlg.STRING_FALSE
        if dlg.ui.autoLengthCB.isChecked():
            autoLength = dlg.STRING_TRUE
        proj.writeEntry(self.SETTINGS, dlg.AUTO_LENGTH, autoLength)
                # Store backdrop configuration
        writeBackdrop = dlg.STRING_FALSE
        if dlg.ui.writeBackdropCB.isChecked():
            writeBackdrop = dlg.STRING_TRUE
        proj.writeEntry(self.SETTINGS, dlg.WRITE_BACKDROP, writeBackdrop)

        # Store data variables
        dataDefs=QWaterModel.DATA_DEFS
        for dataDf,defVal in dataDefs.items():
            #Get widget
            widget=dlg.findChild(QLineEdit,'Txt_'+dataDf)
            inVar=widget.text()
            proj.writeEntry(QWaterPlugin.SETTINGS, dataDf, inVar)
        
        proj.writeEntry(QWaterPlugin.SETTINGS, "TUBOS_MAT", str(self.tableToArray()))

    # Display a message once
    def explainOnce(self, key, title, message):
        proj = QgsProject.instance()
        if GHydraulicsModel.STRING_TRUE == str(proj.readEntry(QWaterPlugin.SETTINGS, key)[0]):
            return True
        reply = QMessageBox.question(self.iface.mainWindow(), title,
                                            message, QMessageBox.Yes |
                                            QMessageBox.No, QMessageBox.Yes)
        if QMessageBox.Yes == reply:
            proj.writeEntry(QWaterPlugin.SETTINGS, key, GHydraulicsModel.STRING_TRUE);
            return True
        return False

    # Check if all fields are in place
    def checkModel(self, maker):
        checker = maker.checker
        if 0 == checker.getLayerCount(EpanetModel.JUNCTIONS) or 0 == checker.getLayerCount(EpanetModel.PIPES):
            question = 'Your junction and/or pipe layer configuration is incomplete. Do you want configure the layers now?'
            reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE, question, QMessageBox.Yes|QMessageBox.No,
                                               QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.showSettings()
            if 0 == checker.getLayerCount(EpanetModel.JUNCTIONS) or 0 == checker.getLayerCount(EpanetModel.PIPES):
                return False
        self.checkForModifications(checker)
        missing = checker.checkFields()
        if 0 < len(missing):
            fieldlist = []
            for name in list(missing.keys()):
                fieldlist.append('<br/>Layer "'+name+'": '+ ', '.join(missing[name]))
            message = 'Your model is missing some fields.'+''.join(fieldlist)+'<br/>Would you like to add them?'
            reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE,
                                                       message, QMessageBox.Yes |
                                                       QMessageBox.No, QMessageBox.Yes)
            if QMessageBox.Yes != reply:
                return False
            if not checker.addFields(missing):
                QMessageBox.critical(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE,
                                      'Not all fields could be added.', QMessageBox.Ok)
                return False
        crss = checker.getCrsDictionary()
        if 1 != len(crss):
            message = 'Your model uses more than one coordinate reference system. Please use only one.'
            QMessageBox.critical(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE,
                                    message, QMessageBox.Ok, QMessageBox.Ok)
            return False

        missing = checker.checkIds()
        if 0 < len(missing):
            question = 'There are '+str(len(missing))+' duplicate '+GHydraulicsModel.ID_FIELD+' values. Do want to fix this automatically now?'
            reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE,
                                               question, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if QMessageBox.Yes != reply:
                return False
            if not maker.enforceUniqueIds():
                return False
        multis = checker.getMultipartCount()
        if 0 < multis:
            question = 'There are '+str(multis)+' pipes with multipart geometries possibly causing problems. Do you want to explode them now?'
            reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE, question,
                                                QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if QMessageBox.Yes == reply:
                maker.explodeMultipartPipes()

    # Fill the node1, node2 fields
    def makeModel(self):
        if self.common.PegaQWaterLayer('PIPES')==False:            
            return
        dlg = self.dlg #GHydraulicsSettingsDialog()
        template = dlg.getTemplate()
        maker = GHydraulicsModelMaker(template)
        self.iface.mainWindow().statusBar().showMessage('Checking EPANET model')
        self.checkModel(maker)
        question = 'Overwrite the fields NODE1 and NODE2 in all line tables?'
        self.iface.mainWindow().statusBar().showMessage("Making EPANET model")
        autolength = dlg.getAutoLength()
        if autolength:
            question = 'Overwrite the fields NODE1, NODE2 and LENGTH in all line tables?'
        if self.explainOnce('makeModelExplanation', 'Make EPANET Model', question):
            vcount = maker.make()
            if 0 < vcount:
                reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsModelChecker.TITLE,
                                           'Your model is missing '+str(vcount)+' junctions. Would you like to add them now?',
                                           QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
                if QMessageBox.Yes == reply:
                    self.iface.mainWindow().statusBar().showMessage('Adding missing junctions to EPANET model')
                    maker.addMissingJunctions()
            #dlg = GHydraulicsSettingsDialog()
            if autolength:
                self.iface.mainWindow().statusBar().showMessage('Pipe length calculation')
                maker.calculateLength()
            maker.cleanup()
        self.iface.mainWindow().statusBar().showMessage('')

    # Prevent problems with unsaved data
    def checkForModifications(self, checker):
        modified = checker.getModifiedLayers()
        if 0 < len(modified):
            message = 'Some of your model layers have not been saved (' + ', '.join(modified) + ').<br/>Do you want to save them now?'
            reply = QMessageBox.question(self.iface.mainWindow(), GHydraulicsInpWriter.TITLE,
                                               message, QMessageBox.Yes|
                                               QMessageBox.No, QMessageBox.Yes)
            if QMessageBox.Yes == reply:
                checker.commitChanges()

    # Write out a file in EPANET INP format
    # returns True on success, False on failure
    def writeInpFile(self):
        # Modified layers may not be exprted correctly
        checker = GHydraulicsModelChecker()
        self.checkForModifications(checker)
        # select a file
        prjfi = os.path.splitext(QgsProject.instance().fileName())[0]+'.inp'
        f, __ =  QFileDialog.getSaveFileName(self.iface.mainWindow(), GHydraulicsInpWriter.TITLE,
                                prjfi,
                                'EPANET INP file (*.inp)');

        if 0 < len(f):
            dlg = self.dlg #GHydraulicsSettingsDialog()
            template = dlg.getTemplate()
            try:
                writer = GHydraulicsInpWriter(template, self.iface)
                writeBackdrop = dlg.getWriteBackdrop()
                if writeBackdrop:
                    backdropfile = writer.getBackdropFromInp(str(f))
                    question = 'Overwrite ' + os.path.basename(backdropfile) + '?'
                    if os.path.exists(backdropfile) and not self.explainOnce('overwriteBackdrop', GHydraulicsInpWriter.TITLE, question):
                        writeBackdrop = False
                writer.write(f, writeBackdrop)
            except GHydraulicsException as e:
                self.warning('Saving an INP file failed: '+str(e))
                return False
            return True
        return False

    # Open CMD sample project
    def openDwCmdSample(self):
        self.iface.addProject(os.path.dirname(__file__)+'/samples/d-w/cmd/ghydraulics.qgs')

    # Open LPS sample project
    def openDwLpsSample(self):
        self.iface.addProject(os.path.dirname(__file__)+'/samples/d-w/lps/qwater_lps.qgs')

    # Open Net1 sample project
    def openHwGpmSample(self):
        self.iface.addProject(os.path.dirname(__file__)+'/samples/h-w/gpm/Net1.qgs')

    # Display warning message
    def warning(self, message):
        self.iface.messageBar().pushMessage(self.SETTINGS, message, level=Qgis.Warning, duration=4)

    # Create a new project, save and configure layers
    def newProject(self):
        self.iface.newProject()        
        project = QgsProject.instance()
        crs = project.crs() #TODO: Solicitar crs ao usuario
        baseName=project.readPath("./")
        for name in EpanetModel.GIS_SECTIONS:
            lname = name.lower()
            #self.iface.mainWindow()
            f, __ = QFileDialog.getSaveFileName(caption='Save new ' + lname + ' layer', 
                                                directory=baseName+'/'+lname + '.shp', filter='ESRI Shapefile (*.shp)')
            if 0 == len(f):
                continue 
            baseName= os.path.split(f)[0]
            fields = QgsFields()
            for i in range(0,len(EpanetModel.COLUMNS[name])):
                field = EpanetModel.COLUMNS[name][i]
                fields.append(QgsField(field, GHydraulicsModel.COLUMN_TYPES[field]))
            geometrytype = QgsWkbTypes.LineString if EpanetModel.PIPES == name else QgsWkbTypes.Point
            writer = QgsVectorFileWriter(f, 'System', fields, geometrytype, crs, 'ESRI Shapefile')
            if writer.hasError() != QgsVectorFileWriter.NoError:
                self.warning('Error creating shapefile: ' + str(writer.hasError()))
                continue
            del writer
            layer = self.iface.addVectorLayer(f, lname, 'ogr')
            if not layer.isValid():
                self.warning('Failed to load layer!')
                continue
            if not crs:
                crs = layer.crs()
            layers = [lname]
            project.writeEntry(self.SETTINGS, name, lname)
        self.LoadStyles()
        self.showSettings()

    def runEpanet(self):
        lyrPipe = self.common.PegaQWaterLayer('PIPES')
        if not lyrPipe:
            return
        # Get a temporary file
        t = tempfile.mkstemp(suffix='.inp')
        os.close(t[0])
        dlg = self.dlg #self.dlg #GHydraulicsSettingsDialog()
        template = dlg.getTemplate()
        try:
            writer = GHydraulicsInpWriter(template, self.iface)
            writer.write(t[1], False)
        except GHydraulicsException as e:
            self.warning('Saving an INP file failed :' + str(e))
            return
        try:
            runner = GHydraulicsModelRunner()
            output, report, steps = runner.run(t[1])
            dlg = GHydraulicsResultDialog(runner.setStep)
            dlg.ui.textOutput.setText(output)
            dlg.ui.textReport.setText(report)
            dlg.ui.comboStep.clear()
            dlg.ui.comboStep.addItems([str(x) for x in range(1, steps+1)])
            dlg.show()
            result = dlg.exec_()
        except GHydraulicsException as e:
            self.warning('Running a simulation failed :' + str(e))
        os.unlink(t[1])
        lyrPipe.triggerRepaint()
    def carregaTabMats(self,tbMats):
        tableWidget=self.dlg.findChild(QTableWidget,'tableWidget')
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)
        for i, tbMat in enumerate(tbMats):
            row = tableWidget.rowCount()
            tableWidget.insertRow(row)
            tableWidget.setColumnCount(len(tbMat))
            for column, data in enumerate(tbMat):
                if column==0:
                    cell_widget = QWidget()
                    lay_out = QHBoxLayout(cell_widget)
                    chk_bx = QCheckBox()
                    if data in [1,'1','t','True']:
                        chk_bx.setCheckState(QtCore.Qt.Checked)
                    else:
                        chk_bx.setCheckState(QtCore.Qt.Unchecked)
                    lay_out.addWidget(chk_bx)
                    lay_out.setAlignment(Qt.AlignCenter)
                    lay_out.setContentsMargins(0,0,0,0)
                    cell_widget.setLayout(lay_out)
                    tableWidget.setCellWidget(row, 0, cell_widget)
                else:
                    item = QTableWidgetItem("{}".format(data))#:7.2f
                    item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
                    tableWidget.setItem(row, column, item)
        tableWidget.setHorizontalHeaderLabels(['On','DN','Diameter','Roughness','Pressure','Referencia'])
        #for i in range(1,4):
        #    tableWidget.resizeColumnToContents(i)
        tableWidget.resizeColumnsToContents()
    def tableToArray(self):
        table=self.dlg.findChild(QTableWidget,'tableWidget')
        result = []
        num_rows, num_cols = table.rowCount(), table.columnCount()
        for row in range(num_rows):
            rows = []
            for col in range(num_cols):
                if col==0:
                    cell_widget = table.cellWidget(row,col).findChild(type(QCheckBox()))
                    if cell_widget.isChecked():#QTableWidget.item(row,column).checkState()==QtCore.Qt.Checked:
                        rows.append(1)
                    else:
                        rows.append(0)
                else:
                    item = table.item(row, col)
                    rows.append(item.text())#if item else ''
            result.append(rows)
        return result
    def LoadStyles(self):
        proj = QgsProject.instance()
        qStyles = {'PIPES':'pipe_headloss.qml','JUNCTIONS':'node_pressure.qml','PUMPS':'node_pump.qml','RESERVOIRS':'node_reserv.qml','TANKS':'node_tank.qml','VALVES':'node_valve.qml'} #{tipo:estilo}
        rootID = QWaterPlugin.SETTINGS
        for tipo, estilo in qStyles.items():
            ProjVar=proj.readEntry(rootID, tipo)[0]
            if ProjVar!='':
                myLayer=proj.mapLayersByName(ProjVar)[0]
                self.CarregaEstilo(myLayer,estilo)

    def CarregaEstilo(self,vLayer,Estilo):
        basepath = os.path.dirname(__file__)#os.path.realpath(
        FullPath=os.path.join(basepath, 'style/'+Estilo)
        vLayer.loadNamedStyle(FullPath)
        vLayer.triggerRepaint()