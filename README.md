# 🚀 Aplicación de Escritorio con Control de Estudio

> 🟢 **IMPORTANTE:** Antes de ejecutar la aplicación, debes instalar **TODAS las dependencias necesarias**.
> ⚠️ **No ejecutes la aplicación antes de completar estos pasos.**

---

## 🧰 1. Requisitos previos

Asegúrate de tener instalado:

* 🐍 Python 3.10 o superior
* 📦 pip
* 💻 Windows, Linux o macOS

Comprueba que Python está instalado:

```bash
python --version
```

En algunos sistemas puede ser necesario:

```bash
python3 --version
```

Comprueba `pip`:

```bash
pip --version
```

o:

```bash
pip3 --version
```

---

# 🔥 2. Instalar las dependencias

La aplicación utiliza los siguientes módulos externos:

| 📦 Módulo        | 🎯 Uso                                   |
| ---------------- | ---------------------------------------- |
| `PySide6`        | 🖥️ Interfaz gráfica                     |
| `pandas`         | 📊 Procesamiento de datos                |
| `beautifulsoup4` | 🌐 Procesamiento de HTML                 |
| `tkcalendar`     | 📅 Calendarios y selección de fechas     |
| `openpyxl`       | 📗 Lectura y escritura de archivos Excel |

### ⚡ Instalación rápida

Ejecuta:

```bash
pip install PySide6 pandas beautifulsoup4 tkcalendar openpyxl
```

Si tu sistema utiliza `pip3`:

```bash
pip3 install PySide6 pandas beautifulsoup4 tkcalendar openpyxl
```

### 🐍 Instalación recomendada usando Python

```bash
python -m pip install --upgrade pip
python -m pip install PySide6 pandas beautifulsoup4 tkcalendar openpyxl
```

---

# 🧪 3. Verificar que los módulos estén instalados

⚠️ **Este paso es obligatorio antes de ejecutar la aplicación.**

Puedes comprobar todos los módulos de una sola vez:

```bash
python -c "import PySide6, pandas, bs4, tkcalendar, openpyxl; print('✅ Todas las dependencias están instaladas correctamente')"
```

Si todo está correcto, deberías obtener:

```text
✅ Todas las dependencias están instaladas correctamente
```

---

## 🔍 4. Verificar cada dependencia individualmente

### 🖥️ PySide6

```bash
python -c "import PySide6; print('✅ PySide6:', PySide6.__version__)"
```

### 📊 Pandas

```bash
python -c "import pandas as pd; print('✅ pandas:', pd.__version__)"
```

### 🌐 BeautifulSoup

```bash
python -c "from bs4 import BeautifulSoup; print('✅ BeautifulSoup está instalado correctamente')"
```

### 📅 tkcalendar

```bash
python -c "import tkcalendar; print('✅ tkcalendar está instalado correctamente')"
```

### 📗 openpyxl

```bash
python -c "import openpyxl; print('✅ openpyxl:', openpyxl.__version__)"
```

---

# 📋 5. Comprobar las dependencias con `pip`

También puedes consultar los paquetes instalados:

```bash
pip list
```

O buscar específicamente:

```bash
pip show PySide6
pip show pandas
pip show beautifulsoup4
pip show tkcalendar
pip show openpyxl
```

Deberías encontrar información similar a:

```text
Name: PySide6
Version: ...

Name: pandas
Version: ...

Name: beautifulsoup4
Version: ...

Name: tkcalendar
Version: ...

Name: openpyxl
Version: ...
```

---

# 🛡️ 6. Recomendado: utilizar un entorno virtual

Para evitar conflictos con otros proyectos de Python, se recomienda crear un entorno virtual.

### 1️⃣ Crear el entorno

```bash
python -m venv .venv
```

### 2️⃣ Activarlo en Windows

```bash
.venv\Scripts\activate
```

### 3️⃣ Activarlo en Linux/macOS

```bash
source .venv/bin/activate
```

Cuando esté activo, normalmente aparecerá algo parecido a:

```text
(.venv) C:\mi-proyecto>
```

### 4️⃣ Instalar las dependencias

```bash
python -m pip install --upgrade pip
python -m pip install PySide6 pandas beautifulsoup4 tkcalendar openpyxl
```

---

# 🚀 7. Ejecutar la aplicación

Una vez instaladas y verificadas **todas las dependencias**:

```bash
python nombre_de_tu_aplicacion.py
```

Por ejemplo:

```bash
python main.py
```

---

# 🧭 8. Flujo recomendado

Sigue **exactamente** este orden:

```text
🐍 Python instalado
        ↓
📦 pip disponible
        ↓
🛡️ Crear entorno virtual (recomendado)
        ↓
⬇️ Instalar dependencias
        ↓
🧪 Verificar módulos
        ↓
✅ Dependencias OK
        ↓
🚀 Aplicación lista
```

---

# ⚠️ 9. Si aparece `ModuleNotFoundError`

Si aparece un error como:

```text
ModuleNotFoundError: No module named 'pandas'
```

significa que falta una dependencia.

Instálala con:

```bash
python -m pip install pandas
```

Para PySide6:

```bash
python -m pip install PySide6
```

Para BeautifulSoup:

```bash
python -m pip install beautifulsoup4
```

Para tkcalendar:

```bash
python -m pip install tkcalendar
```

Para openpyxl:

```bash
python -m pip install openpyxl
```

Después vuelve a ejecutar la verificación:

```bash
python -c "import PySide6, pandas, bs4, tkcalendar, openpyxl; print('✅ Todas las dependencias están instaladas correctamente')"
```

---

# 📦 10. Dependencias externas utilizadas

La aplicación utiliza los siguientes módulos externos que **sí necesitan instalación**:

```text
PySide6
pandas
beautifulsoup4
tkcalendar
openpyxl
```

También utiliza módulos de la biblioteca estándar de Python que **NO necesitan instalación adicional**, entre ellos:

```text
sys
json
subprocess
uuid
pathlib
datetime
os
re
zoneinfo
urllib.parse
```

Estos módulos forman parte de Python.

### ✅ Solo necesitas instalar:

```text
PySide6
pandas
beautifulsoup4
tkcalendar
openpyxl
```

---

# 🟢 11. Comando completo de instalación

Si quieres realizar la instalación de una sola vez:

```bash
python -m pip install --upgrade pip
python -m pip install PySide6 pandas beautifulsoup4 tkcalendar openpyxl
```

Después verifica:

```bash
python -c "import PySide6, pandas, bs4, tkcalendar, openpyxl; print('✅ INSTALACIÓN COMPLETADA CORRECTAMENTE')"
```

Finalmente ejecuta:

```bash
python main.py
```

---

# 🎯 Checklist antes de ejecutar

* [ ] 🐍 Python está instalado
* [ ] 📦 `pip` está disponible
* [ ] 🛡️ El entorno virtual está activado, si se utiliza
* [ ] 🖥️ `PySide6` está instalado
* [ ] 📊 `pandas` está instalado
* [ ] 🌐 `beautifulsoup4` está instalado
* [ ] 📅 `tkcalendar` está instalado
* [ ] 📗 `openpyxl` está instalado
* [ ] 🧪 Las dependencias fueron verificadas
* [ ] ✅ No aparecen errores `ModuleNotFoundError`
* [ ] 🚀 La aplicación está lista para ejecutarse

---

## 💡 Comando de verificación final

> 🟢 **Si este comando termina correctamente, puedes ejecutar la aplicación.**

```bash
python -c "import PySide6, pandas, bs4, tkcalendar, openpyxl; print('''
╔══════════════════════════════════════════╗
║       ✅ DEPENDENCIAS CORRECTAS          ║
║                                          ║
║  🖥️  PySide6          → OK              ║
║  📊  pandas           → OK              ║
║  🌐  BeautifulSoup    → OK              ║
║  📅  tkcalendar       → OK              ║
║  📗  openpyxl         → OK              ║
║                                          ║
║       🚀 APLICACIÓN LISTA               ║
╚══════════════════════════════════════════╝
''')"
```

## 🚀 ¡Listo!

Una vez completados todos los pasos anteriores, la aplicación está preparada para ejecutarse correctamente.

**⚠️ No omitas la instalación y verificación de dependencias.**

---

# 🖥️ Capturas de pantalla

A continuación se muestran algunas de las principales funcionalidades de la aplicación **Gestor de actividades académicas**.

## 🏠 Pantalla principal

La aplicación cuenta con una interfaz gráfica para gestionar, crear, consultar, filtrar y editar las actividades académicas.

---

![Pantalla principal 01](https://i.imgur.com/Ox3pHor.jpeg)

---

![Pantalla principal 02](https://i.imgur.com/wIjKxPx.jpeg)

---

## 📋 Detalle de actividad

![Detalle actividad](https://i.imgur.com/PkRbYIC.jpeg)

---

## 🆕 Nueva actividad

![Nuevo actividad](https://i.imgur.com/5WVnZxC.jpeg)

---

## 📝 Editar actividad

![Editar actividad](https://i.imgur.com/OST7xJB.jpeg)

---

## 🗑️ Eliminar actividad

![Eliminar actividad](https://i.imgur.com/XelCCHa.jpeg)

---

## 📂 Cargar datos

Desde el botón **"Cargar datos"** es posible cargar la información académica almacenada en archivos JSON.

---

![Cargar datos 01](https://i.imgur.com/U4S1HA0.jpeg)

---

![Cargar datos 02](https://i.imgur.com/7GJ2F2e.jpeg)

---

![Cargar datos 03](https://i.imgur.com/Dxw9Vlq.jpeg)

---

## 🔄 Unificación de datos

La aplicación también permite unificar información proveniente de diferentes archivos para facilitar la gestión centralizada de las actividades académicas.

---

![Unificación datos 01](https://i.imgur.com/g7nqL0V.jpeg)

---

![Unificación datos 02](https://i.imgur.com/Qbhmr78.jpeg)

---

![Unificación datos 03](https://i.imgur.com/kQDtTRz.jpeg)

---

![Unificación datos 04](https://i.imgur.com/Md1EmL9.jpeg)

---

## 📊 Exportar Excel → JSON

La aplicación permite seleccionar un archivo Excel y extraer automáticamente la información para convertirla al formato JSON utilizado por el sistema.

---

![Exportar Excel 01](https://i.imgur.com/DPf9J15.jpeg)

---

![Exportar Excel 02](https://i.imgur.com/biwglcV.jpeg)

---

![Exportar Excel 03](https://i.imgur.com/xTcNSLC.jpeg)

---

## 📅 Crear eventos de calendario

La aplicación incluye la función **"Crear Eventos"**, que permite generar eventos de calendario a partir de las actividades académicas registradas.

Esta funcionalidad facilita la organización de las actividades, permitiendo convertir las fechas y horarios de las actividades académicas en eventos de calendario.

---

![Crear eventos 01](https://i.imgur.com/bYVT7IL.jpeg)

---

![Crear eventos 02](https://i.imgur.com/EnIZICG.jpeg)

---

![Crear eventos 03](https://i.imgur.com/bHyogzP.jpeg)

---

![Crear eventos 04](https://i.imgur.com/ipVegAo.jpeg)

---

![Crear eventos 05](https://i.imgur.com/KVrR05J.jpeg)

---
##
