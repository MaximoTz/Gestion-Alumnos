from Modelo.conexion import conexionBD

# MOSTRAR ALUMNOS (En comboBox)
def mostrarAlumnos():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre, apellido FROM Alumno"
    cursor.execute(query)
    alumnos = cursor.fetchall()
    return alumnos

# MOSTRAR ALUMNOS EN LAS TABLAS
def obtenerAlumnos():
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
            SELECT idAlumno, nombre, apellido, dni, telefono, email, 
                   (SELECT nombre FROM Carrera WHERE idCarrera = a.idCarrera) AS carrera,
                   (SELECT nombre FROM Estado WHERE idEstado = a.idEstado) AS estado
            FROM Alumno a
        """
    cursor.execute(query)
    alumnos = cursor.fetchall()
    return alumnos

# FUNCION CRUD (CREATE - READ - UPDATE - DELETE)
# AGREGAR
def registrarAlumno(codigo, nombre, apellido, dni, telefono, email, carrera, estado):
    conexion, cursor = conexionBD.obtenerConexion()
    query_carrera = "SELECT idCarrera FROM Carrera WHERE nombre = ?"
    cursor.execute(query_carrera, carrera)
    id_carrera = cursor.fetchone()
    if not id_carrera:
        return False
    query_estado = "SELECT idEstado FROM Estado WHERE nombre = ?"
    cursor.execute(query_estado, (estado,))
    id_estado = cursor.fetchone()
    if not id_estado:
        return False
    query = """
        INSERT INTO Alumno (idAlumno, nombre, apellido, dni, telefono, email, idCarrera, idEstado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (codigo, nombre, apellido, dni, telefono, email, id_carrera[0], id_estado[0]))
    conexion.commit()
    return True

# EDITAR
def editarAlumno(id_alumno, nombre, apellido, dni, telefono, email, carrera, estado):
    conexion, cursor = conexionBD.obtenerConexion()

    query_carrera = "SELECT idCarrera FROM Carrera WHERE nombre = ?"
    cursor.execute(query_carrera, (carrera,))
    id_carrera = cursor.fetchone()
    if not id_carrera:
        return False 

    query_estado = "SELECT idEstado FROM Estado WHERE nombre = ?"
    cursor.execute(query_estado, (estado,))
    id_estado = cursor.fetchone()
    if not id_estado:
        return False  

    query = """
        UPDATE Alumno
        SET nombre = ?, apellido = ?, dni = ?, telefono = ?, email = ?, 
            idCarrera = ?, idEstado = ?
        WHERE dni = ?
    """
    cursor.execute(query, (nombre, apellido, dni, telefono, email, id_carrera[0], id_estado[0], id_alumno))
    conexion.commit()
    return True

#ELIMINAR
def eliminarAlumno(dni_alumno):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Alumno WHERE dni = ?"
    cursor.execute(query, (dni_alumno,))
    conexion.commit()
    return True

# BUSCAR
def buscarAlumno(dni_alumno):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT 
            A.idAlumno, A.nombre, A.apellido, A.dni, A.telefono, A.email, 
            C.nombre AS carrera, E.nombre
        FROM Alumno A
        INNER JOIN Carrera C ON A.idCarrera = C.idCarrera
        INNER JOIN Estado E ON A.idEstado = E.idEstado
        WHERE A.dni = ?
    """
    cursor.execute(query, (dni_alumno,))
    resultado = cursor.fetchone()
    return resultado


# VERIFICAR
def verificarAlumnoExistente(codigo, dni, email):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
            SELECT COUNT(*)
            FROM Alumno
            WHERE idAlumno = ? OR dni = ? OR email = ?
        """
    cursor.execute(query, (codigo, dni, email))
    resultado = cursor.fetchone()
    
    return resultado[0] > 0