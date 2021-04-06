# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tuto.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(324, 351)
        self.button = QPushButton(Form)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(10, 90, 300, 75))
        self.input = QTextEdit(Form)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(10, 10, 300, 75))
        self.output = QTextBrowser(Form)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(10, 170, 300, 150))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

