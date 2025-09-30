# ⚙️ Guía de Configuración - AudioPro v1.7

Esta guía te ayudará a configurar AudioPro v1.7 correctamente.

---

## 📋 Checklist de Configuración

### ✅ Paso 1: Verificar Python

```bash
python --version
```

**Requerido:** Python 3.9 o superior

Si no está instalado:
- Descargar: https://www.python.org/downloads/
- ⚠️ Marcar "Add Python to PATH" durante instalación

---

### ✅ Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Paquetes que se instalarán:**
- streamlit
- requests
- Pillow
- gdown (para Google Drive)
- Otros...

---

### ✅ Paso 3: Configurar FFmpeg

**Opción A: Script Automático**
```bash
python setup_ffmpeg.py
```

**Opción B: Manual**
1. Descargar: https://ffmpeg.org/download.html
2. Extraer a `C:\ffmpeg`
3. Agregar a PATH: `C:\ffmpeg\bin`

**Verificar instalación:**
```bash
ffmpeg -version
```

---

### ✅ Paso 4: Instalar Reaper

1. **Descargar Reaper:**
   - URL: https://www.reaper.fm/download.php
   - Versión recomendada: 7.x o superior

2. **Instalar en ruta predeterminada:**
   ```
   C:\Program Files\REAPER (x64)\
   ```

3. **Verificar instalación:**
   ```bash
   dir "C:\Program Files\REAPER (x64)\reaper.exe"
   ```

**⚠️ Si instalaste en otra ruta:**
- Edita `app.py` línea 31
- Cambia `REAPER_EXE` a tu ruta

---

### ✅ Paso 5: Configurar Template de Reaper

#### Opción A: Usar Template Existente

Si tienes el template en: `F:\00\00 Reaper\00 Voces.rpp`
- ✅ No necesitas hacer nada

Si está en otra ruta:
- Edita `app.py` línea 32
- Cambia `REAPER_TEMPLATE` a tu ruta

#### Opción B: Crear Nuevo Template

1. **Abre Reaper**

2. **Crea un nuevo proyecto**

3. **Agrega un Track de Audio**

4. **Agrega tus plugins Waves favoritos:**
   - Waves Restoration (ruido)
   - Waves Renaissance EQ (ecualización)
   - Waves Renaissance Compressor (dinámica)
   - Waves L2 Limiter (limitador)
   - Otros según preferencia

5. **Configura Render Settings:**
   - Menú: File > Render
   - Format: WAV
   - Sample Rate: 48000 Hz
   - Bit Depth: 16-bit
   - Guarda estos ajustes

6. **Guarda el proyecto como template:**
   ```
   File > Save Project As
   Nombre: 00 Voces.rpp
   Ubicación: F:\00\00 Reaper\
   ```

7. **Actualiza la ruta en app.py:**
   ```python
   REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
   ```

---

### ✅ Paso 6: Configurar Directorio de Sesiones

Por defecto las sesiones se guardan en:
```
F:\CURSOS\2025\Q3
```

**Para cambiar la ruta:**

1. Edita `app.py` línea 33:
   ```python
   REAPER_SESSIONS_DIR = r"TU_RUTA_AQUI"
   ```

2. Crea el directorio manualmente:
   ```bash
   mkdir "F:\CURSOS\2025\Q3"
   ```

---

### ✅ Paso 7: Configurar ElevenLabs API

1. **Obtener API Key:**
   - Visita: https://elevenlabs.io/
   - Crea cuenta o inicia sesión
   - Ve a: Settings > API Keys
   - Copia tu API key

2. **Crear archivo de configuración:**
   ```bash
   # En: .streamlit\secrets.toml
   ```

3. **Agregar configuración:**
   ```toml
   [elevenlabs]
   api_key = "tu_api_key_real_aqui"
   base_url = "https://api.elevenlabs.io/v1"
   ```

4. **Archivo de ejemplo:**
   - Renombra `.streamlit\secrets.toml.example`
   - Quita el `.example`
   - Agrega tu API key

**⚠️ Importante:**
- No compartas este archivo
- No lo subas a GitHub
- Ya está en `.gitignore`

---

## 🔧 Configuración Avanzada

### Ajustar Workers (Procesamiento Paralelo)

Edita `app.py` línea 37:

```python
MAX_WORKERS = 2  # Cambia según tu CPU
```

**Recomendaciones:**
- CPU 4 cores → `MAX_WORKERS = 2`
- CPU 8 cores → `MAX_WORKERS = 4`
- CPU 16 cores → `MAX_WORKERS = 6`

---

### Cambiar Límite de Tamaño de Archivo

Edita `app.py` línea 36:

```python
MAX_FILE_MB = 800  # Cambia a tu límite en MB
```

---

### Personalizar Tema Visual

El tema Platzi está en `streamlit_config.py`

Para cambiar colores, edita las variables CSS:
```python
--platzi-green: #98CA3F;
--platzi-blue: #121F3D;
# etc...
```

---

## 🗂️ Resumen de Rutas Configurables

| Configuración | Archivo | Línea | Valor por Defecto |
|--------------|---------|-------|-------------------|
| Reaper EXE | app.py | 31 | `C:\Program Files\REAPER (x64)\reaper.exe` |
| Template | app.py | 32 | `F:\00\00 Reaper\00 Voces.rpp` |
| Sesiones | app.py | 33 | `F:\CURSOS\2025\Q3` |
| Max Workers | app.py | 37 | `2` |
| Max File MB | app.py | 36 | `800` |
| ElevenLabs | .streamlit/secrets.toml | - | Manual |

---

## ✅ Verificación Final

Ejecuta este checklist antes de usar:

- [ ] Python 3.9+ instalado
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] FFmpeg instalado y en PATH
- [ ] Reaper instalado
- [ ] Template de Reaper existe
- [ ] Directorio de sesiones creado
- [ ] API key de ElevenLabs configurada
- [ ] Todas las rutas verificadas en app.py

---

## 🚀 Prueba de Funcionamiento

### 1. Iniciar la aplicación:
```bash
streamlit run app.py
```

### 2. Subir un archivo de prueba pequeño (ej: 1 minuto)

### 3. Verificar que:
- ✅ Se extrae el audio
- ✅ ElevenLabs procesa (si está configurado)
- ✅ Reaper crea la sesión
- ✅ Se renderiza correctamente
- ✅ Se genera el archivo final

---

## 🐛 Problemas Comunes

### Error: "ModuleNotFoundError"
**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "FFmpeg not found"
**Solución:**
```bash
python setup_ffmpeg.py
# O instala manualmente y agrega a PATH
```

### Error: "Reaper not found"
**Solución:**
- Verifica ruta de instalación
- Edita `app.py` línea 31

### Error: "Template not found"
**Solución:**
- Verifica que el archivo existe
- Edita `app.py` línea 32

### Error: "ElevenLabs API"
**Solución:**
- Verifica `.streamlit/secrets.toml`
- Confirma API key válida
- Revisa conexión a internet

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs** en la terminal
2. **Verifica todas las rutas** en app.py
3. **Confirma instalaciones** (Python, FFmpeg, Reaper)
4. **Revisa la documentación:**
   - README.md
   - README_v17.md
   - QUICK_START_v17.md

---

## ✨ ¡Listo!

Una vez completada toda la configuración:

```bash
# Usa el script de inicio
start.bat

# O directamente
streamlit run app.py
```

**¡Disfruta de AudioPro v1.7!** 🎛️
