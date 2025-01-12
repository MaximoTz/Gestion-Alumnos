import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from Modelo.carreras import mostrarCarreras
from Modelo.estado import mostrarEstado 
from Modelo.alumnos import obtenerAlumnos, registrarAlumno, verificarAlumnoExistente, eliminarAlumno, buscarAlumno, editarAlumno

class VentanaAgregarEstudiantes(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaAgregarEstudiantes, self).__init__(parent)
        uic.loadUi("UI/ventanaEstudiantes.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargarCarreras()
        self.cargarEstado()
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarEstudiante)
        self.btnEditar.clicked.connect(self.editarEstudiante)
        self.btnEliminar.clicked.connect(self.eliminarEstudiante)
        self.btnBuscar.clicked.connect(self.buscarEstudiante)
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


    def cargarCarreras(self):
        carreras = mostrarCarreras()
        if carreras:
            self.cmbCarrera.addItems(carreras)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron carreras")

    def cargarEstado(self):
        estado = mostrarEstado()
        if estado:
            self.cmbEstado.addItems(estado)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron estados")

    def limpiarCampos(self):
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtDNI.clear()
        self.txtTelefono.clear()
        self.txtEmail.clear()
        self.cmbCarrera.setCurrentIndex(0)
        self.cmbEstado.setCurrentIndex(0)

    def actualizarTabla(self):
        self.tblEstudiantes.setColumnCount(8)
        self.tblEstudiantes.setHorizontalHeaderLabels([
            "ID Alumno", "Nombre", "Apellido", "DNI", 
            "Teléfono", "Email", "Carrera", "Estado"
        ])

        self.tblEstudiantes.setRowCount(0)

        alumnos = obtenerAlumnos()
        for alumno in alumnos:
            row_position = self.tblEstudiantes.rowCount()
            self.tblEstudiantes.insertRow(row_position)
            for col, value in enumerate(alumno):
                self.tblEstudiantes.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblEstudiantes.horizontalHeader()
        for columna in range(self.tblEstudiantes.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

    def registrarEstudiante(self):
        codigo = self.txtCodigo.text()
        nombre = self.txtNombre.text()
        apellido = self.txtApellido.text()
        dni = self.txtDNI.text()
        email = self.txtEmail.text()
        telefono = self.txtTelefono.text()
        carrera = self.cmbCarrera.currentText()
        estado = self.cmbEstado.currentText()

        if not all ([codigo, nombre, apellido, dni, telefono, email, carrera, estado]):
            QMessageBox.warning(self, "Campos incompletos", "Todos los campos son obligatorios")
            return
        
        if verificarAlumnoExistente(codigo, dni, email):
            QMessageBox.warning(self, "Alumno existente", "Ya existe un alumno registrado con los mismos datos")
            self.limpiarCampos()
            return

        if registrarAlumno(codigo, nombre, apellido, dni, telefono, email, carrera, estado):
            QMessageBox.information(self, "Registro exitoso", "El estudiante se ha registrado con éxito")
            self.actualizarTabla()
            self.limpiarCampos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo registrar el estudiante")

    def editarEstudiante(self):
        respuesta = QMessageBox.question(
            self, "Confirmar edición",
            "¿Desea guardar los cambios realizados?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            nombre_actualizado = self.txtNombre.text()
            apellido_actualizado = self.txtApellido.text()
            dni_actualizado = self.txtDNI.text()
            telefono_actualizado = self.txtTelefono.text()
            email_actualizado = self.txtEmail.text()
            carrera_actualizada = self.cmbCarrera.currentText()
            estado_actualizado = self.cmbEstado.currentText()

            if not all([nombre_actualizado, apellido_actualizado, dni_actualizado, telefono_actualizado, email_actualizado]):
                QMessageBox.warning(self, "Error", "Por favor, complete todos los campos antes de guardar.")
                return
        else:
            return
            
        if editarAlumno(
            self.dni_alumno_actual, 
            nombre_actualizado, 
            apellido_actualizado,
            dni_actualizado, 
            telefono_actualizado, 
            email_actualizado,
            carrera_actualizada, 
            estado_actualizado
        ):
            QMessageBox.information(self, "Éxito", "Los datos se han actualizado correctamente.")
            self.actualizarTabla()
            self.limpiarCampos()
            del self.dni_alumno_actual
        else:
            QMessageBox.warning(self, "Error", "No se pudieron guardar los cambios. Verifique los datos.")

    def eliminarEstudiante(self):
        dni_alumno, ok = QInputDialog.getText(
            self, "Eliminar Alumno", "Ingrese el DNI del alumno:"
        )

        if ok and dni_alumno:
            resultado = buscarAlumno(dni_alumno)
            if resultado:
                
                id_alumno, nombre, apellido, dni, telefono, email, carrera, estado = resultado
                self.txtCodigo.setText(id_alumno)
                self.txtNombre.setText(nombre)
                self.txtApellido.setText(apellido)
                self.txtDNI.setText(dni)
                self.txtTelefono.setText(telefono)
                self.txtEmail.setText(email)
                self.cmbCarrera.setCurrentText(carrera)
                self.cmbEstado.setCurrentText(estado)
            
                respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                         f"¿Estás seguro que deseas eliminar el alumno con DNI: {dni_alumno}",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
                if respuesta == QMessageBox.Yes:
                    if eliminarAlumno(dni):
                        QMessageBox.information(self, "Eliminación exitosa", "El estudiante se ha elimininado.")
                        self.actualizarTabla()
                        self.limpiarCampos()
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo eliminar al alumno.")
                else:
                    self.limpiarCampos()
            else:
                QMessageBox.warning(self, "Error", "No se encontró un alumno con ese DNI.")

    def buscarEstudiante(self):
        dni_alumno, ok = QInputDialog.getText(
            self, "Buscar Alumno", "Ingrese el DNI del alumno:"
        )

        if ok and dni_alumno:
            resultado = buscarAlumno(dni_alumno)
            if resultado:
                self.dni_alumno_actual = resultado[3]
                
                id_alumno, nombre, apellido, dni, telefono, email, carrera, estado = resultado
                self.txtCodigo.setText(id_alumno)
                self.txtNombre.setText(nombre)
                self.txtApellido.setText(apellido)
                self.txtDNI.setText(dni)
                self.txtTelefono.setText(telefono)
                self.txtEmail.setText(email)
                self.cmbCarrera.setCurrentText(carrera)
                self.cmbEstado.setCurrentText(estado)
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se encontró un alumno con ese DNI.")