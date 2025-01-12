import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import QDate
from Modelo.alumnos import mostrarAlumnos
from Modelo.carreras import mostrarCarreras
from Modelo.docentes import mostrarDocentes
from Modelo.calificaciones import obtenerCalificaciones, agregarCalificacion, editarCalificacion, buscarCalificacion, eliminarCalificacion

class VentanaAsignarCalificaciones(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaAsignarCalificaciones, self).__init__(parent)
        uic.loadUi("UI/ventanaCalificaciones.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargarAlumnos()
        self.cargarCarreras()
        self.cargarDocentes()
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarCalificaciones)
        self.btnEditar.clicked.connect(self.editarCalificaciones)
        self.btnEliminar.clicked.connect(self.eliminarCalificaciones)
        self.btnBuscar.clicked.connect(self.buscarCalificaciones)
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

    def cargarDocentes(self):
        docentes = mostrarDocentes()
        if docentes:
            self.cmbDocente.addItems([f"{docente[0]} {docente[1]}" for docente in docentes])
        else:
            QMessageBox.warning(self, "Error", "No se encontraron docentes")

    def limpiarCampos(self):
        self.cmbAlumno.setCurrentIndex(0)
        self.cmbCarrera.setCurrentIndex(0)
        self.cmbDocente.setCurrentIndex(0)
        self.dsbNota.setValue(0)
        self.dteFechaCalificacion.setDate(QDate.currentDate())

    def actualizarTabla(self):
        self.tblCalificaciones.setColumnCount(6)
        self.tblCalificaciones.setHorizontalHeaderLabels([
            "ID Calificación", "Alumno", "Docente", "Carrera", "Nota", "Fecha Calificación"
        ])
        self.tblCalificaciones.setRowCount(0)

        calificaciones = obtenerCalificaciones()
        for calificacion in calificaciones:
            row_position = self.tblCalificaciones.rowCount()
            self.tblCalificaciones.insertRow(row_position)
            for col, value in enumerate(calificacion):
                self.tblCalificaciones.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblCalificaciones.horizontalHeader()
        for columna in range(self.tblCalificaciones.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

    def registrarCalificaciones(self):
        alumno = self.cmbAlumno.currentText()
        docente = self.cmbDocente.currentText()
        carrera = self.cmbCarrera.currentText()
        nota = self.dsbNota.value()
        fecha_calificacion = self.dteFechaCalificacion.date().toString("yyyy-MM-dd")

        if not all ([alumno, docente, carrera, nota, fecha_calificacion]):
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos")
            return

        if agregarCalificacion(alumno, docente, carrera, nota, fecha_calificacion):
            QMessageBox.information(self, "Exito", "Calificación registrada con éxito")
            self.limpiarCampos()
            self.actualizarTabla()
        else:
            QMessageBox.warning(self, "Error", "Error al registrar calificación")

    def editarCalificaciones(self):
        if hasattr(self, 'id_calificacion_actual'): 
            
            id_calificacion = self.id_calificacion_actual
            alumno = self.cmbAlumno.currentText()
            docente = self.cmbDocente.currentText()
            carrera = self.cmbCarrera.currentText()
            nota = self.dsbNota.value()
            fecha = self.dteFechaCalificacion.date().toString('yyyy-MM-dd')

            
            editarCalificacion(id_calificacion, alumno, docente, carrera, nota, fecha)
            self.limpiarCampos()
            QMessageBox.information(self, "Éxito", "Calificación editada correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna calificación para editar")

    def eliminarCalificaciones(self):
        id_calificacion, ok = QInputDialog.getText(
            self, "Eliminar Calificación", "Ingrese el ID de la calificación a eliminar: "
        )

        if ok and id_calificacion:
            resultado = buscarCalificacion(id_calificacion)
            if resultado:
                idCalificacion, nombreAlumno, nombreDocente, nombreCarrera, nota, fecha_Calificacion = resultado

                self.cmbAlumno.setCurrentText(nombreAlumno)
                self.cmbDocente.setCurrentText(nombreDocente)
                self.cmbCarrera.setCurrentText(nombreCarrera)
                self.dsbNota.setValue(nota)
                fechaCalificacion = QDate.fromString(fecha_Calificacion, 'yyyy-MM-dd')
                self.dteFechaCalificacion.setDate(fechaCalificacion)
                self.limpiarCampos()
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente")

                respuesta = QMessageBox.question(self, "Continua eliminación",
                                                 f"¿Estás seguro que deseas eliminar la calificación con ID: {idCalificacion}", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                if respuesta == QMessageBox.Yes:
                    if eliminarCalificacion(idCalificacion):
                        QMessageBox.information(self, "Éxito", "La calificación se eliminó con éxito")
                        self.actualizarTabla()
                        self.limpiarCampos()
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo eliminar la calificación")
            else:
                QMessageBox.warning(self, "Error", "No se encontró la calificación con el ID ingresado")


    def buscarCalificaciones(self):
        id_calificacion, ok = QInputDialog.getText(
            self, "Buscar Calificación", "Ingrese el ID de la calificación: "
        )

        if ok and id_calificacion:
            resultado = buscarCalificacion(id_calificacion)
            if resultado:
                self.id_calificacion_actual = resultado[0]

                idCalificacion, nombreAlumno, nombreDocente, nombreCarrera, nota, fecha_Calificacion = resultado

                self.cmbAlumno.setCurrentText(nombreAlumno)
                self.cmbDocente.setCurrentText(nombreDocente)
                self.cmbCarrera.setCurrentText(nombreCarrera)
                self.dsbNota.setValue(nota)
                fechaCalificacion = QDate.fromString(fecha_Calificacion, 'yyyy-MM-dd')
                self.dteFechaCalificacion.setDate(fechaCalificacion)
                QMessageBox.information(self, "Éxito", "Datos cargados correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se encontró la calificación")