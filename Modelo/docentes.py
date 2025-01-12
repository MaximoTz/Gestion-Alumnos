from Modelo.conexion import conexionBD
# MOSTRAR DOCENTES (En comboBox)
def mostrarDocentes():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre, apellido FROM Docente"
    cursor.execute(query)
    docentes = cursor.fetchall()
    return docentes

# MOSTRAR ALUMNOS EN LAS TABLAS
def obtenerDocentes():
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
            SELECT idDocente, nombre, apellido, dni, telefono, email
            FROM Docente
        """
    cursor.execute(query)
    docentes = cursor.fetchall()
    return docentes

# FUNCION CRUD (CREATE - READ - UPDATE - DELETE)
# AGREGAR
def agregarDocente(id_docente, nombre, apellido, dni, telefono, email):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        INSERT INTO Docente (idDocente, nombre, apellido, dni, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (id_docente, nombre, apellido, dni, telefono, email))
    conexion.commit()
    return True

# EDITAR
def editarDocente(id_docente, nombre, apellido, dni, telefono, email):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        UPDATE Docente
        SET nombre = ?, apellido = ?, dni = ?, telefono = ?, email = ?
        WHERE dni = ?
    """
    cursor.execute(query, (nombre, apellido, dni, telefono, email, id_docente))
    conexion.commit()
    return True

# ELIMINAR
def eliminarDocente(dni_docente):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Docente WHERE dni = ?"
    cursor.execute(query, (dni_docente,))
    conexion.commit()
    return True

# BUSCAR
def buscarDocente(dni_docente):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT idDocente, nombre, apellido, dni, telefono, email FROM Docente
        WHERE dni = ?
    """
    cursor.execute(query, (dni_docente,))
    docente = cursor.fetchone()
    return docente

# VERIFICAR
def verificarDocente(id_docente, dni_docente):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT COUNT(*)
        FROM Docente
        WHERE idDocente = ? OR dni = ?
    """
    cursor.execute(query, (id_docente, dni_docente))
    resultado = cursor.fetchone()[0]
    return resultado > 0