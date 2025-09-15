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
# CSS Styling
# -----------------------------
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    
    /* Variables CSS */
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #3b82f6;
        --accent-teal: #0d9488;
        --success-green: #059669;
        --warning-orange: #d97706;
        --danger-red: #dc2626;
        --dark-bg: #0f172a;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-light: #e2e8f0;
        --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Estilo general */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header profesional */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .professional-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
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
    
    .logo-container {
        margin-bottom: 1.5rem;
    }
    
    .company-logo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Cards para módulos */
    .modules-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .module-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.15);
    }
    
    .module-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-teal), var(--secondary-blue));
    }
    
    .module-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .module-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    
    .module-description {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* Botones profesionales */
    .professional-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, var(--accent-teal) 0%, var(--success-green) 100%);
        color: white;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3);
    }
    
    .professional-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
        text-decoration: none;
        color: white;
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, var(--text-secondary) 0%, var(--text-primary) 100%);
        box-shadow: 0 4px 15px rgba(100, 116, 139, 0.3);
    }
    
    .btn-secondary:hover {
        box-shadow: 0 6px 20px rgba(100, 116, 139, 0.4);
    }
    
    /* Sección de configuración */
    .config-section {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-light);
    }
    
    .config-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Footer */
    .professional-footer {
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        border-top: 1px solid var(--border-light);
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    /* Estados activos */
    .module-active {
        border: 2px solid var(--accent-teal);
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .professional-header {
            padding: 2rem 1rem;
        }
        
        .header-title {
            font-size: 2rem;
        }
        
        .modules-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .module-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header Profesional
# -----------------------------
st.markdown("""
<div class="professional-header">
    <div class="header-content">
        <div class="logo-container">
            <img src="https://i.imgur.com/z9xt46F.jpeg" alt="GoPass Logo" class="company-logo">
        </div>
        <h1 class="header-title">GoPass Validador</h1>
        <p class="header-subtitle">Sistema Profesional de Validación y Control de Dobles Cobros</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sistema de navegación con estado
# -----------------------------
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = None

if 'selected_validator' not in st.session_state:
    st.session_state.selected_validator = None

# -----------------------------
# Módulos principales
# -----------------------------
st.markdown("## 🎯 Selecciona un Módulo")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Validadores Dobles Cobros", key="dobles_cobros", use_container_width=True):
        st.session_state.selected_module = "dobles_cobros"
        st.session_state.selected_validator = None

with col2:
    if st.button("⚡ Validador Ezytec", key="ezytec", use_container_width=True):
        st.session_state.selected_module = "ezytec"
        st.session_state.selected_validator = "Ezytec"

# -----------------------------
# Configuración global
# -----------------------------
st.markdown("""
<div class="config-section">
    <h3 class="config-title">⚙️ Configuración General</h3>
</div>
""", unsafe_allow_html=True)

window = st.slider(
    "🕐 Ventana de tiempo para detectar dobles cobros (minutos):",
    min_value=1,
    max_value=1440,
    value=60,
    help="Define el tiempo máximo entre transacciones para considerarlas como posible doble cobro"
)

# -----------------------------
# Contenido dinámico según selección
# -----------------------------
if st.session_state.selected_module == "dobles_cobros":
    st.markdown("---")
    st.markdown("## 🚗 Validadores de Dobles Cobros")
    st.markdown("Selecciona el tipo de validador específico:")
    
    # Grid de validadores
    st.markdown("""
    <div class="modules-grid">
        <div class="module-card">
            <div class="module-icon">🅿️</div>
            <h3 class="module-title">Parqueaderos</h3>
            <p class="module-description">Validación especializada para sistemas de parqueaderos y control de acceso vehicular.</p>
        </div>
        
        <div class="module-card">
            <div class="module-icon">⛽</div>
            <h3 class="module-title">Gasolineras</h3>
            <p class="module-description">Control de transacciones en estaciones de servicio y puntos de combustible.</p>
        </div>
        
        <div class="module-card">
            <div class="module-icon">🛣️</div>
            <h3 class="module-title">Peajes</h3>
            <p class="module-description">Validación para sistemas de cobro en peajes y vías de acceso controlado.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🅿️ Ir a Parqueaderos", key="btn_parqueaderos", use_container_width=True):
            st.session_state.selected_validator = "Parqueaderos"
    
    with col2:
        if st.button("⛽ Ir a Gasolineras", key="btn_gasolineras", use_container_width=True):
            st.session_state.selected_validator = "Gasolineras"
    
    with col3:
        if st.button("🛣️ Ir a Peajes", key="btn_peajes", use_container_width=True):
            st.session_state.selected_validator = "Peajes"

elif st.session_state.selected_module == "ezytec":
    st.markdown("---")
    st.markdown("## ⚡ Validador Ezytec")
    
    st.markdown("""
    <div class="module-card module-active">
        <div class="module-icon">⚡</div>
        <h3 class="module-title">Sistema Ezytec</h3>
        <p class="module-description">Validación especializada para el sistema Ezytec con algoritmos avanzados de detección.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Redirección a validadores específicos
# -----------------------------
if st.session_state.selected_validator:
    st.markdown("---")
    st.markdown(f"### 🎯 Validador Seleccionado: {st.session_state.selected_validator}")
    
    # Links de redirección con botones profesionales
    validator_links = {
        "Gasolineras": "https://dobles-cobros-terpel-angeltorres.streamlit.app/",
        "Parqueaderos": "https://validador-de-dobles-cobros-angeltorres.streamlit.app/",
        "Ezytec": "https://validacion-ezytec-angeltorres.streamlit.app/"
    }
    
    if st.session_state.selected_validator in validator_links:
        link = validator_links[st.session_state.selected_validator]
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="{link}" target="_blank" class="professional-btn">
                🚀 Acceder al Validador {st.session_state.selected_validator}
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Información adicional
        st.info(f"📋 **Configuración aplicada:** Ventana de tiempo de {window} minutos para detección de dobles cobros.")
        
        # Botón para volver
        if st.button("🔙 Volver al menú principal", key="back_button"):
            st.session_state.selected_module = None
            st.session_state.selected_validator = None
            st.experimental_rerun()
    else:
        st.warning("⚠️ Este validador aún no tiene un enlace configurado.")

# -----------------------------
# Footer profesional
# -----------------------------
st.markdown("""
<div class="professional-footer">
    <p><strong>GoPass</strong> · Sistema Profesional de Validación</p>
    <p>Desarrollado con tecnología avanzada para garantizar la precisión en la detección de anomalías</p>
    <p>© 2024 GoPass. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
