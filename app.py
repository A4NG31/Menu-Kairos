import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import base64

# ============================
# Configuración de página
# ============================
st.set_page_config(
    page_title="GoPass - Validador Profesional",
    page_icon="https://i.imgur.com/PgN46mi.jpeg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================
# Funciones auxiliares
# ============================
def to_excel_bytes(df_dict):
    """Convierte múltiples DataFrames en un solo archivo Excel en memoria"""
    from openpyxl import Workbook
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, df in df_dict.items():
            sheet_name = str(name)[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output.getvalue()

def make_download_link(bytes_obj, filename, label="Descargar resultado"):
    """Crea un enlace HTML para descargar un archivo generado"""
    b64 = base64.b64encode(bytes_obj).decode()
    href = f"data:application/octet-stream;base64,{b64}"
    return f"<a href='{href}' download='{filename}'>{label}</a>"

# ============================
# Estilos CSS
# ============================
st.markdown("""<style>
/* Ocultar elementos de Streamlit */
.stDeployButton, footer, .stDecoration, .stSidebar {display:none;}
/* Fondo principal */
.main .block-container, .stApp {
    background: linear-gradient(135deg, #0f1419, #1a202c 25%, #2d3748 50%, #1a202c 75%, #0f1419);
    background-attachment: fixed;
}
/* Header */
.main-header {
    text-align: center; color: #fff; font-size: 2.8rem; font-weight: 800;
    margin-bottom: 3rem; padding: 3rem 2rem;
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 25px; box-shadow: 0 20px 40px rgba(16,185,129,0.3);
    position: relative; overflow: hidden;
}
.main-header img {width:120px; height:120px; border-radius:50%; margin-bottom:1rem; border:3px solid #fff;}
.sub-header {
    color:#fff; font-size:2rem; font-weight:700; margin:3rem 0 2rem;
    padding:1.5rem 2rem; background:linear-gradient(135deg,#047857,#065f46);
    border-radius:20px; text-align:center;
}
/* Tarjetas */
.validators-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(380px,1fr));
    gap:2.5rem; margin:3rem 0;
}
.validator-card {
    background:linear-gradient(145deg,#fff,#f7fafc);
    border-radius:25px; padding:2.5rem;
    box-shadow:0 20px 25px -5px rgba(0,0,0,0.1);
    border:2px solid #e2e8f0; transition:all 0.3s;
}
.validator-card:hover {transform:translateY(-10px); border-color:#10b981;}
.validator-title {font-size:1.8rem; font-weight:700; color:#2d3748; text-align:center;}
.validator-description {color:#4a5568; text-align:center; margin:1rem 0;}
.direct-access-btn {
    display:block; width:100%; padding:1.2rem;
    background:linear-gradient(135deg,#10b981,#059669);
    color:#fff; border:none; border-radius:15px; font-size:1.2rem; font-weight:600;
    cursor:pointer; transition:0.3s;
}
.direct-access-btn:hover {background:linear-gradient(135deg,#059669,#047857);}
.footer {
    text-align:center; padding:3rem 2rem; color:#e2e8f0;
    background:linear-gradient(135deg,#2d3748,#1a202c);
    border-radius:25px; margin-top:4rem;
}
</style>""", unsafe_allow_html=True)

# ============================
# Header Principal
# ============================
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <img src="https://i.imgur.com/PgN46mi.jpeg">
        <h1>Kairos Menú</h1>
        <p class="header-subtitle">Sistema Profesional de Validación y Control de Dobles Cobros</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================
# Sección Validadores
# ============================
st.markdown('<h2 class="sub-header">🔍 Validadores de Dobles Cobros</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="validators-grid">

    <div class="validator-card">
        <div class="validator-icon">🅿️</div>
        <h3 class="validator-title">Parqueaderos</h3>
        <p class="validator-description">
            Validación especializada para sistemas de parqueaderos. Detecta anomalías en cobros de estacionamiento.
        </p>
        <a href="https://validador-de-dobles-cobros-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚀 Acceder al Validador de Parqueaderos</button>
        </a>
    </div>

    <div class="validator-card">
        <div class="validator-icon">🛣️</div>
        <h3 class="validator-title">Peajes</h3>
        <p class="validator-description">
            Validación para sistemas de cobro en peajes. 🚧⚠️ Módulo en construcción ⚠️🚧
        </p>
        <a href="https://dobles-cobros-terpel-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚧 Acceder al Validador de Peajes</button>
        </a>
    </div>

    <div class="validator-card">
        <div class="validator-icon">⛽</div>
        <h3 class="validator-title">Gasolineras</h3>
        <p class="validator-description">
            Control avanzado de transacciones en estaciones de servicio. Detecta cobros duplicados. TERPEL
        </p>
        <a href="https://dobles-cobros-terpel-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚀 Acceder al Validador de Gasolineras</button>
        </a>
    </div>

    <div class="validator-card">
        <div class="validator-icon">🚗</div>
        <h3 class="validator-title">Skidata</h3>
        <p class="validator-description">
            Validación especializada para Skidata con dashboard interactivo.
        </p>
        <a href="https://skidata-dobles-cobros-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🚀 Acceder al Validador de Skidata</button>
        </a>
    </div>

</div>
""", unsafe_allow_html=True)

# ============================
# Ezytec y Cybersource
# ============================
st.markdown("""
<div style="display:flex;flex-wrap:wrap;gap:40px;justify-content:center;">

    <div class="validator-card" style="max-width:48%;">
        <h2 class="sub-header">⚡ Validador Ezytec</h2>
        <img src="https://i.imgur.com/NGGCVFZ.png" style="width:150px;margin-bottom:1rem;">
        <p class="validator-description">
            Validación avanzada con algoritmos de detección en tiempo real.
        </p>
        <a href="https://validacion-ezytec-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">⚡ Acceder al Validador Ezytec</button>
        </a>
    </div>

    <div class="validator-card" style="max-width:48%;">
        <h2 class="sub-header">🌐 Validador Códigos Cybersource</h2>
        <img src="https://i.imgur.com/e22Lpxv.png" style="width:150px;margin-bottom:1rem;">
        <p class="validator-description">
            Validación de transacciones con IA para la pasarela Cybersource.
        </p>
        <a href="https://codigos-pasarela-angeltorres.streamlit.app/" target="_blank">
            <button class="direct-access-btn">🌐 Acceder al Validador Cybersource</button>
        </a>
    </div>

</div>
""", unsafe_allow_html=True)

# ============================
# Power BI
# ============================
st.markdown("""
<div class="validator-card">
    <h2 class="sub-header">📈 Menú reportes BI</h2>
    <img src="https://i.imgur.com/PZFyGpU.png" style="width:260px;margin-bottom:1rem;">
    <p class="validator-description">
        Acceso directo a reportes Power BI para análisis y validaciones.
    </p>
    <a href="https://app.powerbi.com/view?r=eyJrIjoiNzhjOWEwMzctNmZhYy00NjE1LThjZjctNDVlMjdmMmFlNDlmIiwidCI6ImY5MTdlZDFiLWI0MDMtNDljNS1iODBiLWJhYWUzY2UwMzc1YSJ9" target="_blank">
        <button class="direct-access-btn">📈 Acceder a Power BI</button>
    </a>
</div>
""", unsafe_allow_html=True)

# ============================
# Motores de Facturación
# ============================
st.markdown("""
<div class="validator-card">
    <h2 class="sub-header">🧾 Validador Motores Facturación</h2>
    <img src="https://i.imgur.com/VbDfzO5.png" style="width:240px;margin-bottom:1rem;">
    <p class="validator-description">
        Validación especializada mediante scrapping en diferentes portales.
    </p>
    <a href="https://auto-motores-facturacion-angeltorres.streamlit.app/" target="_blank">
        <button class="direct-access-btn">🧾 Acceder al Validador de Facturación</button>
    </a>
</div>
""", unsafe_allow_html=True)

# ============================
# Footer
# ============================
st.markdown("""
<div class="footer">
    <p><strong>GoPass</strong> · Sistema Profesional de Validación</p>
    <p>Desarrollado por Angel Torres</p>
    <p>© 2025 GoPass. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
