import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import base64

st.set_page_config(page_title="GoPass - Validador", page_icon="https://i.imgur.com/z9xt46F.jpeg", layout="wide")

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
# UI: HTML + CSS header (component)
# -----------------------------

header_html = """
<div class="gopass-hero">
  ...
</div>

<style>
:root{
  --gopass-blue-1:#071428;
  --gopass-blue-2:#102a43;
  --gopass-accent:#0ea5a0;
  --glass: rgba(255,255,255,0.04);
}
.gopass-hero{display:flex;justify-content:space-between;align-items:center;padding:18px;border-radius:12px;background:linear-gradient(90deg,var(--gopass-blue-1),var(--gopass-blue-2));box-shadow:0 6px 30px rgba(2,6,23,0.6);color:white;margin-bottom:18px}
...
@media (max-width: 700px){.gopass-hero{flex-direction:column;align-items:flex-start;gap:12px}}
</style>
"""


st.components.v1.html(header_html, height=120)

# -----------------------------
# Sidebar: selección de grupos
# -----------------------------

st.sidebar.title("Módulos")
modo = st.sidebar.radio("Selecciona un grupo:", ("Validadores Dobles Cobros", "Validador Ezytec"))

if modo == "Validadores Dobles Cobros":
    st.sidebar.markdown("**Validadores:**")
    val_choice = st.sidebar.selectbox("Elige el validador:", ("Parqueaderos", "Gasolineras", "Peajes"))
else:
    val_choice = "Ezytec"

st.sidebar.markdown("---")
st.sidebar.markdown("Configuración general")
window = st.sidebar.number_input("Ventana tiempo (minutos) para detectar dobles cobros:", min_value=1, max_value=1440, value=60)

# -----------------------------
# Main content: cada validador
# -----------------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.header(f"{val_choice} — Validador")
st.markdown("</div>", unsafe_allow_html=True)

# Redirecciones específicas
if val_choice == "Gasolineras":
    st.markdown("<a class='btn' href='https://dobles-cobros-terpel-angeltorres.streamlit.app/' target='_blank'>Ir al Validador de Gasolineras</a>", unsafe_allow_html=True)
elif val_choice == "Parqueaderos":
    st.markdown("<a class='btn' href='https://validador-de-dobles-cobros-angeltorres.streamlit.app/' target='_blank'>Ir al Validador de Parqueaderos</a>", unsafe_allow_html=True)
elif val_choice == "Ezytec":
    st.markdown("<a class='btn' href='https://validacion-ezytec-angeltorres.streamlit.app/' target='_blank'>Ir al Validador Ezytec</a>", unsafe_allow_html=True)
else:
    st.info("Este módulo aún no tiene un enlace externo asignado.")

st.markdown("---")
st.markdown("<div class='small-muted'>GoPass · Validador · Interfaz creada con Streamlit — código suministrado</div>", unsafe_allow_html=True)
