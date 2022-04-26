# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'listConsultasgcxyDn.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_consulList(object):
    def setupUi(self, consulList):
        if not consulList.objectName():
            consulList.setObjectName(u"consulList")
        consulList.resize(300, 410)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(consulList.sizePolicy().hasHeightForWidth())
        consulList.setSizePolicy(sizePolicy)
        consulList.setMinimumSize(QSize(300, 410))
        consulList.setMaximumSize(QSize(300, 410))
        consulList.setStyleSheet(u"QWidget\n"
"{\n"
"background:red;\n"
"}\n"
"\n"
"QFrame#FrameBase\n"
"{\n"
"background:#FFFBFF;\n"
"border-radius: 16px;\n"
"}\n"
"\n"
"QFrame#mainFrame\n"
"{\n"
"background:rgba(83, 85, 168, 20);\n"
"\n"
"border-radius: 16px;\n"
"\n"
"}\n"
"\n"
"QFrame#buttonFrame\n"
"{\n"
"background:none;\n"
"}\n"
"\n"
"QFrame#dataFrame\n"
"{\n"
"background:None;\n"
"\n"
"border-bottom-width: 1px;\n"
"border-style: solid;\n"
"border-bottom-color: #E4E1EC;\n"
"}\n"
"\n"
"QFrame#dataButtonFrame\n"
"{\n"
"background:none;\n"
"}\n"
"\n"
"QLabel#iconLabel\n"
"{\n"
"background:None;\n"
"color:#5355A8;\n"
"font-family:Material Icons;\n"
"font-style: normal;\n"
"font-size: 26px;\n"
"}\n"
"\n"
"QLineEdit#searchEdit {\n"
"color:#5355A8;\n"
"font-family: 'Roboto';\n"
"background: transparent;\n"
"border:none;\n"
"font-weight: 500;\n"
"font-size: 14px;\n"
"line-height: 20px;\n"
"}\n"
"\n"
"QScrollArea#scrollAreaList\n"
"{\n"
"background:transparent;\n"
"border:None;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"background:None;\n"
"bord"
                        "er:None;\n"
"width: 0px;\n"
"}\n"
"\n"
"QWidget#listScroll\n"
"{\n"
"background:transparent;\n"
"\n"
"}\n"
"\n"
"QFrame#itemFrame\n"
"{\n"
"background:none;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"background:None;\n"
"}\n"
"\n"
"")
        self.FrameBase = QFrame(consulList)
        self.FrameBase.setObjectName(u"FrameBase")
        self.FrameBase.setGeometry(QRect(0, 0, 245, 400))
        self.FrameBase.setMinimumSize(QSize(125, 56))
        self.FrameBase.setMaximumSize(QSize(245, 400))
        self.FrameBase.setFrameShape(QFrame.StyledPanel)
        self.FrameBase.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.FrameBase)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainFrame = QFrame(self.FrameBase)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.dataFrame = QFrame(self.mainFrame)
        self.dataFrame.setObjectName(u"dataFrame")
        self.dataFrame.setMaximumSize(QSize(245, 334))
        self.dataFrame.setFrameShape(QFrame.StyledPanel)
        self.dataFrame.setFrameShadow(QFrame.Raised)
        self.scrollAreaList = QScrollArea(self.dataFrame)
        self.scrollAreaList.setObjectName(u"scrollAreaList")
        self.scrollAreaList.setGeometry(QRect(3, 9, 239, 331))
        self.scrollAreaList.setMaximumSize(QSize(239, 331))
        self.scrollAreaList.setWidgetResizable(True)
        self.listScroll = QWidget()
        self.listScroll.setObjectName(u"listScroll")
        self.listScroll.setGeometry(QRect(0, 0, 239, 331))
        self.listScroll.setMaximumSize(QSize(16777215, 16777215))
        self.optionsLayout = QVBoxLayout(self.listScroll)
        self.optionsLayout.setSpacing(0)
        self.optionsLayout.setObjectName(u"optionsLayout")
        self.optionsLayout.setContentsMargins(0, 0, 0, 0)
        self.itemFrame = QFrame(self.listScroll)
        self.itemFrame.setObjectName(u"itemFrame")
        self.itemFrame.setEnabled(True)
        self.itemFrame.setMaximumSize(QSize(239, 16777215))
        self.itemFrame.setFrameShape(QFrame.StyledPanel)
        self.itemFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.itemFrame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.optionsLayout.addWidget(self.itemFrame)

        self.verticalSpacer = QSpacerItem(20, 38, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.optionsLayout.addItem(self.verticalSpacer)

        self.scrollAreaList.setWidget(self.listScroll)

        self.verticalLayout_2.addWidget(self.dataFrame)

        self.buttonFrame = QFrame(self.mainFrame)
        self.buttonFrame.setObjectName(u"buttonFrame")
        self.buttonFrame.setMinimumSize(QSize(0, 56))
        self.buttonFrame.setMaximumSize(QSize(16777215, 56))
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.dataButtonFrame = QFrame(self.buttonFrame)
        self.dataButtonFrame.setObjectName(u"dataButtonFrame")
        self.dataButtonFrame.setEnabled(True)
        self.dataButtonFrame.setGeometry(QRect(16, 8, 209, 40))
        self.dataButtonFrame.setMinimumSize(QSize(89, 40))
        self.dataButtonFrame.setMaximumSize(QSize(209, 40))
        self.dataButtonFrame.setFrameShape(QFrame.StyledPanel)
        self.dataButtonFrame.setFrameShadow(QFrame.Raised)
        self.iconLabel = QLabel(self.dataButtonFrame)
        self.iconLabel.setObjectName(u"iconLabel")
        self.iconLabel.setGeometry(QRect(0, 0, 40, 40))
        self.iconLabel.setMinimumSize(QSize(40, 40))
        self.iconLabel.setMaximumSize(QSize(40, 40))
        self.iconLabel.setAlignment(Qt.AlignCenter)
        self.searchEdit = QLineEdit(self.dataButtonFrame)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setGeometry(QRect(40, 10, 160, 20))
        self.searchEdit.setMinimumSize(QSize(35, 20))
        self.searchEdit.setMaximumSize(QSize(160, 20))
        self.searchEdit.setCursorPosition(0)
        self.searchEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.buttonFrame)


        self.verticalLayout.addWidget(self.mainFrame)


        self.retranslateUi(consulList)

        QMetaObject.connectSlotsByName(consulList)
    # setupUi

    def retranslateUi(self, consulList):
        consulList.setWindowTitle(QCoreApplication.translate("consulList", u"Form", None))
        self.iconLabel.setText(QCoreApplication.translate("consulList", u"\ue145", None))
        self.searchEdit.setText(QCoreApplication.translate("consulList", u"Nueva", None))
    # retranslateUi

