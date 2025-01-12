import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from Vista.ventanaAdministrador import VentanaAdministrador
from Vista.ventanaPersonal import VentanaPersonal
from Vista.ventanaProfesor import VentanaProfesor
from Modelo.roles import obtenerRoles
from Modelo.credenciales import obtenerCredenciales

class Login(QMainWindow):

    def __init__(self, parent = None):
        super(Login, self).__init__(parent)
        uic.loadUi('UI/login.ui', self)
        self.show()
        # Zona de Eventos
        self.cargarRoles()
        self.btnIngresar.clicked.connect(self.ingresar)
        self.txtPassword.returnPressed.connect(self.ingresar)

    # Zona de Programación
    def cargarRoles(self):
        roles = obtenerRoles()
        if roles:
            self.cmbRol.addItems(roles)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron roles")

    def limpiarCampos(self):
        self.txtUsuario.clear()
        self.txtPassword.clear()

    def mostrarError(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)
        self.limpiarCampos()

    def ingresar(self):
        rol_seleccionado = self.cmbRol.currentIndex()
        usuario = self.txtUsuario.text()
        password = self.txtPassword.text()

        if not usuario or not password:
            self.mostrarError("No se permiten campos vacios")
            return
        
        credenciales = obtenerCredenciales()
        usuario_valido = None

        for nombre, contrasenia, idRol in credenciales:
            if nombre == usuario and contrasenia == password:
                usuario_valido = idRol
                break

        if usuario_valido is not None:
            if usuario_valido == rol_seleccionado + 1:
                self.close()
                self.rol_usuario = rol_seleccionado
                if rol_seleccionado == 0:
                    self.GUI = VentanaAdministrador(rol_usuario = self.rol_usuario)
                elif rol_seleccionado == 1:
                    self.GUI = VentanaPersonal(rol_usuario = self.rol_usuario)
                elif rol_seleccionado == 2:
                    self.GUI = VentanaProfesor(rol_usuario = self.rol_usuario)
                self.GUI.show()
            else:
                self.mostrarError("El rol no coincide con las credenciales del usuario.")
        else:
            self.mostrarError("Nombre de usuario o contraseña incorrectos")
