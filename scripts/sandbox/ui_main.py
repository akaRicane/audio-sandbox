# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tuto_main.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(800, 599)
        self.mw_widget = QWidget(main)
        self.mw_widget.setObjectName(u"mw_widget")
        self.btn_run_widget = QPushButton(self.mw_widget)
        self.btn_run_widget.setObjectName(u"btn_run_widget")
        self.btn_run_widget.setGeometry(QRect(20, 480, 111, 61))
        self.visualizer = QGraphicsView(self.mw_widget)
        self.visualizer.setObjectName(u"visualizer")
        self.visualizer.setGeometry(QRect(10, 10, 771, 451))
        self.btn_run_analysis = QPushButton(self.mw_widget)
        self.btn_run_analysis.setObjectName(u"btn_run_analysis")
        self.btn_run_analysis.setGeometry(QRect(140, 480, 81, 51))
        self.output_log = QTextBrowser(self.mw_widget)
        self.output_log.setObjectName(u"output_log")
        self.output_log.setGeometry(QRect(230, 470, 551, 81))
        main.setCentralWidget(self.mw_widget)
        self.menubar = QMenuBar(main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main)
        self.statusbar.setObjectName(u"statusbar")
        main.setStatusBar(self.statusbar)

        self.retranslateUi(main)
        self.btn_run_analysis.clicked.connect(self.visualizer.update)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"MainWindow", None))
        self.btn_run_widget.setText(QCoreApplication.translate("main", u"Run MyWidget", None))
        self.btn_run_analysis.setText(QCoreApplication.translate("main", u"Run analysis", None))
    # retranslateUi

