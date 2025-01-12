import pyodbc

import pyodbc

class conexionBD:
    _conexion = None
    _cursor = None

    def obtenerConexion():
        if conexionBD._conexion is None:
            conexionBD._conexion = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=PCMAX;'
                'DATABASE=BDUTP;'
                'UID=sa;'
                'PWD=210105;'
            )
            conexionBD._cursor = conexionBD._conexion.cursor()
        return conexionBD._conexion, conexionBD._cursor
    
    def cerrarConexion():
        if conexionBD._conexion:
            conexionBD._cursor.close()
            conexionBD._conexion.close()
            conexionBD._conexion = None
            conexionBD._cursor = None


"""def obtenerConexion():
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=PCMAX;'
        'DATABASE=BDUTP;'
        'UID=sa;'
        'PWD=210105;'
    )
    cursor = conexion.cursor()
    return conexion, cursor"""
    