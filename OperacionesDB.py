import psycopg2

class OperacionesDB():
    def __init__(self):
        try:
            self.conexion = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = '0123',
                database = 'ProyectoTaxis'
            )
        except:
            print("Error de conexion: ")
            exit()

    #Empresas
    def ingresar_empresa(self, nombre, domicilio, telefono):
        cursor = self.conexion.cursor()
        query = '''
                INSERT INTO Empresas(nombre, domicilio, telefono) VALUES ('{}', '{}', '{}')
                '''.format(nombre, domicilio, telefono)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def mostrar_empresas(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Empresas WHERE Status = 1 ORDER BY Id")
        empresas = cursor.fetchall()
        cursor.close()
        return empresas

    def mostrar_empresa_por_id(self, id):
        cursor = self.conexion.cursor()
        cursor.execute('''SELECT * FROM Empresas WHERE id = '{}' '''.format(id))
        empresa = cursor.fetchone()
        cursor.close()
        return empresa
    
    def modificar_empresa(self, id, nombre, domicilio, telefono):
        cursor = self.conexion.cursor()
        query = '''
                UPDATE Empresas
                SET Nombre = '{}', Domicilio = '{}', Telefono = '{}'
                WHERE Id = '{}'
                '''.format(nombre, domicilio, telefono, id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def eliminar_empresa(self, id):
        cursor = self.conexion.cursor()
        query = '''UPDATE Empresas SET Status = 0 WHERE Id = '{}' '''.format(id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    #Conductores
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

    def modificar_conductor(self, id, nombre, unidad, numero, placa):
        cursor = self.conexion.cursor()
        cursor.execute("CALL modificarConductor(%s, %s, %s, %s, %s)", (id, nombre, unidad, numero, placa))
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
    
    def eliminar_conductor(self, id):
        cursor = self.conexion.cursor()
        query = '''UPDATE Conductores SET Activo = 0 WHERE id = '{}' '''.format(id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()
    
    #Pasajeros
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
                SELECT * FROM Pasajeros WHERE viajeId = '{}'
                '''.format(viajeId)
        cursor.execute(query)
        pasajeros = cursor.fetchall()
        cursor.close()
        return pasajeros
    
    def buscar_pasajero_por_id(self, id):
        cursor = self.conexion.cursor()
        query = '''SELECT * FROM Pasajeros WHERE id = '{}' '''.format(id)
        cursor.execute(query)
        pasajero = cursor.fetchone()
        cursor.close()
        return pasajero
    
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
        query = '''DELETE FROM Pasajeros WHERE Id = '{}' '''.format(id)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    #Viajes
    
    def ingresar_viaje(self, fecha, unidadId, horaInicio, horaFin, empresaId, tipoServicioId, tipoKmId, desvioId, kilometros, costo):
        cursor = self.conexion.cursor()
        query = '''INSERT INTO Viajes(fecha, horaInicio, horaFin, kilometros, costo, conductorId, partidaId, empresaId, tipoKilometroId)
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') RETURNING folio
                '''.format(fecha, horaInicio, horaFin, kilometros, costo, unidadId, tipoServicioId, empresaId, tipoKmId)
        cursor.execute(query)
        if(desvioId != 1 and desvioId < 4):
            folio = cursor.fetchone()[0]
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
        query = '''
                DELETE FROM Pasajeros WHERE viajeId = '{}';
                DELETE FROM Desvios WHERE viajeId = '{}';
                DELETE FROM Viajes WHERE folio = '{}';
                '''.format(folio, folio, folio)
        
        cursor.execute(query)
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
    
    def mostrar_historico(self):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM detalles_viajes WHERE status = 1"
        cursor.execute(query)
        pagos = cursor.fetchall()
        cursor.close()
        return pagos
    
    #Pagos
    def mostrar_pagos(self):
        cursor = self.conexion.cursor()
        query = "SELECT * FROM detalle_pagos"
        cursor.execute(query)
        pagos = cursor.fetchall()
        cursor.close()
        return pagos
    
    def obtener_costosViajes_por_conductor(self, conductorId):
        cursor = self.conexion.cursor()
        query = '''SELECT SUM(costo) FROM viajes WHERE conductorId = '{}' and status = 0 '''.format(conductorId)
        cursor.execute(query)
        viajes = cursor.fetchone()
        cursor.close()
        return viajes
    
    
    def ingresarPago(self):
        porcentaje = float(str(self.mostrar_globales()[4]))
        cursor = self.conexion.cursor()
        queryStatus = "UPDATE viajes SET Status = 1 WHERE Status = 0"
        queryInsertar = '''
                        INSERT INTO Pagos(conductorId, fechaPago, costoTotal)
                            VALUES('{}', CURRENT_DATE, '{}')
                        '''
        conductores = self.mostrar_conductores()
        for conductor in conductores:
            
            costo = self.obtener_costosViajes_por_conductor(conductor[0])[0]
            
            if(costo is not None and float(str(costo)) > 0):
                costo = float(str(costo)) * porcentaje
                cursor.execute(queryInsertar.format(conductor[0], costo))
        
        cursor.execute(queryStatus)
        self.conexion.commit()
        cursor.close()

    def costo_viajes_por_semana(self, numeroSemana):
        cursor = self.conexion.cursor()
        query = '''
                SELECT SUM(costo), fecha FROM viajes
                WHERE EXTRACT(WEEK from fecha) = '{}' and status = 1
                GROUP BY fecha
                '''.format(numeroSemana)
        cursor.execute(query)
        costoViajes = cursor.fetchone()
        cursor.close()
        return costoViajes
    
    def costo_pagos_por_semana(self, numeroSemana):
        cursor = self.conexion.cursor()
        query = '''
                SELECT SUM(costoTotal), fechaPago FROM pagos
                WHERE EXTRACT(WEEK from fechaPago) = '{}'
                GROUP BY fechaPago
                '''.format(numeroSemana)
        cursor.execute(query)
        costoPagos = cursor.fetchone()
        cursor.close()
        return costoPagos

    #globales

    def mostrar_globales(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM valoresGlobales")
        datos = cursor.fetchone()
        cursor.close()
        return datos
    
    def actualizar_kmDiurno(self, valor: float):
        cursor = self.conexion.cursor()
        query = '''UPDATE valoresGlobales SET kmDiurno =  '{}' '''.format(valor)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()
    
    def actualizar_kmNocturno(self, valor: float):
        cursor = self.conexion.cursor()
        query = '''UPDATE valoresGlobales SET kmNocturno =  '{}' '''.format(valor)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def actualizar_desvioDiurno(self, valor: float):
        cursor = self.conexion.cursor()
        query = '''UPDATE valoresGlobales SET desvioDiurno =  '{}' '''.format(valor)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()
    
    def actualizar_desvioNocturno(self, valor: float):
        cursor = self.conexion.cursor()
        query = '''UPDATE valoresGlobales SET desvioNocturno =  '{}' '''.format(valor)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()

    def actualizar_porcentaje(self, valor: float):
        cursor = self.conexion.cursor()
        query = '''UPDATE valoresGlobales SET porcentaje =  '{}' '''.format(valor)
        cursor.execute(query)
        self.conexion.commit()
        cursor.close()