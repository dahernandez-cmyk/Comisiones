import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Modo Ancho para vista tipo Tablero)
st.set_page_config(
    page_title="Dashboard de Productividad Comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ENCABEZADO ESTÉTICO PERSONALIZADO (Mismo estilo azul de tu imagen)
st.markdown("""
    <style>
    /* Estilo para el contenedor principal del título */
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
    /* Ajustes estéticos para las tarjetas laterales de Streamlit */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    </style>
    
    <div class="main-header">
        <h1>Dashboard de Productividad Comercial</h1>
        <p>Usamos lo digital para darte control, claridad y velocidad</p>
    </div>
    """, unsafe_allow_html=True)

# 3. ENLACE DE CONEXIÓN A GOOGLE SHEETS
# Reemplaza TODO este texto de ejemplo por el link que obtuviste en "Publicar en la web" -> formato .csv
URL_PUBLICACION_WEB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTF5HvCvAC9LgTD_uj5nRugoRBX_oc3bo61IcT_uEygW2KPWNMVSahM3TJEvdOHBoFnap1rA0IAtspT/pub?gid=0&single=true&output=csv"

# Función con caché para cargar los datos de forma rápida
@st.cache_data(ttl=600)  # Se actualiza automáticamente cada 10 minutos
def cargar_datos(url):
    # Lee el archivo CSV generado por la publicación web de Google
    return pd.read_csv(url)

# 4. CONTROL DE FLUJO Y RENDERIZADO DEL TABLERO
try:
    # Intentamos conectarnos y leer el archivo
    df = cargar_datos(URL_PUBLICACION_WEB)
    
    # Limpieza estándar de nombres de columnas (elimina espacios ocultos si los hay)
    df.columns = df.columns.str.strip()

    # 5. CONFIGURACIÓN DE LOS FILTROS EN LA BARRA LATERAL (SIDEBAR)
    st.sidebar.markdown("### **PARÁMETROS DE FILTRADO**")
    st.sidebar.markdown("---")
    
    # Filtro de Regional (Multiselect para poder elegir varias o todas a la vez)
    opciones_regionales = sorted(df['REGIONAL'].dropna().unique())
    regionales_seleccionadas = st.sidebar.multiselect(
        "REGIONAL",
        options=opciones_regionales,
        default=opciones_regionales  # Por defecto selecciona todas como en "Nacional"
    )
    
    # Filtro de Mes
    opciones_meses = df['MES'].dropna().unique() if 'MES' in df.columns else []
    if len(opciones_meses) > 0:
        mes_seleccionado = st.sidebar.selectbox("MES", options=opciones_meses)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Proyecto: Comisiones 2026 | Usuario: dahernandez")

    # 6. APLICAR FILTROS A LOS DATOS
    df_filtrado = df[df['REGIONAL'].isin(regionales_seleccionadas)]
    if len(opciones_meses) > 0:
        df_filtrado = df_filtrado[df_filtrado['MES'] == mes_seleccionado]

    # 7. DISEÑO DE LAS GRÁFICAS EN COLUMNAS (Estructura 50/50 como tu captura)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 **Productividad por cargo**")
        # Gráfico de barras interactivo
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

    with col2:
        st.markdown("### 📈 **Evolución mensual de productividad**")
        # Gráfico de líneas/tendencias
        if 'MES' in df_filtrado.columns:
            fig_line = px.line(
                df_filtrado, 
                x='MES', 
                y='PRODUCTIVIDAD', 
                markers=True,
                line_shape="linear",
                template="plotly_white"
            )
            # Pintamos la línea con el azul corporativo
            fig_line.update_traces(line_color='#003366', marker=dict(size=8, color='#008080'))
            fig_line.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Añade una columna llamada 'MES' en tu Google Sheets para activar el gráfico de evolución.")

    # 8. TABLA DE DATOS INFERIOR (Opcional, para verificar lo filtrado)
    with st.expander("👀 Ver registros detallados del filtro actual"):
        st.dataframe(df_filtrado, use_container_width=True)

except Exception as error_conexion:
    # Mensaje elegante si las políticas de seguridad de Coninsa bloquean la URL en la nube
    st.error("### 🔒 Acceso Restringido por la Organización")
    st.warning(
        "El servidor de Streamlit Cloud no ha podido saltarse los sistemas de autenticación de tu cuenta corporativa. "
        "Esto significa que la seguridad de **Coninsa Ramon H S.A.** está funcionando perfectamente protegiendo tus datos."
    )
    
    st.markdown("""
    **¿Cómo solucionarlo si te aparece este error?**
    1. Si no puedes cambiar las políticas del Google Sheets, la única alternativa es cambiar tu repositorio de GitHub a **Privado**.
    2. Guarda tu archivo de Excel con el nombre `COMISIONES_ABR_2026.xlsx` dentro de la carpeta del proyecto.
    3. Cambia la línea de carga en este código por: 
       `df = pd.read_excel('COMISIONES_ABR_2026.xlsx')`
    4. Sube el Excel a tu repositorio privado. Al ser privado, tus datos estarán 100% seguros y Streamlit podrá leerlos sin pedirle permisos a Google.
    """)
    
    # Imprime el error técnico real abajo de forma discreta para auditoría
    with st.expander("Detalles técnicos del error"):
        st.code(str(error_conexion))