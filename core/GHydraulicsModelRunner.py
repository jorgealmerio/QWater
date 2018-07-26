from __future__ import absolute_import
from builtins import str
#
# This file is part of GHydraulics
#
# GHydraulictModelRunner.py - Run EPANET models
#
# Copyright 2013-2014 Steffen Macke <sdteffen@sdteffen.de>
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

import array
import platform
import tempfile
import os
import subprocess

from .GHydraulicsCommon import *
from .GHydraulicsException import *
from .GHydraulicsModel import *
from .EpanetResultReader import *

# Run EPANET models
class GHydraulicsModelRunner(GHydraulicsCommon):

    # Run the EPANET simulation, return output and report, number of steps
    def run(self, filename):
        report = tempfile.mkstemp(suffix='.txt')
        os.close(report[0])
        binary = tempfile.mkstemp(suffix='.bin')
        os.close(binary[0])
        out = tempfile.mkstemp(suffix='.out')
        os.fstat(out[0])
        err = tempfile.mkstemp(suffix='.err')
        os.fstat(err[0])
        input = tempfile.mkstemp(suffix='.input')
        os.fstat(input[0])
        self.log(str(subprocess.call([self.epanet, filename, report[1], binary[1]], cwd=tempfile.gettempdir(), stdin=input[0], stdout=out[0], stderr=err[0])))
        os.close(input[0])
        self.deleteIfExists(input[1])
        os.close(out[0])
        os.close(err[0])
        o = open(out[1], 'r')
        output = o.read()
        o.close()
        os.unlink(out[1])
        e = open(err[1], 'r')
        errors = e.read()
        if 0 < len(errors):
            self.log('ERRORS')
            self.log(errors)
        e.close()
        self.deleteIfExists(err[1])
        r = open(report[1], 'r')
        report = r.read()
        r.close()
        steps = 0
        success = True
        try:
            e = EpanetResultReader(binary[1])
        except EOFError as ex:
            success = False
        if success:
            self.log('Number of nodes: '+str(e.ia[e.NODECOUNT]))
            self.log('Number of links: '+str(e.ia[e.LINKCOUNT]))
            self.log('Number of tanks: ' +str(e.ia[e.TANKCOUNT]))
            self.log('Number of pumps: '+str(e.ia[e.PUMPCOUNT]))
            self.log('Report start: '+str(e.ia[e.REPORTSTART]))
            self.log('Report time step: '+str(e.ia[e.REPORTTIMESTEP]))
            self.log('Simulation duration: '+str(e.ia[e.DURATION]))
            steps = e.ia[e.DURATION]//e.ia[e.REPORTTIMESTEP]+1
            self.log('Number of periods: '+str(steps))
        e.close()
        self.deleteIfExists(binary[1])
        self.deleteIfExists(report[1])
        self.e = e
        return output, report, steps

    # Delete a file if it exists
    def deleteIfExists(self, file):
        if os.path.isfile(file):
            try:
                os.unlink(file)
            except:
                self.log('Failed to delete file: '+file)

    # Fill the attribute tables
    def setStepResults(self, step, sections, results, getter):
        for section in sections:
            # loop over all layers
            if section not in self.layers:
                continue
            for name in self.layers[section]:
                maplayers = QgsProject.instance().mapLayers()
                for l,layer in maplayers.items():
                    if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                        provider = layer.dataProvider()
                        if not layer.isEditable() and not layer.startEditing():
                            raise GHydraulicsException('ERROR: Unable to edit layer '+name)
                        layer.beginEditCommand('Loading step '+str(step))
                        attributes = []
                        # loop over result fields
                        for fieldname in results:
                            if -1 == provider.fieldNameIndex(fieldname):
                                attributes.append(QgsField(fieldname, QVariant.Double))
                        provider.addAttributes(attributes)
                        layer.updateFields()
                        idx = {}
                        for fieldname in results:
                            idx[fieldname] = provider.fieldNameIndex(fieldname)
                        ididx = provider.fieldNameIndex(GHydraulicsModel.ID_FIELD)
                        # loop over features
                        iter = layer.getFeatures()
                        for feature in iter:
                            results = getter(step, feature.attributes()[ididx])
                            for fieldname, result in results.items():
                                layer.changeAttributeValue(feature.id(), idx[fieldname], result)
                        layer.endEditCommand()

    # Save the results of a given timestep to the layers
    def setStep(self, step):
        self.beginEditCommand('Loading Step '+str(step+1))
        # node results
        self.setStepResults(step, EpanetModel.COORDINATE_SECTIONS, GHydraulicsModel.NODE_RESULTS, self.e.getNodeResult)
        # link results
        self.setStepResults(step, EpanetModel.LINK_SECTIONS, GHydraulicsModel.LINK_RESULTS, self.e.getLinkResult)
        self.endEditCommand()

    # Determine the EPANET binary to use
    def __init__(self):
        if '' != platform.mac_ver()[0]:
            self.epanet = 'osx/epanet2d'
        else:
            a = platform.architecture()
            self.epanet = a[0]+'/'+a[1]+'/epanet2d'
            if 'WindowsPE' == a[1]:
                self.epanet = self.epanet + '.exe'
        self.epanet = os.path.dirname(__file__)+'/bin/' + self.epanet
        if not os.path.isfile(self.epanet):
            raise GHydraulicsException('Could not determine EPANET executable. Please send an email with information about your platform to sdteffen@gmail.com (or use the bug tracker).')
        try:
            os.chmod(self.epanet, 0o755)
        except:
            raise GHydraulicsException('Failed to make '+self.epanet+' excecutable.')
        self.log(self.epanet)
        self.getLayers()
