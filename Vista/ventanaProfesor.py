import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from Vista.ventanaVerEstudiantes import VentanaVerEstudiantes
from Vista.ventanaCalificaciones import VentanaAsignarCalificaciones
from Vista.ventanaReporteAlumnos import VentanaReporteAlumnos
from Vista.ventanaReporteCalificaciones import VentanaReporteCalificaciones


class VentanaProfesor(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaProfesor, self).__init__(parent)
        uic.loadUi("UI/ventanaProfesor.ui", self)
        self.show()

        menu_bar = self.menuBar()

        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0; /* Color de fondo */
                font-size: 14px; /* Tamaño de fuente */
            }
            QMenuBar::item {
                padding: 10px 15px; /* Espaciado entre elementos */
            }
            QMenuBar::item:selected {
                background-color: rgb(218, 13, 58); /* Color al seleccionar */
                color: white;
            }
        """)
        self.rol_usuario = rol_usuario
        self.menu_VerListaAlumnos.triggered.connect(self.opcionVerEstudiantes)
        self.menu_RegistrarCalificaciones.triggered.connect(self.opcionAsignarCalificaciones)
        self.menu_GenerarReporteAlumno.triggered.connect(self.opcionVerReportesAlumnos)
        self.menu_GenerarReporteCalificaciones.triggered.connect(self.opcionVerReportesCalificaciones)
        self.menu_CerrarSesion.triggered.connect(self.cerrarSesion)
        
    # ESTUDIANTES
    def opcionVerEstudiantes(self):
        self.close()
        self.rol_usuario = "Profesor"
        self.ventanaEstudiantes = VentanaVerEstudiantes(rol_usuario = self.rol_usuario)
        self.ventanaEstudiantes.show()

    # GESTIÓN ACADÉMICA
    def opcionAsignarCalificaciones(self):
        self.close()
        self.rol_usuario = "Profesor"
        self.ventanaCalificaciones = VentanaAsignarCalificaciones(rol_usuario = self.rol_usuario)
        self.ventanaCalificaciones.show()

    # REPORTES
    def opcionVerReportesAlumnos(self):
        self.close()
        self.rol_usuario = "Profesor"
        self.ventanaReporteAlumno = VentanaReporteAlumnos(rol_usuario = self.rol_usuario)
        self.ventanaReporteAlumno.show()

    def opcionVerReportesCalificaciones(self):
        self.close()
        self.rol_usuario = "Profesor"
        self.ventanaReporteCalificacion = VentanaReporteCalificaciones(rol_usuario = self.rol_usuario)
        self.ventanaReporteCalificacion.show()

    # CONFIGURACIÓN
    def cerrarSesion(self):
        from Vista.login import Login
        self.close()
        self.login = Login()
        self.login.show()