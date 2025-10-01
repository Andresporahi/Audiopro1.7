"""
Funciones auxiliares para AudioPro v1.7
Contiene todas las funciones de procesamiento de audio
"""

import os
import tempfile
import subprocess
import requests
import gdown
from typing import Optional, Tuple
import streamlit as st


def get_bytes_from_local_path(file_path: str) -> Optional[Tuple[bytes, str, str]]:
    """Obtiene bytes de un archivo desde una ruta local.

    Args:
        file_path: Ruta al archivo

    Returns:
        Tuple de (bytes, nombre_archivo, directorio_origen) o None
    """
    try:
        if not os.path.exists(file_path):
            st.error(f"❌ Archivo no encontrado: {file_path}")
            return None

        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        file_name = os.path.basename(file_path)
        source_dir = os.path.dirname(file_path)

        return file_bytes, file_name, source_dir

    except Exception as e:
        st.error(f"❌ Error leyendo archivo {file_path}: {e}")
        return None


def get_bytes_from_drive(drive_url: str) -> Optional[Tuple[bytes, str]]:
    """Obtiene bytes de un archivo desde Google Drive.

    Args:
        drive_url: URL de Google Drive

    Returns:
        Tuple de (bytes, nombre_archivo) o None
    """
    try:
        # Extraer ID del archivo de la URL
        if 'id=' in drive_url:
            file_id = drive_url.split('id=')[1].split('&')[0]
        elif '/file/d/' in drive_url:
            file_id = drive_url.split('/file/d/')[1].split('/')[0]
        else:
            st.error("❌ URL de Google Drive no válida")
            return None

        # Descargar archivo
        download_url = f"https://drive.google.com/uc?id={file_id}"
        file_path = gdown.download(download_url, quiet=True)

        if not file_path:
            st.error("❌ No se pudo descargar el archivo de Google Drive")
            return None

        # Leer bytes
        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        file_name = os.path.basename(file_path)

        # Limpiar archivo temporal
        try:
            os.unlink(file_path)
        except Exception:
            pass

        return file_bytes, file_name

    except Exception as e:
        st.error(f"❌ Error descargando de Google Drive: {e}")
        return None


def extract_audio_wav16_mono(input_file: str) -> str:
    """Extrae audio de un archivo y lo convierte a WAV mono 48kHz.

    Args:
        input_file: Ruta al archivo de entrada

    Returns:
        Ruta al archivo WAV generado
    """
    # Guardar audio extraído directamente en F:\00\00 Reaper\Eleven\
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    eleven_dir = r"F:\00\00 Reaper\Eleven"
    os.makedirs(eleven_dir, exist_ok=True)
    
    output_file = os.path.join(eleven_dir, f"extracted_{timestamp}.wav")

    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-ac', '1',  # mono
        '-ar', '48000',  # 48kHz (estándar profesional)
        '-acodec', 'pcm_s16le',  # 16-bit PCM
        '-sample_fmt', 's16',  # Asegurar formato 16-bit
        output_file
    ]

    run_ffmpeg(cmd)
    st.info(f"📁 Audio extraído guardado en: {output_file}")
    return output_file


def run_ffmpeg(cmd: list) -> None:
    """Ejecuta un comando FFmpeg.

    Args:
        cmd: Lista de argumentos del comando
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode != 0:
            st.error(f"❌ Error FFmpeg: {result.stderr}")
            raise Exception(f"FFmpeg failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        st.error("❌ FFmpeg excedió el tiempo límite (10 min)")
        raise Exception("FFmpeg timeout")
    except Exception as e:
        st.error(f"❌ Error ejecutando FFmpeg: {e}")
        raise


def is_audio_only_file(file_path: str) -> bool:
    """Determina si un archivo es solo audio.

    Args:
        file_path: Ruta al archivo

    Returns:
        True si es solo audio, False si es video
    """
    audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
    _, ext = os.path.splitext(file_path.lower())
    return ext in audio_extensions


def process_audio_with_elevenlabs(audio_file: str) -> str:
    """Procesa audio con ElevenLabs Audio Isolation.

    Args:
        audio_file: Ruta al archivo de audio

    Returns:
        Ruta al archivo procesado
    """
    try:
        # Obtener configuración de ElevenLabs
        api_key = st.secrets.get("elevenlabs", {}).get("api_key")
        base_url = st.secrets.get("elevenlabs", {}).get("base_url", "https://api.elevenlabs.io")

        if not api_key:
            st.warning("⚠️ API key de ElevenLabs no configurada")
            return audio_file

        # Verificar si ElevenLabs está deshabilitado temporalmente
        if st.session_state.get('disable_elevenlabs', False):
            st.info("ℹ️ ElevenLabs deshabilitado temporalmente - Continuando sin Voice Isolator")
            return audio_file

        # Preparar request con multipart/form-data (según documentación)
        headers = {
            'xi-api-key': api_key
        }

        # Endpoint de Audio Isolation (según documentación oficial)
        url = f"{base_url}/audio-isolation"

        # Preparar archivos para multipart/form-data
        with open(audio_file, 'rb') as f:
            files = {
                'audio': (os.path.basename(audio_file), f, 'audio/wav')
            }

            # Enviar request con reintentos
            st.info(f"🌐 Enviando a ElevenLabs: {url}")
            st.info(f"📊 Archivo: {os.path.basename(audio_file)}")
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    st.info(f"🔄 Intento {attempt + 1}/{max_retries}...")
                    response = requests.post(url, headers=headers, files=files, timeout=180)
                    st.info(f"📡 Respuesta recibida: {response.status_code}")
                    break
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 3  # Incrementar tiempo de espera
                        st.warning(f"⚠️ Intento {attempt + 1} falló, reintentando en {wait_time}s... ({e})")
                        import time
                        time.sleep(wait_time)
                    else:
                        st.error(f"❌ Error de conexión con ElevenLabs después de {max_retries} intentos")
                        return audio_file

            if response.status_code == 200:
                # Guardar resultado temporal primero
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                eleven_dir = r"F:\00\00 Reaper\Eleven"
                os.makedirs(eleven_dir, exist_ok=True)
                
                # Guardar respuesta temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                
                # Convertir a WAV puro usando FFmpeg (eliminar metadata ID3)
                output_file = os.path.join(eleven_dir, f"elevenlabs_{timestamp}.wav")
                
                st.info("🔧 Convirtiendo a WAV puro compatible con Reaper...")
                cmd = [
                    'ffmpeg', '-y', '-i', temp_file,
                    '-ar', '48000',  # 48kHz
                    '-ac', '1',  # Mono
                    '-acodec', 'pcm_s16le',  # 16-bit PCM
                    '-sample_fmt', 's16',  # Asegurar formato 16-bit
                    '-fflags', '+bitexact',  # Sin metadata
                    '-flags:v', '+bitexact',
                    '-flags:a', '+bitexact',
                    output_file
                ]
                
                run_ffmpeg(cmd)
                
                # Eliminar archivo temporal
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass
                
                st.success(f"✅ Voice Isolator aplicado y convertido a WAV puro: {output_file}")
                return output_file
            elif response.status_code == 401:
                st.error("❌ Error de autenticación ElevenLabs - Verifica tu API key")
                return audio_file
            elif response.status_code == 404:
                st.warning("⚠️ Voice Isolator no disponible en tu cuenta de ElevenLabs")
                st.info("💡 Tip: Deshabilita ElevenLabs temporalmente usando el botón en el sidebar")
                return audio_file
            elif response.status_code == 429:
                st.error("❌ Límite de rate excedido en ElevenLabs - Espera unos minutos")
                return audio_file
            else:
                st.error(f"❌ Error ElevenLabs: {response.status_code} - {response.text}")
                return audio_file

    except Exception as e:
        st.error(f"❌ Error procesando con ElevenLabs: {e}")
        return audio_file


def register_user_session() -> None:
    """Registra la sesión del usuario para estadísticas."""
    if 'user_sessions' not in st.session_state:
        st.session_state.user_sessions = []

    # Agregar sesión actual
    import time
    current_time = time.time()
    st.session_state.user_sessions.append(current_time)

    # Mantener solo las últimas 100 sesiones
    if len(st.session_state.user_sessions) > 100:
        st.session_state.user_sessions = st.session_state.user_sessions[-100:]


def display_user_stats() -> None:
    """Muestra estadísticas de usuarios activos."""
    if 'user_sessions' not in st.session_state:
        st.session_state.user_sessions = []

    total_sessions = len(st.session_state.user_sessions)

    if total_sessions > 0:
        st.metric("Sesiones Activas", total_sessions)
    else:
        st.info("No hay sesiones registradas")
