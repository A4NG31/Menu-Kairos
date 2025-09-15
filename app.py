import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import base64

# Configuración de página
st.set_page_config(
    page_title="GoPass - Validador Profesional", 
    page_icon="https://i.imgur.com/z9xt46F.jpeg", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Helper functions
# -----------------------------
def to_excel_bytes(df_dict):
    from openpyxl import Workbook
    import openpyxl
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, df in df_dict.items():
            sheet_name = str(name)[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
    return output.getvalue()

def make_download_link(bytes_obj, filename, label="Descargar resultado"):
    b64 = base64.b64encode(bytes_obj).decode()
    href = f"data:application/octet-stream;base64,{b64}"
    return f"<a href='{href}' download='{filename}'>{label}</a>"

# -----------------------------
# CSS Styling Mejorado
# -----------------------------
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    .stSidebar {display:none;}
    
    /* Fondo de la página con gradiente */
    .main .block-container {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 25%, #faf0f5 50%, #f0fff0 75%, #fff8dc 100%);
        background-attachment: fixed;
        min-height: 100vh;
        padding: 2rem;
        max-width: 1200px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 25%, #faf0f5 50%, #f0fff0 75%, #fff8dc 100%);
        background-attachment: fixed;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
        border-radius: 20px;
        border: 2px solid #2E86AB;
        box-shadow: 0 10px 30px rgba(46, 134, 171, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(46, 134, 171, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .company-logo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #2E86AB;
        box-shadow: 0 8px 32px rgba(46, 134, 171, 0.3);
        margin-bottom: 1rem;
    }
    
    .header-subtitle {
        color: #A23B72;
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 1rem;
        opacity: 0.9;
    }
    
    /* Sección de módulos */
    .sub-header {
        color: #A23B72;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background-color: #faf0f5;
        border-radius: 15px;
        border-left: 6px solid #A23B72;
        text-align: center;
        box-shadow: 0 4px 15px rgba(162, 59, 114, 0.1);
    }
    
    /* Grid de validadores */
    .validators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .validator-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .validator-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: #2E86AB;
    }
    
    .validator-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
    }
    
    .validator-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    .validator-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .validator-description {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Botones de acceso directo */
    .direct-access-btn {
        display: inline-block;
        width: 100%;
        padding: 1rem 2rem;
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        color: white;
        text-decoration: none;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        box-shadow: 0 5px 20px rgba(46, 134, 171, 0.3);
    }
    
    .direct-access-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(46, 134, 171, 0.4);
        text-decoration: none;
        color: white;
        background: linear-gradient(45deg, #A23B72, #2E86AB);
    }
    
    .ezytec-btn {
        background: linear-gradient(45deg, #28a745, #20c997);
        box-shadow: 0 5px 20px rgba(40, 167, 69, 0.3);
    }
    
    .ezytec-btn:hover {
        background: linear-gradient(45deg, #20c997, #28a745);
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
    }
    
    /* Sección especial para Ezytec */
    .ezytec-section {
        background: linear-gradient(135deg, #f0fff0, #e6ffe6);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid #28a745;
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.1);
    }
    
    .ezytec-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    /* Footer profesional */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        background: linear-gradient(90deg, #f8f9fa, #ffffff);
        border-radius: 20px;
        margin-top: 3rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .footer strong {
        color: #2E86AB;
        font-size: 1.2rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #d0e0ff;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(208, 224, 255, 0.2);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 1.5rem;
        }
        
        .validators-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .validator-card {
            padding: 1.5rem;
        }
        
        .company-logo {
            width: 80px;
            height: 80px;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header Principal con Logo
# -----------------------------
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <img src="https://i.imgur.com/z9xt46F.jpeg" alt="GoPass Logo" class="company-logo">
        <h1>GoPass Validador</h1>
        <p class="header-subtitle">Sistema Profesional de Validación y Control de Dobles Cobros</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sección Validadores de Dobles Cobros
# -----------------------------
st.markdown('<h2 class="sub-header">🔍 Validadores de Dobles Cobros</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="validators-grid">
    <div class="validator-card">
        <div class="validator-icon">🅿️</div>
        <h3 class="validator-title">Parqueaderos</h3>
        <p class="validator-description">
            Validación especializada para sistemas de parqueaderos y control de acceso vehicular. 
            Detecta anomalías en cobros de estacionamiento y tarifas irregulares.
        </p>
        <a href="https://validador-de-dobles-cobros-angeltorres.streamlit.app/" target="_blank" class="direct-access-btn">
            🚀 Acceder a Parqueaderos
        </a>
    </div>
    
    <div class="validator-card">
        <div class="validator-icon">⛽</div>
        <h3 class="validator-title">Gasolineras</h3>
        <p class="validator-description">
            Control avanzado de transacciones en estaciones de servicio y puntos de combustible. 
            Identifica duplicados en ventas de combustible.
        </p>
        <a href="https://dobles-cobros-terpel-angeltorres.streamlit.app/" target="_blank" class="direct-access-btn">
            🚀 Acceder a Gasolineras
        </a>
    </div>
    
    <div class="validator-card">
        <div class="validator-icon">🛣️</div>
        <h3 class="validator-title">Peajes</h3>
        <p class="validator-description">
            Validación para sistemas de cobro en peajes y vías de acceso controlado. 
            Monitoreo de transacciones en tiempo real.
        </p>
        <a href="#" class="direct-access-btn" onclick="alert('Módulo en desarrollo - Próximamente disponible')">
            🚧 Próximamente
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sección Validador Ezytec
# -----------------------------
st.markdown("""
<div class="ezytec-section">
    <h2 class="sub-header">⚡ Validador Ezytec</h2>
    <div class="ezytec-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚡</div>
        <h3 style="color: #28a745; font-size: 1.8rem; font-weight: bold; margin-bottom: 1rem;">
            Sistema Ezytec
        </h3>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem;">
            Validación especializada para el sistema Ezytec con algoritmos avanzados de detección 
            y procesamiento en tiempo real de transacciones.
        </p>
        <a href="https://validacion-ezytec-angeltorres.streamlit.app/" target="_blank" class="direct-access-btn ezytec-btn">
            ⚡ Acceder al Validador Ezytec
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Información adicional
# -----------------------------
st.markdown("""
<div class="info-box">
    <h3 style="color: #2E86AB; margin-bottom: 1rem;">ℹ️ Información Importante</h3>
    <ul style="color: #666; line-height: 1.8;">
        <li><strong>Acceso Directo:</strong> Cada botón te lleva directamente al validador correspondiente</li>
        <li><strong>Seguridad:</strong> Todos los enlaces abren en nuevas pestañas para mantener tu sesión</li>
        <li><strong>Soporte:</strong> Cada validador incluye ayuda contextual y ejemplos de uso</li>
        <li><strong>Rendimiento:</strong> Algoritmos optimizados para procesamiento rápido de grandes volúmenes</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Footer Profesional
# -----------------------------
st.markdown("""
<div class="footer">
    <p><strong>GoPass</strong> · Sistema Profesional de Validación</p>
    <p>Desarrollado con tecnología avanzada para garantizar la precisión en la detección de anomalías</p>
    <p>Interfaz intuitiva y acceso directo a todas las herramientas de validación</p>
    <p style="margin-top: 1rem; opacity: 0.7;">© 2024 GoPass. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
