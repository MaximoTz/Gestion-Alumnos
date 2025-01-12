CREATE DATABASE BDUTP
GO

USE BDUTP

CREATE TABLE Rol (
    idRol INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL UNIQUE,
	descripcion TEXT
);

INSERT INTO Rol VALUES 
('Administrador','Gestiona usuarios, roles y configuraciones del sistema'),
('Personal Academico', 'Organiza horarios y gestiona los reportes, cursos, pagos y todo lo relacionado al alumnado'),
('Profesor(a)','Gestiona clases, tareas y evaluaciones de estudiantes')

CREATE TABLE Usuario (
    idUsuario INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL,              
    apellidos VARCHAR(50) NOT NULL,        
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE, 
	contrasenia VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,         
    fotoPerfil VARBINARY(MAX) NULL,          
    idRol INT NOT NULL,                       
    FOREIGN KEY (idRol) REFERENCES Rol(idRol)
);

INSERT INTO Usuario (nombre, apellidos, nombre_usuario, contrasenia, email, fotoPerfil, idRol) 
VALUES 
('Juan', 'Perez', 'admin', 'admin123', 'jp14@gmail.com', NULL, 1),
('Maria', 'Peña', 'personal', 'personal123', 'mp20@gmail.com', NULL, 2),
('Pedro', 'Lopez', 'profesor','profesor123','pl10@gmail.com', NULL, 3);

CREATE TABLE Carrera (
    idCarrera INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO Carrera VALUES 
('Abogacía / Derecho'),
('Administración de Empresas'), 
('Arte Dramático'), 
('Artes Plásticas'), 
('Artes y Diseño'), 
('Biotecnología'),  
('Ciencias Ambientales'), 
('Ciencias de la Computación e Informática'), 
('Ciencias Políticas y Relaciones Internacionales'), 
('Comunicaciones y Periodismo'), 
('Contabilidad'), 
('Desarrollo de Software'), 
('Economía y Finanzas'),
('Educación'), 
('Enfermería'), 
('Estudios Latinoamericanos y Estudios Globales'), 
('Fisiología Animal'),
('Historia'), 
('Informática Forense'), 
('Ingeniería Aeroespacial y Mecánica'), 
('Ingeniería Civil'), 
('Ingeniería de Sistemas'), 
('Ingeniería Eléctrica y Electrónica'), 
('Ingeniería Industrial'), 
('Ingeniería Química'), 
('Literatura e Idiomas'), 
('Marketing Digital'), 
('Matemáticas'), 
('Medicina Nuclear, Radiología y Radioterapia'), 
('Medicina Veterinaria'), 
('Música y Composición Musical'), 
('Nutrición y Dietética'), 
('Psicología'), 
('Seguridad Nacional e Inteligencia'), 
('Terapia Ocupacional y Rehabilitación'), 
('Turismo');

CREATE TABLE Estado (
    idEstado INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO Estado (nombre) VALUES 
('Activo'),
('Inactivo'),
('Retirado'),
('Pendiente'),
('Pagado'),
('Finalizado'),
('Suspendido');

CREATE TABLE Alumno (
    idAlumno NVARCHAR(60) PRIMARY KEY NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(8) NOT NULL UNIQUE,
    telefono CHAR(9) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    idCarrera INT NOT NULL,
    idEstado INT NOT NULL,
    FOREIGN KEY (idCarrera) REFERENCES Carrera(idCarrera),
    FOREIGN KEY (idEstado) REFERENCES Estado(idEstado)
);

CREATE TABLE TipoPago (
    idTipoPago INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL UNIQUE
)

INSERT INTO TipoPago (nombre) VALUES 
('Tarjeta'),
('Efectivo'),
('Pago Movil');

CREATE TABLE Boleta_Pago (
    idBoleta INT PRIMARY KEY IDENTITY(1,1),
    idAlumno NVARCHAR(60) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    idTipoPago INT NOT NULL,
    fecha_pago DATE NOT NULL,
    idEstado INT NOT NULL,
    FOREIGN KEY (idAlumno) REFERENCES Alumno(idAlumno),
    FOREIGN KEY (idEstado) REFERENCES Estado(idEstado),
    FOREIGN KEY (idTipoPago) REFERENCES TipoPago(idTipoPago)
);

CREATE TABLE Docente (
    idDocente NVARCHAR(60) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(8) NOT NULL UNIQUE,
    telefono CHAR(9) NOT NULL UNIQUE,
    email VARCHAR(50) UNIQUE
);

CREATE TABLE Calificacion (
    idCalificacion INT PRIMARY KEY IDENTITY(1,1),
    idAlumno NVARCHAR(60) NOT NULL,
    idDocente NVARCHAR(60) NOT NULL,
    idCarrera INT NOT NULL,
    nota DECIMAL(5, 2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (idAlumno) REFERENCES Alumno(idAlumno),
    FOREIGN KEY (idDocente) REFERENCES Docente(idDocente),
    FOREIGN KEY (idCarrera) REFERENCES Carrera(idCarrera)  
);

CREATE TABLE Matricula (
    idMatricula INT PRIMARY KEY IDENTITY(1,1),
    idAlumno NVARCHAR(60) NOT NULL,
    idCarrera INT NOT NULL,
    fecha_matricula DATE NOT NULL,
    idEstado INT NOT NULL DEFAULT 1,
    FOREIGN KEY (idAlumno) REFERENCES Alumno(idAlumno),
    FOREIGN KEY (idCarrera) REFERENCES Carrera(idCarrera),
    FOREIGN KEY (idEstado) REFERENCES Estado(idEstado)
);

