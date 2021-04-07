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


class Ui_widget(object):
    def setupUi(self, widget):
        if not widget.objectName():
            widget.setObjectName(u"widget")
        widget.resize(325, 340)
        self.button = QPushButton(widget)
        self.button.setObjectName(u"button")
        self.button.setGeometry(QRect(10, 90, 300, 75))
        self.input = QTextEdit(widget)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(10, 10, 300, 75))
        self.output = QTextBrowser(widget)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(10, 170, 300, 150))

        self.retranslateUi(widget)

        QMetaObject.connectSlotsByName(widget)
    # setupUi

    def retranslateUi(self, widget):
        widget.setWindowTitle(QCoreApplication.translate("widget", u"Form", None))
        self.button.setText(QCoreApplication.translate("widget", u"Say hello", None))
    # retranslateUi

