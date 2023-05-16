-- Database: ProyectoTaxis

-- DROP DATABASE IF EXISTS "ProyectoTaxis";

CREATE DATABASE "ProyectoTaxis"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	


drop view detalles_viajes, detalle_pagos;
drop table autos, conductores, desvios, empresas, pagos, partidas, pasajeros, tipodesvio, tipokilometro, viajes;

CREATE TABLE Conductores(
	Id varchar(15) not null,
	Nombre varchar(35) not null,
	Numero varchar(15) not null,
	Activo int default 1 not null,
	primary key(Id)
);

CREATE TABLE Pagos(
	ConductorId varchar(15) references Conductores(Id) ON UPDATE cascade ON DELETE no action,
	FechaPago date,
	CostoTotal numeric(8, 2),
	primary key(ConductorId, FechaPago)
);

CREATE TABLE Autos(
	ConductorId varchar(15) references Conductores(Id) ON UPDATE cascade ON DELETE no action,
	Placas varchar(15),
	primary key(ConductorId, Placas)
);



CREATE TABLE Partidas(
	Id serial,
	Nombre varchar(25) not null,
	primary key(Id)
);

INSERT INTO Partidas(Nombre)
VALUES ('Entrada'), ('Salida')

CREATE TABLE Empresas(
	Id serial,
	Nombre varchar(35) not null,
	Domicilio varchar(35) not null,
	Telefono varchar(15),
	Status int default 1,
	primary key(Id)
);

/*
INSERT INTO Empresas(Nombre, Domicilio, Telefono)
VALUES('Mercado Libre', 'El Salto', '332921292'),
('Flex Norte', 'EL Salto', '33391912'),
('Flex Sur', 'El Salto', '331313112')
*/


CREATE TABLE TipoKilometro(
	Id serial,
	Nombre varchar(35),
	primary key(Id)
);

INSERT INTO TipoKilometro(Nombre) VALUES
('Diurno'), ('Nocturno')

CREATE TABLE Viajes(
	Folio serial,
	Fecha date,
	HoraInicio time,
	HoraFin time,
	Kilometros float,
	Costo numeric(8, 2),
	Status int default 0,
	ConductorId varchar(15) references Conductores(Id) ON UPDATE cascade ON DELETE no action,
	PartidaId int references Partidas(Id) ON UPDATE cascade,
	EmpresaId int references Empresas(Id) ON UPDATE cascade ON DELETE no action,
	TipoKilometroId int references TipoKilometro(Id) ON UPDATE cascade,
	primary key(Folio)
);


CREATE TABLE TipoDesvio(
	Id serial,
	Nombre varchar(35),
	primary key(Id)
);

INSERT INTO TipoDesvio(Nombre) VALUES
('Diurno'), ('Nocturno')

CREATE TABLE Desvios(
	Id serial,
	ViajeId int references Viajes(Folio) ON UPDATE cascade ON DELETE cascade,
	TipoDesvioId int references TipoDesvio(Id),
	primary key(Id, ViajeId)
);

CREATE TABLE Pasajeros(
	Id serial,
	ViajeId int references Viajes(Folio) ON UPDATE cascade ON DELETE cascade,
	Nombre varchar(50),
	Destino varchar(50),
	primary key(Id, ViajeId)
);

--SELECT * FROM detalles_viajes WHERE status = 0;

CREATE OR REPLACE VIEW detalles_viajes AS
SELECT folio, fecha, horaInicio, horaFin, viajes.kilometros, viajes.costo
		, conductorId, partidas.Id - 1 as tipoServicioId, partidas.Nombre as tipoServicio,
		empresas.Id - 1 as empresaId, empresas.Nombre as empresa,
		tipoKilometro.Id - 1 as tipoKilometroId, tipoKilometro.Nombre as tipoKilometro,
		tipoDesvio.Id - 1 as tipoDesvioId, tipoDesvio.Nombre as tipoDesvio,
		viajes.status
FROM viajes
INNER JOIN partidas
ON viajes.partidaId = partidas.Id
INNER JOIN empresas
ON empresas.Id = viajes.empresaId
INNER JOIN tipoKilometro
ON tipoKilometro.Id = viajes.tipoKilometroId
LEFT JOIN desvios
ON viajes.folio = desvios.viajeId
LEFT JOIN tipoDesvio
ON desvios.tipoDesvioId = tipoDesvio.Id;

CREATE OR REPLACE PROCEDURE ingresarConductor(nombreConductor varchar(35), unidadNumero int, numeroConductor varchar(15), placa varchar(15))
LANGUAGE plpgsql
AS $$
DECLARE
	Unidad varchar(15) := 'TB';
BEGIN
	Unidad := CONCAT(Unidad, unidadNumero);
	INSERT INTO Conductores(id, nombre, numero, activo) VALUES(Unidad, nombreConductor, numeroConductor, default);
	INSERT INTO Autos VALUES(Unidad, placa);
	
END;
$$

CREATE OR REPLACE PROCEDURE modificarConductor(idConductor varchar(15), nombreConductor varchar(35), unidadNumero int, numeroConductor varchar(15), placaConductor varchar(15))
LANGUAGE plpgsql
AS $$
DECLARE
	Unidad varchar(15) := 'TB-';
BEGIN
	Unidad := CONCAT(Unidad, unidadNumero);
	UPDATE Autos
	SET Placas = placaConductor
	WHERE conductorId = idConductor;
	
	UPDATE Conductores
	SET Nombre = nombreConductor, numero = numeroConductor, id = Unidad
	WHERE id = idConductor;
	
END;
$$

CREATE OR REPLACE PROCEDURE eliminarViajes(folioId int)
LANGUAGE plpgsql
AS $$
BEGIN
	DELETE FROM Viajes
	WHERE folio = folioId;

	DELETE FROM Desvios
	WHERE ViajeId = folioId;

	DELETE FROM Pasajeros
	WHERE ViajeId = folioId;
END;
$$

-- DROP PROCEDURE mostrarPagos

CREATE OR REPLACE PROCEDURE mostrarPagos()
LANGUAGE plpgsql
AS $$
DECLARE
	resultado
BEGIN
	SELECT pagos.Unidad, pagos.FechaPago, funcionKmDiurno(conductores.Id, pagos.FechaPago),
	funcionKmNocturno(conductores.Id, pagos.fechaPago),
	pagos.Costo
	INTO resultado
	FROM viajes
	INNER JOIN conductores
	ON conductores.Id = viajes.conductorId
	INNER JOIN pagos
	ON conductores.Id = pagos.conductorId
	GROUP BY pagos.fechaPago;
	
END;
$$

CREATE OR REPLACE VIEW detalle_Pagos AS
SELECT pagos.ConductorId, pagos.FechaPago, funcionKmDiurno(pagos.ConductorId, pagos.FechaPago) AS kmDiurno,
    funcionKmNocturno(pagos.ConductorId, pagos.FechaPago) AS kmNocturno,
    funcionDesvioDiurno(pagos.ConductorId, pagos.FechaPago) AS desvioDiurno,
    funcionDesvioNocturno(pagos.ConductorId, pagos.FechaPago) AS desvioNocturno,
    pagos.costoTotal
FROM viajes
INNER JOIN pagos ON viajes.conductorId = pagos.ConductorId
GROUP BY pagos.FechaPago, pagos.ConductorId;

CREATE OR REPLACE FUNCTION funcionKmDiurno(unidad varchar(15), fechaPago date)
RETURNS float AS
$$
DECLARE
    kmDiurno float := 0;
	fechaRangoInferior int := EXTRACT(WEEK from fechaPago) - 1;
BEGIN
	
	
	SELECT SUM(kilometros) INTO kmDiurno
	FROM viajes
	WHERE status = 1 and EXTRACT(WEEK from viajes.Fecha) = fechaRangoInferior
			and ConductorId = unidad and TipoKilometroId = 1;
	
    RETURN kmDiurno;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION funcionKmNocturno(unidad varchar(15), fechaPago date)
RETURNS float AS
$$
DECLARE
    kmNocturno float := 0;
	fechaRangoInferior int := EXTRACT(WEEK from fechaPago) - 1;
BEGIN
	
	
	SELECT SUM(kilometros) INTO kmNocturno
	FROM viajes
	WHERE status = 1 and EXTRACT(WEEK from viajes.Fecha) = fechaRangoInferior
			and ConductorId = unidad and TipoKilometroId = 2;
	
    RETURN kmNocturno;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION funcionDesvioDiurno(unidad varchar(15), fechaPago date)
RETURNS float AS
$$
DECLARE
    desvioDiurno float := 0;
	fechaRangoInferior int := EXTRACT(WEEK from fechaPago) - 1;
BEGIN
	
	
	SELECT COUNT(*) INTO desvioDiurno
	FROM viajes
	INNER JOIN desvios
	ON viajes.folio = desvios.viajeId
	WHERE status = 1 and EXTRACT(WEEK from viajes.Fecha) = fechaRangoInferior
			and ConductorId = unidad and desvios.tipoDesvioId = 1;
	
    RETURN desvioDiurno;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION funcionDesvioNocturno(unidad varchar(15), fechaPago date)
RETURNS float AS
$$
DECLARE
    desvioNocturno float := 0;
	fechaRangoInferior int := EXTRACT(WEEK from fechaPago) - 1;
BEGIN
	
	
	SELECT COUNT(*) INTO desvioNocturno
	FROM viajes
	INNER JOIN desvios
	ON viajes.folio = desvios.viajeId
	WHERE status = 1 and EXTRACT(WEEK from viajes.Fecha) = fechaRangoInferior
			and ConductorId = unidad and desvios.tipoDesvioId = 2;
	
    RETURN desvioNocturno;
END;
$$
LANGUAGE plpgsql;

--SELECT * FROM detalles_viajes;