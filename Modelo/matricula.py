from Modelo.conexion import conexionBD

def obtenerMatricula():
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT M.idMatricula, A.nombre + ' ' + A.apellido AS Alumno, C.nombre AS Carrera, M.fecha_matricula, E.nombre AS Estado
        FROM Matricula M
        INNER JOIN Alumno A ON M.idAlumno = A.idAlumno
        INNER JOIN Estado E ON M.idEstado = E.idEstado
        INNER JOIN Carrera C ON M.idCarrera = C.idCarrera
    """
    cursor.execute(query)
    matricula = cursor.fetchall()
    return matricula

# FUNCION CRUD (CREATE - READ - UPDATE - DELETE)
# AGREGAR
def registrarMatricula(alumno, carrera, fecha_matricula, estado):
    conexion, cursor = conexionBD.obtenerConexion()
    query_alumno = "SELECT idAlumno FROM Alumno WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_alumno, (alumno,))
    id_alumno = cursor.fetchone()[0]
    cursor.execute("SELECT idCarrera FROM Carrera WHERE nombre = ?", (carrera,))
    id_carrera = cursor.fetchone()[0]
    cursor.execute("SELECT idEstado FROM Estado WHERE nombre = ?", (estado,))
    id_estado = cursor.fetchone()[0]
    
    query = """
        INSERT INTO Matricula (idAlumno, idCarrera, fecha_matricula, idEstado)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (id_alumno, id_carrera, fecha_matricula, id_estado))
    conexion.commit()
    return True

# EDITAR
def editarMatricula(idMatricula, alumno, carrera, fecha_matricula, estado):
    conexion, cursor = conexionBD.obtenerConexion()
    
    cursor.execute("SELECT idAlumno FROM Alumno WHERE CONCAT(nombre, ' ', apellido) = ?", (alumno,))
    id_alumno = cursor.fetchone()[0]
    cursor.execute("SELECT idCarrera FROM Carrera WHERE nombre = ?", (carrera,))
    id_carrera = cursor.fetchone()[0]
    cursor.execute("SELECT idEstado FROM Estado WHERE nombre = ?", (estado,))
    id_estado = cursor.fetchone()[0]
    
    query = """
        UPDATE Matricula
        SET idAlumno = ?, idCarrera = ?, fecha_matricula = ?, idEstado = ?
        WHERE idMatricula = ?
    """
    cursor.execute(query, (id_alumno, id_carrera, fecha_matricula, id_estado, idMatricula))
    conexion.commit()
    return True

# ELIMINAR
def eliminarMatricula(id_matricula):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Matricula WHERE idMatricula = ?"
    cursor.execute(query, (id_matricula,))
    conexion.commit()
    return True

# BUSCAR
def buscarMatricula(id_matricula):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT M.idMatricula, CONCAT(A.nombre, ' ', A.apellido) AS Alumno, 
               C.nombre AS Carrera, M.fecha_matricula, E.nombre AS Estado
        FROM Matricula M
        INNER JOIN Alumno A ON M.idAlumno = A.idAlumno
        INNER JOIN Estado E ON M.idEstado = E.idEstado
        INNER JOIN Carrera C ON M.idCarrera = C.idCarrera
        WHERE M.idMatricula = ?
    """
    cursor.execute(query, (id_matricula,))
    matricula = cursor.fetchone()
    return matricula