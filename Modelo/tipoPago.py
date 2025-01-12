from Modelo.conexion import conexionBD

# MOSTRAR TIPO PAGO (En comboBox)
def mostrarTipoPago():
    conexion, cursor = conexionBD.obtenerConexion()
    query = "SELECT nombre FROM TipoPago"
    cursor.execute(query)
    tipo_pago = cursor.fetchall()
    return [fila.nombre for fila in tipo_pago]


