from Modelo.conexion import conexionBD

def mostrarEstado():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre FROM Estado"
    cursor.execute(query)
    estado = cursor.fetchall()
    return [estado[0] for estado in estado]
