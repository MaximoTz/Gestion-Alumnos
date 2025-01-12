from Modelo.conexion import conexionBD

def obtener_reporte_alumnos(carrera):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT A.idAlumno, A.nombre + ' ' + A.apellido AS nombre_completo, C.nombre AS carrera, E.nombre AS estado
        FROM Alumno A
        INNER JOIN Carrera C ON A.idCarrera = C.idCarrera
        INNER JOIN Estado E ON A.idEstado = E.idEstado
        WHERE LOWER(C.nombre) = LOWER(?)
    """
    cursor.execute(query, (carrera,))
    resultado = cursor.fetchall()
    return resultado