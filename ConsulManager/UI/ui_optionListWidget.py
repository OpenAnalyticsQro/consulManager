# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optionListWidgetMurZEk.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_optionListWidget(object):
    def setupUi(self, optionListWidget):
        if not optionListWidget.objectName():
            optionListWidget.setObjectName(u"optionListWidget")
        optionListWidget.resize(350, 56)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(optionListWidget.sizePolicy().hasHeightForWidth())
        optionListWidget.setSizePolicy(sizePolicy)
        optionListWidget.setMinimumSize(QSize(0, 56))
        optionListWidget.setMaximumSize(QSize(350, 56))
        optionListWidget.setStyleSheet(u"QFrame#mainFrameOption\n"
"{\n"
"background:transparent;\n"
"}\n"
"\n"
"QFrame#mainFrameOption::hover\n"
"{\n"
"background:rgba(83, 85, 168, 0.12);\n"
"}\n"
"\n"
"QLabel#optionIcon\n"
"{\n"
"background:transparent;\n"
"color:#777680;\n"
"font-family:Material Icons;\n"
"font-style: normal;\n"
"font-size: 32px;\n"
"line-height: 1px;\n"
"}\n"
"\n"
"QLabel#optionName\n"
"{\n"
"background:transparent;\n"
"font-family: 'Roboto';\n"
"font-style: normal;\n"
"font-weight: 400;\n"
"font-size: 16px;\n"
"line-height: 24px;\n"
"letter-spacing: 0.5px;\n"
"color: #1B1B1F;\n"
"}\n"
"\n"
"QLabel#optionPhone\n"
"{\n"
"background:transparent;\n"
"font-family: 'Roboto';\n"
"font-style: normal;\n"
"font-weight: 500;\n"
"font-size: 12px;\n"
"line-height: 16px;\n"
"letter-spacing: 0.5px;\n"
"color: #5355A8;\n"
"}")
        self.verticalLayout = QVBoxLayout(optionListWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainFrameOption = QFrame(optionListWidget)
        self.mainFrameOption.setObjectName(u"mainFrameOption")
        self.mainFrameOption.setFrameShape(QFrame.StyledPanel)
        self.mainFrameOption.setFrameShadow(QFrame.Raised)
        self.optionIcon = QLabel(self.mainFrameOption)
        self.optionIcon.setObjectName(u"optionIcon")
        self.optionIcon.setGeometry(QRect(12, 16, 24, 24))
        self.optionIcon.setMinimumSize(QSize(24, 24))
        self.optionIcon.setMaximumSize(QSize(24, 24))
        font = QFont()
        font.setFamilies([u"Material Icons"])
        font.setItalic(False)
        self.optionIcon.setFont(font)
        self.optionIcon.setAlignment(Qt.AlignCenter)
        self.optionName = QLabel(self.mainFrameOption)
        self.optionName.setObjectName(u"optionName")
        self.optionName.setGeometry(QRect(44, 8, 290, 24))
        self.optionName.setMinimumSize(QSize(0, 24))
        self.optionName.setMaximumSize(QSize(290, 24))
        self.optionPhone = QLabel(self.mainFrameOption)
        self.optionPhone.setObjectName(u"optionPhone")
        self.optionPhone.setGeometry(QRect(44, 32, 290, 16))
        self.optionPhone.setMinimumSize(QSize(0, 16))
        self.optionPhone.setMaximumSize(QSize(290, 16))

        self.verticalLayout.addWidget(self.mainFrameOption)


        self.retranslateUi(optionListWidget)

        QMetaObject.connectSlotsByName(optionListWidget)
    # setupUi

    def retranslateUi(self, optionListWidget):
        optionListWidget.setWindowTitle(QCoreApplication.translate("optionListWidget", u"Form", None))
        self.optionIcon.setText(QCoreApplication.translate("optionListWidget", u"\ue7fd", None))
        self.optionName.setText(QCoreApplication.translate("optionListWidget", u"Nuevo Cliente", None))
        self.optionPhone.setText(QCoreApplication.translate("optionListWidget", u"###", None))
    # retranslateUi

