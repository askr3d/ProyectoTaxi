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
	
CREATE TABLE Conductores(
	Id serial,
	Unidad varchar(15) not null,
	Nombre varchar(35) not null,
	primary key(Id)
);

CREATE TABLE Autos(
	ConductorId int references Conductores(Id),
	Modelo varchar(15),
	Anio char(5),
	Placas varchar(15),
	primary key(ConductorId)
);

CREATE TABLE Partidas(
	Id serial,
	Nombre varchar(25) not null,
	primary key(Id)
);

CREATE TABLE Empresas(
	Id serial,
	Nombre varchar(35) not null,
	Domicilio varchar(35) not null,
	Telefono varchar(15),
	primary key(Id)
);

CREATE TABLE Rutas(
	Id serial,
	Nombre varchar(40),
	EmpresaId int references Empresas(Id),
	primary key(Id)
);

CREATE TABLE Viajes(
	Id serial,
	Folio varchar(15),
	Fecha date,
	HoraInicio time,
	HoraFin time,
	Kilometros float,
	Costo numeric(8, 2),
	ConductorId int references Conductores(Id),
	PartidaId int references Partidas(Id),
	RutaId int references Rutas(Id),
	primary key(Id)
);

CREATE TABLE Pasajeros(
	ViajeId int references Viajes(Id),
	Nombre varchar(50),
	Destino varchar(50),
	primary key(ViajeId)
);