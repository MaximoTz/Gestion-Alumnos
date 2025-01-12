from Modelo.conexion import conexionBD

# MOSTRAR TIPO PAGO EN LAS TABLAS
def obtenerPago():
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT 
            BP.idBoleta, 
            A.nombre + ' ' + A.apellido AS alumno,
            BP.monto,
            TP.nombre AS tipo_pago,
            BP.fecha_pago,
            E.nombre AS estado
        FROM Boleta_Pago BP
        INNER JOIN Alumno A ON BP.idAlumno = A.idAlumno
        INNER JOIN TipoPago TP ON BP.idTipoPago = TP.idTipoPago
        INNER JOIN Estado E ON BP.idEstado = E.idEstado
    """
    cursor.execute(query)
    pago = cursor.fetchall()
    return pago

# FUNCION CRUD (CREATE - READ - UPDATE - DELETE)
# AGREGAR
def registraPago(alumno, monto, fecha_pago, tipo_pago, estado):
    conexion, cursor = conexionBD.obtenerConexion()
    query_alumno = "SELECT idAlumno FROM Alumno WHERE CONCAT(nombre, ' ', apellido) = ?"
    cursor.execute(query_alumno, (alumno,))
    id_alumno = cursor.fetchone()
    query_tipo_pago = "SELECT idTipoPago FROM TipoPago WHERE nombre = ?"
    cursor.execute(query_tipo_pago, (tipo_pago,))
    id_tipo_pago = cursor.fetchone()
    query_estado = "SELECT idEstado FROM Estado WHERE nombre = ?"
    cursor.execute(query_estado, (estado,))
    id_estado = cursor.fetchone()

    if id_alumno and id_tipo_pago and id_estado:
        id_alumno = id_alumno[0]
        id_tipo_pago = id_tipo_pago[0]
        id_estado = id_estado[0]

        query_insert = """
            INSERT INTO Boleta_Pago (idAlumno, monto, fecha_pago, idTipoPago, idEstado)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query_insert, (id_alumno, monto, fecha_pago, id_tipo_pago, id_estado))
        conexion.commit()
        return True
    else:
        return False


# EDITAR
def editarPago(id_boleta, alumno_actualizado, monto_actualizado, fecha_pago_actualizado, tipo_pago_actualizado, estado_actualizado):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        UPDATE Boleta_Pago
        SET monto = ?, fecha_pago = ?, idTipoPago = (SELECT idTipoPago FROM TipoPago WHERE nombre = ?), 
            idEstado = (SELECT idEstado FROM Estado WHERE nombre = ?)
        WHERE idBoleta = ?
    """
    cursor.execute(query, (monto_actualizado, fecha_pago_actualizado, tipo_pago_actualizado, estado_actualizado, id_boleta))
    conexion.commit()
    return True


# ELIMINAR
def eliminarPago(id_boleta):
    conexion, cursor = conexionBD.obtenerConexion()
    query = "DELETE FROM Boleta_Pago WHERE idBoleta = ?"
    cursor.execute(query, (id_boleta,)) 
    conexion.commit()
    return True

# BUSCAR
def buscarPago(id_boleta):
    conexion, cursor = conexionBD.obtenerConexion()
    query = """
        SELECT BP.idBoleta, A.nombre, A.apellido, BP.monto, TP.nombre AS tipo_pago, BP.fecha_pago, E.nombre AS estado
        FROM Boleta_Pago BP
        INNER JOIN Alumno A ON BP.idAlumno = A.idAlumno
        INNER JOIN TipoPago TP ON BP.idTipoPago = TP.idTipoPago
        INNER JOIN Estado E ON BP.idEstado = E.idEstado
        WHERE BP.idBoleta = ?
    """
    cursor.execute(query, (id_boleta,))
    resultado = cursor.fetchone()
    return resultado