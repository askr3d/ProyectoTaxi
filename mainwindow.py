from ui_mainwindow import *
from ui_subwindow import Ui_Form
import psycopg2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPropertyAnimation

from OperacionesDB import OperacionesDB
import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.actualizar_fecha()
        self.costo_kilometro = 0
        
        self.db = OperacionesDB()
        # Botones_tablas
        # self.ui.btn_act = QPushButton("Actualizar", self)
        # self.btn_pasajeros = QPushButton("Pasajeros", self)
        # self.btn_eliminar = QPushButton("Eliminar", self)
        
        # Crear una instancia de la subventana
        self.subventana = QDialog(self)
        self.subventana_ui = Ui_Form()
        self.subventana_ui.setupUi(self.subventana)
        self.subventana.setWindowFlag(Qt.FramelessWindowHint)
        self.subventana.setWindowOpacity(1)        
        
        # Objeto conexion con la base de datos
        """
        try:
            self.conexion = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'password',
                database = 'ProyectoTaxis'
            )
        except:
            print("Error al conectar la base de datos")
            exit()
        """
        # Eventos ----------------------------------------------------------------
        
        # Eliminar barra de titulo
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        

        # Sizerip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        
        # Mover ventana
        self.ui.frame_superior.mouseMoveEvent =  self.mover_ventana # Hacer funcion 
        
        # Acceder a las paginas
        self.ui.btn_inicio.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_inicio)])
        self.ui.btn_viajes.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_viaje), self.mostrar_viajes()])
        self.ui.btn_historico.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_historico), self.mostrar_historico_viajes()])
        self.ui.btn_conductor.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pg_conductor))
        self.ui.btn_pagos.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pg_pagos))
        self.ui.btn_factura.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pg_factura))
        self.ui.btn_ajustes.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pg_ajustes))
        
        # Control de barra de titulos
        self.ui.btn_minimizar.clicked.connect(self.minimizar)
        self.ui.btn_restaurar.clicked.connect(self.normal)
        self.ui.btn_maximizar.clicked.connect(self.maximizar)
        self.ui.btn_cerrar.clicked.connect(self.salir)
        self.ui.btn_restaurar.hide()
        
        # Menu lateral
        self.ui.btn_menu.clicked.connect(self.mostrar_menu)

        # Menu ajustes
        self.ui.checkBox.stateChanged.connect(self.fecha_manual)
        
        # Botones
        # -------------------------------------------------------------------------------
        # Viaje
        self.ui.btn_guardar_viaje.clicked.connect(self.guardar_viaje)
        self.ui.btn_buscar_viaje.clicked.connect(self.buscar_viaje)
        
        # self.ui.btn_act.clicked.connect(self.copiar_viaje)
        # self.btn_pasajeros.clicked.connect(self.abrir_subventana)
        # self.btn_eliminar.clicked.connect(self.eliminar_viaje)
        
        # Conductor
        self.ui.btn_guardar_conductor.clicked.connect(self.guardar_conductor)
        self.ui.btn_buscar_conductor.clicked.connect(self.buscar_conductor)
        # Pagos
        self.ui.btn_buscar_conductor_pagos.clicked.connect(self.buscar_conductor_pagos)
        # Historico
        self.ui.btn_buscar_historico.clicked.connect(self.buscar_historico)
        # Factura
        self.ui.btn_generar_factura.clicked.connect(self.generar_factura)
        # Ajustes
        self.ui.btn_actualizar_fecha.clicked.connect(self.actualizar_fecha)
        self.ui.btn_actualizar_costo.clicked.connect(self.actualizar_costo)
        
        # Ajustar Tablas
        self.ui.tabla_viajes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_conductores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_historico.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_pagos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
    # Funciones interfaz
    # -----------------------------------------------------------------------------------
    def salir(self):
        self.db.conexion.close()
        self.close()
    def minimizar(self):
        self.showMinimized()
    def normal(self):
        self.showNormal()
        self.ui.btn_restaurar.hide()
        self.ui.btn_maximizar.show()
    def maximizar(self):
        self.showMaximized()
        self.ui.btn_restaurar.show()
        self.ui.btn_maximizar.hide()
    def mostrar_menu(self):
        if True:
            width = self.ui.frame_menu.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.ui.frame_menu, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
    # SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
    # Mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        
        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()
            
    # Menu ajustes
    # Apartado hora y fecha
    def actualizar_fecha(self):
        if self.ui.checkBox.isChecked():
            self.ui.fecha_sistema_dateTimeEdit.setDateTime(QDateTime.currentDateTime())
            self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
            self.ui.ajustes_fecha_TimeEdit.setDateTime(QDateTime.currentDateTime())
        else:
            self.ui.fecha_sistema_dateTimeEdit.setDateTime(self.ui.ajustes_fecha_TimeEdit.dateTime())
            self.ui.dateTimeEdit.setDateTime(self.ui.ajustes_fecha_TimeEdit.dateTime())
            
        # Menu inicio   
        # Numero de semana
        fecha_actual = self.ui.fecha_sistema_dateTimeEdit.dateTime()
        timestamp = fecha_actual.toSecsSinceEpoch()
        fecha_hora = datetime.datetime.fromtimestamp(timestamp)
        numero_semana, anio = fecha_hora.isocalendar()[1:]
        self.ui.ledt_numero_semana.setText(str(numero_semana))
        self.ui.lineEdit_5.setText(self.ui.ledt_numero_semana.text())
        self.ui.lineEdit_6.setText(str(int(self.ui.ledt_numero_semana.text()) - 1))
        self.ui.dateEdit_2.setDate(self.ui.ajustes_fecha_TimeEdit.date())
    
    def fecha_manual(self):
        if self.ui.checkBox.isChecked():
            self.actualizar_fecha()
            self.ui.ajustes_fecha_label.setStyleSheet('color: rgb(185, 185, 185)')
            self.ui.ajustes_fecha_TimeEdit.setReadOnly(True)
            self.ui.ajustes_fecha_TimeEdit.setStyleSheet('color: rgb(185, 185, 185)')
            self.ui.btn_actualizar_fecha.setStyleSheet('''
    QPushButton {
        border:none;
        background-color:  rgb(214, 214, 214);
        color: rgb(185, 185, 185);
    }
    QPushButton:hover {
	    background-color: rgb(214, 214, 214);
    }
''')
        else:
            self.ui.ajustes_fecha_label.setStyleSheet('color: black')
            self.ui.ajustes_fecha_TimeEdit.setReadOnly(False)
            self.ui.ajustes_fecha_TimeEdit.setStyleSheet('color: rgb(0, 0, 0)')
            self.ui.btn_actualizar_fecha.setStyleSheet('''
    QPushButton {
        border:none;
        color: rgb(255, 255, 255);
        background-color:  rgb(60, 115, 120);
    }
    QPushButton:hover {
        background-color: rgb(0, 85, 120);
    }
''')
    # Apartado costos
    def actualizar_costo(self):
        self.costo_kilometro = float(self.ui.ledt_costo.text())
    # Funciones DB
    # -----------------------------------------------------------------------------------    
    def guardar_viaje(self):
        # Convertir fecha de la interfaz a formato de postgre
        selected_date_time = self.ui.dateTimeEdit.dateTime()
        timestamp = selected_date_time.toSecsSinceEpoch()
        fecha_hora = datetime.datetime.fromtimestamp(timestamp)
        
        self.db.ingresar_viaje()
        
    def mostrar_viajes(self):
        # self.abrir_subventana()
        selected_date = self.ui.dateTimeEdit.date()
        fecha = str(selected_date.toPython().strftime('%Y-%m-%d'))
        cursor = self.conexion.cursor()
        cursor.execute(
            f"select * from Viajes WHERE Fecha BETWEEN date_trunc('week', '{fecha}'::date) AND date_trunc('week', '{fecha}'::date + INTERVAL '1 week' - INTERVAL '1 day');")
        viajes = cursor.fetchall()
        i = len(viajes)
        self.ui.tabla_viajes.setRowCount(i)
        tablerow = 0
        self.ui.btn_act = QPushButton("Actualizar", self)
        self.ui.btn_act.clicked.connect(self.copiar_viaje)
        for row in viajes:
            # self.btn_pasajeros.setProperty("id", row[0])

            self.ui.btn_act.setProperty("id", row[0])
            
            # self.btn_eliminar.setProperty("id", row[0])
            
            self.ui.tabla_viajes.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_viajes.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_viajes.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_viajes.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabla_viajes.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabla_viajes.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.ui.tabla_viajes.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.ui.tabla_viajes.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.ui.tabla_viajes.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            self.ui.tabla_viajes.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[9])))
            
            # self.ui.tabla_viajes.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[10]))) TIPO DESVIO
            
            # Botones
            # self.ui.tabla_viajes.setCellWidget(tablerow, 11, self.btn_pasajeros)
            # self.ui.tabla_viajes.setCellWidget(tablerow, 12, self.btn_act)
            # self.ui.tabla_viajes.setCellWidget(tablerow, 13, self.btn_eliminar)
            
            tablerow += 1
    def copiar_viaje(self):
        # self.btn_act.property("row")
        pass
    """
    str(self.ui.ledt_viajes_empresa.text()), str(self.ui.ledt_viajes_matricula.text()), str(self.ui.ledt_viajes_tipo.text()), 
            str(self.ui.ledt_viajes_contacto.text()), str(self.ui.ledt_viajes_municipio.text()), str(self.ui.ledt_viajes_colonia.text()), 
            str(self.ui.ledt_viajes_calle.text()), str(self.ui.ledt_viajes_cel.text())))
            
    """

    def mostrar_historico_viajes(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM viajes")
        viajes = cursor.fetchall()
        i = len(viajes)
        self.ui.tabla_historico.setRowCount(i)
        tablerow = 0
        
            
        for row in viajes:
            self.ui.tabla_historico.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_historico.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_historico.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_historico.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabla_historico.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabla_historico.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.ui.tabla_historico.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.ui.tabla_historico.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.ui.tabla_historico.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))
            self.ui.tabla_historico.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[9])))
            self.ui.tabla_historico.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[10])))
            
            tablerow += 1
            
    def buscar_viaje(self):
        pass
    def eliminar_viaje(self):
        pass 
        # Preguntar primero
    def guardar_conductor(self):
        pass
    def buscar_conductor(self):
        pass
    def buscar_conductor_pagos(self):
        pass
    def buscar_historico(self):
        pass
    def generar_factura(self):
        pass
    def abrir_subventana(self):
        self.subventana.exec_()