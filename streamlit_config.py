"""
Configuración específica para Streamlit Cloud
Aplica los colores de Platzi directamente en la aplicación
"""

import streamlit as st


def apply_platzi_theme():
    """Aplica el tema de Platzi a la aplicación Streamlit basado en el diseño
    actual de platzi.com"""

    # CSS personalizado inspirado en el diseño actual de Platzi
    platzi_css = """
    <style>
    /* Importar fuentes de Google */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Variables de colores actuales de Platzi */
    :root {
        --platzi-green: #98CA3F;
        --platzi-green-dark: #7FB32E;
        --platzi-green-light: #A8D65F;
        --platzi-blue: #2C3E50;
        --platzi-blue-light: #34495E;
        --platzi-gray: #F8F9FA;
        --platzi-gray-dark: #6C757D;
        --platzi-gray-light: #E9ECEF;
        --platzi-white: #FFFFFF;
        --platzi-black: #212529;
        --platzi-shadow: rgba(152, 202, 63, 0.15);
        --platzi-shadow-dark: rgba(44, 62, 80, 0.1);
    }

    /* Configuración global */
    .stApp {
        background: linear-gradient(135deg, #E9ECEF 0%, #DEE2E6 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        min-height: 100vh !important;
        position: relative !important;
    }

    .stApp::before {
        content: '' !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="platzi-pattern" width="40" height="40" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="%23ADB5BD" opacity="0.4"/><circle cx="0" cy="0" r="0.5" fill="%23ADB5BD" opacity="0.3"/><circle cx="40" cy="40" r="0.5" fill="%23ADB5BD" opacity="0.3"/></pattern></defs><rect width="100" height="100" fill="url(%23platzi-pattern)"/></svg>') !important;
        opacity: 0.6 !important;
        z-index: -1 !important;
        pointer-events: none !important;
    }

    /* Header principal estilo Platzi */
    .main-header {
        background: linear-gradient(135deg, var(--platzi-green) 0%, var(--platzi-green-dark) 100%) !important;
        padding: 3rem 2rem !important;
        border-radius: 24px !important;
        margin: -1rem -1rem 3rem -1rem !important;
        box-shadow: 0 12px 40px var(--platzi-shadow) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .main-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>') !important;
        opacity: 0.3 !important;
    }

    .main-header h1 {
        color: white !important;
        text-align: center !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        position: relative !important;
        z-index: 1 !important;
        letter-spacing: -0.02em !important;
    }

    .main-header .subtitle {
        color: rgba(255,255,255,0.95) !important;
        text-align: center !important;
        font-size: 1.3rem !important;
        margin-top: 1rem !important;
        font-weight: 500 !important;
        position: relative !important;
        z-index: 1 !important;
    }

    /* Botones estilo Platzi */
    .stButton > button {
        background: linear-gradient(135deg, var(--platzi-green) 0%, var(--platzi-green-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px var(--platzi-shadow) !important;
        font-family: 'Inter', sans-serif !important;
        text-transform: none !important;
        letter-spacing: 0.01em !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--platzi-green-dark) 0%, #6A9A2A 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px var(--platzi-shadow) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px var(--platzi-shadow) !important;
    }

    /* Botón primario especial */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--platzi-green) 0%, var(--platzi-green-dark) 100%) !important;
        font-size: 1.1rem !important;
        padding: 1rem 2.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 20px var(--platzi-shadow) !important;
    }

    /* Sidebar moderna */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--platzi-blue) 0%, var(--platzi-blue-light) 100%) !important;
        border-radius: 0 24px 24px 0 !important;
        box-shadow: 4px 0 20px var(--platzi-shadow-dark) !important;
    }

    .css-1d391kg .css-1v0mbdj {
        color: white !important;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--platzi-green) 0%, var(--platzi-green-dark) 100%) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px var(--platzi-shadow) !important;
    }

    /* Selectbox moderno */
    .stSelectbox > div > div {
        border: 2px solid var(--platzi-gray-light) !important;
        border-radius: 12px !important;
        background: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: var(--platzi-green) !important;
        box-shadow: 0 0 0 3px rgba(152, 202, 63, 0.1) !important;
    }

    /* File uploader moderno */
    .stFileUploader > div {
        border: 2px dashed var(--platzi-green) !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, rgba(152, 202, 63, 0.03) 0%, rgba(152, 202, 63, 0.08) 100%) !important;
        transition: all 0.3s ease !important;
        padding: 2rem !important;
    }

    .stFileUploader > div:hover {
        border-color: var(--platzi-green-dark) !important;
        background: linear-gradient(135deg, rgba(152, 202, 63, 0.05) 0%, rgba(152, 202, 63, 0.12) 100%) !important;
        transform: translateY(-1px) !important;
    }

    /* Cards modernos estilo Platzi */
    .modern-card {
        background: white !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06) !important;
        border: 1px solid var(--platzi-gray-light) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .modern-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, var(--platzi-green) 0%, var(--platzi-green-dark) 100%) !important;
    }

    .modern-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 48px rgba(0,0,0,0.1) !important;
        border-color: var(--platzi-green) !important;
    }

    /* Títulos modernos */
    h1, h2, h3, h4, h5, h6 {
        color: var(--platzi-blue) !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.01em !important;
    }

    h2 {
        font-size: 2rem !important;
        margin-bottom: 1.5rem !important;
    }

    h3 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Mensajes de estado */
    .stSuccess {
        border-left: 4px solid var(--platzi-green) !important;
        background: linear-gradient(135deg, rgba(152, 202, 63, 0.05) 0%, rgba(152, 202, 63, 0.1) 100%) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 16px var(--platzi-shadow) !important;
    }

    .stInfo {
        border-left: 4px solid var(--platzi-blue) !important;
        background: linear-gradient(135deg, rgba(44, 62, 80, 0.05) 0%, rgba(44, 62, 80, 0.1) 100%) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 16px var(--platzi-shadow-dark) !important;
    }

    .stWarning {
        border-left: 4px solid #F39C12 !important;
        background: linear-gradient(135deg, rgba(243, 156, 18, 0.05) 0%, rgba(243, 156, 18, 0.1) 100%) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
    }

    .stError {
        border-left: 4px solid #E74C3C !important;
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.05) 0%, rgba(231, 76, 60, 0.1) 100%) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
    }

    /* Métricas estilo Platzi */
    .metric-container {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
        border: 1px solid var(--platzi-gray-light) !important;
        transition: all 0.3s ease !important;
    }

    .metric-container:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1) !important;
    }

    /* Animaciones suaves */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem !important;
            margin: -1rem -0.5rem 2rem -0.5rem !important;
        }

        .main-header h1 {
            font-size: 2.5rem !important;
        }

        .modern-card {
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
        }

        .stButton > button {
            padding: 0.75rem 1.5rem !important;
            font-size: 0.95rem !important;
        }
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px !important;
    }

    ::-webkit-scrollbar-track {
        background: var(--platzi-gray-light) !important;
        border-radius: 4px !important;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--platzi-green) !important;
        border-radius: 4px !important;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--platzi-green-dark) !important;
    }
    </style>
    """

    # Aplicar el CSS
    st.markdown(platzi_css, unsafe_allow_html=True)


# Si se ejecuta directamente, aplicar el tema
if __name__ == "__main__":
    st.set_page_config(
        page_title="AudioPro - Tema Platzi",
        page_icon="🎵",
        layout="wide"
    )

    apply_platzi_theme()

    st.title("🎨 Tema de Platzi Aplicado")
    st.success("✅ Los colores de Platzi han sido aplicados correctamente")
    st.info("🔧 Este archivo se puede importar en app.py para aplicar el tema")
