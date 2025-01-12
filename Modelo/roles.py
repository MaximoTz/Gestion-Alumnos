from Modelo.conexion import conexionBD

def obtenerRoles():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre FROM Rol"
    cursor.execute(query)
    roles = [rol[0] for rol in cursor.fetchall()]
    return roles