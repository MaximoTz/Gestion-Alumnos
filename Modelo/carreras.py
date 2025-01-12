from Modelo.conexion import conexionBD

def mostrarCarreras():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre FROM Carrera"
    cursor.execute(query)
    carreras = cursor.fetchall()
    return [carrera[0] for carrera in carreras]