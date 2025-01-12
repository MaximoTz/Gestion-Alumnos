from Modelo.conexion import conexionBD

#
def obtenerCalificaciones():
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT Cal.idCalificacion, A.nombre + ' ' + A.apellido, 
        D.nombre + ' ' + D.apellido, C.nombre, Cal.nota, Cal.fecha
        FROM Calificacion Cal
        INNER JOIN Alumno A ON Cal.idAlumno = A.idAlumno
        INNER JOIN Docente D ON Cal.idDocente = D.idDocente
        INNER JOIN Carrera C ON Cal.idCarrera = C.idCarrera
    """
    cursor.execute(query)
    resultado = cursor.fetchall()
    return resultado

# CRUD (AGREGAR - EDITAR - ELIMINAR - BUSCAR)
# AGREGAR
def agregarCalificacion(alumno, docente, carrera, nota, fecha):
    conexion, cursor = conexionBD.obtenerConexion()

    query_alumno = "SELECT idAlumno FROM Alumno WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_alumno, (alumno,))
    idAlumno = cursor.fetchone()
    if not idAlumno:
        return False 

    query_docente = "SELECT idDocente FROM Docente WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_docente, (docente,))
    idDocente = cursor.fetchone()
    if not idDocente:
        return False 

    query_carrera = "SELECT idCarrera FROM Carrera WHERE nombre = ?"
    cursor.execute(query_carrera, (carrera,))
    idCarrera = cursor.fetchone()
    if not idCarrera:
        return False  

    query = """
        INSERT INTO Calificacion (idAlumno, idDocente, idCarrera, nota, fecha)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (idAlumno[0], idDocente[0], idCarrera[0], nota, fecha))
    conexion.commit()

    return True 

    
# EDITAR
def editarCalificacion(idCalificacion, alumno, docente, carrera, nota, fecha):
    conexion, cursor = conexionBD.obtenerConexion()

    query_alumno = "SELECT idAlumno FROM Alumno WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_alumno, (alumno,))
    idAlumno = cursor.fetchone()
    if not idAlumno:
        return False 

    query_docente = "SELECT idDocente FROM Docente WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_docente, (docente,))
    idDocente = cursor.fetchone()
    if not idDocente:
        return False 

    query_carrera = "SELECT idCarrera FROM Carrera WHERE nombre = ?"
    cursor.execute(query_carrera, (carrera,))
    idCarrera = cursor.fetchone()
    if not idCarrera:
        return False

    query = """
        UPDATE Calificacion
        SET idAlumno = ?, idDocente = ?, idCarrera = ?, nota = ?, fecha = ?
        WHERE idCalificacion = ?
    """
    cursor.execute(query, (idAlumno[0], idDocente[0], idCarrera[0], nota, fecha, idCalificacion))
    conexion.commit()

    return True 

# ELIMINAR
def eliminarCalificacion(id_calificacion):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Calificacion WHERE idCalificacion = ?"
    cursor.execute(query, (id_calificacion),)
    conexion.commit()
    return True

# BUSCAR
def buscarCalificacion(id_calificacion):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT Cal.idCalificacion, CONCAT(A.nombre, ' ', A.apellido) AS Alumno,
                CONCAT(D.nombre, ' ', D.apellido) AS Docente, C.nombre, Cal.nota,
                Cal.fecha
        FROM Calificacion Cal
        INNER JOIN Alumno A ON Cal.idAlumno = A.idAlumno
        INNER JOIN Docente D ON Cal.idDocente = D.idDocente
        INNER JOIN Carrera C ON Cal.idCarrera = C.idCarrera
        WHERE Cal.idCalificacion = ?
    """
    cursor.execute(query, (id_calificacion,))
    resultado = cursor.fetchone()
    return resultado