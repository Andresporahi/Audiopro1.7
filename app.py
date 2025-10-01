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
from audio_utils import (
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
REAPER_SESSIONS_DIR = r"F:\00\00 Reaper\Procesados"

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


def test_reaper_script():
    """Función de prueba para verificar que Reaper funciona correctamente."""
    lua_script = os.path.join(os.path.dirname(__file__), "test_reaper.lua")
    
    if not os.path.exists(lua_script):
        st.error("❌ Script de prueba no encontrado")
        return

    # Ejecutar script de prueba
    cmd = [
        REAPER_EXE,
        '-nosplash',
        lua_script,
        "test_audio.wav",
        "F:\\00\\00 Reaper\\test_session.rpp"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        st.info(f"Resultado: {result.returncode}")
        st.info(f"Salida: {result.stdout}")
        if result.stderr:
            st.error(f"Error: {result.stderr}")
    except Exception as e:
        st.error(f"❌ Error ejecutando prueba: {e}")


def add_audio_to_reaper_session(session_path: str, audio_file: str, original_name: str = None):
    """Agrega un archivo de audio a una sesión de Reaper usando ReaScript Lua.

    Args:
        session_path: Ruta al archivo .rpp de la sesión
        audio_file: Ruta al archivo de audio a agregar
        original_name: Nombre original del archivo (sin extensión)
    """
    # Usar el script Lua estático
    lua_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "add_audio_to_session.lua"))
    if not os.path.exists(lua_script):
        st.error("❌ Script Lua no encontrado: add_audio_to_session.lua")
        return

    # Crear script temporal que establece ExtState y ejecuta el script principal
    # Según documentación: usar SetExtState para pasar parámetros
    temp_script = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.lua',
        delete=False,
        encoding='utf-8'
    )

    # Convertir rutas a formato compatible con Lua (usar / en lugar de \)
    lua_script_path = lua_script.replace('\\', '/')
    audio_file_path = audio_file.replace('\\', '/')
    session_path_path = session_path.replace('\\', '/')
    template_path = REAPER_TEMPLATE.replace('\\', '/')
    
    # Usar el nombre original proporcionado o fallback al nombre del audio_file
    if not original_name:
        original_name = os.path.splitext(os.path.basename(audio_file))[0]

    temp_script.write(f"""
-- Script temporal para pasar parámetros usando ExtState
-- Según documentación de ReaScript: https://www.reaper.fm/sdk/reascript/reascript.php

-- Establecer parámetros usando ExtState
reaper.SetExtState("AudioPro", "audio_file", [[{audio_file_path}]], false)
reaper.SetExtState("AudioPro", "session_name", [[{session_path_path}]], false)
reaper.SetExtState("AudioPro", "template_path", [[{template_path}]], false)
reaper.SetExtState("AudioPro", "original_name", [[{original_name}]], false)

-- Ejecutar el script principal
dofile([[{lua_script_path}]])

-- Limpiar ExtState
reaper.DeleteExtState("AudioPro", "audio_file", false)
reaper.DeleteExtState("AudioPro", "session_name", false)
reaper.DeleteExtState("AudioPro", "template_path", false)
reaper.DeleteExtState("AudioPro", "original_name", false)
""")
    temp_script.close()

    # Ejecutar ReaScript según documentación
    cmd = [
        REAPER_EXE,
        '-nosplash',
        temp_script.name
    ]

    try:
        # Ejecutar Reaper en background para que permanezca abierto
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar un poco para que Reaper inicie y ejecute el script
        import time
        time.sleep(5)  # Esperar 5 segundos para que el script se ejecute
        
        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            st.success("✅ Audio agregado a sesión de Reaper - Reaper permanecerá abierto")
        else:
            # Si terminó, verificar el código de salida
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                st.error(f"❌ Error ejecutando ReaScript: {stderr}")
            else:
                st.success("✅ Audio agregado a sesión de Reaper")
    except Exception as e:
        st.error(f"❌ Error ejecutando ReaScript: {e}")
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(temp_script.name)
        except Exception:
            pass


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


def render_reaper_session(session_path: str, reaper_exe: str, original_name: str = None) -> str:
    """El render ya se hace en add_audio_to_reaper_session, solo retorna la ruta esperada.

    Args:
        session_path: Ruta al archivo .rpp de la sesión
        reaper_exe: Ruta al ejecutable de Reaper
        original_name: Nombre original del archivo (sin extensión)

    Returns:
        Ruta al archivo renderizado
    """
    # El render ya se ejecutó en add_audio_to_reaper_session
    # Solo retornamos la ruta esperada del archivo renderizado
    session_dir = os.path.dirname(session_path)
    
    if original_name:
        # Usar nombre original del archivo
        output_file = os.path.join(session_dir, f"{original_name}_renderizado.wav")
    else:
        # Fallback al nombre de sesión
        session_name = os.path.splitext(os.path.basename(session_path))[0]
        output_file = os.path.join(session_dir, f"{session_name}_renderizado.wav")
    
    st.info(f"🔍 Buscando archivo renderizado en: {output_file}")
    
    # Verificar que el archivo existe
    if os.path.exists(output_file):
        st.success(f"✅ Render completado: {output_file}")
        return output_file
    else:
        st.error(f"❌ Archivo renderizado no encontrado en: {output_file}")
        # Listar archivos en el directorio para debug
        if os.path.exists(session_dir):
            files = os.listdir(session_dir)
            st.info(f"📂 Archivos en {session_dir}: {files}")
        return None


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
        st.info(f"📤 Enviando a ElevenLabs: {audio_wav}")
        audio_wav_before = audio_wav
        audio_wav = process_audio_with_elevenlabs(audio_wav)
        if audio_wav != audio_wav_before:
            st.success(f"✅ ElevenLabs procesó correctamente: {audio_wav}")
        else:
            st.warning("⚠️ ElevenLabs no procesó el audio - usando original")
    else:
        st.warning("⚠️ ElevenLabs no configurado - saltando Audio Isolation")

    # 4) Crear directorio de sesiones si no existe
    os.makedirs(REAPER_SESSIONS_DIR, exist_ok=True)
    
    # 5) Definir ruta de la nueva sesión
    session_path = os.path.join(REAPER_SESSIONS_DIR, f"{session_name}.rpp")
    
    st.info(f"🎛️ Creando sesión de Reaper: {session_name}")
    st.info(f"📁 Sesión se guardará en: {session_path}")
    
    # 6) Agregar audio a la sesión (esto crea la sesión desde el template)
    st.info("📂 Agregando audio a sesión de Reaper...")
    st.info(f"📤 Enviando a Reaper: {audio_wav}")
    
    # Obtener nombre original sin extensión para pasar a Reaper
    original_name_clean = os.path.splitext(original_name)[0]
    add_audio_to_reaper_session(session_path, audio_wav, original_name_clean)

    # 7) Esperar a que Reaper termine el render
    st.info("⚙️ Esperando a que Reaper complete el render...")
    st.warning("⏰ Por favor, ten paciencia. El procesamiento con Reaper puede tomar varios minutos.")
    
    # Esperar hasta 10 minutos para que el archivo renderizado aparezca
    session_dir = os.path.dirname(session_path)
    expected_render = os.path.join(session_dir, f"{original_name_clean}_renderizado.wav")
    
    import time
    max_wait = 600  # 10 minutos
    elapsed = 0
    check_interval = 5  # Verificar cada 5 segundos
    
    while elapsed < max_wait:
        if os.path.exists(expected_render):
            # Esperar un poco más para asegurar que el archivo esté completamente escrito
            time.sleep(2)
            st.success(f"✅ Render completado: {expected_render}")
            rendered_audio = expected_render
            break
        time.sleep(check_interval)
        elapsed += check_interval
        if elapsed % 30 == 0:  # Mostrar progreso cada 30 segundos
            st.info(f"⏳ Esperando render... ({elapsed}s / {max_wait}s)")
    else:
        st.error(f"❌ Timeout esperando el archivo renderizado: {expected_render}")
        raise Exception("Timeout esperando render de Reaper")

    # Verificar que el render fue exitoso
    if not rendered_audio or not os.path.exists(rendered_audio):
        st.error("❌ El render de Reaper no generó un archivo de salida")
        raise Exception("Render de Reaper falló")

    # 8) Determinar directorio de salida
    if source_dir:
        output_dir = os.path.join(source_dir, 'procesados')
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.dirname(rendered_audio)

    # 9) Procesar según tipo de archivo
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
        'is_video': is_video,
        'is_local': source_dir is not None  # Indica si es archivo local
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
        st.header("🤖 ElevenLabs")

        # Botón para deshabilitar ElevenLabs
        if st.button("🔧 Deshabilitar ElevenLabs temporalmente"):
            st.session_state['disable_elevenlabs'] = True
            st.success("✅ ElevenLabs deshabilitado - Se saltará Voice Isolator")

        if st.button("🔄 Rehabilitar ElevenLabs"):
            st.session_state['disable_elevenlabs'] = False
            st.success("✅ ElevenLabs habilitado - Se aplicará Voice Isolator")
            
        st.divider()
        
        # Botón de prueba para Reaper
        if st.button("🧪 Probar Reaper"):
            test_reaper_script()

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
                
                if result.get('is_local', False):
                    # Archivo local - solo mostrar ruta
                    st.success(f"✅ Archivo procesado guardado en:")
                    st.code(result['output_file'], language=None)
                    st.info(f"🎛️ Sesión de Reaper guardada en:")
                    st.code(result['reaper_session'], language=None)
                    st.info("💡 Los archivos están listos en tu sistema local")
                else:
                    # Archivo subido - mostrar preview y descarga
                    st.success(f"✅ Archivo procesado: `{result['output_file']}`")
                    st.info(f"🎛️ Sesión de Reaper: `{result['reaper_session']}`")
                    
                    # Preview
                    if result['is_video']:
                        st.video(result['output_file'])
                    else:
                        st.audio(result['output_file'])
                    
                    # Botón de descarga
                    with open(result['output_file'], 'rb') as f:
                        st.download_button(
                            label=f"📥 Descargar {os.path.basename(result['output_file'])}",
                            data=f.read(),
                            file_name=os.path.basename(result['output_file']),
                            mime='video/mp4' if result['is_video'] else 'audio/wav'
                        )


if __name__ == '__main__':
    main()
