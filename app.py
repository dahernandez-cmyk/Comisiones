import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página ancha para que se vea como tu imagen
st.set_page_config(page_title="Dashboard Comisiones", layout="wide")

# Estilo CSS personalizado para el encabezado azul
st.markdown("""
    <style>
    .main-header {
        background-color: #003366;
        padding: 20px;
        color: white;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    </style>
    <div class="main-header">
        <h1>Dashboard de Productividad Comercial</h1>
        <p>Información digital para control, claridad y visibilidad</p>
    </div>
    """, unsafe_allow_html=True)

# Ruta del archivo (usando r para evitar errores de barras en Windows)
ruta_excel = r"G:\Unidades compartidas\dahernandez\info 2026\Documentos - copia\COMISIONES\COMISIONES 2026\COMISIONES 2026 ABR.xlsx"

@st.cache_data
def cargar_datos():
    # Nota: Asegúrate de tener instalada la librería openpyxl
    return pd.read_excel(ruta_excel)

df = cargar_datos()

# Filtros en el Sidebar
st.sidebar.header("FILTROS")
regional = st.sidebar.multiselect("Regional", options=df['REGIONAL'].unique(), default=df['REGIONAL'].unique())

# Filtrar datos
df_filtrado = df[df['REGIONAL'].isin(regional)]

# Crear columnas para las gráficas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Productividad por Cargo")
    fig_bar = px.bar(df_filtrado, x='CARGO', y='PRODUCTIVIDAD', color='CARGO', template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Evolución Mensual")
    fig_line = px.line(df_filtrado, x='MES', y='PRODUCTIVIDAD', markers=True, template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

**Para ejecutarlo:**
1. Guarda el código en un archivo llamado `tablero.py`.
2. En tu terminal escribe: `streamlit run tablero.py`.

#¿Te gustaría que ajustemos algún gráfico específico basado en las columnas reales de tu Excel?