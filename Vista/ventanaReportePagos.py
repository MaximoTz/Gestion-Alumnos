import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from Modelo.reportePagos import obtener_reporte_pagos
from Modelo.estado import mostrarEstado
from reportlab.pdfgen import canvas

class VentanaReportePagos(QMainWindow):
    def __init__(self, rol_usuario, parent = None):
        super(VentanaReportePagos, self).__init__(parent)
        uic.loadUi("UI/ventanaReportesPagos.ui", self)
        self.show()

        self.rol_usuario = rol_usuario
        self.cargar_Estado()
        self.actualizarTabla()
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

    def cargar_Estado(self):
        estado = mostrarEstado()
        self.cmbEstado.addItems(estado)

    def actualizarTabla(self):
        self.tblReporte.setColumnCount(4)
        self.tblReporte.setHorizontalHeaderLabels([
            "ID Boleta", "Nombre Completo", "Estado", "Monto Pagado"
        ])

        estado_selecionado = self.cmbEstado.currentText()
        reportes = obtener_reporte_pagos(estado_selecionado.lower())
        for reporte in reportes:
            row_position = self.tblReporte.rowCount()
            self.tblReporte.insertRow(row_position)
            for col, value in enumerate(reporte):
                self.tblReporte.setItem(row_position, col, QTableWidgetItem(str(value)))

        encabezado = self.tblReporte.horizontalHeader()
        for columna in range(self.tblReporte.columnCount()):
            encabezado.setSectionResizeMode(columna, QtWidgets.QHeaderView.Stretch)
        
    def generar_reporte(self):
        estado_selecionado = self.cmbEstado.currentText()
        datos = obtener_reporte_pagos(estado_selecionado.lower())

        self.tblReporte.setRowCount(0)

        if not datos:
            QtWidgets.QMessageBox.warning(self, "Sin datos", "No hay pagos registrados para este estado.")
            return

        for fila, (id_boleta, nombre_completo, estado, monto) in enumerate(datos):
            self.tblReporte.insertRow(fila)
            self.tblReporte.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(id_boleta)))
            self.tblReporte.setItem(fila, 1, QtWidgets.QTableWidgetItem(nombre_completo))
            self.tblReporte.setItem(fila, 2, QtWidgets.QTableWidgetItem(estado))
            self.tblReporte.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(monto)))

        self.tblReporte.resizeRowsToContents()

    def exportar_pdf(self):
        filename = "reporte_pagos.pdf"
        c = canvas.Canvas(filename)

        c.drawString(100, 800, "Reporte de Pagos")
        c.drawString(50, 750, f"Estado: {self.cmbEstado.currentText()}")
        c.drawString(50, 730, "ID Boleta | Nombre | Estado | Monto Pagado")

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

    