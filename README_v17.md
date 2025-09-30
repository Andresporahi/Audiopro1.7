# 🎛️ AudioPro v1.7 - Reaper Edition

## 🚀 Nueva Versión con Integración Profesional de Reaper

AudioPro v1.7 introduce un flujo de trabajo revolucionario que combina la potencia de ElevenLabs con el procesamiento profesional de Reaper y plugins Waves.

---

## ✨ ¿Qué hay de nuevo en v1.7?

### 🎯 Flujo de Trabajo Profesional

```
📁 Fuente → 🎵 Extracción → 🤖 ElevenLabs → 🎛️ Reaper + Waves → ✅ Resultado Final
```

1. **Fuente de Audio/Video**
   - Subida manual de archivos
   - Links de Google Drive
   - Rutas locales/NAS

2. **Extracción de Audio**
   - FFmpeg extrae el audio del video
   - Conversión a WAV mono 16kHz

3. **Audio Isolation (ElevenLabs)**
   - Separación profesional de voz
   - Eliminación de ruido de fondo

4. **Procesamiento en Reaper**
   - Sesión automática desde template
   - Plugins Waves predefinidos
   - Render automático

5. **Resultado Final**
   - Mux con video original
   - Guardado en carpeta `procesados/`

---

## 📋 Requisitos

### Software Necesario

- **Python 3.9+**
- **FFmpeg** (instalado y en PATH)
- **Reaper** (instalado en `C:\Program Files\REAPER (x64)\`)
- **Plugins Waves** (configurados en el template)

### Configuración de Rutas

Asegúrate de tener estas rutas configuradas:

```python
# En app_v17_reaper.py
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\CURSOS\2025\Q3"
```

### Dependencias Python

```bash
pip install -r requirements.txt
```

---

## 🎛️ Template de Reaper

El template debe incluir:

1. **Track de Audio** con plugins Waves configurados:
   - Restauración espectral
   - EQ
   - Compresión
   - Limitador
   - Otros efectos según necesidades

2. **Configuración de Render**:
   - Formato: WAV
   - Sample Rate: 48kHz
   - Bit Depth: 16-bit

3. **Automatización** (opcional):
   - Volumen
   - Efectos
   - Pan

---

## 🚀 Uso

### 1. Iniciar la Aplicación

```bash
streamlit run app_v17_reaper.py
```

### 2. Seleccionar Fuente

**Opción A: Subir Archivos**
- Arrastra y suelta archivos
- Soporta: MP3, MP4, WAV, AVI, MOV, MKV, M4A, FLAC

**Opción B: Google Drive**
- Pega links de Drive
- Uno por línea
- Click en "Cargar desde Drive"

**Opción C: NAS/Local**
- Pega rutas completas
- Una por línea
- Click en "Cargar desde Rutas"

### 3. Procesar

- Click en "🎛️ Procesar con Reaper"
- Espera el procesamiento (puede tomar varios minutos)
- Descarga o reproduce el resultado

---

## 📂 Estructura de Archivos

```
AudioPro/
│
├── app_v17_reaper.py          # 🎛️ Aplicación principal v1.7
├── app.py                      # 📦 Versión 1.6 (sin cambios)
├── streamlit_config.py         # 🎨 Tema Platzi
├── setup_ffmpeg.py             # ⚙️ Configuración FFmpeg
│
├── requirements.txt            # 📋 Dependencias
├── README_v17.md               # 📖 Esta documentación
│
└── .streamlit/
    └── secrets.toml            # 🔐 API Keys (ElevenLabs)
```

---

## 🔧 Configuración de ElevenLabs

Crea `.streamlit/secrets.toml`:

```toml
[elevenlabs]
api_key = "tu_api_key_aqui"
base_url = "https://api.elevenlabs.io/v1"
```

---

## 🎯 Flujo Técnico Detallado

### 1. Extracción de Audio

```python
# FFmpeg extrae audio mono 16kHz
audio_wav = extract_audio_wav16_mono(input_file)
```

### 2. Audio Isolation (ElevenLabs)

```python
# API de ElevenLabs para separar voz
cleaned_audio = process_audio_with_elevenlabs(audio_wav)
```

### 3. Creación de Sesión Reaper

```python
# Genera sesión desde template
session_path = create_reaper_session_from_template(
    REAPER_TEMPLATE,
    session_name,
    cleaned_audio,
    REAPER_SESSIONS_DIR
)
```

### 4. Render en Reaper

```python
# Reaper renderiza con plugins
rendered_audio = render_reaper_session(session_path, REAPER_EXE)
```

### 5. Mux Final

```python
# Combina audio procesado con video original
ffmpeg -i video.mp4 -i audio_procesado.wav -c:v copy output.mp4
```

---

## 🐛 Solución de Problemas

### Reaper no se encuentra

```python
# Verifica la ruta en app_v17_reaper.py
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
```

### Template no se carga

```python
# Verifica que el archivo existe
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
```

### Render falla

- Revisa que los plugins Waves estén instalados
- Verifica que el template tenga configuración de render
- Comprueba los logs de Reaper

### Audio no se procesa

- Verifica API key de ElevenLabs
- Comprueba conexión a internet
- Revisa logs en Streamlit

---

## 📊 Comparación v1.6 vs v1.7

| Característica | v1.6 | v1.7 |
|---------------|------|------|
| Procesamiento | FFmpeg + Python | FFmpeg + ElevenLabs + Reaper |
| Plugins | Filtros básicos | Waves profesionales |
| Automatización | Manual | Completa |
| Calidad | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Velocidad | Rápido | Medio |
| Setup | Simple | Avanzado |

---

## 🎓 Tips Profesionales

1. **Optimiza el Template**
   - Guarda presets de plugins favoritos
   - Configura automatizaciones comunes
   - Ajusta render settings por proyecto

2. **Batch Processing**
   - Procesa múltiples archivos a la vez
   - Usa rutas NAS para grandes lotes

3. **Respaldo de Sesiones**
   - Las sesiones se guardan en `F:\CURSOS\2025\Q3`
   - Puedes abrirlas manualmente en Reaper
   - Modificar y re-renderizar si es necesario

4. **Performance**
   - Usa SSD para archivos temporales
   - Ajusta MAX_WORKERS según tu CPU
   - Cierra otros programas durante render

---

## 📝 Notas Importantes

- ⚠️ **Esta versión es LOCAL ONLY** (no usar en Streamlit Cloud)
- 🎛️ Requiere Reaper instalado localmente
- 💾 Necesita espacio en disco para sesiones y renders
- ⚡ El procesamiento puede tomar varios minutos por archivo
- 🔐 Mantén segura tu API key de ElevenLabs

---

## 🆚 Versiones

- **v1.6.1** - Versión estable con 3 fuentes + tema Platzi
- **v1.7.0** - Nueva versión con integración Reaper + Waves

Para volver a v1.6:
```bash
streamlit run app.py
```

---

## 📞 Soporte

¿Problemas? Revisa:
1. Logs en terminal
2. Configuración de rutas
3. Instalación de Reaper
4. API key de ElevenLabs

---

## 🎉 ¡Disfruta de AudioPro v1.7!

Procesamiento profesional de audio al alcance de un click 🚀
