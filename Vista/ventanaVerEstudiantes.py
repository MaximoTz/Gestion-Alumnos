import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from Modelo.alumnos import obtenerAlumnos

class VentanaVerEstudiantes(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaVerEstudiantes, self).__init__(parent)
        uic.loadUi("UI/ventanaListaEstudiantes.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.actualizarTabla()
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