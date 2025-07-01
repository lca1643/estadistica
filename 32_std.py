# app.py (versión para Media y Desviación Estándar)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Dispersión",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Dispersión")
    st.subheader("3.2 Desviación Estándar")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna = None
    color = '#0288d1' # Un color azul diferente para esta app

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.header("2. Seleccionar Variable y Opciones")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if not numeric_cols:
            st.error("El archivo no contiene columnas numéricas.")
            st.stop()
        
        columna = st.selectbox(
            "Elige la columna para analizar:",
            options=numeric_cols
        )
        
        color = st.color_picker(
            "Elige un color para el histograma:",
            value='#0288d1'
        )

# --- 3. Panel Principal ---
st.title("📏 Análisis de Media y Desviación Estándar")
st.write(
    "Esta herramienta visualiza cómo se distribuyen tus datos alrededor de la media, "
    "marcando el rango de una desviación estándar."
)

if uploaded_file is None:
    st.warning("Por favor, sube un archivo para comenzar.")
    st.stop()

if df is None or columna is None or columna not in df.columns:
    st.info("Por favor, selecciona una columna en el panel de la izquierda.")
    st.stop()

# --- 4. Lógica de Cálculo y Visualización ---
st.markdown("---")
st.header(f"Análisis de la columna: '{columna}'")

datos = df[columna].dropna()

if datos.empty or not pd.api.types.is_numeric_dtype(datos):
    st.warning("La columna seleccionada no contiene datos numéricos válidos.")
else:
    # --- Cálculo de Media y Desviación Estándar ---
    media = datos.mean()
    desviacion_estandar = datos.std()
    
    # --- Mostrar las métricas ---
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Media", value=f"{media:.2f}")
    with col2:
        st.metric(label=f"Desviación Estándar (DE)", value=f"{desviacion_estandar:.2f}")

    # --- Visualización en Pestañas ---
    tab_grafico, tab_datos = st.tabs(["📈 Histograma", "📄 Estadísticas Detalladas"])

    with tab_grafico:
        st.subheader(f"Histograma con Media y +/- 1 Desviación Estándar")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(datos, bins='auto', edgecolor='black', alpha=0.7, color=color)
        
        # --- Añadir las líneas verticales ---
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2.5, label=f'Media = {media:.2f}')
        ax.axvline(media + desviacion_estandar, color='green', linestyle='dotted', linewidth=2, label=f'+1 DE ({media + desviacion_estandar:.2f})')
        ax.axvline(media - desviacion_estandar, color='green', linestyle='dotted', linewidth=2, label=f'-1 DE ({media - desviacion_estandar:.2f})')
        
        # Personalizar
        ax.set_title(f'Distribución de {columna}')
        ax.set_xlabel(columna)
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # --- Botón de descarga ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf,
            file_name=f"histograma_dispersion_{columna}.png",
            mime="image/png"
        )
        
        st.pyplot(fig)

    with tab_datos:
        st.subheader("Resumen Estadístico Completo")
        
        stats_csv = datos.describe().to_csv().encode('utf-8')
        st.download_button(
            label="📥 Descargar Estadísticas (CSV)",
            data=stats_csv,
            file_name=f"estadisticas_{columna}.csv",
            mime="text/csv"
        )
        st.dataframe(datos.describe())