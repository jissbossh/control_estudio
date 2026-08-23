from pathlib import Path
import sys
import json
import pandas as pd

from datetime import datetime, date, time

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QFont, QIcon

# ============================================================
# CARGAR CONFIGURACIONES POR DEFECTO
# ============================================================


def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


config = leer_json("config.json")

# FUENTE_APLICACION = "Segoe UI"
FUENTE_APLICACION = config["FUENTE_APLICACION"]

# TAMANO_FUENTE = 12
TAMANO_FUENTE = int(config["TAMANO_FUENTE"])

TEMA = config["TEMA"]

# ========================================================
# TEMA CLARO
# ========================================================


def aplicar_tema_claro(self):

    self.setStyleSheet(f"""
            QWidget {{
                font-family: "{FUENTE_APLICACION}";
                font-size: {TAMANO_FUENTE}pt;
                color: #212529;
            }}

            QMainWindow,
            QDialog {{
                background-color: #f5f7fa;
            }}

            QLabel {{
                color: #212529;
            }}

            QLineEdit,
            QComboBox,
            QDateTimeEdit,
            QDoubleSpinBox {{
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: white;
                color: #212529;
            }}

            QPushButton {{
                padding: 7px 14px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                background-color: white;
                color: #212529;
            }}

            QPushButton:hover {{
                background-color: #e9ecef;
            }}

            QTableWidget {{
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                color: #212529;
                selection-background-color: #cfe2ff;
                selection-color: #000000;
            }}

            QHeaderView::section {{
                background-color: #212529;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }}

            QComboBox QAbstractItemView {{
                background-color: white;
                color: #212529;
                selection-background-color: #cfe2ff;
            }}

            QDialogButtonBox QPushButton {{
                min-width: 90px;
            }}
            """)


# ========================================================
# TEMA OSCURO
# ========================================================


def aplicar_tema_oscuro(self):

    self.setStyleSheet(f"""
            QWidget {{
                font-family: "{FUENTE_APLICACION}";
                font-size: {TAMANO_FUENTE}pt;
                background-color: #121212;
                color: #eeeeee;
            }}

            QMainWindow,
            QDialog {{
                background-color: #121212;
            }}

            QLabel {{
                color: #eeeeee;
            }}

            QLineEdit,
            QComboBox,
            QDateTimeEdit,
            QDoubleSpinBox {{
                padding: 6px;
                border: 1px solid #444444;
                border-radius: 5px;
                background-color: #1e1e1e;
                color: #eeeeee;
            }}

            QPushButton {{
                padding: 7px 14px;
                border: 1px solid #444444;
                border-radius: 5px;
                background-color: #242424;
                color: #eeeeee;
            }}

            QPushButton:hover {{
                background-color: #333333;
            }}

            QTableWidget {{
                background-color: #1e1e1e;
                alternate-background-color: #252525;
                gridline-color: #3a3a3a;
                color: #eeeeee;
                selection-background-color: #264f78;
                selection-color: white;
            }}

            QHeaderView::section {{
                background-color: #000000;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }}

            QComboBox QAbstractItemView {{
                background-color: #1e1e1e;
                color: white;
                selection-background-color: #264f78;
            }}

            QScrollBar:vertical {{
                background: #1e1e1e;
                width: 12px;
            }}

            QScrollBar::handle:vertical {{
                background: #555555;
                border-radius: 5px;
            }}

            QDialogButtonBox QPushButton {{
                min-width: 90px;
            }}

            QMessageBox {{
                background-color: #1e1e1e;
                color: #eeeeee;
            }}

            QMessageBox QLabel {{
                color: #eeeeee;
            }}

            QMessageBox QPushButton {{
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
            }}

            QMessageBox QPushButton:hover {{
                background-color: #444444;
            }}

            QTableWidget {{
            background-color: #1e1e1e;
            color: white;
            gridline-color: #333333;
            }}

            QHeaderView::section {{
            background-color: #000000;
            color: white;
            padding: 5px;
            border: 1px solid #333333;
            }}

            QTableCornerButton::section {{
            background-color: #000000;
            border: 1px solid #333333;
            }}
            """)


# ============================================================
# SELECCIONAR HOJA
# ============================================================


class VentanaSeleccionHoja(QDialog):

    def __init__(self, hojas, parent=None):

        super().__init__(parent)

        self.hoja_seleccionada = None

        # ----------------------------------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # ----------------------------------------------------

        self.setWindowTitle("Seleccionar hoja")

        self.setFixedSize(400, 300)

        if TEMA == "CLARO":
            aplicar_tema_claro(self)
        else:
            aplicar_tema_oscuro(self)

        ruta_icono = Path(__file__).resolve().parent / "icono.png"

        if ruta_icono.exists():

            self.setWindowIcon(QIcon(str(ruta_icono)))
        # ----------------------------------------------------
        # LAYOUT
        # ----------------------------------------------------

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(10)

        # ----------------------------------------------------
        # TEXTO
        # ----------------------------------------------------

        etiqueta = QLabel("Selecciona la hoja que quieres convertir:")

        # etiqueta.setStyleSheet("""
        #     QLabel {
        #         font-size: 11px;
        #     }
        #     """)

        layout.addWidget(etiqueta)

        # ----------------------------------------------------
        # LISTA
        # ----------------------------------------------------

        self.lista_hojas = QListWidget()

        self.lista_hojas.addItems(hojas)

        # Permitir seleccionar una sola hoja
        self.lista_hojas.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        layout.addWidget(self.lista_hojas)

        # ----------------------------------------------------
        # BOTÓN
        # ----------------------------------------------------

        boton = QPushButton("Seleccionar hoja")

        boton.setFixedHeight(50)

        boton.clicked.connect(self.seleccionar)

        layout.addWidget(boton)

        # ----------------------------------------------------
        # DOBLE CLICK
        # ----------------------------------------------------

        self.lista_hojas.itemDoubleClicked.connect(self.seleccionar)

        self.setLayout(layout)

    # ========================================================
    # SELECCIONAR
    # ========================================================

    def seleccionar(self):

        item = self.lista_hojas.currentItem()

        if item is None:

            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una hoja.")

            return

        self.hoja_seleccionada = item.text()

        self.accept()


# ============================================================
# CONVERTIR VALOR
# ============================================================


def convertir_valor(valor):

    # --------------------------------------------------------
    # Fechas y horas
    # --------------------------------------------------------

    if isinstance(valor, (datetime, date, time)):

        return valor.isoformat()

    # --------------------------------------------------------
    # Timestamp de pandas
    # --------------------------------------------------------

    if isinstance(valor, pd.Timestamp):

        return valor.isoformat()

    # --------------------------------------------------------
    # Valores vacíos
    # --------------------------------------------------------

    if pd.isna(valor):

        return None

    # --------------------------------------------------------
    # Tipos numéricos de pandas
    # --------------------------------------------------------

    if hasattr(valor, "item"):

        try:

            return valor.item()

        except Exception:

            pass

    return valor


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================


def main():

    # ========================================================
    # CREAR APLICACIÓN
    # ========================================================

    app = QApplication.instance()

    if app is None:

        app = QApplication(sys.argv)

    # ========================================================
    # VENTANA PADRE
    # ========================================================

    ventana = QWidget()

    ventana.hide()

    # ========================================================
    # SELECCIONAR ARCHIVO EXCEL
    # ========================================================

    archivo_excel, _ = QFileDialog.getOpenFileName(
        ventana,
        "Selecciona el archivo Excel",
        "",
        "Archivos Excel (*.xlsx *.xls);;" "Todos los archivos (*)",
    )

    if not archivo_excel:

        print("No seleccionaste ningún archivo.")

        return

    # ========================================================
    # OBTENER HOJAS
    # ========================================================

    try:

        excel = pd.ExcelFile(archivo_excel)

        hojas = excel.sheet_names

    except Exception as e:

        QMessageBox.critical(
            ventana, "Error", "No se pudo leer el archivo Excel:\n\n" f"{e}"
        )

        return

    # ========================================================
    # COMPROBAR QUE HAYA HOJAS
    # ========================================================

    if not hojas:

        QMessageBox.warning(ventana, "Sin hojas", "El archivo Excel no contiene hojas.")

        return

    # ========================================================
    # VENTANA PARA SELECCIONAR HOJA
    # ========================================================

    dialogo = VentanaSeleccionHoja(hojas, ventana)

    # --------------------------------------------------------
    # Hacer que el diálogo sea modal
    # --------------------------------------------------------

    dialogo.setWindowModality(Qt.WindowModality.ApplicationModal)

    resultado_dialogo = dialogo.exec()

    # ========================================================
    # COMPROBAR SELECCIÓN
    # ========================================================

    if resultado_dialogo != QDialog.DialogCode.Accepted:

        print("No seleccionaste ninguna hoja.")

        return

    hoja_seleccionada = dialogo.hoja_seleccionada

    if not hoja_seleccionada:

        print("No seleccionaste ninguna hoja.")

        return

    print(f"Hoja seleccionada: " f"{hoja_seleccionada}")

    # ========================================================
    # LEER EXCEL
    # ========================================================

    try:

        df = pd.read_excel(archivo_excel, sheet_name=hoja_seleccionada)

    except Exception as e:

        QMessageBox.critical(ventana, "Error", "No se pudo leer la hoja:\n\n" f"{e}")

        return

    # ========================================================
    # RELLENAR CELDAS COMBINADAS
    # ========================================================

    df = df.ffill()

    # ========================================================
    # CONVERTIR VALORES
    # ========================================================

    df = df.map(convertir_valor)

    # ========================================================
    # DATAFRAME A REGISTROS
    # ========================================================

    datos = df.to_dict(orient="records")

    # ========================================================
    # SELECCIONAR DÓNDE GUARDAR
    # ========================================================

    archivo_json, _ = QFileDialog.getSaveFileName(
        ventana,
        "Guardar archivo JSON",
        f"{hoja_seleccionada}.json",
        "Archivos JSON (*.json);;" "Todos los archivos (*)",
    )

    if not archivo_json:

        print("No seleccionaste dónde guardar " "el archivo.")

        return

    # ========================================================
    # ASEGURAR EXTENSIÓN .JSON
    # ========================================================

    if not archivo_json.lower().endswith(".json"):

        archivo_json += ".json"

    # ========================================================
    # GUARDAR JSON
    # ========================================================

    try:

        with open(archivo_json, "w", encoding="utf-8") as archivo:

            json.dump(datos, archivo, ensure_ascii=False, indent=4)

    except Exception as e:

        QMessageBox.critical(ventana, "Error", "No se pudo crear el JSON:\n\n" f"{e}")

        return

    # ========================================================
    # MENSAJE FINAL
    # ========================================================

    QMessageBox.information(
        ventana,
        "Proceso completado",
        "La hoja:\n"
        f"'{hoja_seleccionada}'\n\n"
        "fue convertida correctamente.\n\n"
        "Archivo generado:\n"
        f"{archivo_json}",
    )

    print("Conversión realizada correctamente.")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    main()
