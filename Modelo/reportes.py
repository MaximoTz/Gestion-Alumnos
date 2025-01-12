from Modelo.conexion import conexionBD

def obtener_alumnos():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT id, nombre, apellido, email FROM alumnos"
    cursor.execute(query)
    alumnos = cursor.fetchall()
    return alumnos

def obtener_calificaciones():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT id_alumno, asignatura, calificacion FROM calificaciones"
    cursor.execute(query)
    calificaciones = cursor.fetchall()
    return calificaciones

def obtener_pagos():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT id_alumno, monto, fecha_pago FROM pagos"
    cursor.execute(query)
    pagos = cursor.fetchall()
    return pagos