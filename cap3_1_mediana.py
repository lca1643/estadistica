# app.py (versión con Media y Mediana)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Medidas de Tendencia Central",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Tendencia Central")
    st.subheader("3.1 Media y Mediana")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna = None
    color = '#3498db'

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.header("2. Seleccionar Variable y Color")
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
            value='#3498db'
        )

# --- 3. Panel Principal ---
st.title("⚖️ Análisis de Media y Mediana")
st.write(
    "Esta herramienta calcula y visualiza la media y la mediana de una variable numérica, "
    "mostrando su posición en un histograma de distribución."
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
    # --- Cálculo de Media y Mediana ---
    media = datos.mean()
    mediana = datos.median()
    
    # Mostrar ambas métricas usando columnas para un layout limpio
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Media de '{columna}'", value=f"{media:.2f}")
    with col2:
        st.metric(label=f"Mediana de '{columna}'", value=f"{mediana:.2f}")

    # --- Visualización en Pestañas ---
    tab_grafico, tab_datos = st.tabs(["📈 Histograma", "📄 Estadísticas Detalladas"])

    with tab_grafico:
        st.subheader(f"Histograma con Media y Mediana")
        
        # --- Crear la figura del gráfico ---
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(datos, bins=15, edgecolor='black', alpha=0.7, color=color)
        
        # --- Añadir ambas líneas verticales ---
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2.5, label=f'Media = {media:.2f}')
        ax.axvline(mediana, color='green', linestyle='solid', linewidth=2.5, label=f'Mediana = {mediana:.2f}')
        
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
            file_name=f"histograma_media_mediana_{columna}.png",
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