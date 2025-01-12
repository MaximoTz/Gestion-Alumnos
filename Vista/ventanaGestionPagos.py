import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import QDate
from Modelo.alumnos import mostrarAlumnos
from Modelo.estado import mostrarEstado
from Modelo.tipoPago import mostrarTipoPago
from Modelo.gestionPagos import obtenerPago, registraPago, buscarPago, eliminarPago, editarPago

class VentanaGestionarPagos(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaGestionarPagos, self).__init__(parent)
        uic.loadUi("UI/ventanaGestionPagos.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargarAlumnos()
        self.cargarEstado()
        self.cargarTipoPago()
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarPago)
        self.btnEditar.clicked.connect(self.editarPago)
        self.btnEliminar.clicked.connect(self.eliminarPago)
        self.btnBuscar.clicked.connect(self.buscarPago)
        self.btnVolver.clicked.connect(self.botonVolver)

    
    def botonVolver(self):
        if self.rol_usuario == "Administrador":
            from Vista.ventanaAdministrador import VentanaAdministrador
            self.administrador = VentanaAdministrador(rol_usuario = self.rol_usuario)
            self.administrador.show()
        elif self.rol_usuario == "Personal":
            from Vista.ventanaPersonal import VentanaPersonal
            self.personal = VentanaPersonal(rol_usuario = self.rol_usuario)
            self.personal.show()
        elif self.rol_usuario == "Profesor":
            from Vista.ventanaProfesor import VentanaProfesor
            self.profesor = VentanaProfesor(rol_usuario = self.rol_usuario)
            self.profesor.show()
        self.close()

    def cargarAlumnos(self):
        alumnos = mostrarAlumnos()
        if alumnos:
            self.cmbAlumno.addItems([f"{alumno[0]} {alumno[1]}" for alumno in alumnos])
        else:
            QMessageBox.warning(self, "Error", "No se encontraron alumnos")

    def cargarTipoPago(self):
        tipoPago = mostrarTipoPago()
        if tipoPago:
            self.cmbTipoPago.addItems(tipoPago)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron tipos de pago")

    def cargarEstado(self):
        estados = mostrarEstado()
        if estados:
            self.cmbEstado.addItems(estados)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron estados")

    def limpiarCampos(self):
        self.cmbAlumno.setCurrentIndex(0) 
        self.txtMonto.clear() 
        self.cmbTipoPago.setCurrentIndex(0) 
        self.dteFechaPago.setDate(self.dteFechaPago.minimumDate()) 
        self.cmbEstado.setCurrentIndex(0) 

    def actualizarTabla(self):
        self.tblPagos.setColumnCount(6)
        self.tblPagos.setHorizontalHeaderLabels([
            "ID Boleto", "Alumno", "Monto", "Tipo Pago", 
            "Fecha Pago", "Estado"
        ])

        self.tblPagos.setRowCount(0)

        pagos = obtenerPago()
        for pago in pagos:
            row_position = self.tblPagos.rowCount()
            self.tblPagos.insertRow(row_position)
            for col, value in enumerate(pago):
                self.tblPagos.setItem(row_position, col, QTableWidgetItem(str(value)))

        header = self.tblPagos.horizontalHeader()
        for i in range(self.tblPagos.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def registrarPago(self):
        alumno = self.cmbAlumno.currentText()
        monto = self.txtMonto.text()
        fecha_pago = self.dteFechaPago.date().toString("yyyy-MM-dd")
        tipo_pago = self.cmbTipoPago.currentText()
        estado = self.cmbEstado.currentText()

        if not all ([alumno, monto, fecha_pago, tipo_pago, estado]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
        
        try:
            monto = float(monto) 
        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser un número válido.")
            return

        if registraPago(alumno, monto, fecha_pago, tipo_pago, estado):
            QMessageBox.information(self, "Exito", "Pago registrado con exito")
            self.actualizarTabla()
            self.limpiarCampos()
        else:
            QMessageBox.warning(self, "Error", "Error al registrar pago")


    def editarPago(self):
        if not hasattr(self, 'id_boleta_actual'):
            QMessageBox.warning(self, "Error", "No se ha seleccionado ningún pago para editar.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar edición",
            "¿Desea guardar los cambios realizados?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            alumno_actualizado = self.cmbAlumno.currentText()
            monto_actualizado = self.txtMonto.text()
            fecha_pago_actualizado = self.dteFechaPago.date().toString('yyyy-MM-dd')
            tipo_pago_actualizado = self.cmbTipoPago.currentText()
            estado_actualizado = self.cmbEstado.currentText()

            id_boleta = self.id_boleta_actual 
            if editarPago(id_boleta, alumno_actualizado, monto_actualizado, fecha_pago_actualizado, tipo_pago_actualizado, estado_actualizado):
                QMessageBox.information(self, "Éxito", "Los datos se han actualizado correctamente.")
                self.actualizarTabla()
                self.limpiarCampos()
            else:
                QMessageBox.warning(self, "Error", "No se pudieron guardar los cambios. Verifique los datos.")

    def eliminarPago(self):
        id_boleta, ok = QInputDialog.getText(
            self, "Eliminar Pago", "Ingrese el ID de la boleta a eliminar: "
        )

        if ok and id_boleta:
            resultado = buscarPago(id_boleta) 
            if resultado:
                self.id_boleta_actual = resultado[0]

                idBoleta, nombreAlumno, monto, tipoPago, fechaPago, estado = resultado
                self.cmbAlumno.setCurrentText(nombreAlumno)
                self.txtMonto.setText(str(monto))
                self.cmbTipoPago.setCurrentText(tipoPago)
                
                fecha_qdate = QDate.fromString(fechaPago, 'yyyy-MM-dd')
                self.dteFechaPago.setDate(fecha_qdate)

                self.cmbEstado.setCurrentText(estado)

                respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                                f"¿Estás seguro que deseas eliminar la boleta con ID: {idBoleta}?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if respuesta == QMessageBox.Yes:
                    if eliminarPago(idBoleta):
                        QMessageBox.information(self, "Éxito", "La boleta se eliminó con éxito")
                        self.actualizarTabla()
                        self.limpiarCampos()
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo eliminar la boleta")
            else:
                QMessageBox.warning(self, "Error", "No se encontraron pagos")

    def buscarPago(self):
        id_boleta, ok = QInputDialog.getText(self, "Buscar Pago", "Ingrese el ID de la boleta: ")

        if ok and id_boleta:
            resultado = buscarPago(id_boleta) 
            if resultado:
                self.id_boleta_actual = resultado[0]

                idBoleta, nombreAlumno, apellidoAlumno, monto, tipoPago, fechaPago, estado = resultado
                
                nombre_completo = f"{nombreAlumno} {apellidoAlumno}"
                index = self.cmbAlumno.findText(nombre_completo)
                if index != -1:
                    self.cmbAlumno.setCurrentIndex(index)

                self.txtMonto.setText(str(monto))
                self.cmbTipoPago.setCurrentText(tipoPago)
                fecha_qdate = QDate.fromString(fechaPago, 'yyyy-MM-dd')
                self.dteFechaPago.setDate(fecha_qdate)
                self.cmbEstado.setCurrentText(estado)
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se encontraron pagos.")