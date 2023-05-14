import psycopg2

class OperacionesDB():
    def __init__(self):
        self.conexion = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '0123',
            database = 'proyectoTaxi'
        )

    def ingresar_conductor(self, nombre, unidad, numero, placa):
        cursor = self.conexion.cursor()
        cursor.execute("CALL ingresarConductor(%s, %s, %s, %s)", (nombre, unidad, numero, placa))
        self.conexion.commit()
        cursor.close()

    def buscar_conductor_por_id(self, unidad):
        cursor = self.conexion.cursor()
        query = '''SELECT conductores.*, Autos.Placas
                    FROM conductores
                    INNER JOIN autos
                    ON autos.conductorId = conductores.Id
                    WHERE activo = 1 and id = '{}'
                    '''.format(unidad)
        cursor.execute(query)
        conductor = cursor.fetchone()
        cursor.close()
        return conductor

    def modificar_conductor(self, nombre, unidad, numero, placa):
        cursor = self.conexion.cursor()
        query = '''
                UPDATE conductores
                SET nombre = '{}', unidad = '{}', numero = '{}'
                WHERE unidad = '{}';

                UPDATE autos
                SET placa = '{}'
                WHERE conductorId = '{}'
                '''.format(nombre, unidad, numero, unidad, placa, unidad)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()
        

    def mostrar_conductores(self):
        cursor = self.conexion.cursor()
        query = '''SELECT conductores.*, Autos.Placas
                    FROM conductores
                    INNER JOIN autos
                    ON autos.conductorId = conductores.Id
                    WHERE activo = 1
                    '''
        cursor.execute(query)
        conductores = cursor.fetchall()
        cursor.close()
        return conductores
    
    def ingresar_pasajero(self, viajeId, nombre, destino):
        cursor = self.conexion.cursor()
        query = '''
                INSERT INTO Pasajeros(viajeId, nombre, destino) VALUES('{}', '{}', '{}')
                '''.format(viajeId, nombre, destino)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def mostrar_pasejeros_por_viaje(self, viajeId):
        cursor = self.conexion.cursor()
        query = '''
                SELECT * Pasejeros WHERE viajeId = '{}'
                '''.format(viajeId)
        cursor.execute(query)
        pasajeros = cursor.fetchall()
        cursor.close()
        return pasajeros
    
    def modificar_pasajero(self, id, nombre, destino):
        cursor = self.conexion.cursor()
        query = '''
                UPDATE Pasajeros
                SET nombre = '{}', destino = '{}'
                WHERE id = '{}'
                '''.format(nombre, destino, id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def eliminar_pasajero(self, id):
        cursor = self.conexion.cursor()
        query = '''DELETE Pasajeros WHERE Id = '{}' '''.format(id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def ingresar_viaje(self, folio, fecha, unidadId, horaInicio, horaFin, empresaId, tipoServicioId, tipoKmId, desvioId, kilometros, costo, kilometrosDesvio):
        cursor = self.conexion.cursor()
        query = '''INSERT INTO Viajes(folio, fecha, horaInicio, horaFin, kilometros, costo, conductorId, partidaId, empresaId, tipoKilometroId)
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(folio, fecha, horaInicio, horaFin, kilometros, costo, unidadId, tipoServicioId, empresaId, tipoKmId)
        cursor.execute(query)
        if(desvioId != 1 and desvioId < 4):
            desvioId = desvioId - 1
            query = '''
                    INSERT INTO Desvios(ViajeId, TipoDesvioId, Kilometros)
                    VALUES('{}', '{}', '{}')
                    '''.format(folio, desvioId, kilometrosDesvio)
            cursor.execute(query)
        
        self.conexion.commit()
        cursor.close()

    def modificar_viaje(self, folio, fecha, unidadId, horaInicio, horaFin, empresaId, tipoServicioId, tipoKmId, desvioId, kilometros, costo, kilometrosDesvio):
        cursor = self.conexion.cursor()
        query = '''
                UPDATE Viajes
                SET folio = '{}', fecha= '{}', horaInicio = '{}', horaFin = '{}', kilometros = '{}', costo = '{}', conductorId = '{}', partidaId = '{}', empresaId = '{}', tipoKilometroId = '{}'
                WHERE folio = '{}'
                '''.format(folio, fecha, horaInicio, horaFin, kilometros, costo, unidadId, tipoServicioId, empresaId, tipoKmId, folio)
        cursor.execute(query)

        query = '''SELECT * FROM desvios WHERE viajeId = '{}' '''.format(folio)
        cursor.execute(query)
        existe = cursor.fetchone()

        if existe is not None:
            if(desvioId != 1 and desvioId < 4):
                desvioId = desvioId - 1
                query = '''
                        UPDATE desvios
                        SET viajeId = '{}', tipoDesvioId = '{}', kilometros = '{}'
                        WHERE viajeId = '{}'
                        '''.format(folio, desvioId, kilometrosDesvio, folio)
            else:
                query = '''DELETE FROM desvios WHERE viajeId = '{}' '''.format(folio)
            cursor.execute(query)
        else:
            if(desvioId != 1 and desvioId < 4):
                desvioId = desvioId - 1
                query = '''
                        INSERT INTO Desvios(ViajeId, TipoDesvioId, kilometros)
                        VALUES('{}', '{}', '{}')
                        '''.format(folio, desvioId, kilometrosDesvio)
                cursor.execute(query)

        self.conexion.commit()
        cursor.close()

    def eliminar_viaje(self, folio):
        cursor = self.conexion.cursor()
        cursor.execute("CALL eliminarViajes(%s)", (folio))
        self.conexion.commit()
        cursor.close()

    def mostrar_viajes(self):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM detalles_viajes WHERE status = 0"
        cursor.execute(query)
        viajes = cursor.fetchall()
        cursor.close()
        return viajes
    
    def buscar_viaje_por_folio(self, folio):
        cursor = self.conexion.cursor()
        query = '''SELECT * FROM detalles_viajes WHERE folio = '{}' '''.format(folio)
        cursor.execute(query)
        viaje = cursor.fetchone()
        cursor.close()
        return viaje

    def mostrar_pagos(self):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM detalle_pagos"
        cursor.execute(query)
        pagos = cursor.fetchall()
        cursor.close()
        return pagos
    
    def mostrar_historico(self):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM detalles_viajes WHERE status = 1"
        cursor.execute(query)
        pagos = cursor.fetchall()
        cursor.close()
        return pagos
    
    def obtener_costosViajes_por_conductor(self, conductorId):
        cursor = self.conexion.cursor()
        query = '''SELECT SUM(costo) FROM viajes WHERE conductorId = '{}', status = 0 '''.format(conductorId)
        cursor.execute(query)
        viajes = cursor.fetchone()
        cursor.close()
        return viajes
    
    def ingresarPago(self, kmDiurno, kmNocturno, desvioDiurno, desvioNocturno):
        cursor = self.conexion.cursor()
        queryInsertar = '''
                        INSERT INTO Pagos(conductorId, fechaPago, costoTotal)
                            VALUES('{}', CURRENT_DATE, '{}')
                        '''
        conductores = self.mostrar_conductores
        for conductor in conductores:
            costo = self.obtener_costosViajes_por_conductor(conductor[0]) * 0.8
            if(costo > 0):
                cursor.execute(queryInsertar.format(conductor[0], costo))
        
        self.conexion.commit()
        cursor.close()
        