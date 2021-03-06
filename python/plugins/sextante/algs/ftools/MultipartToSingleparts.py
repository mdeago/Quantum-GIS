# -*- coding: utf-8 -*-

"""
***************************************************************************
    MultipartToSingleparts.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

from PyQt4.QtCore import *

from qgis.core import *

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from sextante.core.QGisLayers import QGisLayers

from sextante.parameters.ParameterVector import ParameterVector

from sextante.outputs.OutputVector import OutputVector

class MultipartToSingleparts(GeoAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    #===========================================================================
    # def getIcon(self):
    #    return QtGui.QIcon(os.path.dirname(__file__) + "/icons/multi_to_single.png")
    #===========================================================================

    def defineCharacteristics(self):
        self.name = "Multipart to singleparts"
        self.group = "Vector geometry tools"

        self.addParameter(ParameterVector(self.INPUT, "Input layer"))
        self.addOutput(OutputVector(self.OUTPUT, "Output layer"))

    def processAlgorithm(self, progress):
        layer = QGisLayers.getObjectFromUri(self.getParameterValue(self.INPUT))

        provider = layer.dataProvider()

        geomType = self.multiToSingleGeom(provider.geometryType())

        writer = self.getOutputFromName(self.OUTPUT).getVectorWriter(layer.pendingFields(),
                     geomType, layer.crs())

        outFeat = QgsFeature()
        inGeom = QgsGeometry()

        current = 0
        features = QGisLayers.features(layer)
        total = 100.0 / float(len(features))
        for inFeat in features:
            inGeom = inFeat.geometry()
            atMap = inFeat.attributes()

            features = self.extractAsSingle(inGeom)
            outFeat.setAttributes(atMap)

            for f in features:
                outFeat.setGeometry(f)
                writer.addFeature(outFeat)

            current += 1
            progress.setPercentage(int(current * total))

        del writer


    def multiToSingleGeom(self, wkbType):
        try:
            if wkbType in (QGis.WKBPoint, QGis.WKBMultiPoint,
                            QGis.WKBPoint25D, QGis.WKBMultiPoint25D):
                return QGis.WKBPoint
            elif wkbType in (QGis.WKBLineString, QGis.WKBMultiLineString,
                              QGis.WKBMultiLineString25D, QGis.WKBLineString25D):
                return QGis.WKBLineString
            elif wkbType in (QGis.WKBPolygon, QGis.WKBMultiPolygon,
                              QGis.WKBMultiPolygon25D, QGis.WKBPolygon25D):
                return QGis.WKBPolygon
            else:
                return QGis.WKBUnknown
        except Exception, err:
            raise GeoAlgorithmExecutionException(unicode(err))

    def extractAsSingle(self, geom):
        multiGeom = QgsGeometry()
        geometries = []
        if geom.type() == QGis.Point:
            if geom.isMultipart():
                multiGeom = geom.asMultiPoint()
                for i in multiGeom:
                    geometries.append(QgsGeometry().fromPoint(i))
            else:
                geometries.append(geom)
        elif geom.type() == QGis.Line:
            if geom.isMultipart():
                multiGeom = geom.asMultiPolyline()
                for i in multiGeom:
                    geometries.append(QgsGeometry().fromPolyline(i))
            else:
                geometries.append(geom)
        elif geom.type() == QGis.Polygon:
            if geom.isMultipart():
                multiGeom = geom.asMultiPolygon()
                for i in multiGeom:
                    geometries.append(QgsGeometry().fromPolygon(i))
            else:
                geometries.append(geom)
        return geometries
