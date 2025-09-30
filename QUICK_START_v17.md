# 🚀 Inicio Rápido - AudioPro v1.7

## 📦 Versiones Disponibles

### ✅ v1.6.1 - Versión Estable (Streamlit Cloud)
```bash
streamlit run app.py
```
- ✨ Procesamiento con FFmpeg
- 🎨 Tema Platzi
- 📤 3 fuentes: Upload, Drive, NAS
- ☁️ Compatible con Streamlit Cloud

### 🎛️ v1.7.0 - Reaper Edition (Solo Local)
```bash
streamlit run app_v17_reaper.py
```
- ✨ Procesamiento profesional con Reaper
- 🎚️ Plugins Waves incluidos
- 🤖 Audio Isolation con ElevenLabs
- 📤 3 fuentes: Upload, Drive, NAS
- 💻 **SOLO LOCAL** (requiere Reaper instalado)

---

## 🎯 ¿Cuál versión usar?

### Usa v1.6.1 si:
- ✅ Quieres procesamiento rápido
- ✅ Usas Streamlit Cloud
- ✅ No tienes Reaper instalado
- ✅ Procesamiento básico es suficiente

### Usa v1.7.0 si:
- ✅ Necesitas calidad profesional
- ✅ Tienes Reaper instalado
- ✅ Tienes plugins Waves
- ✅ Ejecutas en local
- ✅ Puedes esperar más tiempo de procesamiento

---

## ⚙️ Requisitos v1.7.0

### 1. Software Requerido

**Reaper DAW**
- Descargar: https://www.reaper.fm/
- Instalado en: `C:\Program Files\REAPER (x64)\`

**Plugins Waves** (configurados en template)
- Waves Restoration
- Waves Renaissance EQ
- Waves Renaissance Compressor
- Waves L2 Limiter
- (Otros según tu template)

**Python 3.9+**
```bash
python --version
```

**FFmpeg**
```bash
ffmpeg -version
```

### 2. Configuración de Rutas

Edita `app_v17_reaper.py` si tus rutas son diferentes:

```python
# Líneas 31-33
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\CURSOS\2025\Q3"
```

### 3. API de ElevenLabs

Crea `.streamlit/secrets.toml`:

```toml
[elevenlabs]
api_key = "tu_api_key_aqui"
base_url = "https://api.elevenlabs.io/v1"
```

---

## 🚀 Instalación

### 1. Clonar Repositorio

```bash
git clone https://github.com/Andresporahi/procesamientoaudio.git
cd Audiopro
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar FFmpeg (si no está instalado)

```bash
python setup_ffmpeg.py
```

### 4. Verificar Reaper (solo v1.7)

```bash
# Verificar que existe:
dir "C:\Program Files\REAPER (x64)\reaper.exe"

# Verificar template:
dir "F:\00\00 Reaper\00 Voces.rpp"
```

---

## ▶️ Ejecución

### Versión 1.6.1 (Estable)

```bash
streamlit run app.py
```

### Versión 1.7.0 (Reaper)

```bash
streamlit run app_v17_reaper.py
```

O usa el script batch (Windows):
```bash
start_v17.bat
```

---

## 🎛️ Flujo de Trabajo v1.7

```
┌─────────────────┐
│  1. Seleccionar │
│     Fuente      │
│ (Upload/Drive/  │
│      NAS)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Extraer     │
│     Audio       │
│   (FFmpeg)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Audio       │
│   Isolation     │
│ (ElevenLabs)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Crear       │
│    Sesión       │
│   (Reaper)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Procesar    │
│    Plugins      │
│   (Waves)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. Render      │
│   (Reaper)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  7. Mux Final   │
│   (Video +      │
│    Audio)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ Archivo     │
│   Procesado     │
└─────────────────┘
```

---

## 📂 Estructura de Archivos

```
Audiopro/
│
├── app.py                  # v1.6.1 - Versión estable
├── app_v17_reaper.py       # v1.7.0 - Reaper Edition
│
├── streamlit_config.py     # Tema Platzi
├── setup_ffmpeg.py         # Configuración FFmpeg
│
├── requirements.txt        # Dependencias
├── README.md               # Documentación principal
├── README_v17.md           # Documentación v1.7
├── QUICK_START_v17.md      # Esta guía
│
└── .streamlit/
    └── secrets.toml        # API Keys
```

---

## 🔧 Solución de Problemas

### Error: "Reaper no encontrado"

**Solución:**
```python
# Edita app_v17_reaper.py línea 31
REAPER_EXE = r"TU_RUTA_A_REAPER\reaper.exe"
```

### Error: "Template no encontrado"

**Solución:**
```python
# Edita app_v17_reaper.py línea 32
REAPER_TEMPLATE = r"TU_RUTA_AL_TEMPLATE\00 Voces.rpp"
```

### Error: "Render falla"

**Causas posibles:**
1. Plugins Waves no instalados
2. Template corrupto
3. Permisos de directorio

**Solución:**
- Verifica plugins en Reaper
- Abre template manualmente en Reaper
- Verifica permisos en `F:\CURSOS\2025\Q3`

### Error: "ElevenLabs API"

**Solución:**
1. Verifica API key en `.streamlit/secrets.toml`
2. Revisa conexión a internet
3. Confirma créditos en cuenta ElevenLabs

---

## 💡 Tips Profesionales

### 1. Optimizar Template

**Para mejores resultados:**
- Ajusta plugins a tu preferencia
- Guarda presets personalizados
- Configura render settings (48kHz, 16-bit)

### 2. Batch Processing

**Procesar múltiples archivos:**
- Usa tab "Desde NAS/Local"
- Pega múltiples rutas (una por línea)
- Click "Procesar con Reaper"

### 3. Respaldo

**Las sesiones se guardan en:**
```
F:\CURSOS\2025\Q3\[nombre_archivo]_[timestamp]\
```

Puedes:
- Abrir manualmente en Reaper
- Modificar y re-renderizar
- Guardar como nuevo template

### 4. Performance

**Para mejor rendimiento:**
- Cierra otros programas
- Usa SSD para sesiones
- Ajusta `MAX_WORKERS` en línea 37

---

## 📊 Comparación Detallada

| Característica | v1.6.1 | v1.7.0 |
|---------------|--------|--------|
| **Procesamiento** | FFmpeg + Python | Reaper + Waves |
| **Calidad Audio** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | Rápido (1-2 min) | Medio (3-5 min) |
| **Setup** | Simple | Avanzado |
| **Streamlit Cloud** | ✅ Sí | ❌ No |
| **Reaper Requerido** | ❌ No | ✅ Sí |
| **Plugins** | Básicos | Waves Pro |
| **Automatización** | Parcial | Completa |
| **Edición Manual** | ❌ No | ✅ Sí (sesiones) |

---

## 🎓 Próximos Pasos

### 1. Personalizar Template

1. Abre template en Reaper:
   ```
   F:\00\00 Reaper\00 Voces.rpp
   ```

2. Ajusta plugins a tu gusto

3. Guarda cambios

4. Reinicia AudioPro v1.7

### 2. Crear Templates Adicionales

**Para diferentes escenarios:**
- Podcasts
- Música
- Diálogos de cine
- Webinars

**Pasos:**
1. Duplica template base
2. Ajusta cadena de plugins
3. Actualiza `REAPER_TEMPLATE` en código

### 3. Automatización Avanzada

**Posibles mejoras:**
- Detección automática de tipo de contenido
- Selección dinámica de template
- Post-procesamiento adicional
- Metadata y tags automáticos

---

## 📞 Soporte y Recursos

### Documentación
- 📖 [README.md](README.md) - Documentación principal
- 📖 [README_v17.md](README_v17.md) - Detalles v1.7
- 🚀 [QUICK_START_v17.md](QUICK_START_v17.md) - Esta guía

### Recursos
- 🎛️ [Reaper DAW](https://www.reaper.fm/)
- 🔊 [Waves Plugins](https://www.waves.com/)
- 🤖 [ElevenLabs](https://elevenlabs.io/)
- 🎨 [Platzi](https://platzi.com/)

### GitHub
- 📦 [Repositorio](https://github.com/Andresporahi/procesamientoaudio)
- 🏷️ Tags: `v1.6.1`, `v1.7.0`

---

## 🎉 ¡Listo para Empezar!

### Comando Rápido:

**v1.6.1 (Estable):**
```bash
streamlit run app.py
```

**v1.7.0 (Reaper):**
```bash
streamlit run app_v17_reaper.py
```

---

*AudioPro - Procesamiento profesional de audio al alcance de un click* 🚀
