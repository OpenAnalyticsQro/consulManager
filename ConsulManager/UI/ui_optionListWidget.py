# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optionListWidgetOOqAFy.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QSizePolicy, QWidget)

class Ui_optionListWidget(object):
    def setupUi(self, optionListWidget):
        if not optionListWidget.objectName():
            optionListWidget.setObjectName(u"optionListWidget")
        optionListWidget.resize(220, 48)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(optionListWidget.sizePolicy().hasHeightForWidth())
        optionListWidget.setSizePolicy(sizePolicy)
        optionListWidget.setMinimumSize(QSize(0, 48))
        optionListWidget.setMaximumSize(QSize(1000, 48))
        optionListWidget.setStyleSheet(u"QFrame#mainFrame\n"
"{\n"
"background:red;\n"
"}")
        self.mainFrame = QFrame(optionListWidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setGeometry(QRect(0, 0, 101, 48))
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setMinimumSize(QSize(0, 48))
        self.mainFrame.setMaximumSize(QSize(1000, 48))
        self.mainFrame.setFrameShape(QFrame.NoFrame)
        self.mainFrame.setFrameShadow(QFrame.Plain)

        self.retranslateUi(optionListWidget)

        QMetaObject.connectSlotsByName(optionListWidget)
    # setupUi

    def retranslateUi(self, optionListWidget):
        optionListWidget.setWindowTitle(QCoreApplication.translate("optionListWidget", u"Form", None))
    # retranslateUi

