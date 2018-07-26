from builtins import object
#
# This file is part of QWater
#
# QWater_00Model.py - Standand variables for QWater plugin
#
# Copyright 2017 - 2017 Jorge Almerio <jorgealmerio@yahoo.com.br>
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

# Describe the model structure
from qgis.PyQt.QtCore import *

class QWaterModel(object):
    # Pipes ['On','DN','Diameter','Roughness','Pressure','Referencia']
    TUBOS_MAT=[[1,50.,54.6,1.0,60.0,'PVC PBA CL12 JEI'],
               [1,50.,53.4,1.0,75.0,'PVC PBA CL15 JEI'],
               [1,50.,51.4,1.0,100.0,'PVC PBA CL20 JEI'],
               [1,75.,77.2,1.0,60.0,'PVC PBA CL12 JEI'],
               [1,75.,75.6,1.0,75.0,'PVC PBA CL15 JEI'],
               [1,75.,72.8,1.0,100.0,'PVC PBA CL20 JEI'],
               [1,100.,100.0,1.0,60.0,'PVC PBA CL12 JEI'],
               [1,100.,97.8,1.0,75.0,'PVC PBA CL15 JEI'],
               [1,100.,94.4,1.0,100.0,'PVC PBA CL20 JEI'],
               [1,100.,108.4,1.0,100.0,'PVC DEFoFo'],
               [1,150.,156.4,1.0,100.0,'PVC DEFoFo'],
               [1,200.,204.2,1.0,100.0,'PVC DEFoFo'],
               [1,250.,252.0,1.0,100.0,'PVC DEFoFo'],
               [1,300.,299.8,1.0,100.0,'PVC DEFoFo'],
               [1,350.,347.6,1.0,100.0,'PVC DEFoFo'],
               [1,400.,394.6,1.0,100.0,'PVC DEFoFo'],
               [1,500.,489.4,1.0,100.0,'PVC DEFoFo']]
    # Parameters and default values
    DATA_DEFS = {'POPINI':'0',
                 'POPFIM':'0',
                 'DIAM_MIN':'50',
                 'COVER_MIN':'0.60',
                 'PERCAPTA':'150',
                 'K1_DIA':'1.2',
                 'K2_HORA':'1.5',
                 'COEF_ATEND':'1.0'}

    # Preferred column types
    COLUMN_TYPES = {
        'DC_ID': QVariant.String,
        'DIAMETER': QVariant.Double,
        'DEMAND': QVariant.Double,
        'ELEVATION': QVariant.Double,
        'HEAD': QVariant.Double,
        'LENGTH': QVariant.Double,
        'INITIALLEV': QVariant.Double,
        'MAXIMUMLEV': QVariant.Double,
        'MINIMUMLEV': QVariant.Double,
        'MINIMUMVOL': QVariant.Double,
        'MINORLOSS': QVariant.Double,
        'NODE1': QVariant.String,
        'NODE2': QVariant.String,
        'PATTERN': QVariant.String,
        'PROPERTIES':QVariant.String,
        'ROUGHNESS': QVariant.Double, #Almerio: mudei esse campo de String para Double
        'SETTING': QVariant.String,
        'STATUS': QVariant.String,
        'TYPE': QVariant.String,
        'VOLUMECURV': QVariant.String
        }
