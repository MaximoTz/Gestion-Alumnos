import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QTableWidgetItem
from PyQt5.QtCore import QDate
from Modelo.alumnos import mostrarAlumnos
from Modelo.carreras import mostrarCarreras
from Modelo.estado import mostrarEstado
from Modelo.matricula import registrarMatricula, editarMatricula, eliminarMatricula, buscarMatricula, obtenerMatricula

class VentanaMatricularEstudiantes(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaMatricularEstudiantes, self).__init__(parent)
        uic.loadUi("UI/ventanaMatricularEstudiantes.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargarCarreras()
        self.cargarEstado()
        self.cargarAlumnos()
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarMatricula)
        self.btnEditar.clicked.connect(self.editarMatricula)
        self.btnEliminar.clicked.connect(self.eliminarMatricula)
        self.btnBuscar.clicked.connect(self.buscarMatricula)
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

    def actualizarTabla(self):
        self.tblMatriculados.setColumnCount(5)
        self.tblMatriculados.setHorizontalHeaderLabels([
            "ID Matricula", "Alumno", "Carrera", "Fecha Matricula",
            "Estado"
        ])

        self.tblMatriculados.setRowCount(0)

        matriculas = obtenerMatricula()
        for matricula in matriculas:
            row_position = self.tblMatriculados.rowCount()
            self.tblMatriculados.insertRow(row_position)
            for col, value in enumerate(matricula):
                self.tblMatriculados.setItem(row_position, col, QTableWidgetItem(str(value)))

        header = self.tblMatriculados.horizontalHeader()
        for i in range(self.tblMatriculados.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def registrarMatricula(self):
        alumno = self.cmbAlumno.currentText()
        carrera = self.cmbCarrera.currentText()
        fecha_matricula = self.dteMatricula.date().toString("yyyy-MM-dd")
        estado = self.cmbEstado.currentText()

        if not all ([alumno, carrera, fecha_matricula, estado]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
              
        if registrarMatricula(alumno, carrera, fecha_matricula, estado):
            QMessageBox.information(self, "Éxito", "Matricula registrada con éxito")
            self.actualizarTabla()
        else:
            QMessageBox.warning(self, "Error", "Error al registrar matricula")

    def editarMatricula(self):
        if not hasattr(self, 'id_matricula_actual') or self.id_matricula_actual is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar una matrícula para editar.")
            return
        
        respuesta = QMessageBox.question(
            self, "Confirmar edición",
            "¿Desea guardar los cambios realizados?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            alumno_actualizado = self.cmbAlumno.currentText()
            carrera_actualizado = self.cmbCarrera.currentText()
            fecha_matricula_actualizado = self.dteMatricula.date().toString('yyyy-MM-dd') 
            estado_actualizado = self.cmbEstado.currentText()

            if editarMatricula(
                self.id_matricula_actual,
                alumno_actualizado,
                carrera_actualizado,
                fecha_matricula_actualizado,
                estado_actualizado
            ):
                QMessageBox.information(self, "Éxito", "Los datos se han actualizado correctamente.")
                self.actualizarTabla()
                self.id_matricula_actual = None  # Restablecer el ID
            else:
                QMessageBox.warning(self, "Error", "No se pudieron guardar los cambios. Verifique los datos.")
        else:
            QMessageBox.warning(self, "Error")
            return

    def eliminarMatricula(self):
        id_matricula, ok = QInputDialog.getText(
            self, "Eliminar Matricula", "Ingrese el ID de la matricula a eliminar: "
        )

        if ok and id_matricula:
            resultado = buscarMatricula(id_matricula)
            if resultado:
                idMatricula, nombreAlumno, nombreCarrera, fecha_matricula, estado = resultado
                self.cmbAlumno.setCurrentText(nombreAlumno)
                self.cmbCarrera.setCurrentText(nombreCarrera)
                fechaMatricula = QDate.fromString(fecha_matricula, 'yyyy-MM-dd')
                self.dteMatricula.setDate(fechaMatricula)
                self.cmbEstado.setCurrentText(estado)

                respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                                f"¿Estás seguro que deseas eliminar la matricula con ID: {idMatricula}?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                if respuesta == QMessageBox.Yes:
                    if eliminarMatricula(idMatricula):
                        QMessageBox.information(self, "Éxito", "La matricula se eliminó con éxito")
                        self.actualizarTabla()
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo eliminar la matricula")
            else:
                QMessageBox.warning(self, "Error", "No se encontraron matriculas")

    def buscarMatricula(self):
        id_matricula, ok = QInputDialog.getText(
            self, "Buscar Matricula", "Ingrese el ID de la matricula: "
        )

        if ok and id_matricula:
            resultado = buscarMatricula(id_matricula)
            if resultado:
                self.id_matricula_actual = resultado[0]

                idMatricula, nombreAlumno, nombreCarrera, fecha_matricula, estado = resultado
                self.cmbAlumno.setCurrentText(nombreAlumno)
                self.cmbCarrera.setCurrentText(nombreCarrera)
                fechaMatricula = QDate.fromString(fecha_matricula, 'yyyy-MM-dd')
                self.dteMatricula.setDate(fechaMatricula)
                self.cmbEstado.setCurrentText(estado)
                
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se encontraron matriculas")