# 🎛️ AudioPro v1.7 - Reaper Edition

> **Procesamiento Profesional de Audio con Reaper + Waves**

Esta es la versión profesional de AudioPro que integra Reaper DAW para procesamiento de audio de nivel profesional usando plugins Waves.

---

## 🚀 Inicio Rápido

### Comando Simple:

```bash
streamlit run app.py
```

### O usa el script batch (Windows):

```bash
start.bat
```

---

## ✨ Características v1.7

- 🎛️ **Integración con Reaper DAW** - Procesamiento profesional
- 🎚️ **Plugins Waves** - Calidad de estudio
- 🤖 **Audio Isolation** - ElevenLabs para separación de voz
- 📤 **3 Fuentes de Entrada**:
  - Subida manual de archivos
  - Links de Google Drive
  - Rutas locales/NAS
- 🎨 **Tema Platzi** - Interfaz moderna y atractiva
- 💾 **Sesiones Guardadas** - Para edición posterior en Reaper

---

## 📋 Requisitos Previos

### 1. Software Requerido

✅ **Python 3.9+**
```bash
python --version
```

✅ **FFmpeg** (instalado y en PATH)
```bash
ffmpeg -version
```

✅ **Reaper DAW**
- Descargar: https://www.reaper.fm/
- Instalado en: `C:\Program Files\REAPER (x64)\`

✅ **Plugins Waves**
- Configurados en el template de Reaper

### 2. Configuración de Rutas

El archivo `app.py` usa estas rutas por defecto:

```python
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\CURSOS\2025\Q3"
```

**⚠️ IMPORTANTE:** Edita `app.py` (líneas 31-33) si tus rutas son diferentes.

### 3. API de ElevenLabs

Crea el archivo `.streamlit/secrets.toml`:

```toml
[elevenlabs]
api_key = "tu_api_key_aqui"
base_url = "https://api.elevenlabs.io/v1"
```

---

## 📦 Instalación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar FFmpeg (si no está instalado)

```bash
python setup_ffmpeg.py
```

### 3. Verificar Reaper

```bash
# Verificar ejecutable
dir "C:\Program Files\REAPER (x64)\reaper.exe"

# Verificar template
dir "F:\00\00 Reaper\00 Voces.rpp"
```

---

## ▶️ Ejecución

### Método 1: Comando Python

```bash
streamlit run app.py
```

### Método 2: Script Batch (Windows)

```bash
start.bat
```

La aplicación se abrirá en tu navegador predeterminado (usualmente en `http://localhost:8501`).

---

## 🎯 Flujo de Trabajo

### Paso a Paso:

1. **📁 Seleccionar Fuente**
   - Sube archivos manualmente, O
   - Pega link de Google Drive, O
   - Ingresa ruta local/NAS

2. **🎵 Extracción Automática**
   - FFmpeg extrae el audio del video

3. **🤖 Audio Isolation**
   - ElevenLabs separa la voz del ruido

4. **🎛️ Procesamiento en Reaper**
   - Crea sesión automáticamente
   - Aplica plugins Waves
   - Renderiza el audio procesado

5. **🎬 Resultado Final**
   - Combina audio con video original
   - Guarda en carpeta `procesados/`

### Diagrama de Flujo:

```
📤 Upload/Drive/NAS
        ↓
🎵 Extracción Audio (FFmpeg)
        ↓
🤖 Audio Isolation (ElevenLabs)
        ↓
🎛️ Sesión Reaper Automática
        ↓
🎚️ Procesamiento Plugins Waves
        ↓
⚙️ Render Automático
        ↓
🎬 Mux con Video Original
        ↓
✅ Archivo Procesado
```

---

## 📂 Estructura del Proyecto

```
Audiopro 1.7/
│
├── app.py                  # 🎛️ Aplicación principal
├── streamlit_config.py     # 🎨 Configuración tema Platzi
├── setup_ffmpeg.py         # ⚙️ Setup de FFmpeg
│
├── requirements.txt        # 📋 Dependencias Python
├── README.md              # 📖 Este archivo
├── README_v17.md          # 📖 Documentación técnica
├── QUICK_START_v17.md     # 🚀 Guía rápida
│
├── start.bat              # 🚀 Script de inicio
│
└── .streamlit/
    └── secrets.toml       # 🔐 API Keys (crear manualmente)
```

---

## 🛠️ Configuración Avanzada

### Personalizar Rutas de Reaper

Edita `app.py` líneas 31-33:

```python
REAPER_EXE = r"TU_RUTA\reaper.exe"
REAPER_TEMPLATE = r"TU_RUTA\template.rpp"
REAPER_SESSIONS_DIR = r"TU_RUTA\sesiones"
```

### Ajustar Workers

Edita `app.py` línea 37 para cambiar procesamiento paralelo:

```python
MAX_WORKERS = 2  # Aumenta según tu CPU
```

### Modificar Template de Reaper

1. Abre tu template en Reaper
2. Ajusta plugins y configuración
3. Guarda cambios
4. Reinicia AudioPro

---

## 🐛 Solución de Problemas

### ❌ Error: "Reaper no encontrado"

**Solución:**
```python
# Edita app.py línea 31
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
```

### ❌ Error: "Template no encontrado"

**Solución:**
```python
# Edita app.py línea 32
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
```

### ❌ Error: "Render falla"

**Causas posibles:**
- Plugins Waves no instalados
- Template corrupto
- Permisos insuficientes

**Solución:**
1. Verifica plugins en Reaper
2. Abre template manualmente
3. Verifica permisos de directorios

### ❌ Error: "ElevenLabs API"

**Solución:**
1. Verifica `.streamlit/secrets.toml`
2. Confirma API key válida
3. Revisa conexión a internet

---

## 💡 Tips Profesionales

### 1. Optimización de Template

- Guarda presets de plugins favoritos
- Ajusta cadena de procesamiento
- Configura render a 48kHz, 16-bit

### 2. Batch Processing

- Usa tab "Desde NAS/Local"
- Procesa múltiples archivos
- Los archivos se procesan en paralelo

### 3. Edición Manual

Las sesiones se guardan en:
```
F:\CURSOS\2025\Q3\[nombre_archivo]_[timestamp]\
```

Puedes:
- Abrir en Reaper manualmente
- Modificar y re-renderizar
- Guardar como nuevo template

### 4. Performance

- Cierra otros programas durante render
- Usa SSD para mejor velocidad
- Ajusta MAX_WORKERS según CPU

---

## 📊 Comparación con v1.6

| Característica | v1.6 | v1.7 (Esta versión) |
|---------------|------|---------------------|
| Procesamiento | FFmpeg básico | Reaper + Waves Pro |
| Calidad | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Velocidad | Rápido | Medio |
| Setup | Simple | Avanzado |
| Plugins | Filtros básicos | Waves profesionales |
| Edición Manual | ❌ | ✅ (sesiones Reaper) |
| Streamlit Cloud | ✅ | ❌ (solo local) |

---

## 📚 Documentación Adicional

- 📖 **README_v17.md** - Documentación técnica completa
- 🚀 **QUICK_START_v17.md** - Guía de inicio rápido y comparaciones

---

## 🔗 Recursos Externos

- 🎛️ [Reaper DAW](https://www.reaper.fm/)
- 🔊 [Waves Plugins](https://www.waves.com/)
- 🤖 [ElevenLabs](https://elevenlabs.io/)
- 🎨 [Platzi](https://platzi.com/)
- 📦 [Repositorio GitHub](https://github.com/Andresporahi/procesamientoaudio)

---

## ⚠️ Notas Importantes

1. **Solo Local** - Esta versión requiere Reaper instalado localmente
2. **No Streamlit Cloud** - No compatible con despliegue en la nube
3. **API Key** - Requiere cuenta de ElevenLabs
4. **Espacio en Disco** - Las sesiones ocupan espacio considerable
5. **Tiempo de Proceso** - Puede tomar 3-5 minutos por archivo

---

## 🎉 ¡Listo para Usar!

### Comando de Inicio:

```bash
streamlit run app.py
```

O simplemente:

```bash
start.bat
```

---

<div align="center">

**AudioPro v1.7 - Reaper Edition**

*Procesamiento profesional de audio al alcance de un click* 🎛️

</div>
