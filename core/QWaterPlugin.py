from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
# -*- coding: utf-8 -*-#
# This file is part of QWater
#
# QWaterPlugin.py - The QWater plugin
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
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QLineEdit, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QCheckBox, QDialogButtonBox, QToolButton
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
from .QWater_01Rename import *
from .QWater_03Export import *
from .QWater_04Static_Head import *

#qepanet imports
from .addon.qepanet.tools.parameters import Parameters
from .addon.qepanet.ui.curvespatterns_ui import GraphDialog
from .addon.qepanet.model.system_ops import Curve

import configparser

from .addon.profiletool.tools.profiletool_core import ProfileToolCore
# initialize Qt resources from file resouces.py
from . import resources

# import QWaterNet_addon
from .addon.waterNet.QWaterNet import QWaterNet_addon
ClassName='QWaterPlugin'
class QWaterPlugin:
    # Store settings in QGIS projects under this key
    SETTINGS ="QWater"

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        try:
            pluginMetadata = configparser.ConfigParser()
            pluginMetadata.read(os.path.join(self.plugin_dir, 'metadata.txt'))
            self.VERSION = pluginMetadata.get('general', 'version')
        except:
            self.VERSION = "3.0.0"
        
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QWater_{}.qm'.format(locale))

        if os.path.exists(locale_path):#se n for pt traduz pra ingles
            self.translator = QTranslator()
            self.translator.load(locale_path)            
            if qVersion() > '4.3.3':
                instal = QCoreApplication.installTranslator(self.translator)
                QgsMessageLog.logMessage('Translator; Installed:{} from:{} '.format(instal, locale_path), self.SETTINGS, Qgis.Info)
                QgsMessageLog.logMessage('transQt:{} QWater:{} Lng: {}'.format(qVersion(),self.VERSION,locale), self.SETTINGS, Qgis.Info)
        
        # Create the dialog (after translation) and keep reference
        self.dlg = QWaterSettingsDialog()#QWater_SettingsDialog()
        #self.dlg.setWindowModality( Qt.WindowStaysOnTopHint ) #ApplicationModal
        self.dlg.setWindowFlag(Qt.WindowStaysOnTopHint )
        self.VazaoClasse=QWater_02Flow()
        self.dxfOutClasse=QWater_03Export()        
        
        self.common=QWater_00Common()
        self.separators=[]

        # Profile tool
        self.profiletool = ProfileToolCore(self.iface,self)
        #qepanet tool used for Pump Curves
        self.params = Parameters()
        self.QW_layers = self.get_QWater_layers()
        self.canvas=self.iface.mapCanvas()

    def tr(self, message):
        return QCoreApplication.translate(ClassName, message)
        
    def initGui(self):
        # create actions
        defIconPath=":/plugins/QWater/icons/qwater.svg"
        self.action = QAction(QIcon(':/plugins/QWater/icons/sizing.svg'), self.tr('Calculate economic diameters'), self.iface.mainWindow())
        self.StaticHead_action = QAction(QIcon(':/plugins/QWater/icons/04staticHead.svg'), self.tr('Calculate static head'), self.iface.mainWindow())
        self.calcDiameter_IterativeAction = QAction(QIcon(':/plugins/QWater/icons/sizing_iterative.svg'), self.tr('Calculate economic diameters (Iterative)'), self.iface.mainWindow()) 
        self.action.setWhatsThis("Calculate economic pipe diameters based on flow data.")
        self.settingsAction = QAction(QIcon(':/plugins/QWater/icons/00settings.svg'), self.tr('Settings'), self.iface.mainWindow())
        self.makeModelAction = QAction(QIcon(':/plugins/QWater/icons/makemodel.svg'), self.tr('Make Model'), self.iface.mainWindow())
        self.fillFieldsAction = QAction(QIcon(':/plugins/QWater/icons/fields_fill.svg'), self.tr('Fill up Fields'), self.iface.mainWindow())
        self.writeInpAction = QAction(QIcon(':/plugins/QWater/icons/epanet.svg'), self.tr('Write EPANET INP file'), self.iface.mainWindow())
        self.runEpanetAction = QAction(QIcon(':/plugins/QWater/icons/run.svg'), self.tr('Run EPANET simulation'), self.iface.mainWindow())
        self.saveEditsAction = QAction(QIcon(':/plugins/QWater/icons/SaveEdits.svg'), self.tr('Save All QWater Edits'), self.iface.mainWindow())        
        self.aboutAction = QAction(QIcon(":/plugins/QWater/icons/qwater.svg"), self.tr("&About"), self.iface.mainWindow())      
        
        self.LoadStylesAction = QAction(QIcon(":/plugins/QWater/icons/style.svg"), self.tr("Load default styles"), self.iface.mainWindow())
        self.GetElevationAction = QAction(QIcon(":/plugins/QWater/icons/getelevation.svg"), self.tr("Get Elevation from DEM"), self.iface.mainWindow())
        self.vazaoAction = QAction(QIcon(':/plugins/QWater/icons/02vazao.svg'), self.tr('Calc Flow'), self.iface.mainWindow())        
        self.renameAction = QAction(QIcon(':/plugins/QWater/icons/01rename.svg'), self.tr('Renumber Network'), self.iface.mainWindow())
        self.updateDN_Action = QAction(QIcon(":/plugins/QWater/icons/qwater.svg"), self.tr("Update DN field"), self.iface.mainWindow())
        self.profileDockOpen_Action = QAction(QIcon(":/plugins/QWater/icons/profile.svg"), self.tr("Show profile"), self.iface.mainWindow())
        self.curveEditor_Action = QAction(QIcon(":/plugins/QWater/icons/curves.svg"), self.tr("Curve Editor"), self.iface.mainWindow())
        self.DxfExport_Action = QAction(QIcon(':/plugins/QWater/icons/03dxfout.svg'), self.tr('Export to DXF'), self.iface.mainWindow())
        
        # Connect actions to triggers
        self.action.triggered.connect(self.run)
        self.StaticHead_action.triggered.connect(self.StaticHead_calc)
        self.calcDiameter_IterativeAction.triggered.connect(self.calcDiameter_Iterative)
        self.settingsAction.triggered.connect(self.showSettings)
        self.makeModelAction.triggered.connect(self.makeModel)
        self.fillFieldsAction.triggered.connect(self.fillFields)        
        self.writeInpAction.triggered.connect(self.writeInpFile)
        self.GetElevationAction.triggered.connect(self.AtualizaCotaTN)# era GetElevation
        self.updateDN_Action.triggered.connect(self.update_DN)
        self.profileDockOpen_Action.triggered.connect(self.openProfileWidget)
        self.curveEditor_Action.triggered.connect(self.curve_editor)        
        #self.profiletool.dockwidget.close.connect(self.profileDock_closed)
        
        self.runEpanetAction.triggered.connect(self.runEpanet)
        self.saveEditsAction.triggered.connect(self.save_QWater_Edits)
        self.aboutAction.triggered.connect(self.about)
        
        self.RenameClasse=Rename_Tools(self.iface)
        self.renameAction.triggered.connect(self.RenameCall)
        
        Qwflow=QWater_02Flow().CalcFlow
        self.vazaoAction.triggered.connect(self.VazaoClasse.CalcFlow) #self.Vazao #ListNoDemandNodes #QWater_02Flow.CalcFlow
        
        #dxf Export
        self.DxfExport_Action.triggered.connect(self.dxfOutClasse.run)
        
        
        self.LoadStylesAction.triggered.connect(self.LoadStyles)

        #Create toolbar
        self.toolbar = self.iface.addToolBar('&QWater')
        self.toolbar.setObjectName('&QWater')

        # add toolbar buttons
        self.toolbar.addAction(self.settingsAction)        
        self.toolbar.addAction(self.makeModelAction)
        self.toolbar.addAction(self.renameAction)
        self.toolbar.addAction(self.fillFieldsAction)
        self.toolbar.addAction(self.vazaoAction)        
        self.toolbar.addAction(self.runEpanetAction)
        
        #Add separator
        self.toolbar.addSeparator()
        
        #Save Edits button
        self.toolbar.addAction(self.saveEditsAction)
        self.saveEditsAction.setEnabled(False)
        #self.QWater_layers_connect()
        self.canvas.layersChanged.connect(self.QWater_layers_connect)
        
        #Add separator
        self.toolbar.addSeparator()
        
        #Add economic diameter button
        self.toolbar.addAction(self.action)
        
        # Add ToolButton (with Menu)
        self.menuButton = QToolButton()#QPushButton()#QToolButton
        self.menuButton.setMenu(QMenu())
        self.menuButton.setPopupMode(QToolButton.MenuButtonPopup)
        # self.menuButton.setAutoRaise(True)        
        
        m = self.menuButton.menu()
        m.addAction(self.LoadStylesAction)
        m.addAction(self.writeInpAction)
        m.addAction(self.GetElevationAction)
        m.addAction(self.updateDN_Action)
        m.addAction(self.calcDiameter_IterativeAction)
        m.addAction(self.StaticHead_action)
        
        self.menuButton.setDefaultAction(self.GetElevationAction)
        self.menuButtonAction = self.toolbar.addWidget(self.menuButton)

        #Add profile tool button
        self.toolbar.addAction(self.profileDockOpen_Action)   
        #Add curve Editor tool button
        self.toolbar.addAction(self.curveEditor_Action)
        #Add DXF Export tool button
        self.toolbar.addAction(self.DxfExport_Action)
        
        # add menu items
        self.newProjectAction = QAction(self.iface.actionNewProject().icon(), self.tr('New QWater Project'), self.iface.mainWindow())
        self.newProjectAction.triggered.connect(self.newProject)
        self.iface.addPluginToMenu("&QWater", self.newProjectAction)
        
        self.iface.addPluginToMenu("&QWater", self.settingsAction)
        self.iface.addPluginToMenu('&QWater', self.makeModelAction)
        self.iface.addPluginToMenu('&QWater', self.renameAction)
        self.iface.addPluginToMenu('&QWater', self.fillFieldsAction)
        self.iface.addPluginToMenu('&QWater', self.vazaoAction)
        self.iface.addPluginToMenu('&QWater', self.runEpanetAction)
        
        #Add separator
        separator = self.toolbar.addSeparator()
        self.separators.append(separator)        
        self.iface.addPluginToMenu('&QWater', separator)
        
        #Add economic diameter tool menu
        self.iface.addPluginToMenu("&QWater", self.action)        
        
        # tools submenu
        self.tools_menu = QMenu(self.tr('&Tools'))
        self.tools_menu.addAction(self.LoadStylesAction)
        self.tools_menu.addAction(self.writeInpAction)
        self.tools_menu.addAction(self.GetElevationAction)
        self.tools_menu.addAction(self.updateDN_Action)
        self.tools_menu.addAction(self.calcDiameter_IterativeAction)
        self.tools_menu.addAction(self.StaticHead_action)

        # Projects submenu
        self.project_menu = QMenu(self.tr('&Projects'))

        self.sampleDwCmdAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), self.tr('Sample Darcy-Weisbach, cubic meters/day'), self.iface.mainWindow())
        self.sampleDwCmdAction.triggered.connect(self.openDwCmdSample)
        self.project_menu.addAction(self.sampleDwCmdAction)

        self.sampleDwLpsAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), self.tr('Sample Darcy-Weisbach, liters/second'), self.iface.mainWindow())
        self.sampleDwLpsAction.triggered.connect(self.openDwLpsSample)
        self.project_menu.addAction(self.sampleDwLpsAction)

        self.sampleHwGpmAction = QAction(QIcon(':/python/plugins/ghydraulic/icon.xpm'), self.tr('Sample Hazen-Williams, gallons/min'), self.iface.mainWindow())
        self.sampleHwGpmAction.triggered.connect(self.openHwGpmSample)
        self.project_menu.addAction(self.sampleHwGpmAction)

        # Back in main menu
        self.iface.addPluginToMenu("&QWater", self.tools_menu.menuAction())
        self.iface.addPluginToMenu("&QWater", self.project_menu.menuAction())
        self.iface.addPluginToMenu("&QWater", self.aboutAction)
        
        #Water distribution network tools
        self.QWaterNet_addon_Classe=QWaterNet_addon(self.iface)
        self.QWaterNet_addon_Classe.initGui()

    def unload(self):
        #QWaterNet_addon unload
        self.QWaterNet_addon_Classe.unload()
        try:
            self.canvas.layersChanged.disconnect(self.QWater_layers_disconnect)
        except:
            pass
        
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&QWater", self.aboutAction)
        self.iface.removePluginMenu('&QWater', self.runEpanetAction)
        self.iface.removePluginMenu("&QWater", self.writeInpAction)
        self.iface.removePluginMenu("&QWater", self.GetElevationAction)
        self.iface.removePluginMenu("&QWater", self.LoadStylesAction)
        self.iface.removePluginMenu("&QWater", self.updateDN_Action)
        self.iface.removePluginMenu("&QWater", self.calcDiameter_IterativeAction)
        self.iface.removePluginMenu("&QWater", self.StaticHead_action)
        self.iface.removePluginMenu("&QWater", self.newProjectAction)
        
        self.iface.removePluginMenu('&QWater', self.vazaoAction)
        self.iface.removePluginMenu('&QWater', self.makeModelAction)
        self.iface.removePluginMenu('&QWater', self.fillFieldsAction)
        self.iface.removePluginMenu('&QWater', self.renameAction)        
        self.iface.removePluginMenu("&QWater", self.settingsAction)
        self.iface.removePluginMenu("&QWater", self.action)
        self.iface.removePluginMenu("&QWater", self.project_menu.menuAction())
        self.iface.removePluginMenu("&QWater", self.tools_menu.menuAction())
        
        # remove Separators
        for sep in self.separators:
            self.iface.removePluginMenu(
                '&QWater',
                sep)
        
        self.iface.removeToolBarIcon(self.settingsAction)
        self.toolbar.removeAction(self.settingsAction)
        self.toolbar.removeAction(self.LoadStylesAction)
        self.toolbar.removeAction(self.GetElevationAction)
        self.toolbar.removeAction(self.updateDN_Action)
        self.toolbar.removeAction(self.calcDiameter_IterativeAction)
        self.toolbar.removeAction(self.StaticHead_action)
        
        self.toolbar.removeAction(self.vazaoAction)
        self.toolbar.removeAction(self.saveEditsAction)
        self.toolbar.removeAction(self.runEpanetAction)
        self.toolbar.removeAction(self.fillFieldsAction)
        self.toolbar.removeAction(self.makeModelAction)
        self.toolbar.removeAction(self.action)
        self.toolbar.removeAction(self.renameAction)
        self.toolbar.removeAction(self.menuButtonAction)
        self.toolbar.removeAction(self.profileDockOpen_Action) #profile tool button
        self.toolbar.removeAction(self.curveEditor_Action) #Curve Editor tool button
        self.toolbar.removeAction(self.DxfExport_Action) #dxf Export
        
        # profile tool
        self.profileDockOpened = False
        
        # remove the toolbar
        self.iface.mainWindow().removeToolBar(self.toolbar)
        del self.toolbar
    
    def StaticHead_calc(self):
        self.menuButton.setDefaultAction(self.StaticHead_action)
        QWater_04Static_Head(self.iface).StaticHead_calculate()
        
    def profileDock_closed(self):
        QgsMessageLog.logMessage('profileDock_closed',self.SETTINGS,Qgis.Info)
    def openProfileWidget(self):
        #self.warning('Profile tool still under development!', nivel=Qgis.Info)        
        if not self.profiletool.Opened: #not self.profileDockOpened:
            #if self.profiletool is None: 
            self.profiletool = ProfileToolCore(self.iface,self)            
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.profiletool.dockwidget) # self.profiletool.dockwidget.location            
            #self.profiletool.dockwidget.setFloating(True) #Enable to load undocked
            #self.profiletool.dockwidget.closed.connect(self.profiletool.cleaning)
            self.profileDockOpened = True
            self.profiletool.activateProfileMapTool()
        else:            
            self.profiletool.activateProfileMapTool()
            self.warning(self.tr('Profile tool already opened'),Qgis.Info)

    def RenameCall(self):
        self.RenameClasse.initGui()
    def fillFields(self):
        proj=QgsProject.instance()
        autolen=proj.readEntry(QWaterPlugin.SETTINGS, 'autolength', "0")[0]
        undefs=False
        preencheu=False
        fillCOLUMNS = {'JUNCTIONS': {'ELEVATION':0},
                   'PIPES': {'LENGTH':'CALCULA', 'DIAMETER':54.6, 'ROUGHNESS':1, 'MINORLOSS':0, 'STATUS':'OPEN'}}
        for secao in ['PIPES','JUNCTIONS']:
            vLayer = self.common.PegaQWaterLayer(secao)
            if vLayer!=False:
                feicoes=vLayer.getFeatures()
                vLayer.startEditing()
                for feicao in feicoes:                    
                    camposPadroes=fillCOLUMNS[secao]                    
                    for (campo,valorPad) in camposPadroes.items():
                        featVal=feicao[campo]
                        if campo=='LENGTH' and autolen=='1':
                            ext=feicao.geometry().length()
                            feicao[campo]=ext
                            preencheu=True
                        else:
                            if featVal==NULL or featVal is None:
                                feicao[campo]=valorPad
                                preencheu=True
                    vLayer.updateFeature(feicao)
            else:
                undefs=True
        if not undefs:
            if preencheu:
                self.warning(self.tr('Successfull fill in!'),Qgis.Info)
            else:
                self.warning(self.tr('Nothing to fill in!'),Qgis.Info)

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
    
    #Iterative runEpanet and Diameter sizing until 
    #1) pressure differences lower than accuracy (defined in settings dialog by user) or
    #2) number of iterations (defined in settings dialog by user)
    def calcDiameter_Iterative(self):
        self.menuButton.setDefaultAction(self.calcDiameter_IterativeAction)
        
        lyrPipe = self.common.PegaQWaterLayer('PIPES')
        if not lyrPipe:
            return

        dlg = self.dlg
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
            return
        try:
            runner = GHydraulicsModelRunner()
            output, report, steps = runner.run(t[1])
            
            #if has errors or warnings
            if any(x in output for x in erros):
                msgTxt = self.tr('QWater can NOT Calculate Economic Diameters (Iterative way) while there are errors or warnings!')
                dlg = GHydraulicsResultDialog(runner.setStep)                
                dlg.ui.textOutput.setText(output+msgTxt)
                self.StyleOutput(output,dlg.ui)
                dlg.ui.textReport.setText(report+msgTxt)
                dlg.ui.comboStep.clear()
                dlg.ui.comboStep.addItems([str(x) for x in range(1, steps+1)])
                dlg.show()                
                result = dlg.exec_()
                return            

            if any(x in output for x in erros):
                QgsMessageLog.logMessage('First run had warnings! Trying to Continue...',self.SETTINGS,Qgis.Info)
            QgsMessageLog.logMessage("Starting and saving first simulation results...",self.SETTINGS,Qgis.Info)
            runner.setStep(0) #Load simulation Step 1 (first step=0) to features, First Time
            junctionResults0 = self.readResults('JUNCTIONS', 'RESULT_PRE', runner) #Junction pressure results 
            
            iterFeat = self.common.getUser_iterFeat() # Ask user choose to run only selected feratures or not
            if iterFeat is None:
                return
            self.calc_EcoDiameter(iterFeat) #Calculate economic Diameters and load to features            
            pipeDiameters0 = self.layerField_to_Dict(lyrPipe,GHydraulicsModel.ID_FIELD,EpanetModel.DIAMETER)
            
            iterNum = 1
            IterCount = 15
            pressDiffMax = 9999
            pressAccuracy = 0.1
            diamChanged = True
            while (diamChanged or pressDiffMax >= pressAccuracy) and iterNum <= IterCount:            
                # Get a temporary file
                t = tempfile.mkstemp(suffix='.inp')
                os.close(t[0])
                try:
                    writer = GHydraulicsInpWriter(template, self.iface)
                    writer.write(t[1], False, silent=True)
                except GHydraulicsException as e:
                    self.warning(self.tr('Saving an INP file failed :') + str(e))
                    return            
                output, report, steps = runner.run(t[1]) #Run epanet
                
                runner.setStep(0) #Load simulation Step 1 (first step=0) to features                
                #Save results to variables
                junctionResults1 = self.readResults('JUNCTIONS', 'RESULT_PRE', runner) #Junction pressure results
                self.calc_EcoDiameter(iterFeat) #Calculate economic Diameters and load to features
                pipeDiameters1 = self.layerField_to_Dict(lyrPipe,GHydraulicsModel.ID_FIELD,EpanetModel.DIAMETER)

                
                #Check Diameter change between simulations
                diamChanged = False
                for key, value in pipeDiameters1.items():
                    if value-pipeDiameters0[key] > 0.001:
                        diamChanged = True
                        break #exit for                
                if diamChanged == False:  
                    pressDiffMax = 0
                    #Check max pressure difference between simulations
                    for key, value in junctionResults1.items():
                        pressDiff = abs(value - junctionResults0[key])                        
                        pressDiffMax = max(pressDiff, pressDiffMax)
                junctionResults0=junctionResults1
                pipeDiameters0=pipeDiameters1
                if pressDiffMax==9999:                    
                    QgsMessageLog.logMessage('iteration: {}; pressDiffMax:"Not checked!"; diamChanged={}'.format(iterNum, diamChanged),self.SETTINGS,Qgis.Info)
                else:
                    QgsMessageLog.logMessage('iteration: {}; pressDiffMax:{:.5f}; diamChanged={}'.format(iterNum, pressDiffMax, diamChanged),self.SETTINGS,Qgis.Info)                
                QApplication.processEvents()
                lyrPipe.triggerRepaint()
                iterNum+=1
                
        except GHydraulicsException as e:
            self.warning(self.tr('Running a simulation failed :') + str(e))
        os.unlink(t[1])
        lyrPipe.triggerRepaint()
    
    def layerField_to_Dict(self, layer, idField, field):
        dict={}
        for feature in layer.getFeatures():
            id=feature[idField]
            dict[id]=feature[field]
        return dict
    
    def calc_EcoDiameter(self, iterFeat):
        template = self.dlg.getTemplate()
        maker = GHydraulicsModelMaker(template)
        # Execute the action
        ecodia = GhyEconomicDiameter(GHydraulicsModel.RESULT_FLO, EpanetModel.DIAMETER, iterFeat)
        maker.beginEditCommand('Calculate economic diameters')
        try:
            maker.eachLayer(ecodia.commitEconomicDiametersForLayer, [EpanetModel.PIPES])
        except GHydraulicsException as e:
            self.warning(str(e))
        maker.endEditCommand()
        self.update_DN()
        
    def runEpanet(self):
        lyrPipe = self.common.PegaQWaterLayer('PIPES')
        if not lyrPipe:
            return
        # Get a temporary file
        t = tempfile.mkstemp(suffix='.inp')
        os.close(t[0])
        dlg = self.dlg
        template = dlg.getTemplate()
        try:
            writer = GHydraulicsInpWriter(template, self.iface)
            writer.write(t[1], False)
        except GHydraulicsException as e:
            self.warning(self.tr('Saving an INP file failed :') + str(e))
            return
        try:
            runner = GHydraulicsModelRunner()
            output, report, steps = runner.run(t[1])
            dlg = GHydraulicsResultDialog(runner.setStep)
            self.StyleOutput(output,dlg.ui)
            dlg.ui.textOutput.setText(output)
            dlg.ui.textReport.setText(report)
            dlg.ui.comboStep.clear()
            dlg.ui.comboStep.addItems([str(x) for x in range(1, steps+1)])
            dlg.show()
            result = dlg.exec_()
            if result:
                # muda os estilos
                self.selectStyle(lyrPipe, 'Headloss')
                nodeLayer = self.common.PegaQWaterLayer('JUNCTIONS')
                if nodeLayer:                    
                    self.selectStyle(nodeLayer, 'Pressure')
            
        except GHydraulicsException as e:
            self.warning(self.tr('Running a simulation failed :') + str(e))
        os.unlink(t[1])
        lyrPipe.triggerRepaint()
    
    # Calculate economic diameters
    def run(self): #run call_EcoDiameters        
        dlg = self.dlg
        template = dlg.getTemplate()
        inp = GHydraulicsInpReader(template)
        inpunits = inp.getValue('OPTIONS', 'Units').upper()
        if inpunits != EpanetModel.LPS:
            self.warning(self.tr('Requires "LPS" flow units instead of "{}". Please change the template INP file').format(inpunits))
            return

        maker = GHydraulicsModelMaker(template)
        self.checkModel(maker)

        # Let user agree to the change
        selectedbutton = QMessageBox.question(self.iface.mainWindow(), self.SETTINGS, self.tr("This will overwrite all DIAMETER and ROUGHNESS field values using Pipes Table data from settings Dialog. Do you want to continue?"), QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Cancel)
        if QMessageBox.Cancel == selectedbutton:
            return

        iterFeat = self.common.getUser_iterFeat()
        if iterFeat is None:
            return

        # Execute the action
        ecodia = GhyEconomicDiameter(GHydraulicsModel.RESULT_FLO, EpanetModel.DIAMETER, iterFeat)
        maker.beginEditCommand('Calculate economic diameters')
        try:
            maker.eachLayer(ecodia.commitEconomicDiametersForLayer, [EpanetModel.PIPES])
        except GHydraulicsException as e:
            self.warning(str(e))
        maker.endEditCommand()
        self.update_DN()
    # Display the About dialog
    def about(self):
        infoString = self.tr(self.SETTINGS+" Plugin "+self.VERSION+self.tr('<br />This plugin integrates EPANET with QGIS.<br />Copyright (c) 2017 - 2017 Jorge Almerio<br />')+'<a href=\"https://github.com/jorgealmerio/QWater/blob/master/README.md\">github.com/jorgealmerio/QWater</a>\n')
        QMessageBox.information(self.iface.mainWindow(), self.tr("About ")+self.SETTINGS, infoString)

    # Display the settings dialog
    def showSettings(self):
        dlg = self.dlg
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
            elif secao=='DEM':
                self.DEM_ComboBox_prepare(widget)                
            else:
                if secao=='ZONES':
                    widget.setFilters(QgsMapLayerProxyModel.PolygonLayer)
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
                        QgsMessageLog.logMessage('Error on section:'+secao,self.SETTINGS,Qgis.Info)
                        continue
            else:
                msgs+='\n{} -> Previous Settings NOT found'.format(secao)
                widget.setLayer(None)

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
            if not isinstance(tubos[0][0], str):
                QgsMessageLog.logMessage('Wrong Pipes settings'+tubosMat,self.SETTINGS,Qgis.Warning) #Show Warning Message
                tubos=QWaterModel.TUBOS_MAT

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
        
        #Call Combobox Zones activated signal to refresh it
        cmbZones = dlg.ui.CMBZONES
        cmbZones.activated.emit(cmbZones.currentIndex())
        
        dlg.ui.Txt_POPINI.editingFinished.emit()
        # show the dialog
        dlg.show()
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
            proj.writeEntry(self.SETTINGS,secao, lyrName)
        
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
        dlg = self.dlg
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
                    lyrJunctions = self.common.PegaQWaterLayer('JUNCTIONS')
                    lyrJunctions.triggerRepaint()
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
        self.menuButton.setDefaultAction(self.writeInpAction) #Change default toolbutton to writeInpAction
        checker = GHydraulicsModelChecker()
        self.checkForModifications(checker)
        # select a file
        prjfi = os.path.splitext(QgsProject.instance().fileName())[0]+'.inp'
        f, __ =  QFileDialog.getSaveFileName(self.iface.mainWindow(), GHydraulicsInpWriter.TITLE,
                                prjfi,
                                'EPANET INP file (*.inp)');

        if 0 < len(f):
            dlg = self.dlg
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

    # Display message
    def warning(self, message, nivel=Qgis.Warning):
        self.iface.messageBar().pushMessage(self.SETTINGS, message, level=nivel, duration=4)

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
    
    def StyleOutput(self, output, dialogUI):
        if 'erro' in output:
            myColor='#ff8e8e' #light red
        elif 'warning' in output:
            myColor='#ffff7f' #light yellow
        else:
            return #No errors or warnings, do nothing
        dialogUI.textOutput.setStyleSheet("background-color: {};".format(myColor))
        dialogUI.textReport.setStyleSheet("background-color: {};".format(myColor))
        
    def carregaTabMats(self,tbMats):
        tableWidget=self.dlg.findChild(QTableWidget,'tableWidget')
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)
        for i, tbMat in enumerate(tbMats):
            row = tableWidget.rowCount()
            tableWidget.insertRow(row)
            tableWidget.setColumnCount(len(tbMat))
            if row<1:                
                tableWidget.setHorizontalHeaderLabels(tbMat)
            else:
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
        tableWidget.removeRow(0)
        tableWidget.resizeColumnsToContents()

    def tableToArray(self):
        table=self.dlg.findChild(QTableWidget,'tableWidget')
        result = [self.LeCabecalho(table)]
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
    def LeCabecalho(self, tblWid):
        header=[]
        for column in range(tblWid.columnCount()):
            header.append(tblWid.horizontalHeaderItem(column).text())
        return header
        
    def selectStyle(self, layer, styleName):
        # muda o estilo para fittings
        style_manager = layer.styleManager()

        # read valid style from layer
        style = QgsMapLayerStyle()
        style.readFromLayer(layer)
        
        style_manager.setCurrentStyle(styleName)
        
    def LoadStyles(self):
        self.menuButton.setDefaultAction(self.LoadStylesAction)
        proj = QgsProject.instance()
        #qStyles = #{'PIPES':'pipe_headloss.qml','JUNCTIONS':'node_pressure.qml','PUMPS':'node_pump.qml','RESERVOIRS':'node_reserv.qml','TANKS':'node_tank.qml','VALVES':'node_valve.qml'} #{tipo:estilo}
        qStyles = {'PIPES':[['Headloss','pipe_headloss.qml'],
                            ['Diameter','pipe_by_DN.qml'],
                            ['Diameter with Length','pipe_dn_len.qml'],                            
                            ['Nodes ID','pipe_id_nodes.qml'],
                            ['Full data','pipe_id_len_dn_flow.qml']],
                'JUNCTIONS':[['ID','node_id.qml'],
                        ['ID with Pressure','node_id_pressure.qml'],
                        ['Demands','node_demand.qml'],
                        ['Fittings','node_fittings.qml'],                        
                        ['Pressure','node_pressure.qml'],
                        ['Static Pressure','node_StaticPressure.qml']],
                'PUMPS':[['Pump','node_pump.qml']],
                'RESERVOIRS':[['Reservoir','node_reserv.qml']],
                'TANKS':[['Tank','node_tank.qml']],
                'VALVES':[['Valve','node_valve.qml']]}
        
        
        
        rootID = QWaterPlugin.SETTINGS
        for tipo, estilo in qStyles.items():
            ProjVar=proj.readEntry(rootID, tipo)[0]
            if ProjVar!='':
                myLayer=proj.mapLayersByName(ProjVar)[0]
                self.CarregaEstilo(myLayer,estilo)
    
    #Load Multiple Styles
    def CarregaEstilo(self,layer,Estilo):
        basepath = os.path.dirname(__file__)
        qml_path=os.path.join(basepath, 'style/')
    
        style_manager = layer.styleManager()

        # read valid style from layer
        style = QgsMapLayerStyle()
        style.readFromLayer(layer)
        
        for qml_Lst in Estilo:
            # get style name from file
            style_name = qml_Lst[0]
            # add style with new name
            style_manager.addStyle(style_name, style)
            # set new style as current
            style_manager.setCurrentStyle(style_name)
            # load qml to current style
            (message, success) = layer.loadNamedStyle(os.path.join(qml_path, qml_Lst[1]))
            if not success:  # if style not loaded remove it
                style_manager.removeStyle(style_name)
                QgsMessageLog.logMessage('{} \'{}\''.format(message,style_name),self.SETTINGS,Qgis.Info)                
        '''
        basepath = os.path.dirname(__file__)#os.path.realpath(
        FullPath=os.path.join(basepath, 'style/'+Estilo)
        layer.loadNamedStyle(FullPath)
        layer.triggerRepaint()
        '''

    #Get elevation from Raster
    def AtualizaCotaTN(self):
        proj = QgsProject.instance()
        msgTxt=''
        NodesLyr = {'JUNCTIONS': 'ELEVATION',
               'RESERVOIRS': 'HEAD',
               'TANKS': 'ELEVATION',
               'PUMPS': 'ELEVATION',
               'VALVES': 'ELEVATION'}
               
        lyrTipos = list(NodesLyr.keys())
        lyrList={}
        notFound=[]
        unDefined=[]
        for lyrTipo in lyrTipos:
            ProjNode=proj.readEntry("QWater", lyrTipo)[0]
            if ProjNode!='':
                vLayerLst=proj.mapLayersByName(ProjNode)
                if vLayerLst:
                    vLayer=vLayerLst[0]
                    lyrList[lyrTipo]= [vLayer , NodesLyr[lyrTipo]]
                else:
                    notFound.append(ProjNode)
            else:
                unDefined.append(lyrTipo)         
        if notFound:
            msgTxt= self.tr(u'Layer(s) not found: {}').format(', '.join(notFound))
        if unDefined:
            msgTxt= msgTxt +' / '+ self.tr('Layer(s) undefined: {}').format(', '.join(unDefined))
        if msgTxt!=''and not lyrList:
            iface.messageBar().pushMessage("QWater:", msgTxt, level=Qgis.Warning, duration=5)
            return False
        self.GetElevation(lyrList)
    
    def DEM_ComboBox_prepare(self, widget):
        outList=[]
        widget.setExceptedLayerList(outList) #reset
        
        widget.setFilters( QgsMapLayerProxyModel.RasterLayer | QgsMapLayerProxyModel.MeshLayer )
        #filter out raster without info capabilities        
        for i in range(0,widget.count()):
            layer = widget.layer(i)
            if layer and (layer.type() != layer.MeshLayer):
                caps = layer.dataProvider().capabilities()
                if not (caps & Qgis.RasterInterfaceCapability.IdentifyValue): #era: caps<=1024:
                    outList.append(layer)

        widget.setExceptedLayerList(outList)
        
    def GetElevation(self, lyrList):
        self.menuButton.setDefaultAction(self.GetElevationAction) #Change default toolbutton to GetElevationAction
        dlg = QDialog()
        dlg.setWindowTitle(self.tr('Select Elevation Raster'))
        
        #Raster and mesh Combobox
        ml=QgsMapLayerComboBox()
        ml.setFilters( QgsMapLayerProxyModel.RasterLayer | QgsMapLayerProxyModel.MeshLayer )
        #filter out raster without info capabilities
        outList=[]
        for i in range(0,ml.count()):
            layer = ml.layer(i)
            if layer and (layer.type() != layer.MeshLayer):
                caps = layer.dataProvider().capabilities()
                if not (caps & Qgis.RasterInterfaceCapability.IdentifyValue): #era: caps<6
                    outList.append(layer)
        ml.setExceptedLayerList(outList) 
        
        #Check Dem Layer is defined and select
        proj = QgsProject.instance()
        ProjVar=proj.readEntry(QWaterPlugin.SETTINGS, 'DEM')[0]        
        if ProjVar!='':            
            demLyr=proj.mapLayersByName(ProjVar)[0]
            if demLyr:
                ml.setLayer(demLyr)
        
        #ButtonBox
        bb=QDialogButtonBox()
        bb.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)        
        
        #layout
        layOut = QVBoxLayout()
        layOut.addWidget(ml)
        
        #Add checkBoxes
        for tipo in lyrList:
            nome = lyrList[tipo][0].name()
            chkbox = QCheckBox('{}: {}'.format(tipo, nome))
            layOut.addWidget(chkbox)
        
        #return to layout add button bar
        layOut.addWidget(bb)
        dlg.setLayout(layOut)        
        dlg.setMinimumWidth(300)
        
        # Signals answers
        def ok():            
            for i in range(layOut.count()):
                item = layOut.itemAt(i)
                widget = item.widget()
                if isinstance(widget, QCheckBox):
                    tipo = widget.text().split(':')[0]
                    if widget.isChecked():
                        self.RasterSampling(ml.currentLayer(),lyrList[tipo])
            QApplication.restoreOverrideCursor()
            dlg.close()
            #self.RasterSampling(ml.currentLayer())
            #curlyr = ml.currentLayer()
        def cancel():            
            dlg.close()
            QApplication.restoreOverrideCursor()
            
        #connect to signals
        bb.accepted.connect(ok)
        bb.rejected.connect(cancel)
        
        dlg.show()
    def RasterSampling(self, mdtLyr, lyr_Fld):
        nodeLyr=lyr_Fld[0]
        tnField=lyr_Fld[1]       
        if nodeLyr.selectedFeatureCount()==0:
            feicoes=nodeLyr.getFeatures()
        else:
            msg = self.tr('Update only selected features {}?')
            resp=QMessageBox.question(None,'QWater',msg.format(nodeLyr.name()),
                                      QMessageBox.Yes, QMessageBox.No)
            if resp==QMessageBox.Yes:
                feicoes=nodeLyr.selectedFeatures()
            else:
                feicoes=nodeLyr.getFeatures()
        noElevPtos=[]
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # if meshlayer type create render before get values
        if mdtLyr.type() == mdtLyr.MeshLayer:
            mdtLyr.createMapRenderer(QgsRenderContext())
            dataset = QgsMeshDatasetIndex(0,0)
        nodeLyr.startEditing()
        for pto in feicoes:
            ptoGeo = pto.geometry()
            if ptoGeo.isMultipart():
                point = ptoGeo.asMultiPoint()[0]
            else:
                point = ptoGeo.asPoint()
            
            if mdtLyr.type() == mdtLyr.MeshLayer:
                try:                    
                    value = mdtLyr.datasetValue(dataset, point).scalar()
                except:                    
                    value = None

                #workaround to qgis Mesh bug #36041, move point by 0.0001 to right and get value again
                if math.isnan(value):
                    ptoGeo.translate(0.0001,0)
                    if ptoGeo.isMultipart():
                        point = ptoGeo.asMultiPoint()[0]
                    else:
                        point = ptoGeo.asPoint()
                    value = mdtLyr.datasetValue(dataset, point).scalar()
                    QgsMessageLog.logMessage('Point moved by 0.0001 to get elevation: {}'.format(pto['DC_ID']),'QWater', Qgis.Info)

            else: #Raster layer
                value = mdtLyr.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]            
            if value and not math.isnan(value):                
                pto[tnField]=value
                nodeLyr.updateFeature(pto)
            else:
                noElevPtos.append(pto.id())
        if noElevPtos:            
            nodeLyr.selectByIds(noElevPtos) 
            mapCanvas = iface.mapCanvas()
            mapCanvas.zoomToSelected(nodeLyr)
            iface.messageBar().pushMessage('QWater', self.tr('Check not found elevation in selected elements {}:').format(nodeLyr.name()), level=Qgis.Warning, duration=0)
        else:
            iface.messageBar().pushMessage('QWater', self.tr('Successed updated elevation in {}!').format(nodeLyr.name()), level=Qgis.Info, duration=10)
        nodeLyr.triggerRepaint()
        
    def update_DN(self):
        try:
            self.menuButton.setDefaultAction(self.updateDN_Action)
        except:
            pass
        #Check and get Pipes Layer
        pipeLyr = self.common.PegaQWaterLayer('PIPES')
        if not pipeLyr:            
            return
        
        #Check and create field 'DN' #NPS (Nominal Pipe Size)
        field_index = pipeLyr.fields().indexFromName('DN')
        pipeLyr.startEditing()
        if field_index == -1:
            #if field does not exist create it
            DNfld = QgsField("DN", QVariant.Int)            
            pipeLyr.addAttribute(DNfld)
            pipeLyr.updateFields()
            field_index = pipeLyr.fields().indexFromName('DN')
            editSet = QgsEditorWidgetSetup ('TextEdit' , {}) #{'IsMultiline': 'True'}
            pipeLyr.setEditorWidgetSetup(field_index,editSet)
        #Carrega Tubos 
        proj = QgsProject.instance()
        tubosMat=proj.readEntry(self.SETTINGS, "TUBOS_MAT","0")[0]            
        if tubosMat=='0':
            raise GHydraulicsException(self.tr('ERROR: Please, Define Pipes on settings dialog First!'))
        else:
            tubos=eval(tubosMat)
            if not isinstance(tubos[0][0], str):
                raise GHydraulicsException(self.tr('ERROR: Incorrect Pipes definition!. Please, Define Pipes on settings dialog First!'))    
        
        cabecalho = tubos[0]
        diaIdx = cabecalho.index('Diameter')
        dnIdx = cabecalho.index('DN')
        indices = [diaIdx,dnIdx]
        diaXdn={}
        for linha in range(1,len(tubos)):
            diam = eval(tubos[linha][diaIdx])
            diaXdn[diam]=eval(tubos[linha][dnIdx])
        
        noDNdef = []
        #Update DN field
        for f in pipeLyr.getFeatures():
            diam = f['DIAMETER']
            #Check if Diameter exists in Pipes Table Setting
            if diam not in diaXdn:
                noDNdef.append(f.id())
            else:
                f['DN']=diaXdn[diam]
                pipeLyr.updateFeature(f)
        pipeLyr.triggerRepaint()
        if noDNdef:
            pipeLyr.selectByIds(noDNdef)
            mapCanvas = iface.mapCanvas()
            mapCanvas.zoomToSelected(pipeLyr)
            iface.messageBar().pushMessage(self.SETTINGS, self.tr('Check Selected features with Diameters not in Pipes Table Setting or use Calculate economic Diameters tool!'), level=Qgis.Warning, duration=0)
        else:
            iface.messageBar().pushMessage(self.SETTINGS, self.tr('DN success updated!'), level=Qgis.Info, duration=3)
    
    #base on read_curves() from 'qepanet\model\inp_writer.py'
    def read_Project_Curves(self):
        proj = QgsProject.instance()
        curvesStr = proj.readEntry(self.SETTINGS, "CURVES","0")[0]
        curves_d = {}
        resp = False
        if curvesStr:
            curvesDict = eval(curvesStr)
            if curvesDict:
                for curvaID in curvesDict:
                    curvaArray = curvesDict[curvaID]                    
                    i=0                    
                    for linha in curvaArray:
                        if i==0: #First line has description and curve type
                            curve_desc = linha[0]
                            curve_type = linha[1]
                            curves_d[curvaID] = Curve(curvaID, curve_type, curve_desc)
                            i+=1
                        else:
                            x = linha[1]
                            y = linha[2]
                            curves_d[curvaID].append_xy(x, y)                
                resp = curves_d
        return resp

    def curve_editor(self):        
        curvas = self.read_Project_Curves()
        if curvas:
            self.params.curves = curvas        
        curve_dialog = GraphDialog(self, self.iface.mainWindow(), self.params, edit_type=1)
        curve_dialog.exec_()
    
    #Return a dictionary with QWater layers like: {secao: layer}
    def get_QWater_layers(self):
        proj = QgsProject.instance()
        QW_layers={}
        QWaterEntries=proj.entryList(QWaterPlugin.SETTINGS, '')        
        # get QWater layers        
        for secao in EpanetModel.GIS_SECTIONS:
            if secao in QWaterEntries:
                lyrName=proj.readEntry(QWaterPlugin.SETTINGS, secao, "")[0]
                layerEntry=proj.mapLayersByName(lyrName)
                if layerEntry:
                    QW_layers[secao]=layerEntry[0]
        return QW_layers
    def QWater_layers_connect(self):        
        QW_layers = self.get_QWater_layers()
        for layer in QW_layers.values():
            layer.layerModified.connect(self.QWater_layers_Editing)                

    def QWater_layers_disconnect(self):
        QW_layers = self.get_QWater_layers()        
        for layer in QW_layers.values():  
            try:
                layer.layerModified.disconnect(self.QWater_layers_Editing)                
            except:
                pass

    def QWater_layers_isEditing(self):
        QW_layers = self.get_QWater_layers()
        for layer in QW_layers.values():            
            if layer.isEditable():
                if layer.isModified():
                    return True
        return False

    def QWater_layers_Editing(self):
        self.saveEditsAction.setEnabled(self.QWater_layers_isEditing())        
        
    def save_QWater_Edits(self):
        curLayer = self.iface.activeLayer()
        QW_layers = self.get_QWater_layers()
        for layer in QW_layers.values():
            if layer.isEditable():
                if layer.isModified():
                    layer.commitChanges()
                else:
                    layer.rollBack()
        self.iface.layerTreeView().currentLayerChanged.emit(curLayer)
        self.saveEditsAction.setEnabled(False)
