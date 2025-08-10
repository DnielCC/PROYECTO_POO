create database bolsa_trabajo_1;
use bolsa_trabajo_1;


create table estatus(
	id int auto_increment,
    estatus varchar(150),
    primary key (id)
);

insert into estatus (estatus) values
('Activa'),
('Pausada'),
('Cerrada'),
('En Revisión'),
('Aceptado'),
('Rechazado'); 

-- INICIA INFORMACIÓN DE REGISTRO DE USUARIOS
create table login(
	id int auto_increment,
    correo varchar(100),
    contra varchar(255),
    username varchar(150) null,
    tipo_usuario enum('aspirante', 'admin', 'reclutador') default 'aspirante',
    primary key (id)
);


insert into login(correo, contra, username ,tipo_usuario)
values
('admin@workfy.com', '123456789', 'Administrador prueba','admin'),
('reclutador@workfy.com', '123456789', 'Reclutador prueba','reclutador'),
('usuario@workfy.com', '123456789', 'Usuario prueba','aspirante');



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
-- TERMINA INFORMACIÓN DE REGISTRO DE USUARIOS


-- INICIA INFORMACIÓN PARA VACANTES
CREATE TABLE empresas (
    id INT AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tipos_trabajo ( -- Catalogo
    id INT AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

insert into tipos_trabajo (nombre) values
('Tiempo Completo'),
('Medio Tiempo'),
('Por Contrato'),
('Prácticas');

CREATE TABLE modalidades_trabajo ( -- Catalogo
    id INT AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

insert into modalidades_trabajo (nombre) values
('Presencial'),
('Remoto'),
('Híbrido');


CREATE TABLE niveles_experiencia ( -- Catalogo
    id INT AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

insert into niveles_experiencia (nombre) values 
('Sin experiencia'),
('Junior (1-3 años)'),
('Mid-level (3-5 años)'),
('Senior (5+ años)'),
('Lead/Manager');


CREATE TABLE ubicaciones (
    id INT AUTO_INCREMENT,
    ciudad VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE vacantes (
    id INT AUTO_INCREMENT,
    id_usuario int,
    id_empresa INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    id_ubicacion INT NOT NULL,
    id_tipo_trabajo INT NOT NULL,
    id_modalidad_trabajo INT NOT NULL,
    salario_minimo DECIMAL(10,2),
    salario_maximo DECIMAL(10,2),
    id_nivel_experiencia INT,
    fecha_limite DATE,
    numero_vacantes INT,
    descripcion TEXT NOT NULL,
    requisitos TEXT NOT NULL,
    beneficios TEXT,
    email_contacto VARCHAR(100) NOT NULL,
    telefono_contacto VARCHAR(20),
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activa BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    foreign key (id_usuario) references login(id),
    FOREIGN KEY (id_empresa) REFERENCES empresas(id),
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id),
    FOREIGN KEY (id_tipo_trabajo) REFERENCES tipos_trabajo(id),
    FOREIGN KEY (id_modalidad_trabajo) REFERENCES modalidades_trabajo(id),
    FOREIGN KEY (id_nivel_experiencia) REFERENCES niveles_experiencia(id)
);

CREATE TABLE habilidades (
    id INT AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE vacantes_habilidades_requeridas (
	id INT auto_increment,
    id_vacante INT NOT NULL,
    id_habilidad INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vacante) REFERENCES vacantes(id),
    FOREIGN KEY (id_habilidad) REFERENCES habilidades(id)
);


CREATE TABLE vacantes_habilidades_deseadas (
	id int auto_increment,
    id_vacante INT NOT NULL,
    id_habilidad INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_vacante) REFERENCES vacantes(id),
    FOREIGN KEY (id_habilidad) REFERENCES habilidades(id)
);

CREATE TABLE estado_vacantes (
	id int auto_increment,
    id_vacante int, 
    id_estatus int default 1,
    primary key (id),
    foreign key (id_vacante) references vacantes(id),
    foreign key (id_estatus) references estatus(id)
);
-- TERMINA INFORMACIÓN PARA VACANTES

-- INICIA INFORMACIÓN DE POSTULACIÓNES

CREATE TABLE postulaciones (
	id int auto_increment,
    id_usuario int,
    id_vacante int,
    id_estatus int default 4,
    fecha_postulacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) references login(id),
    FOREIGN KEY (id_vacante) REFERENCES vacantes(id),
    foreign key (id_estatus) references estatus(id)
);