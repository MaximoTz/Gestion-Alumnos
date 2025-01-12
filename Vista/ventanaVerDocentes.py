import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QInputDialog
from Modelo.docentes import obtenerDocentes, agregarDocente, editarDocente, eliminarDocente, buscarDocente, verificarDocente

class VentanaVerDocentes(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaVerDocentes, self).__init__(parent)
        uic.loadUi("UI/ventanaAgregarDocentes.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarDocentes)
        self.btnEditar.clicked.connect(self.editarDocentes)
        self.btnEliminar.clicked.connect(self.eliminarDocente)
        self.btnBuscar.clicked.connect(self.buscarDocente)
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

    def limpiarCampos(self):
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtDNI.clear()
        self.txtTelefono.clear()
        self.txtEmail.clear()

    def actualizarTabla(self):
        self.tblDocentes.setColumnCount(6)
        self.tblDocentes.setHorizontalHeaderLabels([
            "ID Docente", "Nombre", "Apellido", "DNI",
            "Teléfono", "Email"
        ])
        self.tblDocentes.setRowCount(0)

        docentes = obtenerDocentes()
        for docente in docentes:
            row_position = self.tblDocentes.rowCount()
            self.tblDocentes.insertRow(row_position)
            for col, value in enumerate(docente):
                self.tblDocentes.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblDocentes.horizontalHeader()
        for columna in range(self.tblDocentes.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

    def registrarDocentes(self):
        codigo = self.txtCodigo.text()
        nombre = self.txtNombre.text()
        apellido = self.txtApellido.text()
        dni = self.txtDNI.text()
        telefono = self.txtTelefono.text()
        email = self.txtEmail.text()

        if not all([codigo, nombre, apellido, dni, telefono, email]):
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos")
            return

        if verificarDocente(codigo, dni):
            QMessageBox.warning(self, "Error", "El docente ya existe")
            self.limpiarCampos()
            return

        if agregarDocente(codigo, nombre, apellido, dni, telefono, email):
            QMessageBox.information(self, "Exito", "Docente agregado con exito")
            self.actualizarTabla()
            self.limpiarCampos()
        else:
            QMessageBox.warning(self, "Error", "Error al agregar docente")

    def editarDocentes(self):
        respuesta = QMessageBox.question(
            self, "Confirmar edición",
            "¿Desea guardar los cambios realizados?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return
        
        if respuesta == QMessageBox.Yes:
            nombre_actualizado = self.txtNombre.text()
            apellido_actualizado = self.txtApellido.text()
            dni_actualizado = self.txtDNI.text()
            telefono_actualizado = self.txtTelefono.text()
            email_actualizado = self.txtEmail.text()

            if not all([nombre_actualizado, apellido_actualizado, dni_actualizado, telefono_actualizado, email_actualizado]):
                QMessageBox.warning(self, "Error", "Por favor, complete todos los campos antes de guardar.")
                return

            if editarDocente(
                self.dni_docente_actual, nombre_actualizado, apellido_actualizado, dni_actualizado, telefono_actualizado, email_actualizado
            ):
                QMessageBox.information(self, "Exito", "Docente editado con exito")
                self.actualizarTabla()
                self.limpiarCampos()
                del self.dni_docente_actual
            else:
                QMessageBox.warning(self, "Error", "Error al editar docente")
    
    def eliminarDocente(self):
        dni_docente, ok = QInputDialog.getText(
            self, "Eliminar Docente", "Ingrese el DNI del docente:"
        )

        if ok and dni_docente:
            resultado = buscarDocente(dni_docente)
            if resultado:

                id_docente, nombre, apellido, dni, telefono, email = resultado
                self.txtCodigo.setText(id_docente)
                self.txtNombre.setText(nombre)
                self.txtApellido.setText(apellido)
                self.txtDNI.setText(dni)
                self.txtTelefono.setText(telefono)
                self.txtEmail.setText(email)
                
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Desea eliminar al docente con DNI: {dni_docente}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

                if respuesta == QMessageBox.Yes:
                    if eliminarDocente(dni_docente):
                        QMessageBox.information(
                            self, "Eliminación Exitosa", "El docente se ha eliminado correctamente."
                        )
                        self.actualizarTabla()
                        self.limpiarCampos()
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo eliminar el docente. Verifique la información."
                        )
                else:
                    self.limpiarCampos()
            else:
                QMessageBox.warning(
                    self, "Error", "No se encontró un docente con ese DNI."
                )

    def buscarDocente(self):
        dni_docente, ok = QInputDialog.getText(self, "Buscar Docente", "Ingrese el DNI del docente:")

        if ok and dni_docente:
            resultado = buscarDocente(dni_docente)
            if resultado:
                self.dni_docente_actual = resultado[3]

                id_docente, nombre, apellido, dni, telefono, email = resultado
                self.txtCodigo.setText(id_docente)
                self.txtNombre.setText(nombre)
                self.txtApellido.setText(apellido)
                self.txtDNI.setText(dni)
                self.txtTelefono.setText(telefono)
                self.txtEmail.setText(email)
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se encontró un docente con ese DNI.")
    
