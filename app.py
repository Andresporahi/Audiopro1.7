"""
AudioPro v1.7 - Integración con Reaper
Este archivo implementa el flujo completo con Reaper para procesamiento profesional
"""

import os
import streamlit as st
import tempfile
import subprocess
import shutil
from datetime import datetime
from typing import Optional
from app import (
    get_bytes_from_local_path,
    get_bytes_from_drive,
    extract_audio_wav16_mono,
    run_ffmpeg,
    is_audio_only_file,
    process_audio_with_elevenlabs,
    register_user_session,
    display_user_stats
)

##############################
# Configuración / Parámetros #
##############################
APP_TITLE = "🎵 AudioPro v1.7 - Reaper Edition"
PIPELINE_VERSION = "v1.7.0"

# Rutas de Reaper
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\CURSOS\2025\Q3"

# Límite de archivos
MAX_FILE_MB = int(os.getenv("MAX_FILE_MB", "800"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))

# ElevenLabs
try:
    ELEVENLABS_API_KEY = st.secrets.get("elevenlabs", {}).get("api_key")
    ELEVENLABS_BASE_URL = st.secrets.get("elevenlabs", {}).get("base_url")
except Exception:
    ELEVENLABS_API_KEY = None
    ELEVENLABS_BASE_URL = None

#########################
# Funciones de Reaper #
#########################


def create_reaper_session_from_template(
    template_path: str,
    session_name: str,
    audio_file: str,
    output_dir: str
) -> str:
    """Crea una nueva sesión de Reaper a partir del template.

    Args:
        template_path: Ruta al template .rpp
        session_name: Nombre para la nueva sesión
        audio_file: Ruta al archivo de audio a procesar
        output_dir: Directorio donde guardar la sesión

    Returns:
        Ruta al archivo .rpp de la nueva sesión
    """
    # Crear directorio de sesión
    session_dir = os.path.join(output_dir, session_name)
    os.makedirs(session_dir, exist_ok=True)

    # Leer template
    with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
        template_content = f.read()

    # Modificar template para la nueva sesión
    # Actualizar RENDER_FILE path
    new_render_path = os.path.join(session_dir, session_name)
    template_content = template_content.replace(
        'RENDER_FILE "F:\\CURSOS\\2025\\Q2\\2505_php\\Prueba Reaper"',
        f'RENDER_FILE "{new_render_path}"'
    )

    # Guardar nueva sesión
    new_session_path = os.path.join(session_dir, f"{session_name}.rpp")
    with open(new_session_path, 'w', encoding='utf-8') as f:
        f.write(template_content)

    return new_session_path


def add_audio_to_reaper_session(session_path: str, audio_file: str):
    """Agrega un archivo de audio a una sesión de Reaper.

    Args:
        session_path: Ruta al archivo .rpp de la sesión
        audio_file: Ruta al archivo de audio a agregar
    """
    # Leer sesión actual
    with open(session_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Encontrar la sección de TRACK y agregar el item
    track_found = False
    insert_index = 0

    for i, line in enumerate(lines):
        if '<TRACK' in line:
            track_found = True
        if track_found and '>' in line and '<' not in line:
            insert_index = i + 1
            break

    # Crear item de audio
    audio_item = f'''    <ITEM
      POSITION 0
      SNAPOFFS 0
      LENGTH {get_audio_duration(audio_file)}
      LOOP 0
      ALLTAKES 0
      FADEIN 1 0 0 1 0 0 0
      FADEOUT 1 0 0 1 0 0 0
      MUTE 0 0
      SEL 0
      IGUID {{GENERATED_GUID}}
      IID 1
      NAME "{os.path.basename(audio_file)}"
      VOLPAN 1 0 1 -1
      SOFFS 0
      PLAYRATE 1 1 0 -1 0 0.0025
      CHANMODE 0
      GUID {{GENERATED_GUID2}}
      <SOURCE WAVE
        FILE "{audio_file}"
      >
    >
'''

    # Insertar item
    lines.insert(insert_index, audio_item)

    # Guardar sesión actualizada
    with open(session_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def get_audio_duration(audio_file: str) -> float:
    """Obtiene la duración de un archivo de audio usando ffprobe.

    Args:
        audio_file: Ruta al archivo de audio

    Returns:
        Duración en segundos
    """
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', audio_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except Exception:
        return 10.0  # Default 10 segundos


def render_reaper_session(session_path: str, reaper_exe: str) -> str:
    """Renderiza una sesión de Reaper y retorna la ruta del archivo renderizado.

    Args:
        session_path: Ruta al archivo .rpp de la sesión
        reaper_exe: Ruta al ejecutable de Reaper

    Returns:
        Ruta al archivo renderizado
    """
    # Comando para renderizar
    cmd = [
        reaper_exe,
        '-renderproject', session_path,
        '-nosplash',
        '-close'
    ]

    st.info(f"🎛️ Renderizando en Reaper: {os.path.basename(session_path)}")

    # Ejecutar Reaper
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Esperar con timeout
    try:
        process.wait(timeout=300)  # 5 minutos max
    except subprocess.TimeoutExpired:
        process.kill()
        raise Exception("Reaper excedió el tiempo límite de render (5 min)")

    # Buscar archivo renderizado
    session_dir = os.path.dirname(session_path)
    session_name = os.path.splitext(os.path.basename(session_path))[0]

    # Buscar archivo con patrón
    possible_files = [
        os.path.join(session_dir, f"{session_name}.wav"),
        os.path.join(session_dir, f"{session_name}-master.wav"),
        os.path.join(session_dir, f"{session_name} master.wav"),
    ]

    for file_path in possible_files:
        if os.path.exists(file_path):
            return file_path

    # Si no se encuentra, buscar en el directorio
    for file in os.listdir(session_dir):
        if file.endswith('.wav') and session_name in file:
            return os.path.join(session_dir, file)

    raise Exception(f"No se encontró archivo renderizado en {session_dir}")


def process_with_reaper_pipeline(
    file_bytes: bytes,
    original_name: str,
    source_dir: Optional[str] = None
) -> dict:
    """Pipeline completo con Reaper.

    Args:
        file_bytes: Bytes del archivo original
        original_name: Nombre del archivo original
        source_dir: Directorio de origen (opcional)

    Returns:
        Dict con información del archivo procesado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = f"{os.path.splitext(original_name)[0]}_{timestamp}"

    # 1) Guardar archivo original temporalmente
    tmp_input = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(original_name)[1]
    ).name
    with open(tmp_input, 'wb') as f:
        f.write(file_bytes)

    st.info(f"📁 Procesando: {original_name}")

    # 2) Extraer audio
    st.info("🎵 Extrayendo audio...")
    audio_wav = extract_audio_wav16_mono(tmp_input)

    # 3) ElevenLabs Audio Isolation
    if ELEVENLABS_API_KEY and ELEVENLABS_BASE_URL:
        st.info("🤖 Aplicando Audio Isolation (ElevenLabs)...")
        audio_wav = process_audio_with_elevenlabs(audio_wav)
    else:
        st.warning("⚠️ ElevenLabs no configurado - saltando Audio Isolation")

    # 4) Crear sesión de Reaper
    st.info(f"🎛️ Creando sesión de Reaper: {session_name}")
    session_path = create_reaper_session_from_template(
        REAPER_TEMPLATE,
        session_name,
        audio_wav,
        REAPER_SESSIONS_DIR
    )

    # 5) Agregar audio a la sesión
    st.info("📂 Agregando audio a sesión de Reaper...")
    add_audio_to_reaper_session(session_path, audio_wav)

    # 6) Renderizar en Reaper
    st.info("⚙️ Renderizando en Reaper (esto puede tomar unos minutos)...")
    rendered_audio = render_reaper_session(session_path, REAPER_EXE)

    # 7) Determinar directorio de salida
    if source_dir:
        output_dir = os.path.join(source_dir, 'procesados')
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.dirname(rendered_audio)

    # 8) Procesar según tipo de archivo
    is_video = not is_audio_only_file(tmp_input)

    if is_video:
        # Mux audio con video
        st.info("🎬 Combinando audio procesado con video...")
        base_name = os.path.splitext(original_name)[0]
        final_out = os.path.join(output_dir, f"{base_name}_procesado.mp4")

        cmd = [
            'ffmpeg', '-y', '-i', tmp_input, '-i', rendered_audio,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
            '-ar', '48000', '-map', '0:v:0', '-map', '1:a:0',
            '-shortest', final_out
        ]
        run_ffmpeg(cmd)
    else:
        # Solo copiar audio procesado
        base_name = os.path.splitext(original_name)[0]
        ext = os.path.splitext(original_name)[1]
        final_out = os.path.join(output_dir, f"{base_name}_procesado{ext}")
        shutil.copy(rendered_audio, final_out)

    # 9) Limpiar archivos temporales
    try:
        os.unlink(tmp_input)
        os.unlink(audio_wav)
    except Exception:
        pass

    st.success(f"✅ Procesado completado: {os.path.basename(final_out)}")

    return {
        'original_name': original_name,
        'output_file': final_out,
        'reaper_session': session_path,
        'is_video': is_video
    }


def main():
    st.set_page_config(
        page_title="AudioPro v1.7 - Reaper Edition",
        page_icon="🎛️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Aplicar tema de Platzi
    try:
        from streamlit_config import apply_platzi_theme
        apply_platzi_theme()
    except Exception:
        pass

    # Registrar sesión
    register_user_session()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎛️ AudioPro v1.7</h1>
        <div class="subtitle">Procesamiento Profesional con Reaper + Waves</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🎛️ Configuración Reaper")

        # Mostrar configuración
        st.info(f"""
        **Template**: `{os.path.basename(REAPER_TEMPLATE)}`

        **Sesiones**: `{REAPER_SESSIONS_DIR}`

        **Reaper**: `{REAPER_EXE}`
        """)

        st.markdown("---")
        st.header("👥 Usuarios Activos")
        display_user_stats()

        st.markdown("---")
        st.caption(f"🎵 AudioPro {PIPELINE_VERSION}")

    # Tabs para fuentes
    tab1, tab2, tab3 = st.tabs([
        "📤 Subir Archivos",
        "🔗 Desde Google Drive",
        "💾 Desde NAS/Ruta Local"
    ])

    files_to_process = []

    with tab1:
        st.markdown("### 📤 Subir Archivos Manualmente")
        uploaded_files = st.file_uploader(
            "Selecciona archivos",
            type=['mp3', 'mp4', 'wav', 'avi', 'mov', 'mkv', 'm4a', 'flac'],
            accept_multiple_files=True
        )

        if uploaded_files:
            for f in uploaded_files:
                files_to_process.append({
                    'bytes': f.getbuffer(),
                    'name': f.name,
                    'source_dir': None
                })

    with tab2:
        st.markdown("### 🔗 Desde Google Drive")
        drive_links = st.text_area(
            "Links de Google Drive (uno por línea)",
            height=150
        )

        if drive_links and st.button("📥 Cargar desde Drive"):
            links_list = [link.strip() for link in drive_links.split('\n') if link.strip()]
            for link in links_list:
                result = get_bytes_from_drive(link)
                if result:
                    file_bytes, file_name = result
                    files_to_process.append({
                        'bytes': file_bytes,
                        'name': file_name,
                        'source_dir': None
                    })

    with tab3:
        st.markdown("### 💾 Desde NAS/Ruta Local")
        local_paths = st.text_area(
            "Rutas de archivos (una por línea)",
            height=150
        )

        if local_paths and st.button("📥 Cargar desde Rutas"):
            paths_list = [p.strip() for p in local_paths.split('\n') if p.strip()]
            for path in paths_list:
                result = get_bytes_from_local_path(path)
                if result:
                    file_bytes, file_name, source_dir = result
                    files_to_process.append({
                        'bytes': file_bytes,
                        'name': file_name,
                        'source_dir': source_dir
                    })

    # Botón de procesamiento
    if files_to_process:
        st.markdown("---")
        st.info(f"📋 {len(files_to_process)} archivo(s) listo(s) para procesar")

        if st.button("🎛️ Procesar con Reaper", type="primary"):
            results = []

            progress_bar = st.progress(0)
            status = st.empty()

            for idx, file_data in enumerate(files_to_process):
                progress = (idx + 1) / len(files_to_process)
                progress_bar.progress(progress)
                status.info(
                    f"Procesando {idx + 1}/{len(files_to_process)}: "
                    f"{file_data['name']}"
                )

                try:
                    result = process_with_reaper_pipeline(
                        file_data['bytes'],
                        file_data['name'],
                        file_data['source_dir']
                    )
                    results.append(result)
                except Exception as e:
                    st.error(f"❌ Error en {file_data['name']}: {e}")

            status.success(
                f"🎉 Procesamiento completado: {len(results)} archivo(s)"
            )

            # Mostrar resultados
            st.header("✅ Resultados")
            for result in results:
                st.subheader(f"📁 {result['original_name']}")
                st.success(f"✅ Archivo procesado: `{result['output_file']}`")
                st.info(f"🎛️ Sesión de Reaper: `{result['reaper_session']}`")

                # Preview si es posible
                if result['is_video']:
                    st.video(result['output_file'])
                else:
                    st.audio(result['output_file'])


if __name__ == '__main__':
    main()
