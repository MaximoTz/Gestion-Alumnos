from Modelo.conexion import conexionBD

def obtener_reporte_calificaciones(carrera):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT 
            A.idAlumno, 
            A.nombre + ' ' + A.apellido AS nombre_completo, 
            C.nombre AS carrera, 
            CL.nota AS calificacion
        FROM Alumno A
        INNER JOIN Carrera C ON A.idCarrera = C.idCarrera
        INNER JOIN Calificacion CL ON A.idAlumno = CL.idAlumno
        WHERE LOWER(C.nombre) = LOWER(?)
    """
    cursor.execute(query, (carrera,))
    resultado = cursor.fetchall()
    return resultado
