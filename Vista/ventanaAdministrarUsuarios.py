import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from Modelo.roles import obtenerRoles
from Modelo.usuarios import agregarUsuario, editarUsuario, eliminarUsuario, buscarUsuarioPorCodigo, obtenerUsuarios, obtenerIdRolPorNombre

class VentanaAdministrarUsuarios(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaAdministrarUsuarios, self).__init__(parent)
        uic.loadUi("UI/ventanaAdministrarUsuarios.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.id_usuario_actual = None
        self.cargarRoles()
        self.actualizarTabla()
        self.btnAgregar.clicked.connect(self.registrarUsuarios)
        self.btnEditar.clicked.connect(self.editarUsuario)
        self.btnEliminar.clicked.connect(self.eliminarUsuario)
        self.btnBuscar.clicked.connect(self.buscarUsuario)
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

    def cargarRoles(self):
        roles = obtenerRoles()
        if roles:
            self.cmbRol.addItems(roles)
        else:
            QMessageBox.warning(self, "Error", "No se encontraron roles")

    def limpiarCampos(self):
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtEmail.clear()
        self.cmbRol.setCurrentIndex(0)
        self.txtUsuario.clear()
        self.txtPassword.clear()

    def actualizarTabla(self):
        self.tblUsuarios.setColumnCount(7)
        self.tblUsuarios.setHorizontalHeaderLabels([
            "ID Usuario", "Nombre", "Apellido", "Email", "Rol", "Usuario", "Contraseña"
        ])
        self.tblUsuarios.setRowCount(0)

        usuarios = obtenerUsuarios()
        for usuario in usuarios:
            row_position = self.tblUsuarios.rowCount()
            self.tblUsuarios.insertRow(row_position)
            for col, value in enumerate(usuario):
                self.tblUsuarios.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblUsuarios.horizontalHeader()
        for columna in range(self.tblUsuarios.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
    
    def registrarUsuarios(self):
        nombre = self.txtNombre.text().strip()
        apellido = self.txtApellido.text().strip()
        email = self.txtEmail.text().strip()
        rol = self.cmbRol.currentText().strip()
        usuario = self.txtUsuario.text().strip()
        password = self.txtPassword.text().strip()

        if not all([nombre, apellido, email, rol, usuario, password]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return
        
        idRol = obtenerIdRolPorNombre(rol)
        if not idRol:
            QMessageBox.warning(self, "Error", "El rol seleccionado no es válido")
            return
            
        if agregarUsuario(nombre, apellido, usuario, password, email, idRol):
            QMessageBox.information(self, "Éxito", "Usuario agregado con éxito")
            self.actualizarTabla()
            self.limpiarCampos()
        else:
            QMessageBox.warning(self, "Error", "Error al agregar usuario")

    def editarUsuario(self):
        if not self.id_usuario_actual:  
            QMessageBox.warning(self, "Error", "Debe buscar un usuario antes de editar.")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar edición",
            "¿Desea guardar los cambios realizados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            nombre_actualizado = self.txtNombre.text().strip()
            apellido_actualizado = self.txtApellido.text().strip()
            email_actualizado = self.txtEmail.text().strip()
            rol_actualizado = self.cmbRol.currentText().strip()
            usuario_actualizado = self.txtUsuario.text().strip()
            password_actualizado = self.txtPassword.text().strip()

            if not all([nombre_actualizado, apellido_actualizado, email_actualizado,
                        rol_actualizado, usuario_actualizado]):
                QMessageBox.warning(self, "Error", "Por favor, complete todos los campos antes de guardar.")
                return

            idRol = obtenerIdRolPorNombre(rol_actualizado)
            if not idRol:
                QMessageBox.warning(self, "Error", "El rol seleccionado no es válido.")
                return

            exito = editarUsuario(
                self.id_usuario_actual,
                nombre_actualizado,
                apellido_actualizado,
                usuario_actualizado,
                password_actualizado,
                email_actualizado,
                idRol
            )

            if exito:
                QMessageBox.information(self, "Éxito", "Usuario editado con éxito.")
                self.actualizarTabla()
                self.limpiarCampos()
            else:
                QMessageBox.warning(self, "Error", "Error al editar usuario.")

    def eliminarUsuario(self):
        idUsuario, ok = QInputDialog.getText(self, "Eliminar Usuario", "Ingrese el ID del usuario:")
        
        if ok and idUsuario:
            resultado = buscarUsuarioPorCodigo(idUsuario)
            
            if resultado:

                idUsuario, nombre, apellido, nombre_usuario, contrasenia, email, rol = resultado
                self.txtNombre.setText(nombre)
                self.txtApellido.setText(apellido)
                self.txtUsuario.setText(nombre_usuario)
                self.txtPassword.setText(contrasenia)
                self.txtEmail.setText(email)
                self.cmbRol.setCurrentText(rol)

                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Desea eliminar al usuario con ID: {idUsuario}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                
                if respuesta == QMessageBox.Yes:
                    if eliminarUsuario(idUsuario):
                        QMessageBox.information(self, "Eliminación Exitosa", "El usuario se ha eliminado correctamente.")
                        self.actualizarTabla()
                        self.limpiarCampos()
                    else:
                        QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario. Verifique la información.")
            else:
                QMessageBox.warning(self, "Error", "No se encontró un usuario con ese ID.")

    def buscarUsuario(self):
        idUsuario, ok = QInputDialog.getText(self, "Buscar Usuario", "Ingrese el ID del usuario:")

        if ok and idUsuario.strip():
            resultado = buscarUsuarioPorCodigo(idUsuario.strip())

            if resultado:
                self.id_usuario_actual = resultado[0]
                self.txtNombre.setText(resultado[1])
                self.txtApellido.setText(resultado[2])
                self.txtUsuario.setText(resultado[3])
                self.txtPassword.setText("")
                self.txtEmail.setText(resultado[4])
                self.cmbRol.setCurrentText(resultado[5])

                QMessageBox.information(self, "Éxito", "Datos cargados correctamente. Ahora puede modificarlos y guardar los cambios.")
            else:
                QMessageBox.warning(self, "Error", "No se encontró un usuario con ese ID.")


