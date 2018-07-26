from builtins import object
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created: Sat Jan  4 02:51:18 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QDialogButtonBox, QTabWidget, QWidget, QTextBrowser, QComboBox, QLabel, QSizePolicy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QCoreQApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QCoreApplication.translate(context, text, disambig)

class Ui_GHydraulicsResultDialog(object):
    def setupUi(self, GHydraulicsResultDialog):
        GHydraulicsResultDialog.setObjectName(_fromUtf8("GHydraulicsResultDialog"))
        GHydraulicsResultDialog.resize(640, 480)
        self.buttonBox = QDialogButtonBox(GHydraulicsResultDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 620, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QTabWidget(GHydraulicsResultDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 620, 390))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabOutput = QWidget()
        self.tabOutput.setObjectName(_fromUtf8("tabOutput"))
        self.textOutput = QTextBrowser(self.tabOutput)
        self.textOutput.setGeometry(QtCore.QRect(10, 10, 600, 340))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textOutput.sizePolicy().hasHeightForWidth())
        self.textOutput.setSizePolicy(sizePolicy)
        self.textOutput.setObjectName(_fromUtf8("textOutput"))
        self.tabWidget.addTab(self.tabOutput, _fromUtf8(""))
        self.tabReport = QWidget()
        self.tabReport.setObjectName(_fromUtf8("tabReport"))
        self.textReport = QTextBrowser(self.tabReport)
        self.textReport.setGeometry(QtCore.QRect(10, 10, 600, 340))
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textReport.sizePolicy().hasHeightForWidth())
        self.textReport.setSizePolicy(sizePolicy)
        self.textReport.setObjectName(_fromUtf8("textReport"))
        self.tabWidget.addTab(self.tabReport, _fromUtf8(""))
        self.comboStep = QComboBox(GHydraulicsResultDialog)
        self.comboStep.setGeometry(QtCore.QRect(150, 410, 80, 27))
        self.comboStep.setObjectName(_fromUtf8("comboStep"))
        self.labelStep = QLabel(GHydraulicsResultDialog)
        self.labelStep.setGeometry(QtCore.QRect(10, 415, 120, 17))
        self.labelStep.setObjectName(_fromUtf8("labelStep"))

        self.retranslateUi(GHydraulicsResultDialog)
        self.tabWidget.setCurrentIndex(0)
        
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GHydraulicsResultDialog.accept)
        self.buttonBox.accepted.connect(GHydraulicsResultDialog.accept)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GHydraulicsResultDialog.reject)
        self.buttonBox.rejected.connect(GHydraulicsResultDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GHydraulicsResultDialog)

    def retranslateUi(self, GHydraulicsResultDialog):
        GHydraulicsResultDialog.setWindowTitle(_translate("GHydraulicsResultDialog", "EPANET Results", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOutput), _translate("GHydraulicsResultDialog", "EPANET Output", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReport), _translate("GHydraulicsResultDialog", "Report", None))
        self.labelStep.setText(_translate("GHydraulicsResultDialog", "Load time step", None))

