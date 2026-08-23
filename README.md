# # 🚀 Aplicación de Escritorio con Control de Estudio

> 🟢 **IMPORTANTE:** Antes de ejecutar la aplicación, debes instalar **TODAS las dependencias necesarias**.
> ⚠️ **No ejecutes la aplicación antes de completar estos pasos.**

---

## 🧰 1. Requisitos previos

Asegúrate de tener instalado:

* 🐍 **Python 3.10 o superior**
* 📦 **pip**
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

| 📦 Módulo        | 🎯 Uso                    |
| ---------------- | ------------------------- |
| `PySide6`        | 🖥️ Interfaz gráfica      |
| `pandas`         | 📊 Procesamiento de datos |
| `beautifulsoup4` | 🌐 Procesamiento de HTML  |

### ⚡ Instalación rápida

Ejecuta:

```bash
pip install PySide6 pandas beautifulsoup4
```

Si tu sistema utiliza `pip3`:

```bash
pip3 install PySide6 pandas beautifulsoup4
```

### 🐍 Instalación recomendada usando Python

```bash
python -m pip install --upgrade pip
python -m pip install PySide6 pandas beautifulsoup4
```

---

# 🧪 3. Verificar que los módulos estén instalados

⚠️ **Este paso es obligatorio antes de ejecutar la aplicación.**

Puedes comprobar todos los módulos de una sola vez:

```bash
python -c "import PySide6, pandas, bs4; print('✅ Todas las dependencias están instaladas correctamente')"
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
```

Deberías encontrar información similar a:

```text
Name: PySide6
Version: ...

Name: pandas
Version: ...

Name: beautifulsoup4
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
python -m pip install PySide6 pandas beautifulsoup4
```

---

# 🚀 7. Ejecutar la aplicación

Una vez instaladas y verificadas las dependencias:

```bash
python nombre_de_tu_aplicacion.py
```

Por ejemplo:

```bash
python main.py
```

---

# 🧭 8. Flujo recomendado

Sigue **exactamente este orden**:

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
🚀 Ejecutar aplicación
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

Después vuelve a ejecutar la verificación:

```bash
python -c "import PySide6, pandas, bs4; print('✅ Todas las dependencias están instaladas correctamente')"
```

---

# 📦 10. Dependencias externas utilizadas

La aplicación utiliza módulos de la biblioteca estándar de Python que **NO necesitan instalación adicional**, entre ellos:

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
```

---

# 🟢 11. Comando completo de instalación

Si quieres realizar la instalación de una sola vez:

```bash
python -m pip install --upgrade pip
python -m pip install PySide6 pandas beautifulsoup4
```

Después verifica:

```bash
python -c "import PySide6, pandas, bs4; print('✅ INSTALACIÓN COMPLETADA CORRECTAMENTE')"
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
* [ ] 🧪 Las dependencias fueron verificadas
* [ ] ✅ No aparecen errores `ModuleNotFoundError`
* [ ] 🚀 La aplicación está lista para ejecutarse

---

## 💡 Comando de verificación final

> 🟢 **Si este comando termina correctamente, puedes ejecutar la aplicación.**

```bash
python -c "import PySide6, pandas, bs4; print('''
╔══════════════════════════════════════════╗
║       ✅ DEPENDENCIAS CORRECTAS          ║
║                                          ║
║  🖥️  PySide6          → OK              ║
║  📊  pandas           → OK              ║
║  🌐  BeautifulSoup    → OK              ║
║                                          ║
║       🚀 APLICACIÓN LISTA               ║
╚══════════════════════════════════════════╝
''')"
```

# 🚀 ¡Listo!

Una vez completados todos los pasos anteriores, la aplicación está preparada para ejecutarse correctamente.

**⚠️ No omitas la instalación y verificación de dependencias.**
