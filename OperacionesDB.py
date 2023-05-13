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

    def ingresar_viaje(self, folio, fecha, unidadId, horaInicio, horaFin, empresaId, tipoServicioId, tipoKmId, desvioId, kilometros, costo):
        cursor = self.conexion.cursor()
        query = '''INSERT INTO Viajes(folio, fecha, horaInicio, horaFin, kilometros, costo, conductorId, partidaId, empresaId, tipoKilometroId)
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                '''.format(folio, fecha, horaInicio, horaFin, kilometros, costo, unidadId, tipoServicioId, empresaId, tipoKmId)
        cursor.execute(query)
        if(desvioId != 1 and desvioId < 4):
            desvioId = desvioId - 1
            query = '''
                    INSERT INTO Desvios(ViajeId, TipoDesvioId)
                    VALUES('{}', '{}')
                    '''.format(folio, desvioId)
            cursor.execute(query)
        
        self.conexion.commit()
        cursor.close()

    def modificar_viaje(self, folio, fecha, unidadId, horaInicio, horaFin, empresaId, tipoServicioId, tipoKmId, desvioId, kilometros, costo):
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
                        SET viajeId = '{}', tipoDesvioId = '{}'
                        WHERE viajeId = '{}'
                        '''.format(folio, desvioId, folio)
            else:
                query = '''DELETE FROM desvios WHERE viajeId = '{}' '''.format(folio)
            cursor.execute(query)
        else:
            if(desvioId != 1 and desvioId < 4):
                desvioId = desvioId - 1
                query = '''
                        INSERT INTO Desvios(ViajeId, TipoDesvioId)
                        VALUES('{}', '{}')
                        '''.format(folio, desvioId)
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
        query = "SELECT * FROM detalles_viajes"
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
        query = "SELECT * FROM viajes"
        cursor.execute(query)
        pagos = cursor.fetchall()
        cursor.close()
        return pagos