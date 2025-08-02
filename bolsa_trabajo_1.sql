create database bolsa_trabajo_1;
use bolsa_trabajo_1;

create table login(
	id int auto_increment,
    correo varchar(100),
    contra varchar(255),
    tipo_usuario enum('aspirante', 'admin', 'reclutador') default 'aspirante',
    primary key (id)
);

insert into login(correo, contra, tipo_usuario)
values
('admin@workfy.com', 's2022025', 'admin');

insert into login(correo, contra, tipo_usuario)
values
('admin01@workfy.com', '123456789', 'admin');

create table empleos( -- Catalogo
	id int auto_increment,
    empleo varchar(100),
    primary key (id)
);

INSERT INTO empleos (empleo) VALUES 
('Becario'),
('Auxiliar en Sistemas'),
('Desarrollador Junior'),
('Técnico en Informática'),
('Analista de Datos'),
('Administrador de Sistemas'),
('Programador Web'),
('Diseñador Web'),
('Consultor IT');

create table experiencia ( -- Catalogo
	id int auto_increment,
    experiencia varchar(100),
    primary key (id)
);

INSERT INTO experiencia (experiencia) VALUES 
('Sin experiencia'),
('Menos de 1 año'),
('1-2 años'),
('3-5 años'),
('5-10 años'),
('Más de 10 años');

create table grado_estudios ( -- Catalogo
	id int auto_increment,
    grado varchar(150),
    primary key (id)
);

INSERT INTO grado_estudios (grado) VALUES 
('Secundaria'),
('Preparatoria/Bachillerato'),
('Técnico Superior'),
('Licenciatura en curso'),
('Licenciatura terminada'),
('Ingeniería en curso'),
('Ingeniería terminada');

create table ciudad_referencia ( -- Catalogo
	id int auto_increment,
    ciudad varchar (150),
    primary key(id)
);

INSERT INTO ciudad_referencia (ciudad) VALUES 
('Amealco de Bonfil'),
('Arroyo Seco'),
('Cadereyta de Montes'),
('Colón'),
('Corregidora'),
('Ezequiel Montes'),
('Huimilpan'),
('Jalpan de Serra'),
('Landa de Matamoros'),
('El Marqués'),
('Pedro Escobedo'),
('Peñamiller'),
('Pinal de Amoles'),
('Querétaro'),
('San Joaquín'),
('San Juan del Río'),
('Tequisquiapan'),
('Tolimán');

create table cp (
	id int auto_increment,
    cp varchar (5),
    primary key (id)
);

create table informacion(
	id int auto_increment,
    id_usuario int,
    nombre varchar(100),
    apellidos varchar(150),
    id_empleos int,
    id_experiencia int, 
    id_grado_estudios int, 
    id_ciudad int,
    id_cp int,
    foreign key (id_usuario) references login (id),
    foreign key (id_experiencia) references experiencia (id),
    foreign key (id_empleos) references empleos (id),
    foreign key (id_grado_estudios) references grado_estudios (id),
    foreign key (id_ciudad) references ciudad_referencia (id),
    foreign key (id_cp) references cp (id),
    primary key (id)
);

