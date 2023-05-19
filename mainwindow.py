import os
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
        self.actualizar_inicio()
        
        # Crear una instancia de la subventana
        self.subventana = QDialog(self)
        self.subventana_ui = Ui_Form()
        self.subventana_ui.setupUi(self.subventana)
        self.subventana.setWindowFlag(Qt.FramelessWindowHint)
        self.subventana.setWindowOpacity(1)        
        
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
        self.ui.btn_inicio.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_inicio), self.actualizar_inicio()])
        self.ui.btn_viajes.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_viaje), self.mostrar_globales(), self.mostrar_viajes(), self.llenar_datos_viajes()])
        self.ui.btn_historico.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_historico), self.mostrar_historico_viajes()])
        self.ui.btn_conductor.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_conductor),self.mostrar_conductores()])
        self.ui.btn_pagos.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_pagos), self.mostrar_pagos()])
        self.ui.btn_ajustes.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_ajustes), self.mostrar_globales()])
        self.ui.btn_empresa.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.pg_empresa), self.mostrar_empresas()])
        
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

        self.ui.btn_finalizar_viajes.clicked.connect(self.finalizar_viajes)
        # Pasajero
        self.subventana_ui.btn_agregar_pasajero.clicked.connect(self.guardar_pasajeros)
        
        # Empresa
        self.ui.btn_guardar_empresa.clicked.connect(self.guardar_empresa)
        # self.ui.btn_buscar_empresa.clicked.connect(self.buscar_empresa)
        # Conductor
        self.ui.btn_guardar_conductor.clicked.connect(self.guardar_conductor)
        # self.ui.btn_buscar_conductor.clicked.connect(self.buscar_conductor)
        # Pagos
        # Historico
 
        # Ajustes
        self.ui.btn_actualizar_fecha.clicked.connect(self.actualizar_fecha)
        
        self.ui.btn_actualizar_costo.clicked.connect(self.actualizar_costo_conductores) 
        
        self.ui.btn_actualizar_costo_km_diurno.clicked.connect(self.actualizar_costo_km_diurno)
        self.ui.btn_actualizar_costo_km_nocturno.clicked.connect(self.actualizar_costo_km_nocturno)
        self.ui.btn_actualizar_costo_desvio_diurno.clicked.connect(self.actualizar_costo_desvio_diurno)
        self.ui.btn_actualizar_costo_desvio_nocturno.clicked.connect(self.actualizar_costo_desvio_nocturno)
        
        
        # Ajustar Tablas
        self.ui.tabla_viajes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_conductores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_historico.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_pagos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.ui.tabla_empresa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subventana_ui.tabla_pasajeros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
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
                try:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()
                except AttributeError:
                    pass
        
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
    def actualizar_costo_conductores(self):
        costo = int(self.ui.ledt_costo_conductores.text()) / 100
        self.db.actualizar_porcentaje(str(costo))
        
    def actualizar_costo_km_diurno(self):
        self.db.actualizar_kmDiurno(float(self.ui.ledt_costo_km_diurno.text()))
    def actualizar_costo_km_nocturno(self):
        self.db.actualizar_kmNocturno(float(self.ui.ledt_costo_km_nocturno.text()))
    def actualizar_costo_desvio_diurno(self):
        self.db.actualizar_desvioDiurno(float(self.ui.ledt_costo_desvio_diurno.text()))
    def actualizar_costo_desvio_nocturno(self):
        self.db.actualizar_desvioNocturno(float(self.ui.ledt_costo_desvio_nocturno.text()))
        
        
    # Funciones DB
    # -----------------------------------------------------------------------------------    
    def mostrar_globales(self):
        globales = self.db.mostrar_globales()
        self.ui.ledt_costo_km_diurno.setText(str(globales[0]))
        self.ui.ledt_costo_km_nocturno.setText(str(globales[1]))
        self.ui.ledt_costo_desvio_diurno.setText(str(globales[2]))
        self.ui.ledt_costo_desvio_nocturno.setText(str(globales[3]))
        self.ui.ledt_costo_conductores.setText(str(int(float(str(globales[4]) ) * 100)))
    
    
    def finalizar_viajes(self):
        respuesta = QMessageBox.question(None, "Confirmación", "¿Estás seguro de finalizar el registro? \n esta acción no se puede revertir!")
        # Verificar la respuesta del usuario
        if respuesta == QMessageBox.Yes:
            self.db.ingresarPago()
            self.mostrar_viajes()
            
    def guardar_viaje(self):
        # Convertir fecha de la interfaz a formato de postgre
        id = self.ui.ledt_viajes_id.text()
        selected_date_time = self.ui.dateTimeEdit.dateTime()
        timestamp = selected_date_time.toSecsSinceEpoch()
        date_time = datetime.datetime.fromtimestamp(timestamp)
        fecha = date_time.date()
        hora_inicio = self.ui.timeEdit_hora_inicio.time().toString("HH:mm")
        hora_fin = self.ui.timeEdit_hora_fin.time().toString("HH:mm")
        conductor = self.ui.cbx_viajes_conductor.currentText()
        empresa = self.ui.cbx_viajes_empresa.currentIndex() + 1
        tipo_servicio = self.ui.cbx_viajes_tipo_servicio.currentIndex() + 1
        tipo_km = self.ui.cbx_viajes_tipo_km.currentIndex() + 1 
        tipo_desvio = self.ui.cbx_viajes_tipo_desvio.currentIndex() + 1
        kilometros = self.ui.ledt_viajes_kilometros.text()
        costo = 0.0
        try:
            if tipo_km == 1:
                costo = float(kilometros) * float(self.ui.ledt_costo_km_diurno.text())
            else:
                costo = float(kilometros) * float(self.ui.ledt_costo_km_nocturno.text())
        except ValueError:
            pass
        if tipo_desvio == 1:
            costo += (float(self.ui.ledt_costo_desvio_diurno.text()) * int(self.ui.cbx_viajes_numero_desvios.currentText()))
        elif tipo_desvio == 2:
            costo += (float(self.ui.ledt_costo_desvio_nocturno.text()) * int(self.ui.cbx_viajes_numero_desvios.currentText()))
            
        if (self.ui.cbx_viajes_numero_desvios.currentText() == "0" and self.ui.cbx_viajes_tipo_desvio.currentIndex() == 0) or \
        (self.ui.cbx_viajes_numero_desvios.currentText() != "0" and self.ui.cbx_viajes_tipo_desvio.currentIndex() != 0):

            if kilometros != "":
                if id == "":
                    self.db.ingresar_viaje(fecha, conductor, hora_inicio, hora_fin, empresa, tipo_servicio, tipo_km, tipo_desvio, kilometros, costo)
                else:
                    self.db.modificar_viaje(id, fecha, conductor, hora_inicio, hora_fin, empresa, tipo_servicio, tipo_km, tipo_desvio, kilometros, costo)
                    
                self.ui.ledt_viajes_id.clear()
                self.ui.ledt_viajes_kilometros.clear()
                self.llenar_datos_viajes()
                self.mostrar_viajes()
                
            else:
                respuesta = QMessageBox()
                respuesta.setText("Complete todos los campos!")
                respuesta.exec_()
        else:
            respuesta = QMessageBox()
            respuesta.setText("Error en el tipo de desvío!")
            respuesta.exec_()
            
    def llenar_datos_viajes(self):
        conductores = self.db.mostrar_conductores()
        empresas = self.db.mostrar_empresas()
        self.ui.cbx_viajes_conductor.clear()
        self.ui.cbx_viajes_empresa.clear()
        self.ui.dateEdit_viajes.setDate(QDate.currentDate())
        self.ui.timeEdit_hora_inicio.setTime(QTime.currentTime())
        self.ui.timeEdit_hora_fin.setTime(QTime.currentTime())
        for conductor in conductores:
            self.ui.cbx_viajes_conductor.addItem(conductor[0])
        
        for empresa in empresas:
            self.ui.cbx_viajes_empresa.addItem(empresa[1])
    
        
    def mostrar_viajes(self):
        viajes = self.db.mostrar_viajes()
        i = len(viajes)
        
        self.ui.tabla_viajes.setRowCount(i)
        self.ui.tabla_viajes.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        tablerow = 0
        
        for row in viajes:
            btn_actualizar = QPushButton("Actualizar")
            btn_eliminar = QPushButton("Eliminar")
            btn_pasajeros = QPushButton("Pasajeros")
            btn_actualizar.setProperty("id", row[0])
            btn_eliminar.setProperty("id", row[0])
            btn_pasajeros.setProperty("id", row[0])
            
            btn_actualizar.clicked.connect(self.copiar_viaje)
            btn_eliminar.clicked.connect(self.eliminar_viaje)
            btn_pasajeros.clicked.connect(self.abrir_subventana)
            
            self.ui.tabla_viajes.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_viajes.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_viajes.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_viajes.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabla_viajes.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabla_viajes.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.ui.tabla_viajes.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.ui.tabla_viajes.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[8])))
            self.ui.tabla_viajes.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[10])))
            self.ui.tabla_viajes.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[12])))
            self.ui.tabla_viajes.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[14])))

            self.ui.tabla_viajes.setCellWidget(tablerow, 11, btn_pasajeros)
            self.ui.tabla_viajes.setCellWidget(tablerow, 12, btn_actualizar)
            self.ui.tabla_viajes.setCellWidget(tablerow, 13, btn_eliminar)
            
            tablerow += 1
            
    def mostrar_pasajeros(self):
        id_boton = self.subventana_ui.ledt_pasajeros_id_viaje.text()
        pasajeros = self.db.mostrar_pasejeros_por_viaje(id_boton)
        i = len(pasajeros)
        self.subventana_ui.tabla_pasajeros.setRowCount(i)
        tablerow = 0
        
        for row in pasajeros:
            btn_actualizar = QPushButton("Actualizar")
            btn_eliminar = QPushButton("Eliminar")
            btn_actualizar.setProperty("id", row[0])
            btn_eliminar.setProperty("id", row[0])
            btn_actualizar.clicked.connect(self.copiar_pasajero)
            btn_eliminar.clicked.connect(self.eliminar_pasajero)
            self.subventana_ui.tabla_pasajeros.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[2])))
            self.subventana_ui.tabla_pasajeros.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[3])))
            self.subventana_ui.tabla_pasajeros.setCellWidget(tablerow, 2, btn_actualizar)
            self.subventana_ui.tabla_pasajeros.setCellWidget(tablerow, 3, btn_eliminar)
            tablerow += 1
            
    def abrir_subventana(self):
        self.subventana_ui.ledt_pasajeros_id_viaje.setText(str(self.sender().property("id")))
        self.mostrar_pasajeros()
        self.subventana.exec_()

    def mostrar_pagos(self):
        pagos = self.db.mostrar_pagos()
        i = len(pagos)
        self.ui.tabla_pagos.setRowCount(i)
        tablerow = 0
        
        for row in pagos:

            self.ui.tabla_pagos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_pagos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_pagos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_pagos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabla_pagos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabla_pagos.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.ui.tabla_pagos.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            
            tablerow += 1
    def generar_factura(self):
        self.ui.lineEdit_7.setText(self.ui.lineEdit_2.text())
        
        
    def actualizar_inicio(self):
        semana_actual = int(self.ui.lineEdit_5.text())
        semana_previa = int(self.ui.lineEdit_6.text())
        costo_conductores = self.db.costo_pagos_por_semana(str(semana_actual))
        costo_viajes = self.db.costo_viajes_por_semana(str(semana_previa))
        
        if costo_conductores is not None and costo_viajes is not None:
            self.ui.lineEdit_3.setText(str(costo_conductores[0]))
            self.ui.lineEdit_2.setText(str(costo_viajes[0]))
            total = float(str(costo_viajes[0])) - float(str(costo_conductores[0])) 
            self.ui.lineEdit_4.setText(str(total))
            
    def guardar_pasajeros(self):
        id_viaje =  self.subventana_ui.ledt_pasajeros_id_viaje.text()
        id = self.subventana_ui.ledt_pasajeros_id.text()
        nombre = self.subventana_ui.ledt_pasajeros_nombre.text()
        destino = self.subventana_ui.ledt_pasajeros_destino.text()
        if nombre != "" and destino != "":
            if id == "":
                self.db.ingresar_pasajero(id_viaje, nombre, destino)
            else:
                self.db.modificar_pasajero(id, nombre, destino)
            self.mostrar_pasajeros()
            self.subventana_ui.ledt_pasajeros_id.clear()
            self.subventana_ui.ledt_pasajeros_nombre.clear()
            self.subventana_ui.ledt_pasajeros_destino.clear()
        else:
            respuesta = QMessageBox()
            respuesta.setText("Complete todos los campos!")
            respuesta.exec_()
             
    def copiar_pasajero(self):
        id_boton = self.sender().property("id")
        pasajero = self.db.buscar_pasajero_por_id(id_boton)
        self.subventana_ui.ledt_pasajeros_id.setText(str(pasajero[0]))
        self.subventana_ui.ledt_pasajeros_nombre.setText(str(pasajero[2]))
        self.subventana_ui.ledt_pasajeros_destino.setText(str(pasajero[3]))
        
    def eliminar_pasajero(self):
        respuesta = QMessageBox.question(None, "Confirmación", "¿Estás seguro de eliminar el registro?")
        if respuesta == QMessageBox.Yes:
            id_boton = self.sender().property("id")
            self.db.eliminar_pasajero(id_boton)
            self.mostrar_pasajeros() 
         
            
    def eliminar_viaje(self):
        respuesta = QMessageBox.question(None, "Confirmación", "¿Estás seguro de eliminar el registro?")
        if respuesta == QMessageBox.Yes:
            id_boton = self.sender().property("id")
            self.db.eliminar_viaje(id_boton)
            self.mostrar_viajes()  
    
    def copiar_viaje(self):
        id_boton = self.sender().property("id")
        viaje = self.db.buscar_viaje_por_folio(id_boton)
        self.ui.ledt_viajes_id.setText(str(viaje[0]))
        self.ui.cbx_viajes_conductor.setCurrentText(str(viaje[6]))
        self.ui.timeEdit_hora_inicio.setTime(QTime.fromString(str(viaje[2])))
        self.ui.timeEdit_hora_fin.setTime(QTime.fromString(str(viaje[3])))
        self.ui.cbx_viajes_empresa.setCurrentIndex(int(viaje[9]))
        self.ui.cbx_viajes_tipo_servicio.setCurrentIndex(int(viaje[7]))
        self.ui.cbx_viajes_tipo_km.setCurrentIndex(int(viaje[11]))
        if viaje[13] is None:
            self.ui.cbx_viajes_tipo_desvio.setCurrentIndex(0)
        else:
            self.ui.cbx_viajes_tipo_desvio.setCurrentIndex(int(viaje[13]))
            
        self.ui.ledt_viajes_kilometros.setText(str(viaje[4]))
        self.ui.ledt_viajes_costo.setText(str(viaje[5]))
        self.ui.dateEdit_viajes.setDate(QDate.fromString(str(viaje[1])))
        
    def guardar_conductor(self):
        id = self.ui.ledt_conductor_id.text()
        nombre = self.ui.ledt_conductor_nombre.text()
        unidad = self.ui.ledt_conductor_unidad.text()
        numero = self.ui.ledt_conductor_numero.text()
        placa = self.ui.ledt_conductor_matricula.text()
        
        if nombre != "" and numero != "" and placa != "" and unidad != "":
            if id == "":
                self.db.ingresar_conductor(nombre, unidad, numero, placa)
            else:
                self.db.modificar_conductor(id, nombre, unidad, numero, placa)
            self.mostrar_conductores()
            self.ui.ledt_conductor_id.clear()
            self.ui.ledt_conductor_nombre.clear()
            self.ui.ledt_conductor_unidad.clear()
            self.ui.ledt_conductor_numero.clear()
            self.ui.ledt_conductor_matricula.clear()
        else:
            respuesta = QMessageBox()
            respuesta.setText("Complete todos los campos!")
            respuesta.exec_()
        
        
    def mostrar_conductores(self):
        conductores = self.db.mostrar_conductores()
        i = len(conductores)
        
        self.ui.tabla_conductores.setRowCount(i)
        tablerow = 0
        
        for row in conductores:
            btn_actualizar = QPushButton("Actualizar")
            btn_eliminar = QPushButton("Eliminar")
            btn_actualizar.setProperty("id", row[0])
            btn_eliminar.setProperty("id", row[0])
            
            btn_actualizar.clicked.connect(self.copiar_conductor)
            btn_eliminar.clicked.connect(self.eliminar_conductor)
            
            self.ui.tabla_conductores.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_conductores.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_conductores.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_conductores.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[4])))
            
            self.ui.tabla_conductores.setCellWidget(tablerow, 4, btn_actualizar)
            self.ui.tabla_conductores.setCellWidget(tablerow, 5, btn_eliminar)
            
            tablerow += 1
    def copiar_conductor(self):
        id_boton = self.sender().property("id")
        conductor = self.db.buscar_conductor_por_id(id_boton)
        num_unidad = str(conductor[0]).split("-")[-1]
        self.ui.ledt_conductor_id.setText(str(conductor[0]))
        self.ui.ledt_conductor_nombre.setText(str(conductor[1]))
        self.ui.ledt_conductor_unidad.setText(num_unidad)
        self.ui.ledt_conductor_numero.setText(str(conductor[2]))
        self.ui.ledt_conductor_matricula.setText(str(conductor[4]))

    def eliminar_conductor(self):
        respuesta = QMessageBox.question(None, "Confirmación", "¿Estás seguro de eliminar el registro?")
        if respuesta == QMessageBox.Yes:
            id_boton = self.sender().property("id")
            self.db.eliminar_conductor(id_boton)
            self.mostrar_conductores()  
    
    def guardar_empresa(self):
        id = self.ui.ledt_empresa_id.text()
        nombre = self.ui.ledt_empresa_nombre.text()
        domicilio = self.ui.ledt_empresa_domicilio.text()
        telefono = self.ui.ledt_empresa_telefono.text()
        if nombre != "" and domicilio != "" and telefono != "":
            if id == "":
                self.db.ingresar_empresa(nombre, domicilio, telefono)
            else:
                self.db.modificar_empresa(id, nombre, domicilio, telefono)
            self.mostrar_empresas()
            self.ui.ledt_empresa_nombre.clear()
            self.ui.ledt_empresa_domicilio.clear()
            self.ui.ledt_empresa_telefono.clear()
            self.ui.ledt_empresa_id.clear()
        else:
            respuesta = QMessageBox()
            respuesta.setText("Complete todos los campos!")
            respuesta.exec_()
        
    def copiar_empresa(self):
        id_boton = self.sender().property("id")
        empresa = self.db.mostrar_empresa_por_id(id_boton)
        
        self.ui.ledt_empresa_id.setText(str(empresa[0]))
        self.ui.ledt_empresa_nombre.setText(str(empresa[1]))
        self.ui.ledt_empresa_domicilio.setText(str(empresa[2]))
        self.ui.ledt_empresa_telefono.setText(str(empresa[3]))
        
    def eliminar_empresa(self):
        respuesta = QMessageBox.question(None, "Confirmación", "¿Estás seguro de eliminar el registro?")
        if respuesta == QMessageBox.Yes:
            id_boton = self.sender().property("id")
            self.db.eliminar_empresa(id_boton)
            self.mostrar_empresas()   
        
    def mostrar_empresas(self):
        empresas = self.db.mostrar_empresas()
        i = len(empresas)
        
        self.ui.tabla_empresa.setRowCount(i)
        tablerow = 0
        
        for row in empresas:
            btn_actualizar = QPushButton("Actualizar")
            btn_eliminar = QPushButton("Eliminar")
            btn_actualizar.setProperty("id", row[0])
            btn_eliminar.setProperty("id", row[0])
            
            btn_actualizar.clicked.connect(self.copiar_empresa)
            btn_eliminar.clicked.connect(self.eliminar_empresa)
            
            self.ui.tabla_empresa.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabla_empresa.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabla_empresa.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabla_empresa.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            
            self.ui.tabla_empresa.setCellWidget(tablerow, 4, btn_actualizar)
            self.ui.tabla_empresa.setCellWidget(tablerow, 5, btn_eliminar)
            
            tablerow += 1

    def mostrar_historico_viajes(self):
        viajes = self.db.mostrar_historico()
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
            self.ui.tabla_historico.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[8])))
            self.ui.tabla_historico.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[10])))
            self.ui.tabla_historico.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(row[12])))
            self.ui.tabla_historico.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(row[14])))
            
            tablerow += 1
    