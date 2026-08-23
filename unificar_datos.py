import json

import os

from pathlib import Path

import sys

import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
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
# ============================================================
# SELECCIONAR CARPETA
# ============================================================


def seleccionar_carpeta():

    carpeta = QFileDialog.getExistingDirectory(
        ventana,
        "Selecciona la carpeta que contiene los archivos Excel",
    )

    if carpeta:

        entrada_ruta.setText(carpeta)


# ============================================================
# UNIFICAR EXCEL
# ============================================================


def unificar_excel():

    carpeta = entrada_ruta.text().strip()

    # --------------------------------------------------------
    # COMPROBAR CARPETA
    # --------------------------------------------------------

    if not carpeta:

        QMessageBox.warning(
            ventana,
            "Falta la carpeta",
            "Selecciona una carpeta primero.",
        )

        return

    if not os.path.isdir(carpeta):

        QMessageBox.critical(
            ventana,
            "Error",
            "La carpeta seleccionada no existe.",
        )

        return

    # --------------------------------------------------------
    # BUSCAR ARCHIVOS EXCEL
    # --------------------------------------------------------

    archivos_excel = [
        archivo
        for archivo in os.listdir(carpeta)
        if archivo.lower().endswith((".xlsx", ".xls"))
    ]

    # --------------------------------------------------------
    # EVITAR LEER EL ARCHIVO GENERADO
    # --------------------------------------------------------

    archivos_excel = [
        archivo
        for archivo in archivos_excel
        if archivo.lower() != "datos_unificados.xlsx"
    ]

    # --------------------------------------------------------
    # COMPROBAR ARCHIVOS
    # --------------------------------------------------------

    if not archivos_excel:

        QMessageBox.information(
            ventana,
            "Sin archivos",
            "No se encontraron archivos Excel " "en la carpeta seleccionada.",
        )

        return

    datos = []
    errores = []

    # --------------------------------------------------------
    # LEER CADA ARCHIVO
    # --------------------------------------------------------

    for archivo in archivos_excel:

        ruta_archivo = os.path.join(
            carpeta,
            archivo,
        )

        try:

            df = pd.read_excel(ruta_archivo)

            datos.append(df)

        except Exception as e:

            errores.append(f"{archivo}: {str(e)}")

    # --------------------------------------------------------
    # COMPROBAR DATOS
    # --------------------------------------------------------

    if not datos:

        QMessageBox.critical(
            ventana,
            "Error",
            "No se pudo leer ningún archivo Excel.",
        )

        return

    # --------------------------------------------------------
    # UNIFICAR
    # --------------------------------------------------------

    resultado = pd.concat(
        datos,
        ignore_index=True,
    )

    # --------------------------------------------------------
    # RUTA DE SALIDA
    # --------------------------------------------------------

    ruta_salida = os.path.join(
        carpeta,
        "datos_unificados.xlsx",
    )

    # --------------------------------------------------------
    # GUARDAR
    # --------------------------------------------------------

    try:

        resultado.to_excel(
            ruta_salida,
            index=False,
        )

    except Exception as e:

        QMessageBox.critical(
            ventana,
            "Error al guardar",
            "No se pudo guardar el archivo:\n\n" f"{e}",
        )

        return

    # --------------------------------------------------------
    # MENSAJE FINAL
    # --------------------------------------------------------

    mensaje = (
        "Proceso terminado correctamente.\n\n"
        f"Archivos encontrados: "
        f"{len(archivos_excel)}\n"
        f"Archivos procesados: "
        f"{len(datos)}\n"
        f"Filas unificadas: "
        f"{len(resultado):,}\n\n"
        "Archivo generado:\n"
        f"{ruta_salida}"
    )

    # --------------------------------------------------------
    # ERRORES
    # --------------------------------------------------------

    if errores:

        mensaje += f"\n\nArchivos con errores: " f"{len(errores)}\n\n" + "\n".join(
            errores
        )

    QMessageBox.information(
        ventana,
        "Proceso terminado",
        mensaje,
    )


# ============================================================
# APLICACIÓN
# ============================================================

app = QApplication(sys.argv)

# ========================================================
# TEMA CLARO
# ========================================================


def aplicar_tema_claro():

    ventana.setStyleSheet(f"""
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


def aplicar_tema_oscuro():

    ventana.setStyleSheet(f"""
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
# VENTANA PRINCIPAL
# ============================================================

ventana = QWidget()

ventana.setWindowTitle("Unificar archivos Excel")

ventana.setFixedSize(
    650,
    220,
)

if TEMA == "CLARO":
    aplicar_tema_claro()
else:
    aplicar_tema_oscuro()

ruta_icono = Path(__file__).resolve().parent / "icono.png"

if ruta_icono.exists():

    ventana.setWindowIcon(QIcon(str(ruta_icono)))


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

layout_principal = QVBoxLayout()

layout_principal.setContentsMargins(
    20,
    15,
    20,
    15,
)

layout_principal.setSpacing(10)


# ============================================================
# TÍTULO
# ============================================================

titulo = QLabel("Unificar archivos Excel")

titulo.setStyleSheet("""
    QLabel {
        font-size: 18px;
        font-weight: bold;
    }
    """)

titulo.setAlignment(Qt.AlignCenter)

layout_principal.addWidget(titulo)


# ============================================================
# FILA DE CARPETA
# ============================================================

layout_ruta = QHBoxLayout()

layout_ruta.setSpacing(10)


# ------------------------------------------------------------
# ETIQUETA
# ------------------------------------------------------------

etiqueta = QLabel("Carpeta:")

# etiqueta.setStyleSheet("""
#     QLabel {
#         font-size: 14px;
#     }
#     """)

layout_ruta.addWidget(etiqueta)


# ------------------------------------------------------------
# CAMPO DE RUTA
# ------------------------------------------------------------

entrada_ruta = QLineEdit()

entrada_ruta.setPlaceholderText("Selecciona una carpeta...")

entrada_ruta.setMinimumHeight(30)

layout_ruta.addWidget(
    entrada_ruta,
    1,
)


# ------------------------------------------------------------
# BOTÓN EXAMINAR
# ------------------------------------------------------------

boton_examinar = QPushButton("Examinar...")

boton_examinar.setFixedWidth(140)

boton_examinar.setMinimumHeight(30)

boton_examinar.clicked.connect(seleccionar_carpeta)

layout_ruta.addWidget(boton_examinar)


layout_principal.addLayout(layout_ruta)


# ============================================================
# BOTÓN UNIFICAR
# ============================================================

boton_unificar = QPushButton("UNIFICAR ARCHIVOS EXCEL")

boton_unificar.setMinimumHeight(45)

boton_unificar.setStyleSheet("""
    QPushButton {
        background-color: #1976D2;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
    }

    QPushButton:hover {
        background-color: #1565C0;
    }

    QPushButton:pressed {
        background-color: #0D47A1;
    }
    """)

boton_unificar.clicked.connect(unificar_excel)

layout_principal.addWidget(boton_unificar)


# ============================================================
# ASIGNAR LAYOUT
# ============================================================

ventana.setLayout(layout_principal)


# ============================================================
# MOSTRAR VENTANA
# ============================================================

ventana.show()


# ============================================================
# EJECUTAR
# ============================================================

sys.exit(app.exec())
