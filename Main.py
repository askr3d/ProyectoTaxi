from PySide2.QtWidgets import QApplication
from mainwindow import MainWindow
import sys

app = QApplication()
window = MainWindow()
window.show()
sys.exit(app.exec_())

"""
create table conductores(id serial, codigo varchar[6], 
						 nombre varchar[50], direcion varchar[100], numero char[12],
						modelo varchar[20], anio char[4], color varchar[10], placa varchar[10])
ALTER TABLE conductores
ADD CONSTRAINT codigo_unico UNIQUE (codigo);
"""
