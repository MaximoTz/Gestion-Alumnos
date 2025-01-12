from Modelo.conexion import conexionBD

def obtener_reporte_pagos(estado):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT BP.idBoleta, A.nombre + ' ' + A.apellido AS nombre_completo, E.nombre AS estado, BP.monto AS monto
        FROM Alumno A
        INNER JOIN Estado E ON A.idEstado = E.idEstado
        INNER JOIN Boleta_Pago BP ON A.idAlumno = BP.idAlumno
        WHERE LOWER(E.nombre) = LOWER(?)
    """
    cursor.execute(query, (estado,))
    resultado = cursor.fetchall()
    return resultado