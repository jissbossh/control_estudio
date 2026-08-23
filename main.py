# ============================================================
# IMPORTACIONES
# ============================================================
import sys

import json

import subprocess

import uuid

from pathlib import Path

from datetime import datetime

# ============================================================
# IMPORTACIONES PARA GUI
# ============================================================
from PySide6.QtCore import QDateTime, QTimer, Qt

from PySide6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QBrush,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QDateTimeEdit,
    QDoubleSpinBox,
    QHeaderView,
    QAbstractItemView,
    QFrame,
    QTextEdit,
)

# ============================================================
# CARGAR CONFIGURACIONES POR DEFECTO
# ============================================================

# def leer_json(ruta):
#     with open(ruta, "r", encoding="utf-8") as archivo:
#         datos = json.load(archivo)
#     return


def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


config = leer_json("config.json")
# ============================================================
# CONFIGURACIÓN DE FUENTE
# ============================================================

# FUENTE_APLICACION = "Segoe UI"
FUENTE_APLICACION = config["FUENTE_APLICACION"]

# TAMANO_FUENTE = 12
TAMANO_FUENTE = int(config["TAMANO_FUENTE"])

# ============================================================
# VERIFICACIÓN DE LIBRERÍAS
# ============================================================


def verificar_e_instalar_dependencias():
    """
    Verifica que las librerías externas necesarias estén instaladas.
    Si falta alguna, pregunta al usuario si desea instalarlas.
    """

    dependencias = {
        "PySide6": "PySide6",
        "tkcalendar": "tkcalendar",
        "pandas": "pandas",
        "beautifulsoup4": "beautifulsoup4"
    }

    faltantes = []

    for nombre, modulo in dependencias.items():

        try:
            __import__(modulo)

        except ImportError:
            faltantes.append(nombre)

    if not faltantes:
        return True

    print("=" * 60)
    print("FALTAN LIBRERÍAS")
    print("=" * 60)

    print("\nLas siguientes librerías no están instaladas:")

    for dependencia in faltantes:
        print(f"  - {dependencia}")

    print()

    respuesta = (
        input("¿Deseas instalar automáticamente las dependencias? [S/N]: ")
        .strip()
        .lower()
    )

    if respuesta not in ("s", "si", "sí", "y", "yes"):

        print("\nInstalación cancelada.")
        print("La aplicación no puede ejecutarse.")

        return False

    for dependencia in faltantes:

        print(f"\nInstalando {dependencia}...")

        try:

            resultado = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    dependencia,
                ],
                check=False,
            )

            if resultado.returncode != 0:

                print(f"\nNo se pudo instalar {dependencia}.")

                return False

            print(f"{dependencia} instalada correctamente.")

        except Exception as error:

            print(f"\nError instalando {dependencia}:")

            print(error)

            return False

    print("\nTodas las dependencias están instaladas.")

    return True


# ============================================================
# VERIFICAR DEPENDENCIAS ANTES DE IMPORTAR PYSIDE6
# ============================================================

if not verificar_e_instalar_dependencias():

    input("\nPresiona ENTER para salir...")

    sys.exit(1)


# ============================================================
# CONFIGURACIÓN
# ============================================================

COLUMNAS = [
    "PERIODO",
    "MOMENTO",
    "RAC",
    "CURSO",
    "TAREA",
    "ESTADO",
    "FECHA INDICADA",
    "FECHA INICIO",
    "FECHA ENTREGA",
    "FECHA CALIFICADA",
    "FALTAN",
    "CALIFICACION",
]

# ARCHIVO_POR_DEFECTO = "datos.json"
ARCHIVO_POR_DEFECTO = config["ARCHIVO_POR_DEFECTO"]

CAMPO_ID = "_ID"

# ============================================================
# COLORES DE LOS ESTADOS
# ============================================================

COLORES_ESTADOS = {
    "PENDIENTE": "#dc3545",
    "COMPLETADA": "#4361EE",
    "ENTREGADO": "#06D6A0",
    "CALIFICADA": "#0059FF",
    "EN PROCESO": "#FF9F1C",
    "EN REVISION": "#9B5DE5",
    "POR CALIFICAR": "#F15BB5",
    "REALIZADO": "#4CC9F0",
    "NO ASIGNADA": "#6C757D",
}


def color_estado(estado):

    return COLORES_ESTADOS.get(
        str(estado).strip().upper(),
        "#0d6efd",
    )


# ============================================================
# QLINEEDIT CON MAYÚSCULAS AUTOMÁTICAS
# ============================================================


class LineEditMayusculas(QLineEdit):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.textChanged.connect(self.convertir_mayusculas)

    def convertir_mayusculas(self, texto):

        texto_mayusculas = texto.upper()

        if texto != texto_mayusculas:

            posicion = self.cursorPosition()

            self.blockSignals(True)

            self.setText(texto_mayusculas)

            self.setCursorPosition(posicion)

            self.blockSignals(False)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================


def generar_id():

    return str(uuid.uuid4())


def asegurar_id(registro):

    if not registro.get(CAMPO_ID):

        registro[CAMPO_ID] = generar_id()

    return registro[CAMPO_ID]


def parsear_fecha(fecha):

    if not fecha:

        return None

    try:

        return datetime.fromisoformat(str(fecha))

    except (ValueError, TypeError):

        return None


def formatear_fecha(fecha):

    dt = parsear_fecha(fecha)

    if not dt:

        return fecha or ""

    return dt.strftime("%d/%m/%Y %H:%M")


# ============================================================
# CÁLCULO DINÁMICO DE FALTAN
# ============================================================


def calcular_faltan(
    fecha_entrega,
    estado="PENDIENTE",
):
    """
    Calcula dinámicamente cuánto tiempo falta para
    la fecha de entrega utilizando siempre la fecha
    y hora actual.
    """

    estado = str(estado).strip().upper()

    if estado == "NO ASIGNADA":

        return "No asignada"

    fecha = parsear_fecha(fecha_entrega)

    if fecha is None:

        return "Sin fecha"

    ahora = datetime.now()

    diferencia = fecha - ahora

    segundos = int(diferencia.total_seconds())

    if segundos < 0:

        segundos = abs(segundos)

        dias = segundos // 86400

        segundos %= 86400

        horas = segundos // 3600

        segundos %= 3600

        minutos = segundos // 60

        return f"Vencida hace {dias} días, " f"{horas} horas, " f"{minutos} minutos"

    dias = segundos // 86400

    segundos %= 86400

    horas = segundos // 3600

    segundos %= 3600

    minutos = segundos // 60

    return f"Faltan {dias} días, " f"{horas} horas, " f"{minutos} minutos"


def datetime_a_iso(widget):

    return widget.dateTime().toPython().isoformat(timespec="seconds")


def iso_a_qdatetime(fecha):

    dt = parsear_fecha(fecha)

    if dt is None:

        return QDateTime.currentDateTime()

    return QDateTime(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
    )


# ============================================================
# DIÁLOGO NUEVO / EDITAR
# ============================================================


class RegistroDialog(QDialog):

    def __init__(
        self,
        registro=None,
        parent=None,
    ):

        super().__init__(parent)

        self.registro_original = registro or {}

        if registro:

            self.setWindowTitle("✏️ Editar registro")

        else:

            self.setWindowTitle("➕ Nuevo registro")

        self.setMinimumWidth(700)

        self.construir_formulario()

        self.cargar_registro()

    # ========================================================
    # FORMULARIO
    # ========================================================

    def construir_formulario(self):

        layout = QVBoxLayout(self)

        titulo = QLabel(
            "Editar actividad" if self.registro_original else "Crear nueva actividad"
        )

        titulo.setFont(
            QFont(
                FUENTE_APLICACION,
                17,
                QFont.Bold,
            )
        )

        layout.addWidget(titulo)

        formulario = QGridLayout()

        formulario.setVerticalSpacing(10)

        formulario.addWidget(
            QLabel("Periodo:"),
            0,
            0,
        )

        self.periodo = LineEditMayusculas()

        self.periodo.setPlaceholderText("Ejemplo: 2026-2")

        formulario.addWidget(
            self.periodo,
            0,
            1,
        )

        formulario.addWidget(
            QLabel("Momento:"),
            1,
            0,
        )

        self.momento = QComboBox()

        self.momento.addItems(
            [
                "INICIAL",
                "INTERMEDIO",
                "FINAL",
            ]
        )

        formulario.addWidget(
            self.momento,
            1,
            1,
        )

        formulario.addWidget(
            QLabel("RAC:"),
            2,
            0,
        )

        self.rac = QComboBox()

        self.rac.addItems(
            [
                "RAC 1",
                "RAC 2",
                "RAC 3",
                "RAC 4",
                "RAC 5",
            ]
        )

        formulario.addWidget(
            self.rac,
            2,
            1,
        )

        formulario.addWidget(
            QLabel("Curso:"),
            3,
            0,
        )

        self.curso = LineEditMayusculas()

        formulario.addWidget(
            self.curso,
            3,
            1,
        )

        formulario.addWidget(
            QLabel("Tarea:"),
            4,
            0,
        )

        self.tarea = LineEditMayusculas()

        formulario.addWidget(
            self.tarea,
            4,
            1,
        )

        formulario.addWidget(
            QLabel("Estado:"),
            5,
            0,
        )

        self.estado = QComboBox()

        self.estado.addItems(
            [
                "ENTREGADO",
                "PENDIENTE",
                "REALIZADO",
                "EN PROCESO",
                "EN REVISION",
                "POR CALIFICAR",
                "COMPLETADA",
                "CALIFICADA",
                "NO ASIGNADA",
            ]
        )

        formulario.addWidget(
            self.estado,
            5,
            1,
        )

        campos_fecha = [
            (
                "Fecha indicada:",
                "fecha_indicada",
                6,
            ),
            (
                "Fecha inicio:",
                "fecha_inicio",
                7,
            ),
            (
                "Fecha entrega:",
                "fecha_entrega",
                8,
            ),
            (
                "Fecha calificada:",
                "fecha_calificada",
                9,
            ),
        ]

        for texto, atributo, fila in campos_fecha:

            formulario.addWidget(
                QLabel(texto),
                fila,
                0,
            )

            widget = QDateTimeEdit()

            widget.setCalendarPopup(True)

            widget.setDisplayFormat("dd/MM/yyyy HH:mm")

            setattr(
                self,
                atributo,
                widget,
            )

            formulario.addWidget(
                widget,
                fila,
                1,
            )

        formulario.addWidget(
            QLabel("Calificación:"),
            10,
            0,
        )

        self.calificacion = QDoubleSpinBox()

        self.calificacion.setRange(
            0,
            500,
        )

        self.calificacion.setDecimals(2)

        self.calificacion.setSingleStep(0.5)

        formulario.addWidget(
            self.calificacion,
            10,
            1,
        )

        layout.addLayout(formulario)

        botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        botones.accepted.connect(self.validar_y_aceptar)

        botones.rejected.connect(self.reject)

        layout.addWidget(botones)

    # ========================================================
    # CARGAR REGISTRO
    # ========================================================

    def cargar_registro(self):

        registro = self.registro_original

        if not registro:

            ahora = QDateTime.currentDateTime()

            self.fecha_indicada.setDateTime(ahora)

            self.fecha_inicio.setDateTime(ahora)

            self.fecha_entrega.setDateTime(ahora)

            self.fecha_calificada.setDateTime(ahora)

            return

        self.periodo.setText(
            str(
                registro.get(
                    "PERIODO",
                    "",
                )
            )
        )

        self.seleccionar_combo(
            self.momento,
            registro.get(
                "MOMENTO",
                "INICIAL",
            ),
        )

        self.seleccionar_combo(
            self.rac,
            registro.get(
                "RAC",
                "RAC 1",
            ),
        )

        self.curso.setText(
            registro.get(
                "CURSO",
                "",
            )
        )

        self.tarea.setText(
            registro.get(
                "TAREA",
                "",
            )
        )

        self.seleccionar_combo(
            self.estado,
            registro.get(
                "ESTADO",
                "PENDIENTE",
            ),
        )

        self.fecha_indicada.setDateTime(iso_a_qdatetime(registro.get("FECHA INDICADA")))

        self.fecha_inicio.setDateTime(iso_a_qdatetime(registro.get("FECHA INICIO")))

        self.fecha_entrega.setDateTime(iso_a_qdatetime(registro.get("FECHA ENTREGA")))

        self.fecha_calificada.setDateTime(
            iso_a_qdatetime(registro.get("FECHA CALIFICADA"))
        )

        try:

            self.calificacion.setValue(
                float(
                    registro.get(
                        "CALIFICACION",
                        0,
                    )
                )
            )

        except (ValueError, TypeError):

            self.calificacion.setValue(0)

    # ========================================================
    # COMBO
    # ========================================================

    @staticmethod
    def seleccionar_combo(
        combo,
        valor,
    ):

        indice = combo.findText(str(valor))

        if indice >= 0:

            combo.setCurrentIndex(indice)

    # ========================================================
    # VALIDAR
    # ========================================================

    def validar_y_aceptar(self):

        if not self.periodo.text().strip():

            QMessageBox.warning(
                self,
                "Dato requerido",
                "Debes indicar el período.",
            )

            return

        if not self.curso.text().strip():

            QMessageBox.warning(
                self,
                "Dato requerido",
                "Debes indicar el curso.",
            )

            return

        if not self.tarea.text().strip():

            QMessageBox.warning(
                self,
                "Dato requerido",
                "Debes indicar la tarea.",
            )

            return

        if self.registro_original:

            titulo = "Confirmar modificación"

            mensaje = "¿Deseas guardar los cambios " "realizados en este registro?"

        else:

            titulo = "Confirmar nuevo registro"

            mensaje = "¿Deseas crear este nuevo registro?"

        respuesta = QMessageBox.question(
            self,
            titulo,
            mensaje,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if respuesta != QMessageBox.Yes:

            return

        self.accept()

    # ========================================================
    # OBTENER REGISTRO
    # ========================================================

    def obtener_registro(self):

        estado = self.estado.currentText()

        fecha_entrega = datetime_a_iso(self.fecha_entrega)

        registro = {
            "PERIODO": self.periodo.text().strip(),
            "MOMENTO": self.momento.currentText(),
            "RAC": self.rac.currentText(),
            "CURSO": self.curso.text().strip(),
            "TAREA": self.tarea.text().strip(),
            "ESTADO": estado,
            "FECHA INDICADA": datetime_a_iso(self.fecha_indicada),
            "FECHA INICIO": datetime_a_iso(self.fecha_inicio),
            "FECHA ENTREGA": fecha_entrega,
            "FECHA CALIFICADA": datetime_a_iso(self.fecha_calificada),
            "FALTAN": calcular_faltan(
                fecha_entrega,
                estado,
            ),
            "CALIFICACION": self.calificacion.value(),
        }

        if self.registro_original:

            registro[CAMPO_ID] = self.registro_original.get(CAMPO_ID) or generar_id()

        else:

            registro[CAMPO_ID] = generar_id()

        return registro


# ============================================================
# DIÁLOGO DE DETALLE
# ============================================================


class DetalleDialog(QDialog):

    def __init__(
        self,
        registro,
        parent=None,
    ):

        super().__init__(parent)

        self.registro = registro

        self.setWindowTitle("🔎 Detalle de actividad")

        self.setMinimumSize(
            650,
            550,
        )

        self.construir_interfaz()

    def construir_interfaz(self):

        layout = QVBoxLayout(self)

        titulo = QLabel("📋 Detalle de la actividad")

        titulo.setFont(
            QFont(
                FUENTE_APLICACION,
                18,
                QFont.Bold,
            )
        )

        layout.addWidget(titulo)

        texto = QTextEdit()

        texto.setReadOnly(True)

        texto.setHtml(self.generar_html())

        layout.addWidget(
            texto,
            1,
        )

        botones = QDialogButtonBox(QDialogButtonBox.Close)

        botones.rejected.connect(self.reject)

        botones.accepted.connect(self.accept)

        layout.addWidget(botones)

    def generar_html(self):

        registro = self.registro

        estado = registro.get(
            "ESTADO",
            "",
        )

        color_estado_actual = color_estado(estado)

        filas = []

        campos = [
            ("PERIODO", "Periodo"),
            ("MOMENTO", "Momento"),
            ("RAC", "RAC"),
            ("CURSO", "Curso"),
            ("TAREA", "Tarea"),
            ("ESTADO", "Estado"),
            (
                "FECHA INDICADA",
                "Fecha indicada",
            ),
            (
                "FECHA INICIO",
                "Fecha inicio",
            ),
            (
                "FECHA ENTREGA",
                "Fecha entrega",
            ),
            (
                "FECHA CALIFICADA",
                "Fecha calificada",
            ),
            ("FALTAN", "Tiempo"),
            (
                "CALIFICACION",
                "Calificación",
            ),
        ]

        for campo, nombre in campos:

            valor = registro.get(
                campo,
                "",
            )

            if campo.startswith("FECHA"):

                valor = formatear_fecha(valor)

            elif campo == "FALTAN":

                valor = calcular_faltan(
                    registro.get("FECHA ENTREGA"),
                    registro.get("ESTADO"),
                )

            if campo == "ESTADO":

                valor_html = (
                    '<span style="'
                    f"color:{color_estado_actual};"
                    'font-weight:bold;">'
                    f"{valor}"
                    "</span>"
                )

            else:

                valor_html = str(valor)

            filas.append(f"""
                <tr>
                    <td style="
                        padding:8px;
                        font-weight:bold;
                        width:180px;
                    ">
                        {nombre}
                    </td>

                    <td style="
                        padding:8px;
                    ">
                        {valor_html}
                    </td>
                </tr>
                """)

        return f"""
        <html>
        <body>

        <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="100%"
        >

            {''.join(filas)}

        </table>

        </body>
        </html>
        """


# ============================================================
# VENTANA PRINCIPAL
# ============================================================


class VentanaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("📚 Gestor de actividades académicas")

        self.resize(
            1550,
            800,
        )

        self.setMinimumSize(
            1100,
            600,
        )

        self.showMaximized()

        ruta_icono = Path(__file__).resolve().parent / "icono.png"

        if ruta_icono.exists():

            self.setWindowIcon(QIcon(str(ruta_icono)))

        self.registros = []

        self.archivo_actual = Path(ARCHIVO_POR_DEFECTO)

        self.tema_actual = "oscuro"

        self.construir_interfaz()

        self.aplicar_tema_oscuro()

        self.cargar_json()

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.actualizar_faltan)

        self.timer.start(60000)

    # ========================================================
    # INTERFAZ
    # ========================================================

    def construir_interfaz(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # ====================================================
        # CABECERA
        # ====================================================

        cabecera = QHBoxLayout()

        titulo = QLabel("📚 Gestor de actividades académicas")

        titulo.setFont(
            QFont(
                FUENTE_APLICACION,
                20,
                QFont.Bold,
            )
        )

        cabecera.addWidget(titulo)

        cabecera.addStretch()

        self.boton_tema = QPushButton("☀️ Modo claro")

        self.boton_tema.clicked.connect(self.cambiar_tema)

        # cabecera.addWidget(self.boton_tema)

        boton_cargar_datos = QPushButton("📥 Cargar datos")

        boton_cargar_datos.setToolTip("Ejecutar el script cargar_datos.py")

        boton_cargar_datos.clicked.connect(self.ejecutar_cargar_datos)

        cabecera.addWidget(boton_cargar_datos)

        boton_unificar_datos = QPushButton("🔀 Unificar datos")

        boton_unificar_datos.setToolTip("Ejecutar el script unificar_datos.py")

        boton_unificar_datos.clicked.connect(self.ejecutar_unificar_datos)

        cabecera.addWidget(boton_unificar_datos)

        boton_excel_json = QPushButton("📊 Excel → JSON")

        boton_excel_json.setToolTip("Ejecutar el script excel_to_json.py")

        boton_excel_json.clicked.connect(self.ejecutar_excel_to_json)

        cabecera.addWidget(boton_excel_json)

        boton_calendar_json = QPushButton("📅 Crear Eventos")

        boton_calendar_json.setToolTip("Ejecutar el script crear_eventos.py")

        boton_calendar_json.clicked.connect(self.ejecutar_crear_eventos)

        cabecera.addWidget(boton_calendar_json)

        layout.addLayout(cabecera)

        # ====================================================
        # ARCHIVO
        # ====================================================

        self.label_archivo = QLabel(f"Archivo: {self.archivo_actual}")

        self.label_archivo.setStyleSheet("font-weight: bold;")

        layout.addWidget(self.label_archivo)

        # ====================================================
        # BUSCADOR + ARCHIVOS
        # ====================================================

        barra_archivo = QHBoxLayout()

        barra_archivo.addWidget(QLabel("🔍 Buscar:"))

        self.buscar = LineEditMayusculas()

        self.buscar.setPlaceholderText(
            "Buscar por período, curso, tarea, RAC, momento..."
        )

        self.buscar.textChanged.connect(self.aplicar_filtros)

        barra_archivo.addWidget(
            self.buscar,
            2,
        )

        boton_abrir = QPushButton("📂 Abrir JSON")

        boton_abrir.clicked.connect(self.abrir_json)

        barra_archivo.addWidget(boton_abrir)

        boton_recargar = QPushButton("🔄 Recargar")

        boton_recargar.setToolTip("Volver a cargar los datos del archivo JSON actual")

        boton_recargar.clicked.connect(self.recargar_json)

        barra_archivo.addWidget(boton_recargar)

        boton_guardar = QPushButton("💾 Guardar")

        boton_guardar.clicked.connect(self.guardar_json)

        barra_archivo.addWidget(boton_guardar)

        boton_guardar_como = QPushButton("💾 Guardar como...")

        boton_guardar_como.clicked.connect(self.guardar_como)

        barra_archivo.addWidget(boton_guardar_como)

        layout.addLayout(barra_archivo)

        # ====================================================
        # SEPARADOR
        # ====================================================

        linea = QFrame()

        linea.setFrameShape(QFrame.HLine)

        layout.addWidget(linea)

        # ====================================================
        # FILTROS
        # ====================================================

        filtros = QHBoxLayout()

        filtros.addWidget(QLabel("Periodo:"))

        self.filtro_periodo = QComboBox()

        self.filtro_periodo.addItem("Todos")

        self.filtro_periodo.currentTextChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.filtro_periodo)

        filtros.addWidget(QLabel("Momento:"))

        self.filtro_momento = QComboBox()

        self.filtro_momento.addItems(
            [
                "Todos",
                "INICIAL",
                "INTERMEDIO",
                "FINAL",
            ]
        )

        self.filtro_momento.currentTextChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.filtro_momento)

        filtros.addWidget(QLabel("RAC:"))

        self.filtro_rac = QComboBox()

        self.filtro_rac.addItems(
            [
                "Todos",
                "RAC 1",
                "RAC 2",
                "RAC 3",
                "RAC 4",
                "RAC 5",
            ]
        )

        self.filtro_rac.currentTextChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.filtro_rac)

        filtros.addWidget(QLabel("Curso:"))

        self.filtro_curso = QComboBox()

        self.filtro_curso.addItem("Todos")

        self.filtro_curso.currentTextChanged.connect(self.aplicar_filtros)

        filtros.addWidget(
            self.filtro_curso,
            2,
        )

        filtros.addWidget(QLabel("Estado:"))

        self.filtro_estado = QComboBox()

        self.filtro_estado.addItems(
            [
                "Todos",
                "PENDIENTE",
                "ENTREGADO",
                "REALIZADO",
                "EN PROCESO",
                "EN REVISION",
                "POR CALIFICAR",
                "COMPLETADA",
                "CALIFICADA",
                "NO ASIGNADA",
            ]
        )

        self.filtro_estado.currentTextChanged.connect(self.aplicar_filtros)

        filtros.addWidget(self.filtro_estado)

        boton_limpiar = QPushButton("Limpiar filtros")

        boton_limpiar.clicked.connect(self.limpiar_filtros)

        filtros.addWidget(boton_limpiar)

        layout.addLayout(filtros)

        # ====================================================
        # TABLA
        # ====================================================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(len(COLUMNAS))

        self.tabla.setHorizontalHeaderLabels(COLUMNAS)

        self.tabla.verticalHeader().setDefaultSectionSize(60)

        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tabla.setEditTriggers(QAbstractItemView.EditKeyPressed)

        self.tabla.setAlternatingRowColors(True)

        self.tabla.setSortingEnabled(True)

        self.tabla.cellChanged.connect(self.celda_modificada)

        header = self.tabla.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.Interactive)

        header.setStretchLastSection(True)

        anchos = {
            0: 120,
            1: 120,
            2: 140,
            3: 500,
            4: 500,
            5: 130,
            6: 180,
            7: 180,
            8: 180,
            9: 200,
            10: 320,
            11: 160,
        }

        # Ajustar columnas al contenido
        self.tabla.resizeColumnsToContents()

        # for columna, ancho_minimo in anchos.items():
        #     ancho_actual = self.tabla.columnWidth(columna)

        # if ancho_actual < ancho_minimo:
        #     self.tabla.setColumnWidth(
        #         columna,
        #         ancho_minimo,
        #     )

        for columna, ancho in anchos.items():

            self.tabla.setColumnWidth(
                columna,
                ancho,
            )

        layout.addWidget(
            self.tabla,
            1,
        )

        # ====================================================
        # BOTONES INFERIORES
        # ====================================================

        botones = QHBoxLayout()

        boton_nuevo = QPushButton("➕ Nuevo")

        boton_nuevo.clicked.connect(self.nuevo_registro)

        botones.addWidget(boton_nuevo)

        boton_detalle = QPushButton("🔎 Ver detalle")

        boton_detalle.clicked.connect(self.ver_detalle)

        botones.addWidget(boton_detalle)

        boton_editar = QPushButton("✏️ Editar")

        boton_editar.clicked.connect(self.editar_registro)

        botones.addWidget(boton_editar)

        boton_eliminar = QPushButton("🗑️ Eliminar")

        boton_eliminar.clicked.connect(self.eliminar_registro)

        botones.addWidget(boton_eliminar)

        botones.addStretch()

        self.label_registros = QLabel("Registros: 0")

        botones.addWidget(self.label_registros)

        version = leer_json("version.json")

        VERSION = version["VERSION"]

        AUTOR = version["AUTOR"]

        self.label_info = QLabel(
            "          Version de la aplicacion: " + VERSION + "    Autor: " + AUTOR
        )

        botones.addWidget(self.label_info)

        layout.addLayout(botones)

    # ========================================================
    # EJECUTAR CARGAR_DATOS.PY
    # ========================================================

    def ejecutar_cargar_datos(self):

        ruta_script = Path(__file__).resolve().parent / "cargar_datos.py"

        if not ruta_script.exists():

            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                (
                    "No se encontró el archivo:\n\n"
                    f"{ruta_script}\n\n"
                    "Verifica que cargar_datos.py esté "
                    "en la misma carpeta que la aplicación."
                ),
            )

            return

        try:

            resultado = subprocess.run(
                [
                    sys.executable,
                    str(ruta_script),
                ],
                check=False,
            )

            if resultado.returncode == 0:

                self.statusBar().showMessage("📥 Cargar datos ejecutado correctamente.")

                QMessageBox.information(
                    self,
                    "Cargar datos",
                    ("El script cargar_datos.py " "se ejecutó correctamente."),
                )

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    (
                        "El script cargar_datos.py terminó "
                        "con un código de error.\n\n"
                        f"Código: {resultado.returncode}"
                    ),
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al ejecutar script",
                ("No se pudo ejecutar " "cargar_datos.py.\n\n" f"Error:\n{error}"),
            )

    # ========================================================
    # EJECUTAR UNIFICAR_DATOS.PY
    # ========================================================

    def ejecutar_unificar_datos(self):

        ruta_script = Path(__file__).resolve().parent / "unificar_datos.py"

        if not ruta_script.exists():

            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                (
                    "No se encontró el archivo:\n\n"
                    f"{ruta_script}\n\n"
                    "Verifica que unificar_datos.py esté "
                    "en la misma carpeta que la aplicación."
                ),
            )

            return

        try:

            resultado = subprocess.run(
                [
                    sys.executable,
                    str(ruta_script),
                ],
                check=False,
            )

            if resultado.returncode == 0:

                self.statusBar().showMessage(
                    "🔀 Unificación de datos ejecutada correctamente."
                )

                QMessageBox.information(
                    self,
                    "Unificar datos",
                    ("El script unificar_datos.py " "se ejecutó correctamente."),
                )

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    (
                        "El script unificar_datos.py terminó "
                        "con un código de error.\n\n"
                        f"Código: {resultado.returncode}"
                    ),
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al ejecutar script",
                ("No se pudo ejecutar " "unificar_datos.py.\n\n" f"Error:\n{error}"),
            )

    # ========================================================
    # EJECUTAR EXCEL_TO_JSON.PY
    # ========================================================

    def ejecutar_excel_to_json(self):

        ruta_script = Path(__file__).resolve().parent / "excel_to_json.py"

        if not ruta_script.exists():

            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                (
                    "No se encontró el archivo:\n\n"
                    f"{ruta_script}\n\n"
                    "Verifica que excel_to_json.py esté "
                    "en la misma carpeta que la aplicación."
                ),
            )

            return

        try:

            resultado = subprocess.run(
                [
                    sys.executable,
                    str(ruta_script),
                ],
                check=False,
            )

            if resultado.returncode == 0:

                self.statusBar().showMessage("📊 Excel → JSON ejecutado correctamente.")

                QMessageBox.information(
                    self,
                    "Excel → JSON",
                    ("El script excel_to_json.py " "se ejecutó correctamente."),
                )

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    (
                        "El script excel_to_json.py terminó "
                        "con un código de error.\n\n"
                        f"Código: {resultado.returncode}"
                    ),
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al ejecutar script",
                ("No se pudo ejecutar " "excel_to_json.py.\n\n" f"Error:\n{error}"),
            )

    # ========================================================
    # EJECUTAR EJECUTAR_CREAR_EVENTOS.PY
    # ========================================================

    def ejecutar_crear_eventos(self):

        ruta_script = Path(__file__).resolve().parent / "crear_eventos.py"

        if not ruta_script.exists():

            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                (
                    "No se encontró el archivo:\n\n"
                    f"{ruta_script}\n\n"
                    "Verifica que crear_eventos.py esté "
                    "en la misma carpeta que la aplicación."
                ),
            )

            return

        try:

            resultado = subprocess.run(
                [
                    sys.executable,
                    str(ruta_script),
                ],
                check=False,
            )

            if resultado.returncode == 0:

                self.statusBar().showMessage(
                    "📅 Crear Eventos ejecutado correctamente."
                )

                QMessageBox.information(
                    self,
                    "Crear Eventos",
                    ("El script crear_eventos.py " "se ejecutó correctamente."),
                )

            else:

                QMessageBox.warning(
                    self,
                    "Error",
                    (
                        "El script excel_to_json.py terminó "
                        "con un código de error.\n\n"
                        f"Código: {resultado.returncode}"
                    ),
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error al ejecutar script",
                ("No se pudo ejecutar " "crear_eventos.py.\n\n" f"Error:\n{error}"),
            )

    # ========================================================
    # TEMA
    # ========================================================

    def cambiar_tema(self):

        if self.tema_actual == "claro":

            self.tema_actual = "oscuro"

            self.aplicar_tema_oscuro()

            self.boton_tema.setText("☀️ Modo claro")

        else:

            self.tema_actual = "claro"

            self.aplicar_tema_claro()

            self.boton_tema.setText("🌙 Modo oscuro")

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

    # ========================================================
    # CARGAR JSON
    # ========================================================

    def cargar_json(self):

        if not self.archivo_actual.exists():

            self.registros = []

            self.actualizar_filtros()

            self.mostrar_tabla()

            return

        try:

            with open(
                self.archivo_actual,
                "r",
                encoding="utf-8",
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):

                raise ValueError("El JSON debe contener una lista.")

            for registro in datos:

                if "PERIODO" not in registro:

                    registro["PERIODO"] = ""

                asegurar_id(registro)

                registro["FALTAN"] = calcular_faltan(
                    registro.get("FECHA ENTREGA"),
                    registro.get("ESTADO"),
                )

            self.registros = datos

            self.actualizar_filtros()

            self.mostrar_tabla()

            self.statusBar().showMessage(f"Se cargaron {len(datos)} registros.")

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar el JSON:\n\n{e}",
            )

    # ========================================================
    # RECARGAR JSON
    # ========================================================

    def recargar_json(self):

        if not self.archivo_actual.exists():

            QMessageBox.information(
                self,
                "Recargar",
                (
                    "El archivo actualmente seleccionado "
                    "no existe:\n\n"
                    f"{self.archivo_actual}"
                ),
            )

            return

        respuesta = QMessageBox.question(
            self,
            "Recargar datos",
            (
                "Se volverán a cargar los datos "
                "desde el archivo JSON.\n\n"
                "Los cambios realizados en la aplicación "
                "que todavía no hayas guardado se perderán.\n\n"
                "¿Deseas continuar?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if respuesta != QMessageBox.Yes:

            return

        self.cargar_json()

        self.statusBar().showMessage(
            ("🔄 Datos recargados desde: " f"{self.archivo_actual}")
        )

    # ========================================================
    # MOSTRAR TABLA
    # ========================================================

    def mostrar_tabla(self):

        self.tabla.blockSignals(True)

        self.tabla.setSortingEnabled(False)

        self.tabla.setRowCount(len(self.registros))

        for fila, registro in enumerate(self.registros):

            registro_id = asegurar_id(registro)

            estado_actual = registro.get(
                "ESTADO",
                "",
            )

            color_actual = color_estado(estado_actual)

            for columna, nombre in enumerate(COLUMNAS):

                valor = registro.get(
                    nombre,
                    "",
                )

                if nombre in [
                    "FECHA INDICADA",
                    "FECHA INICIO",
                    "FECHA ENTREGA",
                    "FECHA CALIFICADA",
                ]:

                    texto = formatear_fecha(valor)

                elif nombre == "FALTAN":

                    texto = calcular_faltan(
                        registro.get("FECHA ENTREGA"),
                        registro.get("ESTADO"),
                    )

                else:

                    texto = str(valor)

                item = QTableWidgetItem(texto)

                # ------------------------------------------------
                # IMPORTANTE:
                # GUARDAMOS EL ID DEL REGISTRO EN CADA FILA
                # ------------------------------------------------

                item.setData(
                    Qt.UserRole,
                    registro_id,
                )

                if nombre in [
                    "PERIODO",
                    "MOMENTO",
                    "RAC",
                    "ESTADO",
                    "CALIFICACION",
                ]:

                    item.setTextAlignment(Qt.AlignCenter)

                item.setForeground(QBrush(QColor(color_actual)))

                if nombre == "ESTADO":

                    fuente = item.font()

                    fuente.setBold(True)

                    item.setFont(fuente)

                self.tabla.setItem(
                    fila,
                    columna,
                    item,
                )

        self.tabla.setSortingEnabled(True)

        self.tabla.blockSignals(False)

        self.actualizar_contador()

        self.aplicar_filtros()

    # ========================================================
    # FILTROS
    # ========================================================

    def actualizar_filtros(self):

        periodo_actual = (
            self.filtro_periodo.currentText()
            if hasattr(
                self,
                "filtro_periodo",
            )
            else "Todos"
        )

        periodos = sorted(
            set(
                str(
                    r.get(
                        "PERIODO",
                        "",
                    )
                )
                for r in self.registros
                if r.get("PERIODO")
            )
        )

        self.filtro_periodo.blockSignals(True)

        self.filtro_periodo.clear()

        self.filtro_periodo.addItem("Todos")

        self.filtro_periodo.addItems(periodos)

        indice = self.filtro_periodo.findText(periodo_actual)

        if indice >= 0:

            self.filtro_periodo.setCurrentIndex(indice)

        self.filtro_periodo.blockSignals(False)

        # ----------------------------------------------------
        # MOMENTO
        # ----------------------------------------------------

        momento_actual = (
            self.filtro_momento.currentText()
            if hasattr(
                self,
                "filtro_momento",
            )
            else "Todos"
        )

        momentos = sorted(
            set(
                str(
                    r.get(
                        "MOMENTO",
                        "",
                    )
                )
                for r in self.registros
                if r.get("MOMENTO")
            )
        )

        self.filtro_momento.blockSignals(True)

        self.filtro_momento.clear()

        self.filtro_momento.addItem("Todos")

        self.filtro_momento.addItems(momentos)

        indice = self.filtro_momento.findText(momento_actual)

        if indice >= 0:

            self.filtro_momento.setCurrentIndex(indice)

        self.filtro_momento.blockSignals(False)

        # ----------------------------------------------------
        # RAC
        # ----------------------------------------------------

        rac_actual = (
            self.filtro_rac.currentText()
            if hasattr(
                self,
                "filtro_rac",
            )
            else "Todos"
        )

        racs = sorted(
            set(
                str(
                    r.get(
                        "RAC",
                        "",
                    )
                )
                for r in self.registros
                if r.get("RAC")
            )
        )

        self.filtro_rac.blockSignals(True)

        self.filtro_rac.clear()

        self.filtro_rac.addItem("Todos")

        self.filtro_rac.addItems(racs)

        indice = self.filtro_rac.findText(rac_actual)

        if indice >= 0:

            self.filtro_rac.setCurrentIndex(indice)

        self.filtro_rac.blockSignals(False)

        # ----------------------------------------------------
        # CURSO
        # ----------------------------------------------------

        curso_actual = (
            self.filtro_curso.currentText()
            if hasattr(
                self,
                "filtro_curso",
            )
            else "Todos"
        )

        cursos = sorted(
            set(
                str(
                    r.get(
                        "CURSO",
                        "",
                    )
                )
                for r in self.registros
                if r.get("CURSO")
            )
        )

        self.filtro_curso.blockSignals(True)

        self.filtro_curso.clear()

        self.filtro_curso.addItem("Todos")

        self.filtro_curso.addItems(cursos)

        indice = self.filtro_curso.findText(curso_actual)

        if indice >= 0:

            self.filtro_curso.setCurrentIndex(indice)

        self.filtro_curso.blockSignals(False)

    # ========================================================
    # APLICAR FILTROS
    # ========================================================

    def aplicar_filtros(self):
        """
        Aplica los filtros utilizando el ID del registro
        asociado a cada fila visual de la tabla.

        Esto permite que los filtros funcionen correctamente
        incluso después de ordenar cualquier columna.
        """

        texto = self.buscar.text().strip().upper()

        periodo = self.filtro_periodo.currentText().strip().upper()

        momento = self.filtro_momento.currentText().strip().upper()

        rac = self.filtro_rac.currentText().strip().upper()

        curso = self.filtro_curso.currentText().strip().upper()

        estado = self.filtro_estado.currentText().strip().upper()

        visibles = 0

        # ----------------------------------------------------
        # RECORRER LAS FILAS VISUALES
        # ----------------------------------------------------

        for fila in range(self.tabla.rowCount()):

            item_id = self.tabla.item(
                fila,
                0,
            )

            if item_id is None:

                self.tabla.setRowHidden(
                    fila,
                    True,
                )

                continue

            registro_id = item_id.data(Qt.UserRole)

            if not registro_id:

                self.tabla.setRowHidden(
                    fila,
                    True,
                )

                continue

            # ------------------------------------------------
            # BUSCAR REGISTRO REAL MEDIANTE ID
            # ------------------------------------------------

            registro = None

            for elemento in self.registros:

                if elemento.get(CAMPO_ID) == registro_id:

                    registro = elemento

                    break

            if registro is None:

                self.tabla.setRowHidden(
                    fila,
                    True,
                )

                continue

            # ------------------------------------------------
            # VALORES DEL REGISTRO
            # ------------------------------------------------

            registro_periodo = (
                str(
                    registro.get(
                        "PERIODO",
                        "",
                    )
                )
                .strip()
                .upper()
            )

            registro_momento = (
                str(
                    registro.get(
                        "MOMENTO",
                        "",
                    )
                )
                .strip()
                .upper()
            )

            registro_rac = (
                str(
                    registro.get(
                        "RAC",
                        "",
                    )
                )
                .strip()
                .upper()
            )

            registro_curso = (
                str(
                    registro.get(
                        "CURSO",
                        "",
                    )
                )
                .strip()
                .upper()
            )

            registro_estado = (
                str(
                    registro.get(
                        "ESTADO",
                        "",
                    )
                )
                .strip()
                .upper()
            )

            # ------------------------------------------------
            # BUSCADOR GENERAL
            # ------------------------------------------------

            contenido = " ".join(
                str(
                    registro.get(
                        campo,
                        "",
                    )
                )
                for campo in COLUMNAS
            ).upper()

            coincide_texto = not texto or texto in contenido

            # ------------------------------------------------
            # PERIODO
            # ------------------------------------------------

            coincide_periodo = periodo == "TODOS" or registro_periodo == periodo

            # ------------------------------------------------
            # MOMENTO
            # ------------------------------------------------

            coincide_momento = momento == "TODOS" or registro_momento == momento

            # ------------------------------------------------
            # RAC
            # ------------------------------------------------

            coincide_rac = rac == "TODOS" or registro_rac == rac

            # ------------------------------------------------
            # CURSO
            # ------------------------------------------------

            coincide_curso = curso == "TODOS" or registro_curso == curso

            # ------------------------------------------------
            # ESTADO
            # ------------------------------------------------

            coincide_estado = estado == "TODOS" or registro_estado == estado

            # ------------------------------------------------
            # COMBINACIÓN DE TODOS LOS FILTROS
            # ------------------------------------------------

            visible = (
                coincide_texto
                and coincide_periodo
                and coincide_momento
                and coincide_rac
                and coincide_curso
                and coincide_estado
            )

            self.tabla.setRowHidden(
                fila,
                not visible,
            )

            if visible:

                visibles += 1

        self.label_registros.setText(
            f"Mostrando: {visibles} / " f"{len(self.registros)}"
        )

    # ========================================================
    # LIMPIAR FILTROS
    # ========================================================

    def limpiar_filtros(self):

        self.buscar.clear()

        self.filtro_periodo.setCurrentIndex(0)

        self.filtro_momento.setCurrentIndex(0)

        self.filtro_rac.setCurrentIndex(0)

        self.filtro_curso.setCurrentIndex(0)

        self.filtro_estado.setCurrentIndex(0)

        self.aplicar_filtros()

    # ========================================================
    # REGISTRO SELECCIONADO
    # ========================================================

    def obtener_registro_seleccionado(self):

        filas = self.tabla.selectionModel().selectedRows()

        if not filas:

            return None

        fila_visual = filas[0].row()

        item = self.tabla.item(
            fila_visual,
            0,
        )

        if item is None:

            return None

        registro_id = item.data(Qt.UserRole)

        if not registro_id:

            return None

        for registro in self.registros:

            if registro.get(CAMPO_ID) == registro_id:

                return registro

        return None

    # ========================================================
    # ÍNDICE SELECCIONADO
    # ========================================================

    def fila_seleccionada(self):

        filas = self.tabla.selectionModel().selectedRows()

        if not filas:

            return None

        fila_visual = filas[0].row()

        item = self.tabla.item(
            fila_visual,
            0,
        )

        if item is None:

            return None

        registro_id = item.data(Qt.UserRole)

        if not registro_id:

            return None

        for indice, registro in enumerate(self.registros):

            if registro.get(CAMPO_ID) == registro_id:

                return indice

        return None

    # ========================================================
    # NUEVO
    # ========================================================

    def nuevo_registro(self):

        dialogo = RegistroDialog(parent=self)

        if dialogo.exec() == QDialog.Accepted:

            registro = dialogo.obtener_registro()

            self.registros.append(registro)

            self.actualizar_filtros()

            self.mostrar_tabla()

            self.statusBar().showMessage("✅ Registro creado correctamente.")

            QMessageBox.information(
                self,
                "Registro creado",
                ("El nuevo registro se creó " "correctamente."),
            )

    # ========================================================
    # VER DETALLE
    # ========================================================

    def ver_detalle(self):

        registro = self.obtener_registro_seleccionado()

        if registro is None:

            QMessageBox.information(
                self,
                "Ver detalle",
                "Selecciona primero una fila.",
            )

            return

        dialogo = DetalleDialog(
            registro,
            self,
        )

        dialogo.exec()

    # ========================================================
    # EDITAR
    # ========================================================

    def editar_registro(self):

        indice = self.fila_seleccionada()

        if indice is None:

            QMessageBox.information(
                self,
                "Editar registro",
                "Selecciona primero una fila.",
            )

            return

        registro = self.registros[indice]

        dialogo = RegistroDialog(
            registro,
            self,
        )

        if dialogo.exec() == QDialog.Accepted:

            self.registros[indice] = dialogo.obtener_registro()

            self.actualizar_filtros()

            self.mostrar_tabla()

            self.statusBar().showMessage("✅ Registro actualizado.")

            QMessageBox.information(
                self,
                "Registro modificado",
                (
                    "Los cambios del registro "
                    "se guardaron correctamente "
                    "en la aplicación.\n\n"
                    "Recuerda utilizar el botón "
                    "'Guardar' para conservarlos "
                    "en el archivo JSON."
                ),
            )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar_registro(self):

        indice = self.fila_seleccionada()

        if indice is None:

            QMessageBox.information(
                self,
                "Eliminar registro",
                "Selecciona primero una fila.",
            )

            return

        registro = self.registros[indice]

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            (
                "¿Estás seguro de eliminar "
                "este registro?\n\n"
                f"Periodo: "
                f"{registro.get('PERIODO', '')}\n"
                f"Curso: "
                f"{registro.get('CURSO', '')}\n"
                f"Tarea: "
                f"{registro.get('TAREA', '')}"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if respuesta != QMessageBox.Yes:

            return

        del self.registros[indice]

        self.actualizar_filtros()

        self.mostrar_tabla()

        self.statusBar().showMessage("🗑️ Registro eliminado.")

    # ========================================================
    # EDITAR CELDA
    # ========================================================

    def celda_modificada(
        self,
        fila,
        columna,
    ):
        """
        Edita el registro utilizando el ID asociado
        a la fila, no la posición de la fila.

        Esto permite editar correctamente incluso
        después de ordenar la tabla.
        """

        item = self.tabla.item(
            fila,
            columna,
        )

        if item is None:

            return

        valor = item.text()

        nombre = COLUMNAS[columna]

        # ----------------------------------------------------
        # OBTENER ID REAL DE LA FILA
        # ----------------------------------------------------

        item_id = self.tabla.item(
            fila,
            0,
        )

        if item_id is None:

            return

        registro_id = item_id.data(Qt.UserRole)

        if not registro_id:

            return

        # ----------------------------------------------------
        # BUSCAR REGISTRO
        # ----------------------------------------------------

        registro = None

        for elemento in self.registros:

            if elemento.get(CAMPO_ID) == registro_id:

                registro = elemento

                break

        if registro is None:

            return

        # ----------------------------------------------------
        # FALTAN NO SE EDITA
        # ----------------------------------------------------

        if nombre == "FALTAN":

            self.mostrar_tabla()

            return

        # ----------------------------------------------------
        # FECHAS
        # ----------------------------------------------------

        if nombre in [
            "FECHA INDICADA",
            "FECHA INICIO",
            "FECHA ENTREGA",
            "FECHA CALIFICADA",
        ]:

            try:

                dt = datetime.strptime(
                    valor,
                    "%d/%m/%Y %H:%M",
                )

                registro[nombre] = dt.isoformat(timespec="seconds")

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Fecha incorrecta",
                    ("Formato incorrecto.\n\n" "Usa:\n" "DD/MM/YYYY HH:MM"),
                )

                self.mostrar_tabla()

                return

        # ----------------------------------------------------
        # CALIFICACIÓN
        # ----------------------------------------------------

        elif nombre == "CALIFICACION":

            try:

                calificacion = float(
                    valor.replace(
                        ",",
                        ".",
                    )
                )

                if not (0 <= calificacion <= 500):

                    raise ValueError

                registro[nombre] = calificacion

            except ValueError:

                QMessageBox.warning(
                    self,
                    "Calificación incorrecta",
                    ("La calificación debe " "estar entre 0 y 500."),
                )

                self.mostrar_tabla()

                return

        # ----------------------------------------------------
        # CAMPOS NORMALES
        # ----------------------------------------------------

        else:

            registro[nombre] = valor

        # ----------------------------------------------------
        # ACTUALIZAR FALTAN
        # ----------------------------------------------------

        registro["FALTAN"] = calcular_faltan(
            registro.get("FECHA ENTREGA"),
            registro.get("ESTADO"),
        )

        # ----------------------------------------------------
        # ACTUALIZAR FILTROS
        # ----------------------------------------------------

        self.actualizar_filtros()

        self.mostrar_tabla()

        self.statusBar().showMessage(
            ("✏️ Cambio realizado. " "Guarda el archivo para conservarlo.")
        )

    # ========================================================
    # ACTUALIZAR FALTAN
    # ========================================================

    def actualizar_faltan(self):

        for registro in self.registros:

            registro["FALTAN"] = calcular_faltan(
                registro.get("FECHA ENTREGA"),
                registro.get("ESTADO"),
            )

        self.mostrar_tabla()

    # ========================================================
    # GUARDAR JSON
    # ========================================================

    def guardar_json(self):

        try:

            for registro in self.registros:

                registro["FALTAN"] = calcular_faltan(
                    registro.get("FECHA ENTREGA"),
                    registro.get("ESTADO"),
                )

            with open(
                self.archivo_actual,
                "w",
                encoding="utf-8",
            ) as archivo:

                datos_guardar = []

                for registro in self.registros:

                    copia = dict(registro)

                    datos_guardar.append(copia)

                json.dump(
                    datos_guardar,
                    archivo,
                    ensure_ascii=False,
                    indent=4,
                )

            self.statusBar().showMessage(
                ("💾 Guardado correctamente: " f"{self.archivo_actual}")
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                ("No se pudo guardar " f"el archivo:\n\n{e}"),
            )

    # ========================================================
    # GUARDAR COMO
    # ========================================================

    def guardar_como(self):

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar JSON",
            str(self.archivo_actual),
            "Archivos JSON (*.json)",
        )

        if not archivo:

            return

        self.archivo_actual = Path(archivo)

        self.label_archivo.setText(f"Archivo: {self.archivo_actual}")

        self.guardar_json()

    # ========================================================
    # ABRIR
    # ========================================================

    def abrir_json(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo JSON",
            "",
            "Archivos JSON (*.json)",
        )

        if not archivo:

            return

        self.archivo_actual = Path(archivo)

        self.label_archivo.setText(f"Archivo: {self.archivo_actual}")

        self.cargar_json()

    # ========================================================
    # CONTADOR
    # ========================================================

    def actualizar_contador(self):

        self.label_registros.setText(f"Registros: {len(self.registros)}")


# ============================================================
# MAIN
# ============================================================


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("Gestor de actividades académicas")

    fuente = QFont(
        FUENTE_APLICACION,
        TAMANO_FUENTE,
    )

    app.setFont(fuente)

    ruta_icono = Path(__file__).resolve().parent / "icono.png"

    if ruta_icono.exists():

        app.setWindowIcon(QIcon(str(ruta_icono)))

    ventana = VentanaPrincipal()

    ventana.show()

    sys.exit(app.exec())


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()
