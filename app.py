import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="GoPass - Validadores",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado inspirado en el diseño elegante
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding: 0;
        background: linear-gradient(135deg, #0a4d3a 0%, #1a5f4a 50%, #2d7a5f 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Header personalizado */
    .custom-header {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: 20px;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    
    .logo-container img {
        height: 60px;
        margin-right: 15px;
    }
    
    .main-title {
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        margin: 5px 0 0 0;
        font-weight: 300;
    }
    
    /* Contenedor principal */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Grupos de módulos */
    .module-group {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .group-title {
        color: #0a4d3a;
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 20px;
        text-align: center;
        position: relative;
    }
    
    .group-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #2d7a5f, #1a5f4a);
        border-radius: 2px;
    }
    
    /* Botones de módulos */
    .module-button {
        background: linear-gradient(135deg, #2d7a5f 0%, #1a5f4a 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        width: calc(33.333% - 20px);
        min-height: 120px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 8px 25px rgba(45, 122, 95, 0.3);
        display: inline-block;
        text-align: center;
        text-decoration: none;
    }
    
    .module-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(45, 122, 95, 0.4);
        background: linear-gradient(135deg, #3d8a6f 0%, #2a6f5a 100%);
    }
    
    .module-button-single {
        width: calc(50% - 20px);
        background: linear-gradient(135deg, #4a7c59 0%, #2d5a3d 100%);
    }
    
    .module-button-single:hover {
        background: linear-gradient(135deg, #5a8c69 0%, #3d6a4d 100%);
    }
    
    /* Iconos para los módulos */
    .module-icon {
        font-size: 2rem;
        margin-bottom: 10px;
        display: block;
    }
    
    /* Formularios */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid rgba(45, 122, 95, 0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2d7a5f;
        box-shadow: 0 0 0 2px rgba(45, 122, 95, 0.2);
    }
    
    /* Botones de Streamlit */
    .stButton > button {
        background: linear-gradient(135deg, #2d7a5f 0%, #1a5f4a 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3d8a6f 0%, #2a6f5a 100%);
        transform: translateY(-2px);
    }
    
    /* Tablas */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Alertas */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #2d7a5f;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .module-button, .module-button-single {
            width: calc(100% - 20px);
            margin: 10px 0;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .module-group {
            padding: 20px;
            margin: 20px 0;
        }
    }
    
    /* Efectos de partículas de fondo */
    .background-pattern {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.1;
        z-index: -1;
        background-image: 
            radial-gradient(circle at 25% 25%, #ffffff 2px, transparent 2px),
            radial-gradient(circle at 75% 75%, #ffffff 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Patrón de fondo
    st.markdown('<div class="background-pattern"></div>', unsafe_allow_html=True)
    
    # Header personalizado
    st.markdown("""
    <div class="custom-header">
        <div class="logo-container">
            <img src="https://i.imgur.com/z9xt46F.jpeg" alt="GoPass Logo">
        </div>
        <h1 class="main-title">GOPASS</h1>
        <p class="subtitle">Sistema de Validación Inteligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor principal
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Inicializar estado de sesión
    if 'current_module' not in st.session_state:
        st.session_state.current_module = 'home'
    
    # Navegación
    if st.session_state.current_module == 'home':
        show_home()
    elif st.session_state.current_module == 'parqueaderos':
        validador_parqueaderos()
    elif st.session_state.current_module == 'gasolineras':
        validador_gasolineras()
    elif st.session_state.current_module == 'peajes':
        validador_peajes()
    elif st.session_state.current_module == 'ezytec':
        validador_ezytec()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    # Grupo 1: Validadores de Dobles Cobros
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">🔍 Validadores de Dobles Cobros</h2>
        <div style="text-align: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🅿️ PARQUEADEROS", key="park", help="Validar dobles cobros en parqueaderos"):
            st.markdown("""
            <script>
                window.open('https://validador-de-dobles-cobros-angeltorres.streamlit.app/', '_blank');
            </script>
            """, unsafe_allow_html=True)
            st.info("🔗 Redirigiendo al validador de parqueaderos...")
    
    with col2:
        if st.button("⛽ GASOLINERAS", key="gas", help="Validar dobles cobros en gasolineras"):
            st.markdown("""
            <script>
                window.open('https://dobles-cobros-terpel-angeltorres.streamlit.app/', '_blank');
            </script>
            """, unsafe_allow_html=True)
            st.info("🔗 Redirigiendo al validador de gasolineras...")
    
    with col3:
        if st.button("🛣️ PEAJES", key="toll", help="Validar dobles cobros en peajes"):
            st.session_state.current_module = 'peajes'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Grupo 2: Validador Ezytec
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">⚡ Validador Especializado</h2>
        <div style="text-align: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔧 VALIDADOR EZYTEC", key="ezytec", help="Validador especializado Ezytec"):
            st.markdown("""
            <script>
                window.open('https://validacion-ezytec-angeltorres.streamlit.app/', '_blank');
            </script>
            """, unsafe_allow_html=True)
            st.info("🔗 Redirigiendo al validador Ezytec...")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Información adicional
    st.markdown("""
    <div class="module-group">
        <h3 style="color: #0a4d3a; text-align: center; margin-bottom: 20px;">📊 Información del Sistema</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: center;">
            <div style="padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px;">
                <h4 style="color: #2d7a5f; margin-bottom: 10px;">🎯 Precisión</h4>
                <p style="color: #666; margin: 0;">Detección avanzada de duplicados</p>
            </div>
            <div style="padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px;">
                <h4 style="color: #2d7a5f; margin-bottom: 10px;">⚡ Velocidad</h4>
                <p style="color: #666; margin: 0;">Procesamiento en tiempo real</p>
            </div>
            <div style="padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px;">
                <h4 style="color: #2d7a5f; margin-bottom: 10px;">🔒 Seguridad</h4>
                <p style="color: #666; margin: 0;">Datos protegidos y encriptados</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def validador_parqueaderos():
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">🅿️ Validador de Dobles Cobros - Parqueaderos</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Volver al Inicio", key="back_park"):
        st.session_state.current_module = 'home'
        st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 Configuración")
        
        fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
        fecha_fin = st.date_input("Fecha de fin", value=date.today())
        
        tipo_validacion = st.selectbox(
            "Tipo de validación",
            ["Por placa", "Por hora", "Por monto", "Combinada"]
        )
        
        tolerancia = st.slider("Tolerancia (minutos)", 0, 60, 15)
        
    with col2:
        st.subheader("📁 Cargar Datos")
        
        uploaded_file = st.file_uploader(
            "Selecciona el archivo de transacciones",
            type=['csv', 'xlsx', 'xls'],
            help="Formatos soportados: CSV, Excel"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Archivo cargado: {len(df)} registros")
                
                if st.button("🔍 Ejecutar Validación", type="primary"):
                    with st.spinner("Procesando validación..."):
                        # Simulación de procesamiento
                        import time
                        time.sleep(2)
                        
                        # Resultados simulados
                        duplicados = len(df) // 10  # 10% de duplicados simulados
                        
                        st.success(f"✅ Validación completada")
                        
                        col_res1, col_res2, col_res3 = st.columns(3)
                        with col_res1:
                            st.metric("Total Registros", len(df))
                        with col_res2:
                            st.metric("Duplicados Encontrados", duplicados, delta=f"-{duplicados}")
                        with col_res3:
                            st.metric("Registros Únicos", len(df) - duplicados)
                        
                        if duplicados > 0:
                            st.warning(f"⚠️ Se encontraron {duplicados} posibles dobles cobros")
                            
                            # Tabla de ejemplo de duplicados
                            st.subheader("📊 Duplicados Detectados")
                            duplicados_df = pd.DataFrame({
                                'Placa': ['ABC123', 'XYZ789', 'DEF456'],
                                'Fecha': ['2024-01-15', '2024-01-15', '2024-01-16'],
                                'Hora_1': ['10:30', '14:20', '09:15'],
                                'Hora_2': ['10:35', '14:25', '09:18'],
                                'Monto': ['$5,000', '$8,000', '$6,500'],
                                'Diferencia_Min': [5, 5, 3]
                            })
                            st.dataframe(duplicados_df, use_container_width=True)
                        else:
                            st.success("🎉 No se encontraron dobles cobros")
                            
            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {str(e)}")

def validador_gasolineras():
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">⛽ Validador de Dobles Cobros - Gasolineras</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Volver al Inicio", key="back_gas"):
        st.session_state.current_module = 'home'
        st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Validación", "⚙️ Configuración", "📈 Reportes"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Parámetros de Validación")
            
            estacion = st.selectbox(
                "Estación de servicio",
                ["Todas", "Terpel", "Mobil", "Esso", "Petrobras", "Shell"]
            )
            
            tipo_combustible = st.multiselect(
                "Tipo de combustible",
                ["Gasolina Corriente", "Gasolina Extra", "Diesel", "Gas Natural"],
                default=["Gasolina Corriente"]
            )
            
            rango_monto = st.slider(
                "Rango de monto a validar",
                0, 500000, (10000, 200000),
                step=5000,
                format="$%d"
            )
            
        with col2:
            st.subheader("📁 Datos de Entrada")
            
            uploaded_file = st.file_uploader(
                "Archivo de transacciones de gasolineras",
                type=['csv', 'xlsx'],
                key="gas_file"
            )
            
            if uploaded_file:
                st.info("📋 Vista previa de datos disponible después de cargar")
                
                if st.button("🚀 Iniciar Validación", type="primary"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        status_text.text(f'Procesando... {i+1}%')
                        time.sleep(0.01)
                    
                    st.success("✅ Validación de gasolineras completada")
                    
                    # Métricas de resultado
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    with col_m1:
                        st.metric("Transacciones", "1,247")
                    with col_m2:
                        st.metric("Duplicados", "23", delta="-23")
                    with col_m3:
                        st.metric("Ahorro", "$1,150,000", delta="1150000")
                    with col_m4:
                        st.metric("Eficiencia", "98.2%", delta="2.1%")
    
    with tab2:
        st.subheader("⚙️ Configuración Avanzada")
        
        col_cfg1, col_cfg2 = st.columns(2)
        
        with col_cfg1:
            st.write("**Criterios de Detección**")
            
            tiempo_tolerancia = st.number_input(
                "Tolerancia de tiempo (minutos)",
                min_value=1,
                max_value=120,
                value=10
            )
            
            monto_tolerancia = st.number_input(
                "Tolerancia de monto (%)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1
            )
            
            validar_placa = st.checkbox("Validar por placa", value=True)
            validar_ubicacion = st.checkbox("Validar por ubicación", value=True)
            
        with col_cfg2:
            st.write("**Filtros Adicionales**")
            
            excluir_corporativos = st.checkbox("Excluir clientes corporativos", value=False)
            solo_efectivo = st.checkbox("Solo transacciones en efectivo", value=False)
            
            horario_inicio = st.time_input("Horario de inicio")
            horario_fin = st.time_input("Horario de fin")
    
    with tab3:
        st.subheader("📈 Reportes y Estadísticas")
        
        # Gráfico simulado
        import numpy as np
        
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Duplicados Detectados', 'Falsos Positivos', 'Ahorro Generado']
        )
        
        st.line_chart(chart_data)
        
        st.subheader("📋 Resumen Ejecutivo")
        st.info("""
        **Resumen del último período:**
        - Total de transacciones analizadas: 15,847
        - Dobles cobros detectados: 127 (0.8%)
        - Ahorro total generado: $8,450,000
        - Tiempo de procesamiento: 2.3 segundos
        - Precisión del algoritmo: 97.8%
        """)

def validador_peajes():
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">🛣️ Validador de Dobles Cobros - Peajes</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Volver al Inicio", key="back_toll"):
        st.session_state.current_module = 'home'
        st.rerun()
    
    st.markdown("---")
    
    # Layout principal
    col_main1, col_main2 = st.columns([2, 1])
    
    with col_main1:
        st.subheader("🎯 Configuración de Validación")
        
        # Selección de peajes
        peajes_disponibles = [
            "Peaje Autopista Norte",
            "Peaje Bogotá-Girardot",
            "Peaje Medellín-Bogotá",
            "Peaje Cali-Buenaventura",
            "Peaje Barranquilla-Cartagena",
            "Todos los peajes"
        ]
        
        peaje_seleccionado = st.selectbox(
            "Seleccionar peaje",
            peajes_disponibles,
            index=len(peajes_disponibles)-1
        )
        
        # Configuración de fechas
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            fecha_inicio = st.date_input("Fecha inicio", value=date.today())
        with col_date2:
            fecha_fin = st.date_input("Fecha fin", value=date.today())
        
        # Configuración de categorías
        categorias = st.multiselect(
            "Categorías de vehículos",
            ["Categoría I (Autos)", "Categoría II (Buses)", "Categoría III (Camiones)", 
             "Categoría IV (Tractomulas)", "Categoría V (Especiales)"],
            default=["Categoría I (Autos)"]
        )
        
        # Parámetros avanzados
        with st.expander("⚙️ Configuración Avanzada"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                ventana_tiempo = st.slider(
                    "Ventana de tiempo para duplicados (minutos)",
                    5, 60, 15
                )
                
                sensibilidad = st.select_slider(
                    "Sensibilidad de detección",
                    options=["Baja", "Media", "Alta", "Muy Alta"],
                    value="Alta"
                )
            
            with col_adv2:
                incluir_exentos = st.checkbox("Incluir vehículos exentos")
                validar_sentido = st.checkbox("Validar sentido de viaje", value=True)
    
    with col_main2:
        st.subheader("📊 Estado del Sistema")
        
        # Métricas en tiempo real
        st.metric("🚗 Transacciones Hoy", "2,847", delta="147")
        st.metric("⚠️ Alertas Activas", "3", delta="-2")
        st.metric("💰 Ahorro del Mes", "$2.1M", delta="340K")
        
        # Estado de conexión
        st.success("🟢 Sistema Operativo")
        st.info("🔄 Última actualización: Hace 2 min")
        
        # Botón de validación
        if st.button("🚀 EJECUTAR VALIDACIÓN", type="primary", use_container_width=True):
            # Simulación de procesamiento
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    "Conectando a base de datos...",
                    "Cargando transacciones...",
                    "Aplicando filtros...",
                    "Detectando duplicados...",
                    "Generando reporte...",
                    "Finalizando proceso..."
                ]
                
                for i, stage in enumerate(stages):
                    progress = (i + 1) * 100 // len(stages)
                    progress_bar.progress(progress)
                    status_text.text(stage)
                    time.sleep(0.5)
                
                st.success("✅ Validación completada exitosamente")
    
    # Resultados de la validación
    st.markdown("---")
    st.subheader("📋 Resultados de la Validación")
    
    # Tabs para diferentes vistas de resultados
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumen", "🔍 Duplicados", "📈 Análisis", "📄 Exportar"])
    
    with tab1:
        # Métricas principales
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.metric(
                "Total Procesadas",
                "15,847",
                help="Total de transacciones analizadas"
            )
        
        with col_res2:
            st.metric(
                "Duplicados Detectados",
                "89",
                delta="-89",
                delta_color="inverse",
                help="Posibles dobles cobros identificados"
            )
        
        with col_res3:
            st.metric(
                "Tasa de Duplicación",
                "0.56%",
                delta="-0.12%",
                delta_color="inverse"
            )
        
        with col_res4:
            st.metric(
                "Ahorro Estimado",
                "$4,450,000",
                delta="450,000"
            )
        
        # Gráfico de distribución
        st.subheader("📊 Distribución por Categoría")
        
        chart_data = pd.DataFrame({
            'Categoría': ['Cat I', 'Cat II', 'Cat III', 'Cat IV', 'Cat V'],
            'Transacciones': [8500, 3200, 2100, 1800, 247],
            'Duplicados': [45, 18, 12, 11, 3]
        })
        
        st.bar_chart(chart_data.set_index('Categoría'))
    
    with tab2:
        st.subheader("🔍 Detalle de Duplicados Detectados")
        
        # Tabla de duplicados simulada
        duplicados_data = {
            'ID': ['PJ001', 'PJ002', 'PJ003', 'PJ004', 'PJ005'],
            'Placa': ['ABC123', 'XYZ789', 'DEF456', 'GHI789', 'JKL012'],
            'Peaje': ['Autopista Norte', 'Bogotá-Girardot', 'Autopista Norte', 'Medellín-Bogotá', 'Cali-Buenaventura'],
            'Fecha': ['2024-01-15', '2024-01-15', '2024-01-16', '2024-01-16', '2024-01-17'],
            'Hora_1': ['10:30:15', '14:20:30', '09:15:45', '16:45:20', '11:30:10'],
            'Hora_2': ['10:32:18', '14:22:15', '09:17:30', '16:47:05', '11:32:25'],
            'Categoría': ['I', 'II', 'I', 'III', 'I'],
            'Monto': ['$8,500', '$15,200', '$8,500', '$22,800', '$8,500'],
            'Diferencia': ['2m 3s', '1m 45s', '1m 45s', '1m 45s', '2m 15s'],
            'Estado': ['Pendiente', 'Revisado', 'Pendiente', 'Confirmado', 'Pendiente']
        }
        
        df_duplicados = pd.DataFrame(duplicados_data)
        
        # Filtros para la tabla
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            filtro_estado = st.selectbox(
                "Filtrar por estado",
                ["Todos", "Pendiente", "Revisado", "Confirmado"]
            )
        
        with col_filter2:
            filtro_peaje = st.selectbox(
                "Filtrar por peaje",
                ["Todos"] + list(df_duplicados['Peaje'].unique())
            )
        
        with col_filter3:
            filtro_categoria = st.selectbox(
                "Filtrar por categoría",
                ["Todas"] + list(df_duplicados['Categoría'].unique())
            )
        
        # Aplicar filtros
        df_filtered = df_duplicados.copy()
        if filtro_estado != "Todos":
            df_filtered = df_filtered[df_filtered['Estado'] == filtro_estado]
        if filtro_peaje != "Todos":
            df_filtered = df_filtered[df_filtered['Peaje'] == filtro_peaje]
        if filtro_categoria != "Todas":
            df_filtered = df_filtered[df_filtered['Categoría'] == filtro_categoria]
        
        st.dataframe(df_filtered, use_container_width=True)
        
        # Acciones en lote
        st.subheader("⚡ Acciones en Lote")
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("✅ Marcar como Revisados"):
                st.success("Registros marcados como revisados")
        
        with col_action2:
            if st.button("❌ Marcar como Falsos Positivos"):
                st.info("Registros marcados como falsos positivos")
        
        with col_action3:
            if st.button("🔄 Revalidar Seleccionados"):
                st.info("Revalidación iniciada")
    
    with tab3:
        st.subheader("📈 Análisis Detallado")
        
        # Análisis temporal
        col_analysis1, col_analysis2 = st.columns(2)
        
        with col_analysis1:
            st.write("**Distribución Horaria de Duplicados**")
            
            # Datos simulados para el gráfico
            horas = list(range(0, 24))
            duplicados_por_hora = np.random.poisson(3, 24)
            
            hora_data = pd.DataFrame({
                'Hora': horas,
                'Duplicados': duplicados_por_hora
            })
            
            st.bar_chart(hora_data.set_index('Hora'))
        
        with col_analysis2:
            st.write("**Tendencia Semanal**")
            
            dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            duplicados_semana = [12, 15, 18, 14, 22, 8, 6]
            
            semana_data = pd.DataFrame({
                'Día': dias,
                'Duplicados': duplicados_semana
            })
            
            st.line_chart(semana_data.set_index('Día'))
        
        # Análisis por peaje
        st.write("**Ranking de Peajes con Mayor Incidencia**")
        
        peajes_ranking = pd.DataFrame({
            'Peaje': ['Autopista Norte', 'Bogotá-Girardot', 'Medellín-Bogotá', 'Cali-Buenaventura'],
            'Duplicados': [28, 22, 19, 15],
            'Porcentaje': [31.5, 24.7, 21.3, 16.9]
        })
        
        st.dataframe(peajes_ranking, use_container_width=True)
    
    with tab4:
        st.subheader("📄 Exportar Resultados")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            st.write("**Opciones de Exportación**")
            
            formato_export = st.selectbox(
                "Formato de archivo",
                ["Excel (.xlsx)", "CSV (.csv)", "PDF (.pdf)"]
            )
            
            incluir_graficos = st.checkbox("Incluir gráficos", value=True)
            incluir_resumen = st.checkbox("Incluir resumen ejecutivo", value=True)
            incluir_detalles = st.checkbox("Incluir detalles de duplicados", value=True)
            
            if st.button("📥 Generar Reporte", type="primary"):
                with st.spinner("Generando reporte..."):
                    time.sleep(2)
                    st.success("✅ Reporte generado exitosamente")
                    st.download_button(
                        "⬇️ Descargar Reporte",
                        data="Contenido del reporte simulado",
                        file_name=f"reporte_peajes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        with col_export2:
            st.write("**Programar Reportes Automáticos**")
            
            frecuencia = st.selectbox(
                "Frecuencia",
                ["Diario", "Semanal", "Mensual"]
            )
            
            email_destino = st.text_input("Email de destino")
            
            if st.button("📅 Programar Reporte"):
                if email_destino:
                    st.success(f"✅ Reporte {frecuencia.lower()} programado para {email_destino}")
                else:
                    st.error("❌ Por favor ingresa un email válido")

def validador_ezytec():
    st.markdown("""
    <div class="module-group">
        <h2 class="group-title">🔧 Validador Ezytec</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Volver al Inicio", key="back_ezytec"):
        st.session_state.current_module = 'home'
        st.rerun()
    
    st.markdown("---")
    
    # Información del sistema Ezytec
    st.info("""
    🔧 **Sistema Ezytec** - Validador especializado para tecnología de cobro automático
    
    Este módulo está diseñado específicamente para validar transacciones del sistema Ezytec,
    incluyendo validaciones de integridad, consistencia y detección de anomalías.
    """)
    
    # Layout principal
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Validación", "📊 Monitoreo", "⚙️ Configuración", "📋 Logs"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔍 Parámetros de Validación")
            
            # Tipo de validación Ezytec
            tipo_validacion_ezytec = st.selectbox(
                "Tipo de validación Ezytec",
                [
                    "Validación de Integridad",
                    "Detección de Anomalías",
                    "Verificación de Protocolos",
                    "Análisis de Rendimiento",
                    "Validación Completa"
                ]
            )
            
            # Configuración de dispositivos
            dispositivos = st.multiselect(
                "Dispositivos Ezytec a validar",
                [
                    "EZY-001 (Peaje Norte)",
                    "EZY-002 (Peaje Sur)",
                    "EZY-003 (Estación Central)",
                    "EZY-004 (Terminal)",
                    "EZY-005 (Backup)"
                ],
                default=["EZY-001 (Peaje Norte)"]
            )
            
            # Rango de fechas
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                fecha_inicio_ez = st.date_input("Fecha inicio", key="ez_start")
            with col_date2:
                fecha_fin_ez = st.date_input("Fecha fin", key="ez_end")
            
            # Configuración avanzada
            with st.expander("⚙️ Configuración Avanzada Ezytec"):
                protocolo_version = st.selectbox(
                    "Versión del protocolo",
                    ["v2.1", "v2.0", "v1.9", "Todas"]
                )
                
                nivel_detalle = st.slider(
                    "Nivel de detalle del análisis",
                    1, 5, 3,
                    help="1=Básico, 5=Exhaustivo"
                )
                
                incluir_diagnosticos = st.checkbox("Incluir diagnósticos de hardware", value=True)
                validar_checksums = st.checkbox("Validar checksums de datos", value=True)
        
        with col2:
            st.subheader("📁 Carga de Datos")
            
            # Carga de archivos específicos de Ezytec
            uploaded_file_ez = st.file_uploader(
                "Archivo de logs Ezytec",
                type=['log', 'txt', 'csv', 'json'],
                help="Formatos: .log, .txt, .csv, .json",
                key="ezytec_file"
            )
            
            if uploaded_file_ez:
                st.success(f"✅ Archivo cargado: {uploaded_file_ez.name}")
                
                # Mostrar información del archivo
                file_info = {
                    "Nombre": uploaded_file_ez.name,
                    "Tamaño": f"{uploaded_file_ez.size / 1024:.2f} KB",
                    "Tipo": uploaded_file_ez.type
                }
                
                for key, value in file_info.items():
                    st.text(f"{key}: {value}")
            
            st.markdown("---")
            
            # Estado del sistema
            st.subheader("🔋 Estado del Sistema")
            
            col_status1, col_status2 = st.columns(2)
            
            with col_status1:
                st.metric("Dispositivos Online", "4/5", delta="1")
                st.metric("Última Sincronización", "2 min")
            
            with col_status2:
                st.metric("Transacciones/Hora", "1,247", delta="47")
                st.metric("Tasa de Error", "0.02%", delta="-0.01%")
            
            # Botón de validación
            if st.button("🚀 EJECUTAR VALIDACIÓN EZYTEC", type="primary", use_container_width=True):
                # Simulación de validación Ezytec
                progress_container = st.container()
                
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    ezytec_stages = [
                        "Conectando a dispositivos Ezytec...",
                        "Verificando protocolos de comunicación...",
                        "Analizando logs de transacciones...",
                        "Validando integridad de datos...",
                        "Detectando anomalías del sistema...",
                        "Generando reporte de validación...",
                        "Proceso completado"
                    ]
                    
                    for i, stage in enumerate(ezytec_stages):
                        progress = (i + 1) * 100 // len(ezytec_stages)
                        progress_bar.progress(progress)
                        status_text.text(stage)
                        time.sleep(0.7)
                    
                    st.success("✅ Validación Ezytec completada exitosamente")
                    
                    # Resultados de la validación
                    st.subheader("📊 Resultados de Validación Ezytec")
                    
                    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                    
                    with col_res1:
                        st.metric("Registros Validados", "8,547")
                    with col_res2:
                        st.metric("Errores Detectados", "3", delta="-2")
                    with col_res3:
                        st.metric("Integridad", "99.97%", delta="0.02%")
                    with col_res4:
                        st.metric("Rendimiento", "Óptimo", delta="Estable")
    
    with tab2:
        st.subheader("📊 Monitoreo en Tiempo Real")
        
        # Dashboard de monitoreo
        col_mon1, col_mon2, col_mon3 = st.columns(3)
        
        with col_mon1:
            st.metric("🔌 Dispositivos Activos", "4/5", delta="0")
            st.metric("📡 Señal Promedio", "98%", delta="2%")
        
        with col_mon2:
            st.metric("⚡ Transacciones/Min", "87", delta="12")
            st.metric("🔄 Sincronización", "OK", delta="Estable")
        
        with col_mon3:
            st.metric("🛡️ Seguridad", "Activa", delta="Normal")
            st.metric("💾 Almacenamiento", "78%", delta="5%")
        
        # Gráfico de monitoreo en tiempo real
        st.subheader("📈 Actividad en Tiempo Real")
        
        # Simulación de datos en tiempo real
        import numpy as np
        
        tiempo = pd.date_range(start='2024-01-01 00:00', periods=24, freq='H')
        transacciones = np.random.poisson(80, 24) + np.sin(np.arange(24) * np.pi / 12) * 20 + 60
        errores = np.random.poisson(2, 24)
        
        monitoring_data = pd.DataFrame({
            'Hora': tiempo.hour,
            'Transacciones': transacciones.astype(int),
            'Errores': errores
        })
        
        st.line_chart(monitoring_data.set_index('Hora'))
        
        # Alertas del sistema
        st.subheader("🚨 Alertas del Sistema")
        
        alertas = [
            {"Tipo": "⚠️ Advertencia", "Mensaje": "Dispositivo EZY-005 desconectado", "Tiempo": "Hace 15 min"},
            {"Tipo": "ℹ️ Info", "Mensaje": "Actualización de firmware disponible", "Tiempo": "Hace 2 horas"},
            {"Tipo": "✅ Resuelto", "Mensaje": "Problema de conectividad solucionado", "Tiempo": "Hace 4 horas"}
        ]
        
        for alerta in alertas:
            st.info(f"{alerta['Tipo']} {alerta['Mensaje']} - {alerta['Tiempo']}")
    
    with tab3:
        st.subheader("⚙️ Configuración del Sistema Ezytec")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            st.write("**Configuración de Dispositivos**")
            
            # Configuración de cada dispositivo
            for i in range(1, 6):
                with st.expander(f"🔧 Dispositivo EZY-00{i}"):
                    st.text_input(f"IP Address", value=f"192.168.1.{100+i}", key=f"ip_{i}")
                    st.selectbox(f"Estado", ["Activo", "Inactivo", "Mantenimiento"], key=f"status_{i}")
                    st.slider(f"Timeout (seg)", 1, 30, 10, key=f"timeout_{i}")
        
        with col_config2:
            st.write("**Configuración General**")
            
            intervalo_sync = st.number_input(
                "Intervalo de sincronización (minutos)",
                min_value=1,
                max_value=60,
                value=5
            )
            
            max_reintentos = st.number_input(
                "Máximo reintentos de conexión",
                min_value=1,
                max_value=10,
                value=3
            )
            
            nivel_log = st.selectbox(
                "Nivel de logging",
                ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                index=1
            )
            
            backup_automatico = st.checkbox("Backup automático", value=True)
            
            if backup_automatico:
                frecuencia_backup = st.selectbox(
                    "Frecuencia de backup",
                    ["Cada hora", "Cada 6 horas", "Diario", "Semanal"]
                )
            
            # Botones de configuración
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("💾 Guardar Configuración"):
                    st.success("✅ Configuración guardada")
            
            with col_btn2:
                if st.button("🔄 Restaurar Defaults"):
                    st.info("ℹ️ Configuración restaurada")
    
    with tab4:
        st.subheader("📋 Logs del Sistema")
        
        # Filtros para logs
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            filtro_nivel = st.selectbox(
                "Nivel de log",
                ["Todos", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            )
        
        with col_filter2:
            filtro_dispositivo = st.selectbox(
                "Dispositivo",
                ["Todos", "EZY-001", "EZY-002", "EZY-003", "EZY-004", "EZY-005"]
            )
        
        with col_filter3:
            filtro_fecha = st.date_input("Fecha de logs", value=date.today())
        
        # Simulación de logs
        logs_data = [
            {"Timestamp": "2024-01-15 10:30:15", "Nivel": "INFO", "Dispositivo": "EZY-001", "Mensaje": "Transacción procesada correctamente - ID: TXN001234"},
            {"Timestamp": "2024-01-15 10:30:18", "Nivel": "DEBUG", "Dispositivo": "EZY-002", "Mensaje": "Heartbeat recibido - Status: OK"},
            {"Timestamp": "2024-01-15 10:30:22", "Nivel": "WARNING", "Dispositivo": "EZY-005", "Mensaje": "Timeout en conexión - Reintentando..."},
            {"Timestamp": "2024-01-15 10:30:25", "Nivel": "ERROR", "Dispositivo": "EZY-003", "Mensaje": "Error en validación de checksum - Datos: 0xABCD1234"},
            {"Timestamp": "2024-01-15 10:30:30", "Nivel": "INFO", "Dispositivo": "EZY-001", "Mensaje": "Backup automático completado - Archivo: backup_20240115.log"},
            {"Timestamp": "2024-01-15 10:30:35", "Nivel": "CRITICAL", "Dispositivo": "EZY-004", "Mensaje": "Falla crítica en hardware - Requiere intervención inmediata"}
        ]
        
        # Mostrar logs en formato tabla
        df_logs = pd.DataFrame(logs_data)
        
        # Aplicar filtros
        if filtro_nivel != "Todos":
            df_logs = df_logs[df_logs['Nivel'] == filtro_nivel]
        if filtro_dispositivo != "Todos":
            df_logs = df_logs[df_logs['Dispositivo'] == filtro_dispositivo]
        
        # Colorear logs según nivel
        def color_logs(val):
            if val == 'CRITICAL':
                return 'background-color: #ffebee; color: #c62828'
            elif val == 'ERROR':
                return 'background-color: #fff3e0; color: #ef6c00'
            elif val == 'WARNING':
                return 'background-color: #fffde7; color: #f57f17'
            elif val == 'INFO':
                return 'background-color: #e8f5e8; color: #2e7d32'
            elif val == 'DEBUG':
                return 'background-color: #f3e5f5; color: #7b1fa2'
            return ''
        
        styled_df = df_logs.style.applymap(color_logs, subset=['Nivel'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Opciones de exportación de logs
        st.subheader("📤 Exportar Logs")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            formato_log = st.selectbox(
                "Formato de exportación",
                ["CSV", "JSON", "TXT"]
            )
        
        with col_export2:
            if st.button("📥 Exportar Logs"):
                st.success("✅ Logs exportados exitosamente")
                st.download_button(
                    "⬇️ Descargar Archivo",
                    data="Logs simulados del sistema Ezytec",
                    file_name=f"ezytec_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato_log.lower()}",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
