from Modelo.conexion import conexionBD

def obtenerCredenciales():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre_usuario, contrasenia, idRol FROM Usuario"  
    cursor.execute(query)
    credenciales = cursor.fetchall()
    return credenciales