from Modelo.conexion import conexionBD

def obtenerUsuarios():
    conexion, cursor = conexionBD.obtenerConexion()
    cursor.execute("SELECT idUsuario, nombre, apellidos, email, idRol, nombre_usuario, contrasenia FROM Usuario")
    usuarios = cursor.fetchall()
    return usuarios

# obtener el idRol basado en el nombre del Rol
def obtenerIdRolPorNombre(rol_nombre):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT idRol FROM Rol WHERE nombre = ?"
    cursor.execute(query, (rol_nombre,))
    rol = cursor.fetchone()
    return rol[0] if rol else None

# FUNCION CRUD (CREATE - READ - UPDATE - DELETE)
# AGREGAR
def agregarUsuario(nombre, apellidos, nombre_usuario, contrasenia, email, idRol):
    conexion, cursor = conexionBD.obtenerConexion() 
    query = """
        INSERT INTO Usuario (nombre, apellidos, nombre_usuario, contrasenia, email, idRol)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (nombre, apellidos, nombre_usuario, contrasenia, email, idRol))
    conexion.commit()
    return True

# EDITAR
def editarUsuario(idUsuario, nombre, apellidos, nombre_usuario, contrasenia, email, idRol):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        UPDATE Usuario SET nombre = ?, apellidos = ?, nombre_usuario = ?, contrasenia = ?, email = ?, idRol = ?
        WHERE idUsuario = ?
    """
    cursor.execute(query, (nombre, apellidos, nombre_usuario, contrasenia, email, idRol, idUsuario))
    conexion.commit()
    return True

# ELIMINAR
def eliminarUsuario(idUsuario):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Usuario WHERE idUsuario = ?"
    cursor.execute(query, (idUsuario,))
    conexion.commit()
    return True

# BUSCAR
def buscarUsuarioPorCodigo(idUsuario):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT U.idUsuario, U.nombre, U.apellidos, U.nombre_usuario, U.contrasenia, U.email, R.nombre  
        FROM Usuario U
        INNER JOIN  Rol R ON U.idRol = R.idRol
        WHERE idUsuario = ?
    """
    cursor.execute(query, (idUsuario,))
    usuario = cursor.fetchone()
    return usuario