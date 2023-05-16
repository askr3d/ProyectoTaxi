# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'subwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(814, 605)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_14 = QGridLayout(self.groupBox_3)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.frame_superior = QFrame(self.groupBox_3)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setMinimumSize(QSize(0, 40))
        self.frame_superior.setMaximumSize(QSize(16777215, 40))
        self.frame_superior.setStyleSheet(u"background-color: rgb(19, 86, 120);")
        self.frame_superior.setFrameShape(QFrame.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_superior)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_28 = QLabel(self.frame_superior)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.label_28)

        self.horizontalSpacer = QSpacerItem(656, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_cerrar = QPushButton(self.frame_superior)
        self.btn_cerrar.setObjectName(u"btn_cerrar")
        self.btn_cerrar.setMaximumSize(QSize(16777215, 35))
        self.btn_cerrar.setStyleSheet(u"QPushButton{\n"
"border-radius:7px;\n"
"background-color: rgb(60, 100, 120);\n"
"}\n"
"QPushButton:hover{\n"
"	border:10px solid rgb(50, 83, 100);\n"
"	\n"
"	background-color: rgb(255, 255, 255);\n"
"\n"
"}")
        icon = QIcon()
        icon.addFile(u"images/51517.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_cerrar.setIcon(icon)
        self.btn_cerrar.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.btn_cerrar)


        self.gridLayout_14.addWidget(self.frame_superior, 0, 0, 1, 1)

        self.frame_26 = QFrame(self.groupBox_3)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMaximumSize(QSize(16777215, 190))
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_26)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.groupBox_31 = QGroupBox(self.frame_26)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.groupBox_31.setMinimumSize(QSize(0, 190))
        self.groupBox_31.setMaximumSize(QSize(16777215, 190))
        font = QFont()
        font.setPointSize(10)
        self.groupBox_31.setFont(font)
        self.horizontalLayout_29 = QHBoxLayout(self.groupBox_31)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, -1)
        self.horizontalSpacer_35 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_35)

        self.frame_38 = QFrame(self.groupBox_31)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)
        self.gridLayout_30 = QGridLayout(self.frame_38)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.frame_39 = QFrame(self.frame_38)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setMinimumSize(QSize(315, 141))
        self.frame_39.setMaximumSize(QSize(301, 141))
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_39)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.groupBox_32 = QGroupBox(self.frame_39)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.gridLayout_32 = QGridLayout(self.groupBox_32)
        self.gridLayout_32.setSpacing(0)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_41 = QVBoxLayout()
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_20)

        self.label_14 = QLabel(self.groupBox_32)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(60, 60))
        self.label_14.setPixmap(QPixmap(u"images/949663.png"))
        self.label_14.setScaledContents(True)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_31.addWidget(self.label_14)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_5)


        self.verticalLayout_41.addLayout(self.horizontalLayout_31)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_27)

        self.label_88 = QLabel(self.groupBox_32)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setFont(font)

        self.horizontalLayout.addWidget(self.label_88)

        self.ledt_pasajeros_nombre = QLineEdit(self.groupBox_32)
        self.ledt_pasajeros_nombre.setObjectName(u"ledt_pasajeros_nombre")
        self.ledt_pasajeros_nombre.setMinimumSize(QSize(170, 0))

        self.horizontalLayout.addWidget(self.ledt_pasajeros_nombre)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_29)


        self.verticalLayout_41.addLayout(self.horizontalLayout)


        self.gridLayout_32.addLayout(self.verticalLayout_41, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.groupBox_32, 0, 0, 1, 1)


        self.gridLayout_30.addWidget(self.frame_39, 0, 0, 1, 1)


        self.horizontalLayout_29.addWidget(self.frame_38)

        self.frame_40 = QFrame(self.groupBox_31)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_40)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalSpacer_19 = QSpacerItem(17, 27, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_19)

        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.btn_agregar_pasajero = QPushButton(self.frame_40)
        self.btn_agregar_pasajero.setObjectName(u"btn_agregar_pasajero")
        self.btn_agregar_pasajero.setMinimumSize(QSize(80, 25))
        self.btn_agregar_pasajero.setStyleSheet(u"QPushButton{\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	background-color: rgb(60, 115, 120);\n"
"	\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(0, 85, 120);\n"
"}")

        self.verticalLayout_39.addWidget(self.btn_agregar_pasajero)


        self.verticalLayout_40.addLayout(self.verticalLayout_39)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_2)


        self.horizontalLayout_29.addWidget(self.frame_40)

        self.frame_47 = QFrame(self.groupBox_31)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setFrameShape(QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.gridLayout_33 = QGridLayout(self.frame_47)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.frame_48 = QFrame(self.frame_47)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setMinimumSize(QSize(315, 141))
        self.frame_48.setMaximumSize(QSize(301, 141))
        self.frame_48.setFrameShape(QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_48)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.groupBox_33 = QGroupBox(self.frame_48)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.gridLayout_34 = QGridLayout(self.groupBox_33)
        self.gridLayout_34.setSpacing(0)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_42 = QVBoxLayout()
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_22)

        self.label_32 = QLabel(self.groupBox_33)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMaximumSize(QSize(60, 60))
        self.label_32.setPixmap(QPixmap(u"images/10733323.png"))
        self.label_32.setScaledContents(True)

        self.horizontalLayout_32.addWidget(self.label_32)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_21)


        self.verticalLayout_42.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_28)

        self.label_97 = QLabel(self.groupBox_33)
        self.label_97.setObjectName(u"label_97")
        self.label_97.setFont(font)

        self.horizontalLayout_30.addWidget(self.label_97)

        self.ledt_pasajeros_destino = QLineEdit(self.groupBox_33)
        self.ledt_pasajeros_destino.setObjectName(u"ledt_pasajeros_destino")
        self.ledt_pasajeros_destino.setMinimumSize(QSize(170, 0))

        self.horizontalLayout_30.addWidget(self.ledt_pasajeros_destino)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_30)


        self.verticalLayout_42.addLayout(self.horizontalLayout_30)


        self.gridLayout_34.addLayout(self.verticalLayout_42, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.groupBox_33, 0, 0, 1, 1)


        self.gridLayout_33.addWidget(self.frame_48, 0, 0, 1, 1)


        self.horizontalLayout_29.addWidget(self.frame_47)

        self.horizontalSpacer_38 = QSpacerItem(39, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_38)


        self.verticalLayout_38.addWidget(self.groupBox_31)


        self.gridLayout_14.addWidget(self.frame_26, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.groupBox_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.frame_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.groupBox_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabla_pasajeros = QTableWidget(self.frame_6)
        if (self.tabla_pasajeros.columnCount() < 2):
            self.tabla_pasajeros.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabla_pasajeros.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabla_pasajeros.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tabla_pasajeros.setObjectName(u"tabla_pasajeros")
        self.tabla_pasajeros.setMinimumSize(QSize(0, 239))
        self.tabla_pasajeros.setStyleSheet(u"QTableWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(60, 115, 120);\n"
"	color: rgb(255, 255, 255);\n"
"	font-size:10pt;\n"
"}")

        self.gridLayout_3.addWidget(self.tabla_pasajeros, 0, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.frame_6)

        self.groupBox_30 = QGroupBox(self.groupBox_4)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.groupBox_30.setMinimumSize(QSize(0, 40))
        self.groupBox_30.setStyleSheet(u"background-color: rgb(60, 100, 120);")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_30)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(119, 18, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addWidget(self.groupBox_30)


        self.gridLayout_2.addWidget(self.groupBox_4, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_2, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)


        self.retranslateUi(Form)
        self.btn_cerrar.clicked.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_3.setTitle("")
        self.label_28.setText(QCoreApplication.translate("Form", u"     Pasajeros", None))
        self.btn_cerrar.setText("")
        self.groupBox_31.setTitle(QCoreApplication.translate("Form", u"Registro", None))
        self.groupBox_32.setTitle("")
        self.label_14.setText("")
        self.label_88.setText(QCoreApplication.translate("Form", u"Nombre:  ", None))
        self.btn_agregar_pasajero.setText(QCoreApplication.translate("Form", u"Agregar", None))
        self.groupBox_33.setTitle("")
        self.label_32.setText("")
        self.label_97.setText(QCoreApplication.translate("Form", u"Destino:  ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Consulta", None))
        ___qtablewidgetitem = self.tabla_pasajeros.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Nombre", None));
        ___qtablewidgetitem1 = self.tabla_pasajeros.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Destino", None));
        self.groupBox_30.setTitle("")
    # retranslateUi

