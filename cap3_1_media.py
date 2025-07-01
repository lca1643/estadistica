# app.py (versión para analizar UNA variable a la vez, con selector de color)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Calculadora de Media",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Tendencia Central")
    st.subheader("3.1 Media")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    # Inicializar df fuera del if para que exista en el scope
    df = None
    columna = None
    color = '#3498db' # Color por defecto

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.header("2. Seleccionar Variable y Color")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if not numeric_cols:
            st.error("El archivo no contiene columnas numéricas.")
            st.stop()
        
        # --- CAMBIO 1: Reemplazar multiselect por selectbox ---
        columna = st.selectbox(
            "Elige la columna para analizar:",
            options=numeric_cols
        )
        
        # --- CAMBIO 2: Añadir el selector de color ---
        color = st.color_picker(
            "Elige un color para el histograma:",
            value='#3498db' # Valor inicial del color
        )

# --- 3. Panel Principal ---
st.title("⚖️ Calculadora de Media y Visualizador de Distribución")

if uploaded_file is None:
    st.warning("Por favor, sube un archivo para comenzar.")
    st.stop()

# Verificar si la selección de columna se hizo correctamente
if df is None or columna is None:
    st.info("Por favor, selecciona una columna en el panel de la izquierda.")
    st.stop()

# --- 4. Lógica de Cálculo y Visualización (SIN BUCLE) ---
st.markdown("---")
st.header(f"Análisis de la columna: '{columna}'")

# Preparar los datos de la columna seleccionada
datos = df[columna].dropna()

if datos.empty or not pd.api.types.is_numeric_dtype(datos):
    st.warning("La columna seleccionada no contiene datos numéricos válidos.")
else:
    # --- Cálculo de la Media ---
    media = datos.mean()
    st.metric(label=f"Media de '{columna}'", value=f"{media:.2f}")

    # --- Visualización en Pestañas ---
    tab_grafico, tab_datos = st.tabs(["📈 Histograma", "📄 Estadísticas Detalladas"])

    with tab_grafico:
        st.subheader(f"Histograma de la Distribución")
        
        # --- Crear la figura del gráfico ---
        fig, ax = plt.subplots(figsize=(10, 5))
        # --- CAMBIO 3: Usar el color seleccionado ---
        ax.hist(datos, bins=15, edgecolor='black', alpha=0.7, color=color)
        
        # Añadir la línea de la media
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {media:.2f}')
        
        # Personalizar
        ax.set_title(f'Distribución de {columna}')
        ax.set_xlabel(columna)
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # --- Botón de descarga del gráfico ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf,
            file_name=f"histograma_media_{columna}.png",
            mime="image/png"
        )
        
        st.pyplot(fig)

    with tab_datos:
        st.subheader("Resumen Estadístico Completo")
        
        # Botón de descarga para las estadísticas
        stats_csv = datos.describe().to_csv().encode('utf-8')
        st.download_button(
            label="📥 Descargar Estadísticas (CSV)",
            data=stats_csv,
            file_name=f"estadisticas_{columna}.csv",
            mime="text/csv"
        )
        st.dataframe(datos.describe())