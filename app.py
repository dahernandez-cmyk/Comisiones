import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Modo Ancho)
st.set_page_config(
    page_title="Dashboard de Productividad Comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ENCABEZADO ESTÉTICO PERSONALIZADO (Estilo Azul de Coninsa)
st.markdown("""
    <style>
    .main-header {
        background-color: #003366; /* Azul profundo corporativo */
        padding: 20px 30px;
        color: white;
        text-align: left;
        border-radius: 8px;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 600;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #e2e8f0;
        opacity: 0.9;
    }
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    </style>
    
    <div class="main-header">
        <h1>Dashboard de Productividad Comercial</h1>
        <p>Usamos lo digital para darte control, claridad y velocidad</p>
    </div>
    """, unsafe_allow_html=True)

# 3. ENLACE REAL DE TU GOOGLE SHEETS
URL_PUBLICACION_WEB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTF5HvCvAC9LgTD_uj5nRugoRBX_oc3bo61IcT_uEygW2KPWNMVSahM3TJEvdOHBoFnap1rA0IAtspT/pub?gid=0&single=true&output=csv"

# Función con caché para cargar los datos de forma rápida
@st.cache_data(ttl=600)  # Se actualiza automáticamente cada 10 minutos
def cargar_datos(url):
    return pd.read_csv(url)

# 4. PROCESAMIENTO Y CONTROL DE ERRORES
try:
    df = cargar_datos(URL_PUBLICACION_WEB)
    
    # Limpieza estándar de nombres de columnas (elimina espacios ocultos si los hay)
    df.columns = df.columns.str.strip()

    # 5. CONFIGURACIÓN DE LOS FILTROS EN LA BARRA LATERAL (SIDEBAR)
    st.sidebar.markdown("### **PARÁMETROS DE FILTRADO**")
    st.sidebar.markdown("---")
    
    # Filtro de Regional
    if 'REGIONAL' in df.columns:
        opciones_regionales = sorted(df['REGIONAL'].dropna().unique())
        regionales_seleccionadas = st.sidebar.multiselect(
            "REGIONAL",
            options=opciones_regionales,
            default=opciones_regionales  # Por defecto selecciona todas
        )
        df_filtrado = df[df['REGIONAL'].isin(regionales_seleccionadas)]
    else:
        st.sidebar.error("No se encontró la columna 'REGIONAL'")
        df_filtrado = df
    
    # Filtro de Mes
    if 'MES' in df.columns:
        opciones_meses = df['MES'].dropna().unique()
        if len(opciones_meses) > 0:
            mes_seleccionado = st.sidebar.selectbox("MES", options=opciones_meses)
            df_filtrado = df_filtrado[df_filtrado['MES'] == mes_seleccionado]
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Proyecto: Comisiones 2026 | Usuario: dahernandez")

    # 6. DISEÑO DE LAS GRÁFICAS EN COLUMNAS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 **Productividad por cargo**")
        if 'CARGO' in df_filtrado.columns and 'PRODUCTIVIDAD' in df_filtrado.columns:
            fig_bar = px.bar(
                df_filtrado, 
                x='CARGO', 
                y='PRODUCTIVIDAD',
                color='CARGO',
                color_discrete_sequence=px.colors.qualitative.Prism,
                template="plotly_white"
            )
            fig_bar.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Verifica que existan las columnas 'CARGO' y 'PRODUCTIVIDAD' en tu archivo.")

    with col2:
        st.markdown("### 📈 **Evolución mensual de productividad**")
        if 'MES' in df_filtrado.columns and 'PRODUCTIVIDAD' in df_filtrado.columns:
            fig_line = px.line(
                df_filtrado, 
                x='MES', 
                y='PRODUCTIVIDAD', 
                markers=True,
                template="plotly_white"
            )
            fig_line.update_traces(line_color='#003366', marker=dict(size=8, color='#008080'))
            fig_line.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Se requiere la columna 'MES' y 'PRODUCTIVIDAD' para mostrar la evolución.")

    # 7. TABLA DE DATOS INFERIOR
    with st.expander("👀 Ver registros detallados del filtro actual"):
        st.dataframe(df_filtrado, use_container_width=True)

except Exception as error_conexion:
    # Si la seguridad de Coninsa bloquea por completo la lectura externa
    st.error("### 🔒 Acceso Restringido por la Organización")
    st.warning(
        "El servidor de Streamlit Cloud no ha podido consumir el enlace debido a las políticas estrictas "
        "de Google Workspace de Coninsa Ramon H S.A."
    )
    st.markdown("""
    **¿Qué hacer si ves este error?**
    Dado que tu repositorio de GitHub es público, no puedes meter el Excel allí. La única alternativa corporativa es:
    1. Cambiar tu repositorio de GitHub a **Privado**.
    2. Guardar el archivo `.xlsx` de Excel en la misma carpeta de tu código.
    3. Cambiar la línea de lectura por: `df = pd.read_excel('Nombre_Tu_Archivo.xlsx')` y subirlo todo a GitHub.
    """)
    with st.expander("Detalles técnicos del error"):
        st.code(str(error_conexion))