import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import base64

# Configuración de página
st.set_page_config(
    page_title="GoPass - Validador Profesional", 
    page_icon="https://i.imgur.com/PgN46mi.jpeg", 
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
# CSS Styling Profesional
# -----------------------------
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    .stSidebar {display:none;}
    
    /* Fondo profesional con gradiente suave */
    .main .block-container {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 25%, #2d3748 50%, #1a202c 75%, #0f1419 100%);
        background-attachment: fixed;
        min-height: 100vh;
        padding: 2rem;
        max-width: 1200px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 25%, #2d3748 50%, #1a202c 75%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    /* Header principal con verde GoPass */
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 3rem;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 25px;
        border: none;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
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
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 25s linear infinite;
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
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid rgba(255,255,255,0.8);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .company-logo:hover {
        transform: scale(1.05);
    }
    
    .header-subtitle {
        color: #e2e8f0;
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 1rem;
        opacity: 0.95;
        line-height: 1.5;
    }
    
    /* Títulos de secciones con verde profesional */
    .sub-header {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 3rem 0 2rem 0;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        border-radius: 20px;
        border-left: 6px solid #34d399;
        text-align: center;
        box-shadow: 0 10px 25px rgba(4, 120, 87, 0.25);
        position: relative;
    }
    
    .sub-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #34d399, #10b981);
        border-radius: 0 0 20px 20px;
    }
    
    /* Grid de validadores */
    .validators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
        gap: 2.5rem;
        margin: 3rem 0;
    }
    
    .validator-card {
        background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 2px solid #e2e8f0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .validator-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.25),
            0 20px 20px -5px rgba(0, 0, 0, 0.1);
        border-color: #10b981;
    }
    
    .validator-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #10b981 0%, #059669 50%, #34d399 100%);
    }
    
    .validator-icon {
        font-size: 4.5rem;
        margin-bottom: 1.5rem;
        display: block;
        text-align: center;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .validator-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
        text-align: center;
        line-height: 1.2;
    }
    
    .validator-description {
        color: #4a5568;
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 2.5rem;
        text-align: center;
        font-weight: 400;
    }
    
    /* Botones profesionales con verde GoPass */
    .direct-access-btn {
        display: inline-block;
        width: 100%;
        padding: 1.2rem 2.5rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        text-decoration: none;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .direct-access-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .direct-access-btn:hover::before {
        left: 100%;
    }
    
    .direct-access-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4);
        text-decoration: none;
        color: #ffffff;
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    .direct-access-btn:active {
        transform: translateY(-1px);
    }
    
    /* Botón Ezytec con verde más intenso */
    .ezytec-btn {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 10px 20px rgba(5, 150, 105, 0.3);
    }
    
    .ezytec-btn:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 15px 30px rgba(5, 150, 105, 0.4);
    }
    
    /* Botón deshabilitado */
    .btn-disabled {
        background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
        box-shadow: 0 5px 15px rgba(160, 174, 192, 0.2);
        cursor: not-allowed;
    }
    
    .btn-disabled:hover {
        transform: none;
        background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
        box-shadow: 0 5px 15px rgba(160, 174, 192, 0.2);
    }
    
    /* Sección Ezytec con verde corporativo */
    .ezytec-section {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin: 3rem 0;
        border: 3px solid #10b981;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .ezytec-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
        animation: rotate 30s linear infinite reverse;
    }
    
    .ezytec-card {
        background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }
    
    /* Info boxes con verde profesional */
    .info-box {
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #10b981;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.15);
        color: #064e3b;
    }
    
    .info-box h3 {
        color: #047857;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .info-box ul {
        color: #065f46;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    .info-box strong {
        color: #064e3b;
        font-weight: 600;
    }
    
    /* Footer profesional */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #e2e8f0;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 25px;
        margin-top: 4rem;
        border: 2px solid #4a5568;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    .footer strong {
        color: #10b981;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .footer p {
        margin: 0.8rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Responsive mejorado */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.2rem;
            padding: 2rem 1.5rem;
        }
        
        .validators-grid {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        .validator-card {
            padding: 2rem;
        }
        
        .company-logo {
            width: 100px;
            height: 100px;
        }
        
        .sub-header {
            font-size: 1.6rem;
            padding: 1rem 1.5rem;
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
        <img src="https://i.imgur.com/PgN46mi.jpeg">
        <h1>Kairos Menú</h1>
        <p class="header-subtitle">Sistema Profesional de Validación y Control de Dobles Cobros</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sección Validadores de Dobles Cobros
# -----------------------------
st.markdown('<h2 class="sub-header">🔍 Validadores de Dobles Cobros</h2>', unsafe_allow_html=True)

# Función JavaScript para redirección
st.markdown("""
<script>
function redirectTo(url) {
    window.open(url, '_blank');
}
function showAlert(message) {
    alert(message);
}
</script>
""", unsafe_allow_html=True)

st.markdown("""
<div class="validators-grid">
    <div class="validator-card">
        <div class="validator-icon">🅿️</div>
        <h3 class="validator-title">Parqueaderos</h3>
        <p class="validator-description">
            Validación especializada para sistemas de parqueaderos y control de acceso vehicular. 
            Detecta anomalías en cobros de estacionamiento y tarifas irregulares con algoritmos avanzados.
        </p>
        <a href="https://validador-de-dobles-cobros-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚀 Acceder al Validador de Parqueaderos</button>
        </a>
    </div>
    
   <div class="validator-card">
        <div class="validator-icon">🛣️</div>
        <h3 class="validator-title">Peajes</h3>
        <p class="validator-description">
            🚧Validación para sistemas de cobro en peajes y vías de acceso controlado. 
            Monitoreo de transacciones en tiempo real y detección de irregularidades.
            🚨⚠️MODULO EN CONSTRUCCIÓN⚠️🚨🚧
        </p>
        <a href="https://dobles-cobros-terpel-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚧🚀 Acceder al Validador de Peajes🚧</button>
        </a>
    </div>

   <div class="validator-card">
        <div class="validator-icon">⛽</div>
        <h3 class="validator-title">Gasolineras</h3>
        <p class="validator-description">
            Control avanzado de transacciones en estaciones de servicio y puntos de combustible. 
            Identifica duplicados en ventas de combustible y anomalías en el sistema de facturación.
        </p>
        <a href="https://dobles-cobros-terpel-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚀 Acceder al Validador de Gasolineras</button>
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
        <div style="text-align: center; margin-bottom: 1.5rem;">
        <img src="https://i.imgur.com/mWsxLPA.png" alt="Ezytec" style="width: 150px; height: 140px;">
        </div>
        <h3 style="color: #047857; font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;">
            Sistema Ezytec
        </h3>
        <p style="color: #4a5568; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2.5rem;">
            Validación especializada para el sistema Ezytec con algoritmos avanzados de detección 
            y procesamiento en tiempo real de transacciones. Tecnología de punta para máxima precisión.
        </p>
        <a href="https://validacion-ezytec-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn ezytec-btn">⚡ Acceder al Validador Ezytec</button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sección Validador Codigos Pasarela Cybersource
# -----------------------------
st.markdown("""
<div class="ezytec-section">
    <h2 class="sub-header">🌐 Validador Códigos Cybersource</h2>
    <div class="ezytec-card">
        <div style="text-align: center; margin-bottom: 1.5rem;">
        <img src="https://i.imgur.com/e22Lpxv.png" alt="Cybersource" style="width: 150px; height: 140px;">
        </div>
        <h3 style="color: #1E3A8A; font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;">
            Pasarela Cybersource
        </h3>
        <p style="color: #4a5568; font-size: 1.1rem; line-height: 1.7; margin-bottom: 2.5rem;">
            Validación especializada de códigos y transacciones mediante <strong>IA</strong> en la pasarela de pago Cybersource. 
            Asegura la detección de errores y anomalías con algoritmos optimizados para procesos financieros críticos.
        </p>
        <a href="https://codigos-pasarela-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn ezytec-btn">🌐 Acceder al Validador Cybersource</button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Información adicional
# -----------------------------
st.markdown("""
<div class="info-box">
    <h3>ℹ️ Información Importante</h3>
    <ul>
        <li><strong>Acceso Directo:</strong> Cada botón te lleva directamente al validador correspondiente en una nueva pestaña</li>
        <li><strong>Seguridad:</strong> Conexiones seguras y encriptadas para proteger tus datos</li>
        <li><strong>Soporte:</strong> Cada validador incluye ayuda contextual, ejemplos y documentación completa</li>
        <li><strong>Rendimiento:</strong> Algoritmos optimizados para procesamiento rápido de grandes volúmenes de datos</li>
        <li><strong>Actualizaciones:</strong> Sistema en constante mejora con nuevas funcionalidades</li>
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
    <p>Soporte técnico especializado y actualizaciones continuas</p>
    <p>Desarrollado por Angel Torres</p>
    <p style="margin-top: 2rem; opacity: 0.8; font-size: 0.9rem;">© 2025 GoPass. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
