#!/usr/bin/env python3
"""
Script de configuración automática de FFmpeg para Streamlit Cloud
Este script se ejecuta automáticamente al iniciar la aplicación
"""

import os
import subprocess
import sys


def setup_ffmpeg():
    """Configura FFmpeg en Streamlit Cloud."""
    print("🔧 Configurando FFmpeg para Streamlit Cloud...")

    # Verificar si estamos en Streamlit Cloud
    is_streamlit_cloud = os.getenv(
        'STREAMLIT_SERVER_HEADLESS', 'false'
    ).lower() == 'true'

    if is_streamlit_cloud:
        print("🌐 Detectado Streamlit Cloud")

        # En Streamlit Cloud, FFmpeg debería estar disponible via packages.txt
        try:
            # Verificar si ffmpeg está disponible
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print("✅ FFmpeg ya está disponible")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Intentar instalar FFmpeg usando apt-get (Ubuntu en Streamlit Cloud)
        try:
            print("📥 Instalando FFmpeg...")
            subprocess.run(
                ['sudo', 'apt-get', 'update'],
                capture_output=True, timeout=60
            )
            subprocess.run(
                ['sudo', 'apt-get', 'install', '-y', 'ffmpeg'],
                capture_output=True, timeout=120
            )

            # Verificar instalación
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print("✅ FFmpeg instalado exitosamente")
                return True
            else:
                print("❌ FFmpeg no se pudo instalar")
                return False

        except Exception as e:
            print(f"❌ Error instalando FFmpeg: {e}")
            return False
    else:
        print("💻 Ejecutando localmente - FFmpeg debe estar instalado manualmente")
        return True


def create_symlinks():
    """Crea enlaces simbólicos para ffprobe si es necesario."""
    try:
        # Verificar si ffprobe está disponible
        subprocess.run(
            ['ffprobe', '-version'],
            capture_output=True, text=True, timeout=10
        )
        print("✅ ffprobe disponible")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        try:
            # Crear enlace simbólico de ffmpeg a ffprobe si es necesario
            if os.path.exists('/usr/bin/ffmpeg'):
                os.symlink('/usr/bin/ffmpeg', '/usr/bin/ffprobe')
                print("✅ Enlace simbólico ffprobe creado")
            else:
                print("⚠️ No se pudo crear enlace simbólico para ffprobe")
        except Exception as e:
            print(f"⚠️ Error creando enlace simbólico: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando configuración de AudioPro 1.6...")

    # Configurar FFmpeg
    ffmpeg_ok = setup_ffmpeg()

    if ffmpeg_ok:
        # Crear enlaces simbólicos si es necesario
        create_symlinks()
        print("🎉 Configuración completada exitosamente!")
    else:
        print("❌ Configuración falló - FFmpeg no disponible")
        sys.exit(1)
