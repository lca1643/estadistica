# app.py (versión con Media, Mediana, Moda y Tabla de Frecuencias)

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
    st.subheader("3.1 Media, Mediana y Moda")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna = None
    color = '#3498db'
    num_bins = 15 # Valor por defecto para los bins

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
        
        # Añadir control para el número de bins en la barra lateral
        num_bins = st.number_input("Número de Bins para el Histograma:", min_value=1, max_value=100, value=15, step=1)
        
        color = st.color_picker(
            "Elige un color para el histograma:",
            value='#3498db'
        )

# --- 3. Panel Principal ---
st.title("⚖️ Análisis de Media, Mediana y Moda")
st.write(
    "Esta herramienta calcula y visualiza las tres medidas de tendencia central de una variable numérica."
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
    st.warning("La columna seleccionada no tiene datos numéricos válidos.")
else:
    # --- Cálculo de Medidas de Tendencia Central ---
    media = datos.mean()
    mediana = datos.median()
    modas = datos.mode().tolist()
    
    # --- Mostrar las métricas ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"Media", value=f"{media:.2f}")
    with col2:
        st.metric(label=f"Mediana", value=f"{mediana:.2f}")
    with col3:
        if len(modas) == len(datos) and len(modas) > 1:
            moda_texto = "No hay moda"
        else:
            moda_texto = ", ".join([f"{m:.2f}" for m in modas])
        st.metric(label="Moda(s)", value=moda_texto)

    # --- Cálculo de la Tabla de Frecuencias ---
    frecuencias, bins = np.histogram(datos, bins=num_bins)
    marcas_clase = (bins[:-1] + bins[1:]) / 2
    
    tabla_frecuencias = pd.DataFrame({
        'Intervalo': [f"[{bins[i]:.2f} - {bins[i+1]:.2f})" for i in range(len(frecuencias))],
        'Marca de Clase': marcas_clase.round(2),
        'Frecuencia Absoluta': frecuencias,
        'Frecuencia Relativa (%)': (frecuencias / frecuencias.sum() * 100).round(2)
    })
    tabla_frecuencias.iloc[-1, 0] = f"[{bins[-2]:.2f} - {bins[-1]:.2f}]"
    tabla_frecuencias.index = np.arange(1, len(tabla_frecuencias) + 1)
    tabla_frecuencias.index.name = "N"

    # --- Visualización en Pestañas ---
    tab_grafico, tab_datos = st.tabs(["📈 Histograma", "📄 Tabla y Estadísticas"])

    with tab_grafico:
        st.subheader(f"Histograma con Medidas de Tendencia Central")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(datos, bins=num_bins, edgecolor='black', alpha=0.7, color=color)
        
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2.5, label=f'Media = {media:.2f}')
        ax.axvline(mediana, color='green', linestyle='solid', linewidth=2.5, label=f'Mediana = {mediana:.2f}')
        
        if moda_texto != "No hay moda":
            for i, m in enumerate(modas):
                ax.axvline(m, color='purple', linestyle='dotted', linewidth=2.5, label=f'Moda = {m:.2f}')
        
        ax.set_title(f'Distribución de {columna}')
        ax.set_xlabel(columna)
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf,
            file_name=f"histograma_tendencia_central_{columna}.png",
            mime="image/png"
        )
        st.pyplot(fig)

    with tab_datos:
        # --- AÑADIDO: Mostrar la Tabla de Frecuencias ---
        st.subheader("Tabla de Frecuencias")
        
        # Botón de descarga para la tabla de frecuencias
        csv_tabla = tabla_frecuencias.to_csv(index=True).encode('utf-8')
        st.download_button(
            label="📥 Descargar Tabla de Frecuencias (CSV)",
            data=csv_tabla,
            file_name=f"tabla_frecuencias_{columna}.csv",
            mime="text/csv",
        )
        st.dataframe(tabla_frecuencias)

        # Expander para las estadísticas descriptivas
        with st.expander("Ver Resumen Estadístico Completo"):
            stats_csv = datos.describe().to_csv().encode('utf-8')
            st.download_button(
                label="📥 Descargar Estadísticas (CSV)",
                data=stats_csv,
                file_name=f"estadisticas_{columna}.csv",
                mime="text/csv",
                key=f"download-stats-{columna}" # Clave única para el botón
            )
            st.dataframe(datos.describe())