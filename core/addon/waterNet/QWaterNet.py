from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from ...QWater_00Common import *

ClassName='QWaterNet_addon'
class QWaterNet_addon(object):
    # Store settings in QGIS projects under this key
    SETTINGS ="QWater"
    FITS_FLDS = {
        'FITTING': QVariant.String,
        'FITT_ROT': QVariant.Double,
        'FITT_DN1': QVariant.Int,
        'FITT_DN2': QVariant.Int}
    FITTINGS = {1:'k',
                2:'c90',
                3:'te',
                4:'cruzeta',
                5:'c22',
                6:'c45',
                7:'rd'}
    progress = None
    progressMBar = None
    
    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        self.common=QWater_00Common()
        
    def tr(self, Texto):
        return QCoreApplication.translate(ClassName,Texto)

    def initGui(self):
        # create actions
        defIconPath=":/plugins/QWater/addon/waterNet/icons/fittings.svg"

        self.createFittings_Action = QAction(QIcon(defIconPath), self.tr('Create Fittings\'s'), self.iface.mainWindow())
    
        # Connect actions to triggers
        self.createFittings_Action.triggered.connect(self.createFittings)

        # Find QWater ToolBar
        for x in self.iface.mainWindow().findChildren(QToolBar): 
            # print x.windowTitle()
            if x.windowTitle() == '&QWater':
                #x.addWidget(iface.toolButton)
                self.toolbar = x               
        
        #Add separator
        #self.toolbar.addSeparator()
        
        #Add tool button
        self.toolbar.addAction(self.createFittings_Action)        
    
    def unload(self):
        # remove actions        
        self.toolbar.removeAction(self.createFittings_Action)
        del self.toolbar
    
    # Display message
    def warning(self, message, nivel=Qgis.Warning):
        self.iface.messageBar().pushMessage(self.SETTINGS, message, level=nivel, duration=4)
    
    def FeicaoSelecionaMostraAvisa(self,Layer,FeicaoID,aviso):
        Layer.select(FeicaoID)
        mapCanvas = iface.mapCanvas()
        mapCanvas.zoomToSelected(Layer)
        iface.messageBar().pushMessage("QWater:", aviso, level=Qgis.Warning, duration=4)
    
    def checkBefore_Run(self, junctLyr, pipeLyr):
        msg = self.tr('Field \'{}\' can NOT be empty! Use Make model tool first!')
        for feat in junctLyr.getFeatures():
            featID = feat.id()
            campo='DC_ID'
            nodeID = feat[campo]
            if not nodeID:
                self.FeicaoSelecionaMostraAvisa(junctLyr,featID, msg.format(campo))
                return False

        for feat in pipeLyr.getFeatures():
            featID = feat.id()
            campos=['DC_ID','NODE1','NODE2']
            for campo in campos:            
                nodeID = feat[campo]
                if not nodeID:
                    self.FeicaoSelecionaMostraAvisa(pipeLyr,featID, msg.format(campo))
                    return False
        return True
    
    def addMissingFields(self, layer):
        missing=[]
        provider = layer.dataProvider()
        for fname in self.FITS_FLDS:
            if -1 == provider.fieldNameIndex(fname):
                missing.append(fname)
                #print('field:',self.FITS_FLDS[fname])
        
        if missing and not layer.isEditable() and not layer.startEditing():
            self.warning(self.tr('ERROR: Unable to edit layer {} for add missing fields').format(layer.name()))
            return False
        
        if missing:
            attributes = []
            for missFlds in missing:            
                attributes.append(QgsField(missFlds, self.FITS_FLDS[missFlds]))
            success = provider.addAttributes(attributes)
            if not success:
                self.warning(self.tr('ERROR: Unable to add missing fields'))
                return success
            layer.updateFields()
            return success
        
    def addFittings(self, point_layer, line_layer):
        #point_layer - vector layer with points
        #line_layer - vector layer with lines

        iter_p=list(point_layer.getFeatures()) #features from point layer
        iter_l=list(line_layer.getFeatures()) #changing iterator to list to avoid exhaustion
        nroNos=len(iter_p)
        connections=0 #counter for number of intersections
        cont=0
        point_layer.startEditing()
        self.progress, self.progressMBar=self.common.startProgressBar(self.tr('Starting fittings calcution...'))
        for p in iter_p:
            DNs=[] #reset diameters
            cont+=1
            percent = int((cont/float(nroNos)) * 100)
            self.progress.setValue(percent)
            geom_p=p.geometry().buffer(0.2,6) #create a small buffer around points, 10 is an arbitrary value, change it according to precision of Your data
            connections=0 #reseting counter
            lines_geom=[]
            for l in iter_l:
                geom_l=l.geometry()
                if geom_p.intersects(geom_l):
                    connections=connections+1 # if intersection is true increase counter by one                    
                    DNs.append(l['DN']) # add intersected pipe DN to DNs set
                    lines_geom.append(geom_l)
            DNs=sorted(DNs, reverse=True)
            p['FITT_DN1']=DNs[0]
            if connections>1:
                p['FITT_DN2']=DNs[-1]
            else:
                p['FITT_DN2']=NULL
            bool, peca, rot=self.calcFittings(p.geometry(),lines_geom,connections,DNs,p['DC_ID'])
            campoFitting = list(self.FITS_FLDS.keys())[0]
            campoRot = list(self.FITS_FLDS.keys())[1]
            if bool:
                if p[campoFitting]!= 'IGNORE':
                    p[campoFitting]=peca
                    p[campoRot]=rot
            else:
                p[campoFitting]=None
                p[campoRot]=None
            point_layer.updateFeature(p)
        self.progressMBar.setText(self.tr('Fittings updated!'))
        #QApplication.processEvents()
        #import time
        #time.sleep(3)
        #iface.messageBar().clearWidgets()

    def geom2ptoList(self, geom):
        if geom.isMultipart():
            resp = geom.asMultiPolyline()[0]
        else:
            resp = geom.asPolyline()
        return resp

    def orderVertexByDist(self, pt, vertexList):
        dists=[]
        orderedVertex=[]
        for vert in vertexList:
            vertGeo=QgsGeometry.fromPointXY(vert)
            dists.append(QgsGeometry.distance(pt, vertGeo))
        orderedDists = sorted(dists)
        for dist in orderedDists:
            ind=dists.index(dist)
            valor=vertexList[ind]
            orderedVertex.append(valor)
        return orderedVertex
    
    def azimutePto2NearestLine(self, geom_p, line_geom):
        pt = geom_p.asPoint()
        geoList = self.geom2ptoList(line_geom)
        orderedVertex = self.orderVertexByDist(geom_p,geoList)
        nextPto = orderedVertex[1] #second nearest
        az = pt.azimuth(nextPto)
        if az<0:
            az=360+az
        return az            
    
    def curvaByDef(self, deflexao):
        if deflexao>16.875 and deflexao<=33.75:
            return 'c22'
        elif deflexao>33.75 and deflexao<=67.5:
            return 'c45'
        elif deflexao>67.5 and deflexao<=100:
            return 'c90'
        else:
            return ''
    
    def calcFittings(self,geom_p,lines_geom,connCount,DNs, id):        
        if connCount== 1: #k (cap)
            az=self.azimutePto2NearestLine(geom_p,lines_geom[0])
            return True, 'k', az
        elif connCount== 2: #curves or reductions
            az0=self.azimutePto2NearestLine(geom_p,lines_geom[0])
            az1=self.azimutePto2NearestLine(geom_p,lines_geom[1])
            difabs = abs(az1-az0)
            if difabs>180:
                angInt=360-difabs
            else:
                angInt=difabs
            defl=180-angInt
            peca = self.curvaByDef(defl)
            if peca: #45 < angInt < 135:
                bool=True
                azmed = ((az0+az1)/2)
                angs=abs(az1-azmed)+abs(azmed-az0)
                sup= 180 if angs>180 else 0
                ang=((az0+az1)/2)+135+sup
                if peca=='c45':
                    ang-=30
                elif peca=='c22':
                    ang-=30
            else:
                if DNs[0]!=DNs[-1]:
                    bool=True
                    peca='rd'
                    ang = az0
                else:
                    bool=False
                    ang=9999                
            return bool, peca, ang
        elif connCount== 3: #te
            az0=self.azimutePto2NearestLine(geom_p,lines_geom[0])
            az1=self.azimutePto2NearestLine(geom_p,lines_geom[1])
            az2=self.azimutePto2NearestLine(geom_p,lines_geom[2])
            azList=sorted([az0,az1,az2])
            az0=azList[0]
            az1=azList[1]
            az2=azList[2]
            
            dif10=abs(abs(az1-az0)-180)
            dif20=abs(abs(az2-az0)-180)
            dif21=abs(abs(az2-az1)-180)
            
            if dif10<dif20:
                if dif10<dif21:
                    ang=az1+(90 if az1< az2 else -90)
                else:
                    ang=az1+(90 if az1> az2 else -90)
            else:
                if dif20<dif21:
                    ang=az2+(90 if az1<az0 else -90)
                else:
                    ang=az2+(90 if az1> az0 else -90)
            return True, 'te', ang
        elif connCount== 4: #cruzeta
            az0=self.azimutePto2NearestLine(geom_p,lines_geom[0])
            return True, 'cruzeta', az0
        else:
            return False, '', 9999
                
    def createFittings(self):
        nodeLayer = self.common.PegaQWaterLayer('JUNCTIONS')
        if not nodeLayer:
            return False
        pipeLyr = self.common.PegaQWaterLayer('PIPES')
        if not pipeLyr:
            return False        
        if not self.checkBefore_Run(nodeLayer,pipeLyr):
            return False
        
        from ...QWaterPlugin import QWaterPlugin
        QWaterPlugin.update_DN(self) #Create and update DN field
        
        self.addMissingFields(nodeLayer)        
        self.addFittings(nodeLayer, pipeLyr)
        
        # muda o estilo para fittings
        style_manager = nodeLayer.styleManager()

        # read valid style from layer
        style = QgsMapLayerStyle()
        style.readFromLayer(nodeLayer)
        
        style_manager.setCurrentStyle('Fittings')

