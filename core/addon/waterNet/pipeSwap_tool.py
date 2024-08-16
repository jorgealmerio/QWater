# -*- coding: utf-8 -*-
#******************************************************************************
#

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from qgis.core import *
from qgis.gui import *

from ...QWater_00Common import *
from ...QWater_00Model import *
from .pipes_dialog import PipesDialog

class pipeSwapTool(QgsMapTool):
    SETTINGS ="QWater"
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.common=QWater_00Common()
        self.iface = iface
        self.layer = None
        #QApplication.setOverrideCursor(Qt.ArrowCursor)
        
        #self.extentChanged.connect(self.showDialog)        
        
        # Create the dialog (after translation) and keep reference
        self.dlg = PipesDialog()
        self.dlg.setWindowFlag(Qt.WindowStaysOnTopHint )
        btn = self.dlg.buttonBox.button(QDialogButtonBox.Apply)
        btn.clicked.connect(self.apply)        
        self.dlg.tableWidget.currentCellChanged.connect(self.tableCellChanged)
        self.lastValidRow=0
        self.pipefields = ['DN','DIAMETER','ROUGHNESS']
        
        self.cursor = Qt.ArrowCursor #QCursor(QPixmap(':/plugins/uteis/icons/cursor2.png'), 1, 1)    
        
        self.rubberBand = QgsRubberBand(self.canvas, Qgis.GeometryType.Polygon)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.reset()
    
    def apply(self):
        tableWidget=self.dlg.tableWidget
        row = tableWidget.selectionModel().selectedRows()[0].row()
        valores = {}
        i=0
        for col in range(1,4): #cols (1:DN; 2:Diameter; 3:Roughness)
            valor = tableWidget.item(row,col).text()
            valores[self.pipefields[i]]=float(valor)
            i+=1        
        layer=self.layer
        if layer:
            if layer.selectedFeatureCount()>0:
                validFields = self.listFields(layer)
                layer.startEditing()
                for feat in self.layer.getSelectedFeatures():
                    for fld in validFields:
                        feat[fld]=valores[fld]
                    layer.updateFeature(feat)
                layer.triggerRepaint()
            else:
                self.iface.messageBar().pushMessage(self.SETTINGS, self.tr('No selected features to apply!'), level=Qgis.Warning, duration=3)
    
    def listFields(self, layer):        
        valid=[]
        for fld in self.pipefields:
            field_index = layer.fields().indexFromName(fld)
            if field_index != -1:
                valid.append(fld)
        return valid
        
    def tableCellChanged(self,currentRow, currentColumn, previousRow, previousColumn):
        if currentRow==-1 and previousRow>0:
            self.lastValidRow=previousRow
            self.dlg.tableWidget.setCurrentCell(previousRow,3)

    def activate(self):
        self.setCursor(self.cursor)
        pipeLyr = self.common.PegaQWaterLayer('PIPES')
        if pipeLyr:
            self.layer = pipeLyr
            #if pipeLyr.selectedFeatureCount()>0:
            #    print('pipelyr definido e tem selecao')

    def prepare_PipesDialog(self):
        #Carrega Tubos 
        proj = QgsProject.instance()
        tubosMat=proj.readEntry(self.SETTINGS, "TUBOS_MAT","0")[0]
        if tubosMat=='0':#se nao tiver lista de materiais definidas carrega o padrao do modelo
            tubos=QWaterModel.TUBOS_MAT
        else:
            tubos=eval(tubosMat)
            if not isinstance(tubos[0][0], str):
                QgsMessageLog.logMessage('Wrong Pipes settings'+tubosMat,self.SETTINGS,Qgis.Warning) #Log Warning Message
                tubos=QWaterModel.TUBOS_MAT
        self.carregaTabMats(tubos)

    def carregaTabMats(self,tbMats):
        tableWidget=self.dlg.tableWidget #findChild(QTableWidget,'tableWidget')
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
        tableWidget.removeColumn(5) #remove unnecessary headloss column
        tableWidget.resizeColumnsToContents()      
    
    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(Qgis.GeometryType.Polygon)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)    
        
    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        self.showDialog(r, e)

    def showDialog(self, rect, event):        
        #self.clearRubberBand()
        if rect is None:
            searchRadius = self.canvas.mapUnitsPerPixel() * 5
            rectFinal=QgsGeometry.fromPointXY(self.endPoint).buffer(searchRadius,10) #buffer(distance , edgeCount)
        else:
            rectFinal=rect
        if self.layer:
            ids = [f.id() for f in self.layer.getFeatures() if f.geometry().intersects(rectFinal)]
            modf = event.modifiers()
            if modf == Qt.ShiftModifier:
                myBehavior = Qgis.SelectBehavior.AddToSelection
            elif modf == Qt.ControlModifier:
                myBehavior = Qgis.SelectBehavior.RemoveFromSelection
            else:
                myBehavior = Qgis.SelectBehavior.SetSelection                
            
            self.layer.selectByIds(ids, behavior=myBehavior)
            self.prepare_PipesDialog()
            
            self.dlg.show()
            self.dlg.tableWidget.setFocus()
            self.dlg.tableWidget.setCurrentCell(self.lastValidRow,3)

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset()
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())
        point5 = point1

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, False)
        self.rubberBand.addPoint(point5, True)
        # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif (self.startPoint.x() == self.endPoint.x() or \
              self.startPoint.y() == self.endPoint.y()):
            return None
        return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        self.rubberBand.reset()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
        #super().deactivate()
        