from pathlib import Path
import sys

import json

import uuid

import os

from datetime import datetime, timezone

from zoneinfo import ZoneInfo

from urllib.parse import quote

from PySide6.QtCore import Qt

from PySide6.QtGui import QFont, QIcon

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QFrame,
)

# ============================================================
# CARGAR CONFIGURACIONES POR DEFECTO
# ============================================================


def leer_json(ruta):

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


config = leer_json("config.json")


FUENTE_APLICACION = config["FUENTE_APLICACION"]

TAMANO_FUENTE = int(config["TAMANO_FUENTE"])

TEMA = str(config["TEMA"]).strip().upper()


# ============================================================
# CONFIGURACIÓN
# ============================================================

ZONA_HORARIA = ZoneInfo("America/Bogota")

HORA_INICIO = "16:00"
HORA_FIN = "22:00"


# ============================================================
# TEMA CLARO
# ============================================================


def aplicar_tema_claro(self):

    self.setStyleSheet(f"""
        QWidget {{
            font-family: "{FUENTE_APLICACION}";
            font-size: {TAMANO_FUENTE}pt;
            color: #212529;
            background-color: #f5f7fa;
        }}

        QMainWindow,
        QDialog {{
            background-color: #f5f7fa;
        }}

        QLabel {{
            color: #212529;
            background: transparent;
        }}

        QLabel#tituloPrincipal {{
            color: #1f2937;
            font-size: 23px;
            font-weight: bold;
            background: transparent;
        }}

        QLabel#subtituloPrincipal {{
            color: #6b7280;
            background: transparent;
        }}

        QLabel#estadoArchivo {{
            color: #6b7280;
            background: transparent;
        }}

        QFrame#infoConfiguracion {{
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 5px;
        }}

        QLabel#tituloConfiguracion {{
            color: #212529;
            font-weight: bold;
            background: transparent;
            border: none;
        }}

        QLabel#descripcionConfiguracion {{
            color: #6b7280;
            background: transparent;
            border: none;
        }}

        QLabel#etiquetaGenerar,
        QLabel#etiquetaResultado {{
            color: #212529;
            font-weight: bold;
            background: transparent;
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

        QTextEdit {{
            background-color: white;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 3px;
            padding: 5px;
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

        QScrollBar:vertical {{
            background: #f1f1f1;
            width: 12px;
        }}

        QScrollBar::handle:vertical {{
            background: #c0c0c0;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: #999999;
        }}

        QDialogButtonBox QPushButton {{
            min-width: 90px;
        }}

        QMessageBox {{
            background-color: white;
            color: #212529;
        }}

        QMessageBox QLabel {{
            color: #212529;
        }}

        QMessageBox QPushButton {{
            background-color: white;
            color: #212529;
            border: 1px solid #ced4da;
        }}

        QMessageBox QPushButton:hover {{
            background-color: #e9ecef;
        }}
        """)


# ============================================================
# TEMA OSCURO
# ============================================================


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
            background: transparent;
        }}

        QLabel#tituloPrincipal {{
            color: #eeeeee;
            font-size: 23px;
            font-weight: bold;
            background: transparent;
        }}

        QLabel#subtituloPrincipal {{
            color: #aaaaaa;
            background: transparent;
        }}

        QLabel#estadoArchivo {{
            color: #aaaaaa;
            background: transparent;
        }}

        QFrame#infoConfiguracion {{
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 5px;
        }}

        QLabel#tituloConfiguracion {{
            color: #eeeeee;
            font-weight: bold;
            background: transparent;
            border: none;
        }}

        QLabel#descripcionConfiguracion {{
            color: #aaaaaa;
            background: transparent;
            border: none;
        }}

        QLabel#etiquetaGenerar,
        QLabel#etiquetaResultado {{
            color: #eeeeee;
            font-weight: bold;
            background: transparent;
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

        QPushButton:pressed {{
            background-color: #444444;
        }}

        QPushButton:disabled {{
            background-color: #333333;
            color: #777777;
        }}

        QTextEdit {{
            background-color: #1e1e1e;
            color: #eeeeee;
            border: 1px solid #444444;
            border-radius: 3px;
            padding: 5px;
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
            border: 1px solid #333333;
        }}

        QTableCornerButton::section {{
            background-color: #000000;
            border: 1px solid #333333;
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

        QScrollBar::handle:vertical:hover {{
            background: #666666;
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
        """)


# ============================================================
# VENTANA PRINCIPAL
# ============================================================


class GeneradorEventos(QMainWindow):

    def __init__(self):

        super().__init__()

        # ----------------------------------------------------
        # DATOS
        # ----------------------------------------------------

        self.eventos_cargados = []

        self.ruta_json_actual = ""

        # ----------------------------------------------------
        # CONFIGURACIÓN VENTANA
        # ----------------------------------------------------

        self.setWindowTitle("📅 Generador Masivo de Eventos")

        self.resize(1000, 600)

        self.setMinimumSize(800, 400)

        self.showMaximized()

        ruta_icono = Path(__file__).resolve().parent / "icono.png"

        if ruta_icono.exists():

            self.setWindowIcon(QIcon(str(ruta_icono)))
        # ----------------------------------------------------
        # COLORES DE LOS BOTONES
        # ----------------------------------------------------

        self.COLOR_PRIMARIO = "#2563eb"
        self.COLOR_GOOGLE = "#EA4335"
        self.COLOR_OUTLOOK = "#0072C6"
        self.COLOR_JSON = "#9333ea"

        # ----------------------------------------------------
        # CREAR INTERFAZ
        # ----------------------------------------------------

        self.crear_interfaz()

    # ========================================================
    # CREAR INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        # ----------------------------------------------------
        # WIDGET CENTRAL
        # ----------------------------------------------------

        central = QWidget()

        self.setCentralWidget(central)

        # ----------------------------------------------------
        # LAYOUT PRINCIPAL
        # ----------------------------------------------------

        main = QVBoxLayout(central)

        main.setContentsMargins(35, 25, 35, 25)

        main.setSpacing(10)

        # ====================================================
        # ENCABEZADO
        # ====================================================

        titulo = QLabel("📅 Generador Masivo de Eventos")

        titulo.setObjectName("tituloPrincipal")

        main.addWidget(titulo)

        subtitulo = QLabel(
            "Carga un archivo JSON y genera eventos "
            "para Google Calendar, Outlook y .ics"
        )

        subtitulo.setObjectName("subtituloPrincipal")

        main.addWidget(subtitulo)

        # ====================================================
        # CARGAR JSON
        # ====================================================

        frame_json = QFrame()

        frame_json.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
            """)

        layout_json = QHBoxLayout(frame_json)

        layout_json.setContentsMargins(0, 10, 0, 5)

        layout_json.setSpacing(10)

        self.boton_json = QPushButton("📂 Cargar archivo JSON")

        self.boton_json.setStyleSheet(self.estilo_boton(self.COLOR_JSON))

        self.boton_json.clicked.connect(self.cargar_json)

        layout_json.addWidget(self.boton_json)

        self.label_estado = QLabel("Ningún archivo cargado.")

        self.label_estado.setObjectName("estadoArchivo")

        layout_json.addWidget(self.label_estado)

        layout_json.addStretch()

        main.addWidget(frame_json)

        # ====================================================
        # INFORMACIÓN CONFIGURACIÓN
        # ====================================================

        info = QFrame()

        info.setObjectName("infoConfiguracion")

        layout_info = QVBoxLayout(info)

        layout_info.setContentsMargins(15, 12, 15, 12)

        etiqueta_config = QLabel("⚙️ Configuración automática")

        etiqueta_config.setObjectName("tituloConfiguracion")

        layout_info.addWidget(etiqueta_config)

        descripcion_config = QLabel(
            "Título y descripción: "
            "⚠️🎓ENTREGA TAREA RAC CURSO⚠️   |   "
            "Fecha: FECHA ENTREGA   |   "
            "Inicio: 16:00   |   Fin: 22:00"
        )

        descripcion_config.setObjectName("descripcionConfiguracion")

        descripcion_config.setWordWrap(True)

        layout_info.addWidget(descripcion_config)

        main.addWidget(info)

        # ====================================================
        # GENERAR
        # ====================================================

        etiqueta_generar = QLabel("Generar:")

        etiqueta_generar.setObjectName("etiquetaGenerar")

        main.addWidget(etiqueta_generar)

        botones = QHBoxLayout()

        botones.setSpacing(8)

        # ----------------------------------------------------
        # ICS
        # ----------------------------------------------------

        boton_ics = QPushButton("📎 Crear .ics")

        boton_ics.setStyleSheet(self.estilo_boton(self.COLOR_PRIMARIO))

        boton_ics.clicked.connect(self.generar_archivo)

        botones.addWidget(boton_ics)

        # ----------------------------------------------------
        # GOOGLE
        # ----------------------------------------------------

        boton_google = QPushButton("🟠 URLs Google")

        boton_google.setStyleSheet(self.estilo_boton(self.COLOR_GOOGLE))

        boton_google.clicked.connect(self.generar_google_masivo)

        botones.addWidget(boton_google)

        # ----------------------------------------------------
        # OUTLOOK
        # ----------------------------------------------------

        boton_outlook = QPushButton("🟣 URLs Outlook")

        boton_outlook.setStyleSheet(self.estilo_boton(self.COLOR_OUTLOOK))

        boton_outlook.clicked.connect(self.generar_outlook_masivo)

        botones.addWidget(boton_outlook)

        # ----------------------------------------------------
        # TODO
        # ----------------------------------------------------

        boton_todo = QPushButton("✨ Generar todo")

        boton_todo.setStyleSheet(self.estilo_boton(self.COLOR_PRIMARIO))

        boton_todo.clicked.connect(self.generar_todo)

        botones.addWidget(boton_todo)

        botones.addStretch()

        main.addLayout(botones)

        # ====================================================
        # RESULTADO
        # ====================================================

        etiqueta_resultado = QLabel("Resultado:")

        etiqueta_resultado.setObjectName("etiquetaResultado")

        main.addWidget(etiqueta_resultado)

        self.text_resultado = QTextEdit()

        self.text_resultado.setReadOnly(True)

        # self.text_resultado.setFont(QFont("Consolas", 9))

        main.addWidget(self.text_resultado, 1)

        # ====================================================
        # BOTONES INFERIORES
        # ====================================================

        acciones = QHBoxLayout()

        acciones.setSpacing(5)

        # ----------------------------------------------------
        # COPIAR RESULTADO
        # ----------------------------------------------------

        boton_copiar = QPushButton("📋 Copiar resultado")

        boton_copiar.clicked.connect(self.copiar_resultado)

        acciones.addWidget(boton_copiar)

        # ----------------------------------------------------
        # COPIAR GOOGLE
        # ----------------------------------------------------

        boton_copiar_google = QPushButton("🟢 Copiar Google")

        boton_copiar_google.clicked.connect(self.copiar_google)

        acciones.addWidget(boton_copiar_google)

        # ----------------------------------------------------
        # COPIAR OUTLOOK
        # ----------------------------------------------------

        boton_copiar_outlook = QPushButton("🔵 Copiar Outlook")

        boton_copiar_outlook.clicked.connect(self.copiar_outlook)

        acciones.addWidget(boton_copiar_outlook)

        acciones.addStretch()

        # ----------------------------------------------------
        # LIMPIAR
        # ----------------------------------------------------

        boton_limpiar = QPushButton("🗑 Limpiar")

        boton_limpiar.clicked.connect(self.limpiar)

        acciones.addWidget(boton_limpiar)

        main.addLayout(acciones)

        # ====================================================
        # APLICAR TEMA
        # ====================================================

        if TEMA == "CLARO":

            aplicar_tema_claro(self)

        else:

            aplicar_tema_oscuro(self)

    # ========================================================
    # ESTILO BOTÓN
    # ========================================================

    def estilo_boton(self, color):

        colores_hover = {
            "#2563eb": "#1d4ed8",
            "#16a34a": "#15803d",
            "#0078d4": "#005a9e",
            "#9333ea": "#7e22ce",
        }

        hover = colores_hover.get(color, color)

        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {hover};
        }}

        QPushButton:pressed {{
            background-color: {hover};
        }}

        QPushButton:disabled {{
            background-color: #9ca3af;
            color: #e5e7eb;
        }}
        """

    # ========================================================
    # CARGAR JSON
    # ========================================================

    def cargar_json(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo JSON",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*.*)",
        )

        if not ruta:

            return

        try:

            with open(ruta, "r", encoding="utf-8") as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):

                raise ValueError(
                    "El archivo JSON debe contener " "una lista de eventos."
                )

            if len(datos) == 0:

                raise ValueError("El archivo JSON no contiene eventos.")

            # ------------------------------------------------
            # VALIDAR ESTRUCTURA
            # ------------------------------------------------

            campos_requeridos = ["TAREA", "RAC", "CURSO", "FECHA ENTREGA"]

            for numero, evento in enumerate(datos, start=1):

                if not isinstance(evento, dict):

                    raise ValueError(
                        f"El elemento #{numero} del JSON " "no es un objeto válido."
                    )

                for campo in campos_requeridos:

                    if campo not in evento:

                        raise ValueError(
                            f"El evento #{numero} no contiene " f'el campo "{campo}".'
                        )

            self.eventos_cargados = datos

            self.ruta_json_actual = ruta

            # ------------------------------------------------
            # MOSTRAR ESTADO
            # ------------------------------------------------

            self.label_estado.setText(os.path.basename(ruta))

            self.mostrar_resumen_json()

            QMessageBox.information(
                self,
                "JSON cargado",
                f"Se cargaron correctamente " f"{len(self.eventos_cargados)} eventos.",
            )

        except json.JSONDecodeError as error:

            QMessageBox.critical(
                self,
                "JSON inválido",
                "El archivo no contiene un JSON válido.\n\n" f"Detalle:\n{error}",
            )

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # CONVERTIR FECHA
    # ========================================================

    def convertir_fecha(self, fecha_texto):

        try:

            fecha = datetime.fromisoformat(fecha_texto)

            if fecha.tzinfo is None:

                fecha = fecha.replace(tzinfo=ZONA_HORARIA)

            else:

                fecha = fecha.astimezone(ZONA_HORARIA)

            return fecha

        except Exception:

            raise ValueError(f"Fecha inválida: {fecha_texto}")

    # ========================================================
    # CONSTRUIR TEXTO
    # ========================================================

    def construir_texto_evento(self, evento):

        tarea = str(evento.get("TAREA", "")).strip()

        rac = str(evento.get("RAC", "")).strip()

        curso = str(evento.get("CURSO", "")).strip()

        return f"⚠️🎓ENTREGA " f"{tarea} " f"{rac} " f"{curso}" f"⚠️"

    # ========================================================
    # CONSTRUIR DATOS
    # ========================================================

    def construir_datos_evento(self, evento):

        fecha_entrega = self.convertir_fecha(evento["FECHA ENTREGA"])

        fecha = fecha_entrega.date()

        hora_inicio = datetime.strptime(HORA_INICIO, "%H:%M").time()

        hora_fin = datetime.strptime(HORA_FIN, "%H:%M").time()

        inicio = datetime.combine(fecha, hora_inicio).replace(tzinfo=ZONA_HORARIA)

        fin = datetime.combine(fecha, hora_fin).replace(tzinfo=ZONA_HORARIA)

        texto = self.construir_texto_evento(evento)

        return {
            "titulo": texto,
            "inicio": inicio,
            "fin": fin,
            "lugar": "",
            "descripcion": texto,
            "original": evento,
        }

    # ========================================================
    # OBTENER EVENTOS
    # ========================================================

    def obtener_todos_los_eventos(self):

        if not self.eventos_cargados:

            raise ValueError("Primero debes cargar un archivo JSON.")

        eventos = []

        errores = []

        for numero, evento in enumerate(self.eventos_cargados, start=1):

            try:

                datos = self.construir_datos_evento(evento)

                eventos.append(datos)

            except Exception as error:

                errores.append(f"Evento #{numero}: {error}")

        if errores:

            detalle = "\n".join(errores[:10])

            if len(errores) > 10:

                detalle += f"\n... y " f"{len(errores) - 10} " "errores más."

            raise ValueError(
                "Se encontraron errores en algunos " "eventos:\n\n" + detalle
            )

        return eventos

    # ========================================================
    # ESCAPAR ICS
    # ========================================================

    def escapar_ics(self, texto):

        return (
            str(texto)
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace("\r\n", "\\n")
            .replace("\n", "\\n")
            .replace("\r", "\\n")
        )

    # ========================================================
    # GENERAR VEVENT
    # ========================================================

    def generar_vevent(self, datos):

        inicio_utc = datos["inicio"].astimezone(timezone.utc)

        fin_utc = datos["fin"].astimezone(timezone.utc)

        formato = "%Y%m%dT%H%M%SZ"

        uid = f"{uuid.uuid4()}" "@generador-eventos"

        dtstamp = datetime.now(timezone.utc).strftime(formato)

        contenido = (
            "BEGIN:VEVENT\r\n"
            f"UID:{uid}\r\n"
            f"DTSTAMP:{dtstamp}\r\n"
            f"DTSTART:{inicio_utc.strftime(formato)}\r\n"
            f"DTEND:{fin_utc.strftime(formato)}\r\n"
            f"SUMMARY:{self.escapar_ics(datos['titulo'])}\r\n"
            f"DESCRIPTION:{self.escapar_ics(datos['descripcion'])}\r\n"
            "END:VEVENT\r\n"
        )

        return contenido

    # ========================================================
    # GENERAR ICS
    # ========================================================

    def generar_ics_masivo(self, eventos, ruta):

        encabezado = (
            "BEGIN:VCALENDAR\r\n"
            "VERSION:2.0\r\n"
            "PRODID:-//Generador Masivo de Eventos//ES\r\n"
            "CALSCALE:GREGORIAN\r\n"
            "METHOD:PUBLISH\r\n"
            "X-WR-CALNAME:Entregas académicas\r\n"
        )

        contenido = encabezado

        for evento in eventos:

            contenido += self.generar_vevent(evento)

        contenido += "END:VCALENDAR\r\n"

        with open(ruta, "w", encoding="utf-8", newline="") as archivo:

            archivo.write(contenido)

    # ========================================================
    # GOOGLE
    # ========================================================

    def generar_url_google(self, datos):

        inicio_utc = datos["inicio"].astimezone(timezone.utc)

        fin_utc = datos["fin"].astimezone(timezone.utc)

        formato = "%Y%m%dT%H%M%SZ"

        return (
            "https://calendar.google.com/calendar/render"
            "?action=TEMPLATE"
            f"&text={quote(datos['titulo'])}"
            f"&dates="
            f"{inicio_utc.strftime(formato)}/"
            f"{fin_utc.strftime(formato)}"
            f"&details={quote(datos['descripcion'])}"
            f"&location={quote(datos['lugar'])}"
        )

    # ========================================================
    # OUTLOOK
    # ========================================================

    def generar_url_outlook(self, datos):

        inicio_utc = datos["inicio"].astimezone(timezone.utc)

        fin_utc = datos["fin"].astimezone(timezone.utc)

        formato = "%Y-%m-%dT%H:%M:%SZ"

        return (
            "https://outlook.live.com/calendar/0/deeplink/compose"
            f"?subject={quote(datos['titulo'])}"
            f"&startdt={inicio_utc.strftime(formato)}"
            f"&enddt={fin_utc.strftime(formato)}"
            f"&body={quote(datos['descripcion'])}"
            f"&location={quote(datos['lugar'])}"
        )

    # ========================================================
    # MOSTRAR RESULTADO
    # ========================================================

    def mostrar_resultado(self, texto):

        self.text_resultado.setPlainText(texto)

    # ========================================================
    # MOSTRAR RESUMEN
    # ========================================================

    def mostrar_resumen_json(self):

        if not self.eventos_cargados:

            self.mostrar_resultado("")

            return

        nombre_archivo = os.path.basename(self.ruta_json_actual)

        resultado = (
            "📂 ARCHIVO JSON CARGADO\n"
            "========================================\n\n"
            f"Archivo: {nombre_archivo}\n"
            f"Eventos encontrados: "
            f"{len(self.eventos_cargados)}\n\n"
            "Configuración de eventos:\n"
            f"• Hora inicio: {HORA_INICIO}\n"
            f"• Hora fin: {HORA_FIN}\n"
            "• Fecha: FECHA ENTREGA\n\n"
            "Los eventos están listos para ser generados."
        )

        self.mostrar_resultado(resultado)

    # ========================================================
    # CREAR ARCHIVO ICS
    # ========================================================

    def generar_archivo(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar eventos",
                "entregas_academicas.ics",
                "Archivo iCalendar (*.ics);;" "Todos los archivos (*.*)",
            )

            if not ruta:

                return

            self.generar_ics_masivo(eventos, ruta)

            resultado = (
                "📎 ARCHIVO .ICS CREADO\n"
                "========================================\n\n"
                f"Eventos generados: "
                f"{len(eventos)}\n\n"
                f"Archivo:\n{ruta}"
            )

            self.mostrar_resultado(resultado)

            QMessageBox.information(
                self,
                "Éxito",
                f"Se generaron {len(eventos)} " "eventos en el archivo .ics.",
            )

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # GOOGLE MASIVO
    # ========================================================

    def generar_google_masivo(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            resultado = (
                "🟢 GOOGLE CALENDAR\n" "========================================\n\n"
            )

            for numero, evento in enumerate(eventos, start=1):

                url = self.generar_url_google(evento)

                resultado += (
                    f"EVENTO {numero}\n"
                    "----------------------------------------\n"
                    f"{evento['titulo']}\n\n"
                    f"{url}\n\n"
                )

            self.mostrar_resultado(resultado)

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # OUTLOOK MASIVO
    # ========================================================

    def generar_outlook_masivo(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            resultado = "🔵 OUTLOOK\n" "========================================\n\n"

            for numero, evento in enumerate(eventos, start=1):

                url = self.generar_url_outlook(evento)

                resultado += (
                    f"EVENTO {numero}\n"
                    "----------------------------------------\n"
                    f"{evento['titulo']}\n\n"
                    f"{url}\n\n"
                )

            self.mostrar_resultado(resultado)

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # GENERAR TODO
    # ========================================================

    def generar_todo(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar eventos .ics",
                "entregas_academicas.ics",
                "Archivo iCalendar (*.ics);;" "Todos los archivos (*.*)",
            )

            if ruta:

                self.generar_ics_masivo(eventos, ruta)

            resultado = (
                "✨ GENERACIÓN COMPLETA\n"
                "========================================\n\n"
                f"Total de eventos: "
                f"{len(eventos)}\n\n"
            )

            if ruta:

                resultado += (
                    "📎 ARCHIVO ICS\n"
                    "----------------------------------------\n"
                    f"{ruta}\n\n"
                )

            resultado += (
                "🟢 GOOGLE CALENDAR\n"
                "----------------------------------------\n"
                "Se generaron las URLs individuales "
                "para todos los eventos.\n\n"
            )

            for numero, evento in enumerate(eventos, start=1):

                resultado += (
                    f"EVENTO {numero}\n"
                    f"{evento['titulo']}\n"
                    f"{self.generar_url_google(evento)}\n\n"
                )

            resultado += (
                "\n🔵 OUTLOOK\n"
                "----------------------------------------\n"
                "Se generaron las URLs individuales "
                "para todos los eventos.\n\n"
            )

            for numero, evento in enumerate(eventos, start=1):

                resultado += (
                    f"EVENTO {numero}\n"
                    f"{evento['titulo']}\n"
                    f"{self.generar_url_outlook(evento)}\n\n"
                )

            self.mostrar_resultado(resultado)

            QMessageBox.information(
                self, "Éxito", f"Se procesaron {len(eventos)} eventos."
            )

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # COPIAR RESULTADO
    # ========================================================

    def copiar_resultado(self):

        texto = self.text_resultado.toPlainText().strip()

        if not texto:

            QMessageBox.warning(
                self, "Sin contenido", "No hay ningún resultado para copiar."
            )

            return

        QApplication.clipboard().setText(texto)

        QMessageBox.information(self, "Copiado", "Contenido copiado al portapapeles.")

    # ========================================================
    # COPIAR GOOGLE
    # ========================================================

    def copiar_google(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            texto = ""

            for numero, evento in enumerate(eventos, start=1):

                texto += (
                    f"EVENTO {numero}\n"
                    f"{evento['titulo']}\n"
                    f"{self.generar_url_google(evento)}\n\n"
                )

            QApplication.clipboard().setText(texto)

            self.mostrar_resultado(texto)

            QMessageBox.information(
                self,
                "Copiado",
                f"Se copiaron {len(eventos)} " "URLs de Google Calendar.",
            )

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # COPIAR OUTLOOK
    # ========================================================

    def copiar_outlook(self):

        try:

            eventos = self.obtener_todos_los_eventos()

            texto = ""

            for numero, evento in enumerate(eventos, start=1):

                texto += (
                    f"EVENTO {numero}\n"
                    f"{evento['titulo']}\n"
                    f"{self.generar_url_outlook(evento)}\n\n"
                )

            QApplication.clipboard().setText(texto)

            self.mostrar_resultado(texto)

            QMessageBox.information(
                self, "Copiado", f"Se copiaron {len(eventos)} " "URLs de Outlook."
            )

        except Exception as error:

            QMessageBox.critical(self, "Error", str(error))

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        self.eventos_cargados = []

        self.ruta_json_actual = ""

        self.label_estado.setText("Ningún archivo cargado.")

        self.mostrar_resultado("No hay ningún archivo JSON cargado.")


# ============================================================
# INICIAR APLICACIÓN
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = GeneradorEventos()

    ventana.show()

    sys.exit(app.exec())
