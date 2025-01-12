import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from Modelo.carreras import mostrarCarreras
from Modelo.reporteAlumno import obtener_reporte_alumnos
from reportlab.pdfgen import canvas

class VentanaReporteAlumnos(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaReporteAlumnos, self).__init__(parent)
        uic.loadUi("UI/ventanaReportesAlumnos.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargar_carreras()
        self.actualirTabla()
        self.btnVolver.clicked.connect(self.botonVolver)
        self.btnGenerarReporte.clicked.connect(self.generar_reporte)
        self.btnPDF.clicked.connect(self.exportar_pdf)

    
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

    def cargar_carreras(self):
        carreras = mostrarCarreras()
        self.cmbCarrera.addItems(carreras)

    def actualirTabla(self):
        self.tblReporte.setColumnCount(4)
        self.tblReporte.setHorizontalHeaderLabels([
            "ID Alumno", "Nombre Completo", "Carrera", "Estado"
        ])

        reportes = obtener_reporte_alumnos(self.cmbCarrera.currentText())
        for reporte in reportes:
            row_position = self.tblReporte.rowCount()
            self.tblReporte.insertRow(row_position)
            for col, value in enumerate(reporte):
                self.tblReporte.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblReporte.horizontalHeader()
        for columna in range(self.tblReporte.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)

    def generar_reporte(self):
        carrera_selecionada = self.cmbCarrera.currentText()
        datos = obtener_reporte_alumnos(carrera_selecionada.lower())

        self.tblReporte.setRowCount(0)

        if not datos:
            QtWidgets.QMessageBox.warning(self, "Sin datos", "No hay alumnos registrados para esta carrera.")
            return

        self.tblReporte.setRowCount(0)  # Limpiar las filas existentes

        for fila, (id_alumno, nombre_completo, carrera, estado) in enumerate(datos):
            self.tblReporte.insertRow(fila)
            self.tblReporte.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(id_alumno)))
            self.tblReporte.setItem(fila, 1, QtWidgets.QTableWidgetItem(nombre_completo))
            self.tblReporte.setItem(fila, 2, QtWidgets.QTableWidgetItem(carrera))
            self.tblReporte.setItem(fila, 3, QtWidgets.QTableWidgetItem(estado))

        self.tblReporte.resizeRowsToContents()  # Ajustar el tamaño de las filas
   
    def exportar_pdf(self):
        # Exportar el contenido de la tabla a un archivo PDF
        filename = "reporte_alumnos.pdf"
        c = canvas.Canvas(filename)
        
        c.drawString(100, 800, "Reporte de Alumnos")
        c.drawString(50, 750, f"Carrera: {self.cmbCarrera.currentText()}")
        c.drawString(50, 730, "ID Alumno | Nombre | Carrera | Estado")

        y = 700
        for fila in range(self.tblReporte.rowCount()):
            texto_fila = " | ".join(
                self.tblReporte.item(fila, col).text() if self.tblReporte.item(fila, col) else ""
                for col in range(self.tblReporte.columnCount())
            )
            c.drawString(50, y, texto_fila)
            y -= 20

        c.save()
        QtWidgets.QMessageBox.information(self, "PDF Exportado", f"Reporte guardado como {filename}")
