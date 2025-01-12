import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from Vista.ventanaEstudiantes import VentanaAgregarEstudiantes
from Vista.ventanaMatricular import VentanaMatricularEstudiantes
from Vista.ventanaGestionPagos import VentanaGestionarPagos
from Vista.ventanaCalificaciones import VentanaAsignarCalificaciones
from Vista.ventanaVerDocentes import VentanaVerDocentes
from Vista.ventanaAdministrarUsuarios import VentanaAdministrarUsuarios
from Vista.ventanaReporteAlumnos import VentanaReporteAlumnos
from Vista.ventanaReporteCalificaciones import VentanaReporteCalificaciones
from Vista.ventanaReportePagos import VentanaReportePagos

class VentanaAdministrador(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaAdministrador, self).__init__(parent)
        uic.loadUi("UI/ventanaAdministrador.ui", self)
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
        self.menu_agregarEstudiantes.triggered.connect(self.opcionVerEstudiantes)
        self.menu_MatricularEstudiante.triggered.connect(self.opcionMatricularEstudiante)
        self.menu_GestionarPagos.triggered.connect(self.opcionGestionarPagos)
        self.menu_RegistrarCalificaciones.triggered.connect(self.opcionAsignarCalificaciones)
        self.menu_ListaDocentes.triggered.connect(self.opcionVerDocentes)
        self.menu_GenerarReporteAlumno.triggered.connect(self.opcionVerReportesAlumnos)
        self.menu_GenerarReporteCalificaciones.triggered.connect(self.opcionVerReportesCalificaciones)
        self.menu_GenerarReportePagos.triggered.connect(self.opcionVerReportesPagos)
        self.menu_AdministradorUsuarios.triggered.connect(self.opcionAdmnistrarUsuarios)
        self.menu_CerrarSesion.triggered.connect(self.opcionCerrarSesion)

    # ESTUDIANTES
    def opcionVerEstudiantes(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaEstudiantes = VentanaAgregarEstudiantes(rol_usuario = self.rol_usuario)
        self.ventanaEstudiantes.show()

    def opcionMatricularEstudiante(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaMatricular = VentanaMatricularEstudiantes(rol_usuario = self.rol_usuario)
        self.ventanaMatricular.show()

    def opcionGestionarPagos(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaGestionPagos = VentanaGestionarPagos(rol_usuario = self.rol_usuario)
        self.ventanaGestionPagos.show()            

    # GESTIÓN ACADÉMICA
    def opcionAsignarCalificaciones(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaCalificaciones = VentanaAsignarCalificaciones(rol_usuario = self.rol_usuario)
        self.ventanaCalificaciones.show()            
        pass

    def opcionVerDocentes(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaDocentes = VentanaVerDocentes(rol_usuario = self.rol_usuario)
        self.ventanaDocentes.show()

    # REPORTES
    def opcionVerReportesAlumnos(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaReporteAlumno = VentanaReporteAlumnos(rol_usuario = self.rol_usuario)
        self.ventanaReporteAlumno.show()

    def opcionVerReportesCalificaciones(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaReporteCalificacion = VentanaReporteCalificaciones(rol_usuario = self.rol_usuario)
        self.ventanaReporteCalificacion.show()

    def opcionVerReportesPagos(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaReportePago = VentanaReportePagos(rol_usuario = self.rol_usuario)
        self.ventanaReportePago.show()

    # CONFIGURACIÓN
    def opcionAdmnistrarUsuarios(self):
        self.close()
        self.rol_usuario = "Administrador"
        self.ventanaAdministrarUsuario = VentanaAdministrarUsuarios(rol_usuario = self.rol_usuario)
        self.ventanaAdministrarUsuario.show()
        

    def opcionCerrarSesion(self):
        from Vista.login import Login
        self.close()
        self.login = Login()
        self.login.show

    
    
        